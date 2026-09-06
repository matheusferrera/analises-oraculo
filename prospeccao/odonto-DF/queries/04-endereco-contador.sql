-- Endereco de contador refinado.
-- No DF, CEP+numero identifica o PREDIO inteiro (quadras SCS/SCN/CLS), nao a sala:
-- 44% dos leads cairiam no corte se usassemos so CEP+numero >= 10.
-- A assinatura real de escritorio de contabilidade e' CEP+numero+COMPLEMENTO (mesma sala).
SELECT
  APPROX_QUANTILES(n_predio, 100)[OFFSET(50)] AS p50_predio,
  APPROX_QUANTILES(n_predio, 100)[OFFSET(90)] AS p90_predio,
  APPROX_QUANTILES(n_predio, 100)[OFFSET(99)] AS p99_predio,
  MAX(n_predio) AS max_predio
FROM (
  SELECT cep, numero, COUNT(DISTINCT cnpj_basico) AS n_predio
  FROM `basedosdados.br_me_cnpj.estabelecimentos`
  WHERE data = DATE '2026-01-11' AND sigla_uf='DF' AND situacao_cadastral='2'
    AND cep IS NOT NULL AND numero IS NOT NULL
  GROUP BY 1,2
)
