# Propensão a fechar — Odontologia DF

Base: 3.124 clínicas ativas da fila `odonto-DF`. Gerado em 18/08/2026.

## O que este score é — e o que não é

**Não é probabilidade de fechamento.** Os eixos `dor` e `gatilho` do playbook estão NULL:
o estágio 2 (Google Places + Meta Ad Library) não rodou por falta de chave de API. Sem ele
não há velocidade de avaliações, não há faturamento estimado e não há nenhuma medição de
presença digital.

O que se mede aqui é **pré-qualificação estrutural**: quem pode pagar, tem margem para pagar
e decide rápido. Composição:

| Componente | Peso | Natureza |
|---|---|---|
| Capacidade de pagar (porte, capital, regime, unidades, maturidade) | 40% | medido |
| Fit de ticket (especialidade de alto valor no nome) | 20% | medido |
| Renda da região de captação | 15% | medido |
| Agilidade de decisão (natureza jurídica, nº de unidades) | 10% | medido |
| Defasagem digital presumida pela maturidade | 15% | **hipótese** |

O último componente é o único não medido — a premissa de que clínica madura cresceu na
indicação e tem presença digital atrasada. Só o Places e o Instagram confirmam. **Quando
entrarem, a ordem do topo muda.**

## Distribuição

| Grupo | Faixa | Clínicas |
|---|---|---:|
| **A — atacar primeiro** | ≥ 0,75 | **186** |
| B | 0,65–0,75 | 583 |
| C | 0,55–0,65 | 978 |
| D | < 0,55 | 1.377 |

## Arquétipos e a dor de cada um

| Arquétipo | Na fila | No grupo A | Propensão média |
|---|---:|---:|---:|
| especialista alto ticket | 457 | 103 | 0.67 |
| clinica institucional | 566 | 32 | 0.60 |
| clinica geral | 1852 | 32 | 0.54 |
| multi unidade | 59 | 10 | 0.65 |
| marca pessoal | 190 | 9 | 0.53 |

### 1. Especialista de alto ticket — 55% do grupo A

Implantodontia, ortodontia, estética e harmonização. Caso de R$8k a R$30k.

**A dor:** compra de alta consideração. O paciente pesquisa por semanas antes de fechar um
implante — busca no Google, abre o Instagram, procura antes/depois, lê avaliação. Sem esse
rastro, a clínica é **eliminada na pesquisa, antes de qualquer contato**. Ela nunca fica
sabendo que perdeu o paciente, o que faz a dor ser invisível até alguém medir.

**Por que fecha:** com ticket nesse patamar, **um único caso recuperado por mês paga o
contrato várias vezes**. É a conta mais fácil de fazer desta lista inteira.

### 2. Marca pessoal — o menor atrito de venda

O dentista é a marca. 190 na fila (piso — o detector por nome próprio subconta).

**A dor:** 15 ou 20 anos de autoridade clínica que não existem digitalmente. Currículo forte,
Instagram com post de bom dia.

**Por que fecha com a Oráculo especificamente:** é exatamente o portfólio que a casa já tem —
Dr. Adriano Borges, Dr. Pedro Brandão, Dra. Joana Tavares, Dra. Suziellen, Dr. Diego Santos,
Dra. Natália Rinco. Mesma conversa, mesmo entregável, **cases prontos para mostrar na
primeira reunião**. Não é preciso explicar o serviço, só mostrar um relatório já feito.

### 3. Multi-unidade — maior ticket, decisão mais lenta

59 na fila, 10 no grupo A. Conversão para o topo bem acima da média.

**A dor:** cada unidade com ficha própria no Google, frequentemente duplicada, avaliações
fragmentadas e marca inconsistente entre unidades. **É literalmente o diagnóstico do Dr.
Adriano Borges — 3 fichas duplicadas.** Já existe metodologia pronta para isso.

**Por que fecha:** dá para cobrar por unidade. R$3.500 é piso, não teto. Risco: decisão mais
lenta e chance maior de já ter agência.

### 4. Clínica institucional — 32 no grupo A

Centro/Instituto, corpo clínico, várias especialidades.

**A dor:** marca sem rosto. Não há autoridade pessoal para ancorar conteúdo, então o
Instagram vira mural de avisos. Precisa de estratégia de marca institucional — trabalho mais
denso e contrato mais caro, mas ciclo de venda mais longo.

### 5. Clínica geral — volume, não prioridade

1.852 na fila e só 32 no grupo A. Ticket menor, mais dependência de convênio, margem apertada.
A dor existe, a capacidade de pagar não. **Deixar para depois.**

## Top 30

Lista completa com telefone, WhatsApp, e-mail e endereço em `contatos.csv` (3.124 linhas).

| # | Clínica | Prop. | Porte | Região | Idade | Telefone | Arquétipo |
|---|---|---|---|---|---|---|---|
| 1 | **Renove - Estetica E Implantes Orais** | 0.92 | EPP | Asa Norte | 14a | `(61) 9 8179-0097` | especialista alto ticket |
| 2 | **Implantomed** | 0.91 | EPP | Asa Sul | 16a | `(61) 3202-3656` | especialista alto ticket |
| 3 | **Vital Implantes E Tratamentos Dentarios** | 0.91 | EPP | Asa Norte | 18a | `(61) 3032-5666` | especialista alto ticket |
| 4 | **Osteo Implante** | 0.91 | EPP | Taguatinga | 18a | `(61) 3036-6116` | multi unidade |
| 5 | **Patricia Pizzo Ortodontia** | 0.90 | EPP | Norte (Aguas Claras) | 13a | `(61) 3024-1777` | marca pessoal |
| 6 | **Instituto De Ortodontia Machado E Audicao** | 0.90 | EPP | Asa Norte | 17a | `(61) 3225-0655` | especialista alto ticket |
| 7 | **Everface Odontologia Especializada** | 0.90 | EPP | Asa Sul | 16a | `(61) 3326-3361` | especialista alto ticket |
| 8 | **Orthos Taguatinga** | 0.90 | DEMAIS | Areal (Aguas Claras) | 16a | `(61) 3901-2015` | especialista alto ticket |
| 9 | **Fabula Odontopediatria E Ortodontia** | 0.89 | DEMAIS | Asa Norte | 18a | `(61) 9 9967-5834` | multi unidade |
| 10 | **Faces Odontologia Estetica Ltda** | 0.89 | EPP | Aguas Claras | 10a | `(61) 3011-2400` | especialista alto ticket |
| 11 | **Ibi Instituto Brasiliense De Implantodontia** | 0.89 | DEMAIS | Asa Sul | 11a | `(61) 3541-5562` | especialista alto ticket |
| 12 | **Crie Odontologia** | 0.88 | DEMAIS | Asa Norte | 22a | `(61) 3326-4245` | especialista alto ticket |
| 13 | **Sallum - Odontologia Estetica** | 0.88 | DEMAIS | Asa Sul | 13a | `(61) 3225-0655` | especialista alto ticket |
| 14 | **Claudio Pinho Odontologia** | 0.88 | DEMAIS | Asa Sul | 13a | `(61) 3321-0999` | marca pessoal |
| 15 | **Wv Implantodontia** | 0.87 | DEMAIS | Asa Sul | 12a | `(61) 3354-5337` | especialista alto ticket |
| 16 | **Talita Chimeli Odontologia Estetica Avancada** | 0.87 | EPP | Asa Sul | 13a | `(61) 9 8496-7376` | marca pessoal |
| 17 | **Centro Clinico De Ortodontia Gomide Ltda** | 0.87 | EPP | Asa Sul | 18a | `(61) 3327-0404` | especialista alto ticket |
| 18 | **Bicalho Ortodontia** | 0.87 | EPP | Asa Norte | 20a | `(61) 3328-0072` | especialista alto ticket |
| 19 | **Implant Center** | 0.87 | EPP | Asa Sul | 27a | `(61) 3224-2882` | especialista alto ticket |
| 20 | **Cir Premier - Cent De Exc Em Reabilit E Estetica Oral** | 0.86 | DEMAIS | Lago Sul | 32a | `(61) 3346-9001` | especialista alto ticket |
| 21 | **Brasilia Implantes** | 0.86 | DEMAIS | Asa Norte | 15a | `(61) 3201-6011` | especialista alto ticket |
| 22 | **Ortho Life** | 0.86 | DEMAIS | Asa Sul | 13a | `(61) 3225-8767` | especialista alto ticket |
| 23 | **Implanto** | 0.85 | DEMAIS | Asa Sul | 22a | `(61) 3245-1122` | especialista alto ticket |
| 24 | **Siga Odontologia Especializada** | 0.85 | DEMAIS | Asa Sul | 24a | `(61) 2099-5454` | especialista alto ticket |
| 25 | **Aquarium Odontologia E Harmonizacao** | 0.85 | DEMAIS | Asa Sul | 28a | `(61) 9 9988-1987` | especialista alto ticket |
| 26 | **Prime Estetica Facial** | 0.85 | EPP | Asa Sul | 14a | `(61) 9 9699-9798` | especialista alto ticket |
| 27 | **Moya Ortodontia E Ortopedia Facial** | 0.85 | DEMAIS | Asa Norte | 24a | `(61) 3202-5236` | multi unidade |
| 28 | **Amazing Hof** | 0.84 | ME | Sul (Aguas Claras) | 22a | `(61) 9 8213-6761` | especialista alto ticket |
| 29 | **Eduardo Burgel Periodontia E Implantes** | 0.84 | DEMAIS | Asa Norte | 13a | `(61) 3081-8888` | marca pessoal |
| 30 | **Df Implantes** | 0.84 | DEMAIS | Asa Sul | 16a | `(61) 3346-2724` | especialista alto ticket |

## Sobre os telefones

97,2% da fila tem telefone (3.036 de 3.124); 88 não têm nenhum. Duas ressalvas que mudam
o uso prático:

- **1.534 celulares estavam no formato antigo de 8 dígitos** e não completavam a ligação.
  Receberam o nono dígito e estão marcados na coluna `tel_1_corrigido`.
- O número é o do **registro do CNPJ**, podendo estar desatualizado. 1.001 clínicas têm um
  segundo telefone e 2.514 têm e-mail — use como alternativa.

A coluna `tel_1_whatsapp` já vem em formato E.164 (`+5561…`), pronta para link de WhatsApp.

## O que falta para isso virar previsão de verdade

Com a chave do Places (custo US$ 0,00, cabe na cota gratuita):

1. **Quem não tem ficha no Google** — dor máxima, demonstrável em 10 segundos numa reunião
2. **Quem tem ficha abandonada** — nota baixa, avaliações sem resposta, dado desatualizado
3. **Velocidade de avaliações** — destrava o faturamento estimado e substitui a hipótese de
   maturidade por medição real
4. **Ficha duplicada** — o achado que mais converteu no portfólio atual

Com o Instagram (estágio 3, sessão logada): cadência, hiato, ER recente contra ER da amostra.
