# -*- coding: utf-8 -*-
"""Monta leads.db (SQLite) a partir do CSV do BigQuery + aplica score de capacidade."""
import csv, re, sqlite3, os, datetime, json

BASE = '/Users/touchbar/Codigos-Projetos/oraculo/analises-oraculo/prospeccao/odonto-DF'
PARTICAO = '2026-01-11'
FONTE = f'BigQuery basedosdados.br_me_cnpj (particao {PARTICAO})'
HOJE = datetime.date.today().isoformat()

rows  = list(csv.DictReader(open(f'{BASE}/data/odonto-df.csv')))
salas = {r['cnpj_basico']: int(r['n_cnpjs_mesma_sala']) for r in csv.DictReader(open('/tmp/sala.csv'))}

PORTE_DESC = {'1':'ME - Microempresa (ate R$360 mil/ano)',
              '3':'EPP - Empresa de Pequeno Porte (R$360 mil a R$4,8 mi/ano)',
              '5':'DEMAIS - Acima do teto do Simples (>R$4,8 mi/ano)',
              '' :'Nao informado'}
NAT_DESC = {'2062':'Sociedade Empresaria Limitada','2135':'Empresario (Individual)',
            '2240':'Sociedade Simples Limitada','2232':'Sociedade Simples Pura',
            '2054':'Sociedade Anonima Fechada','2127':'Sociedade em Conta de Participacao',
            '4014':'Empresa Individual de Resp. Limitada (EIRELI)','3999':'Associacao Privada',
            '3131':'Entidade Sindical','3077':'Servico Social Autonomo'}

TIPO_PAT = [
 ('radiologia_imagem',   r'\b(RADIOLOG|RADIOGRAF|IMAGEM|IMAGENS|RAIO ?X|RAIOS ?X|TOMOGRAF|DOCUMENTACAO ORTODONT|DIAGNOSTICO POR IMAGEM|CEFALOMETR)'),
 ('laboratorio_protese', r'\b(LABORATORIO|LAB\.? DE PROTESE|PROTESE DENTARIA LTDA)'),
 ('comercio_industria',  r'\b(COMERCIO|DISTRIBUIDORA|DISTRIBUICAO|ATACAD|IMPORTACAO|IMPORTADORA|DEPOSITO DENTARIO|INDUSTRIA|EQUIPAMENTOS ODONTOLOG|PRODUTOS ODONTOLOG|DENTAL SHOP)'),
 ('plano_convenio',      r'\b(PLANO ODONTOLOG|CONVENIO|ODONTOGROUP|UNIODONTO|OPERADORA|ASSISTENCIA ODONTOLOGICA LTDA|BENEFICIOS|AUTOGESTAO|SAUDE SUPLEMENTAR)'),
 ('ensino_treinamento',  r'\b(FACULDADE|ENSINO|CURSOS|CAPACITACAO|EDUCACIONAL|POS ?GRADUACAO|ESCOLA)')]

def classifica_tipo(txt):
    for nome, pat in TIPO_PAT:
        if re.search(pat, txt.upper()): return nome
    return 'clinica'

FRANQUIA = re.compile(r'\b(SORRIDENTS|ODONTOCOMPANY|ODONTO COMPANY|ORTHODONTIC|ORAL ?SIN|'
                      r'ORAL ?UNIC|ODONTOCLINIC\b|UNIODONTO|SOUSMILE|ODONTOGROUP|IMPERIAL ODONT|'
                      r'VITADENT|SIM ?ODONTO|DENTAL ?UNI)\b', re.I)

def brl(v):
    return 'R$ ' + f'{v:,.2f}'.replace(',','@').replace('.',',').replace('@','.')

def fmt_cnpj(c):
    c = (c or '').zfill(14)
    return f'{c[:2]}.{c[2:5]}.{c[5:8]}/{c[8:12]}-{c[12:]}'

def f(x, d=0.0):
    try: return float(x)
    except: return d
def i(x, d=0):
    try: return int(float(x))
    except: return d

# ---------------- score de capacidade (0-100), so proxies do CNPJ ----------------
def pts_porte(p):
    return {'3':32, '5':28, '1':5}.get(p, 14)
def pts_capital(c):
    for lim, p in ((500000,22),(200000,19),(100000,16),(50000,12),(20000,8),(5000,4),(0.01,2)):
        if c >= lim: return p
    return 0
def pts_unidades(n):
    if n >= 5: return 16
    if n >= 3: return 13
    if n == 2: return 9
    return 4
def pts_regime(s):
    return {'0':16, '1':6}.get(s, 9)   # '' = sem registro na tabela Simples
def pts_maturidade(m):
    for lim, p in ((180,14),(120,12),(60,9),(36,6)):
        if m >= lim: return p
    return 3

leads, sinais = [], []
for r in rows:
    cb = r['cnpj_basico']
    porte, cap = r['porte'], f(r['capital_social'])
    n_br  = i(r['n_unidades_br'], 1)
    n_ufs = i(r['n_ufs'], 1)
    idade = i(r['idade_meses'])
    simples = r['opcao_simples']
    n_sala   = salas.get(cb, 1)
    n_predio = i(r['n_cnpjs_no_endereco'], 1)
    fantasia = r['nome_fantasia'].strip()
    tem_contato = bool(r['telefone_1'] or r['telefone_2'] or r['email'])
    end_susp = n_sala >= 10
    franquia = bool(FRANQUIA.search(f"{fantasia} {r['razao_social']}"))
    tipo_negocio = classifica_tipo(f"{fantasia} {r['razao_social']}")
    rede_nac = n_ufs >= 3 or n_br >= 8

    comp = {'porte':pts_porte(porte), 'capital_social':pts_capital(cap),
            'n_unidades':pts_unidades(n_br), 'regime_tributario':pts_regime(simples),
            'maturidade':pts_maturidade(idade)}
    pen = {}
    if end_susp:      pen['endereco_suspeito'] = -20
    if not tem_contato: pen['sem_contato']     = -12
    if not fantasia:  pen['sem_nome_fantasia'] = -4
    if franquia:      pen['franquia']          = -10
    if tipo_negocio != 'clinica': pen[f'fora_do_icp_{tipo_negocio}'] = -12
    bruto = sum(comp.values()); nota = max(0, min(100, bruto + sum(pen.values())))

    desq, motivo = 0, None
    if rede_nac:
        desq, nota, motivo = 1, 0, f'Rede nacional/multi-UF ({n_br} unidades em {n_ufs} UFs) - decisao de marketing centralizada'

    conta = ' + '.join(f'{k} {v}' for k,v in comp.items()) + f' = {bruto}'
    if pen: conta += ' | penalidades: ' + ' '.join(f'{k} {v}' for k,v in pen.items())
    conta += f' | NOTA {nota}/100'

    endereco = ', '.join(x for x in [r['logradouro'], r['numero'], r['complemento'],
                                     r['bairro'], f"CEP {r['cep']}", 'Brasilia/DF'] if x)
    leads.append(dict(
        cnpj_basico=cb, cnpj=r['cnpj'], cnpj_formatado=fmt_cnpj(r['cnpj']),
        razao_social=r['razao_social'], nome_fantasia=fantasia,
        cnae=r['cnae_fiscal_principal'], cnae_descricao=r['cnae_descricao'],
        origem_recorte=r['origem_recorte'],
        municipio='Brasilia/DF', bairro=r['bairro'], endereco=endereco, cep=r['cep'],
        telefone=r['telefone_1'] or r['telefone_2'] or '', telefone_2=r['telefone_2'] if r['telefone_1'] else '',
        email=r['email'],
        data_inicio_atividade=r['data_inicio_atividade'], idade_meses=idade,
        porte=porte, porte_desc=PORTE_DESC.get(porte,'Nao informado'),
        natureza_juridica=r['natureza_juridica'],
        natureza_juridica_desc=NAT_DESC.get(r['natureza_juridica'],''),
        opcao_simples={'1':'Sim','0':'Nao'}.get(simples,'Sem registro'),
        capital_social=cap, n_unidades_df=i(r['n_unidades_df'],1),
        n_unidades_br=n_br, n_ufs=n_ufs,
        n_cnpjs_mesma_sala=n_sala, n_cnpjs_mesmo_predio=n_predio,
        endereco_suspeito=int(end_susp), franquia=int(franquia), rede_nacional=int(rede_nac),
        tipo_negocio=tipo_negocio,
        site=None, instagram=None, place_id=None, faturamento_est=None,
        capacidade=round(nota/100.0, 4), capacidade_conta=conta,
        dor=None, gatilho=None, score=round(nota/100.0, 4),
        estagio='1-filtro_duro', desqualificado=desq, motivo_desq=motivo,
        validado_receita=None, validacao_data=None, validacao_situacao=None,
        criado_em=HOJE, atualizado_em=HOJE))

    ev = [('situacao_cadastral','2 (ATIVA)'), ('cnae_principal',f"{r['cnae_fiscal_principal']} - {r['cnae_descricao']}"),
          ('porte',f"{porte} = {PORTE_DESC.get(porte,'')}"),
          ('capital_social',brl(cap)),
          ('opcao_simples',{'1':'Sim','0':'Nao'}.get(simples,'Sem registro na tabela Simples')),
          ('opcao_mei','0 (nao MEI) - filtro duro aplicado'),
          ('data_inicio_atividade',f"{r['data_inicio_atividade']} ({idade} meses)"),
          ('n_unidades_ativas',f'{n_br} no Brasil ({r["n_unidades_df"]} no DF), {n_ufs} UF(s)'),
          ('concentracao_endereco',f'{n_sala} CNPJs distintos na mesma sala (cep+numero+complemento); '
                                   f'{n_predio} no mesmo predio (cep+numero)'),
          ('nota_capacidade_conta',conta)]
    if franquia: ev.append(('marca_de_rede','nome contem marca de franquia odontologica conhecida'))
    if tipo_negocio != 'clinica':
        ev.append(('tipo_negocio', f'{tipo_negocio} - classificado por termo na razao social/nome fantasia; '
                                    'perfil de compra diferente de clinica que atende paciente final'))
    for t,v in ev:
        sinais.append((cb, t, v, FONTE, None, HOJE))

# ---------------- ordenacao ----------------
leads.sort(key=lambda L: (-L['score'], -L['capital_social'], -L['n_unidades_br'], L['razao_social']))

db = f'{BASE}/leads.db'
if os.path.exists(db): os.remove(db)
con = sqlite3.connect(db); cur = con.cursor()
cur.executescript('''
CREATE TABLE leads (
  id INTEGER PRIMARY KEY, cnpj_basico TEXT UNIQUE, cnpj TEXT, cnpj_formatado TEXT,
  razao_social TEXT, nome_fantasia TEXT, cnae TEXT, cnae_descricao TEXT, origem_recorte TEXT,
  municipio TEXT, bairro TEXT, endereco TEXT, cep TEXT,
  telefone TEXT, telefone_2 TEXT, email TEXT,
  data_inicio_atividade TEXT, idade_meses INTEGER,
  porte TEXT, porte_desc TEXT, natureza_juridica TEXT, natureza_juridica_desc TEXT,
  opcao_simples TEXT, capital_social REAL,
  n_unidades_df INTEGER, n_unidades_br INTEGER, n_ufs INTEGER,
  n_cnpjs_mesma_sala INTEGER, n_cnpjs_mesmo_predio INTEGER,
  endereco_suspeito INTEGER, franquia INTEGER, rede_nacional INTEGER, tipo_negocio TEXT,
  site TEXT, instagram TEXT, place_id TEXT, faturamento_est REAL,
  capacidade REAL, capacidade_conta TEXT, dor REAL, gatilho REAL, score REAL,
  estagio TEXT, desqualificado INTEGER, motivo_desq TEXT,
  validado_receita INTEGER, validacao_data TEXT, validacao_situacao TEXT,
  criado_em TEXT, atualizado_em TEXT);
CREATE TABLE sinais (
  id INTEGER PRIMARY KEY, lead_id INTEGER, tipo TEXT, valor TEXT,
  fonte TEXT, url TEXT, coletado_em TEXT,
  FOREIGN KEY(lead_id) REFERENCES leads(id));
CREATE TABLE contatos (
  id INTEGER PRIMARY KEY, lead_id INTEGER, canal TEXT, data TEXT, resultado TEXT,
  FOREIGN KEY(lead_id) REFERENCES leads(id));
CREATE TABLE outcomes (
  id INTEGER PRIMARY KEY, lead_id INTEGER, label TEXT, valor_fechado REAL, data TEXT,
  FOREIGN KEY(lead_id) REFERENCES leads(id));
CREATE TABLE meta (chave TEXT PRIMARY KEY, valor TEXT);
CREATE INDEX ix_sinais_lead ON sinais(lead_id);
CREATE INDEX ix_leads_score ON leads(score DESC);
''')
cols = list(leads[0].keys())
cur.executemany(f'INSERT INTO leads ({",".join(cols)}) VALUES ({",".join("?"*len(cols))})',
                [tuple(L[c] for c in cols) for L in leads])
idmap = dict(cur.execute('SELECT cnpj_basico, id FROM leads').fetchall())
cur.executemany('INSERT INTO sinais (lead_id,tipo,valor,fonte,url,coletado_em) VALUES (?,?,?,?,?,?)',
                [(idmap[s[0]],)+s[1:] for s in sinais])
cur.executemany('INSERT INTO meta VALUES (?,?)', [
 ('particao_base', PARTICAO),
 ('data_execucao', HOJE),
 ('defasagem_meses', '7'),
 ('fee_alvo_mensal', 'R$ 3.500'),
 ('faturamento_alvo_mensal', 'R$ 85.000 (faixa 80-150 mil)'),
 ('cnaes', '8630504 (todos) + 8630501/02/03/599 apenas com nome fantasia odontologico'),
 ('estagio_2_places_meta', 'BLOQUEADO - sem GOOGLE_PLACES_API_KEY e sem token da Meta Ad Library'),
 ('estagio_3_instagram', 'NAO EXECUTADO nesta rodada'),
 ('score_observacao', 'score = capacidade. Os eixos dor e gatilho ficaram NULL: '
                      'dependem de Places/Meta/Instagram, indisponiveis. '
                      'A formula do playbook (capacidade^1.5 x dor x gatilho) NAO foi aplicada.'),
 ('capacidade_observacao', 'Nota 0-100 derivada EXCLUSIVAMENTE de proxies do CNPJ '
                           '(porte 32 + capital social 22 + n_unidades 16 + regime 16 + maturidade 14), '
                           'com penalidades. NAO ha faturamento estimado por velocidade de reviews.'),
])
con.commit()
print('leads:', cur.execute('SELECT COUNT(*) FROM leads').fetchone()[0])
print('sinais:', cur.execute('SELECT COUNT(*) FROM sinais').fetchone()[0])
print('desqualificados:', cur.execute('SELECT COUNT(*) FROM leads WHERE desqualificado=1').fetchone()[0])
print('endereco_suspeito:', cur.execute('SELECT COUNT(*) FROM leads WHERE endereco_suspeito=1').fetchone()[0])
print('franquia:', cur.execute('SELECT COUNT(*) FROM leads WHERE franquia=1').fetchone()[0])
print('\ntop 15:')
for r in cur.execute('''SELECT round(score*100), porte, capital_social, n_unidades_br,
    substr(coalesce(nullif(nome_fantasia,""),razao_social),1,44), bairro
    FROM leads WHERE desqualificado=0 ORDER BY score DESC, capital_social DESC LIMIT 15'''):
    print(f'  {r[0]:3.0f} p{r[1]} R${r[2]:>12,.0f} un{r[3]} {r[4]:46} {r[5]}')
print('\ndistribuicao de nota:')
for r in cur.execute('''SELECT CAST(score*100/10 AS INT)*10 f, COUNT(*) FROM leads
   WHERE desqualificado=0 GROUP BY 1 ORDER BY 1 DESC'''): print(f'  {r[0]:3}-{r[0]+9:3}: {r[1]}')
con.close()
