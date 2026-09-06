-- =====================================================================
-- Estagio 0 + 1: enumeracao e filtro duro
-- Odontologia no Distrito Federal
-- Base: basedosdados.br_me_cnpj  | particao: 2026-01-11
-- Recorte de CNAE:
--   (a) 8630504 "Atividade odontologica" -- todos
--   (b) 8630501/02/03/599 -- SOMENTE com nome_fantasia com termo odontologico
--       (nos vizinhos, apenas 15 dos 6.909 ativos tem nome odontologico;
--        incluir os vizinhos inteiros traria ~6.900 clinicas medicas nao-odonto)
-- =====================================================================
DECLARE PART DATE DEFAULT DATE '2026-01-11';

WITH
-- 1) universo DF na familia 86305, ativos
base AS (
  SELECT *
  FROM `basedosdados.br_me_cnpj.estabelecimentos`
  WHERE data = PART AND sigla_uf = 'DF'
    AND cnae_fiscal_principal IN ('8630504','8630503','8630502','8630501','8630599')
    AND situacao_cadastral = '2'
),
-- 2) recorte odontologico
odonto AS (
  SELECT *,
    CASE WHEN cnae_fiscal_principal = '8630504' THEN 'cnae_principal'
         ELSE 'vizinho_nome_odonto' END AS origem_recorte
  FROM base
  WHERE cnae_fiscal_principal = '8630504'
     OR REGEXP_CONTAINS(LOWER(COALESCE(nome_fantasia,'')),
          r'odonto|dental|dentaria|dentario|dentes|ortodont|implantodont|periodont|endodont|bucal|sorriso')
),
-- 3) endereco de contador: quantos cnpj_basico DISTINTOS dividem o mesmo CEP+numero
--    (calculado sobre TODOS os estabelecimentos ativos do DF, nao so odonto)
enderecos AS (
  SELECT cep, numero, COUNT(DISTINCT cnpj_basico) AS n_cnpjs_no_endereco
  FROM `basedosdados.br_me_cnpj.estabelecimentos`
  WHERE data = PART AND sigla_uf = 'DF' AND situacao_cadastral = '2'
    AND cep IS NOT NULL AND numero IS NOT NULL
  GROUP BY 1,2
),
-- 4) numero de unidades ativas do mesmo cnpj_basico em todo o Brasil
unidades AS (
  SELECT cnpj_basico, COUNT(*) AS n_unidades_br, COUNT(DISTINCT sigla_uf) AS n_ufs
  FROM `basedosdados.br_me_cnpj.estabelecimentos`
  WHERE data = PART AND situacao_cadastral = '2'
    AND cnpj_basico IN (SELECT DISTINCT cnpj_basico FROM odonto)
  GROUP BY 1
),
-- 5) uma linha por cnpj_basico: prioriza matriz, depois a mais antiga
ranked AS (
  SELECT o.*,
    ROW_NUMBER() OVER (
      PARTITION BY o.cnpj_basico
      ORDER BY CASE WHEN o.identificador_matriz_filial='1' THEN 0 ELSE 1 END,
               o.data_inicio_atividade ASC
    ) AS rn,
    COUNT(*) OVER (PARTITION BY o.cnpj_basico) AS n_unidades_df
  FROM odonto o
)
SELECT
  r.cnpj_basico,
  r.cnpj,
  r.identificador_matriz_filial,
  emp.razao_social,
  r.nome_fantasia,
  r.cnae_fiscal_principal,
  d.descricao_subclasse           AS cnae_descricao,
  r.origem_recorte,
  r.cnae_fiscal_secundaria,
  TRIM(CONCAT(COALESCE(r.tipo_logradouro,''),' ',COALESCE(r.logradouro,''))) AS logradouro,
  r.numero, r.complemento, r.bairro, r.cep, r.id_municipio,
  CASE WHEN r.ddd_1 IS NOT NULL AND r.telefone_1 IS NOT NULL
       THEN CONCAT('(',r.ddd_1,') ',r.telefone_1) END AS telefone_1,
  CASE WHEN r.ddd_2 IS NOT NULL AND r.telefone_2 IS NOT NULL
       THEN CONCAT('(',r.ddd_2,') ',r.telefone_2) END AS telefone_2,
  LOWER(r.email) AS email,
  r.data_inicio_atividade,
  DATE_DIFF(CURRENT_DATE(), r.data_inicio_atividade, MONTH) AS idade_meses,
  emp.porte,
  emp.capital_social,
  emp.natureza_juridica,
  s.opcao_simples, s.data_opcao_simples,
  s.opcao_mei,
  r.n_unidades_df,
  u.n_unidades_br,
  u.n_ufs,
  ende.n_cnpjs_no_endereco,
  (ende.n_cnpjs_no_endereco >= 10) AS endereco_suspeito
FROM ranked r
JOIN `basedosdados.br_me_cnpj.empresas` emp
  ON emp.cnpj_basico = r.cnpj_basico AND emp.data = PART
LEFT JOIN `basedosdados.br_me_cnpj.simples` s ON s.cnpj_basico = r.cnpj_basico
LEFT JOIN unidades  u  ON u.cnpj_basico = r.cnpj_basico
LEFT JOIN enderecos ende ON ende.cep = r.cep AND ende.numero = r.numero
LEFT JOIN `basedosdados.br_bd_diretorios_brasil.cnae_2` d
  ON d.subclasse = r.cnae_fiscal_principal
WHERE r.rn = 1
  AND COALESCE(s.opcao_mei, 0) <> 1
  AND r.data_inicio_atividade < DATE_SUB(CURRENT_DATE(), INTERVAL 18 MONTH)
ORDER BY emp.capital_social DESC
