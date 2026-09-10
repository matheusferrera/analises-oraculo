# -*- coding: utf-8 -*-
"""Monta NataliaRinco/Analise-de-Posts.html reaproveitando o <style> do Cronograma."""
import re, pathlib

BASE = pathlib.Path(__file__).resolve().parent.parent
SRC = BASE / "NataliaRinco" / "Cronograma-de-Conteudo.html"
OUT = BASE / "NataliaRinco" / "Analise-de-Posts.html"

style = re.search(r"<style>.*?</style>", SRC.read_text(encoding="utf-8"), re.S).group(0)

DESC = ("Análise das 89 publicações públicas do perfil @nataliarinco4055, com foco nos 37 posts da fase de "
        "candidatura: o que alcançou mais gente, que assunto converte alcance em interação, qual dia e qual "
        "horário rendem mais e o que a cadência diária de agosto fez com o desempenho por post. Coleta de 10 de "
        "setembro de 2026 pela Oráculo Tecnologia.")
TITLE = "Análise de posts do Instagram: Natália Rinco 4055 | Oráculo"

head = f"""<!DOCTYPE html>
<html lang="pt-BR">

<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{TITLE}</title>
  <meta name="description" content="{DESC}" />
  <meta property="og:type" content="website" />
  <meta property="og:title" content="{TITLE}" />
  <meta property="og:description" content="{DESC}" />
  <meta property="og:image" content="https://analises-oraculo.vercel.app/NataliaRinco/og-cenario.png" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:url" content="https://analises-oraculo.vercel.app/NataliaRinco/Analise-de-Posts.html" />
  <meta property="og:site_name" content="Oráculo Tecnologia" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:image" content="https://analises-oraculo.vercel.app/NataliaRinco/og-cenario.png" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,200..800&amp;family=Petrona:ital,wght@0,400..700;1,400..600&amp;display=swap" />
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
{style}
</head>
"""

def insight(kind, verdict, texto):
    return f"""      <div class="insight {kind}">
        <div class="insight-header">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>
          O que isso significa para você
        </div>
        <div class="insight-body">
          <span class="verdict">{verdict}</span>
          <p>{texto}</p>
        </div>
      </div>
"""

cover = """
<body>
  <header class="cover">
    <div class="cover-inner">
      <div class="cover-mark"><b>Oráculo Tecnologia</b> · Análise de publicações</div>
      <h1>Publicar todo dia multiplicou o volume por nove e dividiu o alcance por post pela metade. <em>O conteúdo que funciona é sempre o mesmo, e ele é pessoal.</em></h1>
      <p class="cover-sub">Terceira coleta do perfil, feita em 10 de setembro de 2026, dezessete dias depois do cronograma. As 89 publicações públicas foram lidas post a post pela API interna do Instagram, com curtidas, comentários, reproduções, duração de vídeo, horário exato e legenda. Este documento olha só para os posts: o que alcançou mais gente, o que converteu alcance em interação, em que dia e em que horário isso aconteceu, e o que a virada de cadência de 24 de agosto fez com cada número.</p>
      <div class="cover-rule"></div>
      <div class="cover-foot"><span><b>@nataliarinco4055</b></span><span>PSB 4055 · Deputada federal por Goiás</span><span>Coleta de 10 de setembro de 2026</span></div>
    </div>
  </header>

  <div class="kpi-band">
    <div class="kpi-row">
      <div class="kpi">
        <div class="kpi-val">8.858</div>
        <div class="kpi-label">Reproduções do post mais viral</div>
        <div class="kpi-note">Anúncio da pré-candidatura, 16/04, ainda invicto</div>
      </div>
      <div class="kpi">
        <div class="kpi-val">246</div>
        <div class="kpi-label">Comentários nesse mesmo post</div>
        <div class="kpi-note">O segundo colocado da série tem 109</div>
      </div>
      <div class="kpi">
        <div class="kpi-val">9,1</div>
        <div class="kpi-label">Posts por semana desde 24/08</div>
        <div class="kpi-note">Eram 1,0 por semana até 23/08</div>
      </div>
      <div class="kpi">
        <div class="kpi-val">160</div>
        <div class="kpi-label">Interações medianas por post agora</div>
        <div class="kpi-note">Eram 278 na fase de baixa frequência</div>
      </div>
      <div class="kpi">
        <div class="kpi-val">24</div>
        <div class="kpi-label">Dias até o primeiro turno</div>
        <div class="kpi-note">Impulsionamento permitido até 01/10</div>
      </div>
    </div>
  </div>

  <nav class="nav" aria-label="Seções da análise">
    <a href="#essencial">O essencial em dois minutos</a><a href="#viral">O que viralizou</a><a href="#cadencia">Cadência e desgaste</a><a href="#tema">Que assunto rende</a><a href="#quando">Dia e horário</a><a href="#formato">Formato e duração</a><a href="#legenda">Legenda, número e hashtag</a><a href="#acoes">O que fazer nos 24 dias</a>
  </nav>

  <main class="page">
"""

s_essencial = """    <section id="essencial">
      <div class="sec-head">
        <h2>O essencial em dois minutos</h2>
        <p>Quatro achados que entregam o valor inteiro desta leitura.</p>
      </div>
      <div class="essential">
        <div class="essential-main">
          <p class="lede"><b>1. O maior post da conta continua sendo o primeiro.</b> O anúncio da pré-candidatura, publicado em 16 de abril às 9h48, fez 8.858 reproduções, 555 curtidas e 246 comentários. Cinco meses depois, nenhuma publicação chegou perto: o segundo colocado em comentários tem 109. Foi um vídeo de 50 segundos, em primeira pessoa, contando a história da família na Chapada.</p>
          <p><b>2. A cadência diária cobrou caro por post.</b> Entre 25 de abril e 23 de agosto o perfil publicou 1,0 vez por semana e a mediana era de 278 interações e 4.230 reproduções. De 24 de agosto para cá são 9,1 posts por semana, e a mediana caiu para 160 interações e 2.449 reproduções. Semana a semana a queda é contínua: 216, depois 149, depois 90.</p>
          <p><b>3. História pessoal rende o dobro de pauta.</b> Publicações sobre origem, família e trajetória têm mediana de 383 interações. Pauta nacional genérica tem 118. Os dois maiores posts da fase diária são exatamente os dois mais pessoais: o texto sobre a morte do pai, com 650 interações, e a resposta à acusação de candidatura de família, com 405.</p>
          <p><b>4. O horário mais usado é o pior horário.</b> Meio-dia concentra cinco Reels da fase de campanha e entrega mediana de 2.629 reproduções. As 20h entregam 5.350 e as 17h entregam 4.063. A campanha vem publicando no horário de menor retorno.</p>
        </div>
        <div class="card">
          <h3>Como estes números foram apurados</h3>
          <p>Leitura direta de <b>89 publicações públicas</b> de @nataliarinco4055 pela API interna do Instagram, com sessão autenticada, em 10 de setembro de 2026. De cada post foram lidos código, data e hora exatas, tipo de mídia, curtidas, comentários, reproduções, duração do vídeo, marcações e legenda completa. Curtidas estão visíveis em 88 dos 89 posts. Horários convertidos para o fuso de Brasília.</p>
          <p>A fase de candidatura vai de 31 de março a 7 de setembro e reúne <b>37 publicações</b>. Os números do perfil no dia da coleta: 2.847 seguidores, 3.091 contas seguidas.</p>
        </div>
      </div>
      <div class="metric-strip">
        <div class="metric">
          <div class="metric-value">89</div>
          <div class="metric-label">publicações públicas hoje</div>
        </div>
        <div class="metric">
          <div class="metric-value">37</div>
          <div class="metric-label">na fase de candidatura</div>
        </div>
        <div class="metric">
          <div class="metric-value">2.847</div>
          <div class="metric-label">seguidores, contra 2.756 em 24/08</div>
        </div>
        <div class="metric">
          <div class="metric-value">3.796</div>
          <div class="metric-label">reproduções médias por Reel</div>
        </div>
      </div>
"""+insight("info","&#9654; Atenção","A conta cresce 5,4 seguidores por dia desde a coleta de 24 de agosto. No mesmo ritmo, chega ao dia 4 de outubro com cerca de 2.980 seguidores. O alcance dos Reels, 3.796 reproduções em média, já é 1,33 vez a base de seguidores, então a distribuição orgânica está funcionando: o gargalo não é a entrega, é a conversão de quem assiste em quem segue e em quem comenta.")+"""    </section>
"""

s_viral = """    <section id="viral">
      <div class="sec-head">
        <h2>O que viralizou</h2>
        <p>As doze publicações mais fortes da fase de candidatura, por curtidas somadas a comentários.</p>
      </div>
      <h3>Três dos quatro maiores posts falam da própria história, e o quarto é o anúncio oficial.</h3>
      <p>O padrão é estável desde abril. Quando a legenda começa em primeira pessoa e conta um episódio concreto da vida dela, o post sobe. Quando a legenda abre com uma tese ou com um slogan de campanha, o post fica na média. O anúncio de 16 de abril reúne as duas coisas, história e notícia, e por isso continua sendo o teto da conta.</p>
      <div class="table-wrap">
        <table>
          <thead>
            <tr><th>Data e hora</th><th>Dia</th><th>Formato</th><th class="right">Curtidas</th><th class="right">Comentários</th><th class="right">Reproduções</th><th>Assunto</th></tr>
          </thead>
          <tbody>
            <tr><td>16/04, 9h48</td><td>quinta</td><td>Reel 50s</td><td class="right"><b>555</b></td><td class="right"><b>246</b></td><td class="right">8.858</td><td>Anúncio da pré-candidatura</td></tr>
            <tr><td>02/09, 20h01</td><td>quarta</td><td>Reel 225s</td><td class="right">552</td><td class="right">98</td><td class="right">5.350</td><td>Os 16 anos da morte do pai</td></tr>
            <tr><td>04/08, 16h22</td><td>terça</td><td>Foto</td><td class="right">485</td><td class="right">109</td><td class="right">n/a</td><td>Convenção estadual do PSB</td></tr>
            <tr><td>08/08, 17h28</td><td>sábado</td><td>Carrossel 6</td><td class="right">441</td><td class="right">51</td><td class="right">n/a</td><td>Candidatura oficializada</td></tr>
            <tr><td>24/08, 20h42</td><td>segunda</td><td>Reel 76s</td><td class="right">343</td><td class="right">75</td><td class="right">6.695</td><td>Lixão a céu aberto em Alto Paraíso</td></tr>
            <tr><td>16/08, 22h25</td><td>domingo</td><td>Foto</td><td class="right">336</td><td class="right">71</td><td class="right">n/a</td><td>Apresentação como filha de Divaldo</td></tr>
            <tr><td>02/09, 12h03</td><td>quarta</td><td>Reel 73s</td><td class="right">342</td><td class="right">63</td><td class="right">6.309</td><td>Resposta à acusação de candidatura de família</td></tr>
            <tr><td>24/07, 17h11</td><td>sexta</td><td>Reel 38s</td><td class="right">327</td><td class="right">64</td><td class="right">8.113</td><td>Aniversário e o chamado para a política</td></tr>
            <tr><td>29/08, 16h20</td><td>sábado</td><td>Reel 146s</td><td class="right">332</td><td class="right">43</td><td class="right">6.276</td><td>Entrevista sobre as raízes e a região</td></tr>
            <tr><td>31/03, 12h01</td><td>terça</td><td>Carrossel 3</td><td class="right">321</td><td class="right">49</td><td class="right">n/a</td><td>Luto por dona Romilda</td></tr>
            <tr><td>29/05, 15h29</td><td>sexta</td><td>Reel 29s</td><td class="right">288</td><td class="right">40</td><td class="right">4.407</td><td>Ocupar espaços de poder, com João Campos</td></tr>
            <tr><td>01/06, 17h36</td><td>segunda</td><td>Reel 22s</td><td class="right">248</td><td class="right">47</td><td class="right">4.492</td><td>Da menina livre na Chapada à candidata</td></tr>
          </tbody>
        </table>
        <p class="sm muted">Fonte: @nataliarinco4055, coleta de 10/09/2026, 37 publicações da fase de candidatura. Reproduções existem apenas em Reels. Publicações de 5 a 7 de setembro ainda estão acumulando: a comparação com a coleta de 18/08 mostra que um post ganha pouco depois de duas semanas, mas um post de três dias ainda pode subir de 15% a 20%.</p>
      </div>
      <div class="chart"><canvas id="chartTop"></canvas></div>
      <h3>O piso também tem padrão, e é o oposto.</h3>
      <p>As seis publicações mais fracas da fase de candidatura são a composteira caseira (38 interações), o Reel sobre regiões esquecidas com texto de slogan (79), a foto com o ministro em Brasília (92), o banheiro feminino do Senado (94), o vídeo de representatividade feminina (101) e o comentário sobre o caso Banco Master (105). Todas têm em comum uma coisa: falam de um assunto em vez de contar um caso. Nenhuma cita nome de pessoa, de lugar da região ou episódio vivido.</p>
"""+insight("good","&#9650; Bom","Existe uma fórmula funcionando e ela é reproduzível: primeira pessoa, um episódio concreto com nome e lugar, e a conclusão política vindo depois do relato, não antes. Os três posts que mais renderam nas últimas duas semanas seguem exatamente essa ordem. Nos 24 dias que faltam, cada peça de maior investimento deveria nascer desse molde, e os temas nacionais deveriam entrar sempre ancorados num caso da Chapada ou do Nordeste Goiano.")+"""    </section>
"""

s_cadencia = """    <section id="cadencia">
      <div class="sec-head">
        <h2>Cadência e desgaste</h2>
        <p>O que mudou quando o perfil passou a publicar todo dia.</p>
      </div>
      <h3>O volume subiu nove vezes e o retorno por post caiu 42%.</h3>
      <p>Até 23 de agosto o perfil publicava uma vez por semana em média, com mediana de 278 interações e 4.230 reproduções por Reel. De 24 de agosto até 7 de setembro foram 18 publicações em 14 dias, ou 9,1 por semana, com mediana de 160 interações e 2.449 reproduções. O total semanal de interações subiu, porque nove posts fracos somam mais que um post forte, mas a curva está descendo semana a semana e já chegou a um patamar preocupante.</p>
      <div class="table-wrap">
        <table>
          <thead>
            <tr><th>Semana</th><th class="right">Publicações</th><th class="right">Interações medianas</th><th class="right">Reproduções medianas</th><th>Leitura</th></tr>
          </thead>
          <tbody>
            <tr><td>04/08 a 10/08</td><td class="right">3</td><td class="right">492</td><td class="right">3.427</td><td>Convenção e oficialização</td></tr>
            <tr><td>16/08</td><td class="right">1</td><td class="right">407</td><td class="right">n/a</td><td>Único post da semana</td></tr>
            <tr><td>24/08 a 30/08</td><td class="right">8</td><td class="right">216</td><td class="right">2.629</td><td>Primeira semana de cadência diária</td></tr>
            <tr><td>31/08 a 06/09</td><td class="right">8</td><td class="right">149</td><td class="right">2.467</td><td>Queda de 31% sobre a semana anterior</td></tr>
            <tr><td>07/09</td><td class="right">2</td><td class="right">90</td><td class="right">1.014</td><td>Menor patamar da fase de candidatura</td></tr>
          </tbody>
        </table>
        <p class="sm muted">Fonte: @nataliarinco4055, coleta de 10/09/2026. Mediana usada em vez de média para não deixar um post excepcional distorcer a semana. A semana de 07/09 tem só dois posts e ainda está acumulando alcance.</p>
      </div>
      <div class="chart"><canvas id="chartSemana"></canvas></div>
      <h3>Não é a frequência sozinha: é a frequência com peça fraca.</h3>
      <p>Dentro da própria fase diária a dispersão é enorme. No mesmo intervalo de duas semanas convivem um post de 650 interações e um de 79. Nos cinco dias em que houve duas publicações, a segunda superou a primeira em três deles, o que indica que o público aguenta dois posts por dia sem canibalizar. O que derruba a média não é o número de peças, é a proporção de peças genéricas: das 18 publicações desde 24 de agosto, 8 são slogan ou pauta nacional, e essas 8 respondem pelas piores marcas da série.</p>
      <p>Vale registrar o outro lado do intervalo. As 15 publicações feitas depois de três dias ou mais de silêncio têm mediana de 295 interações e 5.544 reproduções, quase o dobro das publicadas com menos de 24 horas de intervalo. Parte disso é efeito da fase, porque os posts espaçados são também os mais antigos e os mais fortes em conteúdo. Mas o sinal é consistente o bastante para justificar concentrar o esforço em menos peças melhores.</p>
"""+insight("warn","&#9654; Atenção","Faltam 24 dias e a curva de alcance por post está caindo há três semanas seguidas. A recomendação não é publicar menos, é redistribuir: manter uma peça por dia, garantir que pelo menos quatro por semana sejam do tipo que rende (história pessoal, episódio local com nome próprio, denúncia com endereço) e transformar as peças de slogan em stories, que é onde elas custam menos atenção do feed.")+"""    </section>
"""

s_tema = """    <section id="tema">
      <div class="sec-head">
        <h2>Que assunto rende</h2>
        <p>As 37 publicações da candidatura classificadas por tema, com a mediana de interações de cada grupo.</p>
      </div>
      <h3>Origem e família rendem 3,2 vezes mais que pauta nacional.</h3>
      <p>A classificação foi feita lendo as 37 legendas inteiras. O resultado repete e agrava o que a coleta de 24 de agosto já indicava: o ativo desta candidatura é a biografia, não a agenda. Pauta ambiental, que é bandeira declarada na bio, continua sendo o pior tema medido, com 38 interações no único post exclusivamente ambiental da fase. Quando o mesmo assunto aparece com endereço, como no vídeo gravado dentro do lixão de Alto Paraíso, ele salta para 418.</p>
      <div class="table-wrap">
        <table>
          <thead>
            <tr><th>Tema</th><th class="right">Posts</th><th class="right">Interações medianas</th><th class="right">Reproduções medianas</th><th>Exemplo mais forte</th></tr>
          </thead>
          <tbody>
            <tr><td>Anúncio de candidatura</td><td class="right">2</td><td class="right"><b>450</b></td><td class="right">n/a</td><td>Oficialização em 08/08</td></tr>
            <tr><td>Origem, família e trajetória</td><td class="right">8</td><td class="right"><b>383</b></td><td class="right">6.276</td><td>Os 16 anos da morte do pai</td></tr>
            <tr><td>Partido e agenda institucional</td><td class="right">8</td><td class="right">180</td><td class="right">3.241</td><td>Ocupar espaços, com João Campos</td></tr>
            <tr><td>Mulheres na política, formato slogan</td><td class="right">5</td><td class="right">172</td><td class="right">1.867</td><td>Dia Laranja em 25/08</td></tr>
            <tr><td>Mobilização e pedido de apoio</td><td class="right">3</td><td class="right">168</td><td class="right">5.246</td><td>Adesivo no carro em Cavalcante</td></tr>
            <tr><td>Território e Chapada</td><td class="right">7</td><td class="right">151</td><td class="right">2.431</td><td>Lixão a céu aberto, com 418</td></tr>
            <tr><td>Pauta, sem ancoragem local</td><td class="right">4</td><td class="right">118</td><td class="right">1.588</td><td>Escala 6x1 no Senado</td></tr>
          </tbody>
        </table>
        <p class="sm muted">Fonte: @nataliarinco4055, coleta de 10/09/2026. Classificação temática feita a partir da leitura integral das 37 legendas da fase de candidatura. Reproduções calculadas apenas sobre os Reels de cada grupo.</p>
      </div>
      <div class="chart"><canvas id="chartTema"></canvas></div>
      <h3>Nem todo alcance vale o mesmo.</h3>
      <p>Dividindo interações por reproduções chega-se à taxa de conversão de cada Reel. A mediana da fase é de 64 interações por mil reproduções. O texto sobre o pai converte 121,5 por mil, quase o dobro da mediana, e é o melhor da série. Na outra ponta, a composteira caseira converte 40,3 e o vídeo da vaquinha converte 42,2, apesar de esse último ter tido 6.595 reproduções. Alcance alto com conversão baixa é o retrato de um vídeo que foi entregue mas não mobilizou.</p>
"""+insight("bad","&#9654; Atenção","Cinco das oito publicações mais recentes são do tipo que a própria série mostra render menos. Numa campanha proporcional com 24 dias restantes, cada peça publicada consome uma janela de distribuição que não volta. A régua sugerida é simples: se a legenda não tem um nome de pessoa, um nome de município da base ou uma data concreta, ela ainda não está pronta para o feed.")+"""    </section>
"""

s_quando = """    <section id="quando">
      <div class="sec-head">
        <h2>Dia e horário</h2>
        <p>Quando as 37 publicações foram ao ar e como cada janela se comportou.</p>
      </div>
      <h3>Meio-dia é o horário mais usado e o de pior retorno.</h3>
      <p>Cinco Reels da fase de candidatura foram publicados entre 12h e 13h, mais do que em qualquer outra faixa, e a mediana dessa janela é de 2.629 reproduções. Os três Reels publicados a partir das 20h têm mediana de 5.350, e os seis publicados entre 17h e 18h têm 4.063. A faixa das 18h30 em diante, com três peças, é a mais fraca de todas, com 1.588.</p>
      <div class="table-wrap">
        <table>
          <thead>
            <tr><th>Faixa</th><th class="right">Reels</th><th class="right">Reproduções medianas</th><th>Leitura</th></tr>
          </thead>
          <tbody>
            <tr><td>20h em diante</td><td class="right">3</td><td class="right"><b>5.350</b></td><td>Melhor janela medida, amostra pequena</td></tr>
            <tr><td>16h às 17h59</td><td class="right">8</td><td class="right"><b>4.063</b></td><td>Melhor janela com amostra relevante</td></tr>
            <tr><td>14h às 15h59</td><td class="right">2</td><td class="right">3.489</td><td>Pouco usada</td></tr>
            <tr><td>12h às 13h59</td><td class="right">5</td><td class="right">2.629</td><td>A mais usada, e abaixo da mediana geral</td></tr>
            <tr><td>Até 11h59</td><td class="right">4</td><td class="right">2.318</td><td>Puxada pelo anúncio de abril, que fez 8.858</td></tr>
            <tr><td>18h às 19h59</td><td class="right">3</td><td class="right">1.588</td><td>Pior janela medida</td></tr>
          </tbody>
        </table>
        <p class="sm muted">Fonte: @nataliarinco4055, coleta de 10/09/2026, 25 Reels da fase de candidatura, horários no fuso de Brasília. Amostra por faixa é pequena, entre 2 e 8 peças, então a leitura serve como orientação e não como regra fechada.</p>
      </div>
      <div class="chart"><canvas id="chartHora"></canvas></div>
      <h3>Quarta e sábado sustentam, segunda-feira derruba.</h3>
      <p>Por dia da semana, quarta-feira tem mediana de 342 interações em 4 publicações e sábado tem 314 em 4. Segunda-feira, com 6 publicações, tem 113, a pior marca da série, e foi justamente o dia escolhido para os dois posts de 7 de setembro. Sexta-feira concentra o maior número de peças, 9, e fica na média, com 190.</p>
      <div class="chart"><canvas id="chartDia"></canvas></div>
"""+insight("info","&#9733; Destaque","Trocar meio-dia por fim de tarde e evitar segunda-feira para as peças de maior investimento é a mudança mais barata desta análise: custa apenas mudar a hora do agendamento. Pela mediana medida, a mesma peça publicada às 17h em vez de às 12h30 tende a alcançar cerca de 1.400 pessoas a mais.")+"""    </section>
"""

s_formato = """    <section id="formato">
      <div class="sec-head">
        <h2>Formato e duração</h2>
        <p>Reel, carrossel e foto fazem trabalhos diferentes, e a série mostra qual é qual.</p>
      </div>
      <h3>Foto e carrossel engajam mais quem já segue; o Reel é o que traz gente nova.</h3>
      <p>Na fase de candidatura, a foto simples tem mediana de 250 interações em 6 peças e o carrossel tem 238 em 6, contra 172 do Reel em 25 peças. Isso não faz do Reel o formato inferior: ele é o único que entrega alcance fora da base. A média de 3.796 reproduções por Reel equivale a 1,33 vez o total de seguidores do perfil. Foto e carrossel circulam essencialmente entre os 2.847 que já seguem.</p>
      <div class="table-wrap">
        <table>
          <thead>
            <tr><th>Formato</th><th class="right">Publicações</th><th class="right">Interações medianas</th><th class="right">Reproduções medianas</th><th>Função na campanha</th></tr>
          </thead>
          <tbody>
            <tr><td>Foto</td><td class="right">6</td><td class="right">250</td><td class="right">n/a</td><td>Registro e marco, converte a base</td></tr>
            <tr><td>Carrossel</td><td class="right">6</td><td class="right">238</td><td class="right">n/a</td><td>Explicação e proposta</td></tr>
            <tr><td>Reel</td><td class="right">25</td><td class="right">172</td><td class="right">3.241</td><td>Único formato que alcança fora da base</td></tr>
          </tbody>
        </table>
      </div>
      <h3>Vídeo longo não afasta: os três maiores Reels da série passam de dois minutos.</h3>
      <p>Separando os 25 Reels por duração, os três acima de 120 segundos têm mediana de 5.350 reproduções e 375 interações, o melhor resultado de todas as faixas. Os de 31 a 60 segundos vêm em seguida, com 3.896 reproduções. Os de até 30 segundos ficam em 2.629 e os de 61 a 120 segundos em 2.554. O vídeo de 225 segundos sobre o pai é o segundo maior post da fase inteira.</p>
      <div class="table-wrap">
        <table>
          <thead>
            <tr><th>Duração</th><th class="right">Reels</th><th class="right">Reproduções medianas</th><th class="right">Interações medianas</th></tr>
          </thead>
          <tbody>
            <tr><td>Acima de 120s</td><td class="right">3</td><td class="right"><b>5.350</b></td><td class="right"><b>375</b></td></tr>
            <tr><td>31s a 60s</td><td class="right">9</td><td class="right">3.896</td><td class="right">186</td></tr>
            <tr><td>Até 30s</td><td class="right">7</td><td class="right">2.629</td><td class="right">170</td></tr>
            <tr><td>61s a 120s</td><td class="right">6</td><td class="right">2.554</td><td class="right">118</td></tr>
          </tbody>
        </table>
        <p class="sm muted">Fonte: @nataliarinco4055, coleta de 10/09/2026, duração lida do próprio arquivo de vídeo. As faixas têm entre 3 e 9 peças, então a diferença entre 31s e 120s é menos confiável do que o contraste entre os extremos.</p>
      </div>
"""+insight("purple","&#9733; Destaque","O que separa o Reel longo bem-sucedido do curto fraco não é o tempo, é ter história suficiente para preencher o tempo. Vale reservar as peças acima de dois minutos para relato pessoal e depoimento de eleitor, e usar cortes de 30 a 45 segundos para recado de agenda. A duração deve seguir o conteúdo, nunca o contrário.")+"""    </section>
"""

s_legenda = """    <section id="legenda">
      <div class="sec-head">
        <h2>Legenda, número e hashtag</h2>
        <p>O que as 37 legendas pedem ao leitor, e o que elas deixam de pedir.</p>
      </div>
      <h3>O 4055 entrou na legenda, e essa correção está feita.</h3>
      <p>A análise de 24 de agosto registrou que apenas 1 de 19 publicações escrevia o número. Hoje o quadro é outro: nas 19 publicações feitas de 16 de agosto para cá, <b>16 trazem 4055 na legenda</b>, contra zero nas 18 anteriores. É a correção mais visível entre as duas coletas e ela custou nada.</p>
      <h3>O que ainda falta é o pedido.</h3>
      <p>Das 37 legendas da fase de candidatura, apenas <b>2 trazem link</b> para a vaquinha ou para as propostas, e apenas <b>5 pedem alguma ação</b> ao leitor, como seguir, compartilhar ou marcar alguém. A publicação que pediu seguidores de forma explícita, em 4 de setembro, fez 172 interações, acima da mediana da semana. O perfil ganhou 91 seguidores em 17 dias, ritmo de 5,4 por dia, com 25 Reels entregando quase 3.800 reproduções cada. Há um funil aberto entre quem assiste e quem segue.</p>
      <div class="table-wrap">
        <table>
          <thead>
            <tr><th>Elemento da legenda</th><th class="right">Publicações</th><th class="right">De 37</th><th>Observação</th></tr>
          </thead>
          <tbody>
            <tr><td>Escreve 4055</td><td class="right">16</td><td class="right">43%</td><td>Zero antes de 16/08, 16 de 19 depois</td></tr>
            <tr><td>Usa a palavra vote ou voto</td><td class="right">9</td><td class="right">24%</td><td>Concentrado nos últimos dez dias</td></tr>
            <tr><td>Pede ação ao leitor</td><td class="right">5</td><td class="right">14%</td><td>Seguir, compartilhar ou marcar</td></tr>
            <tr><td>Traz link</td><td class="right">2</td><td class="right">5%</td><td>Vaquinha e propostas na bio</td></tr>
          </tbody>
        </table>
        <p class="sm muted">Fonte: @nataliarinco4055, coleta de 10/09/2026, varredura por expressão regular sobre as 37 legendas completas da fase de candidatura.</p>
      </div>
      <h3>Três defeitos de hashtag que dividem o alcance ao meio.</h3>
      <p>A etiqueta principal, #chapadadosveadeiros, aparece em 18 das 37 publicações e está correta. Os problemas estão nas outras. A bandeira das mulheres está partida em duas grafias, <b>#mulheresnapolitica com 7 usos e #mulheresnapolítica com 6</b>, e o Instagram trata as duas como etiquetas diferentes, o que divide a audiência do tema em dois grupos que não se encontram. A etiqueta de marca própria foi criada com acento, <b>#natáliarinco4055</b>, com 8 usos, enquanto o handle não tem acento, o que dificulta a busca de quem digita o nome do perfil. E <b>#precandidato</b>, além de estar no masculino, ficou obsoleta desde a convenção de 4 de agosto e ainda aparece em duas publicações.</p>
"""+insight("warn","&#9654; Atenção","Padronizar em #mulheresnapolitica sem acento, criar #nataliarinco4055 sem acento e aposentar #precandidato são três ajustes de texto que valem para todas as peças restantes. E vale acrescentar um pedido explícito de seguir ao final de todo Reel de história pessoal, que é justamente o formato que hoje entrega quase 3.800 reproduções sem converter em seguidor.")+"""    </section>
"""

s_acoes = """    <section id="acoes">
      <div class="sec-head">
        <h2>O que fazer nos 24 dias</h2>
        <p>Seis decisões que saem direto dos números acima.</p>
      </div>
      <div class="table-wrap">
        <table>
          <thead>
            <tr><th>Decisão</th><th>Por que, pelo dado</th><th>Quando</th></tr>
          </thead>
          <tbody>
            <tr><td><b>Mudar o horário padrão de 12h30 para 17h</b></td><td>Meio-dia entrega 2.629 reproduções medianas; a faixa das 16h às 18h entrega 4.063</td><td>Já no próximo agendamento</td></tr>
            <tr><td><b>Nunca colocar a peça principal da semana na segunda-feira</b></td><td>Segunda tem mediana de 113 interações em 6 peças, a pior de todos os dias</td><td>Já</td></tr>
            <tr><td><b>Garantir quatro peças por semana de história pessoal ou episódio local com nome próprio</b></td><td>Esse grupo tem mediana de 383 interações, contra 118 da pauta sem ancoragem</td><td>Toda semana até 04/10</td></tr>
            <tr><td><b>Migrar as peças de slogan para stories</b></td><td>As 8 publicações de slogan e pauta nacional desde 24/08 respondem pelas piores marcas da série</td><td>Já</td></tr>
            <tr><td><b>Fechar toda peça de história com pedido de seguir e com 4055</b></td><td>Só 5 de 37 legendas pedem ação, e a conta cresce 5,4 seguidores por dia com 3.796 reproduções por Reel</td><td>Já</td></tr>
            <tr><td><b>Corrigir as três hashtags</b></td><td>#mulheresnapolitica está partida em duas grafias, a etiqueta de marca tem acento e #precandidato está obsoleta</td><td>Já</td></tr>
          </tbody>
        </table>
      </div>
      <h3>Uma observação sobre o histórico do perfil.</h3>
      <p>Entre a coleta de 18 de agosto e a de hoje, <b>63 das 134 publicações que estavam no ar saíram da grade</b>. São posts de 2015 a 2021, mais uma publicação de 5 de julho de 2026. A grade pública passou de 134 para 89 peças. É uma decisão editorial legítima de limpeza de perfil e ela não afeta nenhum número desta análise, que trata da fase de candidatura, mas vale ficar registrada: as 63 peças removidas somavam 10.101 curtidas de histórico social, e o perfil continua exibindo publicações pessoais antigas de 2014 a 2021 ao lado das de campanha.</p>
"""+insight("purple","&#9733; Destaque","Nenhuma das seis decisões acima exige produção nova, verba ou aprovação de terceiros. Todas são mudanças de horário, de ordem de argumento dentro da legenda e de escolha entre feed e story. Aplicadas nas próximas 24 publicações, valem cerca de 1.400 reproduções a mais por peça só na troca de horário, sem contar o efeito de trocar peça genérica por história.")+"""    </section>
  </main>
"""

closing = """
  <div class="closing">
    <div class="closing-inner">
      <h2>O perfil já sabe o que funciona. Ele só está publicando outra coisa.</h2>
      <p>Os quatro maiores posts desta candidatura foram publicados entre abril e setembro, com formatos diferentes e durações diferentes, e todos os quatro contam uma história em primeira pessoa. Os seis menores foram publicados na mesma janela e nenhum deles cita um nome de pessoa ou de município. Não é uma questão de talento nem de produção: a fórmula está documentada dentro da própria conta, com 37 publicações medidas. Faltam 24 dias e cerca de 24 peças. Cada uma delas pode escolher de que lado dessa linha vai cair.</p>
      <div class="closing-meta">Oráculo Tecnologia · Análise de publicações · @nataliarinco4055 · Coleta de 10 de setembro de 2026</div>
    </div>
  </div>
"""

script = """
  <script>
    (() => {
      const ink = '#1b2e73', primary = '#1d4ed8', soft = '#b3c0ea', warn = '#8f4e07';
      Chart.defaults.font.family = "'Bricolage Grotesque', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif";
      Chart.defaults.color = '#6b7186';
      Chart.defaults.plugins.legend.labels.usePointStyle = true;
      Chart.defaults.plugins.legend.labels.boxWidth = 7;
      const grid = { color: '#ebedf4' };

      new Chart(document.getElementById('chartTop'), { type: 'bar', data: { labels: ['Anúncio 16/04', 'Morte do pai 02/09', 'Convenção 04/08', 'Oficialização 08/08', 'Lixão 24/08', 'Filha de Divaldo 16/08', 'Candidatura de família 02/09', 'Aniversário 24/07', 'Entrevista 29/08', 'Luto 31/03', 'João Campos 29/05', 'Menina da Chapada 01/06'], datasets: [{ label: 'Curtidas', data: [555, 552, 485, 441, 343, 336, 342, 327, 332, 321, 288, 248], backgroundColor: ink, borderRadius: 2 }, { label: 'Comentários', data: [246, 98, 109, 51, 75, 71, 63, 64, 43, 49, 40, 47], backgroundColor: soft, borderRadius: 2 }] }, options: { responsive: true, maintainAspectRatio: false, plugins: { title: { display: true, text: 'As 12 publicações mais fortes da fase de candidatura' } }, scales: { y: { stacked: true, beginAtZero: true, grid }, x: { stacked: true, grid: { display: false }, ticks: { maxRotation: 60, minRotation: 45, font: { size: 9 } } } } } });

      new Chart(document.getElementById('chartSemana'), { type: 'bar', data: { labels: ['04/08 a 10/08', '16/08', '24/08 a 30/08', '31/08 a 06/09', '07/09'], datasets: [{ type: 'bar', label: 'Publicações na semana', data: [3, 1, 8, 8, 2], backgroundColor: soft, borderRadius: 2, yAxisID: 'y1' }, { type: 'line', label: 'Interações medianas por post', data: [492, 407, 216, 149, 90], borderColor: primary, backgroundColor: primary, tension: .3, yAxisID: 'y' }] }, options: { responsive: true, maintainAspectRatio: false, plugins: { title: { display: true, text: 'Mais publicações por semana, menos retorno por publicação' } }, scales: { y: { beginAtZero: true, grid, title: { display: true, text: 'interações medianas' } }, y1: { beginAtZero: true, position: 'right', grid: { display: false }, title: { display: true, text: 'posts' } }, x: { grid: { display: false } } } } });

      new Chart(document.getElementById('chartTema'), { type: 'bar', data: { labels: ['Anúncio de candidatura', 'Origem e família', 'Partido e institucional', 'Mulheres, formato slogan', 'Mobilização e apoio', 'Território e Chapada', 'Pauta sem ancoragem'], datasets: [{ label: 'Interações medianas por publicação', data: [450, 383, 180, 172, 168, 151, 118], backgroundColor: [ink, ink, primary, primary, primary, soft, warn], borderRadius: 2 }] }, options: { responsive: true, maintainAspectRatio: false, indexAxis: 'y', plugins: { legend: { display: false }, title: { display: true, text: 'Biografia rende 3,2 vezes mais que pauta nacional genérica' } }, scales: { x: { beginAtZero: true, grid }, y: { grid: { display: false } } } } });

      new Chart(document.getElementById('chartHora'), { type: 'bar', data: { labels: ['Até 11h59', '12h às 13h59', '14h às 15h59', '16h às 17h59', '18h às 19h59', '20h em diante'], datasets: [{ label: 'Reproduções medianas por Reel', data: [2318, 2629, 3489, 4063, 1588, 5350], backgroundColor: [soft, warn, primary, ink, warn, ink], borderRadius: 2 }] }, options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false }, title: { display: true, text: 'A faixa mais usada, meio-dia, é uma das de menor alcance' } }, scales: { y: { beginAtZero: true, grid }, x: { grid: { display: false } } } } });

      new Chart(document.getElementById('chartDia'), { type: 'bar', data: { labels: ['Quarta', 'Sábado', 'Terça', 'Domingo', 'Sexta', 'Quinta', 'Segunda'], datasets: [{ label: 'Interações medianas por publicação', data: [342, 314, 253, 246, 190, 153, 113], backgroundColor: [ink, ink, primary, primary, soft, soft, warn], borderRadius: 2 }] }, options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false }, title: { display: true, text: 'Quarta e sábado sustentam; segunda é o pior dia da série' } }, scales: { y: { beginAtZero: true, grid }, x: { grid: { display: false } } } } });
    })();
  </script>
  <script>
    (() => {
      const links = [...document.querySelectorAll('.nav a')];
      const sections = links.map(a => document.querySelector(a.getAttribute('href'))).filter(Boolean);
      const observer = new IntersectionObserver(entries => { entries.forEach(entry => { if (entry.isIntersecting) { links.forEach(a => a.classList.toggle('active', a.getAttribute('href') === '#' + entry.target.id)); } }) }, { rootMargin: '-25% 0px -65% 0px' });
      sections.forEach(s => observer.observe(s));
    })();
  </script>
</body>

</html>
"""

html = head + cover + s_essencial + s_viral + s_cadencia + s_tema + s_quando + s_formato + s_legenda + s_acoes + closing + script

# validação
body_only = html[html.index("<body>"):]
prosa = re.sub(r"<script>.*?</script>", "", body_only, flags=re.S)
erros = []
if "—" in prosa: erros.append("travessão no corpo: %d" % prosa.count("—"))
for termo in ["Joana", "drajoanatavares", "Sinfonya", "Pedro Brandão", "Juliana"]:
    if termo in html: erros.append("resquício de outro cliente: " + termo)
aspas = re.findall(r"<[^>]*[”“][^>]*>", html)
if aspas: erros.append("aspas curvas dentro de tag: %d" % len(aspas))
if "background-clip: text" in prosa: erros.append("gradient text")
ids_nav = re.findall(r'href="#([a-z]+)"', html)
ids_sec = re.findall(r'<section id="([a-z]+)"', html)
faltando = [i for i in ids_nav if i not in ids_sec]
if faltando: erros.append("nav aponta para seção inexistente: %s" % faltando)
canvas = re.findall(r'<canvas id="(\w+)"', html)
usados = re.findall(r"getElementById\('(\w+)'\)", html)
if sorted(canvas) != sorted(usados): erros.append("canvas x chart divergentes: %s vs %s" % (canvas, usados))
n_sec = len(ids_sec); n_ins = html.count('class="insight')
if n_ins < n_sec: erros.append("seções sem insight: %d seções, %d insights" % (n_sec, n_ins))

if erros:
    raise SystemExit("FALHOU:\n  " + "\n  ".join(erros))

OUT.write_text(html, encoding="utf-8")
print("ok:", OUT, len(html), "bytes |", n_sec, "seções |", n_ins, "insights |", len(canvas), "gráficos")
