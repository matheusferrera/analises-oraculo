# Prospecção — Advocacia DF

Rodada de 19/08/2026. Fee alvo R$3.500/mês.

## O que este nicho tem de diferente

**1. O campo `porte` da Receita não serve aqui.** 68% dos escritórios marcados como "DEMAIS"
(supostamente acima do teto do Simples) são optantes pelo Simples Nacional — contradição direta.
2.958 são sociedade unipessoal e a mediana de capital social é R$10.000 em todos os portes.
Escritório de advocacia não declara ME/EPP e cai em DEMAIS por omissão.

**O eixo de capacidade é o número de sócios**, com pico em 4 a 12: abaixo disso não sustenta o
fee, acima disso já tem marketing interno e decisão por comitê.

**2. Ausência de anúncio não é dor.** O Provimento 205/2021 da OAB restringe publicidade —
vedada a mercantilização, a promessa de resultado e a captação ostensiva. Escritório que não
anuncia está em conformidade. Tratar como falha numa reunião seria constrangedor, e a vertente
de tráfego pago praticamente não se aplica.

**3. O motor da venda é o descompasso.** Autoridade real (rankings, cargos em entidades,
docência, publicações) que não está capturada digitalmente. Foi por isso que a fórmula mudou:

```
descompasso   = autoridade × (1 - fração capturada digitalmente)
probabilidade = propensão estrutural × max(dor técnica, descompasso) × acessibilidade
```

## Números

| | |
|---|---:|
| Escritórios enumerados (CNPJ raiz, ativos, não-MEI, 18+ meses) | 6625 |
| Na fila após desqualificações | 6418 |
| Com 5 ou mais sócios | 305 |
| Coletados em detalhe | 30 |

Desqualificados: bancas nacionais com só filial no DF (Mattos Filho, TozziniFreire, Pinheiro
Neto e outras 17), endereços com 15+ CNPJs na mesma sala, e três casos identificados na coleta —
Mota Advogados (Porto Alegre) e Ferrareze e Freitas (Passo Fundo) registraram matriz no DF e
escaparam do filtro estrutural.

## Alertas que a coleta levantou

- **Escritório de Advocacia Safe Carneiro** — o decisor, Joaquim José Safe Carneiro, ex-presidente
  da OAB-DF, **faleceu em 27/11/2025**. Identificar a sucessão antes de qualquer contato.
- **Mendonça Wald** — unidade brasiliense do grupo Wald (São Paulo, 1954); decisão de marketing
  provavelmente fora do DF.
- **Claudio Dantas** — o telefone do CNPJ hoje aparece atribuído a outra empresa no mesmo edifício.
  Validar por telefone antes de abordar. Existe jornalista homônimo conhecido.

## Arquivos

```
data/advocacia-df.csv          extração crua do BigQuery
data/socios.csv                contagem de sócios por CNPJ raiz (o eixo de capacidade)
data/socios-top30.csv          nomes dos sócios do top 30
data/coleta-top30.json         coleta digital consolidada
leads.db                       SQLite: leads + propensao
probabilidade-fechamento.md    o entregável
queries/                       SQL reproduzível
scripts/                       build_db.py, propensao.py, probabilidade.py
```

## Reproduzir

```bash
bq query --use_legacy_sql=false --max_rows=20000 --format=csv --project_id=secretario-oraculo \
  < prospeccao/advocacia-DF/queries/01-extracao-advocacia-df.sql > prospeccao/advocacia-DF/data/advocacia-df.csv
python3 prospeccao/advocacia-DF/scripts/build_db.py
python3 prospeccao/advocacia-DF/scripts/propensao.py
python3 prospeccao/advocacia-DF/scripts/probabilidade.py
```
