# Prospeccao — Clinicas odontologicas · Distrito Federal

Rodada de **18/08/2026**. Fee alvo **R$ 3.500/mes** ⇒ faturamento alvo **~R$ 85 mil/mes**
(faixa 80–150 mil), pela regra do playbook `faturamento_alvo ≈ fee × 25`.

## ⚠️ Leia isto antes de usar a fila

O pipeline do playbook tem 5 estagios. **Nesta rodada so os estagios 0 e 1 rodaram.**

| Estagio | Fonte | Status |
|---|---|---|
| 0 — Enumeracao | BigQuery `basedosdados.br_me_cnpj` | ✅ executado |
| 1 — Filtro duro | SQL na mesma query | ✅ executado |
| 2 — Capacidade | Google Places + Meta Ad Library | ❌ **BLOQUEADO** — sem `GOOGLE_PLACES_API_KEY` e sem token da Meta Ad Library |
| 3 — Dor | Instagram + site | ❌ nao executado nesta rodada (sessao logada nao confirmada, volume alto) |
| 4 — Gancho | LLM | ❌ depende dos estagios 2 e 3 |

Consequencias diretas, que **nao devem ser mascaradas ao apresentar a lista**:

- **Nao existe faturamento estimado.** O estimador do playbook depende da velocidade de
  reviews do Google (`reviews_90d / 3 → clientes/mes → ticket`). Sem a chave do Places nao ha
  esse insumo. Nenhum numero de faturamento foi calculado nem inferido.
- **A nota da fila e uma nota de CAPACIDADE (0–100) construida so com proxies do CNPJ:**
  porte, capital social, numero de unidades, regime tributario e idade da empresa.
- **Os eixos `dor` e `gatilho` estao NULL** na tabela `leads`. A formula
  `score = capacidade^1.5 × dor^1.0 × gatilho^0.7` **nao foi aplicada** — seria zero para
  todo mundo, ou um numero falso se assumissemos `dor = gatilho = 1`.
  O campo `score` guarda a capacidade normalizada (0–1) e serve so para ordenar.
- Quando a chave do Places aparecer, a ordem do topo **vai mudar** — clinica grande e
  offline sobe, clinica pequena bem gerida desce.

## Base de dados

- Dataset: `basedosdados.br_me_cnpj` (tabelas `estabelecimentos`, `empresas`, `simples`)
  + diretorio `basedosdados.br_bd_diretorios_brasil.cnae_2`
- **Particao usada: `2026-01-11`** (snapshot mais recente). Toda query filtra
  `data = DATE '2026-01-11'` em `estabelecimentos` e `empresas`; `simples` nao e particionada.
- **Defasagem: ~7 meses** entre o snapshot e a data desta rodada (18/08/2026).
  Empresas baixadas, suspensas ou declaradas inaptas nesse intervalo **ainda aparecem como ATIVAS**.
  Compensacao: validacao ao vivo do **top 40** da fila na Receita (secao abaixo).
- Codigos normalizados da Base dos Dados (diferentes do CSV cru da Receita):
  `situacao_cadastral = '2'` como string; `opcao_mei` / `opcao_simples` como INTEGER 0/1;
  `porte` `'1'` ME, `'3'` EPP, `'5'` DEMAIS; datas ja tipadas como `DATE`.

## CNAEs usados

Descricoes oficiais confirmadas em `basedosdados.br_bd_diretorios_brasil.cnae_2`
(query `queries/01-cnae-descricoes.sql`). Todos pertencem a classe **86305 — Atividades de
atencao ambulatorial executadas por medicos e odontologos**.

| CNAE | Descricao oficial da subclasse | Uso |
|---|---|---|
| **8630504** | **Atividade odontologica** | ✅ **incluido integralmente** — 3.604 estabelecimentos ativos no DF |
| 8630503 | Atividade medica ambulatorial restrita a consultas | ⚠️ so com nome fantasia odontologico |
| 8630502 | Atividade medica ambulatorial com recursos para realizacao de exames complementares | ⚠️ so com nome fantasia odontologico |
| 8630501 | Atividade medica ambulatorial com recursos para realizacao de procedimentos cirurgicos | ⚠️ so com nome fantasia odontologico |
| 8630599 | Atividades de atencao ambulatorial nao especificadas anteriormente | ⚠️ so com nome fantasia odontologico |
| 8630506 | Servicos de vacinacao e imunizacao humana | ❌ fora |
| 8630507 | Atividades de reproducao humana assistida | ❌ fora |

### Decisao sobre os CNAEs vizinhos — e por que ela quase nao muda nada

A hipotese era que muita clinica odontologica se registra no CNAE errado. **Os dados nao
sustentam isso no DF.** Rodando o teste de nome fantasia (`queries/00-cnae-familia-863.sql`):

| CNAE | Ativos no DF | Com nome fantasia odontologico | % |
|---|---:|---:|---:|
| 8630504 | 3.604 | 2.317 | 64,3% |
| 8630503 | 4.138 | 2 | 0,05% |
| 8630599 | 1.351 | 8 | 0,6% |
| 8630502 | 969 | 4 | 0,4% |
| 8630501 | 451 | 1 | 0,2% |

Incluir os vizinhos inteiros arrastaria **~6.900 clinicas medicas nao-odontologicas**.
Incluir so os que tem nome odontologico custa zero e traz **15 estabelecimentos**
(11 empresas apos os filtros, 0,35% da fila). Foi o que se fez: os vizinhos entram
**somente** quando o nome fantasia casa com
`odonto|dental|dentaria|dentario|dentes|ortodont|implantodont|periodont|endodont|bucal|sorriso`.
A coluna `origem_recorte` no CSV marca quem veio por qual caminho.

> **Armadilha corrigida no meio da rodada:** a primeira versao do regex usava `orto(dont|)`
> e `implant`, que casavam **ORTOPEDIA** (medica) e **implante capilar**. Isso injetava ~85
> falsos positivos, varios deles no topo da fila (ex.: "MULTI HAIR IMPLANT",
> "CLINICA HOSPITALAR ORTOPEDICA ARTHROS"). O regex acima e a versao corrigida; todas as
> queries e contagens deste README ja usam a versao corrigida.

**CNAE secundario:** testado e descartado. Fora da familia 8630, os estabelecimentos ativos
do DF que listam `8630504` como CNAE **secundario** sao liderados por `9602502`
(atividades de estetica, 62 casos) e `8211300` (servicos de escritorio, 24) — ruido, nao clinica.

## Funil

| # | Estagio | Empresas / estabelecimentos |
|---|---|---:|
| 0 | Estabelecimentos no DF, classe 86305, **todas as situacoes** | 15.645 |
| 1 | ... com `situacao_cadastral = '2'` (ATIVA) | 10.513 |
| 2a | ... CNAE 8630504 (Atividade odontologica) | 3.604 |
| 2b | ... + vizinhos 86305xx com nome fantasia odontologico | +15 |
| 2 | **Recorte odontologico (estabelecimentos)** | **3.619** |
| 3 | Agrupado por `cnpj_basico` (matriz + filiais viram 1 lead) | 3.549 |
| 4 | ... menos MEI (`opcao_mei = 1`) | 3.549 (**0 descartados**) |
| 5 | ... menos abertas ha < 18 meses | **3.136** |
| 6 | ... menos 5 desqualificados por rede nacional / multi-UF | 3.131 |
| 7 | ... menos 7 reprovados na validacao ao vivo na Receita (INAPTA) | **3.124 na fila** |

Observacoes sobre os cortes:

- **MEI descartou zero.** Atividade odontologica **nao e permitida no MEI** (profissao
  regulamentada), entao o filtro nao tem o que cortar neste nicho. Ele foi mantido no SQL
  por seguranca, mas nao e um filtro util aqui — vale a pena saber antes de contar com ele.
- **417 empresas** cairam por terem menos de 18 meses de atividade.
- **5 desqualificadas** por rede nacional / multi-UF (decisao de marketing centralizada):
  SOUSMILE (8 unidades / 4 UFs), SERMED (63 / 17), ODONTOGROUP (4 / 3), DENTE CROSS (8 / 4)
  e SESC-DF (18 unidades). Continuam no `leads.db` com `desqualificado = 1` e motivo.

## `endereco_suspeito` — o criterio teve que ser refeito para o DF

O criterio do playbook e "muitos CNPJs no mesmo CEP+numero". **No DF isso nao funciona**: as
quadras comerciais (SCS, SCN, CLS, blocos de Aguas Claras) tem **um CEP+numero para o predio
inteiro**. Um endereco chega a **1.229 CNPJs distintos**, e o criterio `>= 10` marcaria
**44% de toda a fila** como endereco de contador — inutil.

A assinatura real de escritorio de contabilidade / endereco virtual e **a mesma SALA**:
`cep + numero + complemento`. Com esse criterio (`>= 10 CNPJs na mesma sala`), a fila tem
**3 leads marcados** — que e a ordem de grandeza esperada. Ambas as contagens ficam gravadas
por lead (`n_cnpjs_mesma_sala` e `n_cnpjs_mesmo_predio`), entao da pra revisar o corte
sem refazer query.

## Classificacao de tipo de negocio

Dentro do CNAE 8630504 nem tudo e clinica que atende paciente final. Cada lead recebe um
`tipo_negocio` derivado da razao social / nome fantasia:

| tipo_negocio | Empresas | Tratamento |
|---|---:|---|
| clinica | 3.090 | ICP — sem ajuste |
| radiologia_imagem | 14 | −12 na nota (B2B, funil e ticket diferentes) |
| comercio_industria | 13 | −12 |
| ensino_treinamento | 7 | −12 |
| plano_convenio | 6 | −12 |
| laboratorio_protese | 6 | −12 |

Penalidade em vez de descarte: a classificacao e por palavra-chave e tem falso positivo
(ha clinica com laboratorio proprio na razao social). O campo esta no CSV para filtrar a mao.

## Nota de capacidade (0–100) — apenas proxies do CNPJ

| Componente | Peso | Escala |
|---|---:|---|
| Porte declarado | 32 | EPP `3` = 32 · DEMAIS `5` = 28 · nao informado = 14 · ME `1` = 5 |
| Capital social | 22 | ≥500k = 22 · 200–500k = 19 · 100–200k = 16 · 50–100k = 12 · 20–50k = 8 · 5–20k = 4 · >0 = 2 · 0 = 0 |
| Unidades ativas (`cnpj_basico`, Brasil) | 16 | ≥5 = 16 · 3–4 = 13 · 2 = 9 · 1 = 4 |
| Regime tributario | 16 | fora do Simples = 16 · sem registro = 9 · optante = 6 |
| Maturidade | 14 | ≥15 anos = 14 · 10–15 = 12 · 5–10 = 9 · 3–5 = 6 · 1,5–3 = 3 |

Penalidades: `endereco_suspeito` −20 · sem telefone e sem e-mail −12 · fora do ICP −12 ·
marca de franquia −10 · sem nome fantasia −4. Resultado limitado a 0–100.

Por que **EPP pontua mais que DEMAIS**: o alvo e R$85 mil/mes = ~R$1,0 mi/ano, que cai
exatamente na faixa EPP (R$360 mil–4,8 mi/ano). DEMAIS paga o fee com folga, mas tem chance
maior de decisao centralizada. ME tem teto de R$360 mil/ano = R$30 mil/mes — **abaixo do alvo**,
por isso pontua 5. Como 2.374 dos 3.124 leads (76%) sao ME, o porte e o principal
discriminante desta fila. `porte` e autodeclarado e envelhece mal — por isso e peso, nunca corte.

A conta completa de cada lead esta no campo `nota_capacidade_conta` (CSV), em
`leads.capacidade_conta` e como sinal `nota_capacidade_conta` na tabela `sinais`.

## Validacao ao vivo do top 40 — a defasagem custa 17,5% do topo da fila

Os **40 primeiros** da fila (ranking pre-validacao) foram consultados um a um na Receita via
**BrasilAPI** (`brasilapi.com.br/api/cnpj/v1/{cnpj}`), com 22 s entre chamadas para respeitar
o rate limit. Data da consulta: **18/08/2026**. Nenhuma chamada falhou.

| Resultado | Empresas |
|---|---:|
| ATIVA (confirmada) | **33** |
| INAPTA (caiu depois do snapshot) | **7** |
| Falha de consulta | 0 |

**7 de 40 = 17,5% do topo da fila ja nao estava ativo** — a defasagem de 7 meses do snapshot
nao e detalhe. As 7 que cairam:

| CNPJ | Nome | Situacao hoje |
|---|---|---|
| 26.498.659/0001-03 | ESTHETICS INSTITUTO DE ODONTOLOGIA | INAPTA |
| 19.262.019/0001-34 | MEDICAL CENTER | INAPTA |
| 02.044.710/0001-49 | AMAZING HOF | INAPTA |
| 47.962.883/0001-84 | VALCENAR ODONTOLOGIA | INAPTA |
| 23.125.049/0001-76 | DF HOSPITAL ODONTOLOGICO | INAPTA |
| 32.192.040/0001-79 | DR MARCIO ROSSI JUNIOR | INAPTA |
| 38.250.861/0001-09 | ALVERNAZ ODONTOLOGIA | INAPTA |

As 7 foram marcadas com `desqualificado = 1` e removidas de `fila.csv` / `fila.md`
(a fila caiu de 3.131 para **3.124**). Continuam no `leads.db` com o motivo registrado, e cada
uma tem um sinal `validacao_receita_ao_vivo` com fonte, URL e data.

Duas leituras importantes:

- **INAPTA nao e o mesmo que fechada.** A situacao "inapta" costuma vir de omissao de
  declaracoes por dois exercicios seguidos; a clinica pode estar funcionando com o CNPJ
  irregular. Vale confirmar por telefone antes de descartar de vez — mas nao e lead de
  primeira abordagem.
- **Extrapolando os 17,5% para a fila inteira, ~550 dos 3.124 leads podem nao estar mais
  ativos.** Isso **nao** foi aplicado a fila (seria inventar dado): so os 40 verificados
  carregam status ao vivo. Os campos `validado_receita`, `validacao_data` e
  `validacao_situacao` ficam vazios para quem nao foi consultado — vazio significa
  "nao verificado", nunca "verificado e ok".
- Ao remover as 7, as posicoes 41–47 do ranking antigo subiram para o top 40 **sem terem
  sido validadas**. Uma proxima rodada deve validar essas.

Reexecutar: `bash scripts/validar_top40.sh && python3 scripts/ingest_validacao.py`

## Limitacoes conhecidas desta fila

1. **Sem os estagios 2–4, a fila mede so capacidade de pagar — nao mede necessidade nem timing.**
   Uma clinica EPP com marketing impecavel e uma clinica EPP sem Instagram tem a mesma nota aqui.
   E exatamente isso que Places/Meta/Instagram resolveriam.
2. **`porte` e autodeclarado e envelhece mal.** Ha casos de contradicao evidente na fila —
   ex.: `AMAZING HOF`, porte ME (teto R$360 mil/ano) com R$2,5 mi de capital social.
   Por isso porte e peso (32 pontos), nunca corte duro.
3. **O CNAE mente e o classificador de `tipo_negocio` e por palavra-chave.** Sobra ruido:
   `BM LOCACOES E CONSTRUCOES` esta registrada no CNAE 8630504 e passou como "clinica"
   (nota 40, fundo da fila). Confirmar o nicho pelo digital continua sendo trabalho do estagio 3.
4. **`endereco_suspeito` cobre endereco de contador, nao consultorio dentro de clinica de terceiros.**
   Muito consultorio odontologico do DF fica em sala de torre comercial compartilhada; o campo
   `n_cnpjs_mesmo_predio` ajuda a identificar isso a mao.
5. **387 leads nao tem nome fantasia** na Receita e **86 nao tem telefone nem e-mail** —
   vao precisar de enriquecimento antes de virar contato.

## Arquivos

```
prospeccao/odonto-DF/
  README.md                        este arquivo
  leads.db                         SQLite: leads, sinais, contatos, outcomes, meta
  fila.csv                         3.124 leads ranqueados, 33 colunas
  fila.md                          resumo + top 50 detalhado
  data/odonto-df.csv               saida crua da query de extracao
  data/funil.csv                   contagens de cada estagio
  data/validacao-top40.jsonl       resposta bruta da Receita para o top 40
  queries/00-cnae-familia-863.sql  reconhecimento de CNAE
  queries/01-cnae-descricoes.sql   descricoes oficiais
  queries/02-extracao-odonto-df.sql  extracao + filtro duro (query principal)
  queries/03-funil.sql             contagem de cada estagio
  queries/04-endereco-contador.sql analise da concentracao de enderecos no DF
  queries/05-endereco-sala.sql     endereco_suspeito por cep+numero+complemento
  scripts/build_db.py              monta leads.db + calcula a nota de capacidade
  scripts/export_fila.py           gera fila.csv e fila.md a partir do leads.db
  scripts/validar_top40.sh         consulta a Receita ao vivo (BrasilAPI, 22s entre chamadas)
  scripts/ingest_validacao.py      grava o resultado da validacao no leads.db
```

Rodar de novo:
`bq query --use_legacy_sql=false --format=csv --project_id=secretario-oraculo < queries/02-extracao-odonto-df.sql`

## Custo em BigQuery

Somando todos os jobs desta rodada (`region-us.INFORMATION_SCHEMA.JOBS_BY_PROJECT`):
**0,81 GB faturados = US$ 0,005** na tabela on-demand — **dentro da cota gratuita de 1 TB/mes**,
ou seja, custo efetivo **US$ 0,00**.

Ressalva de leitura: a maioria dos jobs aparece com `total_bytes_billed = 0` porque o dataset
publico da Base dos Dados tem row-level security, o que mascara a estatistica de bytes por job.
O numero acima e o que o BigQuery de fato registrou como faturavel. O que garante que a conta
nao explode e o filtro de particao (`data = DATE '2026-01-11'`) presente em **todas** as queries
sobre `estabelecimentos` e `empresas` — sem ele, cada query varreria todos os snapshots
historicos de uma tabela de 66 milhoes de linhas.

## Rastreabilidade (LGPD)

Todo numero em `leads` tem linha correspondente em `sinais` com `fonte` e `coletado_em`.
Sao dados publicos de pessoa juridica, tratados sob legitimo interesse comercial.
Nenhum dado pessoal de pessoa fisica foi coletado (a tabela `socios` **nao** foi consultada).
