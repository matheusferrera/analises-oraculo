-- Reconhecimento: distribuicao de CNAEs da familia 863 no DF (partição 2026-01-11)
SELECT cnae_fiscal_principal,
       COUNT(*) AS n_total,
       COUNTIF(situacao_cadastral = '2') AS n_ativos,
       COUNTIF(situacao_cadastral = '2' AND (
            REGEXP_CONTAINS(LOWER(COALESCE(nome_fantasia,'')),
              r'odonto|dental|dentaria|dentario|dentes|ortodont|implantodont|periodont|endodont|bucal|sorriso'))) AS n_ativos_nome_odonto
FROM `basedosdados.br_me_cnpj.estabelecimentos`
WHERE data = DATE '2026-01-11' AND sigla_uf = 'DF'
  AND cnae_fiscal_principal LIKE '863%'
GROUP BY 1 ORDER BY n_ativos DESC
