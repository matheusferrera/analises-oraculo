-- Escritorios de advocacia ativos no DF, nao-MEI, abertos ha 18+ meses.
-- Particao obrigatoria: sem ela a query varre todos os snapshots e queima a cota.
WITH est AS (
  SELECT * FROM `basedosdados.br_me_cnpj.estabelecimentos`
  WHERE data = DATE '2026-01-11'
    AND sigla_uf = 'DF'
    AND cnae_fiscal_principal IN ('6911701','6911702','6911703')  -- advocacia, cartorios, agente propriedade industrial
    AND situacao_cadastral = '2'
    AND data_inicio_atividade < DATE_SUB(CURRENT_DATE(), INTERVAL 18 MONTH)
),
unid AS (
  SELECT cnpj_basico, COUNT(*) AS n_unidades_df FROM est GROUP BY cnpj_basico
),
sala AS (   -- endereco de contador: mesma sala, nao mesmo predio (licao de Brasilia)
  SELECT cep, numero, complemento, COUNT(DISTINCT cnpj_basico) AS n_mesma_sala
  FROM `basedosdados.br_me_cnpj.estabelecimentos`
  WHERE data = DATE '2026-01-11' AND sigla_uf='DF' AND situacao_cadastral='2'
  GROUP BY cep, numero, complemento
),
predio AS (
  SELECT cep, numero, COUNT(DISTINCT cnpj_basico) AS n_mesmo_predio
  FROM `basedosdados.br_me_cnpj.estabelecimentos`
  WHERE data = DATE '2026-01-11' AND sigla_uf='DF' AND situacao_cadastral='2'
  GROUP BY cep, numero
)
SELECT e.cnpj, e.cnpj_basico, e.nome_fantasia, m.razao_social,
       e.cnae_fiscal_principal AS cnae, e.identificador_matriz_filial,
       e.tipo_logradouro, e.logradouro, e.numero, e.complemento, e.bairro, e.cep,
       e.ddd_1, e.telefone_1, e.ddd_2, e.telefone_2, e.email,
       e.data_inicio_atividade, DATE_DIFF(CURRENT_DATE(), e.data_inicio_atividade, MONTH) AS idade_meses,
       m.porte, m.capital_social, m.natureza_juridica,
       COALESCE(s.opcao_simples, 0) AS opcao_simples,
       u.n_unidades_df, sa.n_mesma_sala, pr.n_mesmo_predio
FROM est e
JOIN `basedosdados.br_me_cnpj.empresas` m
  ON m.cnpj_basico = e.cnpj_basico AND m.data = DATE '2026-01-11'
LEFT JOIN `basedosdados.br_me_cnpj.simples` s ON s.cnpj_basico = e.cnpj_basico
JOIN unid u ON u.cnpj_basico = e.cnpj_basico
LEFT JOIN sala sa ON sa.cep=e.cep AND sa.numero=e.numero AND sa.complemento=e.complemento
LEFT JOIN predio pr ON pr.cep=e.cep AND pr.numero=e.numero
WHERE COALESCE(s.opcao_mei, 0) = 0
