# -*- coding: utf-8 -*-
import sqlite3, csv, datetime
BASE='/Users/touchbar/Codigos-Projetos/oraculo/analises-oraculo/prospeccao/odonto-DF'
con=sqlite3.connect(f'{BASE}/leads.db'); con.row_factory=sqlite3.Row; cur=con.cursor()
meta=dict(cur.execute('SELECT chave,valor FROM meta').fetchall())
HOJE=datetime.date.today().strftime('%d/%m/%Y')
def brl(v):
    return 'R$ ' + f'{v:,.2f}'.replace(',','@').replace('.',',').replace('@','.')

COLS=['posicao','nota_capacidade','razao_social','nome_fantasia','cnpj_formatado','cnae',
 'cnae_descricao','endereco','bairro','municipio','telefone','telefone_2','email',
 'data_inicio_atividade','idade_meses','porte','porte_desc','opcao_simples','capital_social',
 'n_unidades_br','n_unidades_df','n_ufs','natureza_juridica_desc','tipo_negocio','franquia',
 'endereco_suspeito','n_cnpjs_mesma_sala','n_cnpjs_mesmo_predio','origem_recorte',
 'validado_receita','validacao_data','validacao_situacao','nota_capacidade_conta']

rows=cur.execute('''SELECT * FROM leads WHERE desqualificado=0
  ORDER BY score DESC, capital_social DESC, n_unidades_br DESC, razao_social''').fetchall()

with open(f'{BASE}/fila.csv','w',newline='',encoding='utf-8') as fh:
    w=csv.writer(fh); w.writerow(COLS)
    for i,r in enumerate(rows,1):
        w.writerow([i, round(r['score']*100), r['razao_social'], r['nome_fantasia'],
          r['cnpj_formatado'], r['cnae'], r['cnae_descricao'], r['endereco'], r['bairro'],
          r['municipio'], r['telefone'], r['telefone_2'], r['email'], r['data_inicio_atividade'],
          r['idade_meses'], r['porte'], r['porte_desc'], r['opcao_simples'],
          f"{r['capital_social']:.2f}", r['n_unidades_br'], r['n_unidades_df'], r['n_ufs'],
          r['natureza_juridica_desc'], r['tipo_negocio'], 'sim' if r['franquia'] else 'nao',
          'sim' if r['endereco_suspeito'] else 'nao', r['n_cnpjs_mesma_sala'],
          r['n_cnpjs_mesmo_predio'], r['origem_recorte'],
          {1:'sim',0:'nao'}.get(r['validado_receita'],''), r['validacao_data'] or '',
          r['validacao_situacao'] or '', r['capacidade_conta']])
print('fila.csv:',len(rows),'linhas')

def q(sql,*a): return cur.execute(sql,a).fetchall()
def n(sql,*a): return cur.execute(sql,a).fetchone()[0]
TOP=50
L=[]
A=L.append
A(f'# Fila de prospeccao — Clinicas odontologicas · Distrito Federal\n')
A(f'**Gerado em {HOJE}** · fee alvo **{meta["fee_alvo_mensal"]}/mes** · faturamento alvo **{meta["faturamento_alvo_mensal"]}**  ')
A(f'Base: `basedosdados.br_me_cnpj`, particao **{meta["particao_base"]}** (defasagem de ~{meta["defasagem_meses"]} meses)\n')
A('> ⚠️ **A nota desta fila e uma nota de CAPACIDADE, nao o score do playbook.**  ')
A('> Google Places e Meta Ad Library estao **bloqueados** (sem chave de API), e o Instagram nao foi coletado nesta rodada.  ')
A('> Logo os eixos **dor** e **gatilho** ficaram vazios e a formula `capacidade^1.5 x dor x gatilho` **nao foi aplicada**.  ')
A('> **Nao ha faturamento estimado** — nao existe velocidade de reviews para alimentar o estimador. ')
A('> Tudo abaixo vem exclusivamente de proxies do CNPJ.\n')
A('## Como a nota e calculada (0–100)\n')
A('| Componente | Peso | Escala |')
A('|---|---:|---|')
A('| Porte declarado | 32 | EPP `3` = 32 (faixa alvo exata: R$360 mil–4,8 mi/ano) · DEMAIS `5` = 28 · nao informado = 14 · ME `1` = 5 (teto R$360 mil/ano = R$30 mil/mes, abaixo do alvo) |')
A('| Capital social | 22 | ≥500k = 22 · 200–500k = 19 · 100–200k = 16 · 50–100k = 12 · 20–50k = 8 · 5–20k = 4 · >0 = 2 · 0 = 0 |')
A('| Unidades ativas (mesmo `cnpj_basico`, Brasil) | 16 | ≥5 = 16 · 3–4 = 13 · 2 = 9 · 1 = 4 |')
A('| Regime tributario | 16 | fora do Simples = 16 (lucro presumido/real ⇒ estrutura maior ou estouro do teto de R$4,8 mi) · sem registro = 9 · optante = 6 |')
A('| Maturidade | 14 | ≥15 anos = 14 · 10–15 = 12 · 5–10 = 9 · 3–5 = 6 · 1,5–3 = 3 |')
A('\n**Penalidades:** endereco suspeito −20 · sem telefone e sem e-mail −12 · fora do ICP (radiologia/laboratorio/comercio/plano/ensino) −12 · marca de franquia −10 · sem nome fantasia −4\n')
A('**Desqualificadores (fora da fila):** rede nacional / multi-UF · MEI · situacao ≠ ATIVA · aberta ha menos de 18 meses\n')
A('## Resumo\n')
A('| | |')
A('|---|---:|')
A(f'| Empresas na fila | **{len(rows)}** |')
A(f'| Nota ≥ 70 | {n("SELECT COUNT(*) FROM leads WHERE desqualificado=0 AND score>=0.70")} |')
A(f'| Nota ≥ 60 | {n("SELECT COUNT(*) FROM leads WHERE desqualificado=0 AND score>=0.60")} |')
A(f'| Nota ≥ 50 | {n("SELECT COUNT(*) FROM leads WHERE desqualificado=0 AND score>=0.50")} |')
A(f'| Porte EPP ou DEMAIS | {n("SELECT COUNT(*) FROM leads WHERE desqualificado=0 AND porte IN (?,?)", "3", "5")} |')
A(f'| Fora do Simples | {n("SELECT COUNT(*) FROM leads WHERE desqualificado=0 AND opcao_simples=?", "Nao")} |')
A(f'| Com 2+ unidades ativas | {n("SELECT COUNT(*) FROM leads WHERE desqualificado=0 AND n_unidades_br>=2")} |')
A(f'| Com e-mail na Receita | {n('SELECT COUNT(*) FROM leads WHERE desqualificado=0 AND email<>?', '')} |')
A('')
A('### Distribuicao de nota\n')
A('| Faixa | Empresas |')
A('|---|---:|')
for r in q('''SELECT CAST(score*100/10 AS INT)*10 f, COUNT(*) c FROM leads
              WHERE desqualificado=0 GROUP BY 1 ORDER BY 1 DESC'''):
    A(f'| {r["f"]}–{r["f"]+9} | {r["c"]} |')
A('')
A('### Top 12 regioes administrativas na fila\n')
A('| Bairro / RA | Empresas | Nota media |')
A('|---|---:|---:|')
for r in q('''SELECT bairro, COUNT(*) c, ROUND(AVG(score)*100,1) m FROM leads
              WHERE desqualificado=0 GROUP BY 1 ORDER BY c DESC LIMIT 12'''):
    A(f'| {r["bairro"]} | {r["c"]} | {r["m"]} |')
A('')
A(f'## Top {TOP} da fila\n')
for i,r in enumerate(rows[:TOP],1):
    nome=r['nome_fantasia'] or r['razao_social']
    A(f'### {i}. {nome} — nota {round(r["score"]*100)}/100\n')
    A(f'- **Razao social:** {r["razao_social"]}')
    A(f'- **CNPJ:** `{r["cnpj_formatado"]}`' + (f' · validado na Receita em {r["validacao_data"]}: **{r["validacao_situacao"]}**' if r['validado_receita'] is not None else ''))
    A(f'- **CNAE:** {r["cnae"]} — {r["cnae_descricao"]}' + ('' if r['origem_recorte']=='cnae_principal' else ' *(recrutado por nome fantasia odontologico em CNAE vizinho)*'))
    A(f'- **Endereco:** {r["endereco"]}')
    tel=' · '.join(x for x in [r['telefone'],r['telefone_2']] if x) or '—'
    A(f'- **Telefone:** {tel} · **E-mail:** {r["email"] or "—"}')
    A(f'- **Aberta em:** {r["data_inicio_atividade"]} ({r["idade_meses"]} meses) · **{r["natureza_juridica_desc"] or "—"}**')
    A(f'- **Porte:** {r["porte_desc"]} · **Simples:** {r["opcao_simples"]} · **Capital social:** {brl(r["capital_social"])}')
    A(f'- **Unidades ativas:** {r["n_unidades_br"]} no Brasil ({r["n_unidades_df"]} no DF, {r["n_ufs"]} UF)')
    A(f'- **Endereco suspeito:** {"SIM" if r["endereco_suspeito"] else "nao"} ({r["n_cnpjs_mesma_sala"]} CNPJs na mesma sala, {r["n_cnpjs_mesmo_predio"]} no mesmo predio)')
    if r['tipo_negocio']!='clinica': A(f'- ⚠️ **Tipo de negocio:** {r["tipo_negocio"]} — perfil de compra diferente de clinica')
    if r['franquia']: A('- ⚠️ **Marca de franquia** no nome — decisao de marketing pode ser parcialmente centralizada')
    A(f'- **Conta da nota:** `{r["capacidade_conta"]}`')
    A('')
A(f'\n---\n\n_Restante da fila ({len(rows)-TOP} empresas) em `fila.csv`. Evidencia por lead na tabela `sinais` de `leads.db`._')
open(f'{BASE}/fila.md','w',encoding='utf-8').write('\n'.join(L))
print('fila.md:',len(L),'linhas')
