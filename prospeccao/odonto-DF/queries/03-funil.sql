-- Contagem em cada estagio do funil (mesma logica da query 02)
WITH base AS (
  SELECT * FROM `basedosdados.br_me_cnpj.estabelecimentos`
  WHERE data = DATE '2026-01-11' AND sigla_uf='DF'
    AND cnae_fiscal_principal IN ('8630504','8630503','8630502','8630501','8630599')
),
ativos AS (SELECT * FROM base WHERE situacao_cadastral='2'),
odonto AS (
  SELECT * FROM ativos
  WHERE cnae_fiscal_principal='8630504'
     OR REGEXP_CONTAINS(LOWER(COALESCE(nome_fantasia,'')),
          r'odonto|dental|dentaria|dentario|dentes|ortodont|implantodont|periodont|endodont|bucal|sorriso')
),
com_simples AS (
  SELECT o.*, s.opcao_mei FROM odonto o
  LEFT JOIN `basedosdados.br_me_cnpj.simples` s USING (cnpj_basico)
)
SELECT
  (SELECT COUNT(*) FROM base)                                          AS e0_estab_familia86305_df_todas_situacoes,
  (SELECT COUNT(*) FROM ativos)                                        AS e1_ativos,
  (SELECT COUNT(*) FROM ativos WHERE cnae_fiscal_principal='8630504')  AS e2a_cnae_8630504_ativos,
  (SELECT COUNT(*) FROM odonto WHERE cnae_fiscal_principal<>'8630504') AS e2b_vizinhos_nome_odonto,
  (SELECT COUNT(*) FROM odonto)                                        AS e2_recorte_odonto_estab,
  (SELECT COUNT(DISTINCT cnpj_basico) FROM odonto)                     AS e3_empresas_distintas,
  (SELECT COUNT(DISTINCT cnpj_basico) FROM com_simples WHERE opcao_mei=1)                 AS e4_descartados_mei,
  (SELECT COUNT(DISTINCT cnpj_basico) FROM com_simples WHERE COALESCE(opcao_mei,0)<>1)    AS e4_apos_mei,
  (SELECT COUNT(DISTINCT cnpj_basico) FROM com_simples
    WHERE COALESCE(opcao_mei,0)<>1
      AND data_inicio_atividade >= DATE_SUB(CURRENT_DATE(), INTERVAL 18 MONTH))           AS e5_descartados_menos_18m,
  (SELECT COUNT(DISTINCT cnpj_basico) FROM com_simples
    WHERE COALESCE(opcao_mei,0)<>1
      AND data_inicio_atividade < DATE_SUB(CURRENT_DATE(), INTERVAL 18 MONTH))            AS e5_fila_final
