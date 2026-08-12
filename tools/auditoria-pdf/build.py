# -*- coding: utf-8 -*-
"""Gera a Auditoria de Presenca Digital do Grupo Sinfonya em HTML A4 pronto para PDF."""
import base64, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_css import CSS

RAIZ = '/Users/touchbar/Codigos-Projetos/oraculo/analises-oraculo'
TMP = os.path.dirname(os.path.abspath(__file__))

FIRA = open(os.path.join(TMP, 'fira-embed.css')).read()
LOGO = base64.b64encode(open(os.path.join(RAIZ, 'logo.png'), 'rb').read()).decode()

DATA = '6 de agosto de 2026'
paginas = []
_n = [0]


def pag(secao, corpo, fecho=None):
    """Pagina de conteudo com cabecalho, rodape e fecho opcional."""
    _n[0] += 1
    f = f'<div class="fecho">{fecho}</div>' if fecho else ''
    paginas.append(
        f'<section class="pagina">'
        f'<div class="cab"><span class="cab-esq">Grupo Sinfonya &middot; Or&aacute;culo Tecnologia</span>'
        f'<span class="cab-dir">{secao}</span></div>'
        f'{corpo}{f}'
        f'<div class="rod"><span>Auditoria de presen&ccedil;a digital</span><span>{_n[0]}</span></div>'
        f'</section>'
    )


def tabela(cols, linhas, fonte=None, compacta=False, alinha=None):
    alinha = alinha or {}
    cls = 't compacta' if compacta else 't'
    th = ''.join(
        f'<th class="num">{c}</th>' if alinha.get(i) == 'num' else f'<th>{c}</th>'
        for i, c in enumerate(cols))
    tr = ''
    for l in linhas:
        if isinstance(l, tuple) and l and l[0] == '__grupo__':
            tr += f'<tr class="grupo"><td colspan="{len(cols)}">{l[1]}</td></tr>'
            continue
        tds = ''
        for i, c in enumerate(l):
            k = []
            if i == 0:
                k.append('forte')
            if alinha.get(i) == 'num':
                k.append('num')
            cl = f' class="{" ".join(k)}"' if k else ''
            tds += f'<td{cl}>{c}</td>'
        tr += f'<tr>{tds}</tr>'
    f = f'<p class="fonte">{fonte}</p>' if fonte else ''
    return f'<table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>{f}'


def defs(itens):
    d = ''.join(f'<div class="def"><div class="def-r">{r}</div><div class="def-d">{t}</div></div>'
                for r, t in itens)
    return f'<div class="defs">{d}</div>'


def grafico(itens, fonte=None, maxv=None):
    """itens: (rotulo, sub, valor, exibicao, destaque)"""
    mx = maxv or max(i[2] for i in itens) or 1
    cols = ''
    for rot, sub, val, exib, on in itens:
        h = max(1.2, val / mx * 36)
        cols += (f'<div class="gr-col"><div class="gr-val">{exib}</div>'
                 f'<div class="gr-bar{" on" if on else ""}" style="height:{h:.1f}mm"></div></div>')
    eixo = ''.join(f'<div><div class="gr-rot">{r}</div><div class="gr-sub">{s}</div></div>'
                   for r, s, _, _, _ in itens)
    f = f'<p class="fonte">{fonte}</p>' if fonte else ''
    return f'<div class="gr"><div class="gr-area">{cols}</div><div class="gr-eixo">{eixo}</div></div>{f}'


def kpis(itens):
    k = ''.join(f'<div class="kpi"><b class="{"az" if az else ""}">{v}</b><span>{t}</span></div>'
                for v, t, az in itens)
    return f'<div class="kpis">{k}</div>'


def nota(titulo, *ps):
    p = ''.join(f'<p>{x}</p>' for x in ps)
    return f'<div class="nota"><b>{titulo}</b>{p}</div>'


# ============================================================ CAPA
paginas.append(f'''<section class="pagina capa">
<div class="capa-topo">
  <img src="data:image/png;base64,{LOGO}" alt="Or&aacute;culo">
  <div class="capa-meta">Documento confidencial<br>{DATA}</div>
</div>
<div class="capa-corpo">
  <div class="capa-kicker">Grupo Sinfonya Turismo e Formaturas</div>
  <h1>Auditoria de presen&ccedil;a digital: o que encontram quando procuram a Sinfonya</h1>
  <p class="capa-lede">Levantamento de tudo que existe sobre a empresa na internet: as cinco contas de
  Instagram, o site, o Perfil da Empresa no Google, o Reclame Aqui, o agregador de links e os cadastros
  de terceiros. Mais o diagn&oacute;stico de duas frentes que hoje n&atilde;o existem, CRM e atendimento
  automatizado no WhatsApp. Cada n&uacute;mero deste documento traz a fonte de onde saiu.</p>
</div>
<div class="capa-rodape">
  <div class="capa-stat"><b>7</b><span>n&uacute;meros de WhatsApp publicados pela empresa</span></div>
  <div class="capa-stat"><b>3</b><span>sites declarados, nenhum registrado</span></div>
  <div class="capa-stat"><b>0 de 5</b><span>buscas comerciais em que a marca aparece</span></div>
  <div class="capa-stat"><b>5</b><span>reclama&ccedil;&otilde;es aguardando resposta</span></div>
</div>
</section>''')

# ============================================================ 2. METODO
pag('M&eacute;todo', f'''
<h2 class="titulo">O que foi levantado, e de onde veio cada dado</h2>
<p class="lede">Nada neste documento foi fornecido pela Sinfonya. Fizemos o caminho que um cliente faria:
procuramos a empresa na internet, abrimos cada canal e testamos se cada bot&atilde;o funciona. Tudo em 6 de
agosto de 2026. Quando a conclus&atilde;o &eacute; uma leitura nossa e n&atilde;o um dado, o texto avisa.</p>
{tabela(['O que olhamos', 'Como foi feito', 'Onde'], [
  ('O site', 'Testamos seis endere&ccedil;os de site com o nome da marca, para ver se algum est&aacute; no ar e se est&atilde;o comprados no nome da empresa', 'Registro.br, o &oacute;rg&atilde;o que controla os endere&ccedil;os .com.br'),
  ('As cinco contas', 'Lemos os campos de cada perfil: link, e-mail, telefone, endere&ccedil;o, cidade e tipo de conta', 'Instagram, leitura direta'),
  ('Os contatos publicados', 'Lemos 428 legendas e bios procurando todo telefone, e-mail e site que a empresa j&aacute; divulgou', 'Instagram, coletas de 4 e 6 de agosto'),
  ('O atendimento', 'Lemos os coment&aacute;rios das publica&ccedil;&otilde;es mais comentadas de tr&ecirc;s contas e medimos quanto tempo a empresa levou para responder cada um', 'Instagram, leitura direta'),
  ('O Google', 'Pesquisamos o nome da marca, a pergunta que o cliente faz antes de comprar e cinco buscas de quem procura viagem', 'google.com.br, em portugu&ecirc;s e no Brasil'),
  ('A reputa&ccedil;&atilde;o', 'Conferimos quantas reclama&ccedil;&otilde;es existem, quantas foram respondidas, em quanto tempo e sobre o qu&ecirc;', 'Reclame Aqui'),
  ('O Linktree', 'Clicamos em cada um dos cinco bot&otilde;es para ver se abrem', 'linktr.ee/gruposinfonyaturismo'),
  ('Os custos', 'Consultamos como o WhatsApp cobra hoje e o pre&ccedil;o de tabela dos CRM mais usados no Brasil', 'Meta e sites dos fornecedores'),
])}
<h3 class="sub">O que n&atilde;o deu para apurar</h3>
<p class="texto">N&atilde;o tivemos acesso ao WhatsApp da empresa nem ao hist&oacute;rico de vendas. Por isso
n&atilde;o sabemos quantas mensagens chegam por m&ecirc;s, em quanto tempo s&atilde;o respondidas ali dentro,
quantas viram venda nem por onde o cliente chegou. O cap&iacute;tulo sobre atendimento e cadastro de clientes
foi montado com o que d&aacute; para ver de fora: os telefones publicados, os coment&aacute;rios respondidos e
as reclama&ccedil;&otilde;es em aberto.</p>
''', 'Este documento olha para a empresa <span class="azul">do lado de fora, como um cliente que ainda n&atilde;o comprou.</span>')

# ============================================================ 3. O MAPA
pag('O mapa', f'''
<h2 class="titulo">Onde a Sinfonya existe hoje, e quem controla cada ponto</h2>
<p class="lede">Checamos onze pontos. A Sinfonya edita quatro, um n&atilde;o existe, e os outros seis s&atilde;o
escritos e mantidos por terceiros. S&atilde;o justamente esses seis que respondem quando algu&eacute;m checa
se a empresa &eacute; confi&aacute;vel.</p>
{tabela(['Ponto', 'Situa&ccedil;&atilde;o', 'Quem edita', 'O que o cliente encontra'], [
  ('Instagram, 5 contas', 'Ativo, duas com pauta', 'A empresa', '95.142 seguidores somados, duas contas paradas'),
  ('Linktree', 'Ativo', 'A empresa', 'Cinco links, dois quebrados, duas marcas ausentes'),
  ('Site pr&oacute;prio', 'N&atilde;o existe', 'ningu&eacute;m', 'Nada. O endere&ccedil;o anunciado n&atilde;o foi comprado'),
  ('Perfil da Empresa no Google', 'Existe, sem dono', 'O Google', 'Nota 4,6, 55 avalia&ccedil;&otilde;es e um bot&atilde;o Site que n&atilde;o abre'),
  ('Reclame Aqui', 'Existe, n&atilde;o verificado', 'Os clientes', '16 reclama&ccedil;&otilde;es ativas, 5 sem resposta'),
  ('JusBrasil', 'Aparece na busca', 'Terceiro', 'P&aacute;gina de processos no nome da empresa'),
  ('Econodata e Solutudo', 'Aparece na busca', 'Terceiro', 'Cadastro p&uacute;blico, um dos CNPJ consta inapto'),
  ('Facebook, 2 p&aacute;ginas', 'Abandonado', 'A empresa', 'Duas p&aacute;ginas distintas, sem pauta'),
  ('Pinterest', 'Existe', 'A empresa', 'Perfil de @sinfonyaformaturas'),
  ('agenciasdeviagens.org', 'Aparece na busca', 'Terceiro', 'Ficha da filial de Patos de Minas'),
  ('cnpj.biz', 'Aparece na busca', 'Terceiro', 'Ficha da filial 14.275.276/0002-78'),
])}
<p class="texto">Na primeira p&aacute;gina do Google para <b>Sinfonya Turismo</b>, oito resultados. Dois s&atilde;o
o Instagram da empresa. Os outros seis foram escritos por outra pessoa: dois pelo Reclame Aqui, um pelo
JusBrasil, um pela Econodata, um pelo Solutudo e um pelo Facebook abandonado.</p>
''', 'A empresa controla o que publica, <span class="azul">mas n&atilde;o controla o que responde por ela.</span>')

# ============================================================ 5. TRES IDENTIDADES
pag('Posicionamento', f'''
<h2 class="titulo">A empresa se apresenta de tr&ecirc;s jeitos diferentes</h2>
<p class="lede">Cada canal declara um site, um telefone e um endere&ccedil;o. Nenhum dos tr&ecirc;s conjuntos
bate com o outro, e os dois sites declarados como oficiais n&atilde;o existem.</p>
{tabela(['Canal', 'Site declarado', 'Telefone', 'Situa&ccedil;&atilde;o'], [
  ('Perfil no Google', 'sinfonyaturismo.com.br', '(61) 3336-5827', 'Ningu&eacute;m assumiu'),
  ('Reclame Aqui', 'sinfonya.com.br', '(61) 3575-0044', 'N&atilde;o verificado, no RA h&aacute; 10 anos'),
  ('Linktree', 'sinfonyaturismo.com.br', 'WhatsApp (61) 98405-5939', 'Ativo, dois links quebrados'),
  ('Instagram principal', 'nenhum', 'WhatsApp (61) 98405-5939', 'Conta de neg&oacute;cio sem endere&ccedil;o'),
], 'Leitura direta de cada canal em 06/08/2026. Os dois endere&ccedil;os de site declarados foram testados um a um.')}
{defs([
  ('Dois sites oficiais, nenhum no ar',
   'O Google e o Linktree apontam para sinfonyaturismo.com.br. O Reclame Aqui aponta para sinfonya.com.br. '
   'Consultamos os dois no Registro.br: <b>nenhum dos dois foi comprado</b>.'),
  ('Dois telefones que a empresa quase n&atilde;o usa',
   'O n&uacute;mero do Google, (61) 3336-5827, aparece 2 vezes em 428 legendas. O do Reclame Aqui, (61) 3575-0044, '
   'n&atilde;o aparece nenhuma. Os dois canais externos publicam fixos que o time n&atilde;o divulga.'),
  ('Endere&ccedil;os que divergem por uma sala',
   'O Google registra Sala 302 do Edif&iacute;cio Spazio Duo. As legendas do Instagram dizem Sala 303 do Edif&iacute;cio Spazzio Duo. '
   'O nome do pr&eacute;dio tamb&eacute;m muda de grafia entre os dois.'),
])}
''', 'Quem pesquisa a empresa antes de pagar encontra tr&ecirc;s vers&otilde;es dela, <span class="azul">e duas apontam para um site que n&atilde;o abre.</span>')

# ============================================================ 6. DOMINIO
pag('O endere&ccedil;o', f'''
<h2 class="titulo">O endere&ccedil;o que a empresa anuncia est&aacute; livre para qualquer um comprar</h2>
<p class="lede">Testamos seis endere&ccedil;os de site com o nome da marca. Nenhum abre. E os quatro principais
nunca foram comprados: est&atilde;o parados na prateleira, dispon&iacute;veis para qualquer pessoa levar.</p>
{tabela(['Endere&ccedil;o de site', 'Abre?', 'Tem e-mail?', 'Est&aacute; comprado?'], [
  ('sinfonyaturismo.com.br', 'N&atilde;o', 'N&atilde;o', 'N&atilde;o, est&aacute; livre'),
  ('sinfonya.com.br', 'N&atilde;o', 'N&atilde;o', 'N&atilde;o, est&aacute; livre'),
  ('gruposinfonya.com.br', 'N&atilde;o', 'N&atilde;o', 'N&atilde;o, est&aacute; livre'),
  ('sinfonyaformaturas.com.br', 'N&atilde;o', 'N&atilde;o', 'N&atilde;o, est&aacute; livre'),
  ('sinfonyaweeding.com.br', 'N&atilde;o', 'N&atilde;o', 'N&atilde;o'),
  ('sinfonyaturismo.com', 'N&atilde;o', 'N&atilde;o', 'N&atilde;o'),
], 'Consulta ao Registro.br, o &oacute;rg&atilde;o que controla os endere&ccedil;os .com.br no Brasil, em 06/08/2026.', compacta=True)}
{nota('O risco n&atilde;o &eacute; hipot&eacute;tico',
 'A ficha da Sinfonya no Google tem um bot&atilde;o escrito <b>Site</b>, e ele aponta para sinfonyaturismo.com.br. '
 'Quem clica hoje n&atilde;o chega a lugar nenhum. Se um concorrente comprar esse endere&ccedil;o, ele passa a receber '
 'todo mundo que clicar nesse bot&atilde;o, e tamb&eacute;m todo mundo que clicar em "Site Grupo Sinfonya Turismo" no Linktree da empresa.',
 'Comprar os quatro endere&ccedil;os custa uma anuidade barata e leva minutos. &Eacute; a a&ccedil;&atilde;o mais simples e a que evita o maior risco de todo este documento.')}
<h3 class="sub">Sem site, tamb&eacute;m n&atilde;o h&aacute; e-mail da empresa</h3>
<p class="texto">O e-mail p&uacute;blico da conta
principal &eacute; <b>reservas3.sinfonya@gmail.com</b>. O n&uacute;mero 3 no nome sugere que existem ao menos
outras duas caixas na mesma l&oacute;gica. Uma ag&ecirc;ncia que vende pacote internacional parcelado envia
contrato e voucher de um endere&ccedil;o gratuito que qualquer pessoa poderia ter criado.</p>
''', 'A empresa tem quinze anos de opera&ccedil;&atilde;o e <span class="azul">nenhum endere&ccedil;o pr&oacute;prio na internet.</span>')

# ============================================================ 7. INSTAGRAM
pag('Instagram', f'''
<h2 class="titulo">Cinco contas e nenhuma delas diz onde a empresa fica</h2>
<p class="lede">O Instagram &eacute; o &uacute;nico canal vivo do grupo. Lendo os campos de perfil de cada uma
das cinco contas, nenhuma est&aacute; configurada como uma empresa que quer ser encontrada.</p>
{tabela(['Conta', 'Seguidores', 'Tipo', 'Link na bio', 'E-mail', 'Cidade'], [
  ('@sinfonyaturismo', '50.386', 'Empresa', 'WhatsApp', 'gmail', 'vazio'),
  ('@sinfonyaformaturas', '25.823', 'Criador', 'Linktree', 'nenhum', 'vazio'),
  ('@sinfonyaweeding', '16.438', 'Empresa', 'Google Forms', 'nenhum', 'vazio'),
  ('@sinfonya_cristao', '1.943', 'Empresa', 'nenhum', 'nenhum', 'vazio'),
  ('@sinfonyaturismo_patosdeminas', '552', 'Empresa', 'WhatsApp', 'nenhum', 'vazio'),
], 'Campos lidos direto do perfil de cada conta em 06/08/2026. "Vazio" significa que o campo existe no perfil e est&aacute; em branco.')}
{defs([
  ('A conta de maior ticket n&atilde;o tem por onde falar',
   '@sinfonya_cristao vende Israel em 2027, o produto mais caro do grupo, e o perfil <b>n&atilde;o tem link, '
   'nem e-mail, nem telefone, nem bot&atilde;o de contato</b>. A bio lista as outras quatro contas e nada mais.'),
  ('A conta de casamentos manda para um formul&aacute;rio do Google',
   'O &uacute;nico caminho de convers&atilde;o de @sinfonyaweeding, com 16.438 seguidores, &eacute; um link do '
   'docs.google.com. Destination wedding e lua de mel s&atilde;o decis&otilde;es longas e caras, atendidas por um formul&aacute;rio gratuito.'),
  ('A conta de formaturas n&atilde;o &eacute; conta de empresa',
   'Com 25.823 seguidores e um produto vendido para comiss&atilde;o de formatura, @sinfonyaformaturas est&aacute; '
   'classificada como perfil de criador de conte&uacute;do. Perde os campos de neg&oacute;cio e a ficha comercial.'),
  ('Nenhuma das cinco preenche cidade',
   'Quatro contas s&atilde;o de neg&oacute;cio e nenhuma tem endere&ccedil;o ou cidade cadastrados. Isso tira as cinco '
   'do mapa e da busca por proximidade dentro do pr&oacute;prio Instagram, numa empresa que vende sa&iacute;da de &ocirc;nibus de Taguatinga.'),
])}
''', 'S&atilde;o 95 mil seguidores distribu&iacute;dos em cinco perfis <span class="azul">que n&atilde;o dizem onde a empresa fica.</span>')

# ============================================================ 8. CONTATO
pag('Contato', f'''
<h2 class="titulo">Sete n&uacute;meros de WhatsApp, nenhum site, nenhum e-mail</h2>
<p class="lede">Lemos as 428 legendas e bios das cinco contas procurando todo telefone, e-mail e site que a empresa j&aacute; publicou. O resultado mostra exatamente como a empresa recebe cliente hoje.</p>
<p class="texto">Das 428, <b>163 publicam ao menos um telefone</b>, e ao todo circulam
<b>sete n&uacute;meros diferentes</b>. Nenhuma delas traz link para site pr&oacute;prio e nenhuma traz e-mail.</p>
{tabela(['N&uacute;mero', 'Ocorr&ecirc;ncias', 'Onde aparece'], [
  ('(61) 98405-5939', '309', 'Turismo, Formaturas, Crist&atilde;o e Patos de Minas'),
  ('(34) 99201-6523', '138', 'Turismo, Formaturas, Crist&atilde;o e Patos de Minas'),
  ('(34) 99198-9798', '20', 'Turismo'),
  ('(61) 3336-5827', '2', 'Formaturas, e &eacute; o telefone do Perfil do Google'),
  ('(61) 98345-4530', '2', 'Formaturas, dado em resposta a coment&aacute;rio'),
  ('(34) 99293-1838', '2', 'Formaturas'),
  ('(34) 99963-7172', '1', 'Patos de Minas'),
], 'Leitura das 428 legendas e bios coletadas em 04 e 06/08/2026. Um oitavo n&uacute;mero, (61) 3575-0044, aparece s&oacute; no cadastro do Reclame Aqui.', compacta=True, alinha={1: 'num'})}
<p class="texto">Os dois primeiros n&uacute;meros concentram 447 das 474 cita&ccedil;&otilde;es e funcionam como
canal oficial. Os outros cinco aparecem soltos, alguns dentro de resposta a coment&aacute;rio. Para o cliente,
todos parecem igualmente v&aacute;lidos.</p>
<p class="texto">O ponto n&atilde;o &eacute; a quantidade de n&uacute;meros: uma empresa com duas pra&ccedil;as
precisa mesmo de mais de um. O ponto &eacute; que <b>cada n&uacute;mero &eacute; um aparelho com hist&oacute;rico
pr&oacute;prio</b>. Quem falou com o (34) 99198-9798 em mar&ccedil;o e volta pelo (61) 98405-5939 em agosto
come&ccedil;a a conversa do zero, com outra pessoa, sem registro do que j&aacute; comprou.</p>
''', 'Em 428 legendas a empresa publicou sete telefones <span class="azul">e nenhum endere&ccedil;o na internet que ela mesma controle.</span>')

# ============================================================ 9. LINKTREE
pag('Linktree', f'''
<h2 class="titulo">O &uacute;nico agregador do grupo tem dois links quebrados</h2>
<p class="lede">O Linktree &eacute; o que a conta de formaturas usa como bio e o que o grupo trata como porta
de entrada. Testamos os cinco links, um a um.</p>
{tabela(['Bot&atilde;o', 'Destino', 'Funciona'], [
  ('Nosso Whatsapp', 'wa.me/5561984055939', 'Sim'),
  ('Insta Sinfonya FORMATURAS', 'instagram.com/sinfonyaformaturas', 'Sim'),
  ('Insta Sinfonya Turismo', 'instagram.com/sinfonyaturismo', 'Sim'),
  ('Insta Sinfonya Crist&atilde;o', 'instagram.com/sinfonyacristao', '<b>N&atilde;o</b>'),
  ('Site Grupo Sinfonya Turismo', 'sinfonyaturismo.com.br', '<b>N&atilde;o</b>'),
], 'Cada destino foi aberto em 06/08/2026.')}
{defs([
  ('Falta um caractere no link da conta crist&atilde;',
   'O bot&atilde;o aponta para <b>instagram.com/sinfonyacristao</b>. O perfil real &eacute; '
   '<b>@sinfonya_cristao</b>, com underline. A URL do Linktree abre a p&aacute;gina de erro do Instagram. '
   'A conta que vende Israel 2027 perde, por um caractere, o &uacute;nico link que apontava para ela.'),
  ('O bot&atilde;o de site leva a um dom&iacute;nio inexistente',
   'O bot&atilde;o mais leg&iacute;timo da p&aacute;gina, o que promete o site oficial do grupo, aponta para um '
   'endere&ccedil;o que nunca foi registrado.'),
  ('Duas das cinco marcas ficaram de fora',
   'O Linktree lista tr&ecirc;s contas. N&atilde;o lista @sinfonyaweeding, que tem 16.438 seguidores, nem '
   '@sinfonyaturismo_patosdeminas, que &eacute; a filial de Minas e a conta que publica pre&ccedil;o.'),
])}
''', 'Dos cinco links, dois n&atilde;o abrem <span class="azul">e as duas marcas ausentes s&atilde;o justamente a de maior ticket e a que publica pre&ccedil;o.</span>')

# ============================================================ 10. GOOGLE MARCA
pag('Google', f'''
<h2 class="titulo">Existe um Perfil da Empresa no Google, e ele n&atilde;o &eacute; da empresa</h2>
<p class="lede">Procurando pelo nome da marca, o Google exibe uma ficha completa da Sinfonya: fotos, endere&ccedil;o,
telefone, hor&aacute;rio, descri&ccedil;&atilde;o e avalia&ccedil;&otilde;es. Junto dela, o pr&oacute;prio Google exibe o link <b>&Eacute; propriet&aacute;rio desta empresa?</b>. Esse link s&oacute; aparece quando ningu&eacute;m assumiu a ficha.</p>
{tabela(['A ficha que o Google exibe', 'O que est&aacute; l&aacute;'], [
  ('Nota', '4,6'),
  ('Avalia&ccedil;&otilde;es', '55'),
  ('Quem &eacute; o dono da ficha', 'Ningu&eacute;m. O Google convida qualquer um a assumir'),
  ('Bot&atilde;o Site', 'Aponta para sinfonyaturismo.com.br, que n&atilde;o abre'),
  ('Telefone', '(61) 3336-5827, o fixo, e n&atilde;o o WhatsApp do atendimento'),
  ('Endere&ccedil;o', 'Sala 302 do Edif&iacute;cio Spazio Duo, Taguatinga Sul'),
], compacta=True)}
{defs([
  ('Um ativo de reputa&ccedil;&atilde;o parado',
   '55 pessoas avaliaram a Sinfonya com m&eacute;dia 4,6. Os coment&aacute;rios em destaque falam de atendimento: '
   '"Atendimento muito bom, e v&aacute;rios pacotes de viagem com pre&ccedil;os acess&iacute;veis", "A equipe da Sinfonya Turismo &eacute; '
   'super atenciosa e profissional". A empresa <b>n&atilde;o pode responder a nenhuma delas</b> porque nunca assumiu a ficha.'),
  ('Uma credencial que o Instagram nunca usa',
   'A descri&ccedil;&atilde;o exibida no painel diz: "Com mais de 500 mil passageiros transportados, a Sinfonya Turismo &eacute; uma '
   'das empresas que mais cresce no Brasil no ramo de Viagens". Esse n&uacute;mero n&atilde;o aparece em nenhuma das 428 legendas auditadas.'),
  ('Quem chega pelo Google cai no vazio',
   'O caminho mais &oacute;bvio da ficha, o bot&atilde;o Site, n&atilde;o leva a lugar nenhum. E o telefone exibido &eacute; o fixo, '
   'n&atilde;o o WhatsApp que a empresa divulga 309 vezes nas legendas.'),
])}
''', 'A Sinfonya tem nota 4,6 com 55 avalia&ccedil;&otilde;es no Google <span class="azul">e n&atilde;o &eacute; dona da p&aacute;gina onde elas est&atilde;o.</span>')

# ============================================================ 11. SERP DE MARCA
pag('Google', f'''
<h2 class="titulo">Quem pesquisa se a empresa &eacute; confi&aacute;vel encontra reclama&ccedil;&atilde;o</h2>
<p class="lede">Rodamos duas consultas do tipo que um cliente faz antes de pagar: o nome da marca e a pergunta
de checagem. Os resultados abaixo s&atilde;o a primeira p&aacute;gina de cada uma.</p>
<h3 class="sub">Consulta: Sinfonya Turismo</h3>
{tabela(['#', 'Resultado', 'Dom&iacute;nio', 'Quem escreveu'], [
  ('1', 'Grupo Sinfonya Turismo, perfil', 'instagram.com', 'A empresa'),
  ('2', 'Sinfonya Turismo e Eventos', 'reclameaqui.com.br', 'Clientes'),
  ('3', 'Grupo Sinfonya Turismo, reels', 'instagram.com', 'A empresa'),
  ('4', 'Sinfonya Turismo e Eventos, Processos', 'jusbrasil.com.br', 'Terceiro'),
  ('5', 'Sinfonya Turismo e Eventos em Bras&iacute;lia', 'econodata.com.br', 'Terceiro'),
  ('6', 'Lista de reclama&ccedil;&otilde;es', 'reclameaqui.com.br', 'Clientes'),
  ('7', 'Sinfonya Turismo', 'facebook.com', 'P&aacute;gina abandonada'),
  ('8', 'Sinfonya Turismo E Eventos', 'solutudo.com.br', 'Terceiro'),
], compacta=True)}
<h3 class="sub">Consulta: Sinfonya Turismo &eacute; confi&aacute;vel</h3>
<p class="texto">As posi&ccedil;&otilde;es <b>1, 2 e 4 s&atilde;o do Reclame Aqui</b>. A posi&ccedil;&atilde;o 3
&eacute; o Instagram. Buscando por <b>Sinfonya Formaturas</b>, o Reclame Aqui aparece em terceiro e, em sexto,
uma reclama&ccedil;&atilde;o com o t&iacute;tulo "Empresa de viagem de formatura n&atilde;o realiza estorno".</p>
<p class="texto">Uma comiss&atilde;o de formatura decidindo entre fornecedores faz exatamente essa pesquisa. O que
ela encontra n&atilde;o &eacute; um site com o portf&oacute;lio, os quinze anos de opera&ccedil;&atilde;o e os
500 mil passageiros. &Eacute; uma lista de reclama&ccedil;&otilde;es de reembolso, sem resposta da empresa.</p>
''', 'A empresa n&atilde;o tem nenhuma p&aacute;gina pr&oacute;pria disputando <span class="azul">a pergunta que decide a compra.</span>')

# ============================================================ 12. BUSCAS COMERCIAIS
pag('Google', f'''
<h2 class="titulo">Em cinco buscas que vendem, a Sinfonya n&atilde;o aparece nenhuma vez</h2>
<p class="lede">Testamos as consultas que correspondem ao que a empresa efetivamente vende, todas na
regi&atilde;o e no idioma certos. A marca n&atilde;o foi citada em nenhuma delas, nem nos resultados nem no
restante da p&aacute;gina.</p>
{tabela(['Consulta', 'Sinfonya', 'Quem ocupa o topo'], [
  ('excurs&atilde;o Caldas Novas saindo de Bras&iacute;lia', 'ausente', 'brasiliatour.com.br, dfviagens.com.br, expressomanini.com.br, privecaldasnovas.com.br'),
  ('viagem de formatura Bras&iacute;lia DF ag&ecirc;ncia', 'ausente', 'ourobrasil.tur.br, supremaviagens.com.br, formaturismo.com.br, boraturismo.com'),
  ('ag&ecirc;ncia de viagem Taguatinga', 'ausente', 'dfviagens.com.br, 3sviagens.com.br, comandoturismo no Instagram'),
  ('pacote Porto Seguro saindo de Bras&iacute;lia', 'ausente', 'cvc.com.br, decolar.com, kayak.com.br, latamairlines.com'),
  ('viagem para Israel 2027 ag&ecirc;ncia brasileira', 'ausente', 'israelcomaline.com.br, terrasantaviagens.com.br, ustravel.com.br, vpiturismo.com.br'),
], 'google.com.br, idioma pt-BR e regi&atilde;o BR, 06/08/2026. "Ausente" significa que a palavra Sinfonya n&atilde;o aparece em nenhum lugar da primeira p&aacute;gina.')}
{defs([
  ('O padr&atilde;o &eacute; o mesmo nas cinco',
   'Quase todo concorrente que ocupa o topo dessas buscas tem <b>site pr&oacute;prio com p&aacute;gina dedicada ao destino</b>. '
   'Nas duas buscas locais, os &uacute;nicos perfis de Instagram que rankeiam s&atilde;o de contas que t&ecirc;m o nome do destino no pr&oacute;prio arroba.'),
  ('A Sinfonya perde para concorrentes menores',
   'Com 50.386 seguidores, a conta principal tem a maior base entre as ag&ecirc;ncias que disputam a mesma rota local. '
   'Na busca, ela perde para ag&ecirc;ncias com menos audi&ecirc;ncia e um site simples.'),
  ('Israel &eacute; a perda mais cara',
   'Peregrina&ccedil;&atilde;o &eacute; um produto que as pessoas pesquisam com anteced&ecirc;ncia e comparam por escrito. '
   'Seis concorrentes ocupam a primeira p&aacute;gina com p&aacute;gina de caravana. A Sinfonya vende Israel 2027 numa conta de 1.943 seguidores sem link.'),
])}
''', 'Quem ocupa essas buscas tem site. <span class="azul">&Eacute; o &uacute;nico ativo que a Sinfonya n&atilde;o tem.</span>')

# ============================================================ 13. RECLAME AQUI
pag('Reputa&ccedil;&atilde;o', f'''
<h2 class="titulo">Seis reclama&ccedil;&otilde;es, cinco sem resposta, vinte dias de espera</h2>
<p class="lede">O perfil da Sinfonya no Reclame Aqui existe h&aacute; dez anos, nunca foi verificado e &eacute; o
segundo resultado do Google para o nome da marca. Os indicadores abaixo s&atilde;o do pr&oacute;prio site, na
janela de 1 de fevereiro a 31 de julho de 2026.</p>
{tabela(['Indicador', 'Sinfonya'], [
  ('Reclama&ccedil;&otilde;es ativas no total', '16'),
  ('Recebidas nos &uacute;ltimos seis meses', '6'),
  ('Quantas foram respondidas', '16,7%, ou seja, uma'),
  ('Aguardando resposta', '5'),
  ('Tempo m&eacute;dio para responder', '20 dias e 19 horas'),
  ('Reputa&ccedil;&atilde;o calculada', 'Nenhuma. O site exige dez avalia&ccedil;&otilde;es e a empresa tem uma'),
], compacta=True)}
{tabela(['Reclama&ccedil;&atilde;o', 'Status', 'Data'], [
  ('Empresa n&atilde;o realiza reembolso de viagem cancelada, mesmo ap&oacute;s promessas de pagamento', 'N&atilde;o respondida', '02/06/2026'),
  ('Reembolso de viagem n&atilde;o realizado integralmente ap&oacute;s cancelamento e acordo de parcelamento', 'N&atilde;o respondida', '07/05/2026'),
  ('N&atilde;o me pagaram o reembolso', 'Respondida', 'h&aacute; 3 meses'),
  ('Empresa n&atilde;o paga o reembolso e s&atilde;o p&eacute;ssimos para contatar', 'Respondida', 'h&aacute; 3 meses'),
  ('Descumprimento de contrato e falta de suporte, solicito reembolso urgente', 'Resolvido', 'h&aacute; 3 meses'),
], 'Reclame Aqui, leitura de 06/08/2026. Exibindo 5 das 16 reclama&ccedil;&otilde;es ativas.', compacta=True)}
{nota('O que os n&uacute;meros escondem',
 'O perfil exibe o selo "Resolve 100,0% das reclama&ccedil;&otilde;es". Esse percentual vem de <b>uma &uacute;nica reclama&ccedil;&atilde;o avaliada</b>. '
 'N&atilde;o h&aacute; reputa&ccedil;&atilde;o calculada porque o RA exige dez avalia&ccedil;&otilde;es, e a empresa n&atilde;o chegou l&aacute;. '
 'O cliente que abre a p&aacute;gina n&atilde;o v&ecirc; um selo bom: v&ecirc; "Sem reputa&ccedil;&atilde;o definida" e "Empresa n&atilde;o verificada".',
 'As cinco reclama&ccedil;&otilde;es vis&iacute;veis tratam do mesmo assunto: <b>reembolso de viagem cancelada</b>. &Eacute; um tema &uacute;nico, o que torna a resposta padronizada e r&aacute;pida de montar.')}
''', 'Responder as cinco pendentes e verificar o perfil &eacute; trabalho de dias <span class="azul">e muda o segundo resultado do Google para o nome da marca.</span>')

# ============================================================ 14. ATENDIMENTO
pag('Atendimento', f'''
<h2 class="titulo">Coment&aacute;rio de elogio &eacute; respondido antes de pergunta de pre&ccedil;o</h2>
<p class="lede">Lemos os coment&aacute;rios das publica&ccedil;&otilde;es mais comentadas de tr&ecirc;s contas,
com as respostas encadeadas, e medimos o intervalo entre a pergunta e a resposta da empresa. O padr&atilde;o
&eacute; consistente e inverte a prioridade comercial.</p>
{grafico([
  ('Relacionamento', 'elogio, emoji, marca&ccedil;&atilde;o<br>m&eacute;dia de 4 casos', 0.7, '0,7 h', False),
  ('Pergunta de pre&ccedil;o', 'valor, vaga, ingresso<br>m&eacute;dia de 4 casos', 4.6, '4,6 h', True),
  ('Acusa&ccedil;&atilde;o p&uacute;blica', 'coment&aacute;rio de golpe<br>1 caso', 5.5, '5,5 h', True),
  ('Pior caso medido', 'Quero o a&eacute;reo<br>1 caso', 14.1, '14,1 h', True),
], 'Horas entre o coment&aacute;rio e a resposta da empresa. Coleta de 06/08/2026 sobre as publica&ccedil;&otilde;es mais comentadas de @sinfonyaturismo, @sinfonyaformaturas e @sinfonyaweeding.')}
{tabela(['Conta', 'Posts lidos', 'Coment&aacute;rios', 'Respondidos pela marca', 'Posts sem nenhuma resposta'], [
  ('@sinfonyaturismo', '15', '56', '14,3%', '9'),
  ('@sinfonyaformaturas', '15', '161', '11,8%', '7'),
  ('@sinfonyaweeding', '3', '4', '0%', '3'),
], alinha={1: 'num', 2: 'num', 3: 'num', 4: 'num'}, compacta=True)}
{nota('Tr&ecirc;s perguntas sem resposta no mesmo post',
 'Na publica&ccedil;&atilde;o DWZ1I5DiSLB de @sinfonyaformaturas, de abril de 2026, cinco pessoas pediram informa&ccedil;&atilde;o ou pre&ccedil;o. '
 'Tr&ecirc;s n&atilde;o foram respondidas. Uma delas, @ladjanefc, escreveu duas vezes: "preciso de informa&ccedil;&otilde;es" e, depois, '
 '"ainda tem pacote com ingressos?". <b>Nenhuma das duas foi respondida.</b>')}
''', 'A empresa responde em minutos quem elogia <span class="azul">e em horas quem pergunta o pre&ccedil;o.</span>')

# ============================================================ 15. O CASO GOLPE
pag('Reputa&ccedil;&atilde;o', f'''
<h2 class="titulo">A empresa foi chamada de golpe em p&uacute;blico e n&atilde;o teve o que mostrar</h2>
<p class="lede">Em abril de 2026, numa publica&ccedil;&atilde;o de oferta de @sinfonyaformaturas, um seguidor
escreveu: <b>"Ingresso? Esse golpe t&aacute; diferente"</b>. Cinco horas e meia depois, a empresa respondeu
defendendo-se: "n&atilde;o somos empresa de golpe, somos uma ag&ecirc;ncia".</p>
<p class="texto">A resposta est&aacute; correta e o tom foi adequado. O problema n&atilde;o &eacute; a resposta,
&eacute; que ela &eacute; a &uacute;nica prova dispon&iacute;vel. Uma pessoa que leu aquele coment&aacute;rio e
foi checar por conta pr&oacute;pria encontrou exatamente isto:</p>
{tabela(['O que a pessoa procurou', 'O que encontrou'], [
  ('Site oficial da empresa', 'Nenhum. O link do Linktree n&atilde;o abre'),
  ('Sinfonya Turismo no Google', 'Reclame Aqui em segundo lugar, JusBrasil em quarto'),
  ('Sinfonya Turismo &eacute; confi&aacute;vel', 'Reclame Aqui em primeiro, segundo e quarto'),
  ('Perfil da empresa no Google', 'Nota 4,6 com 55 avalia&ccedil;&otilde;es, sem nenhuma resposta da empresa'),
  ('Reclame Aqui', 'Empresa n&atilde;o verificada, sem reputa&ccedil;&atilde;o, 5 reclama&ccedil;&otilde;es sem resposta'),
  ('CNPJ da empresa', 'Tr&ecirc;s CNPJ com o mesmo nome, um deles inapto'),
  ('E-mail de contato', 'Um endere&ccedil;o gratuito do Gmail'),
])}
<p class="texto">A Sinfonya tem quinze anos de opera&ccedil;&atilde;o documentada, duas pra&ccedil;as
f&iacute;sicas, associa&ccedil;&atilde;o &agrave; ABAV-DF, 500 mil passageiros declarados e nota 4,6 no Google.
<b>Nenhum desses ativos est&aacute; onde a d&uacute;vida acontece.</b> A suspeita de golpe n&atilde;o vem de
m&aacute;-f&eacute; do seguidor: vem da aus&ecirc;ncia de qualquer prova verific&aacute;vel.</p>
''', 'A empresa tem toda a credibilidade necess&aacute;ria <span class="azul">e nenhum lugar onde guardar isso.</span>')

# ============================================================ 16. CRM DIAGNOSTICO
pag('CRM', f'''
<h2 class="titulo">N&atilde;o existe cadastro de cliente, existe hist&oacute;rico de conversa</h2>
<p class="lede">A empresa n&atilde;o tem CRM. O que ela tem &eacute; sete aparelhos de WhatsApp, cada um com a
mem&oacute;ria do que passou por ele. Sem acesso ao sistema interno, medimos os sinais que aparecem de fora.</p>
{defs([
  ('O hist&oacute;rico est&aacute; no aparelho, n&atilde;o na empresa',
   'Sete n&uacute;meros publicados, dois deles com uso intenso. Quem atendeu no (34) 99198-9798 tem o hist&oacute;rico daquele cliente. '
   'Se essa pessoa sai da empresa ou troca de aparelho, <b>o relacionamento sai junto</b>.'),
  ('Ningu&eacute;m volta a ser procurado',
   'Os destaques do perfil guardam dezenas de clientes que j&aacute; viajaram com a empresa. N&atilde;o h&aacute; nenhuma oferta de anivers&aacute;rio de viagem, ' 'nenhum programa de indica&ccedil;&atilde;o e nenhuma segunda oferta para quem j&aacute; foi. &Eacute; o p&uacute;blico mais barato que a empresa tem para vender de novo.'),
  ('Pergunta comercial se perde na caixa',
   'Nas publica&ccedil;&otilde;es auditadas, 11,8% a 14,3% dos coment&aacute;rios receberam resposta da marca, e a mesma pessoa '
   'perguntou duas vezes sem retorno. O que se v&ecirc; em p&uacute;blico costuma refletir o que acontece na caixa de mensagem.'),
  ('O p&oacute;s-venda vira reclama&ccedil;&atilde;o p&uacute;blica',
   'As cinco reclama&ccedil;&otilde;es vis&iacute;veis no Reclame Aqui tratam de reembolso de viagem cancelada, com queixa recorrente de dificuldade de contato. '
   'Um desses clientes escreveu que a empresa &eacute; "p&eacute;ssima para contatar". Sem registro central de acordo e prazo, cada cobran&ccedil;a recome&ccedil;a a discuss&atilde;o.'),
])}
<h3 class="sub">O que d&aacute; e o que n&atilde;o d&aacute; para afirmar</h3>
<p class="texto">N&atilde;o sabemos quantas mensagens chegam, em quanto tempo s&atilde;o respondidas nem quantas viram venda, e
por isso <b>n&atilde;o &eacute; poss&iacute;vel calcular a perda em reais</b>. O que est&aacute; medido &eacute; o que d&aacute; para ver de fora: perguntas de pre&ccedil;o sem resposta, sete portas de entrada sem hist&oacute;rico
comum e uma lista de clientes antigos que ningu&eacute;m volta a procurar. Com acesso ao WhatsApp e ao
hist&oacute;rico de vendas da empresa, esses tr&ecirc;s itens viram n&uacute;mero em reais.</p>
''', 'A empresa sabe quem viajou. <span class="azul">Ela s&oacute; n&atilde;o tem onde consultar.</span>')

# ============================================================ 17. CRM SOLUCAO
pag('CRM', f'''
<h2 class="titulo">O que resolve: uma caixa de entrada &uacute;nica com ficha de cliente</h2>
<p class="lede">A recomenda&ccedil;&atilde;o n&atilde;o &eacute; um CRM de vendas cl&aacute;ssico, feito para
equipe de campo. &Eacute; um CRM com caixa de WhatsApp compartilhada, que junta os sete n&uacute;meros num
lugar s&oacute; e transforma conversa em ficha.</p>
{defs([
  ('Uma caixa, v&aacute;rios atendentes',
   'Os n&uacute;meros continuam existindo, mas as conversas caem todas na mesma tela. Qualquer atendente v&ecirc; o hist&oacute;rico completo do cliente, '
   'independente de por qual n&uacute;mero ele entrou.'),
  ('Funil com etapa e dono',
   'Cada conversa vira uma oportunidade com destino, data, n&uacute;mero de pessoas, cidade de sa&iacute;da e respons&aacute;vel. '
   'O que hoje est&aacute; na cabe&ccedil;a do atendente passa a ser campo.'),
  ('Ningu&eacute;m depende da pr&oacute;pria mem&oacute;ria',
   'Or&ccedil;amento enviado e sem resposta em 48 horas vira uma tarefa para algu&eacute;m cobrar. &Eacute; onde mais se perde venda numa opera&ccedil;&atilde;o de pacote parcelado.'),
  ('Vender de novo para quem j&aacute; viajou',
   'Com cliente cadastrado por destino e data de viagem, fica poss&iacute;vel oferecer a pr&oacute;xima viagem na hora certa e montar um programa de indica&ccedil;&atilde;o.'),
])}
<h3 class="sub">Faixa de mercado, agosto de 2026</h3>
{tabela(['Ferramenta', 'Pre&ccedil;o de tabela', 'Observa&ccedil;&atilde;o'], [
  ('RD Station CRM', 'plano gratuito; pagos a partir de R$ 59,40 por usu&aacute;rio/m&ecirc;s', 'Brasileiro, cobra em real'),
  ('Pipedrive', 'a partir de R$ 60 a R$ 80 por usu&aacute;rio/m&ecirc;s', 'Pre&ccedil;o em d&oacute;lar, varia com c&acirc;mbio'),
  ('Kommo', 'a partir de R$ 80 por usu&aacute;rio/m&ecirc;s', 'Nasceu em cima de WhatsApp, o mais aderente ao caso'),
], 'Pre&ccedil;os de tabela consultados em 06/08/2026. As mensalidades mudam por fornecedor e por c&acirc;mbio.')}
{nota('Estimativa da Or&aacute;culo, a confirmar em proposta',
 'Implanta&ccedil;&atilde;o, uma vez: <b>R$ 4.500 a R$ 7.000</b>. Cobre juntar os n&uacute;meros num lugar s&oacute;, carregar os clientes j&aacute; atendidos, '
 'montar as etapas da venda e os campos de viagem, conectar Instagram e WhatsApp e treinar a equipe.',
 'Mensalidade do sistema: <b>cerca de R$ 320</b> para quatro atendentes, na faixa de R$ 80 por pessoa. Acompanhamento mensal opcional: <b>R$ 900 a R$ 1.500</b>.',
 'S&atilde;o valores de refer&ecirc;ncia desta auditoria, n&atilde;o proposta comercial. O n&uacute;mero final depende de quantos atendentes entram e de qual ferramenta for escolhida.')}
''')

# ============================================================ 18. BOT WHATSAPP
pag('WhatsApp', f'''
<h2 class="titulo">O bot resolve o problema mais barato de resolver: a primeira resposta</h2>
<p class="lede">A empresa recebe pergunta de pre&ccedil;o e responde em m&eacute;dia 4,6 horas nos coment&aacute;rios.
No WhatsApp, o custo de responder na hora &eacute; zero, e isso n&atilde;o &eacute; estimativa: &eacute; como a
plataforma cobra.</p>
{nota('A regra que muda a conta',
 'Quando o cliente manda mensagem para a empresa, abre-se uma <b>janela de atendimento de 24 horas</b>. Dentro dela, toda resposta da empresa &eacute; gratuita. '
 'A Meta confirma na documenta&ccedil;&atilde;o oficial que conversas de servi&ccedil;o s&atilde;o gratuitas desde novembro de 2024.',
 'Ou seja: um bot que responde imediatamente quem chega <b>n&atilde;o tem custo de mensagem</b>. O custo s&oacute; aparece quando a empresa inicia a conversa.')}
<h3 class="sub">O fluxo recomendado</h3>
{defs([
  ('1. Resposta imediata, sempre',
   'Confirma o recebimento, identifica de qual an&uacute;ncio ou conta a pessoa veio e j&aacute; diz o hor&aacute;rio de atendimento humano. '
   'Elimina o intervalo em que o cliente vai perguntar ao concorrente.'),
  ('2. Qualifica&ccedil;&atilde;o em quatro perguntas',
   'Destino, data pretendida, quantas pessoas e cidade de sa&iacute;da. S&atilde;o os quatro campos que o atendente pergunta hoje &agrave; m&atilde;o '
   'e que o CRM precisa para montar a oportunidade.'),
  ('3. Entrega do que j&aacute; &eacute; p&uacute;blico',
   'Pre&ccedil;o, parcelamento e o que est&aacute; inclu&iacute;do dos pacotes que a empresa j&aacute; publica na conta de Patos de Minas. '
   'Qualifica a conversa antes de ocupar o atendente.'),
  ('4. Transfer&ecirc;ncia com contexto',
   'O humano recebe a conversa com as quatro respostas j&aacute; preenchidas na ficha, n&atilde;o come&ccedil;a do zero.'),
  ('5. Utilidade e p&oacute;s-venda',
   'Lembrete de parcela, documenta&ccedil;&atilde;o da viagem, hor&aacute;rio de embarque e pesquisa depois do retorno. &Eacute; o tipo de mensagem mais barato, como mostra a p&aacute;gina seguinte, '
   'e o que mais reduz reclama&ccedil;&atilde;o de falta de contato.'),
])}
''', 'Responder na hora <span class="azul">n&atilde;o custa mensagem. Custa configurar uma vez.</span>')

# ============================================================ 19. BOT INVESTIMENTO
pag('WhatsApp', f'''
<h2 class="titulo">Quanto custa manter o WhatsApp automatizado</h2>
<p class="lede">Desde julho de 2025 o WhatsApp cobra por mensagem entregue, e n&atilde;o mais por conversa. Cada tipo de mensagem tem um pre&ccedil;o bem diferente, e isso muda como vale a pena usar a ferramenta.</p>
{tabela(['Categoria', 'Quando se aplica', 'Faixa no Brasil'], [
  ('Servi&ccedil;o', 'Resposta dentro da janela de 24 horas aberta pelo cliente', '<b>gratuito</b>'),
  ('Utilidade', 'Lembrete de parcela, voucher, hor&aacute;rio de embarque', 'R$ 0,04 a R$ 0,05 por mensagem'),
  ('Autentica&ccedil;&atilde;o', 'C&oacute;digo de verifica&ccedil;&atilde;o', 'R$ 0,15 a R$ 0,19 por mensagem'),
  ('Marketing', 'Oferta, lan&ccedil;amento de sa&iacute;da, campanha', 'R$ 0,31 a R$ 0,38 por mensagem'),
], 'Regra de cobran&ccedil;a e gratuidade das 24 horas conforme a documenta&ccedil;&atilde;o oficial da Meta, consulta de 06/08/2026. Os valores em real vêm das tabelas p&uacute;blicas de parceiros brasileiros na mesma data.')}
<h3 class="sub">Como isso se traduz em conta mensal</h3>
{defs([
  ('Atender quem chega: R$ 0',
   'Todo o fluxo de primeira resposta, qualifica&ccedil;&atilde;o e transfer&ecirc;ncia acontece dentro da janela gratuita. '
   'Independente do volume, atender n&atilde;o gera custo de mensagem.'),
  ('P&oacute;s-venda e lembrete: barato',
   'Dois mil lembretes por m&ecirc;s ficam entre <b>R$ 80 e R$ 100</b>. &Eacute; a faixa que resolve a queixa de "p&eacute;ssimos para contatar".'),
  ('Campanha de oferta: o que pesa',
   'Tr&ecirc;s mil mensagens de marketing por m&ecirc;s ficam entre <b>R$ 930 e R$ 1.140</b>. Deve entrar depois, e s&oacute; para listas separadas por interesse no CRM.'),
])}
{nota('Estimativa da Or&aacute;culo, a confirmar em proposta',
 'Implanta&ccedil;&atilde;o, uma vez: <b>R$ 6.000 a R$ 9.000</b>. Cobre libera&ccedil;&atilde;o da conta oficial, comprova&ccedil;&atilde;o da empresa junto &agrave; Meta, '
 'desenho e constru&ccedil;&atilde;o do fluxo, integra&ccedil;&atilde;o ao CRM e aprova&ccedil;&atilde;o dos textos padr&atilde;o junto &agrave; Meta.',
 'Sistema de atendimento: <b>R$ 200 a R$ 500 por m&ecirc;s</b>, conforme o fornecedor. Mensagens: vari&aacute;vel, conforme a tabela acima.',
 'Para liberar a conta oficial, a Meta exige CNPJ ativo e nome, endere&ccedil;o e telefone batendo entre si. <b>Ela depende de resolver antes o CNPJ inapto e o endere&ccedil;o divergente.</b>')}
''')

# ============================================================ 20. SITE
pag('Site', f'''
<h2 class="titulo">O site que resolve tr&ecirc;s problemas de uma vez</h2>
<p class="lede">O site n&atilde;o &eacute; um item de imagem. Ele &eacute; a resposta simult&acirc;nea para a
prova de exist&ecirc;ncia, para a busca do Google e para o bot&atilde;o quebrado do Perfil da Empresa. N&atilde;o
precisa ser grande: precisa existir e ser encontr&aacute;vel.</p>
{defs([
  ('P&aacute;gina inicial: prova de que a empresa &eacute; real',
   'Quinze anos de opera&ccedil;&atilde;o, 500 mil passageiros, CNPJ, os dois endere&ccedil;os f&iacute;sicos, a associa&ccedil;&atilde;o &agrave; ABAV-DF e as '
   'avalia&ccedil;&otilde;es do Google. &Eacute; a p&aacute;gina que responde &agrave; d&uacute;vida de golpe.'),
  ('Uma p&aacute;gina por destino',
   'Caldas Novas, Rio Quente, Porto Seguro, Fortaleza, Natal, Gramado, Foz, Madri e Israel 2027. Com sa&iacute;das do m&ecirc;s, pre&ccedil;o, parcelamento e o que est&aacute; inclu&iacute;do. '
   '<b>&Eacute; isso que os concorrentes t&ecirc;m e que faz eles aparecerem nas cinco buscas.</b>'),
  ('Uma p&aacute;gina por linha de neg&oacute;cio',
   'Formaturas, casamentos, turismo crist&atilde;o e a filial de Patos de Minas. Resolve a fragmenta&ccedil;&atilde;o de cinco contas com um &uacute;nico endere&ccedil;o.'),
  ('Formul&aacute;rio que cai no CRM',
   'N&atilde;o em e-mail, n&atilde;o em Google Forms. Substitui o formul&aacute;rio que hoje atende a conta de casamentos.'),
  ('O b&aacute;sico por tr&aacute;s',
   'Endere&ccedil;o de site comprado no nome da empresa, e-mail terminando nesse endere&ccedil;o em vez de gmail, ficha do Google assumida e ligada ao site, '
   'e as informa&ccedil;&otilde;es de contato organizadas do jeito que o Google entende, para ele exibir endere&ccedil;o, telefone e hor&aacute;rio.'),
])}
{nota('Estimativa da Or&aacute;culo, a confirmar em proposta',
 'Site institucional com p&aacute;ginas de destino, formul&aacute;rio integrado ao CRM e a prepara&ccedil;&atilde;o para aparecer na busca do Google: '
 '<b>R$ 9.000 a R$ 16.000</b>, conforme o n&uacute;mero de p&aacute;ginas de destino. Prazo estimado de 4 a 7 semanas.',
 'Hospedagem, dom&iacute;nio e e-mail corporativo: cerca de <b>R$ 120 a R$ 250 por m&ecirc;s</b>. Manuten&ccedil;&atilde;o de conte&uacute;do e sa&iacute;das do m&ecirc;s pode entrar no acompanhamento mensal.')}
''', 'O site &eacute; o &uacute;nico ativo que a empresa registra no pr&oacute;prio nome <span class="azul">e leva junto se trocar de rede social.</span>')

# ============================================================ 21. PRIORIDADES
pag('Prioridades', f'''
<h2 class="titulo">O que resolver primeiro, por esfor&ccedil;o e por risco</h2>
<p class="lede">Ordenado pelo que trava mais neg&oacute;cio com menos trabalho. Os sete primeiros itens s&atilde;o
configura&ccedil;&atilde;o, custam pouco ou nada e podem ser feitos na mesma semana.</p>
{tabela(['#', 'A&ccedil;&atilde;o', 'Esfor&ccedil;o', 'O que destrava'], [
  ('1', 'Comprar os quatro endere&ccedil;os de site da marca', 'minutos', 'Impede que outra empresa fique com o endere&ccedil;o que o Google anuncia'),
  ('2', 'Assumir a ficha da empresa no Google', 'dias', 'Nota 4,6 e 55 avalia&ccedil;&otilde;es passam a ser da empresa'),
  ('3', 'Corrigir o link da conta crist&atilde; no Linktree', 'minutos', 'O produto de maior ticket volta a ter caminho'),
  ('4', 'Trocar o Google Forms da conta de casamentos', 'minutos', '16.438 seguidores de ticket alto ganham contato direto'),
  ('5', 'Colocar contato na bio de @sinfonya_cristao', 'minutos', 'Israel 2027 passa a ter por onde comprar'),
  ('6', 'Preencher cidade e endere&ccedil;o nas cinco contas', 'minutos', 'Descoberta local dentro do Instagram'),
  ('7', 'Converter @sinfonyaformaturas em conta de empresa', 'minutos', 'Campos comerciais e ficha de neg&oacute;cio'),
  ('8', 'Verificar o perfil e responder as 5 reclama&ccedil;&otilde;es', 'dias', 'Muda o segundo resultado do Google para a marca'),
  ('9', 'Publicar o site com p&aacute;gina por destino', 'semanas', 'Prova de exist&ecirc;ncia e entrada nas buscas comerciais'),
  ('10', 'Unificar os sete n&uacute;meros num CRM', 'semanas', 'Hist&oacute;rico deixa de morar no aparelho'),
  ('11', 'Ligar o bot de primeira resposta', 'semanas', 'Fim das 4,6 horas de espera por pergunta de pre&ccedil;o'),
  ('12', 'Regularizar CNPJ inapto e unificar endere&ccedil;o', 'semanas', 'Pr&eacute;-requisito da verifica&ccedil;&atilde;o junto &agrave; Meta'),
])}
<h3 class="sub">O que n&atilde;o recomendamos agora</h3>
<p class="texto">Abrir canal novo, TikTok ou YouTube, e p&ocirc;r m&iacute;dia paga no ar antes de existir site e
ficha do Google assumida. Tr&aacute;fego pago hoje entrega gente numa caixa de mensagem que responde em
horas, sem nenhuma p&aacute;gina onde o cliente possa se convencer sozinho.</p>
''', 'Sete das doze a&ccedil;&otilde;es <span class="azul">n&atilde;o custam nada al&eacute;m de uma tarde de trabalho.</span>')

# ============================================================ 22. FONTES
pag('Fontes', f'''
<h2 class="titulo">De onde veio cada dado</h2>
<p class="lede">Toda informa&ccedil;&atilde;o deste documento pode ser conferida por qualquer pessoa, refazendo as mesmas consultas nas mesmas fontes.</p>
{tabela(['Dado', 'Fonte e data'], [
  ('Situa&ccedil;&atilde;o dos seis endere&ccedil;os de site', 'Registro.br, consulta de 06/08/2026'),
  ('Campos de cada uma das cinco contas', 'Instagram, leitura direta com conta conectada, 06/08/2026'),
  ('Sete telefones e aus&ecirc;ncia de site e e-mail', 'Leitura de 428 legendas e bios, coletas de 04 e 06/08/2026'),
  ('Taxa de resposta e tempo at&eacute; a resposta', '220 coment&aacute;rios de 33 publica&ccedil;&otilde;es de tr&ecirc;s contas, com as respostas da empresa, 06/08/2026'),
  ('Coment&aacute;rio de acusa&ccedil;&atilde;o e resposta da empresa', 'Publica&ccedil;&atilde;o DWZ1I5DiSLB de @sinfonyaformaturas, abril de 2026'),
  ('Links do Linktree e teste de cada destino', 'linktr.ee/gruposinfonyaturismo, 06/08/2026'),
  ('Perfil da Empresa no Google, nota e avalia&ccedil;&otilde;es', 'google.com.br, ficha da empresa exibida na busca, 06/08/2026'),
  ('Primeira p&aacute;gina das sete consultas', 'google.com.br, pt-BR, regi&atilde;o BR, 06/08/2026'),
  ('Indicadores e reclama&ccedil;&otilde;es', 'Reclame Aqui, janela de 01/02/2026 a 31/07/2026, leitura de 06/08/2026'),
  ('CNPJ e situa&ccedil;&atilde;o cadastral', 'Econodata, Serasa Experian, Solutudo e cnpj.biz, consultas de 06/08/2026'),
  ('Modelo de cobran&ccedil;a do WhatsApp', 'P&aacute;ginas oficiais da Meta sobre como o WhatsApp cobra, 06/08/2026'),
  ('Faixas de pre&ccedil;o por mensagem no Brasil', 'Tabelas p&uacute;blicas de parceiros brasileiros do WhatsApp, 06/08/2026'),
  ('Pre&ccedil;o de tabela de CRM', 'P&aacute;ginas de pre&ccedil;o de RD Station CRM, Pipedrive e Kommo, 06/08/2026'),
], compacta=True)}
<h3 class="sub">Sobre as estimativas de investimento</h3>
<p class="texto">Os valores de implanta&ccedil;&atilde;o de CRM, bot e site s&atilde;o <b>estimativas da
Or&aacute;culo para esta auditoria</b>, n&atilde;o proposta comercial. Os pre&ccedil;os de mensalidade e de mensagem s&atilde;o de tabela p&uacute;blica dos fornecedores e mudam sem aviso, inclusive por c&acirc;mbio. O
n&uacute;mero final de qualquer frente depende do escopo fechado com a empresa.</p>
''')

# ============================================================ CONTRACAPA
paginas.append(f'''<section class="pagina fim">
<div class="capa-topo">
  <img src="data:image/png;base64,{LOGO}" alt="Or&aacute;culo">
  <div class="capa-meta">Resumo<br>Auditoria de presen&ccedil;a digital</div>
</div>
<div style="margin-top:auto">
  <h2>Uma empresa de quinze anos que n&atilde;o consegue provar que existe</h2>
  <p class="fim-lede">A Sinfonya tem audi&ecirc;ncia, portf&oacute;lio, duas pra&ccedil;as, nota 4,6 no Google e
  quinze anos de opera&ccedil;&atilde;o. Tudo isso est&aacute; espalhado em canais que ela n&atilde;o controla,
  e a maior parte do conserto custa uma tarde.</p>
  <div class="fim-linhas">
    <div class="fim-linha"><b>O ativo esquecido</b><span>Nota 4,6 com 55 avalia&ccedil;&otilde;es num Perfil do Google que a empresa nunca reivindicou</span></div>
    <div class="fim-linha"><b>O risco aberto</b><span>Os quatro dom&iacute;nios da marca est&atilde;o livres, e o Google anuncia um deles como o site oficial</span></div>
    <div class="fim-linha"><b>O gargalo</b><span>Sete n&uacute;meros de WhatsApp sem hist&oacute;rico comum e pergunta de pre&ccedil;o respondida em 4,6 horas</span></div>
    <div class="fim-linha"><b>A prova que falta</b><span>Zero site, cinco reclama&ccedil;&otilde;es sem resposta e aus&ecirc;ncia total em cinco buscas comerciais</span></div>
  </div>
</div>
<div class="fim-rodape">
  <div><b>Or&aacute;culo Tecnologia</b>Coleta de 4 e 6 de agosto de 2026, sobre 5 contas,<br>428 legendas, 33 publica&ccedil;&otilde;es e 7 consultas de busca</div>
  <div>Documento confidencial, destinado ao Grupo Sinfonya<br>V&aacute;lido por 30 dias a partir do envio</div>
</div>
</section>''')

# ============================================================ MONTAGEM
html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Auditoria de Presen&ccedil;a Digital, Grupo Sinfonya Turismo</title>
<meta name="description" content="Auditoria de presenca digital do Grupo Sinfonya Turismo: Instagram, site, Google, Reclame Aqui, CRM e atendimento automatizado no WhatsApp. Oraculo Tecnologia, agosto de 2026.">
<style>{FIRA}</style>
<style>{CSS}</style>
</head>
<body>
{''.join(paginas)}
</body>
</html>'''

destino = os.path.join(RAIZ, 'SinfonyaGrupo', 'Auditoria-Presenca-Digital.html')
open(destino, 'w', encoding='utf-8').write(html)
print(f'gerado: {destino}')
print(f'paginas: {len(paginas)}  |  tamanho: {len(html)/1024:.0f} KB')

# --------- validacao ---------
erros = []
corpo = re.sub(r'<style>.*?</style>', '', html, flags=re.S)
for termo in ['Joana', 'drajoanatavares', 'ladeguste', 'La Deguste', 'Elora', 'Flavia Melow', 'PECBR']:
    if termo.lower() in corpo.lower():
        erros.append(f'residuo de outro cliente: {termo}')
aspas = re.findall(r'<[^>]*[“”‘’][^>]*>', corpo)
if aspas:
    erros.append(f'aspas curvas dentro de tag: {len(aspas)} -> {aspas[:2]}')
if html.count('<section') != html.count('</section>'):
    erros.append('section desbalanceada')
if 'base64,' not in html:
    erros.append('fonte ou logo nao embutidos')
print('VALIDACAO:', 'ok, sem problemas' if not erros else erros)
