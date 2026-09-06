# Análises de presença digital — Top 15 odonto DF

Auditoria completa das 15 clínicas de maior propensão da fila `odonto-DF`, no padrão
`DebemSantos/Analise-Presenca-Digital.html`, organizada nas linhas de serviço da Oráculo.

Coleta de 18 e 19 de agosto de 2026.

## Os relatórios

| # | Clínica | Nota | Dores | Decisor |
|---|---|---|---|---|
| 01 | [Renove — Estética e Implantes Orais](01-renove-estetica-e-implantes-orais/Analise-Presenca-Digital.html) | 1,4/10 | 4 | Tiago Moura De Almeida |
| 02 | [Implantomed](02-implantomed/Analise-Presenca-Digital.html) | 6,4/10 | 3 | Sheila Mendes Batista |
| 03 | [Vital Implantes e Tratamentos Dentários](03-vital-implantes-e-tratamentos-dentarios/Analise-Presenca-Digital.html) | 6,6/10 | 5 | Cristhian Rogers Silva Domingos |
| 04 | [Osteo Implante](04-osteo-implante/Analise-Presenca-Digital.html) | 5,2/10 | 4 | Fabiano Cesar De Aguida |
| 05 | [Patrícia Pizzo Ortodontia](05-patricia-pizzo-ortodontia/Analise-Presenca-Digital.html) | 6,0/10 | 6 | Patricia Maria Pizzo Reis |
| 06 | [Instituto de Ortodontia Machado e Audição](06-instituto-de-ortodontia-machado-e-audicao/Analise-Presenca-Digital.html) | 4,8/10 | 6 | Rosario Casalenuovo Junior |
| 07 | [Everface Odontologia Especializada](07-everface-odontologia-especializada/Analise-Presenca-Digital.html) | 5,9/10 | 5 | Everton Luis Santos Da Rosa |
| 08 | [Orthos Taguatinga](08-orthos-taguatinga/Analise-Presenca-Digital.html) | 2,8/10 | 8 | Wells Moura Trigueiro |
| 09 | [Fábula Odontopediatria e Ortodontia](09-fabula-odontopediatria-e-ortodontia/Analise-Presenca-Digital.html) | 6,2/10 | 4 | Gabriela Mesquita Lopes |
| 10 | [Faces Odontologia Estética](10-faces-odontologia-estetica-ltda/Analise-Presenca-Digital.html) | 6,0/10 | 4 | Karina De Oliveira Sales Da Cruz |
| 11 | [IBI — Instituto Brasiliense de Implantodontia](11-ibi-instituto-brasiliense-de-implantodontia/Analise-Presenca-Digital.html) | 1,4/10 | 4 | Ronaldo Jose De Oliveira |
| 12 | [CRIE Odontologia](12-crie-odontologia/Analise-Presenca-Digital.html) | 6,8/10 | 2 | Frederico Goulart De Oliveira Silva |
| 13 | [Sallum — Odontologia Estética](13-sallum-odontologia-estetica/Analise-Presenca-Digital.html) | 2,1/10 | 8 | Gabriel De Souza Sallum |
| 14 | [Claudio Pinho Odontologia](14-claudio-pinho-odontologia/Analise-Presenca-Digital.html) | 3,7/10 | 8 | Ticyane De Oliveira Frota Pinho |
| 15 | [WV Implantodontia](15-wv-implantodontia/Analise-Presenca-Digital.html) | 1,7/10 | 4 | Walter Vasques Filho |

O consolidado com probabilidade de fechamento, dor por vertente e contato do decisor está em
[`../probabilidade-fechamento.md`](../probabilidade-fechamento.md).

## As quatro vertentes

Cada dor mapeada aponta para a vertente comercial que a resolve — é o que liga o relatório
à proposta. Total nas 15: **32 de tecnologia**, **31 de
gestão de redes sociais**, **12 de tráfego pago**.

1. **Tecnologia** — site, schema, medição, Google e atendente de IA no WhatsApp
2. **Gestão de redes sociais** — cadência, mix de formato, engajamento e chamada para ação
3. **Tráfego pago** — Meta Ad Library e rastros de pixel
4. **Presença consolidada** — Google, diretórios, consistência de NAP e benchmark

## Como foi coletado

| Pilar | Fonte | Observação |
|---|---|---|
| Cadastro e decisor | Receita Federal via BigQuery `basedosdados.br_me_cnpj` | Snapshot de 2026-01-11 |
| Site e SEO | Requisição HTTP direta à URL conhecida | Sem buscador no meio |
| Instagram | API interna com sessão logada no Chrome | ~120 posts por perfil |
| Google | Leitura do Maps e da SERP via Playwright | Sem chave da Places API |
| Anúncios | Meta Ad Library pública | Sem token de API |

## Regra que vale para tudo aqui

**Campo não coletado é `null` e aparece em `limitacoes`.** Nada é preenchido por inferência.
"Não localizei X" nunca vira "não tem X" — a diferença decide se um argumento de venda é
verdadeiro ou constrangedor.

## Reproduzir

```bash
python3 prospeccao/tools/presenca/semear.py        # cria as pastas e semeia CNPJ/decisor
python3 prospeccao/tools/presenca/rodar_sites.py   # vertente tecnologia
python3 prospeccao/tools/presenca/gerar.py         # gera os 15 HTML
python3 prospeccao/tools/presenca/probabilidade.py # gera o MD consolidado
python3 prospeccao/tools/presenca/schema.py <arquivo.json>   # valida um presenca.json
```

Instagram e Google exigem sessão de navegador e não estão nesse encadeamento.
