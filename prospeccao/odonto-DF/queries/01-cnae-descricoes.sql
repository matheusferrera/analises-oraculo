-- Descricoes oficiais dos CNAEs da familia 8630 (diretorio Base dos Dados)
SELECT subclasse, descricao_subclasse, classe, descricao_classe
FROM `basedosdados.br_bd_diretorios_brasil.cnae_2`
WHERE subclasse LIKE '863%'
ORDER BY subclasse
