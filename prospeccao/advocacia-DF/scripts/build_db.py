#!/usr/bin/env python3
"""
Monta leads.db da advocacia-DF.

DIFERENÇA CRÍTICA PARA A ODONTOLOGIA: o campo `porte` é inútil aqui. 68% dos
marcados como DEMAIS são optantes pelo Simples (contradição), 2.958 são sociedade
unipessoal, e a mediana de capital social é R$10.000 em todos os portes. Escritório
de advocacia não declara ME/EPP e cai em DEMAIS por omissão.

O eixo de capacidade real é o NÚMERO DE SÓCIOS.
"""
import csv, datetime, re, sqlite3, sys, unicodedata, pathlib
sys.path.insert(0, 'prospeccao/tools')
from telefones import classificar

B = pathlib.Path("prospeccao/advocacia-DF")
HOJE = datetime.date.today().isoformat()
NAT = {'2062':'Sociedade Empresária Ltda','2135':'Empresário Individual','2240':'Sociedade Simples Ltda',
       '2232':'Sociedade Simples Pura','2321':'Sociedade Unipessoal de Advocacia','4014':'EIRELI',
       '2143':'Sociedade Simples em Nome Coletivo','1015':'Órgão Público','3999':'Associação Privada'}
CONT = re.compile(r"contab|contabil|escritorio de contab|assessoria contab|conta[dt]or", re.I)
sa = lambda s: unicodedata.normalize("NFKD", s or "").encode("ascii","ignore").decode().upper()

socios = {r['cnpj_basico']: r for r in csv.DictReader(open(B/"data"/"socios.csv"))}
rows = list(csv.DictReader(open(B/"data"/"advocacia-df.csv")))

# Banca nacional: se no DF só existe filial, a matriz (e a decisão de marketing) está fora.
# 20 dos 34 escritórios com 30+ sócios caem aqui — Mattos Filho, TozziniFreire, Pinheiro Neto.
tem_matriz_df = {r['cnpj_basico'] for r in rows if r['identificador_matriz_filial'] == '1'}

# telefone compartilhado entre CNPJs distintos = contato de contador ou de prédio
from collections import Counter
tel_freq = Counter(r['ddd_1']+r['telefone_1'] for r in rows if r['telefone_1'])

con = sqlite3.connect(B/"leads.db")
con.executescript("""
DROP TABLE IF EXISTS leads; DROP TABLE IF EXISTS sinais;
CREATE TABLE leads (
  id INTEGER PRIMARY KEY, cnpj_basico TEXT, cnpj TEXT, cnpj_formatado TEXT,
  razao_social TEXT, nome_fantasia TEXT, cnae TEXT, natureza_juridica TEXT, natureza_desc TEXT,
  municipio TEXT, bairro TEXT, endereco TEXT, cep TEXT,
  telefone TEXT, telefone_tipo TEXT, whatsapp TEXT, telefone_2 TEXT, email TEXT,
  email_de_contador INT, telefone_compartilhado INT,
  data_inicio_atividade TEXT, idade_meses INT, porte TEXT, capital_social REAL,
  opcao_simples INT, n_socios INT, n_administradores INT, n_unidades_df INT,
  n_cnpjs_mesma_sala INT, n_cnpjs_mesmo_predio INT, endereco_suspeito INT,
  capacidade REAL, capacidade_conta TEXT, desqualificado INT, motivo_desq TEXT, criado_em TEXT);
CREATE TABLE sinais (id INTEGER PRIMARY KEY, lead_id TEXT, tipo TEXT, valor TEXT, fonte TEXT, coletado_em TEXT);
""")

vistos, n = set(), 0
for r in rows:
    cb = r['cnpj_basico']
    if cb in vistos: continue          # agrupa por CNPJ raiz
    vistos.add(cb)
    s = socios.get(cb, {})
    ns = int(s.get('n_socios') or 0); na = int(s.get('n_administradores') or 0)
    idade = int(r['idade_meses'] or 0); cap = float(r['capital_social'] or 0)
    sala = int(r['n_mesma_sala'] or 1); predio = int(r['n_mesmo_predio'] or 1)
    unid = int(r['n_unidades_df'] or 1)
    tel_raw = (r['ddd_1'] or '') + (r['telefone_1'] or '')
    f1,e1,t1,_ = classificar(tel_raw); f2,e2,_,_ = classificar((r['ddd_2'] or '')+(r['telefone_2'] or ''))
    compart = tel_freq.get(tel_raw, 0) > 1 if tel_raw else False

    # --- capacidade 0-100: socios manda, o resto ajusta ---
    partes = []
    c = 0.0
    # curva com PICO no meio, nao monotonica: escritorio grande demais ja tem
    # marketing interno e decisao por comite — capacidade sobra, abertura falta.
    if   ns >= 40: c += 16; partes.append(f"{ns} sócios: estrutura própria de marketing (+16)")
    elif ns >= 25: c += 26; partes.append(f"{ns} sócios: provável coordenação interna (+26)")
    elif ns >= 13: c += 38; partes.append(f"{ns} sócios (+38)")
    elif ns >= 5:  c += 45; partes.append(f"{ns} sócios: faixa ideal (+45)")
    elif ns == 4:  c += 42; partes.append("4 sócios: faixa ideal (+42)")
    elif ns == 3:  c += 34; partes.append("3 sócios (+34)")
    elif ns == 2:  c += 22; partes.append("2 sócios (+22)")
    else:          c += 5;  partes.append("sócio único (+5)")
    if unid > 1: c += 10; partes.append(f"{unid} unidades (+10)")
    if cap >= 200000: c += 14; partes.append(f"capital R$ {cap:,.0f} (+14)".replace(",", "."))
    elif cap >= 50000: c += 9; partes.append(f"capital R$ {cap:,.0f} (+9)".replace(",", "."))
    elif cap >= 20000: c += 4; partes.append("capital 20-50k (+4)")
    if   idade >= 240: c += 12; partes.append(f"{idade//12} anos (+12)")
    elif idade >= 120: c += 10; partes.append(f"{idade//12} anos (+10)")
    elif idade >= 60:  c += 6;  partes.append(f"{idade//12} anos (+6)")
    else:              c += 2;  partes.append(f"{idade//12} anos (+2)")
    if na >= 2: c += 5; partes.append(f"{na} administradores (+5)")
    if sala >= 8: c -= 12; partes.append(f"{sala} CNPJs na mesma sala (-12)")
    c = max(0.0, min(100.0, c))

    desq, motivo = 0, None
    if cb not in tem_matriz_df:
        desq, motivo = 1, "banca nacional: no DF só há filial, a matriz e a decisão de marketing estão fora"
    elif sala >= 15:
        desq, motivo = 1, f"endereço com {sala} CNPJs na mesma sala — provável escritório de contabilidade"
    # escritório muito grande costuma ter marketing interno: capacidade sobra, abertura falta


    con.execute("INSERT INTO leads (cnpj_basico,cnpj,cnpj_formatado,razao_social,nome_fantasia,cnae,"
      "natureza_juridica,natureza_desc,municipio,bairro,endereco,cep,telefone,telefone_tipo,whatsapp,"
      "telefone_2,email,email_de_contador,telefone_compartilhado,data_inicio_atividade,idade_meses,"
      "porte,capital_social,opcao_simples,n_socios,n_administradores,n_unidades_df,n_cnpjs_mesma_sala,"
      "n_cnpjs_mesmo_predio,endereco_suspeito,capacidade,capacidade_conta,desqualificado,motivo_desq,criado_em)"
      " VALUES (" + ",".join("?"*35) + ")",
      (cb, r['cnpj'], f"{cb}/{r['cnpj'][8:12]}-{r['cnpj'][12:]}", r['razao_social'].title(),
       (r['nome_fantasia'] or '').title(), r['cnae'], r['natureza_juridica'],
       NAT.get(r['natureza_juridica'], r['natureza_juridica']), 'Brasília', (r['bairro'] or '').title(),
       " ".join(x for x in [r['tipo_logradouro'], r['logradouro'], r['numero'], r['complemento']] if x),
       r['cep'], f1 or f2, t1, e1 or e2, f2 if f1 else None, r['email'] or None,
       int(bool(r['email'] and CONT.search(r['email']))), int(compart),
       r['data_inicio_atividade'], idade, r['porte'], cap,
       int(r['opcao_simples'] in ('1','true','True')), ns, na, unid, sala, predio,
       int(sala >= 8), round(c/100, 4), " · ".join(partes), desq, motivo, HOJE))
    n += 1
con.commit()

print(f"leads gravados: {n}")
for lo, hi, rot in [(.70,1.01,"A  >=0,70"),(.55,.70,"B  0,55-0,70"),(.40,.55,"C  0,40-0,55"),(0,.40,"D  <0,40")]:
    q = con.execute("SELECT COUNT(*) FROM leads WHERE desqualificado=0 AND capacidade>=? AND capacidade<?", (lo,hi)).fetchone()[0]
    print(f"  {rot:16} {q:5}")
print(f"  desqualificados (endereço de contador): "
      f"{con.execute('SELECT COUNT(*) FROM leads WHERE desqualificado=1').fetchone()[0]}")
print(f"  e-mail de contador: {con.execute('SELECT COUNT(*) FROM leads WHERE email_de_contador=1').fetchone()[0]}"
      f" | telefone compartilhado: {con.execute('SELECT COUNT(*) FROM leads WHERE telefone_compartilhado=1').fetchone()[0]}")
