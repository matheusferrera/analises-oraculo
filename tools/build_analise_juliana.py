# -*- coding: utf-8 -*-
import re, io, os

SRC = 'DrAdrianoBorges/Analise-Presenca-Digital.html'
OUT = 'JulianaArantes/Analise-Presenca-Digital.html'

src = open(SRC, encoding='utf-8').read()
i = src.find('<style'); j = src.find('</style>') + len('</style>')
STYLE = src[i:j]
assert len(STYLE) > 11000

TITLE = 'Análise de Presença Digital: Juliana Arantes e MOVE &amp; Connect | Oráculo'
DESC = ('Auditoria da presença digital de Juliana Arantes (@juharantes_) e da marca MOVE &amp; Connect, '
        'de Brasília: 144 publicações do Instagram lidas pela API interna, destaques, marca própria, busca no Google, '
        'domínio, página de venda no Sympla e comparativo com o networking empresarial do DF. '
        'Preparada pela Oráculo Tecnologia.')
BASE = 'https://analises-oraculo.vercel.app/JulianaArantes/'


WA = ('https://wa.me/5561995647260?text=Ol%C3%A1%21%20Vi%20a%20an%C3%A1lise%20de%20presen%C3%A7a%20digital%20'
      'do%20MOVE%20%26%20Connect%20e%20quero%20liberar%20o%20relat%C3%B3rio%20completo.')

LOCK_CSS = '''<style>
  .locked{position:relative;margin-top:1.35rem}
  .locked-content{max-height:24rem;overflow:hidden;filter:blur(7px);opacity:.48;pointer-events:none;user-select:none;-webkit-user-select:none}
  .locked-veil{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;padding:1.4rem;
    background:linear-gradient(180deg,rgba(251,251,253,.28) 0%,rgba(251,251,253,.88) 46%,rgba(251,251,253,.98) 100%)}
  .lock-card{background:var(--surface);border:1px solid var(--rule);width:100%;max-width:33rem;padding:1.5rem 1.6rem;text-align:center}
  .lock-card svg{color:var(--ink)}
  .lock-what{font-family:var(--sans);font-size:.95rem;font-weight:600;line-height:1.45;color:var(--text);margin:.7rem 0 0;text-wrap:balance}
  .lock-sub{font-size:.85rem;line-height:1.5;color:var(--text-3);margin-top:.4rem}
  .lock-cta{display:inline-block;margin-top:1.15rem;background:var(--ink);color:#fff;font-family:var(--sans);font-size:.8rem;font-weight:650;padding:.72rem 1.3rem;text-decoration:none;border:0;cursor:pointer;line-height:1.2}
  .lock-cta:hover{background:var(--primary)}
  .lock-alt{display:block;margin-top:.85rem;font-family:var(--sans);font-size:.76rem;color:var(--text-3);text-decoration:underline;text-underline-offset:3px}
  .lock-alt:hover{color:var(--ink)}
  .lock-form{margin-top:1.1rem;display:flex;flex-wrap:wrap;gap:.5rem;align-items:center;justify-content:center}
  .lock-label{width:100%;font-family:var(--sans);font-size:.72rem;color:var(--text-3)}
  .lock-input{font-family:var(--sans);font-size:.95rem;padding:.6rem .7rem;border:1px solid var(--rule);background:#fff;color:var(--text);width:9.5rem;text-align:center;letter-spacing:.2em}
  .lock-input:focus{outline:2px solid var(--primary);outline-offset:1px}
  .lock-go{font-family:var(--sans);font-size:.8rem;font-weight:650;padding:.63rem 1.1rem;background:var(--ink);color:#fff;border:0;cursor:pointer}
  .lock-go:hover{background:var(--primary)}
  .lock-err{width:100%;font-family:var(--sans);font-size:.75rem;color:var(--warn);margin:.1rem 0 0}
  .nav a.is-locked svg{width:9px;height:9px;margin-left:.32rem;opacity:.55;flex:none}
  .preview-note{border-color:var(--ink)}
  html.is-full .locked-content{max-height:none;overflow:visible;filter:none;opacity:1;pointer-events:auto;user-select:auto;-webkit-user-select:auto}
  html.is-full .locked-veil,html.is-full .nav a.is-locked svg,html.is-full .preview-note{display:none}
  @media(max-width:580px){.locked-content{max-height:19rem}.lock-card{padding:1.2rem 1.1rem}}
  @media print{.lock-card{border-color:var(--rule)}.locked-veil{background:rgba(251,251,253,.92)}}
</style>'''

UNLOCK_JS = '''<script>
(function(){
  window.__oraH=function(t){var v=5381,i;for(i=0;i<t.length;i++){v=(((v*33)%4294967296)^t.charCodeAt(i))>>>0;}return v;};
  window.__oraK=3780170254;
  window.__oraOpen=function(){document.documentElement.className+=' is-full';};
  try{
    var p=new URLSearchParams(location.search),ok=false;
    if(p.get('ver')==='completo'||location.hash==='#completo')ok=true;
    try{if(localStorage.getItem('oraculo-liberado')==='1')ok=true;}catch(e){}
    if(ok)window.__oraOpen();
  }catch(e){}
})();
</script>'''

LOCK_SVG = ('<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
            'stroke-linecap="round"><rect x="4" y="10.4" width="16" height="10.6" rx="1.6"/>'
            '<path d="M8 10.4V7a4 4 0 0 1 8 0v3.4"/></svg>')
NAV_SVG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true">'
           '<rect x="4" y="10.4" width="16" height="10.6" rx="1.6"/><path d="M8 10.4V7a4 4 0 0 1 8 0v3.4"/></svg>')

def veil(what, sub):
    return (f'<div class="locked-veil"><div class="lock-card">{LOCK_SVG}'
            f'<p class="lock-what">{what}</p><p class="lock-sub">{sub}</p>'
            '<button class="lock-cta" type="button" data-unlock>Liberar o relatório completo</button>'
            f'<a class="lock-alt" href="{WA}" target="_blank" rel="noopener">Ainda não tenho a senha, falar com a Oráculo</a>'
            '</div></div>')

def lockup(section_html, what, sub):
    """Envolve tudo o que vem depois do .sec-head no bloco travado."""
    k = section_html.index('<div class="sec-head">')
    e = section_html.index('</div>', k) + len('</div>')
    head, body = section_html[:e], section_html[e:]
    assert body.endswith('</section>')
    body = body[:-len('</section>')]
    return head + '<div class="locked"><div class="locked-content">' + body + '</div>' + veil(what, sub) + '</div></section>'


def insight(kind, verdict, text):
    return (f'<div class="insight {kind}"><div class="insight-header">'
            '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" '
            'style="vertical-align:-2px;margin-right:.35rem"><path d="M12 20h9"/>'
            '<path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>'
            'O que isso significa para você</div>'
            f'<div class="insight-body"><span class="verdict">{verdict}</span><p>{text}</p></div></div>')

def sec(idv, h2, sub=''):
    p = f'<p>{sub}</p>' if sub else ''
    return f'<section id="{idv}"><div class="sec-head"><h2>{h2}</h2>{p}</div>'

HEAD = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>{TITLE}</title>
<meta name="description" content="{DESC}"/>
<meta property="og:type" content="website"/>
<meta property="og:title" content="{TITLE}"/>
<meta property="og:description" content="{DESC}"/>
<meta property="og:image" content="{BASE}og-presenca.png"/>
<meta property="og:image:width" content="1200"/>
<meta property="og:image:height" content="630"/>
<meta property="og:url" content="{BASE}Analise-Presenca-Digital.html"/>
<meta property="og:site_name" content="Oráculo Tecnologia"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:image" content="{BASE}og-presenca.png"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous"/>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,200..800&amp;family=Petrona:ital,wght@0,400..700;1,400..600&amp;display=swap"/>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
{STYLE}
{LOCK_CSS}
{UNLOCK_JS}
</head>
<body>
'''

COVER = f'''<header class="cover">
  <div class="cover-inner">
    <div class="cover-mark"><b>Oráculo Tecnologia</b> · Auditoria de presença digital</div>
    <h1>Uma audiência de 19 mil pessoas e <em>uma marca de 423.</em></h1>
    <p class="cover-sub">Leitura completa de tudo o que um empresário de Brasília encontra sobre Juliana Arantes e o MOVE &amp; Connect antes de decidir se compra o ingresso de R$ 197: o Instagram pessoal, o perfil da marca, os destaques, a busca no Google, o domínio, a imprensa e a página de venda no Sympla.</p>
    <div class="cover-rule"></div>
    <div class="cover-foot"><span><b>Perfil:</b> @juharantes_</span><span><b>Marca:</b> MOVE &amp; Connect (@moveeconnect)</span><span><b>Praça:</b> Brasília, DF</span><span><b>Coleta:</b> 4 de setembro de 2026</span><span><b>Amostra:</b> 144 publicações</span></div>
  </div>
</header>
<div class="kpi-band"><div class="kpi-row">
  <div class="kpi"><div class="kpi-val">19.348</div><div class="kpi-label">Seguidores em @juharantes_</div><div class="kpi-note">289 posts, conta verificada</div></div>
  <div class="kpi"><div class="kpi-val">423</div><div class="kpi-label">Seguidores em @moveeconnect</div><div class="kpi-note">a conta que vende o ingresso</div></div>
  <div class="kpi"><div class="kpi-val">1.473</div><div class="kpi-label">Reproduções por Reel (mediana)</div><div class="kpi-note">7,6% da base, em 100 Reels</div></div>
  <div class="kpi"><div class="kpi-val">6 de 144</div><div class="kpi-label">Posts que levam ao ingresso</div><div class="kpi-note">4,2% da amostra lida</div></div>
  <div class="kpi"><div class="kpi-val">Zero</div><div class="kpi-label">Tags na página de venda</div><div class="kpi-note">sem pixel, GA4 ou Google Ads</div></div>
</div></div>
<nav class="nav">
  <a href="#essencial">O essencial</a><a href="#diagnostico">Diagnóstico</a>
  <a class="is-locked" href="#instagram">Instagram{NAV_SVG}</a>
  <a class="is-locked" href="#marca">A marca MOVE{NAV_SVG}</a>
  <a class="is-locked" href="#busca">Busca no Google{NAV_SVG}</a>
  <a class="is-locked" href="#venda">Caminho até o ingresso{NAV_SVG}</a>
  <a href="#comparativo">Comparativo</a>
  <a class="is-locked" href="#swot">SWOT{NAV_SVG}</a>
  <a class="is-locked" href="#recomendacoes">Plano de 180 dias{NAV_SVG}</a>
  <a class="is-locked" href="#resumo">Resumo{NAV_SVG}</a>
</nav>
<main class="page">
'''

# ---------------- 1. essencial ----------------
S1 = sec('essencial', 'O essencial em dois minutos',
         'Três achados que explicam a distância entre o tamanho da audiência e o resultado comercial.') + '''
<div class="essential">
  <div class="essential-main">
    <p class="lede">O trabalho de audiência está feito. Em 102 dias foram 144 publicações, 100 delas em Reels, com 176.634 reproduções somadas e uma conta verificada de 19.348 seguidores. O que falta é o outro lado: a marca que cobra pelo ingresso tem 423 seguidores, a página de venda não tem uma linha de rastreamento e o link do ingresso apareceu em 6 dos 144 posts lidos.</p>
  </div>
  <div class="card">
    <p class="eyebrow">Escopo desta leitura</p>
    <ul class="essential-list">
      <li>144 de 289 publicações do Instagram, com curtidas, comentários, reproduções e legendas</li>
      <li>16 pastas de destaques e 673 stories fixados</li>
      <li>Perfis @moveeconnect e @kalecozinhasensorial</li>
      <li>Busca de marca e de categoria no Google Brasil</li>
      <li>Registro de domínio, imprensa e redes secundárias</li>
      <li>Página de venda no Sympla, incluindo o código da página</li>
    </ul>
  </div>
</div>
<div class="grid-3">
  <div class="card"><p class="eyebrow">Achado 1</p><h3>A base é grande, a resposta é pequena</h3><p>A mediana de um Reel é de 1.473 reproduções, o equivalente a 7,6% dos seguidores, e a mediana de comentários por publicação é 2. Um perfil de 19 mil pessoas com esse nível de resposta indica uma base que foi construída mais rápido do que o interesse dela.</p></div>
  <div class="card"><p class="eyebrow">Achado 2</p><h3>Quem fala não é quem vende</h3><p>O perfil pessoal tem 45,7 vezes mais seguidores que o @moveeconnect, e a marca é citada em apenas 10% das publicações. Todo o valor construído fica preso em um ativo pessoal que não escala e não pode ser vendido a um patrocinador.</p></div>
  <div class="card"><p class="eyebrow">Achado 3</p><h3>O funil termina no escuro</h3><p>Faltando 15 dias para a 2ª edição, o ingresso apareceu em 2 das últimas 37 publicações. E a página do Sympla não tem pixel da Meta, Google Analytics nem tag do Google Ads, então nem a compra nem a visita podem ser medidas ou reimpactadas.</p></div>
</div>
''' + insight('warn', '&#9654; Atenção',
    'Nenhum dos três achados exige recomeçar nada. O ativo caro, que é a audiência e a produção diária de conteúdo, já está pronto e funcionando. O que está faltando custa pouco e leva dias: uma conta de marca alimentada, um pixel colado na página de venda e um caminho claro entre o Reel e o ingresso.') + '</section>'

# ---------------- 2. diagnostico ----------------
S2 = sec('diagnostico', 'Diagnóstico executivo',
         'Nota geral ponderada pelos seis pilares auditados, com peso maior para o que decide a venda de um ingresso online.') + '''
<div class="score">
  <div class="score-number"><span class="score-val">2,9</span><span class="score-den">/ 10</span></div>
  <p class="score-verdict"><b>Audiência construída, infraestrutura ausente.</b> A nota é baixa porque quatro dos seis pilares avaliados não existem ainda, e não porque o que existe esteja mal feito. O Instagram, sozinho, sustenta quase metade da pontuação.</p>
</div>
<div class="score-grid">
  <div class="score-item"><div class="score-item-head"><span>Instagram: alcance e conteúdo</span><span>5,5</span></div><div class="score-track"><div class="score-fill" style="width:55%"></div></div></div>
  <div class="score-item"><div class="score-item-head"><span>Marca MOVE como ativo</span><span>3,0</span></div><div class="score-track"><div class="score-fill" style="width:30%"></div></div></div>
  <div class="score-item"><div class="score-item-head"><span>Busca no Google</span><span>2,5</span></div><div class="score-track"><div class="score-fill" style="width:25%"></div></div></div>
  <div class="score-item"><div class="score-item-head"><span>Instagram: conversão</span><span>2,0</span></div><div class="score-track"><div class="score-fill" style="width:20%"></div></div></div>
  <div class="score-item"><div class="score-item-head"><span>Site e domínio próprio</span><span>1,0</span></div><div class="score-track"><div class="score-fill" style="width:10%"></div></div></div>
  <div class="score-item"><div class="score-item-head"><span>Rastreamento e mensuração</span><span>0,5</span></div><div class="score-track"><div class="score-fill" style="width:5%"></div></div></div>
</div>
<div class="diag">
  <div class="diag-col"><p class="eyebrow">Situação</p><ul>
    <li>Conta pessoal verificada, 19.348 seguidores e 42 publicações por mês</li>
    <li>Conta da marca com 423 seguidores e 134 publicações</li>
    <li>Nenhum domínio registrado, nenhum site</li>
    <li>Venda inteiramente hospedada no Sympla, sem rastreamento</li>
    <li>Curtidas ocultas em 96% das publicações</li>
  </ul></div>
  <div class="diag-col"><p class="eyebrow">Impacto</p><ul>
    <li>O patrocinador avalia a marca pelo perfil de 423 seguidores, não pelo de 19 mil</li>
    <li>Quem busca "MOVE Connect Brasília" encontra outra empresa na quarta posição</li>
    <li>Não é possível reimpactar quem abriu a página do ingresso e não comprou</li>
    <li>A prova social da 1ª edição não aparece em nenhuma superfície pública além da legenda</li>
    <li>A cada edição, o público volta ao ponto de partida</li>
  </ul></div>
  <div class="diag-col"><p class="eyebrow">Resposta</p><ul>
    <li>Colar o pixel da Meta e o GA4 na página do Sympla, hoje</li>
    <li>Trocar o botão de contato do Instagram de "Ligar" para WhatsApp</li>
    <li>Registrar moveeconnect.com.br, que está livre</li>
    <li>Publicar uma página única do MOVE com números, patrocinadores e lista de espera</li>
    <li>Migrar o público do perfil pessoal para a conta da marca por publicações em colaboração</li>
  </ul></div>
</div>
''' + insight('bad', '&#9654; Atenção',
    'A leitura de uma nota 2,9 não é "está tudo errado". É que a operação inteira está apoiada em um único ponto, o alcance orgânico de um perfil pessoal, e esse ponto vem caindo. Se o alcance cair mais 30%, não existe segundo canal para segurar a venda.') + '</section>'

# ---------------- 3. instagram ----------------
S3 = sec('instagram', 'Instagram: a audiência existe, a resposta dela não',
         '144 publicações entre 25 de maio e 4 de setembro de 2026, metade do acervo do perfil, lidas uma a uma pela API interna do Instagram.') + '''
<div class="metric-strip">
  <div class="metric"><div class="metric-value">1,41</div><div class="metric-label">Publicações por dia (42 por mês)</div></div>
  <div class="metric"><div class="metric-value">1.473</div><div class="metric-label">Reproduções por Reel, mediana</div></div>
  <div class="metric"><div class="metric-value">2</div><div class="metric-label">Comentários por publicação, mediana</div></div>
  <div class="metric"><div class="metric-value">0,023%</div><div class="metric-label">Comentários por seguidor</div></div>
</div>
<h3>O alcance por Reel caiu 44% enquanto o volume de publicação subiu</h3>
<p>Na primeira quinzena de junho a mediana de um Reel era 2.158 reproduções, ou 11,2% dos seguidores. Na primeira quinzena de setembro é 1.215, ou 6,3%. No mesmo intervalo a cadência subiu de 1,19 para 1,53 publicação por dia. É o padrão clássico de um perfil que responde à queda de entrega publicando mais, e o algoritmo lê isso como mais material para distribuir entre as mesmas pessoas.</p>
<div class="chart"><canvas id="chartAlcance"></canvas></div>
<div class="table-wrap"><table>
<thead><tr><th>Quinzena</th><th class="right">Reels</th><th class="right">Reproduções (mediana)</th><th class="right">% dos seguidores</th><th>Momento</th></tr></thead>
<tbody>
<tr><td>2ª de maio de 2026</td><td class="right">5</td><td class="right">1.850</td><td class="right">9,6%</td><td>anúncio da 1ª edição</td></tr>
<tr><td>1ª de junho de 2026</td><td class="right">13</td><td class="right">2.158</td><td class="right">11,2%</td><td>véspera da 1ª edição</td></tr>
<tr><td>2ª de junho de 2026</td><td class="right">14</td><td class="right">1.384</td><td class="right">7,2%</td><td>1ª edição, dia 20</td></tr>
<tr><td>1ª de julho de 2026</td><td class="right">13</td><td class="right">1.847</td><td class="right">9,5%</td><td>pós-evento</td></tr>
<tr><td>2ª de julho de 2026</td><td class="right">26</td><td class="right">1.233</td><td class="right">6,4%</td><td>pico de volume</td></tr>
<tr><td>1ª de agosto de 2026</td><td class="right">14</td><td class="right">1.247</td><td class="right">6,4%</td><td>anúncio da 2ª edição</td></tr>
<tr><td>2ª de agosto de 2026</td><td class="right">9</td><td class="right">1.319</td><td class="right">6,8%</td><td>patrocinadores</td></tr>
<tr><td>1ª de setembro de 2026</td><td class="right">6</td><td class="right">1.215</td><td class="right">6,3%</td><td>15 dias para o evento</td></tr>
</tbody></table></div>
<p class="muted" style="font-size:.8rem">Fonte: 100 Reels da amostra, campo de reproduções da API interna do Instagram, coleta de 04/09/2026. Percentual calculado sobre os 19.348 seguidores do dia da coleta.</p>
<h3>O conteúdo pessoal alcança mais do que o conteúdo comercial</h3>
<p>Entre os 100 Reels lidos, os 43 que citam o MOVE têm mediana de 1.319 reproduções. Os 57 que não citam têm 1.591. A diferença de 17% aparece de forma consistente e diz uma coisa útil: a audiência foi construída em torno da pessoa, não da marca. Isso é uma vantagem enquanto ela puxa o evento pelo próprio nome, e vira um problema no dia em que o MOVE precisar existir sem ela na frente da câmera.</p>
<div class="grid-2">
  <div class="card"><p class="eyebrow">Mix de formatos</p><h3>Reels são 69% do que se publica</h3><p>100 Reels, 29 carrosséis e 15 imagens. A distribuição está correta para o objetivo de alcance, e os carrosséis, que costumam sustentar o conteúdo denso, ficaram em 20%. É o formato com maior espaço para crescer: são eles que aguentam explicar o método do MOVE em profundidade.</p></div>
  <div class="chart sm"><canvas id="chartFormatos"></canvas></div>
</div>
<h3>As curtidas estão ocultas em 96% das publicações</h3>
<p>Em 138 das 144 publicações lidas a contagem de curtidas está desativada. Nas 6 em que ela aparece, porque a decisão pertence a um perfil parceiro, os números vão de 20 a 175 curtidas. Para uma criadora de conteúdo, esconder curtidas é uma escolha legítima de saúde mental. Para quem vende um encontro presencial de R$ 197 apoiado na ideia de que 147 empresários já foram, é o oposto: a prova social é exatamente o produto, e ela está desligada.</p>
''' + insight('bad', '&#9654; Atenção',
    'A conta publica quase todo dia, produz bem e chega, na mediana, a 7,6% da própria base. O gargalo não é esforço nem qualidade de produção, é distribuição e destino. Antes de aumentar o volume outra vez, vale entender de onde vêm os 19 mil seguidores. Esse dado está no aplicativo, na aba de público do perfil profissional, e é a peça que falta para saber quantos deles moram no Distrito Federal.') + '</section>'

# ---------------- 4. marca ----------------
S4 = sec('marca', 'A marca MOVE como ativo digital',
         'O que um patrocinador, um parceiro ou um empresário encontra quando procura pela marca, e não pela pessoa.') + '''
<div class="metric-strip">
  <div class="metric"><div class="metric-value">45,7x</div><div class="metric-label">Diferença entre o perfil pessoal e o da marca</div></div>
  <div class="metric"><div class="metric-value">10%</div><div class="metric-label">Publicações que marcam @moveeconnect</div></div>
  <div class="metric"><div class="metric-value">673</div><div class="metric-label">Stories fixados nos destaques</div></div>
  <div class="metric"><div class="metric-value">4,3%</div><div class="metric-label">Desses stories que falam de negócio</div></div>
</div>
<h3>A conta que vende o ingresso tem 423 seguidores</h3>
<p>Em 22 de junho de 2026 a própria Juliana publicou os números do @moveeconnect: 237 seguidores e 72.300 visualizações em 30 dias. Em 4 de setembro a conta está com 423 seguidores, 228 seguindo e 134 publicações. São 186 seguidores em 74 dias, um ritmo de 2,5 por dia. Nesse ritmo, a marca chega ao dia do evento com pouco mais de 460 pessoas, enquanto o perfil pessoal tem 19.348.</p>
<div class="chart sm"><canvas id="chartMarca"></canvas></div>
<p>A bio do @moveeconnect está bem escrita e já faz o trabalho comercial que a do perfil pessoal divide com outras coisas: traz os 147 empresários da 1ª edição, a data da 2ª, uma frase de posicionamento e o link direto do Sympla. O problema não é o que a conta diz, é quantas pessoas leem.</p>
<div class="callout"><strong>Por que isso custa dinheiro</strong><p>Patrocínio de evento se vende com número de audiência. Quando a VIP Care, a Chopp Brasília ou a Jovem Pan avaliam o MOVE, o que elas abrem é o @moveeconnect. O perfil que carrega a audiência de verdade é o pessoal, e ele não pode ser oferecido como mídia de patrocinador sem transformar a empresária no produto. <b>A conta da marca é o ativo vendável, e hoje ela vale 2,2% do que a pessoal vale.</b></p></div>
<h3>Os destaques são um diário de viagem com um apêndice de negócios</h3>
<p>O perfil tem 16 pastas de destaque somando 673 stories fixados. Treze delas são viagens pela Europa: Croácia, Ístria, Dalmácia, Holanda, Alemanha, França, Bélgica, Áustria, Itália, Espanha, Portugal, Tenerife e Gran Canaria, com 644 stories no total. As três de negócio, MOVE, MOVE 2000 e KALE, somam 29. Os destaques são a vitrine permanente de um perfil, o único lugar onde alguém que chegou hoje consegue entender o que foi a 1ª edição. Hoje 95,7% dessa vitrine mostra a Europa.</p>
<div class="grid-2">
  <div class="chart sm"><canvas id="chartDestaques"></canvas></div>
  <div class="card"><p class="eyebrow">Ordem atual das pastas</p><h3>MOVE 2000 tem 6 stories, Ístria tem 99</h3><p>A pasta do evento que está sendo vendido tem seis stories fixados. A pasta da região da Ístria, na Croácia, tem noventa e nove. Reordenar e reabastecer os destaques é a intervenção mais barata desta auditoria: não custa produção nova, só decisão sobre o que fica na frente.</p></div>
</div>
<h3>Sete nomes para a mesma coisa</h3>
<p>Circulam nas legendas, ao mesmo tempo, MOVE &amp; Connect, MOVE Anos 2000, MOVE KIDS, MOVE TALK, Camarote MOVE, Laboratório MOVE e Embaixadores MOVE. O arroba é @moveeconnect, com dois "e". O Sympla registra o evento como "MOVE &amp; Connect | Anos 2000". A única matéria de imprensa indexada no Google descreve a marca como "Move Conet". Sete sub-marcas em três meses é uma expansão de portfólio que ainda não tem público para sustentar: cada uma divide a atenção da mesma audiência de 423 pessoas.</p>
''' + insight('bad', '&#9733; Destaque',
    'Este é o achado mais caro da auditoria e o mais barato de corrigir. A audiência de 19 mil pessoas foi construída e paga. Migrar parte dela para a conta da marca custa apenas publicar em colaboração, um recurso nativo do Instagram em que o post aparece nos dois perfis e conta para os dois. Feito em toda publicação sobre o evento, ele levaria a marca de 423 para a casa dos milhares antes da 3ª edição.') + '</section>'

# ---------------- 5. busca ----------------
S5 = sec('busca', 'Busca no Google: quem procura o MOVE em Brasília',
         'O que aparece na busca pelo nome da marca e na busca pela categoria, em Brasília, no dia da coleta.') + '''
<h3>Na busca pelo nome da marca, a quarta posição é de outra empresa</h3>
<p>Para "MOVE Connect Brasília networking", a primeira posição é o perfil do Instagram, a segunda é a página do Sympla e a terceira é a matéria do portal Brasília Comércio. A quarta posição é connectmove.com.br, uma agência de experiências internacionais de viagem, que não tem relação com o evento. O domínio moveconnect.com.br pertence a um terceiro desde antes. E existe ainda um coworking chamado Move Connect que aparece nos resultados de vídeo.</p>
<div class="table-wrap"><table>
<thead><tr><th>Posição</th><th>O que aparece</th><th>É seu?</th><th>Tipo</th></tr></thead>
<tbody>
<tr><td>1</td><td>Instagram @moveeconnect</td><td><span class="status good">Sim</span></td><td>Rede social</td></tr>
<tr><td>2</td><td>Sympla, MOVE &amp; Connect Anos 2000</td><td><span class="status good">Sim</span></td><td>Página de venda de terceiro</td></tr>
<tr><td>3</td><td>Brasília Comércio, matéria sobre conexão neutra</td><td><span class="status">Citação</span></td><td>Imprensa local</td></tr>
<tr><td>4</td><td>connectmove.com.br</td><td><span class="status warn">Não</span></td><td>Site de outra empresa</td></tr>
<tr><td>5</td><td>Sympla, MOVE &amp; Connect Edição Junina</td><td><span class="status good">Sim</span></td><td>Evento encerrado</td></tr>
</tbody></table></div>
<p class="muted" style="font-size:.8rem">Fonte: google.com/search com hl=pt-BR e gl=br, consulta "MOVE Connect Brasília networking", 04/09/2026.</p>
<h3>Na busca pela categoria, quem tem site ocupa o lugar</h3>
<p>Para "networking empresarial Brasília evento empresários", o MOVE aparece apenas na décima posição, e ainda assim por meio do perfil do Instagram. A terceira posição é do MOAI Clube de Líderes, que tem site próprio em moaiclubedelideres.com. O padrão é conhecido e simples: quem tem domínio ocupa a busca de categoria, quem só tem rede social ocupa a busca de marca. Hoje o MOVE só é encontrado por quem já sabe o nome.</p>
<div class="callout"><strong>O domínio da marca está livre</strong><p>Consulta ao registro.br em 04/09/2026: <b>moveeconnect.com.br não tem registro</b>, está disponível. O moveconnect.com.br, com um "e" só, pertence a terceiro. Registrar o domínio correto custa menos de cinquenta reais por ano e resolve, de uma vez, a busca de marca, o endereço de e-mail profissional e o lugar onde a prova social da 1ª edição pode finalmente morar.</p></div>
<h3>Fora do Instagram e do Sympla, quase não existe rastro</h3>
<div class="table-wrap"><table>
<thead><tr><th>Canal</th><th>Situação em 04/09/2026</th><th>Estado</th></tr></thead>
<tbody>
<tr><td>Site próprio</td><td>Nenhum domínio registrado em nome da marca</td><td><span class="status warn">Ausente</span></td></tr>
<tr><td>Perfil da Empresa no Google</td><td>Nenhuma ficha para MOVE, Juliana Arantes ou KALE nas buscas locais</td><td><span class="status warn">Ausente</span></td></tr>
<tr><td>Facebook</td><td>Página "Juliana Arantes" com 7 seguidores e conteúdo espelhado do Instagram</td><td><span class="status warn">Inativa</span></td></tr>
<tr><td>LinkedIn</td><td>Nenhum perfil da marca localizado. A busca pelo nome retorna outras pessoas homônimas</td><td><span class="status warn">Ausente</span></td></tr>
<tr><td>YouTube e TikTok</td><td>Nenhum canal localizado nas buscas de marca</td><td><span class="status warn">Ausente</span></td></tr>
<tr><td>Imprensa</td><td>Uma matéria indexada, no portal Brasília Comércio, com o nome grafado "Move Conet"</td><td><span class="status">Parcial</span></td></tr>
<tr><td>Sympla</td><td>Duas edições publicadas, produtor sem página, sem logo e sem descrição</td><td><span class="status">Parcial</span></td></tr>
</tbody></table></div>
''' + insight('info', '&#9654; Atenção',
    'Um evento de networking empresarial vive de reputação verificável: alguém ouve falar, procura o nome, encontra provas e decide. Hoje essa busca termina em duas páginas de terceiros e uma matéria que escreve o nome errado. É um problema de infraestrutura, não de conteúdo, e por isso ele tem prazo de resolução em semanas e não em meses.') + '</section>'

# ---------------- 6. venda ----------------
S6 = sec('venda', 'O caminho até o ingresso',
         'Da primeira reprodução de um Reel ao pagamento de R$ 197, passo a passo, com o que se perde em cada etapa.') + '''
<div class="metric-strip">
  <div class="metric"><div class="metric-value">176.634</div><div class="metric-label">Reproduções somadas em 102 dias</div></div>
  <div class="metric"><div class="metric-value">4,5%</div><div class="metric-label">Delas em posts que citam o ingresso</div></div>
  <div class="metric"><div class="metric-value">7,6%</div><div class="metric-label">Publicações com qualquer chamada</div></div>
  <div class="metric"><div class="metric-value">15 dias</div><div class="metric-label">Até a 2ª edição, em 19/09</div></div>
</div>
<h3>Das 176.634 reproduções, 7.998 vieram de posts que apontam para a compra</h3>
<p>Seis publicações das 144 lidas citam o Sympla, o ingresso ou o link na bio. Elas somam 7.998 reproduções, 4,5% de tudo o que o perfil entregou no período. Nos últimos 30 dias, com o evento já datado e anunciado, foram 2 publicações com o ingresso em 37. Todo o resto do alcance, 168.636 reproduções, passou por um perfil que não pedia nada em troca.</p>
<div class="chart"><canvas id="chartFunil"></canvas></div>
<h3>O botão de contato do perfil está configurado para ligação</h3>
<p>O perfil profissional oferece o botão de contato no modo "Ligar". Para um público de empresários que decide compra dentro do próprio Instagram, telefone é a maior fricção possível: exige sair do aplicativo, escolher um horário e falar. O WhatsApp já está na bio como segundo link, o que mostra que a intenção existe, mas ele não ocupa o lugar em que o dedo do visitante encosta primeiro.</p>
<div class="table-wrap"><table>
<thead><tr><th>Etapa</th><th>O que existe hoje</th><th>O que se perde</th></tr></thead>
<tbody>
<tr><td>1. Descoberta</td><td>Reel com mediana de 1.473 reproduções</td><td>Nada, esta etapa funciona</td></tr>
<tr><td>2. Chamada para ação</td><td>Presente em 7,6% das publicações</td><td>92,4% do alcance não recebe convite algum</td></tr>
<tr><td>3. Perfil</td><td>Bio com dois links e botão "Ligar"</td><td>O ingresso disputa espaço com o WhatsApp, sem hierarquia</td></tr>
<tr><td>4. Página de venda</td><td>Sympla, R$ 197 individual e R$ 357 duplo, 12x</td><td>Sem pixel, sem GA4, sem tag de conversão</td></tr>
<tr><td>5. Pós-visita</td><td>Nenhum público de remarketing existe</td><td>Quem abriu e não comprou não pode ser reimpactado</td></tr>
<tr><td>6. Pós-evento</td><td>Nenhum cadastro próprio, nenhuma lista</td><td>A cada edição a base de compradores recomeça do zero</td></tr>
</tbody></table></div>
<div class="callout"><strong>O que o código da página de venda mostra</strong><p>A leitura do HTML da página do evento no Sympla, em 04/09/2026, mostra os campos de integração todos vazios: o token do Facebook está nulo e os seis eventos do pixel (PageView, AddToCart, InitiateCheckout, AddPaymentInfo, Lead e Purchase) estão todos desligados; não há código do Google Analytics, nem identificador de conversão do Google Ads, nem token do RD Station, nem script no cabeçalho ou no corpo. <b>O Sympla oferece todos esses campos prontos no painel do organizador, sem custo e sem programação.</b> Preenchê-los é trabalho de uma tarde e muda o que se sabe sobre a próxima edição.</p></div>
<h3>A prova social mais forte que existe não está publicada em lugar nenhum</h3>
<p>A página do Sympla e a bio dizem que a 1ª edição teve 147 empresários, que 89% dos expositores geraram negócio e que a permanência média foi de 5 horas. A edição de junho foi anunciada como um encontro para 70 empresários, o que faz do resultado final mais que o dobro do previsto. Esse é o melhor argumento comercial que a marca tem, e ele hoje só existe dentro de uma legenda e de um parágrafo no Sympla. Não há uma página, um post fixado, um destaque nem um release que o registre de forma verificável.</p>
''' + insight('bad', '&#9654; Atenção',
    'Faltam 15 dias para o evento e há duas coisas que ainda dá tempo de fazer, nesta ordem: instalar o pixel da Meta no painel do Sympla, para que a 2ª edição já produza um público de remarketing utilizável na 3ª; e fixar no topo do perfil três publicações, uma com a prova da 1ª edição, uma com o que está incluso e uma com o link de compra. As duas juntas levam menos de uma tarde.') + '</section>'

# ---------------- 7. comparativo ----------------
S7 = sec('comparativo', 'Comparativo com o networking empresarial do DF',
         'Perfis medidos pelo mesmo método e na mesma data, escolhidos por ocuparem o espaço que o MOVE quer ocupar em Brasília.') + '''
<div class="chart"><canvas id="chartConcorrentes"></canvas></div>
<div class="table-wrap"><table>
<thead><tr><th>Perfil</th><th>O que é</th><th class="right">Seguidores</th><th class="right">Publicações</th><th>Para onde o link da bio leva</th></tr></thead>
<tbody>
<tr><td>@juharantes_</td><td>Perfil pessoal, Juliana Arantes</td><td class="right">19.348</td><td class="right">289</td><td>Sympla e WhatsApp <span class="status warn">Sem site</span></td></tr>
<tr><td>@bnidf</td><td>BNI Distrito Federal</td><td class="right">3.136</td><td class="right">393</td><td>bnidf.com.br/seja-bni <span class="status good">Site próprio</span></td></tr>
<tr><td>@bnidfpiloto</td><td>Núcleo BNI DF Piloto</td><td class="right">1.976</td><td class="right">1.226</td><td>bnidf.com.br <span class="status good">Site próprio</span></td></tr>
<tr><td>@empreendeclube</td><td>Clube de empreendedores do DF</td><td class="right">740</td><td class="right">58</td><td>Sem link na bio <span class="status warn">Sem site</span></td></tr>
<tr><td>@moveeconnect</td><td>MOVE &amp; Connect</td><td class="right">423</td><td class="right">134</td><td>Sympla do evento <span class="status warn">Sem site</span></td></tr>
<tr><td>@confraempresariasbsb</td><td>Confraria de empresárias de Brasília</td><td class="right">210</td><td class="right">10</td><td>Grupo de WhatsApp <span class="status warn">Sem site</span></td></tr>
<tr><td>@empresariosdebrasilia</td><td>Comunidade de empresários</td><td class="right">141</td><td class="right">56</td><td>WhatsApp <span class="status warn">Sem site</span></td></tr>
</tbody></table></div>
<p class="muted" style="font-size:.8rem">Fonte: API interna do Instagram, seguidores, publicações e links da bio lidos em 04/09/2026. O MOAI Clube de Líderes não entrou na tabela porque o perfil não foi localizado pela busca do Instagram, mas o site moaiclubedelideres.com ocupa a terceira posição na busca de categoria no Google.</p>
<div class="grid-2">
  <div class="card"><p class="eyebrow">O que você já venceu</p><h3>Nenhum concorrente local tem audiência comparável</h3><p>O maior perfil institucional de networking empresarial do DF encontrado nesta leitura, o @bnidf, tem 3.136 seguidores. O perfil de Juliana tem 6,2 vezes mais. Em uma praça onde ninguém passa de quatro mil seguidores, a audiência já construída é uma vantagem estrutural, não uma vaidade.</p></div>
  <div class="card"><p class="eyebrow">O que falta montar</p><h3>Só quem tem domínio aparece na busca de categoria</h3><p>Dos sete perfis medidos, apenas os dois do BNI levam a um site próprio. Os outros cinco, o MOVE incluído, mandam o visitante para WhatsApp, Sympla ou lugar nenhum. É exatamente por isso que BNI e MOAI aparecem na busca por "networking empresarial Brasília" e o MOVE não: a vantagem de audiência não vira descoberta enquanto não houver um endereço próprio para receber quem procura o assunto, e não o nome.</p></div>
</div>
''' + insight('good', '&#9650; Bom',
    'Esta é a melhor notícia da auditoria. O MOVE não disputa audiência com gigantes, disputa com comunidades locais que têm entre 140 e 3.100 seguidores. A audiência necessária para dominar essa praça já existe, está no perfil pessoal, e só precisa ser transferida para um ativo de marca com endereço próprio.') + '</section>'

# ---------------- 8. swot ----------------
S8 = sec('swot', 'Análise SWOT', 'Síntese da posição nos seis pilares auditados.') + '''
<div class="swot">
  <div class="swot-cell"><h3>Forças</h3><ul>
    <li>19.348 seguidores e conta verificada, seis vezes o maior perfil de networking do DF</li>
    <li>Produção diária consistente, 42 publicações por mês, com identidade visual definida</li>
    <li>Prova de operação real: 147 presentes na 1ª edição, patrocinadores e embaixadores</li>
    <li>Marca gastronômica própria, a KALE, que diferencia a experiência de qualquer concorrente</li>
    <li>Parcerias institucionais já firmadas com EmpreendeDF, Guia BSB e imprensa local</li>
  </ul></div>
  <div class="swot-cell"><h3>Fraquezas</h3><ul>
    <li>Conta da marca com 423 seguidores, 2,2% da audiência pessoal</li>
    <li>Alcance por Reel em queda de 44% desde junho, mesmo com mais publicação</li>
    <li>Nenhum domínio, nenhum site, nenhuma lista de contatos própria</li>
    <li>Página de venda sem qualquer rastreamento instalado</li>
    <li>Curtidas ocultas em 96% das publicações, num negócio que vende prova social</li>
    <li>Chamada para ação em 7,6% das publicações e ingresso em 4,2%</li>
  </ul></div>
  <div class="swot-cell"><h3>Oportunidades</h3><ul>
    <li>O domínio moveeconnect.com.br está livre para registro</li>
    <li>Publicação em colaboração migra audiência do perfil pessoal para a marca sem custo</li>
    <li>O painel do Sympla já tem campos prontos para pixel, GA4 e Google Ads</li>
    <li>Os destaques podem virar a vitrine do método sem nenhuma produção nova</li>
    <li>Nenhum concorrente local ocupa a busca por "networking empresarial em Brasília" com conteúdo</li>
  </ul></div>
  <div class="swot-cell"><h3>Ameaças</h3><ul>
    <li>Colisão de nome com connectmove.com.br e com um coworking chamado Move Connect</li>
    <li>Dependência total do alcance orgânico de um único perfil, que vem caindo</li>
    <li>Sete sub-marcas dividindo a atenção de uma base de 423 pessoas</li>
    <li>BNI e MOAI ocupam a busca de categoria com site e estrutura de captação</li>
    <li>Sem lista própria, cada edição exige reconstruir a demanda do zero</li>
  </ul></div>
</div>
''' + insight('purple', '&#9654; Atenção',
    'As fraquezas desta análise têm uma característica em comum: todas são de infraestrutura, e nenhuma é de produto ou de execução. O evento acontece, tem público, tem patrocinador e tem imprensa. O que não existe ainda é a camada digital que transforma cada edição em base para a seguinte.') + '</section>'

# ---------------- 9. recomendacoes ----------------
S9 = sec('recomendacoes', 'Plano estratégico de 180 dias',
         'Três ciclos com dependência clara: salvar o que dá para salvar antes de 19 de setembro, transformar a 2ª edição em ativo, e construir descoberta.') + '''
<div class="roadmap">
  <div class="phase"><div class="phase-time">Até 19 de setembro, 15 dias</div><h3>Salvar a 2ª edição</h3><ol>
    <li>Instalar o pixel da Meta e o GA4 no painel do Sympla, nos campos de integração do evento</li>
    <li>Trocar o botão de contato do Instagram de "Ligar" para WhatsApp</li>
    <li>Reativar a contagem de curtidas nas publicações sobre o evento</li>
    <li>Fixar três publicações no topo do perfil: prova da 1ª edição, o que está incluso, como comprar</li>
    <li>Publicar todo post do evento em colaboração com o @moveeconnect</li>
    <li>Sequência diária de stories com o link do Sympla, quinze dias seguidos</li>
    <li>Combinar antes a captura do dia: fotos, depoimentos em vídeo e contagem de presentes</li>
  </ol><div class="phase-kpi">Meta: público de remarketing criado e ingresso presente em pelo menos metade das publicações da quinzena.</div></div>
  <div class="phase"><div class="phase-time">Dias 1 a 30 após o evento</div><h3>Transformar a edição em ativo</h3><ol>
    <li>Registrar moveeconnect.com.br e apontar para uma página única do MOVE</li>
    <li>Publicar nessa página os números das duas edições, os patrocinadores e um formulário de lista de espera</li>
    <li>Reordenar os destaques, com MOVE, Edições e Patrocinadores nas três primeiras posições</li>
    <li>Reabastecer o destaque do evento com o material captado em 19 de setembro</li>
    <li>Enviar release da 2ª edição para a imprensa local, com o nome grafado corretamente</li>
    <li>Padronizar um único nome público e recolher as sub-marcas que não têm público próprio</li>
  </ol><div class="phase-kpi">Meta: domínio no ar, primeira lista de e-mails formada e prova social verificável fora do Instagram.</div></div>
  <div class="phase"><div class="phase-time">Dias 31 a 180</div><h3>Construir descoberta</h3><ol>
    <li>Abrir Perfil da Empresa no Google para o MOVE, com área de atendimento em Brasília</li>
    <li>Migrar audiência do perfil pessoal para o @moveeconnect em toda publicação de marca</li>
    <li>Publicar conteúdo de busca no site sobre networking empresarial em Brasília</li>
    <li>Criar página por edição, para que cada evento passado continue captando</li>
    <li>Usar o público de remarketing da 2ª edição para vender a 3ª com mídia paga medida</li>
    <li>Puxar o relatório de público do Instagram e desenhar o conteúdo pela cidade real dos seguidores</li>
  </ol><div class="phase-kpi">Meta: MOVE entre os cinco primeiros resultados para "networking empresarial Brasília" e marca acima de três mil seguidores.</div></div>
</div>
<h3>Sequência que protege o investimento</h3>
<div class="priority"><div class="priority-num">1</div><div><h3>Pixel da Meta e GA4 na página do Sympla</h3><p>Sem eles, a 2ª edição passa sem deixar dado. Com eles, quem visitar a página vira público de remarketing para a 3ª.</p></div><span class="status good">Hoje, sem custo</span></div>
<div class="priority"><div class="priority-num">2</div><div><h3>Publicação em colaboração com o @moveeconnect</h3><p>Recurso nativo do Instagram, aparece nos dois perfis e conta para os dois. É o caminho mais barato de tirar a marca dos 423 seguidores.</p></div><span class="status good">Hoje, sem custo</span></div>
<div class="priority"><div class="priority-num">3</div><div><h3>Registro de moveeconnect.com.br</h3><p>Resolve a busca de marca, dá endereço à prova social e afasta a confusão com connectmove.com.br.</p></div><span class="status">Menos de R$ 50 por ano</span></div>
<div class="priority"><div class="priority-num">4</div><div><h3>Reordenar e reabastecer os destaques</h3><p>A vitrine do perfil hoje tem 644 stories de viagem e 29 de negócio. Reordenar não exige produção nova.</p></div><span class="status">Uma tarde</span></div>
<div class="priority"><div class="priority-num">5</div><div><h3>Botão do perfil no WhatsApp e curtidas visíveis</h3><p>Encurta o caminho entre quem assistiu ao Reel e quem pergunta o preço, e devolve a prova social ao produto que a vende.</p></div><span class="status good">Dois toques</span></div>
''' + insight('info', '&#9650; Bom',
    'As cinco prioridades somam menos de cinquenta reais e algumas horas de trabalho. Nenhuma delas depende de contratar equipe, produzir conteúdo novo ou investir em mídia. Elas apenas conectam entre si as peças que já foram construídas nos últimos quatro meses.') + '</section>'

# ---------------- 10. resumo ----------------
S10 = sec('resumo', 'Resumo executivo e pontuação', 'Onde está o retorno mais rápido.') + '''
<div class="chart"><canvas id="chartScore"></canvas></div>
<div class="grid-3">
  <div class="card"><p class="eyebrow">O que já está pronto</p><h3>Audiência, produção e prova de operação</h3><p>19.348 seguidores verificados, 42 publicações por mês, 147 empresários na 1ª edição, patrocinadores ativos, embaixadores e imprensa local. É a parte cara, e ela está feita.</p></div>
  <div class="card"><p class="eyebrow">O que falta ligar</p><h3>Marca, endereço e medição</h3><p>Uma conta de marca alimentada pela audiência que já existe, um domínio próprio onde a prova social possa morar e um pixel na página que recebe o dinheiro.</p></div>
  <div class="card"><p class="eyebrow">O que decide a 3ª edição</p><h3>O que for capturado em 19 de setembro</h3><p>O público de remarketing, os depoimentos em vídeo, as fotos e a contagem de presentes da 2ª edição são o material com que a 3ª será vendida. Nada disso se recupera depois.</p></div>
</div>
<div class="callout"><strong>A pergunta que esta auditoria não conseguiu responder</strong><p>Não existe forma pública de saber onde moram os 19.348 seguidores do perfil. Para um evento presencial em Brasília, essa é a variável mais importante de todas: se a maior parte da base estiver fora do Distrito Federal, a mediana de 1.473 reproduções por Reel vale menos do que parece. <b>Esse dado está no aplicativo, em Painel profissional e depois Público, e leva dois minutos para ser lido.</b> Ele deve ser o primeiro número a entrar em qualquer plano de mídia.</p></div>
''' + insight('purple', '&#9733; Destaque',
    'A distância entre 19.348 e 423 é o resumo desta auditoria em dois números. Ela não representa um erro de execução, representa quatro meses de trabalho investidos em um ativo pessoal em vez de um ativo de marca. A correção não exige recomeçar: exige que cada publicação, a partir de agora, deixe alguma coisa registrada em um endereço que pertença ao MOVE.') + '</section>'

CLOSING = '''</main>
<div class="closing"><div class="closing-inner"><h2>A audiência já foi construída. Falta dar a ela um lugar para chegar.</h2><p>Esta leitura não encontrou um problema de conteúdo. Encontrou 176.634 reproduções em 102 dias desembocando em uma bio com dois links, um botão de telefone e uma página de venda que não mede nada. O que separa a 2ª edição da 3ª já não depende de alcance. Depende da primeira estrutura própria: uma conta de marca alimentada, um domínio no ar e um pixel instalado antes de 19 de setembro.</p><div class="closing-meta">Oráculo Tecnologia · Presença digital · 1ª coleta · Setembro de 2026</div></div></div>
<footer><span>Oráculo Tecnologia © 2026</span><span>Fontes públicas coletadas em 04/09/2026 · Instagram (144 de 289 publicações via API interna), destaques, perfis @moveeconnect e @kalecozinhasensorial, Google Brasil, registro.br, Facebook e página do evento no Sympla</span></footer>
'''

SCRIPT = '''
<script>
(() => {
  const ink='#1b2e73', primary='#1d4ed8', soft='#b3c0ea', rule='#dfe1ec', good='#15803d', warnc='#d97706', purple='#6d28d9';
  Chart.defaults.font.family="'Bricolage Grotesque', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif";
  Chart.defaults.color='#6b7186';
  Chart.defaults.plugins.legend.labels.usePointStyle=true;
  Chart.defaults.plugins.legend.labels.boxWidth=7;
  const grid={color:'#ebedf4'};

  new Chart(document.getElementById('chartAlcance'),{type:'bar',
    data:{labels:[['2ª mai'],['1ª jun'],['2ª jun'],['1ª jul'],['2ª jul'],['1ª ago'],['2ª ago'],['1ª set']],
      datasets:[{label:'Reproduções por Reel (mediana)',data:[1850,2158,1384,1847,1233,1247,1319,1215],
        backgroundColor:[soft,good,soft,soft,ink,ink,ink,ink],borderRadius:2}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},
      title:{display:true,text:'Mediana de reproduções por Reel, por quinzena · queda de 44% desde a 1ª de junho'},
      tooltip:{callbacks:{afterLabel:c=>(c.parsed.y/19348*100).toFixed(1)+'% dos seguidores'}}},
      scales:{y:{beginAtZero:true,grid},x:{grid:{display:false}}}}});

  new Chart(document.getElementById('chartFormatos'),{type:'doughnut',
    data:{labels:['Reels · 100','Carrosséis · 29','Imagens · 15'],
      datasets:[{data:[100,29,15],backgroundColor:[ink,soft,rule],borderColor:'#fff',borderWidth:3}]},
    options:{responsive:true,maintainAspectRatio:false,cutout:'64%',
      plugins:{legend:{position:'bottom'},title:{display:true,text:'Mix de formatos · 144 publicações'}}}});

  new Chart(document.getElementById('chartMarca'),{type:'bar',
    data:{labels:[['@juharantes_','pessoal'],['@moveeconnect','marca'],['@kalecozinhasensorial','gastronomia']],
      datasets:[{label:'Seguidores',data:[19348,423,367],backgroundColor:[ink,warnc,soft],borderRadius:2}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},
      title:{display:true,text:'Seguidores por conta · a audiência está toda no perfil pessoal'}},
      scales:{y:{type:'logarithmic',grid},x:{grid:{display:false}}}}});

  new Chart(document.getElementById('chartDestaques'),{type:'doughnut',
    data:{labels:['Viagens · 644 stories','Negócio · 29 stories'],
      datasets:[{data:[644,29],backgroundColor:[soft,ink],borderColor:'#fff',borderWidth:3}]},
    options:{responsive:true,maintainAspectRatio:false,cutout:'64%',
      plugins:{legend:{position:'bottom'},title:{display:true,text:'A vitrine do perfil · 16 destaques, 673 stories fixados'}}}});

  new Chart(document.getElementById('chartFunil'),{type:'bar',
    data:{labels:[['Reproduções somadas','em 102 dias'],['Em posts com','qualquer chamada'],['Em posts que','citam o ingresso']],
      datasets:[{label:'Reproduções',data:[176634,16758,7998],backgroundColor:[ink,primary,warnc],borderRadius:2}]},
    options:{responsive:true,maintainAspectRatio:false,indexAxis:'y',plugins:{legend:{display:false},
      title:{display:true,text:'Quanto do alcance chega a pedir alguma coisa'}},
      scales:{x:{beginAtZero:true,grid},y:{grid:{display:false}}}}});

  new Chart(document.getElementById('chartConcorrentes'),{type:'bar',
    data:{labels:['@juharantes_','@bnidf','@bnidfpiloto','@empreendeclube','@moveeconnect','@confraempresariasbsb','@empresariosdebrasilia'],
      datasets:[{label:'Seguidores',data:[19348,3136,1976,740,423,210,141],
        backgroundColor:[ink,soft,soft,soft,warnc,rule,rule],borderRadius:2}]},
    options:{responsive:true,maintainAspectRatio:false,indexAxis:'y',plugins:{legend:{display:false},
      title:{display:true,text:'Networking empresarial no DF · seguidores em 04/09/2026'}},
      scales:{x:{beginAtZero:true,grid},y:{grid:{display:false}}}}});

  new Chart(document.getElementById('chartScore'),{type:'bar',
    data:{labels:['Instagram: alcance e conteúdo','Marca MOVE como ativo','Busca no Google','Instagram: conversão','Site e domínio próprio','Rastreamento e mensuração'],
      datasets:[{label:'Nota',data:[5.5,3.0,2.5,2.0,1.0,0.5],
        backgroundColor:[primary,ink,ink,warnc,warnc,warnc],borderRadius:2}]},
    options:{responsive:true,maintainAspectRatio:false,indexAxis:'y',plugins:{legend:{display:false},
      title:{display:true,text:'Nota por pilar · média ponderada de 2,9 em 10'}},
      scales:{x:{beginAtZero:true,max:10,grid},y:{grid:{display:false}}}}});

  document.addEventListener('click',e=>{
    const b=e.target.closest('[data-unlock]'); if(!b) return;
    const card=b.closest('.lock-card'); if(!card||card.querySelector('.lock-form')) return;
    b.remove();
    const f=document.createElement('form'); f.className='lock-form';
    const id='sen'+Math.random().toString(36).slice(2,7);
    f.innerHTML='<label class="lock-label" for="'+id+'">Senha de acesso</label>'+
      '<input class="lock-input" id="'+id+'" type="password" inputmode="numeric" autocomplete="off" required>'+
      '<button class="lock-go" type="submit">Liberar</button>'+
      '<p class="lock-err" hidden>Senha incorreta. Confira com a Oráculo.</p>';
    card.insertBefore(f,card.querySelector('.lock-alt'));
    f.querySelector('input').focus();
    f.addEventListener('submit',ev=>{
      ev.preventDefault();
      const inp=f.querySelector('input'), v=inp.value.replace(/\s+/g,'');
      if(window.__oraH(v)===window.__oraK){
        try{localStorage.setItem('oraculo-liberado','1');}catch(err){}
        const y=card.getBoundingClientRect().top+window.scrollY-140;
        window.__oraOpen();
        window.scrollTo({top:y,behavior:'smooth'});
      }else{
        f.querySelector('.lock-err').hidden=false; inp.value=''; inp.focus();
      }
    });
  });

  const links=[...document.querySelectorAll('.nav a')];
  const secs=links.map(a=>document.querySelector(a.getAttribute('href'))).filter(Boolean);
  const onScroll=()=>{let cur=secs[0];for(const s of secs){if(s.getBoundingClientRect().top<=120)cur=s;}
    links.forEach(a=>a.classList.toggle('active',a.getAttribute('href')==='#'+cur.id));};
  window.addEventListener('scroll',onScroll,{passive:true});onScroll();
})();
</script>
</body>
</html>
'''

# ---- travas da versão de prévia ----
PREVIEW_NOTE = ('<div class="callout preview-note"><strong>Sobre esta prévia</strong><p>O diagnóstico acima está '
  'inteiro: a nota, os seis pilares e o peso de cada um. O comparativo com os concorrentes de Brasília também está '
  'aberto. As demais seções trazem a apuração que sustenta essa nota e o plano de correção, e abrem com a senha de '
  'acesso, entregue no início do trabalho com a Oráculo. '
  '<b>Nada aqui foi resumido para caber na prévia: o material existe completo e já está escrito.</b></p></div>')

_i = S2.index('<div class="diag">'); _j = S2.index('<div class="insight ')
S2 = (S2[:_i] + '<div class="locked"><div class="locked-content">' + S2[_i:_j] + '</div>'
      + veil('As três colunas do diagnóstico executivo',
             'Situação, impacto e a resposta indicada para cada um dos cinco pontos que derrubam a nota.')
      + '</div>' + S2[_j:])
S2 = S2.replace('</section>', PREVIEW_NOTE + '</section>')

S3 = lockup(S3, 'Oito quinzenas de alcance, medidas uma a uma',
  'A curva completa de reproduções por Reel, o mix dos três formatos, a comparação entre conteúdo pessoal e comercial e o efeito de esconder as curtidas.')
S4 = lockup(S4, 'O inventário dos ativos de marca',
  'As três contas lado a lado, as 16 pastas de destaque com a contagem de stories de cada uma e o achado mais caro desta auditoria.')
S5 = lockup(S5, 'As cinco primeiras posições da busca pelo nome',
  'Quem ocupa cada posição e o que é seu, o mapa dos sete canais fora do Instagram e a situação do domínio da marca no registro.br.')
S6 = lockup(S6, 'As seis etapas entre o Reel e o pagamento',
  'O que se perde em cada etapa, o que o código da página de venda revela sobre a medição e onde a prova social da 1ª edição deixou de ser publicada.')
S8 = lockup(S8, 'A SWOT escrita a partir dos dados desta coleta',
  '5 forças, 6 fraquezas, 5 oportunidades e 5 ameaças, cada uma amarrada a um número apurado, sem afirmação genérica.')
S9 = lockup(S9, '19 ações em três ciclos, com meta por ciclo',
  'As sete primeiras cabem antes de 19 de setembro. Fecha com a sequência de cinco prioridades, na ordem que protege o investimento.')
S10 = lockup(S10, 'Onde está o retorno mais rápido',
  'A pontuação por pilar em gráfico, o que já está pronto, o que falta ligar e a pergunta que decide qualquer investimento em mídia.')

html = HEAD + COVER + S1 + S2 + S3 + S4 + S5 + S6 + S7 + S8 + S9 + S10 + CLOSING + SCRIPT

os.makedirs('JulianaArantes', exist_ok=True)
open(OUT, 'w', encoding='utf-8').write(html)

# ---------------- validação ----------------
errs = []
for w in ['Adriano','adriano','Doctoralia','facelift','Pedro','Sinfonya','Joana','Diego','Debem','dradrianoborges','Suziellen','Natália Rinco']:
    if w in html: errs.append(f'resquício do cliente-template: {w}')
bad = re.findall(r'<[^>]*[“”][^>]*>', html)
if bad: errs.append(f'aspas curvas dentro de tag: {bad[:3]}')
vis = re.sub(r'<script.*?</script>|<style.*?</style>', '', html, flags=re.S)
vis = re.sub(r'<[^>]+>', ' ', vis)
for ch, nm in [('—','travessão em'),('–','meia-risca en')]:
    n = vis.count(ch)
    if n: errs.append(f'{nm}-dash no texto visível: {n}')
if html.count('<section') != html.count('</section>'): errs.append('section desbalanceada')
if html.count('<div') != html.count('</div>'): errs.append(f"div desbalanceada: {html.count('<div')} x {html.count('</div>')}")
ins = len(re.findall(r'<div class="insight ', html))
if ins != 10: errs.append(f'blocos insight: {ins} (esperado 10)')
for cid in ['chartAlcance','chartFormatos','chartMarca','chartDestaques','chartFunil','chartConcorrentes','chartScore']:
    if f'id="{cid}"' not in html: errs.append(f'canvas ausente: {cid}')
    if f"getElementById('{cid}')" not in html: errs.append(f'chart não instanciado: {cid}')
for a in re.findall(r'href="#([a-z]+)"', html):
    if f'id="{a}"' not in html: errs.append(f'âncora sem destino: #{a}')
if 'meta name="description"' not in html: errs.append('falta meta description')

if html.count('<div class="locked">') != 8: errs.append(f"blocos travados: {html.count(chr(60)+'div class=' + chr(34) + 'locked' + chr(34) + chr(62))} (esperado 8)")
if html.count('class="locked-veil"') != 8: errs.append('veil sem par')
if html.count('<div class="locked-content">') != html.count('<div class="locked">'): errs.append('locked-content sem par')
if 'is-full' not in html: errs.append('falta o destrave por URL')
for sid in ['instagram','marca','busca','venda','swot','recomendacoes','resumo']:
    seg = html[html.index(f'id="{sid}"'):]
    seg = seg[:seg.index('</section>')]
    if '<div class="locked">' not in seg: errs.append(f'seção não travada: {sid}')
for sid in ['essencial','comparativo']:
    seg = html[html.index(f'id="{sid}"'):]
    seg = seg[:seg.index('</section>')]
    if '<div class="locked">' in seg: errs.append(f'seção travada por engano: {sid}')
if '103669' in html: errs.append('senha em texto puro no HTML')
if 'data-unlock' not in html: errs.append('botao de senha ausente')
print('BYTES', len(html))
print('ERROS:', errs if errs else 'nenhum')
