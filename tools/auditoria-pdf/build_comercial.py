# -*- coding: utf-8 -*-
"""Proposta Comercial do Grupo Sinfonya, versao 2: os tres planos mensais mais as
frentes de site, cadastro de clientes, atendimento no WhatsApp e Google.
Reconstroi a proposta de 05/08/2026 e acrescenta as frentes novas, com menos texto e mais preco."""
import base64, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_css import CSS

RAIZ = '/Users/touchbar/Codigos-Projetos/oraculo/analises-oraculo'
TMP = os.path.dirname(os.path.abspath(__file__))
FIRA = open(os.path.join(TMP, 'fira-embed.css')).read()
LOGO = base64.b64encode(open(os.path.join(RAIZ, 'logo.png'), 'rb').read()).decode()
DATA = '6 de agosto de 2026'

# CSS extra so desta proposta: quadro de planos e linhas de total
EXTRA = """
table.planos { width: 100%; border-collapse: collapse; margin: 0 0 3mm; }
table.planos th, table.planos td { padding: 3mm 4mm; vertical-align: middle; }
table.planos th.rot, table.planos td.rot { text-align: left; padding-left: 0; width: 42mm;
  font-size: 8.2pt; font-weight: 600; color: var(--tinta); }
table.planos th.col { text-align: center; font-size: 10pt; font-weight: 700; color: var(--tinta);
  border-bottom: .9pt solid var(--reguaf); padding-bottom: 2.5mm; }
table.planos th.col.dest { background: #eef1fb; }
table.planos td.v { text-align: center; font-size: 8.2pt; color: var(--corpo);
  border-bottom: .5pt solid var(--regua); }
table.planos td.v.dest { background: #eef1fb; }
table.planos .rec { display: block; font-size: 6.8pt; font-weight: 600; color: var(--azul);
  margin-bottom: .8mm; letter-spacing: .1pt; }
table.planos .preco { display: block; font-size: 17pt; font-weight: 700; color: var(--tinta); line-height: 1.05; }
table.planos .preco.az { color: var(--azul); }
table.planos .un { display: block; font-size: 6.8pt; color: var(--suave); margin-top: 1mm; }
table.planos tr.grupo td { font-size: 7.4pt; font-weight: 600; color: var(--azul);
  padding: 3.6mm 0 1.4mm; border-bottom: none; text-align: left; }
table.planos.esc td { padding: 2.2mm 4mm; }
table.planos.esc td.rot { font-size: 7.8pt; line-height: 1.35; width: 52mm; padding-left: 0; }
table.planos.esc td.v { font-size: 7.8pt; }
table.planos.esc th.col { font-size: 9pt; }
table.t td.tot, table.t th.tot { font-weight: 700; color: var(--tinta); }
table.t tr.total td { border-bottom: .9pt solid var(--reguaf); font-weight: 700; color: var(--tinta); }
.na { color: var(--fraco); }
.sim { color: var(--azul); font-weight: 600; }
"""

paginas = []
_n = [0]


def pag(secao, corpo, fecho=None):
    _n[0] += 1
    f = f'<div class="fecho">{fecho}</div>' if fecho else ''
    paginas.append(
        f'<section class="pagina">'
        f'<div class="cab"><span class="cab-esq">Grupo Sinfonya &middot; Or&aacute;culo Tecnologia</span>'
        f'<span class="cab-dir">{secao}</span></div>{corpo}{f}'
        f'<div class="rod"><span>Proposta comercial</span><span>{_n[0]}</span></div></section>')


def tabela(cols, linhas, fonte=None, compacta=False, alinha=None):
    alinha = alinha or {}
    cls = 't compacta' if compacta else 't'
    th = ''.join(f'<th class="num">{c}</th>' if alinha.get(i) == 'num' else f'<th>{c}</th>'
                 for i, c in enumerate(cols))
    tr = ''
    for l in linhas:
        if isinstance(l, tuple) and l and l[0] == '__grupo__':
            tr += f'<tr class="grupo"><td colspan="{len(cols)}">{l[1]}</td></tr>'
            continue
        total = isinstance(l, tuple) and l and l[0] == '__total__'
        if total: l = l[1:]
        tds = ''
        for i, c in enumerate(l):
            k = []
            if i == 0: k.append('forte')
            if alinha.get(i) == 'num': k.append('num')
            cl = f' class="{" ".join(k)}"' if k else ''
            tds += f'<td{cl}>{c}</td>'
        tr += f'<tr class="total">{tds}</tr>' if total else f'<tr>{tds}</tr>'
    f = f'<p class="fonte">{fonte}</p>' if fonte else ''
    return f'<table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>{f}'


def defs(itens):
    return '<div class="defs">' + ''.join(
        f'<div class="def"><div class="def-r">{r}</div><div class="def-d">{t}</div></div>'
        for r, t in itens) + '</div>'


def nota(titulo, *ps):
    return f'<div class="nota"><b>{titulo}</b>{"".join(f"<p>{x}</p>" for x in ps)}</div>'


def escopo(titulo, lede, blocos, fonte=None):
    """Tabela de escopo por plano, com a coluna do meio destacada."""
    linhas = ''
    for grupo, itens in blocos:
        linhas += f'<tr class="grupo"><td colspan="4">{grupo}</td></tr>'
        for rot, a, b, c in itens:
            def cel(x):
                if x == 'sim': return '<span class="sim">sim</span>'
                if x == 'nao': return '<span class="na">n&atilde;o inclu&iacute;do</span>'
                return x
            linhas += (f'<tr><td class="rot">{rot}</td>'
                       f'<td class="v">{cel(a)}</td><td class="v dest">{cel(b)}</td><td class="v">{cel(c)}</td></tr>')
    f = f'<p class="fonte">{fonte}</p>' if fonte else ''
    return (f'<h2 class="titulo">{titulo}</h2><p class="lede">{lede}</p>'
            f'<table class="planos esc"><thead><tr><th class="rot">Entrega</th>'
            f'<th class="col">Essencial</th><th class="col dest">Crescimento</th>'
            f'<th class="col">Autoridade</th></tr></thead><tbody>{linhas}</tbody></table>{f}')


# ============================================================ CAPA
paginas.append(f'''<section class="pagina capa">
<div class="capa-topo">
  <img src="data:image/png;base64,{LOGO}" alt="Or&aacute;culo">
  <div class="capa-meta">Documento confidencial<br>{DATA}</div>
</div>
<div class="capa-corpo">
  <div class="capa-kicker">Grupo Sinfonya Turismo e Formaturas</div>
  <h1>Proposta comercial: redes, an&uacute;ncios, site, cadastro e WhatsApp</h1>
  <p class="capa-lede">Auditamos 348 publica&ccedil;&otilde;es das duas contas principais e, depois, toda a
  presen&ccedil;a digital do grupo fora do Instagram. Esta proposta re&uacute;ne as seis frentes que saem
  desses dois levantamentos, com escopo e pre&ccedil;o de cada uma.</p>
</div>
<div class="capa-rodape">
  <div class="capa-stat"><b>6</b><span>frentes no mesmo contrato</span></div>
  <div class="capa-stat"><b>22.900</b><span>reais de entrada, uma vez</span></div>
  <div class="capa-stat"><b>6.900</b><span>reais por m&ecirc;s</span></div>
  <div class="capa-stat"><b>30 dias</b><span>validade desta proposta</span></div>
</div>
</section>''')

# ============================================================ 2. O QUE ENCONTRAMOS
pag('Diagn&oacute;stico', f'''
<h2 class="titulo">O que os dois levantamentos encontraram</h2>
<p class="lede">Tudo abaixo foi apurado direto nas contas e nos canais p&uacute;blicos, em 4 e 6 de agosto de
2026. Os documentos completos t&ecirc;m a fonte de cada n&uacute;mero.</p>
{tabela(['Indicador', '@sinfonyaturismo', '@sinfonyaformaturas'], [
  ('Seguidores', '50.393', '25.821'),
  ('Taxa de engajamento', '0,026%', '0,606%'),
  ('Visualiza&ccedil;&otilde;es m&eacute;dias por Reel', '853', '6.494'),
  ('Alcance do Reel sobre a pr&oacute;pria base', '1,7%', '25,1%'),
  ('Publica&ccedil;&otilde;es por m&ecirc;s, no ritmo atual', '61', '3,9'),
  ('Posts com chamada para a&ccedil;&atilde;o', '79%', '14%'),
], alinha={1: 'num', 2: 'num'}, compacta=True)}
<p class="texto">A conta de turismo tem o dobro de seguidores e recebe um quarto das rea&ccedil;&otilde;es. A de
formaturas engaja vinte e tr&ecirc;s vezes mais e parou de publicar em 2024. Os erros s&atilde;o opostos e
nenhum dos dois exige recome&ccedil;ar do zero.</p>
<h3 class="sub">Fora do Instagram, o que encontramos</h3>
{tabela(['Achado', 'O que isso custa'], [
  ('Os quatro endere&ccedil;os de site da marca nunca foram comprados', 'Um concorrente pode levar o endere&ccedil;o que o Google anuncia como site oficial'),
  ('A ficha no Google tem nota 4,6 e 55 avalia&ccedil;&otilde;es, e ningu&eacute;m assumiu', 'A empresa n&atilde;o responde nenhuma avalia&ccedil;&atilde;o'),
  ('A marca n&atilde;o aparece em nenhuma das cinco buscas que vendem viagem', 'Quem procura excurs&atilde;o ou formatura encontra o concorrente'),
  ('16 reclama&ccedil;&otilde;es no Reclame Aqui, 5 sem resposta', '&Eacute; o segundo resultado do Google para o nome da marca'),
  ('Sete n&uacute;meros de WhatsApp sem hist&oacute;rico comum', 'Cliente que volta pelo n&uacute;mero errado recome&ccedil;a do zero'),
  ('Pergunta de pre&ccedil;o esperando 4,6 horas por resposta', 'Elogio &eacute; respondido em 0,7 hora'),
], compacta=True)}
''', 'A capacidade de produ&ccedil;&atilde;o existe e est&aacute; instalada. <span class="azul">O que falta &eacute; estrutura e dire&ccedil;&atilde;o.</span>')

# ============================================================ 3. RESUMO DO INVESTIMENTO
pag('Investimento', f'''
<h2 class="titulo">O investimento, em uma p&aacute;gina</h2>
<p class="lede">S&atilde;o dois blocos. As obras de entrada s&atilde;o pagas uma vez e constroem o que hoje
n&atilde;o existe. O mensal &eacute; o trabalho cont&iacute;nuo em cima do que foi constru&iacute;do.</p>
{tabela(['', 'Contratando por frente', 'Tudo no mesmo contrato'], [
  ('__grupo__', 'Entrada, pagamento &uacute;nico'),
  ('Site completo, com p&aacute;ginas de destino', '12.000', ''),
  ('Atendimento automatizado no WhatsApp', '7.500', ''),
  ('Cadastro de clientes', '5.500', ''),
  ('Google e reputa&ccedil;&atilde;o', '1.800', ''),
  ('Rastreamento e automa&ccedil;&atilde;o', '500', ''),
  ('__total__', 'Total de entrada', '27.300', '<b>22.900</b>'),
  ('__grupo__', 'Mensal'),
  ('Gest&atilde;o das redes e tr&aacute;fego pago, plano Crescimento', '5.500', ''),
  ('SEO e presen&ccedil;a no Google', '2.500', ''),
  ('__total__', 'Total mensal', '8.000', '<b>6.900</b>'),
], 'Valores em reais, acrescidos de imposto. A entrada pode ser parcelada em at&eacute; doze vezes, o que d&aacute; 1.908 reais por m&ecirc;s.', alinha={1: 'num', 2: 'num'}, compacta=True)}
{nota('A economia de fechar junto',
 'Na entrada, <b>4.400 reais</b>. No mensal, <b>1.100 por m&ecirc;s</b>, ou 13.200 no primeiro ano.',
 'As p&aacute;ginas seguintes detalham o escopo de cada bloco. Verba de an&uacute;ncios e mensalidade de ferramenta '
 's&atilde;o pagas diretamente aos fornecedores e est&atilde;o listadas na p&aacute;gina 9.')}
''', 'Sete dos problemas encontrados <span class="azul">se resolvem na primeira semana, antes de qualquer produ&ccedil;&atilde;o.</span>')

# ============================================================ 4. OS TRES PLANOS
pag('Planos mensais', f'''
<h2 class="titulo">Tr&ecirc;s n&iacute;veis de atua&ccedil;&atilde;o, as duas contas no mesmo contrato</h2>
<p class="lede">Os valores abaixo cobrem @sinfonyaturismo e @sinfonyaformaturas juntas, e s&atilde;o o bloco
mensal de redes sociais e an&uacute;ncios. SEO entra por fora, na p&aacute;gina 8.</p>
<table class="planos">
<thead><tr><th class="rot"></th>
<th class="col">Essencial</th>
<th class="col dest"><span class="rec">Recomendado</span>Crescimento</th>
<th class="col">Autoridade</th></tr></thead>
<tbody>
<tr><td class="rot">Investimento mensal</td>
  <td class="v"><span class="preco">3.500</span><span class="un">reais por m&ecirc;s</span></td>
  <td class="v dest"><span class="preco az">5.500</span><span class="un">reais por m&ecirc;s</span></td>
  <td class="v"><span class="preco">7.500</span><span class="un">reais por m&ecirc;s</span></td></tr>
<tr><td class="rot">Contratando as duas contas em separado</td>
  <td class="v">4.000</td><td class="v dest">7.000</td><td class="v">10.000</td></tr>
<tr><td class="rot">Diferen&ccedil;a no ano</td>
  <td class="v">6.000 a menos</td><td class="v dest">18.000 a menos</td><td class="v">30.000 a menos</td></tr>
<tr><td class="rot">Verba de an&uacute;ncios</td>
  <td class="v"><span class="na">n&atilde;o se aplica</span></td>
  <td class="v dest">1.500 a 3.000 por m&ecirc;s</td>
  <td class="v">a definir</td></tr>
</tbody></table>
<p class="fonte">Valores em reais, acrescidos de imposto. A verba de an&uacute;ncios &eacute; paga separadamente e direto &agrave; plataforma, com relat&oacute;rio de aplica&ccedil;&atilde;o todo m&ecirc;s. Sem fidelidade no primeiro m&ecirc;s em qualquer um dos planos.</p>
<h3 class="sub">Por que o plano Crescimento &eacute; o indicado</h3>
<p class="texto">Ele &eacute; o menor plano que executa o ciclo de 90 dias inteiro. Cobre as quatro
prioridades que a auditoria apontou: Reel gravado no lugar do flyer animado na conta de turismo, retomada do
formato que rendeu v&iacute;deos de 63 mil visualiza&ccedil;&otilde;es na conta de formaturas, subida da taxa de
chamada para a&ccedil;&atilde;o de 14% para 60%, e um caminho medido entre a publica&ccedil;&atilde;o e o
or&ccedil;amento.</p>
''')

# ============================================================ 5. ESCOPO 1
pag('Escopo mensal, parte 1', escopo(
  'Conte&uacute;do e estrutura de perfil',
  'Os volumes abaixo s&atilde;o totais mensais somando as duas contas. A divis&atilde;o entre elas &eacute; '
  'sazonal: a conta de formaturas recebe mais pe&ccedil;as entre setembro e dezembro, e a de turismo domina o resto do ano.',
  [('Conte&uacute;do publicado', [
      ('Publica&ccedil;&otilde;es de feed por m&ecirc;s', '20', '28', '40'),
      ('Reels gravados e editados por m&ecirc;s', '6', '12', '20'),
      ('Stories por semana, em cada perfil', '3', '5', 'di&aacute;rios'),
      ('Cobertura ao vivo de embarque ou viagem', 'nao', '1 por m&ecirc;s', '2 por m&ecirc;s'),
      ('Parceria com creator', 'nao', '1 por temporada', '2 por temporada'),
    ]),
   ('Estrat&eacute;gia e estrutura de perfil', [
      ('Gest&atilde;o das duas contas com calend&aacute;rio aprovado', 'sim', 'sim', 'sim'),
      ('Configura&ccedil;&atilde;o completa dos perfis e reescrita das bios', 'sim', 'sim', 'sim'),
      ('Destaques reorganizados por jornada e por ano de turma', 'sim', 'sim', 'sim'),
      ('Corre&ccedil;&atilde;o dos links quebrados e do agregador', 'sim', 'sim', 'sim'),
      ('Roteiro de Reel e dire&ccedil;&atilde;o de grava&ccedil;&atilde;o remota', 'nao', 'sim', 'sim'),
      ('Gest&atilde;o das contas sat&eacute;lite do grupo', 'nao', 'nao', 'sim'),
    ])],
  'A grade editorial de cada m&ecirc;s &eacute; aprovada antecipadamente pela Sinfonya. As pe&ccedil;as de cobertura e os stories de bastidor s&atilde;o produzidos a partir de material bruto enviado pela equipe em campo.'))

# ============================================================ 6. ESCOPO 2
pag('Escopo mensal, parte 2', escopo(
  'An&uacute;ncios, convers&atilde;o e acompanhamento',
  'Os itens abaixo cobrem a gest&atilde;o das campanhas, a estrutura que liga publica&ccedil;&atilde;o a conversa '
  'e o acompanhamento mensal das duas contas. A verba de an&uacute;ncios &eacute; paga separadamente.',
  [('An&uacute;ncios', [
      ('Meta Ads, no Instagram e no Facebook', 'nao', 'sim', 'sim'),
      ('TikTok Ads', 'nao', 'nao', 'sim'),
      ('Campanhas ativas ao mesmo tempo', 'nao', 'at&eacute; 4', 'at&eacute; 8'),
      ('Otimiza&ccedil;&atilde;o e ajuste de campanha', 'nao', 'semanal', '2 vezes por semana'),
      ('Criativos produzidos para an&uacute;ncio, por m&ecirc;s', 'nao', '6', '12'),
      ('Segmenta&ccedil;&atilde;o por regi&atilde;o de sa&iacute;da e por escola', 'nao', 'sim', 'sim'),
    ]),
   ('Convers&atilde;o e atendimento', [
      ('Link rastre&aacute;vel por destino e por turma', 'nao', 'sim', 'sim'),
      ('Automa&ccedil;&atilde;o de mensagem direta por coment&aacute;rio', 'nao', 'sim', 'sim'),
      ('Scripts de atendimento por tipo de viagem e para comiss&otilde;es', 'nao', 'sim', 'sim'),
    ]),
   ('Acompanhamento', [
      ('Relat&oacute;rio mensal consolidado das duas contas', 'sim', 'sim', 'sim'),
      ('Relat&oacute;rio de convers&atilde;o, com origem das conversas', 'nao', 'sim', 'sim'),
      ('Painel de conte&uacute;do, cliques e comiss&otilde;es em negocia&ccedil;&atilde;o', 'nao', 'nao', 'sim'),
      ('Reuni&atilde;o estrat&eacute;gica', 'nao', 'mensal', 'quinzenal'),
      ('Atendimento por WhatsApp', 'hor&aacute;rio comercial', 'hor&aacute;rio comercial', 'priorit&aacute;rio'),
    ])]))

# ============================================================ 7. OBRAS DE ENTRADA
pag('Obras de entrada', f'''
<h2 class="titulo">Site, cadastro de clientes e WhatsApp</h2>
<p class="lede">S&atilde;o as tr&ecirc;s frentes que hoje n&atilde;o existem no grupo. Cada uma &eacute; paga uma
vez e passa a ser um ativo da empresa. O que cada uma inclui est&aacute; abaixo, sem escopo aberto.</p>
{tabela(['Frente', 'O que inclui', 'Valor'], [
  ('Site completo', 'P&aacute;gina inicial com prova de exist&ecirc;ncia, quatro p&aacute;ginas de linha de neg&oacute;cio, nove p&aacute;ginas de destino com sa&iacute;das, pre&ccedil;o e parcelamento, formul&aacute;rio ligado ao cadastro de clientes e a prepara&ccedil;&atilde;o para aparecer na busca. Entrega em 4 a 7 semanas.', '<b>12.000</b>'),
  ('Site essencial', 'Uma landing page: p&aacute;gina &uacute;nica, sem menu e sem navega&ccedil;&atilde;o, com os quinze anos de opera&ccedil;&atilde;o, o CNPJ, os dois endere&ccedil;os f&iacute;sicos, o v&iacute;nculo com a ABAV-DF, as avalia&ccedil;&otilde;es do Google e o bot&atilde;o de WhatsApp. Resolve a prova de exist&ecirc;ncia e d&aacute; um destino ao bot&atilde;o Site da ficha do Google. Como n&atilde;o tem p&aacute;gina de destino, n&atilde;o disputa a busca.', '1.000'),
  ('Atendimento no WhatsApp', 'Libera&ccedil;&atilde;o da conta oficial, comprova&ccedil;&atilde;o da empresa junto &agrave; Meta, fluxo de primeira resposta, qualifica&ccedil;&atilde;o em quatro perguntas, transfer&ecirc;ncia para o atendente com a ficha preenchida, r&eacute;gua de p&oacute;s-venda e aprova&ccedil;&atilde;o dos textos padr&atilde;o.', '<b>7.500</b>'),
  ('Cadastro de clientes', 'Juntar os sete n&uacute;meros numa caixa s&oacute;, carregar os clientes j&aacute; atendidos, montar as etapas da venda e os campos de viagem, conectar Instagram e WhatsApp e treinar a equipe.', '<b>5.500</b>'),
  ('Google e reputa&ccedil;&atilde;o', 'Compra dos quatro endere&ccedil;os de site, tomada de posse da ficha do Google, corre&ccedil;&atilde;o dos cadastros p&uacute;blicos divergentes, verifica&ccedil;&atilde;o do perfil no Reclame Aqui e resposta &agrave;s cinco reclama&ccedil;&otilde;es abertas.', '<b>1.800</b>'),
  ('Rastreamento e automa&ccedil;&atilde;o', 'Links rastre&aacute;veis por destino, turma, escola e campanha, eventos de clique e conversa configurados, e o fluxo de mensagem direta por coment&aacute;rio.', '500'),
], 'Valores em reais, acrescidos de imposto. Fechando as cinco frentes juntas, a entrada sai por 22.900 em vez de 27.300.')}
''', 'Cada uma dessas frentes fica no nome da Sinfonya <span class="azul">e continua valendo se o contrato acabar.</span>')

# ============================================================ 8. SEO
pag('SEO', f'''
<h2 class="titulo">SEO e presen&ccedil;a no Google, o bloco mensal</h2>
<p class="lede">Testamos cinco buscas que correspondem ao que a Sinfonya vende e a marca n&atilde;o apareceu em
nenhuma. Quase todo concorrente que ocupa o topo dessas buscas tem site com p&aacute;gina do destino.</p>
{tabela(['O que entra todo m&ecirc;s', 'Detalhe'], [
  ('Uma p&aacute;gina de destino nova ou reescrita', 'Com sa&iacute;das do m&ecirc;s, pre&ccedil;o e parcelamento, que &eacute; o formato que disputa a busca'),
  ('Acompanhamento de posi&ccedil;&atilde;o', 'Nas buscas de excurs&atilde;o, formatura, ag&ecirc;ncia local e nos destinos vendidos'),
  ('Ficha do Google alimentada', 'Publica&ccedil;&otilde;es, fotos e hor&aacute;rios atualizados, mais resposta a todas as avalia&ccedil;&otilde;es novas'),
  ('Reclame Aqui acompanhado', 'Resposta dentro do prazo, para que a p&aacute;gina deixe de ser o segundo resultado da marca'),
  ('Relat&oacute;rio de onde a marca aparece', 'Posi&ccedil;&atilde;o por busca, evolu&ccedil;&atilde;o m&ecirc;s a m&ecirc;s e compara&ccedil;&atilde;o com os quatro concorrentes diretos'),
], compacta=True)}
{tabela(['Item', 'Valor'], [
  ('SEO e presen&ccedil;a no Google', '2.500 por m&ecirc;s'),
  ('Instala&ccedil;&atilde;o inicial', '1.800, uma vez, j&aacute; inclusa na entrada'),
], 'Valores em reais, acrescidos de imposto. O bloco de SEO pode ser contratado junto de qualquer um dos tr&ecirc;s planos mensais.', compacta=True)}
{nota('Por que SEO n&atilde;o est&aacute; dentro dos planos de redes',
 'S&atilde;o trabalhos com ritmo diferente. Rede social se mede por semana e SEO se mede por trimestre. '
 'Manter separado deixa vis&iacute;vel o que cada bloco entrega, e permite come&ccedil;ar por um s&oacute; se for a prefer&ecirc;ncia da Sinfonya.')}
''')

# ============================================================ 9. ADICIONAIS E TERCEIROS
pag('Adicionais', f'''
<h2 class="titulo">Servi&ccedil;os avulsos e o que &eacute; pago a terceiros</h2>
<p class="lede">Os itens da primeira tabela entram quando houver demanda. Os da segunda n&atilde;o passam pela
Or&aacute;culo: s&atilde;o pagos direto ao fornecedor, com relat&oacute;rio de aplica&ccedil;&atilde;o todo
m&ecirc;s.</p>
{tabela(['Servi&ccedil;o avulso', 'O que inclui', 'Valor'], [
  ('Produ&ccedil;&atilde;o extra de v&iacute;deos', 'Edi&ccedil;&atilde;o de Reel a partir do material bruto dos embarques, famtours, depoimentos e da viagem de formatura, em vers&otilde;es para feed, stories e TikTok.', '800 por pacote'),
  ('Capta&ccedil;&atilde;o presencial', 'Dia de grava&ccedil;&atilde;o com a equipe em Bras&iacute;lia, em embarques reais e durante a viagem de formatura, com banco de conte&uacute;do para 30 a 60 dias.', 'a combinar'),
  ('P&aacute;gina de destino extra', 'Al&eacute;m da p&aacute;gina mensal inclusa no bloco de SEO, quando a temporada pedir mais destinos de uma vez.', '900 por p&aacute;gina'),
], compacta=True)}
<h3 class="sub">Pago diretamente ao fornecedor</h3>
{tabela(['Item', 'Quanto'], [
  ('Verba de an&uacute;ncios, direto &agrave; plataforma', '1.500 a 3.000 por m&ecirc;s'),
  ('Ferramenta de cadastro de clientes', 'cerca de 320 por m&ecirc;s, para quatro atendentes'),
  ('Sistema de atendimento no WhatsApp', 'cerca de 350 por m&ecirc;s'),
  ('Mensagens do WhatsApp, lembrete e p&oacute;s-venda', 'R$ 0,04 a R$ 0,05 cada'),
  ('Mensagens do WhatsApp, campanha de oferta', 'R$ 0,31 a R$ 0,38 cada'),
  ('Hospedagem e e-mail no endere&ccedil;o pr&oacute;prio', 'cerca de 150 por m&ecirc;s'),
  ('Endere&ccedil;os de site, no Registro.br', 'cerca de 160 por ano, somados os quatro'),
], 'Resposta a quem chega, dentro das 24 horas seguintes &agrave; mensagem do cliente, n&atilde;o tem custo por mensagem. Faixas conforme tabelas p&uacute;blicas consultadas em 06/08/2026.', compacta=True)}
''')

# ============================================================ 10. METAS
pag('Metas', f'''
<h2 class="titulo">O que perseguimos nos primeiros 90 dias</h2>
<p class="lede">Todas as metas abaixo s&atilde;o de alcance, engajamento e qualifica&ccedil;&atilde;o de contato.
N&atilde;o prometemos n&uacute;mero de pacotes vendidos nem de turmas fechadas, porque o fechamento depende da
negocia&ccedil;&atilde;o comercial da Sinfonya com cada cliente.</p>
{tabela(['Indicador', 'Hoje', 'Meta em 90 dias'], [
  ('__grupo__', '@sinfonyaturismo'),
  ('Visualiza&ccedil;&otilde;es m&eacute;dias por Reel', '853', '4.000'),
  ('Taxa de engajamento', '0,026%', '0,300%'),
  ('Publica&ccedil;&otilde;es com localiza&ccedil;&atilde;o marcada', '2%', '100%'),
  ('__grupo__', '@sinfonyaformaturas'),
  ('Visualiza&ccedil;&otilde;es m&eacute;dias por Reel', '874', '9.614'),
  ('Taxa de engajamento', '0,107%', '0,700%'),
  ('Publica&ccedil;&otilde;es com chamada para a&ccedil;&atilde;o', '14%', '60%'),
  ('__grupo__', 'Grupo'),
  ('Conversas de WhatsApp com origem identificada', '0', '40 a 80 por m&ecirc;s'),
  ('Problemas de presen&ccedil;a digital resolvidos', '0 de 11', '11 de 11'),
  ('Buscas comerciais em que a marca aparece', '0 de 5', '2 de 5'),
], 'A meta de views por Reel da conta de formaturas &eacute; o patamar que o pr&oacute;prio perfil sustentou durante todo o ano de 2023.', alinha={1: 'num', 2: 'num'}, compacta=True)}
''', 'A meta de busca &eacute; conservadora de prop&oacute;sito: <span class="azul">p&aacute;gina nova leva de dois a tr&ecirc;s meses para ranquear.</span>')

# ============================================================ 11. CRONOGRAMA E CONDICOES
pag('Como come&ccedil;a', f'''
<h2 class="titulo">Como as seis frentes entram, e em que ordem</h2>
<p class="lede">A ordem &eacute; pelo que trava mais neg&oacute;cio com menos trabalho, e pelo que uma frente
exige da outra para funcionar. O ciclo desemboca na temporada de dezembro.</p>
{defs([
  ('Semana 1',
   'Compra dos quatro endere&ccedil;os de site, tomada de posse da ficha do Google, corre&ccedil;&atilde;o dos dois links quebrados do Linktree, '
   'contato na bio da conta crist&atilde;, troca do formul&aacute;rio do Google na conta de casamentos, cidade e endere&ccedil;o nas cinco contas e '
   'migra&ccedil;&atilde;o da conta de formaturas para conta de empresa.'),
  ('M&ecirc;s 1',
   'Perfil do Reclame Aqui verificado e as cinco reclama&ccedil;&otilde;es respondidas. Bios reescritas com os quinze anos de opera&ccedil;&atilde;o, o v&iacute;nculo com a ABAV-DF e a cidade de sa&iacute;da. '
   'Destaques reorganizados. Rastreamento instalado. Come&ccedil;a a constru&ccedil;&atilde;o do site.'),
  ('M&ecirc;s 2',
   'Site no ar com as p&aacute;ginas de destino. Cadastro de clientes implantado, com os sete n&uacute;meros unificados. Na conta de turismo o volume cai e a qualidade sobe, '
   'com Reel gravado no lugar do flyer animado. Na conta de formaturas volta a s&eacute;rie de contagem de vagas e entra uma creator.'),
  ('M&ecirc;s 3',
   'Atendimento autom&aacute;tico no WhatsApp ligado e conectado ao cadastro. Entrada do tr&aacute;fego pago, agora com site e rastreio prontos. '
   'Primeiro painel ligando publica&ccedil;&atilde;o, clique e conversa.'),
  ('Temporada, setembro a dezembro',
   'Cobertura da viagem de formatura em s&eacute;rie numerada, gerando o acervo que vende a turma seguinte. Na conta de turismo, os destinos vencedores dobram de frequ&ecirc;ncia '
   'e abrem as linhas de turismo religioso e corporativo.'),
])}
<h3 class="sub">Condi&ccedil;&otilde;es comerciais</h3>
<p class="texto">Contrato mensal, sem fidelidade no primeiro m&ecirc;s em qualquer um dos planos. Entrada
parcel&aacute;vel em at&eacute; doze vezes. Onboarding completo em 7 dias a partir da assinatura. A verba
de an&uacute;ncios e as mensalidades de ferramenta s&atilde;o pagas diretamente aos fornecedores. Valores em
reais, acrescidos de imposto. Esta proposta &eacute; v&aacute;lida por 30 dias a partir da data de envio.</p>
''')

# ============================================================ CONTRACAPA
paginas.append(f'''<section class="pagina fim">
<div class="capa-topo">
  <img src="data:image/png;base64,{LOGO}" alt="Or&aacute;culo">
  <div class="capa-meta">Pr&oacute;ximo passo<br>Reuni&atilde;o de alinhamento</div>
</div>
<div style="margin-top:auto">
  <h2>Uma conversa de 30 minutos para fechar o escopo</h2>
  <p class="fim-lede">O que precisa ser decidido antes de come&ccedil;ar: quais destinos entram nas primeiras
  p&aacute;ginas do site, quantos atendentes usam o cadastro de clientes, qual n&uacute;mero vira o WhatsApp
  oficial, quem grava o material em campo e quais destinos entram na primeira grade editorial.</p>
  <div class="fim-linhas">
    <div class="fim-linha"><b>Reuni&atilde;o</b><span>30 minutos, presencial em Bras&iacute;lia ou por v&iacute;deo</span></div>
    <div class="fim-linha"><b>Onboarding</b><span>7 dias, com as contas migradas e a primeira grade aprovada</span></div>
    <div class="fim-linha"><b>Entrada</b><span>22.900 reais, parcel&aacute;vel em at&eacute; 12 vezes de 1.908</span></div>
    <div class="fim-linha"><b>Mensal</b><span>6.900 reais, plano Crescimento mais o bloco de SEO</span></div>
  </div>
</div>
<div class="fim-rodape">
  <div><b>Or&aacute;culo Tecnologia</b>Baseado na auditoria de 348 publica&ccedil;&otilde;es<br>e na auditoria de presen&ccedil;a digital de 6 de agosto de 2026</div>
  <div>Documento confidencial, destinado ao Grupo Sinfonya<br>V&aacute;lido por 30 dias a partir do envio</div>
</div>
</section>''')

# ============================================================ MONTAGEM
html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Proposta Comercial, Grupo Sinfonya Turismo</title>
<meta name="description" content="Proposta comercial do Grupo Sinfonya Turismo: gestao de redes sociais, trafego pago, SEO, criacao de site, cadastro de clientes e atendimento no WhatsApp. Oraculo Tecnologia, agosto de 2026.">
<style>{FIRA}</style>
<style>{CSS}{EXTRA}</style>
</head>
<body>
{''.join(paginas)}
</body>
</html>'''

destino = os.path.join(RAIZ, 'SinfonyaGrupo', 'Proposta-Comercial.html')
open(destino, 'w', encoding='utf-8').write(html)
print(f'gerado: {destino}')
print(f'paginas: {len(paginas)}  |  tamanho: {len(html)/1024:.0f} KB')

# --------- validacao ---------
erros = []
corpo = re.sub(r'<style>.*?</style>', '', html, flags=re.S)
css_only = html.split('<style>')[-1].split('</style>')[0]
for termo in ['Joana', 'ladeguste', 'Elora', 'PECBR', 'Flavia Melow']:
    if termo.lower() in corpo.lower(): erros.append(f'residuo de outro cliente: {termo}')
if re.findall(r'<[^>]*[“”‘’][^>]*>', corpo): erros.append('aspas curvas dentro de tag')
if '&mdash;' in corpo or '—' in re.sub(r'<[^>]+>', ' ', corpo): erros.append('travessao encontrado')
if 'class="kpis"' in corpo: erros.append('KPI strip no corpo')
if [x for x in re.findall(r'border-left:\s*([\d.]+)pt', css_only) if float(x) > 0.76]:
    erros.append('border-left acima de 1px')
if html.count('<section') != html.count('</section>'): erros.append('section desbalanceada')
print('VALIDACAO:', 'ok, sem problemas' if not erros else erros)
