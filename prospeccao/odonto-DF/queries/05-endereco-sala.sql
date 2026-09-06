-- endereco_suspeito refinado: CNPJs distintos na MESMA SALA (cep+numero+complemento)
-- Retorna, para cada cnpj_basico do recorte, o nº de CNPJs na mesma sala e no mesmo predio.
WITH odonto AS (
  SELECT cnpj_basico, cep, numero, UPPER(TRIM(COALESCE(complemento,''))) AS compl
  FROM `basedosdados.br_me_cnpj.estabelecimentos`
  WHERE data = DATE '2026-01-11' AND sigla_uf='DF' AND situacao_cadastral='2'
    AND cnae_fiscal_principal IN ('8630504','8630503','8630502','8630501','8630599')
    AND (cnae_fiscal_principal='8630504'
         OR REGEXP_CONTAINS(LOWER(COALESCE(nome_fantasia,'')),
              r'odonto|dental|dentaria|dentario|dentes|ortodont|implantodont|periodont|endodont|bucal|sorriso'))
),
todos AS (
  SELECT cnpj_basico, cep, numero, UPPER(TRIM(COALESCE(complemento,''))) AS compl
  FROM `basedosdados.br_me_cnpj.estabelecimentos`
  WHERE data = DATE '2026-01-11' AND sigla_uf='DF' AND situacao_cadastral='2'
    AND cep IS NOT NULL AND numero IS NOT NULL
),
sala AS (
  SELECT cep, numero, compl, COUNT(DISTINCT cnpj_basico) AS n_sala
  FROM todos WHERE compl <> '' GROUP BY 1,2,3
)
SELECT DISTINCT o.cnpj_basico,
       COALESCE(sa.n_sala, 1) AS n_cnpjs_mesma_sala
FROM odonto o
LEFT JOIN sala sa ON sa.cep=o.cep AND sa.numero=o.numero AND sa.compl=o.compl
