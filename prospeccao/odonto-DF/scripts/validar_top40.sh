#!/bin/bash
OUT=/tmp/validacao40.jsonl
: > $OUT
n=0
while read -r C; do
  n=$((n+1))
  R=$(curl -s --max-time 30 "https://brasilapi.com.br/api/cnpj/v1/$C")
  if ! echo "$R" | python3 -c "import sys,json;d=json.load(sys.stdin);sys.exit(0 if d.get('descricao_situacao_cadastral') else 1)" 2>/dev/null; then
    sleep 25
    R=$(curl -s --max-time 30 "https://minhareceita.org/$C")
  fi
  python3 -c "
import sys,json
c=sys.argv[1]; raw=sys.argv[2]
try: d=json.loads(raw)
except Exception: d={}
out={'cnpj':c,'situacao':d.get('descricao_situacao_cadastral'),
 'data_situacao':d.get('data_situacao_cadastral'),'razao_social':d.get('razao_social'),
 'nome_fantasia':d.get('nome_fantasia'),'telefone':d.get('ddd_telefone_1'),
 'email':d.get('email'),'capital_social':d.get('capital_social'),
 'porte':d.get('descricao_porte') or d.get('porte'),
 'motivo':d.get('descricao_motivo_situacao_cadastral'),
 'erro': None if d.get('descricao_situacao_cadastral') else (d.get('message') or 'sem resposta')}
print(json.dumps(out,ensure_ascii=False))" "$C" "$R" >> $OUT
  echo "[$n/40] $C -> $(tail -1 $OUT | python3 -c 'import sys,json;d=json.load(sys.stdin);print(d["situacao"] or d["erro"])')"
  sleep 22
done < /tmp/top40.txt
echo FIM
