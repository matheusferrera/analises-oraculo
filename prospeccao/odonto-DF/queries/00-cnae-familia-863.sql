-- Reconhecimento: distribuicao de CNAEs da familia 863 no DF (partição 2026-01-11)
SELECT cnae_fiscal_principal,
       COUNT(*) AS n_total,
       COUNTIF(situacao_cadastral = '2') AS n_ativos,
       COUNTIF(situacao_cadastral = '2' AND (
            LOWER(nome_fantasia) LIKE '%odonto%' OR LOWER(nome_fantasia) LIKE '%dent%'
         OR LOWER(nome_fantasia) LIKE '%orto%'   OR LOWER(nome_fantasia) LIKE '%implant%'
         OR LOWER(nome_fantasia) LIKE '%sorriso%')) AS n_ativos_nome_odonto
FROM `basedosdados.br_me_cnpj.estabelecimentos`
WHERE data = DATE '2026-01-11' AND sigla_uf = 'DF'
  AND cnae_fiscal_principal LIKE '863%'
GROUP BY 1 ORDER BY n_ativos DESC
