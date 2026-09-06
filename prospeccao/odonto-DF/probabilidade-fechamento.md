# Probabilidade de fechamento — Top 15 odonto DF

Coleta de 18 e 19/08/2026. Fonte de cada número declarada em `analises/<clinica>/data/presenca.json`.

## Como ler a probabilidade

**Não é um percentual calibrado.** A Oráculo tem cerca de 13 clientes e nenhuma base de
negócios perdidos — não existe histórico para calibrar. Qualquer "72% de chance" seria
precisão inventada. O que há aqui é uma pontuação com a conta aberta:

```
probabilidade = propensão estrutural  ×  dor digital medida  ×  acessibilidade do decisor
```

- **Propensão estrutural** — capacidade de pagar, ticket do nicho, região, porte, maturidade (já calculada na fila)
- **Dor digital medida** — inverso da nota de presença digital, com piso: nota ruim sem capacidade não vira venda
- **Acessibilidade** — nome do decisor, WhatsApp, Instagram pessoal, decisão única ou compartilhada
- **Orçamento provado** — quem já mantém anúncio ativo na Meta ganha 18%: é o sinal mais forte
  de capacidade de pagar que existe, porque não depende de estimativa

Quando houver 50 a 100 negócios rotulados como ganhos ou perdidos, isso vira regressão
logística e aí sim sai percentual honesto.

## Ranking

| # | Clínica | Prob. | Faixa | Nota digital | O que trava |
|---|---|---|---|---|---|
| 1 | **Renove — Estética e Implantes Orais** | 0.84 | Muito alta | 1,4/10 | Nenhum canal próprio localizado |
| 2 | **IBI — Instituto Brasiliense de Implantodontia** | 0.81 | Muito alta | 1,4/10 | Nenhum canal próprio localizado |
| 3 | **WV Implantodontia** | 0.79 | Muito alta | 1,7/10 | Nenhum canal próprio localizado |
| 4 | **Sallum — Odontologia Estética** | 0.79 | Muito alta | 2,1/10 | O site existe no papel e não abre para ninguém |
| 5 | **Orthos Taguatinga** | 0.77 | Muito alta | 2,8/10 | O site existe no papel e não abre para ninguém |
| 6 | **Claudio Pinho Odontologia** | 0.66 | Alta | 3,7/10 | Site no ar, vitrine social ausente |
| 7 | **Instituto de Ortodontia Machado e Audição** | 0.63 | Alta | 4,8/10 | A conta parou há 47 dias |
| 8 | **Osteo Implante** | 0.54 | Alta | 5,2/10 | Estrutura espalhada, sem eixo |
| 9 | **Implantomed** | 0.48 | Média | 6,4/10 | Publica com constância e quase nunca pede a consulta |
| 10 | **Faces Odontologia Estética** | 0.48 | Média | 6,0/10 | Publica com constância e quase nunca pede a consulta |
| 11 | **Everface Odontologia Especializada** | 0.46 | Média | 5,9/10 | Publica com constância e quase nunca pede a consulta |
| 12 | **Patrícia Pizzo Ortodontia** | 0.45 | Média | 6,0/10 | Publica com constância e quase nunca pede a consulta |
| 13 | **Vital Implantes e Tratamentos Dentários** | 0.42 | Média | 6,6/10 | Base sólida, faltam as peças de conversão |
| 14 | **Fábula Odontopediatria e Ortodontia** | 0.38 | Baixa | 6,2/10 | Estrutura espalhada, sem eixo |
| 15 | **CRIE Odontologia** | 0.31 | Baixa | 6,8/10 | Publica com constância e quase nunca pede a consulta |

---
## Ficha por clínica

### 1. Renove — Estética e Implantes Orais

**Probabilidade: 0.84 — Muito alta**  ·  Nota digital 1,4/10  ·  EPP · Asa Norte · 14 anos

> Nenhum canal próprio localizado. Sem site e sem perfil, a clínica só existe onde terceiros decidem mostrá-la.

**A conta:** propensão estrutural 0.92 × dor 1.00 × acessibilidade 0.80 = **0.84**

**Dores mapeadas, por vertente:**

*Tecnologia (site, Google e atendente de IA no WhatsApp)*

- **Nenhum site próprio** — Nenhuma página no domínio da clínica foi localizada. A presença inteira depende de perfis e diretórios de terceiros
- **Sem Perfil da Empresa no Google** — Nenhuma ficha localizada na busca nem no Maps. A clínica não entra no pacote local, que é onde a busca por dentista começa

*Gestão de redes sociais*

- **Sem Instagram localizado** — Nenhum perfil encontrado para a clínica. Em odontologia estética ninguém fecha sem ver caso tratado

*Tráfego pago*

- **Não anuncia, ou anuncia sem rastrear** — Nenhum pixel da Meta nem tag do Google Ads no site. Alcance limitado ao orgânico, que já está caindo

**Números medidos:**

| | |
|---|---|
| Instagram | nenhum perfil localizado |
| Site | nenhum site próprio localizado |

**Como chegar no decisor:**

- **Tiago Moura De Almeida** — Sócio-Administrador
- Telefone: `(61) 9 8179-0097` (celular)
- WhatsApp: `+5561981790097`
- E-mail: `renove1209@gmail.com`
- Instagram pessoal: não localizado
- Endereço: SETOR SCN QUADRA 2 BLOCO D ENTRADA A SALA, 1209, ASA NORTE, CEP 70712000, Brasilia/DF

<details><summary><b>Limites desta coleta</b> (9 ressalvas)</summary>

- CANDIDATO NAO CONFIRMADO: existe no mesmo shopping uma ficha chamada apenas 'Renov' - nota 3,0 com 2 avaliacoes, categoria 'Clinica odontologica', Liberty Mall Torre B (SCN Q2 Bl D), tel (61) 99836-4626, SEM site vinculado e aparentemente NAO reivindicada (a SERP oferece 'E proprietario desta empresa?'). Nome e torre divergem do registro (Torre A, entrada A, sala 1209), entao NAO tratei como sendo a mesma empresa. Precisa de confirmacao por telefone antes de qualquer uso comercial.
- Confirmação de site próprio ficou inconclusiva.
- Contagem exata de fotos nao coletada: o Google Maps nao exibe o total sem abrir a galeria foto a foto. Registrado apenas se existe ou nao a aba 'Do proprietario'.
- Convencao do campo perfilEncontrado: true = ficha confirmada; 'nao_localizado' = busquei e nao encontrei ficha correspondente (nao equivale a afirmar que a empresa nao possui perfil).
- Instagram do decisor não localizado com confiança.
- Nao localizei ficha do Google com o nome 'Renove - Estetica e Implantes Orais' (CNPJ 16.803.567/0001-36, SCN Q2 Bl D entrada A sala 1209, Liberty Mall Torre A). Isso NAO equivale a afirmar que a empresa nao tem perfil.
- Nenhum perfil de Doctoralia, Facebook, LinkedIn, YouTube ou TikTok da clínica foi localizado — pode ser ausência real de presença nesses canais ou apenas indexação fraca de uma clínica pequena de unidade única.
- Nenhum site proprio localizado por busca web — CONFIRMAR no Chrome antes de afirmar ausencia.
- Recencia baseada nas avaliacoes visiveis na ordenacao padrao do Maps (relevancia), nao em ordenacao por data. E o piso da recencia real, nao o valor exato.

</details>

---

### 2. IBI — Instituto Brasiliense de Implantodontia

**Probabilidade: 0.81 — Muito alta**  ·  Nota digital 1,4/10  ·  DEMAIS · Asa Sul · 11 anos

> Nenhum canal próprio localizado. Sem site e sem perfil, a clínica só existe onde terceiros decidem mostrá-la.

**A conta:** propensão estrutural 0.89 × dor 1.00 × acessibilidade 0.80 = **0.81**

**Dores mapeadas, por vertente:**

*Tecnologia (site, Google e atendente de IA no WhatsApp)*

- **Nenhum site próprio** — Nenhuma página no domínio da clínica foi localizada. A presença inteira depende de perfis e diretórios de terceiros
- **Sem Perfil da Empresa no Google** — Nenhuma ficha localizada na busca nem no Maps. A clínica não entra no pacote local, que é onde a busca por dentista começa

*Gestão de redes sociais*

- **Sem Instagram localizado** — Nenhum perfil encontrado para a clínica. Em odontologia estética ninguém fecha sem ver caso tratado

*Tráfego pago*

- **Não anuncia, ou anuncia sem rastrear** — Nenhum pixel da Meta nem tag do Google Ads no site. Alcance limitado ao orgânico, que já está caindo

**Números medidos:**

| | |
|---|---|
| Instagram | nenhum perfil localizado |
| Site | nenhum site próprio localizado |

**Como chegar no decisor:**

- **Ronaldo Jose De Oliveira** — Sócio-Administrador
- Telefone: `(61) 3541-5562` (fixo)
- WhatsApp: `+556135415562`
- E-mail: `fortecon.contabilidade@gmail.com`
- Instagram pessoal: não localizado
- Endereço: SETOR SRTVS BLOCO, 0, BLOCO: K; SALA: 732; EDIF: EMBASSY TOWER;, ASA SUL, CEP 70340908, Brasilia/DF

<details><summary><b>Limites desta coleta</b> (10 ressalvas)</summary>

- Contato do CNPJ aponta para escritorio de contabilidade ou e compartilhado com outro CNPJ — confirmar o telefone real da clinica antes de ligar.
- Convencao do campo perfilEncontrado: true = ficha confirmada; 'nao_localizado' = busquei e nao encontrei ficha correspondente (nao equivale a afirmar que a empresa nao possui perfil).
- Existe risco real de confusão com a entidade IBIP (nome parecido, mesmo segmento, mesma cidade) — documentado acima para não ser usado por engano em material comercial.
- HOMONIMOS QUE NAO SAO O LEAD - nao usar como ficha do IBI: (a) 'Instituto Brasiliense de Implantodontia e Periodontia' (IBIP), SRTVS Centro Empresarial Brasilia Bloco A sala 310, tel (61) 98122-7123, sem avaliacoes - empresa diferente, CNPJ diferente; (b) 'IBI Odontologia -', St. J Norte QNJ 10, tel (61) 3475-6416, 4,9 com 8 avaliacoes - o telefone corresponde ao CNPJ 08.361.591/0001-34 ('IBI - Instituto Brasiliense de Implante', Taguatinga), tambem empresa distinta.
- Instagram do decisor Ronaldo José de Oliveira não localizado.
- Nao localizei ficha do Google para o IBI - Instituto Brasiliense de Implantodontia (CNPJ 22.580.698/0001-02, Asa Sul, Ed. Embassy Tower sala 732). Isso NAO equivale a afirmar que a empresa nao tem perfil.
- Nenhum site proprio localizado por busca web — CONFIRMAR no Chrome antes de afirmar ausencia.
- Não foi possível confirmar Facebook, LinkedIn, YouTube, TikTok ou Doctoralia próprios.
- Não foi possível confirmar site próprio da IBI (CNPJ 22.580.698/0001-02) — 'não localizei', não 'não tem'.
- Observacao de contexto (NAO e do lead): o IBIP aparece com DUAS fichas praticamente identicas no mesmo endereco e telefone - 'Instituto Brasiliense de Implantodontia e Periodontia' e 'Instituto Brasiliense de Implantodontia e Per', ambas sem avaliacoes. Vi as duas na mesma busca. Registrado so para evitar que alguem confunda essa duplicidade com o lead.

</details>

---

### 3. WV Implantodontia

**Probabilidade: 0.79 — Muito alta**  ·  Nota digital 1,7/10  ·  DEMAIS · Asa Sul · 12 anos

> Nenhum canal próprio localizado. Sem site e sem perfil, a clínica só existe onde terceiros decidem mostrá-la.

**A conta:** propensão estrutural 0.87 × dor 1.00 × acessibilidade 0.80 = **0.79**

**Dores mapeadas, por vertente:**

*Tecnologia (site, Google e atendente de IA no WhatsApp)*

- **Nenhum site próprio** — Nenhuma página no domínio da clínica foi localizada. A presença inteira depende de perfis e diretórios de terceiros
- **Sem Perfil da Empresa no Google** — Nenhuma ficha localizada na busca nem no Maps. A clínica não entra no pacote local, que é onde a busca por dentista começa

*Gestão de redes sociais*

- **Sem Instagram localizado** — Nenhum perfil encontrado para a clínica. Em odontologia estética ninguém fecha sem ver caso tratado

*Tráfego pago*

- **Não anuncia, ou anuncia sem rastrear** — Nenhum pixel da Meta nem tag do Google Ads no site. Alcance limitado ao orgânico, que já está caindo

**Números medidos:**

| | |
|---|---|
| Instagram | nenhum perfil localizado |
| Site | nenhum site próprio localizado |

**Como chegar no decisor:**

- **Walter Vasques Filho** — Sócio-Administrador
- Telefone: `(61) 3354-5337` (fixo)
- WhatsApp: `+556133545337`
- E-mail: `ecominacontabilidade@uol.com.br`
- Instagram pessoal: não localizado
- Endereço: QUADRA SRTVS QUADRA, 701, BLOCO K                   SALA  508, ASA SUL, CEP 70340908, Brasilia/DF

<details><summary><b>Limites desta coleta</b> (9 ressalvas)</summary>

- Contato do CNPJ aponta para escritorio de contabilidade ou e compartilhado com outro CNPJ — confirmar o telefone real da clinica antes de ligar.
- Convencao do campo perfilEncontrado: true = ficha confirmada; 'nao_localizado' = busquei e nao encontrei ficha correspondente (nao equivale a afirmar que a empresa nao possui perfil).
- Doctoralia, LinkedIn, YouTube e TikTok não localizados.
- Instagram pessoal do decisor Walter Vasques Filho não localizado.
- Nao localizei ficha do Google para WV Implantodontia (CNPJ 20.600.926/0001-25, SRTVS, Asa Sul) nem para o decisor Walter Vasques Filho. Isso NAO equivale a afirmar que nao existe perfil.
- Nenhum site proprio localizado por busca web — CONFIRMAR no Chrome antes de afirmar ausencia.
- O cadastro do projeto traz o endereco truncado ('QUADRA SRTVS QUADRA'), entao nao consegui montar uma busca por endereco completo como fiz com o IBI.
- Relação entre WV Implantodontia (CNPJ 20.600.926/0001-25, Asa Sul) e Centro de Reabilitação Oral Dr Walter Vasques (CNPJ 33.512.963/0001-23, Taguatinga) não foi confirmada — mesma família/decisor aparente, mas CNPJs distintos; tratar como entidades separadas até confirmação.
- Site próprio da WV Implantodontia não localizado — 'não localizei', não 'não tem'.

</details>

---

### 4. Sallum — Odontologia Estética

**Probabilidade: 0.79 — Muito alta**  ·  Nota digital 2,1/10  ·  DEMAIS · Asa Sul · 13 anos

> O site existe no papel e não abre para ninguém. Enquanto o domínio não responder, todo investimento em conteúdo devolve o paciente para o concorrente.

**A conta:** propensão estrutural 0.88 × dor 0.99 × acessibilidade 0.80 = **0.79**

**Dores mapeadas, por vertente:**

*Tecnologia (site, Google e atendente de IA no WhatsApp)*

- **O site não abre** — O domínio https://www.sallumodontologia.com.br/ não responde. O DNS do domínio não resolve, verificado em três clientes independentes. Todo clique vindo da busca cai numa porta fechada
- **Fichas duplicadas no Google** — Uma segunda ficha concorrente para o mesmo negócio. O Google divide avaliações e autoridade, e nenhuma acumula o suficiente

*Gestão de redes sociais*

- **Conta parada** — 68 dias desde a última publicação. O algoritmo reduz entrega de quem some, e recuperar custa mais que manter
- **Engajamento no chão** — 0,12% de engajamento nos últimos 90 dias. A maior parte dos seguidores já não vê o que é publicado
- **Publica sem pedir a consulta** — Apenas 4,2% dos posts tem chamada para ação. Audiência construída sem caminho para virar agendamento
- **Mix de formatos invertido** — 61 dos 120 posts da amostra são imagem estática. O maior volume de esforço vai para o formato de menor entrega
- **Cadência insuficiente** — 2 publicações em 90 dias. Abaixo do mínimo para o algoritmo manter entrega estável

*Tráfego pago*

- **Não anuncia, ou anuncia sem rastrear** — Nenhum pixel da Meta nem tag do Google Ads no site. Alcance limitado ao orgânico, que já está caindo

**Números medidos:**

| | |
|---|---|
| Instagram | @sallumodontologia · 10.608 seguidores |
| Última publicação | há 68 dias |
| Engajamento 90 dias | 0,12% |
| Posts nos últimos 90 dias | 2 |
| Posts com chamada para ação | 4,2% |
| Site | **https://www.sallumodontologia.com.br/ não abre** — URLError: <urlopen error [Errno 8] nodename nor servname provided, or not known> |

**Como chegar no decisor:**

- **Gabriel De Souza Sallum** — Sócio-Administrador
- Telefone: `(61) 3225-0655` (fixo)
- WhatsApp: `+556132250655`
- E-mail: `brendo@cclcontabilidade.com.br`
- Instagram pessoal: não localizado
- Endereço: QUADRA SGAS 616 CONJ A BLOCO B SALAS 231,233 E 235, SN, ASA SUL, CEP 70200760, Brasilia/DF

<details><summary><b>Limites desta coleta</b> (7 ressalvas)</summary>

- Contagem exata de fotos nao coletada: o Google Maps nao exibe o total sem abrir a galeria foto a foto. Registrado apenas se existe ou nao a aba 'Do proprietario'.
- Contato do CNPJ aponta para escritorio de contabilidade ou e compartilhado com outro CNPJ — confirmar o telefone real da clinica antes de ligar.
- E-mail institucional (contato@sallumodontologia.com.br) provavelmente também está fora do ar pela mesma quebra de DNS, mas isso não foi testado diretamente (sem envio de e-mail de teste).
- LinkedIn, YouTube e TikTok da clínica não localizados.
- Perfil essencialmente dormente: as avaliacoes visiveis tem 7-8 anos e as respostas do proprietario 6-7 anos. Nao percorri as 13 avaliacoes uma a uma, entao pode existir alguma mais recente fora da amostra visivel.
- Recencia baseada nas avaliacoes visiveis na ordenacao padrao do Maps (relevancia), nao em ordenacao por data. E o piso da recencia real, nao o valor exato.
- Site https://www.sallumodontologia.com.br/ nao respondeu a clientes HTTP (URLError: <urlopen error [Errno 8] nodename nor servname provided, or not known>) — CONFIRMAR no Chrome.

</details>

---

### 5. Orthos Taguatinga

**Probabilidade: 0.77 — Muito alta**  ·  Nota digital 2,8/10  ·  DEMAIS · Areal (Aguas Claras) · 16 anos

> O site existe no papel e não abre para ninguém. Enquanto o domínio não responder, todo investimento em conteúdo devolve o paciente para o concorrente.

**A conta:** propensão estrutural 0.90 × dor 0.90 × acessibilidade 0.90 = **0.77**

**Dores mapeadas, por vertente:**

*Tecnologia (site, Google e atendente de IA no WhatsApp)*

- **O site não abre** — O domínio https://orthosonline.com.br/ não responde. O DNS do domínio não resolve, verificado em três clientes independentes. Todo clique vindo da busca cai numa porta fechada
- **Fichas duplicadas no Google** — Uma segunda ficha concorrente para o mesmo negócio. O Google divide avaliações e autoridade, e nenhuma acumula o suficiente
- **Avaliações sem resposta** — Nenhuma resposta do proprietário nas avaliações visíveis. Resposta do dono é sinal de cuidado e pesa no ranqueamento local

*Gestão de redes sociais*

- **Conta parada** — 84 dias desde a última publicação. O algoritmo reduz entrega de quem some, e recuperar custa mais que manter
- **Engajamento no chão** — 0,49% de engajamento nos últimos 90 dias. A maior parte dos seguidores já não vê o que é publicado
- **Mix de formatos invertido** — 59 dos 120 posts da amostra são imagem estática. O maior volume de esforço vai para o formato de menor entrega
- **Cadência insuficiente** — 2 publicações em 90 dias. Abaixo do mínimo para o algoritmo manter entrega estável

*Tráfego pago*

- **Não anuncia, ou anuncia sem rastrear** — Nenhum pixel da Meta nem tag do Google Ads no site. Alcance limitado ao orgânico, que já está caindo

**Números medidos:**

| | |
|---|---|
| Instagram | @orthosbrasilia · 10.734 seguidores |
| Última publicação | há 84 dias |
| Engajamento 90 dias | 0,49% |
| Posts nos últimos 90 dias | 2 |
| Posts com chamada para ação | 18,3% |
| Site | **https://orthosonline.com.br/ não abre** — DNS nao resolve — confirmado em curl, Python e Chrome (18/08/2026) |

**Como chegar no decisor:**

- **Wells Moura Trigueiro** — Sócio-Administrador
- Decisão **compartilhada** entre dois sócios-administradores: alinhe os dois
- Telefone: `(61) 3901-2015` (fixo)
- WhatsApp: `+556139012015`
- E-mail: `taguatinga@orthosonline.com.br`
- Instagram pessoal: **@wellstrigueiro**
- Endereço: QUADRA QS 3 LOTES 03 A 09 LOJA, 06, AREAL (AGUAS CLARAS), CEP 71953000, Brasilia/DF

<details><summary><b>Limites desta coleta</b> (9 ressalvas)</summary>

- As duas fichas correspondem a enderecos diferentes (Aguas Claras e Taguatinga), entao nao sao duplicata do mesmo ponto - o problema e o nome identico, sem sufixo de unidade.
- Contagem exata de fotos nao coletada: o Google Maps nao exibe o total sem abrir a galeria foto a foto. Registrado apenas se existe ou nao a aba 'Do proprietario'.
- Encontrei uma possível página do Facebook (facebook.com/orthosodontologiabsb, 'Orthos Ortodontia e Estética'), mas não consegui confirmar que corresponde a esta unidade específica — a rede tem várias unidades em Brasília com nomes semelhantes, então preferi não afirmar o vínculo sem confirmação.
- Nenhum site proprio localizado por busca web — CONFIRMAR no Chrome antes de afirmar ausencia.
- Nenhuma das 3 avaliacoes visiveis na ficha de Aguas Claras tinha resposta, incluindo uma negativa detalhada de 1 mes atras. Nao percorri as 223 avaliacoes.
- Não localizei YouTube ou TikTok da clínica.
- Não localizei página Doctoralia específica da unidade Taguatinga/Águas Claras (só encontrei um 'Orthos Odontologia' homônimo em Parnamirim/RN, sem relação).
- Recencia baseada nas avaliacoes visiveis na ordenacao padrao do Maps (relevancia), nao em ordenacao por data. E o piso da recencia real, nao o valor exato.
- Site orthosonline.com.br fora do ar: DNS nao resolve em tres clientes independentes.

</details>

---

### 6. Claudio Pinho Odontologia

**Probabilidade: 0.66 — Alta**  ·  Nota digital 3,7/10  ·  DEMAIS · Asa Sul · 13 anos

> Site no ar, vitrine social ausente. Em odontologia estética a decisão passa por ver caso tratado, e não há onde ver.

**A conta:** propensão estrutural 0.88 × dor 0.79 × acessibilidade 0.90 = **0.66**

**Dores mapeadas, por vertente:**

*Tecnologia (site, Google e atendente de IA no WhatsApp)*

- **Site sem HTTPS** — A home responde em HTTP puro. O navegador marca como não seguro e o Google rebaixa na busca
- **Sem schema de negócio local** — Nenhum JSON-LD de LocalBusiness ou Dentist na home. Perde rich result na busca local, onde o paciente de implante procura
- **O site não mede nada** — Sem GA4 e sem Tag Manager no HTML. Impossível saber de onde vem paciente, logo impossível investir com critério
- **Sem agendamento na página** — Nenhum caminho de agendamento na home. Toda marcação depende de alguém atender no horário comercial
- **Ficha sem nenhuma avaliação** — O Perfil da Empresa existe e não tem avaliação alguma. Reputação zero na vitrine que mais pesa na decisão local
- **Avaliações sem resposta** — Nenhuma resposta do proprietário nas avaliações visíveis. Resposta do dono é sinal de cuidado e pesa no ranqueamento local

*Gestão de redes sociais*

- **Sem Instagram localizado** — Nenhum perfil encontrado para a clínica. Em odontologia estética ninguém fecha sem ver caso tratado

*Tráfego pago*

- **Não anuncia, ou anuncia sem rastrear** — Nenhum pixel da Meta nem tag do Google Ads no site. Alcance limitado ao orgânico, que já está caindo

**Números medidos:**

| | |
|---|---|
| Instagram | nenhum perfil localizado |
| Site | http://www.drclaudiopinho.com.br/ · WordPress |
| Falhas do site | sem HTTPS, sem schema local, sem analytics, sem pixel de anúncio |

**Como chegar no decisor:**

- **Ticyane De Oliveira Frota Pinho** — Sócio-Administrador
- Decisão **compartilhada** entre dois sócios-administradores: alinhe os dois
- Telefone: `(61) 3321-0999` (fixo)
- WhatsApp: `+556133210999`
- E-mail: `gerencia@drclaudiopinho.com.br`
- Instagram pessoal: **@claudio_pinho**
- Endereço: SETOR SETOR DE GRANDES AREAS SUL QD 614, S/N, CONJ  C                   SALA  40, ASA SUL, CEP 70200740, Brasilia/DF

<details><summary><b>Limites desta coleta</b> (8 ressalvas)</summary>

- A ficha existe mas esta NAO REIVINDICADA (o Maps oferece 'Reivindicar esta empresa') e com ZERO avaliacoes - nao ha nota nem historico para medir recencia.
- A página do Facebook encontrada (claudiopinhoestetica) está fortemente associada à Integrato Ensino Especializado (instituição de ensino do Dr. Cláudio), não exclusivamente à clínica — registrado como está, sem reinterpretar.
- Contagem exata de fotos nao coletada: o Google Maps nao exibe o total sem abrir a galeria foto a foto. Registrado apenas se existe ou nao a aba 'Do proprietario'.
- Contato do CNPJ aponta para escritorio de contabilidade ou e compartilhado com outro CNPJ — confirmar o telefone real da clinica antes de ligar.
- Doctoralia da clínica não localizado (site oficial nunca menciona Doctoralia).
- Instagram pessoal de Ticyane de Oliveira Frota Pinho não localizado.
- LinkedIn, YouTube e TikTok não localizados.
- O endereco da ficha (SGAS 614) bate com o cadastro do projeto (SGAS QD 614); a referencia 'SEPS 710/910' do briefing nao apareceu em nenhuma ficha. Nao localizei uma segunda ficha nesse endereco.

</details>

---

### 7. Instituto de Ortodontia Machado e Audição

**Probabilidade: 0.63 — Alta**  ·  Nota digital 4,8/10  ·  EPP · Asa Norte · 17 anos

> A conta parou há 47 dias. Alcance orgânico é cumulativo: cada semana parada custa entrega que não volta sozinha.

**A conta:** propensão estrutural 0.90 × dor 0.65 × acessibilidade 0.80 × orçamento provado 1,18 = **0.63**

> **Já investe em anúncio:** 2 criativos ativos na Meta, no ar há 9,2 meses. Não é preciso convencer que marketing vale — a verba já existe e já é gasta.

**Dores mapeadas, por vertente:**

*Tecnologia (site, Google e atendente de IA no WhatsApp)*

- **Sem schema de negócio local** — Nenhum JSON-LD de LocalBusiness ou Dentist na home. Perde rich result na busca local, onde o paciente de implante procura

*Gestão de redes sociais*

- **Conta parada** — 47 dias desde a última publicação. O algoritmo reduz entrega de quem some, e recuperar custa mais que manter
- **Engajamento no chão** — 0,0% de engajamento nos últimos 90 dias. A maior parte dos seguidores já não vê o que é publicado
- **Mix de formatos invertido** — 76 dos 120 posts da amostra são imagem estática. O maior volume de esforço vai para o formato de menor entrega
- **Cadência insuficiente** — 1 publicação em 90 dias. Abaixo do mínimo para o algoritmo manter entrega estável

*Tráfego pago*

- **Não anuncia, ou anuncia sem rastrear** — Nenhum pixel da Meta nem tag do Google Ads no site. Alcance limitado ao orgânico, que já está caindo

**Números medidos:**

| | |
|---|---|
| Instagram | @institutomachadobrasilia_ · 1.236 seguidores |
| Última publicação | há 47 dias |
| Engajamento 90 dias | 0,0% |
| Posts nos últimos 90 dias | 1 |
| Posts com chamada para ação | 15,8% |
| Site | https://institutomachado.com.br/ · WordPress + Elementor |
| Falhas do site | sem schema local, sem pixel de anúncio |

**Como chegar no decisor:**

- **Rosario Casalenuovo Junior** — Sócio-Administrador
- Telefone: `(61) 3225-0655` (fixo)
- WhatsApp: `+556132250655`
- E-mail: `brendo@cclcontabilidade.com.br`
- Instagram pessoal: não localizado
- Endereço: SETOR SHN QUADRA 2 BLOCO H, 30, LOJA  65 70 74            SLJ, ASA NORTE, CEP 70702905, Brasilia/DF

<details><summary><b>Limites desta coleta</b> (6 ressalvas)</summary>

- Contagem exata de fotos nao coletada: o Google Maps nao exibe o total sem abrir a galeria foto a foto. Registrado apenas se existe ou nao a aba 'Do proprietario'.
- Contato do CNPJ aponta para escritorio de contabilidade ou e compartilhado com outro CNPJ — confirmar o telefone real da clinica antes de ligar.
- Divergencia de nome entre a razao/nome comercial esperado ('Instituto de Ortodontia Machado e Audicao') e o nome da ficha ('Instituto Machado Odontologia Funcional Brasilia'). Considerei a mesma empresa pelo endereco (SHN Q2 Bloco H), mas vale confirmar.
- Endereço completo da unidade Brasília não é exibido no site institutomachado.com.br; a correspondência com SHN Quadra 2 Bloco H não foi confirmada de forma independente, apenas inferida pelo nome do diretor e CNPJ raiz.
- Não localizei página Doctoralia específica da unidade Brasília do Instituto Machado.
- Recencia baseada nas avaliacoes visiveis na ordenacao padrao do Maps (relevancia), nao em ordenacao por data. E o piso da recencia real, nao o valor exato.

</details>

---

### 8. Osteo Implante

**Probabilidade: 0.54 — Alta**  ·  Nota digital 5,2/10  ·  EPP · Taguatinga · 18 anos

> Estrutura espalhada, sem eixo. Os canais existem isolados e nenhum sustenta o outro.

**A conta:** propensão estrutural 0.91 × dor 0.60 × acessibilidade 0.65 × orçamento provado 1,18 = **0.54**

> **Já investe em anúncio:** 14 criativos ativos na Meta, no ar há 3,6 meses. Não é preciso convencer que marketing vale — a verba já existe e já é gasta.

**Dores mapeadas, por vertente:**

*Tecnologia (site, Google e atendente de IA no WhatsApp)*

- **Sem schema de negócio local** — Nenhum JSON-LD de LocalBusiness ou Dentist na home. Perde rich result na busca local, onde o paciente de implante procura
- **Avaliações sem resposta** — Nenhuma resposta do proprietário nas avaliações visíveis. Resposta do dono é sinal de cuidado e pesa no ranqueamento local

*Gestão de redes sociais*

- **Engajamento no chão** — 0,39% de engajamento nos últimos 90 dias. A maior parte dos seguidores já não vê o que é publicado
- **Cadência insuficiente** — 3 publicações em 90 dias. Abaixo do mínimo para o algoritmo manter entrega estável

**Números medidos:**

| | |
|---|---|
| Instagram | @osteoimplante · 6.924 seguidores |
| Última publicação | há 8 dias |
| Engajamento 90 dias | 0,39% |
| Posts nos últimos 90 dias | 3 |
| Posts com chamada para ação | 20,0% |
| Site | https://osteoimplante.com.br/ · WordPress + Elementor |
| Falhas do site | sem schema local |

**Como chegar no decisor:**

- **Fabiano Cesar De Aguida** — Sócio-Administrador
- Decisão **compartilhada** entre dois sócios-administradores: alinhe os dois
- Telefone: `(61) 3036-6116` (fixo)
- WhatsApp: `+556130366116`
- Instagram pessoal: não localizado
- Endereço: QUADRA QNC 07 LOTE 02 LOJAS 01, 02, 03 E 04, S/N, TERREO, TAGUATINGA, CEP 72115570, Brasilia/DF

<details><summary><b>Limites desta coleta</b> (11 ressalvas)</summary>

- A empresa tem um segundo CNPJ na Asa Norte (27.410.508/0001-14, SCN Quadra 2) na base do projeto. Nao localizei ficha do Google para essa unidade. 'Osteon - Centro de Implantodontia' NAO e a mesma empresa (nome e endereco diferentes) e nao deve ser contado como ficha da Osteo.
- Contagem exata de fotos nao coletada: o Google Maps nao exibe o total sem abrir a galeria foto a foto. Registrado apenas se existe ou nao a aba 'Do proprietario'.
- Contato do CNPJ aponta para escritorio de contabilidade ou e compartilhado com outro CNPJ — confirmar o telefone real da clinica antes de ligar.
- Convencao do campo perfilEncontrado: true = ficha confirmada; 'nao_localizado' = busquei e nao encontrei ficha correspondente (nao equivale a afirmar que a empresa nao possui perfil).
- DentMap não pôde ser verificado ao vivo (404 no fetch direto), apesar de aparecer em cache de busca.
- Doctoralia não localizado para esta clínica.
- Existência de uma segunda página de Facebook (osteoimplanteodontologia) não foi esclarecida — pode ser duplicata ou filial.
- LinkedIn não localizado (o único resultado com nome parecido, 'Osteo Implantes Ortopédicos', é uma empresa distinta de ortopedia, não odontologia — descartado).
- Nenhuma das 3 avaliacoes visiveis tinha resposta do proprietario; nao percorri as 60 avaliacoes, entao 'respostasDoProprietario: false' vale para a amostra visivel.
- Recencia baseada nas avaliacoes visiveis na ordenacao padrao do Maps (relevancia), nao em ordenacao por data. E o piso da recencia real, nao o valor exato.
- TikTok não localizado.

</details>

---

### 9. Implantomed

**Probabilidade: 0.48 — Média**  ·  Nota digital 6,4/10  ·  EPP · Asa Sul · 16 anos

> Publica com constância e quase nunca pede a consulta. A audiência existe, o caminho para virar agendamento não.

**A conta:** propensão estrutural 0.91 × dor 0.45 × acessibilidade 1.00 × orçamento provado 1,18 = **0.48**

> **Já investe em anúncio:** 3 criativos ativos na Meta. Não é preciso convencer que marketing vale — a verba já existe e já é gasta.

**Dores mapeadas, por vertente:**

*Tecnologia (site, Google e atendente de IA no WhatsApp)*

- **Sem schema de negócio local** — Nenhum JSON-LD de LocalBusiness ou Dentist na home. Perde rich result na busca local, onde o paciente de implante procura
- **Fichas duplicadas no Google** — Uma segunda ficha concorrente para o mesmo negócio. O Google divide avaliações e autoridade, e nenhuma acumula o suficiente

*Gestão de redes sociais*

- **Publica sem pedir a consulta** — Apenas 2,3% dos posts tem chamada para ação. Audiência construída sem caminho para virar agendamento

**Números medidos:**

| | |
|---|---|
| Instagram | @implantomed · 3.119 seguidores |
| Última publicação | há 1 dias |
| Engajamento 90 dias | 0,85% |
| Posts nos últimos 90 dias | 54 |
| Posts com chamada para ação | 2,3% |
| Site | https://implantomed.com.br/ · stack não identificada |
| Falhas do site | sem schema local |

**Como chegar no decisor:**

- **Sheila Mendes Batista** — Sócio-Administrador
- Telefone: `(61) 3202-3656` (fixo)
- WhatsApp: `+556132023656`
- E-mail: `contato@implantomed.com.br`
- Instagram pessoal: **@implantomed**
- Endereço: QUADRA SGAS 614, SN, CONJ  C                   SALA  53 55 TERREO, ASA SUL, CEP 70200740, Brasilia/DF

<details><summary><b>Limites desta coleta</b> (6 ressalvas)</summary>

- Contagem exata de fotos nao coletada: o Google Maps nao exibe o total sem abrir a galeria foto a foto. Registrado apenas se existe ou nao a aba 'Do proprietario'.
- Nao confirmei se 'Implantomed Senior' e uma unidade/servico deliberadamente separado ou uma ficha duplicada por engano - so a empresa pode dizer. O fato registrado e que sao duas fichas distintas no mesmo endereco.
- Nenhum LinkedIn ou TikTok da clínica localizado.
- Nota e nº de opiniões do Doctoralia são do perfil pessoal da Dra. Sheila (que É a técnica responsável/decisora), não necessariamente um perfil separado 'da clínica' no Doctoralia.
- Não há canal de YouTube próprio confirmado, apenas vídeos avulsos de terceiros.
- Recencia baseada nas avaliacoes visiveis na ordenacao padrao do Maps (relevancia), nao em ordenacao por data. E o piso da recencia real, nao o valor exato.

</details>

---

### 10. Faces Odontologia Estética

**Probabilidade: 0.48 — Média**  ·  Nota digital 6,0/10  ·  EPP · Aguas Claras · 10 anos

> Publica com constância e quase nunca pede a consulta. A audiência existe, o caminho para virar agendamento não.

**A conta:** propensão estrutural 0.89 × dor 0.50 × acessibilidade 0.80 × orçamento provado 1,18 = **0.48**

> **Já investe em anúncio:** 3 criativos ativos na Meta, no ar há 0,4 meses. Não é preciso convencer que marketing vale — a verba já existe e já é gasta.

**Dores mapeadas, por vertente:**

*Tecnologia (site, Google e atendente de IA no WhatsApp)*

- **Sem schema de negócio local** — Nenhum JSON-LD de LocalBusiness ou Dentist na home. Perde rich result na busca local, onde o paciente de implante procura
- **Avaliações sem resposta** — Nenhuma resposta do proprietário nas avaliações visíveis. Resposta do dono é sinal de cuidado e pesa no ranqueamento local

*Gestão de redes sociais*

- **Publica sem pedir a consulta** — Apenas 0,0% dos posts tem chamada para ação. Audiência construída sem caminho para virar agendamento

*Tráfego pago*

- **Não anuncia, ou anuncia sem rastrear** — Nenhum pixel da Meta nem tag do Google Ads no site. Alcance limitado ao orgânico, que já está caindo

**Números medidos:**

| | |
|---|---|
| Instagram | @facesodontologia · 2.938 seguidores |
| Última publicação | há 1 dias |
| Engajamento 90 dias | 0,79% |
| Posts nos últimos 90 dias | 11 |
| Posts com chamada para ação | 0,0% |
| Site | https://facesodontologia.com.br/ · WordPress + Elementor |
| Falhas do site | sem schema local, sem pixel de anúncio |

**Como chegar no decisor:**

- **Karina De Oliveira Sales Da Cruz** — Sócio-Administrador
- Telefone: `(61) 3011-2400` (fixo)
- WhatsApp: `+556130112400`
- E-mail: `contato@facesodontologia.com.br`
- Instagram pessoal: não localizado
- Endereço: AVENIDA DAS ARAUCARIAS LOTES 1835,1905,1955 E 2005 SALA, 551, EDIF  SHOP AGUAS CLARAS, AGUAS CLARAS, CEP 71936250, Brasilia/DF

<details><summary><b>Limites desta coleta</b> (5 ressalvas)</summary>

- Contagem exata de fotos nao coletada: o Google Maps nao exibe o total sem abrir a galeria foto a foto. Registrado apenas se existe ou nao a aba 'Do proprietario'.
- Nenhuma das 3 avaliacoes visiveis tinha resposta do proprietario - com 348 avaliacoes e nota 5,0, e o unico buraco visivel da ficha. Nao percorri todas as avaliacoes.
- Não localizei YouTube ou TikTok da clínica.
- Não localizei página do Facebook da clínica.
- Recencia baseada nas avaliacoes visiveis na ordenacao padrao do Maps (relevancia), nao em ordenacao por data. E o piso da recencia real, nao o valor exato.

</details>

---

### 11. Everface Odontologia Especializada

**Probabilidade: 0.46 — Média**  ·  Nota digital 5,9/10  ·  EPP · Asa Sul · 16 anos

> Publica com constância e quase nunca pede a consulta. A audiência existe, o caminho para virar agendamento não.

**A conta:** propensão estrutural 0.90 × dor 0.51 × acessibilidade 1.00 = **0.46**

**Dores mapeadas, por vertente:**

*Tecnologia (site, Google e atendente de IA no WhatsApp)*

- **Sem schema de negócio local** — Nenhum JSON-LD de LocalBusiness ou Dentist na home. Perde rich result na busca local, onde o paciente de implante procura
- **Avaliações sem resposta** — Nenhuma resposta do proprietário nas avaliações visíveis. Resposta do dono é sinal de cuidado e pesa no ranqueamento local
- **Categoria errada no Google** — Categoria declarada: Cirurgiao dentista. A ficha deixa de aparecer nas buscas do procedimento que a clínica de fato vende

*Gestão de redes sociais*

- **Publica sem pedir a consulta** — Apenas 4,5% dos posts tem chamada para ação. Audiência construída sem caminho para virar agendamento

*Tráfego pago*

- **Não anuncia, ou anuncia sem rastrear** — Nenhum pixel da Meta nem tag do Google Ads no site. Alcance limitado ao orgânico, que já está caindo

**Números medidos:**

| | |
|---|---|
| Instagram | @everface_odontologia · 886 seguidores |
| Última publicação | há 11 dias |
| Engajamento 90 dias | 1,59% |
| Posts nos últimos 90 dias | 15 |
| Posts com chamada para ação | 4,5% |
| Site | https://drevertondarosa.com/ · WordPress + Elementor |
| Falhas do site | sem schema local, sem pixel de anúncio |

**Como chegar no decisor:**

- **Everton Luis Santos Da Rosa** — Sócio-Administrador
- Telefone: `(61) 3326-3361` (fixo)
- WhatsApp: `+556133263361`
- E-mail: `institutoer@gmail.com`
- Instagram pessoal: **@everton_da_rosa**
- Endereço: SETOR SRTVS QUADRA 701 CONJUNTO L BLOCO 2, S/N, SALA  531                 EDIF  ASSIS CHATEAUBRIAND, ASA SUL, CEP 70340906, Brasilia/DF

<details><summary><b>Limites desta coleta</b> (6 ressalvas)</summary>

- Contagem exata de fotos nao coletada: o Google Maps nao exibe o total sem abrir a galeria foto a foto. Registrado apenas se existe ou nao a aba 'Do proprietario'.
- Não localizei LinkedIn, YouTube ou TikTok da clínica.
- O site vinculado e o dominio pessoal do profissional (drevertondarosa.com), nao um dominio da marca Everface. Nao verifiquei se existe site proprio da Everface.
- Recencia baseada nas avaliacoes visiveis na ordenacao padrao do Maps (relevancia), nao em ordenacao por data. E o piso da recencia real, nao o valor exato.
- URL completa do Facebook (facebook.com/people/Dr-Everton-da-Rosa/) veio truncada na fonte, sem o ID numérico final — pode não abrir direto sem busca adicional.
- categoriaCorreta marcada como false porque a ficha esta como 'Cirurgiao dentista' (categoria de profissional) e nao como clinica/especialidade - avaliacao minha, nao um dado do Google.

</details>

---

### 12. Patrícia Pizzo Ortodontia

**Probabilidade: 0.45 — Média**  ·  Nota digital 6,0/10  ·  EPP · Norte (Aguas Claras) · 13 anos

> Publica com constância e quase nunca pede a consulta. A audiência existe, o caminho para virar agendamento não.

**A conta:** propensão estrutural 0.90 × dor 0.50 × acessibilidade 1.00 = **0.45**

**Dores mapeadas, por vertente:**

*Tecnologia (site, Google e atendente de IA no WhatsApp)*

- **Site nao mede nada** — Sem GA4, sem GTM, sem pixel da Meta e sem tag do Google Ads no HTML. Impossivel saber de onde vem paciente, entao impossivel investir com criterio
- **Sem schema de negocio local** — Nenhum JSON-LD de LocalBusiness/Dentist na home. Perde rich result na busca local, onde o paciente de implante procura

*Gestão de redes sociais*

- **Mix de formatos invertido** — 69% dos posts sao imagem estatica, o formato com ER de 0,09% — nove vezes pior que o carrossel (0,81%). O maior volume de esforco esta no formato que menos entrega alcance
- **Cadencia em queda livre** — 13 posts em janeiro contra 2 em agosto: queda de 85% no ano. Perda de alcance composta — o algoritmo reduz entrega de quem some
- **Publica sem pedir a consulta** — Apenas 3,7% dos 108 posts tem qualquer chamada para acao. Audiencia de 10 mil pessoas sem caminho para virar agendamento

*Tráfego pago*

- **Nao anuncia** — Nenhum pixel de anuncio instalado; mediana de 708 plays por Reel para 10 mil seguidores. Alcance limitado ao organico, que ja esta caindo com a cadencia

**Números medidos:**

| | |
|---|---|
| Instagram | @odontopatriciapizzo · 10.146 seguidores |
| Última publicação | há 2 dias |
| Engajamento 90 dias | 0,51% |
| Posts nos últimos 90 dias | 9 |
| Posts com chamada para ação | 3,7% |
| Site | https://patriciapizzo.com.br/ · WordPress + Elementor |
| Falhas do site | sem schema local, sem analytics, sem pixel de anúncio |

**Como chegar no decisor:**

- **Patricia Maria Pizzo Reis** — Sócio-Administrador
- Telefone: `(61) 3024-1777` (fixo)
- WhatsApp: `+556130241777`
- E-mail: `patriciapizzoreis@gmail.com`
- Instagram pessoal: **@odontopatriciapizzo**
- Endereço: RUA 5 NORTE LOTE, 3, SALA  414, NORTE (AGUAS CLARAS), CEP 71907720, Brasilia/DF

<details><summary><b>Limites desta coleta</b> (8 ressalvas)</summary>

- Amostra de 108 dos 2.319 posts (cobre out/2025 a ago/2026).
- Contagem exata de fotos nao coletada: o Google Maps nao exibe o total sem abrir a galeria foto a foto. Registrado apenas se existe ou nao a aba 'Do proprietario'.
- Doctoralia não localizado para o nome 'Patricia Pizzo' apesar de busca direta no site (www.doctoralia.com.br/pesquisa?q=Patricia+Pizzo) — parece não ter perfil na plataforma, mas não é 100% conclusivo dado o volume de nomes semelhantes na base.
- Instagram do decisor é a mesma conta de negócio/pessoal já usada pela clínica — não há perfil pessoal distinto identificado.
- LinkedIn não localizado.
- Nao investiguei a causa da ausencia no pacote local (pode ser categoria primaria, proximidade do centroide da busca ou relevancia por termo).
- Recencia baseada nas avaliacoes visiveis na ordenacao padrao do Maps (relevancia), nao em ordenacao por data. E o piso da recencia real, nao o valor exato.
- TikTok não localizado.

</details>

---

### 13. Vital Implantes e Tratamentos Dentários

**Probabilidade: 0.42 — Média**  ·  Nota digital 6,6/10  ·  EPP · Asa Norte · 18 anos

> Base sólida, faltam as peças de conversão. O trabalho aqui é de ajuste fino, não de reconstrução.

**A conta:** propensão estrutural 0.91 × dor 0.43 × acessibilidade 0.80 × orçamento provado 1,18 = **0.42**

> **Já investe em anúncio:** 25 criativos ativos na Meta, no ar há 2,1 meses. Não é preciso convencer que marketing vale — a verba já existe e já é gasta.

**Dores mapeadas, por vertente:**

*Tecnologia (site, Google e atendente de IA no WhatsApp)*

- **Sem schema de negócio local** — Nenhum JSON-LD de LocalBusiness ou Dentist na home. Perde rich result na busca local, onde o paciente de implante procura

*Gestão de redes sociais*

- **Engajamento no chão** — 0,16% de engajamento nos últimos 90 dias. A maior parte dos seguidores já não vê o que é publicado
- **Publica sem pedir a consulta** — Apenas 5,8% dos posts tem chamada para ação. Audiência construída sem caminho para virar agendamento
- **Mix de formatos invertido** — 56 dos 120 posts da amostra são imagem estática. O maior volume de esforço vai para o formato de menor entrega

*Tráfego pago*

- **Não anuncia, ou anuncia sem rastrear** — Nenhum pixel da Meta nem tag do Google Ads no site. Alcance limitado ao orgânico, que já está caindo

**Números medidos:**

| | |
|---|---|
| Instagram | @vitalimplantes · 18.419 seguidores |
| Última publicação | há 2 dias |
| Engajamento 90 dias | 0,16% |
| Posts nos últimos 90 dias | 14 |
| Posts com chamada para ação | 5,8% |
| Site | https://www.vitalimplantes.com.br/ · stack não identificada |
| Falhas do site | sem schema local, sem pixel de anúncio |

**Como chegar no decisor:**

- **Cristhian Rogers Silva Domingos** — Sócio-Administrador
- Telefone: `(61) 3032-5666` (fixo)
- WhatsApp: `+556130325666`
- E-mail: `adm@vitalclinica.com.br`
- Instagram pessoal: não localizado
- Endereço: CONJUNTO SETOR DE DIVERSOES NORTE CONJUNTO A, S/N, SALA  5075 - 5077 - 5079  SALA  5116 - 5118, ASA NORTE, CEP 70077900, Brasilia/DF

<details><summary><b>Limites desta coleta</b> (7 ressalvas)</summary>

- As duas unidades usam o mesmo telefone (61) 3030-5757 na ficha; nao verifiquei se ha desvio por unidade.
- Contagem exata de fotos nao coletada: o Google Maps nao exibe o total sem abrir a galeria foto a foto. Registrado apenas se existe ou nao a aba 'Do proprietario'.
- Doctoralia da clínica ainda não tem avaliações publicadas ('Opiniões em breve'), então não há nota.
- Existência de duas URLs de Facebook (vitalimplantes vs vitalimplantesetratamentosdentarios) não foi totalmente esclarecida — registrei a mais recorrente como principal.
- Ha avaliacao negativa grave e recente (2 semanas) na unidade Taguatinga relatando tratamento pago e nao concluido - li o inicio do texto, nao a resposta completa da clinica.
- Recencia baseada nas avaliacoes visiveis na ordenacao padrao do Maps (relevancia), nao em ordenacao por data. E o piso da recencia real, nao o valor exato.
- TikTok não localizado.

</details>

---

### 14. Fábula Odontopediatria e Ortodontia

**Probabilidade: 0.38 — Baixa**  ·  Nota digital 6,2/10  ·  DEMAIS · Asa Norte · 18 anos

> Estrutura espalhada, sem eixo. Os canais existem isolados e nenhum sustenta o outro.

**A conta:** propensão estrutural 0.89 × dor 0.47 × acessibilidade 0.80 = **0.38**

**Dores mapeadas, por vertente:**

*Tecnologia (site, Google e atendente de IA no WhatsApp)*

- **Sem schema de negócio local** — Nenhum JSON-LD de LocalBusiness ou Dentist na home. Perde rich result na busca local, onde o paciente de implante procura

*Gestão de redes sociais*

- **Engajamento no chão** — 0,37% de engajamento nos últimos 90 dias. A maior parte dos seguidores já não vê o que é publicado
- **Mix de formatos invertido** — 61 dos 120 posts da amostra são imagem estática. O maior volume de esforço vai para o formato de menor entrega

*Tráfego pago*

- **Não anuncia, ou anuncia sem rastrear** — Nenhum pixel da Meta nem tag do Google Ads no site. Alcance limitado ao orgânico, que já está caindo

**Números medidos:**

| | |
|---|---|
| Instagram | @fabulaodonto · 6.975 seguidores |
| Última publicação | há 6 dias |
| Engajamento 90 dias | 0,37% |
| Posts nos últimos 90 dias | 12 |
| Posts com chamada para ação | 14,2% |
| Site | https://fabulaodonto.com.br/ · WordPress + Elementor |
| Falhas do site | sem schema local, sem pixel de anúncio |

**Como chegar no decisor:**

- **Gabriela Mesquita Lopes** — Sócio-Administrador
- Telefone: `(61) 9 9967-5834` (celular)
- WhatsApp: `+5561999675834`
- E-mail: `gabimlopes@gmail.com`
- Instagram pessoal: não localizado
- Endereço: SETOR SETOR COMERCIAL NORTE, QUADRA 02, BLOCO D, ENTRADA B, SN, SALA  1108 1110 E 1111, ASA NORTE, CEP 70712903, Brasilia/DF

<details><summary><b>Limites desta coleta</b> (6 ressalvas)</summary>

- A categoria exibida variou entre 'Clinica de odontopediatria' e 'Odontopediatra' em consultas diferentes - o Google alterna a categoria mostrada conforme o termo buscado. Nao e possivel ler a categoria primaria real sem acesso ao painel do proprietario.
- Contagem exata de fotos nao coletada: o Google Maps nao exibe o total sem abrir a galeria foto a foto. Registrado apenas se existe ou nao a aba 'Do proprietario'.
- Nao abri a ficha da unidade Asa Norte em detalhe; os dados dela vieram da listagem do Maps.
- Não localizei LinkedIn ou TikTok da clínica.
- Não localizei URL de página Doctoralia dedicada à clínica (buscas indicam que ela aparece indexada nas listagens de odontopediatria de Brasília, mas não achei a ficha própria com nota/opiniões).
- Recencia baseada nas avaliacoes visiveis na ordenacao padrao do Maps (relevancia), nao em ordenacao por data. E o piso da recencia real, nao o valor exato.

</details>

---

### 15. CRIE Odontologia

**Probabilidade: 0.31 — Baixa**  ·  Nota digital 6,8/10  ·  DEMAIS · Asa Norte · 22 anos

> Publica com constância e quase nunca pede a consulta. A audiência existe, o caminho para virar agendamento não.

**A conta:** propensão estrutural 0.88 × dor 0.40 × acessibilidade 0.70 = **0.31**

**Dores mapeadas, por vertente:**

*Tecnologia (site, Google e atendente de IA no WhatsApp)*

- **Sem schema de negócio local** — Nenhum JSON-LD de LocalBusiness ou Dentist na home. Perde rich result na busca local, onde o paciente de implante procura

*Gestão de redes sociais*

- **Publica sem pedir a consulta** — Apenas 4,2% dos posts tem chamada para ação. Audiência construída sem caminho para virar agendamento

**Números medidos:**

| | |
|---|---|
| Instagram | @crieodontologia · 5.197 seguidores |
| Última publicação | há 4 dias |
| Engajamento 90 dias | 1,02% |
| Posts nos últimos 90 dias | 28 |
| Posts com chamada para ação | 4,2% |
| Site | https://www.crieodontologia.com.br/ · WordPress + Elementor |
| Falhas do site | sem schema local |

**Como chegar no decisor:**

- **Frederico Goulart De Oliveira Silva** — Sócio-Administrador
- Decisão **compartilhada** entre dois sócios-administradores: alinhe os dois
- Telefone: `(61) 3326-4245` (fixo)
- WhatsApp: `+556133264245`
- E-mail: `admin@crieodontologia.com.br`
- Instagram pessoal: não localizado
- Endereço: SETOR SMHN, 44, QUADRA02                  BLOCO C                   SALA  601 602 608 E 609   EDIF  DR. CRISPIM, ASA NORTE, CEP 70710100, Brasilia/DF

<details><summary><b>Limites desta coleta</b> (7 ressalvas)</summary>

- Contagem exata de fotos nao coletada: o Google Maps nao exibe o total sem abrir a galeria foto a foto. Registrado apenas se existe ou nao a aba 'Do proprietario'.
- LinkedIn: URL localizada via busca, mas o fetch direto retornou HTTP 429 (rate limit) — não foi possível confirmar seguidores/atividade recentes.
- Nao investiguei a causa da ausencia no pacote local para o termo generico.
- Nota do Doctoralia aparece como 0 estrelas com apenas 1 opinião (de 2015, texto elogioso) — possível anomalia de exibição da plataforma; registrado literalmente como veio, não corrigido por inferência.
- O cadastro do projeto lista a 2a unidade como 'CRIE LOUNGE' no SMHN Q2 Bloco B consultorios 207; a ficha do Google diz Sala 210. Nao verifiquei qual esta correto.
- Recencia baseada nas avaliacoes visiveis na ordenacao padrao do Maps (relevancia), nao em ordenacao por data. E o piso da recencia real, nao o valor exato.
- YouTube e TikkTok mencionados de forma genérica em resultados de busca ("Crie incentiva seguir no YouTube"), mas nenhuma URL de canal específica foi localizada — ficou em branco.

</details>

---

---

# Fichas resumidas — posições 16 a 30

Coleta leve: site, Instagram, Google e contato do decisor. **Não é auditoria completa** —
sem métricas de engajamento, sem análise de SEO técnico e sem leitura de anúncios.
Serve para priorizar quem merece o relatório completo na próxima rodada.

| # | Clínica | Prob. | Google | Site | Instagram |
|---|---|---|---|---|---|
| 29 | **Eduardo Burgel Periodontia e Implantes** | 0.80 | 4.2 · 5 aval. | não localizado | — |
| 25 | **Aquarium Odontologia e Harmonização** | 0.73 | não localizado | não localizado | — |
| 21 | **Brasília Implantes** | 0.46 | 5.0 · 1 aval. | não localizado | — |
| 17 | **Centro Clínico de Ortodontia Gomide** | 0.36 | 4.9 · 41 aval. | não localizado | — |
| 30 | **DF Implantes** | 0.33 | 5.0 · 3 aval. | não localizado | @dfimplante |
| 26 | **Prime Estética Facial** | 0.29 | 5.0 · 33 aval. | **fora do ar** | @primeesteticafacial |
| 28 | **Amazing HOF** | 0.26 | 5.0 · 32 aval. | **fora do ar** | @amazinghof |
| 16 | **Talita Chimeli Odontologia Estética Avançada** | 0.25 | 5.0 · 76 aval. | ativo | @talitachimeli |
| 18 | **Bicalho Ortodontia** | 0.25 | 5.0 · 121 aval. | ativo | @bicalho.ortodontia |
| 19 | **Implant Center** | 0.25 | 5.0 · 127 aval. | ativo | @implantcenterdf |
| 20 | **CIR Premier** | 0.25 | 4.8 · 374 aval. | ativo | @cirbyaureliobelas |
| 23 | **Implanto** | 0.24 | 5.0 · 16 aval. | ativo | @implantodontologia |
| 27 | **Moya Ortodontia e Ortopedia Facial** | 0.24 | 5.0 · 25 aval. | ativo | @drjoaomoya |
| 24 | **SIGA Odontologia Especializada** | 0.22 | 4.9 · 711 aval. | ativo | @sigaodontologiadf |
| 22 | **Ortho Life** | **DESQUALIFICADA** | 3.0 · 2 aval. | não localizado | — |

## Detalhe

### 29. Eduardo Burgel Periodontia e Implantes

**Probabilidade estimada: 0.80** · Asa Norte · 13 anos

**O que trava:** nenhum site localizado; nenhum Instagram localizado; apenas 5 avaliações no Google

- Google: 4.2 com 5 avaliações
- Site: não localizado
- Instagram: não localizado

**Contato:**

- **Eduardo De Araujo Burgel** — Sócio-Administrador
- Telefone: `(61) 3081-8888`
- WhatsApp: `+556130818888`
- E-mail: `eduardoburgel.implantes@gmail.com`
- Instagram pessoal: **@eduardo.burgel**

<details><summary>Limites (1)</summary>

- Instagram da clinica nao localizado - so foi encontrada a conta pessoal do decisor.

</details>

---

### 25. Aquarium Odontologia e Harmonização

**Probabilidade estimada: 0.73** · Asa Sul · 28 anos

**O que trava:** nenhum site localizado; nenhum Instagram localizado; nenhum Perfil da Empresa localizado

- Google: perfil não localizado
- Site: não localizado
- Instagram: não localizado

**Contato:**

- **Rogerio Rocha Saud** — Sócio-Administrador
- Telefone: `(61) 9 9988-1987`
- WhatsApp: `+5561999881987`
- E-mail: `saudrr@gmail.com`
- Instagram pessoal: não localizado

<details><summary>Limites (3)</summary>

- Perfil da Empresa nao localizado - isso NAO comprova que nao exista, apenas que nao apareceu nas buscas por nome e por endereco.
- Instagram da clinica nao localizado.
- Instagram pessoal do decisor nao localizado (busca por 'rogerio saud' so retornou homonimos de outras areas).

</details>

---

### 21. Brasília Implantes

**Probabilidade estimada: 0.46**

**O que trava:** nenhum site localizado; nenhum Instagram localizado; apenas 1 avaliações no Google

- Google: 5.0 com 1 avaliações
- Site: não localizado
- Instagram: não localizado

**Contato:**

- **decisor não identificado**
- Instagram pessoal: não localizado

<details><summary>Limites (2)</summary>

- Instagram da clinica nao localizado - o homonimo @brasiliaimplantesdf e de Nucleo Bandeirante e foi descartado por divergencia de endereco.
- Instagram pessoal do decisor nao localizado.

</details>

---

### 17. Centro Clínico de Ortodontia Gomide

**Probabilidade estimada: 0.36**

**O que trava:** nenhum site localizado; nenhum Instagram localizado

- Google: 4.9 com 41 avaliações
- Site: não localizado
- Instagram: não localizado

**Contato:**

- **decisor não identificado**
- Instagram pessoal: não localizado

<details><summary>Limites (3)</summary>

- Instagram da clinica nao localizado (busca por 'ortodontia gomide' e 'gomide odontologia brasilia' no Instagram nao retornou o perfil) - nao confirma ausencia.
- Instagram pessoal dos decisores nao localizado.
- O bloco no Google (Bloco I) difere do bloco no CNPJ (Bloco F); mesma quadra, mesmo CEP e mesma sala 217, mas a correspondencia nao e literal.

</details>

---

### 30. DF Implantes

**Probabilidade estimada: 0.33** · Setor Sudoeste · 1 anos

**O que trava:** nenhum site localizado; apenas 3 avaliações no Google

- Google: 5.0 com 3 avaliações
- Site: não localizado
- Instagram: @dfimplante · 2.119 seguidores

**Contato:**

- **decisor não identificado**
- Telefone: `(61) 9 9633-3328`
- WhatsApp: `+5561996333328`
- E-mail: `dfimplantes2024@gmail.com`
- Instagram pessoal: não localizado

<details><summary>Limites (2)</summary>

- A sala no Google (Sl 522) difere da sala no CNPJ (consultorio 421); mesmo predio (Edificio Pacini), mesma quadra.
- Instagram pessoal do decisor nao localizado.

</details>

---

### 26. Prime Estética Facial

**Probabilidade estimada: 0.29**

**O que trava:** site fora do ar

- Google: 5.0 com 33 avaliações
- Site: https://primeesteticafacial.com.br/ (status None)
- Instagram: @primeesteticafacial · 3.343 seguidores

**Contato:**

- **decisor não identificado**
- Instagram pessoal: **@dr.julioevangelista**

<details><summary>Limites (2)</summary>

- Nao foi localizado Perfil da Empresa sob o nome 'Prime Estetica Facial' - o perfil encontrado esta sob o nome do socio.
- Seguidores de @dr.julioevangelista vem arredondados como '14K'; valor aproximado.

</details>

---

### 28. Amazing HOF

**Probabilidade estimada: 0.26** · Sul (Aguas Claras) · 2 anos

**O que trava:** site fora do ar

- Google: 5.0 com 32 avaliações
- Site: https://www.dravaniamedeiros.com.br/ (status None)
- Instagram: @amazinghof · 23.000 seguidores

**Contato:**

- **decisor não identificado**
- Telefone: `(61) 9 8277-7704`
- WhatsApp: `+5561982777704`
- E-mail: `vaniamedeiross@gmail.com`
- Instagram pessoal: **@dravaniamedeiros**

<details><summary>Limites (1)</summary>

- Seguidores de @amazinghof e @dravaniamedeiros vem arredondados pelo Instagram como '23K' e '15K'; valores aproximados.

</details>

---

### 16. Talita Chimeli Odontologia Estética Avançada

**Probabilidade estimada: 0.25** · Asa Sul · 13 anos

- Google: 5.0 com 76 avaliações
- Site: https://talitachimeli.com.br/ (status 200)
- Instagram: @talitachimeli · 29.156 seguidores

**Contato:**

- **Talita Baumgratz Cachapuz Chimeli** — Sócio-Administrador
- Telefone: `(61) 9 8496-7376`
- WhatsApp: `+5561984967376`
- E-mail: `joaquimpinheiro@gmail.com`
- Instagram pessoal: **@talitachimeli**

<details><summary>Limites (1)</summary>

- Nao foi verificado se talitachimeli.com (Chimeli Dental Studio) pertence ao mesmo CNPJ ou e outra pessoa juridica.

</details>

---

### 18. Bicalho Ortodontia

**Probabilidade estimada: 0.25** · Asa Norte · 20 anos

- Google: 5.0 com 121 avaliações
- Site: https://bicalhoortodontia.com.br/ (status 200)
- Instagram: @bicalho.ortodontia · 2.720 seguidores

**Contato:**

- **Rafael De Faria Bicalho** — Sócio-Administrador
- Telefone: `(61) 3328-0072`
- WhatsApp: `+556133280072`
- E-mail: `jaime.bicalho@terra.com.br`
- Instagram pessoal: **@rafael.fbicalho**

---

### 19. Implant Center

**Probabilidade estimada: 0.25** · Asa Sul · 27 anos

- Google: 5.0 com 127 avaliações
- Site: https://implantcenter.com.br/ (status 200)
- Instagram: @implantcenterdf · 2.325 seguidores

**Contato:**

- **George Furtado Guimaraes** — Sócio-Administrador
- Telefone: `(61) 3224-2882`
- WhatsApp: `+556132242882`
- E-mail: `adm@implantcenter.com.br`
- Instagram pessoal: **@implantcenterdf** (confiança media)

<details><summary>Limites (1)</summary>

- Nao foi localizada conta pessoal do decisor separada da conta da clinica.

</details>

---

### 20. CIR Premier

**Probabilidade estimada: 0.25** · Lago Sul · 32 anos

- Google: 4.8 com 374 avaliações
- Site: https://www.cir.com.br/ (status 200)
- Instagram: @cirbyaureliobelas · 79.000 seguidores

**Contato:**

- **Aurelio Belas Lustosa** — Sócio-Administrador
- Telefone: `(61) 3346-9001`
- WhatsApp: `+556133469001`
- E-mail: `contato@cir.com.br`
- Instagram pessoal: **@aureliobelaslustosa**

<details><summary>Limites (1)</summary>

- Seguidores do @cirbyaureliobelas vem arredondados pelo Instagram como '79K'; o valor 79000 e aproximado.

</details>

---

### 23. Implanto

**Probabilidade estimada: 0.24** · Asa Sul · 16 anos

- Google: 5.0 com 16 avaliações
- Site: https://implanto.com.br/ (status 200)
- Instagram: @implantodontologia · 1.268 seguidores

**Contato:**

- **Sheila Mendes Batista** — Sócio-Administrador
- Telefone: `(61) 3202-3656`
- WhatsApp: `+556132023656`
- E-mail: `contato@implantomed.com.br`
- Instagram pessoal: não localizado

<details><summary>Limites (1)</summary>

- Instagram pessoal do decisor nao localizado.

</details>

---

### 27. Moya Ortodontia e Ortopedia Facial

**Probabilidade estimada: 0.24** · Asa Norte · 24 anos

- Google: 5.0 com 25 avaliações
- Site: https://moyaortodontia.com.br/ (status 200)
- Instagram: @drjoaomoya · 3.815 seguidores

**Contato:**

- **Daniela De Assis Moya Yokomizo** — Sócio-Administrador
- Telefone: `(61) 3202-5236`
- WhatsApp: `+556132025236`
- E-mail: `atendimento@marf.com.br`
- Instagram pessoal: **@drjoaomoya** (confiança media)

<details><summary>Limites (2)</summary>

- Instagram pessoal de Daniela de Assis Moya Yokomizo nao localizado - o perfil @danielamoya encontrado e de uma 'Consultora de Marketing' e nao foi atribuido por risco de homonimo.
- Nao foi possivel determinar qual das duas fichas do Google e a principal.

</details>

---

### 24. SIGA Odontologia Especializada

**Probabilidade estimada: 0.22** · Asa Sul · 24 anos

- Google: 4.9 com 711 avaliações
- Site: https://www.sigaodontologia.com.br/ (status 200)
- Instagram: @sigaodontologiadf · 2.580 seguidores

**Contato:**

- **Josafa Martins De Lima** — Sócio-Administrador
- Telefone: `(61) 2099-5454`
- WhatsApp: `+556120995454`
- E-mail: `patio@sigaodontologia.com.br`
- Instagram pessoal: não localizado

<details><summary>Limites (2)</summary>

- Instagram pessoal do decisor nao localizado.
- Nao foi verificado qual dos dois dominios o Perfil da Empresa do Google linka.

</details>

---

### 22. Ortho Life

> ⛔ **O Google marca esta empresa como permanentemente fechada.** Confirme por telefone antes de qualquer contato — pode ser encerramento real ou ficha desatualizada, e as duas hipóteses mudam completamente a abordagem.

**Probabilidade estimada: desqualificada por encerramento** · Asa Sul · 13 anos

**O que trava:** nenhum site localizado; nenhum Instagram localizado; apenas 2 avaliações no Google

- Google: 3.0 com 2 avaliações
- Site: não localizado
- Instagram: não localizado

**Contato:**

- **Marcelo Vieira** — Sócio-Administrador
- Telefone: `(61) 3225-8767`
- WhatsApp: `+556132258767`
- Instagram pessoal: não localizado

<details><summary>Limites (4)</summary>

- Site nao localizado e nao conclusivo: ortholife.com.br existe mas nao resolve e o titular ('ORTHO LIFE CONSULT') nao foi vinculado a este CNPJ.
- Instagram da clinica nao localizado - todos os candidatos ('ortholiferv', 'ortholife.brasileia', 'ortholife_odonto', 'ortholifeodontologia') sao de outras cidades e foram descartados.
- Instagram pessoal de Marcelo Vieira nao localizado (nome muito comum).
- Nao foi confirmado se a operacao migrou para o endereco do Patio Brasil Shopping.

</details>

---
