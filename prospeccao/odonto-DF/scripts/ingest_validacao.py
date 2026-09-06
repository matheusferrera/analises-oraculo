# -*- coding: utf-8 -*-
"""Grava a validacao ao vivo do top 40 no leads.db."""
import json, sqlite3, datetime, shutil, os
BASE='/Users/touchbar/Codigos-Projetos/oraculo/analises-oraculo/prospeccao/odonto-DF'
HOJE=datetime.date.today().isoformat()
recs=[json.loads(l) for l in open('/tmp/validacao40.jsonl') if l.strip()]
os.makedirs(f'{BASE}/data',exist_ok=True)
shutil.copy('/tmp/validacao40.jsonl', f'{BASE}/data/validacao-top40.jsonl')
con=sqlite3.connect(f'{BASE}/leads.db'); cur=con.cursor()
ok=caiu=erro=0
for d in recs:
    sit=d.get('situacao')
    lid=cur.execute('SELECT id FROM leads WHERE cnpj=?',(d['cnpj'],)).fetchone()
    if not lid: print('nao achou',d['cnpj']); continue
    lid=lid[0]
    if not sit:
        erro+=1
        cur.execute('UPDATE leads SET validado_receita=0, validacao_data=?, validacao_situacao=? WHERE id=?',
                    (HOJE, f'falha na consulta: {d.get("erro")}', lid))
        cur.execute('INSERT INTO sinais (lead_id,tipo,valor,fonte,url,coletado_em) VALUES (?,?,?,?,?,?)',
                    (lid,'validacao_receita_ao_vivo',f'FALHA: {d.get("erro")}','BrasilAPI / Minha Receita',
                     f'https://brasilapi.com.br/api/cnpj/v1/{d["cnpj"]}',HOJE))
        continue
    ativa = sit.upper()=='ATIVA'
    ok += ativa; caiu += (not ativa)
    desq_extra = None
    if not ativa:
        desq_extra = f'Situacao cadastral mudou para {sit} apos o snapshot de 2026-01-11 (verificado {HOJE})'
        cur.execute('UPDATE leads SET desqualificado=1, motivo_desq=?, score=0, capacidade=0 WHERE id=?',
                    (desq_extra, lid))
    cur.execute('UPDATE leads SET validado_receita=1, validacao_data=?, validacao_situacao=?, atualizado_em=? WHERE id=?',
                (HOJE, sit, HOJE, lid))
    val=f'{sit}' + (f' desde {d["data_situacao"]}' if d.get('data_situacao') else '')
    if d.get('motivo'): val += f' — motivo: {d["motivo"]}'
    cur.execute('INSERT INTO sinais (lead_id,tipo,valor,fonte,url,coletado_em) VALUES (?,?,?,?,?,?)',
                (lid,'validacao_receita_ao_vivo',val,'BrasilAPI (Receita Federal, consulta ao vivo)',
                 f'https://brasilapi.com.br/api/cnpj/v1/{d["cnpj"]}',HOJE))
    if d.get('telefone'):
        cur.execute('INSERT INTO sinais (lead_id,tipo,valor,fonte,url,coletado_em) VALUES (?,?,?,?,?,?)',
                    (lid,'telefone_confirmado_ao_vivo',str(d['telefone']),'BrasilAPI',
                     f'https://brasilapi.com.br/api/cnpj/v1/{d["cnpj"]}',HOJE))
con.commit()
print(f'validados: {len(recs)} | ATIVAS: {ok} | caidas: {caiu} | falhas: {erro}')
for r in cur.execute('''SELECT validacao_situacao, COUNT(*) FROM leads
    WHERE validado_receita IS NOT NULL GROUP BY 1 ORDER BY 2 DESC'''): print('  ',r[0],r[1])
print('\ncaidas:')
for r in cur.execute('''SELECT cnpj_formatado, coalesce(nullif(nome_fantasia,''),razao_social), validacao_situacao
    FROM leads WHERE validado_receita=1 AND validacao_situacao<>'ATIVA' '''): print('  ',*r,sep=' | ')
con.close()
