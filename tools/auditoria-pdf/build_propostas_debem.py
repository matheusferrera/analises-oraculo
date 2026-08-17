# -*- coding: utf-8 -*-
"""Propostas comerciais das tres frentes da Debem e Santos: o escritorio (unidade de
Brasilia), a marca pessoal do socio Diego Santos e a marca pessoal da advogada
Suziellen Aleixo. Mesmo formato editorial A4 da proposta do Grupo Sinfonya.

Cada documento e fechado em si e traz uma pagina com o valor combinado das tres frentes.
Todos os numeros citados vem das auditorias de presenca digital de 12 e 13/08/2026,
guardadas em <Pasta>/data/presenca-digital.json e <Pasta>/data/<handle>-scan.json.
"""
import base64, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_css import CSS

RAIZ = '/Users/touchbar/Codigos-Projetos/oraculo/analises-oraculo'
TMP = os.path.dirname(os.path.abspath(__file__))
FIRA = open(os.path.join(TMP, 'fira-embed.css')).read()
LOGO = base64.b64encode(open(os.path.join(RAIZ, 'logo.png'), 'rb').read()).decode()
DATA = '15 de agosto de 2026'

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
table.t tr.destaque td { background: #eef1fb; }
.na { color: var(--fraco); }
.sim { color: var(--azul); font-weight: 600; }
.duas { display: flex; gap: 9mm; }
.duas > div { flex: 1; }
.duas h4 { font-size: 8.4pt; font-weight: 700; color: var(--tinta); margin: 0 0 2.4mm;
  padding-bottom: 1.8mm; border-bottom: .9pt solid var(--reguaf); }
.duas ul { margin: 0; padding: 0; list-style: none; }
.duas li { font-size: 8pt; line-height: 1.5; color: var(--corpo);
  padding: 2.4mm 0; border-bottom: .5pt solid var(--regua); }
"""


# ---------------------------------------------------------------- helpers
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
        classe = ''
        if isinstance(l, tuple) and l and l[0] == '__total__':
            classe, l = 'total', l[1:]
        elif isinstance(l, tuple) and l and l[0] == '__destaque__':
            classe, l = 'destaque', l[1:]
        tds = ''
        for i, c in enumerate(l):
            k = []
            if i == 0: k.append('forte')
            if alinha.get(i) == 'num': k.append('num')
            cl = f' class="{" ".join(k)}"' if k else ''
            tds += f'<td{cl}>{c}</td>'
        tr += f'<tr class="{classe}">{tds}</tr>' if classe else f'<tr>{tds}</tr>'
    f = f'<p class="fonte">{fonte}</p>' if fonte else ''
    return f'<table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>{f}'


def defs(itens):
    return '<div class="defs">' + ''.join(
        f'<div class="def"><div class="def-r">{r}</div><div class="def-d">{t}</div></div>'
        for r, t in itens) + '</div>'


def nota(titulo, *ps):
    return f'<div class="nota"><b>{titulo}</b>{"".join(f"<p>{x}</p>" for x in ps)}</div>'


def duas_colunas(titulo_a, itens_a, titulo_b, itens_b):
    def col(t, itens):
        li = ''.join(f'<li>{x}</li>' for x in itens)
        return f'<div><h4>{t}</h4><ul>{li}</ul></div>'
    return f'<div class="duas">{col(titulo_a, itens_a)}{col(titulo_b, itens_b)}</div>'


def escopo(titulo, lede, blocos, fonte=None):
    linhas = ''
    for grupo, itens in blocos:
        linhas += f'<tr class="grupo"><td colspan="4">{grupo}</td></tr>'
        for rot, a, b, c in itens:
            def cel(x):
                if x == 'sim': return '<span class="sim">sim</span>'
                if x == 'nao': return '<span class="na">não incluído</span>'
                return x
            linhas += (f'<tr><td class="rot">{rot}</td>'
                       f'<td class="v">{cel(a)}</td><td class="v dest">{cel(b)}</td><td class="v">{cel(c)}</td></tr>')
    f = f'<p class="fonte">{fonte}</p>' if fonte else ''
    return (f'<h2 class="titulo">{titulo}</h2><p class="lede">{lede}</p>'
            f'<table class="planos esc"><thead><tr><th class="rot">Entrega</th>'
            f'<th class="col">Essencial</th><th class="col dest">Crescimento</th>'
            f'<th class="col">Autoridade</th></tr></thead><tbody>{linhas}</tbody></table>{f}')


class Doc:
    """Acumula as paginas de um documento e numera o rodape."""

    def __init__(self, cabecalho):
        self.cab = cabecalho
        self.paginas = []
        self.n = 0

    def bruta(self, html):
        self.paginas.append(html)

    def pag(self, secao, corpo, fecho=None):
        self.n += 1
        f = f'<div class="fecho">{fecho}</div>' if fecho else ''
        self.paginas.append(
            f'<section class="pagina">'
            f'<div class="cab"><span class="cab-esq">{self.cab} &middot; Oráculo Tecnologia</span>'
            f'<span class="cab-dir">{secao}</span></div>{corpo}{f}'
            f'<div class="rod"><span>Proposta comercial</span><span>{self.n}</span></div></section>')

    def capa(self, kicker, h1, lede, stats):
        s = ''.join(f'<div class="capa-stat"><b>{a}</b><span>{b}</span></div>' for a, b in stats)
        self.bruta(f'''<section class="pagina capa">
<div class="capa-topo">
  <img src="data:image/png;base64,{LOGO}" alt="Oráculo">
  <div class="capa-meta">Documento confidencial<br>{DATA}</div>
</div>
<div class="capa-corpo">
  <div class="capa-kicker">{kicker}</div>
  <h1>{h1}</h1>
  <p class="capa-lede">{lede}</p>
</div>
<div class="capa-rodape">{s}</div>
</section>''')

    def contracapa(self, h2, lede, linhas, rodape_esq):
        ls = ''.join(f'<div class="fim-linha"><b>{a}</b><span>{b}</span></div>' for a, b in linhas)
        self.bruta(f'''<section class="pagina fim">
<div class="capa-topo">
  <img src="data:image/png;base64,{LOGO}" alt="Oráculo">
  <div class="capa-meta">Próximo passo<br>Reunião de alinhamento</div>
</div>
<div style="margin-top:auto">
  <h2>{h2}</h2>
  <p class="fim-lede">{lede}</p>
  <div class="fim-linhas">{ls}</div>
</div>
<div class="fim-rodape">
  <div><b>Oráculo Tecnologia</b>{rodape_esq}</div>
  <div>Documento confidencial, destinado à Debem e Santos Advogados Associados<br>Válido por 30 dias a partir do envio</div>
</div>
</section>''')

    def salvar(self, destino, titulo, descricao):
        html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo}</title>
<meta name="description" content="{descricao}">
<style>{FIRA}</style>
<style>{CSS}{EXTRA}</style>
</head>
<body>
{''.join(self.paginas)}
</body>
</html>'''
        open(destino, 'w', encoding='utf-8').write(html)
        return html


# ---------------------------------------------------------------- blocos comuns
NOTA_OAB_CURTA = (
    'A publicidade da advocacia segue o Provimento 205/2021 do Conselho Federal da OAB. '
    'A página de publicidade e OAB lista o que a norma permite, o que ela veda e como isso '
    'muda o escopo.')

PAGINA_OAB_LEDE = (
    'A advocacia tem norma própria de publicidade. Todas as peças produzidas nesta proposta seguem o '
    'Provimento 205/2021 do Conselho Federal da OAB, que trata da publicidade e da informação na '
    'advocacia. A norma muda o que se pode dizer e o que se pode impulsionar, e por isso está escrita '
    'aqui, antes de qualquer produção.')

OAB_PERMITE = [
    'Conteúdo informativo sobre direito, procedimento, jurisprudência e direitos do cidadão.',
    'Divulgação de nome, número de inscrição na OAB, áreas de atuação, endereço, telefone e perfis.',
    'Impulsionamento pago de conteúdo informativo, com verba declarada e relatório de aplicação.',
    'Currículo, titulação, produção acadêmica, participação em evento e atuação institucional.',
    'Chamada para contato, sem oferta de serviço e sem condição comercial.',
]

OAB_VEDA = [
    'Valor de honorário, desconto, gratuidade, parcelamento ou permuta.',
    'Promessa de resultado, de prazo de êxito ou de concessão de benefício.',
    'Mensagem enviada a quem não pediu, e abordagem de pessoa envolvida em caso concreto.',
    'Citação de cliente ou de caso sem autorização expressa.',
    'Impulsionamento de peça que ofereça serviço ou que mercantilize a atividade.',
]

OAB_NOTA = nota(
    'O que isso muda na prática',
    'As chamadas para ação desta proposta são de informação e de contato, nunca de oferta. Os anúncios '
    'levam a conteúdo, não a orçamento. Nenhuma meta deste documento é de causas fechadas ou de receita, '
    'porque prometer resultado é vedado e porque o fechamento depende do atendimento do escritório.',
    'Cada peça passa por conferência com a norma antes de ir ao ar, com registro do que foi ajustado. '
    'A responsabilidade disciplinar permanece do advogado inscrito, e a conferência da Oráculo não a substitui.')

TERCEIROS_FONTE = ('Valores em reais. Faixas conforme tabelas públicas dos fornecedores, consultadas em '
                   '15/08/2026. Nenhum destes itens passa pela Oráculo.')

CONDICOES = (
    '<h3 class="sub">Condições comerciais</h3>'
    '<p class="texto">Contrato mensal, sem fidelidade no primeiro mês. A entrada é parcelável em até doze '
    'vezes. Onboarding completo em 7 dias a partir da assinatura. A verba de impulsionamento e as '
    'mensalidades de ferramenta são pagas diretamente aos fornecedores, com relatório de aplicação todo '
    'mês. Valores em reais, acrescidos de imposto. Esta proposta é válida por 30 dias a partir da data '
    'de envio.</p>')


def pagina_grupo(doc, destaque, debem=('11.100', '5.099'), diego=('6.100', '3.199'),
                 suziellen=('5.100', '3.199'), soma=('22.300', '11.497'), pacote=('20.300', '10.497'),
                 economia='2.000 na entrada e de 1.000 por mês, o que dá 12.000 no primeiro ano'):
    """Pagina do valor combinado das tres frentes. `destaque` marca a linha do cliente do documento."""
    linhas = []
    for chave, rot, ent, men in [
        ('debem', 'Debem e Santos, escritório e implantação da unidade de Brasília') + debem,
        ('diego', 'Diego Santos, marca pessoal do sócio') + diego,
        ('suziellen', 'Suziellen Aleixo, marca pessoal da advogada') + suziellen,
    ]:
        l = (rot, ent, men)
        linhas.append(('__destaque__',) + l if chave == destaque else l)
    linhas.append(('__total__', 'Contratando as três em separado') + soma)
    linhas.append(('__total__', 'As três no mesmo contrato', f'<b>{pacote[0]}</b>', f'<b>{pacote[1]}</b>'))

    doc.pag('As três frentes', f'''
<h2 class="titulo">As três frentes juntas, e por que elas se sustentam</h2>
<p class="lede">A Oráculo auditou o escritório e os dois advogados separadamente, em 12 e 13 de agosto de
2026. Os três documentos apontam para o mesmo lugar. A linha destacada abaixo é a frente tratada nesta
proposta; as outras duas estão aqui para que a decisão seja tomada com o quadro inteiro à vista.</p>
{tabela(['Frente', 'Entrada', 'Mensal'], linhas,
        'Valores em reais, acrescidos de imposto. O mensal de cada frente é o do próprio documento: '
        'plano Crescimento na Debem e Santos, e o nível de entrada nas duas marcas pessoais. '
        f'Contratando as três, a economia é de {economia}.',
        alinha={1: 'num', 2: 'num'}, compacta=True)}
<h3 class="sub">O que a auditoria mostrou sobre a relação entre elas</h3>
<p class="texto">As três publicações de melhor desempenho do perfil do escritório em 2026 são
colaborações assinadas em conjunto com o perfil pessoal de Diego Santos, que tem audiência 1,5 vez maior.
Somadas, essas três publicações reuniram 810 interações. Excluindo as colaborações, o engajamento do
perfil do escritório cai de 4,72% para 1,61%. O alcance do escritório hoje depende do perfil pessoal do
sócio, e o perfil do sócio não tem nenhum caminho de contato.</p>
<p class="texto">Do outro lado, a unidade de Brasília foi anunciada em agosto de 2026 e coassinada por
Suziellen Aleixo, o único nome do escritório com sinais públicos de residência na praça. Se a premissa se
confirmar, a marca pessoal dela é o ativo humano da unidade nova, e o custo de construir essa presença
cai quando as duas frentes andam juntas.</p>
{nota('Se a preferência for começar por uma só',
      'A ordem recomendada é escritório, depois Diego Santos, depois Suziellen Aleixo. A implantação '
      'digital da unidade de Brasília é a única frente com prazo externo: quanto mais tarde o Perfil da '
      'Empresa for aberto, mais tarde começa a contagem de reputação local, que hoje está em zero contra '
      '47, 313 e 1.371 avaliações dos três vizinhos medidos na Asa Sul.')}
''', 'A auditoria das três frentes já foi feita. <span class="azul">A execução é que ainda não começou.</span>')


def pagina_oab(doc, sujeito):
    doc.pag('Publicidade e OAB', f'''
<h2 class="titulo">O que a norma da OAB permite, e o que ela veda</h2>
<p class="lede">{PAGINA_OAB_LEDE}</p>
{duas_colunas('A norma permite', OAB_PERMITE, 'A norma veda', OAB_VEDA)}
{OAB_NOTA}
<p class="fonte">Provimento 205/2021 do Conselho Federal da OAB, que dispõe sobre publicidade,
publicidade profissional e informação na advocacia, combinado com o Código de Ética e Disciplina da OAB.
Leitura aplicada ao caso de {sujeito}, sem caráter de parecer jurídico.</p>
''', 'Anúncio de advogado leva a informação. <span class="azul">Nenhuma peça desta proposta oferece serviço ou preço.</span>')


# ================================================================ 1. DEBEM E SANTOS
def planos_com_escopo(titulo, lede, precos, blocos, fonte=None, rotulo_preco='Investimento mensal'):
    """Tabela de tres niveis com a linha de preco no topo e o escopo logo abaixo."""
    a, b, c = precos
    linhas = (f'<tr><td class="rot">{rotulo_preco}</td>'
              f'<td class="v"><span class="preco">{a}</span><span class="un">reais por mês</span></td>'
              f'<td class="v dest"><span class="preco az">{b}</span><span class="un">reais por mês</span></td>'
              f'<td class="v"><span class="preco">{c}</span><span class="un">reais por mês</span></td></tr>')
    for grupo, itens in blocos:
        linhas += f'<tr class="grupo"><td colspan="4">{grupo}</td></tr>'
        for rot, x, y, z in itens:
            def cel(v):
                if v == 'sim': return '<span class="sim">sim</span>'
                if v == 'nao': return '<span class="na">não incluído</span>'
                return v
            linhas += (f'<tr><td class="rot">{rot}</td>'
                       f'<td class="v">{cel(x)}</td><td class="v dest">{cel(y)}</td>'
                       f'<td class="v">{cel(z)}</td></tr>')
    f = f'<p class="fonte">{fonte}</p>' if fonte else ''
    return (f'<h2 class="titulo">{titulo}</h2><p class="lede">{lede}</p>'
            f'<table class="planos esc"><thead><tr><th class="rot"></th>'
            f'<th class="col">Essencial</th>'
            f'<th class="col dest"><span class="rec">Recomendado</span>Crescimento</th>'
            f'<th class="col">Autoridade</th></tr></thead><tbody>{linhas}</tbody></table>{f}')


def build_debem():
    d = Doc('Debem e Santos Advogados Associados')

    d.capa(
        'Debem e Santos Advogados Associados',
        'Proposta comercial: tecnologia, gestão de redes sociais e tráfego pago',
        'A auditoria de presença digital de 12 de agosto de 2026 avaliou a marca em 3,7 de 10 e listou '
        'treze pontos de correção. Esta proposta organiza a resposta em três vertentes, cada uma com escopo '
        'e preço próprios, contratáveis juntas ou separadamente.',
        [('3', 'vertentes contratáveis'), ('13', 'pontos de correção apontados'),
         ('11.100', 'reais de entrada, uma vez'), ('5.099', 'reais por mês')])

    # --- 1. diagnostico
    d.pag('Diagnóstico', f'''
<h2 class="titulo">Os treze pontos que a auditoria encontrou</h2>
<p class="lede">Tudo abaixo foi apurado direto nos canais públicos do escritório, em 12 de agosto de 2026.
A última coluna mostra qual das três vertentes resolve cada ponto, e é ela que organiza esta proposta.</p>
{tabela(['Ponto de correção', 'O que isso custa', 'Vertente'], [
  ('Não existe Perfil da Empresa da unidade de Brasília', 'A busca de marca devolve a ficha de Palhoça', 'Tecnologia'),
  ('O site não tem página da unidade da Asa Sul', 'Quem chega pelo anúncio não acha endereço nem equipe', 'Tecnologia'),
  ('A home não tem nenhum H1', 'O Google não recebe o assunto da página', 'Tecnologia'),
  ('A home não tem meta description, Open Graph nem JSON-LD', 'O escritório não controla como aparece na busca e perde o resultado enriquecido', 'Tecnologia'),
  ('O HTML declara idioma pt-PT', 'Sinal de localização errado para busca no Brasil', 'Tecnologia'),
  ('Cinco páginas genéricas indexáveis, entre elas “Hello world!”', 'Metade do que o site publica não é do escritório', 'Tecnologia'),
  ('Três grafias de endereço e quatro telefones publicados', 'Cadastro divergente é sinal fraco de existência', 'Tecnologia'),
  ('Reputação local de Brasília em zero avaliação', 'Sem ficha própria não há onde receber avaliação', 'Tecnologia'),
  ('Dois hiatos de publicação no Instagram, de 151 e 74 dias', 'A conta recomeça o alcance a cada retomada', 'Redes sociais'),
  ('Doze das 18 publicações recentes são imagem estática', 'O formato entrega 0,74% contra 4,35% do Reel', 'Redes sociais'),
  ('Três chamadas para ação em 18 publicações', 'Quem se interessa não é levado a lugar nenhum', 'Redes sociais'),
  ('A unidade nova não alcança quem ainda não segue a marca', 'O anúncio da expansão só chegou a quem já seguia', 'Tráfego pago'),
  ('Os 1.919 seguidores foram construídos em Santa Catarina', 'O conteúdo de Brasília nasce falando para a praça errada', 'Tráfego pago'),
], 'Auditoria de presença digital da Debem e Santos, coleta de 12/08/2026: Google Search e painel público '
   'da empresa, debemesantos.com.br, robots.txt e wp-sitemap.xml, Instagram @debemesantos e sites públicos '
   'dos concorrentes da Asa Sul.', compacta=True)}
<h3 class="sub">O que já funciona</h3>
<p class="texto">A ficha de Palhoça tem nota 5,0 com 22 avaliações, o site responde o primeiro byte em
0,19 segundo e o Instagram tem categoria jurídica declarada, link para o site e seis destaques
organizados. A marca chega a Brasília com vinte anos de operação declarados. Nada disso precisa ser
refeito.</p>
''', 'A marca chegou a Brasília. <span class="azul">A presença local ainda não.</span>')

    # --- 2. as tres vertentes
    d.pag('As três vertentes', f'''
<h2 class="titulo">Três vertentes, três contratos possíveis</h2>
<p class="lede">Cada vertente tem entrada e mensal próprios e pode ser contratada sozinha. Elas foram
separadas por natureza de trabalho: a primeira constrói ativos, a segunda produz conteúdo e a terceira
compra alcance para o que as duas anteriores criaram.</p>
{defs([
  ('1. Tecnologia',
   'Um site profissional para os três escritórios, a ficha do Google da unidade nova, o atendimento no '
   'WhatsApp e a medição que liga tudo. Resolve oito dos treze pontos da auditoria e é o que fica no nome '
   'do escritório mesmo que o contrato acabe.'),
  ('2. Gestão de redes sociais',
   'Sistema de design próprio e produção mensal de conteúdo para o perfil @debemesantos, com grade aprovada, '
   'série técnica por área de atuação e recorte declarado de Brasília. Fecha os hiatos de 151 e 74 dias, e é '
   'a única vertente sem valor de entrada.'),
  ('3. Tráfego pago',
   'Impulsionamento de conteúdo informativo no Meta Ads, dentro da norma da OAB, para alcançar quem ainda '
   'não segue a marca na Asa Sul. A busca do Google entra a partir do nível Crescimento. Depende da '
   'medição instalada na vertente 1 para poder ser conferido.'),
])}
{tabela(['Vertente', 'Entrada', 'Mensal'], [
  ('1. Tecnologia', '11.000', '600'),
  ('2. Gestão de redes sociais', '<span class="na">sem entrada</span>', '3.199'),
  ('3. Tráfego pago', '1.400', '2.000'),
  ('__total__', 'Contratando as três em separado', '12.400', '5.799'),
  ('__total__', 'As três no mesmo contrato', '<b>11.100</b>', '<b>5.099</b>'),
], 'Valores em reais, acrescidos de imposto. O mensal considerado nas vertentes 2 e 3 é o plano '
   'Crescimento; os três níveis estão nas páginas 6 e 8. A entrada pode ser parcelada em até doze vezes, '
   'o que dá 925 reais por mês no contrato das três. A verba de anúncios é paga direto à plataforma e '
   'não está somada aqui.', alinha={1: 'num', 2: 'num'}, compacta=True)}
<h3 class="sub">Contratando duas das três</h3>
{tabela(['Combinação', 'Entrada', 'Mensal'], [
  ('Tecnologia e redes sociais', '10.500', '3.499'),
  ('Tecnologia e tráfego pago', '11.700', '2.400'),
  ('Redes sociais e tráfego pago', '1.400', '4.799'),
], 'Tráfego pago sem a vertente de tecnologia funciona, mas o resultado passa a ser medido apenas dentro '
   'da plataforma de anúncios, sem ligação com o site e com a conversa no WhatsApp.',
   alinha={1: 'num', 2: 'num'}, compacta=True)}
''', 'A ordem que protege o investimento é tecnologia, depois conteúdo, <span class="azul">e só então anúncio.</span>')

    # --- 3 e 4. tecnologia, duas paginas amarradas pela mesma tabela de resumo
    resumo_tec = tabela(['O investimento da vertente 1', 'Valor'], [
      ('Pagamento único, a construção', '11.000'),
      ('Mensal, a sustentação', '600'),
    ], 'Valores em reais, acrescidos de imposto. O pagamento único pode ser parcelado em até doze vezes. '
       'No contrato das três vertentes, a entrada somada cai de 12.400 para 11.100.',
       alinha={1: 'num'}, compacta=True)

    d.pag('Tecnologia, construção', f'''
<h2 class="titulo">Vertente 1: Tecnologia</h2>
<p class="lede">Esta vertente tem duas partes. Esta página trata da primeira: o que é pago uma vez e
constrói os ativos que hoje não existem. A página seguinte trata do mensal que os mantém funcionando.</p>
{resumo_tec}
<h3 class="sub">Pagamento único, a construção</h3>
{tabela(['Obra', 'O que inclui', 'Valor'], [
  ('Site profissional', 'Um site profissional único para os três escritórios, com página própria de cada unidade, página por área de atuação, página de equipe com os advogados e formulário ligado ao WhatsApp. Home com H1, meta description, Open Graph e JSON-LD de escritório de advocacia. Idioma corrigido para pt-BR e remoção das cinco páginas genéricas indexáveis. Entrega em 4 a 6 semanas.', '<b>3.500</b>'),
  ('Atendimento no WhatsApp', 'Liberação da conta oficial, comprovação do escritório junto à Meta, primeira resposta automática, triagem por área e por unidade, transferência para o advogado com a ficha preenchida e aprovação dos textos padrão.', '<b>3.200</b>'),
  ('Unidade de Brasília', 'Abertura e verificação do Perfil da Empresa da Asa Sul, escolha da categoria principal e das secundárias, fotos, horários, área de atendimento, telefone local próprio e cadastro nos diretórios que aparecem na busca da praça.', '<b>2.000</b>'),
  ('Base técnica e medição', 'Google Analytics, Search Console, eventos de clique e de conversa, sitemap revisado e painel único ligando busca, site, perfil e WhatsApp. É o que permite conferir as outras duas vertentes.', '<b>1.400</b>'),
  ('Endereço e telefones', 'Padronização das três grafias de endereço e definição de um telefone público por unidade, aplicada no site, no Google, no Instagram e nos diretórios.', '<b>900</b>'),
  ('__total__', 'Pagamento único', '', '<b>11.000</b>'),
], 'Os defeitos de site citados acima foram verificados em 12/08/2026 no HTML público de '
   'debemesantos.com.br. O site é único e atende os três escritórios no mesmo domínio, com uma página '
   'própria por unidade: é isso que resolve o ponto mais caro da auditoria, que é a busca pela marca em '
   'Brasília devolver a ficha e o endereço de Palhoça.')}
''', 'Oito dos treze pontos da auditoria <span class="azul">se resolvem nesta construção.</span>')

    d.pag('Tecnologia, mensal', f'''
<h2 class="titulo">Vertente 1: Tecnologia</h2>
<p class="lede">Esta é a segunda parte da vertente. Depois de construídos, o site e o atendimento no
WhatsApp precisam de manutenção para continuar funcionando. É só isso que o mensal cobre, e por isso ele
é baixo.</p>
{resumo_tec}
<h3 class="sub">Mensal, a sustentação</h3>
{tabela(['O que entra todo mês', 'Detalhe', 'Valor'], [
  ('Suporte do site', 'Atualizações de sistema, cópia de segurança, correção de erro, ajuste de conteúdo institucional e acompanhamento de disponibilidade', ''),
  ('Suporte do CRM do WhatsApp', 'Ajuste da triagem e dos textos padrão, correção do encaminhamento por unidade, acompanhamento da fila de atendimento e apoio à equipe no uso', ''),
  ('__total__', 'Mensal', '', '<b>600</b>'),
], 'Não há três níveis nesta vertente: o escopo é fechado e o volume não varia por plano.', compacta=True)}
<h3 class="sub">Pago diretamente ao fornecedor</h3>
{tabela(['Item', 'Quanto'], [
  ('Sistema de atendimento no WhatsApp', '500 por mês'),
  ('Hospedagem e e-mail no domínio próprio', 'cerca de 150 por mês'),
  ('Registro do domínio no Registro.br', 'cerca de 40 por ano'),
], TERCEIROS_FONTE, compacta=True)}
{nota('O que este mensal não cobre',
      'Produção de página nova, alimentação da ficha do Google, resposta a avaliação e acompanhamento de '
      'posição na busca não estão neste valor. São trabalhos de conteúdo e de busca, com ritmo próprio, e '
      'podem ser contratados à parte. ' + NOTA_OAB_CURTA)}
''', 'O que foi construído fica no nome do escritório <span class="azul">e continua valendo se o contrato acabar.</span>')

    # --- 5, 6 e 7. redes sociais: sem pagamento unico, tudo dentro dos planos
    d.pag('Redes sociais, primeiro mês', f'''
<h2 class="titulo">Vertente 2: Gestão de redes sociais</h2>
<p class="lede">Antes da primeira publicação, o perfil precisa ser organizado. Esse trabalho é feito no
primeiro mês, sem pagamento separado. A última coluna mostra a partir de qual nível cada entrega
entra.</p>
{tabela(['Entrega do primeiro mês', 'O que inclui', 'A partir de'], [
  ('Organização do perfil', 'Bio reescrita com as áreas de atuação e as unidades, categoria profissional revisada, dados de contato, endereço e telefone corretos e link do site conferido', 'Essencial'),
  ('Destaques reorganizados', 'Os seis destaques atuais reordenados por área de atuação e por unidade, com capas padronizadas', 'Essencial'),
  ('Arquitetura de conteúdo', 'Linhas editoriais definidas por área de atuação e por unidade, com a primeira grade editorial aprovada pelo escritório', 'Essencial'),
  ('Sistema de design para o Instagram', 'Paleta, tipografia, grade de capas e modelos prontos de post, de carrossel e de story, para que toda peça futura saia no mesmo padrão visual e o perfil seja reconhecível na rolagem', '<b>Crescimento</b>'),
  ('Arquivos editáveis entregues', 'Os modelos do sistema de design ficam com o escritório e continuam valendo se o contrato acabar', '<b>Crescimento</b>'),
], 'A organização é feita uma vez e não se repete a cada mês. É ela que evita que o perfil volte ao estado '
   'apurado na auditoria de 12/08/2026, com dois hiatos de 151 e 74 dias e sem padrão visual entre as '
   'publicações. No nível Essencial as peças seguem um modelo básico: o sistema de design próprio e a '
   'entrega dos arquivos editáveis entram a partir do nível Crescimento.')}
{nota('Esta vertente não tem pagamento de entrada',
      'Diferente da vertente de tecnologia, aqui não há valor pago à parte. A organização entra no '
      'primeiro mês do plano escolhido, e o escritório passa a pagar apenas a mensalidade a partir daí.')}
''', 'O sistema de design é o que faz <span class="azul">doze publicações por mês parecerem do mesmo escritório.</span>')

    d.pag('Redes sociais, planos', f'''
<h2 class="titulo">Vertente 2: Gestão de redes sociais</h2>
<p class="lede">A vertente é toda mensal, em três níveis. O que separa um nível do outro é o volume
publicado por mês. Não há valor de entrada.</p>
<table class="planos">
<thead><tr><th class="rot"></th>
<th class="col">Essencial</th>
<th class="col dest"><span class="rec">Recomendado</span>Crescimento</th>
<th class="col">Autoridade</th></tr></thead>
<tbody>
<tr><td class="rot">Investimento mensal</td>
  <td class="v"><span class="preco">1.999</span><span class="un">reais por mês</span></td>
  <td class="v dest"><span class="preco az">3.199</span><span class="un">reais por mês</span></td>
  <td class="v"><span class="preco">4.999</span><span class="un">reais por mês</span></td></tr>
<tr><td class="rot">Publicações de feed por mês</td>
  <td class="v">6</td><td class="v dest">12</td><td class="v">18</td></tr>
<tr><td class="rot">Stories por mês</td>
  <td class="v">10</td><td class="v dest">20</td><td class="v">30</td></tr>
<tr><td class="rot">Reels editados por mês</td>
  <td class="v">2</td><td class="v dest">4</td><td class="v">8</td></tr>
<tr class="grupo"><td colspan="4">Feito no primeiro mês, sem custo separado</td></tr>
<tr><td class="rot">Organização do perfil e reescrita da bio</td>
  <td class="v"><span class="sim">sim</span></td><td class="v dest"><span class="sim">sim</span></td><td class="v"><span class="sim">sim</span></td></tr>
<tr><td class="rot">Sistema de design para o Instagram</td>
  <td class="v"><span class="na">não incluído</span></td><td class="v dest"><span class="sim">sim</span></td><td class="v"><span class="sim">sim</span></td></tr>
<tr><td class="rot">Destaques reorganizados por área e por unidade</td>
  <td class="v"><span class="sim">sim</span></td><td class="v dest"><span class="sim">sim</span></td><td class="v"><span class="sim">sim</span></td></tr>
<tr><td class="rot">Arquivos editáveis entregues ao escritório</td>
  <td class="v"><span class="na">não incluído</span></td><td class="v dest"><span class="sim">sim</span></td><td class="v"><span class="sim">sim</span></td></tr>
</tbody></table>
<p class="fonte">Valores em reais, acrescidos de imposto. Sem fidelidade no primeiro mês em qualquer um dos
planos. O escopo completo de cada nível está na página seguinte.</p>
{nota('Como o volume é contado',
      'Publicação de feed é um post publicado no perfil, seja imagem única ou carrossel, com quantas telas '
      'o assunto pedir. Story é contado por tela. Reel editado é montado a partir do material gravado pela '
      'equipe do escritório.',
      'A divisão exata entre os formatos é definida na grade editorial aprovada todo mês, e pode variar '
      'sem mudar o total contratado.')}
<h3 class="sub">Por que o plano Crescimento é o indicado</h3>
<p class="texto">O ritmo atual do perfil é de 1,9 publicação por mês, apurado sobre 18 publicações entre
22/10/2025 e 11/08/2026, com dois hiatos de 151 e 74 dias. Doze publicações de feed por mês é o menor
volume que fecha esses hiatos e ainda comporta uma série técnica por área de atuação.</p>
''')

    d.pag('Redes sociais, escopo', escopo(
        'Vertente 2: o que entra em cada nível',
        'Os volumes são totais mensais do perfil @debemesantos. A grade editorial de cada mês é aprovada '
        'antecipadamente pelo escritório.',
        [('Produção', [
            ('Publicações de feed por mês', '6', '12', '18'),
            ('Stories por mês', '10', '20', '30'),
            ('Reels editados a partir do material enviado', '2', '4', '8'),
            ('Roteiro do vídeo, com o que gravar e como', 'nao', 'sim', 'sim'),
            ('Série técnica por área de atuação', 'nao', '1 por mês', '2 por mês'),
            ('Peça com recorte declarado de Brasília', '2 por mês', '4 por mês', '8 por mês'),
          ]),
         ('Estrutura e direção', [
            ('Gestão do perfil com calendário aprovado', 'sim', 'sim', 'sim'),
            ('Legenda, hashtag e localização em toda publicação', 'sim', 'sim', 'sim'),
            ('Sistema de design próprio e arquivos editáveis', 'nao', 'sim', 'sim'),
            ('Destaques mantidos por área e por unidade', 'sim', 'sim', 'sim'),
            ('Conferência de cada peça com o Provimento 205/2021', 'sim', 'sim', 'sim'),
            ('Gestão dos perfis pessoais dos sócios', 'nao', 'nao', 'sim'),
          ]),
         ('Acompanhamento', [
            ('Relatório mensal do perfil', 'sim', 'sim', 'sim'),
            ('Relatório de origem das conversas de WhatsApp', 'nao', 'sim', 'sim'),
            ('Reunião estratégica', 'nao', 'mensal', 'quinzenal'),
          ])]) + f'''
{nota('Captação de foto e de vídeo não está incluída',
      'Nenhum dos três planos inclui fotógrafo ou cinegrafista. O mensal cobre roteiro, edição, legenda, '
      'capa e publicação a partir do material gravado pela própria equipe do escritório. Quando houver '
      'necessidade de captação profissional, a Oráculo indica e coordena o fornecedor, e o serviço é '
      'orçado e pago diretamente a ele.')}
''')

    # --- 7. trafego pago
    d.pag('Tráfego pago', planos_com_escopo(
        'Vertente 3: impulsionamento de conteúdo informativo',
        'Esta vertente compra alcance para quem ainda não segue a marca na Asa Sul. A entrada de 1.400 '
        'reais é paga uma vez e cobre a abertura e a verificação do Gerenciador de Negócios, o pixel e a '
        'API de conversões, os públicos por unidade e por área e a estrutura inicial de campanhas.',
        ('1.200', '2.000', '2.900'),
        [('Plataformas', [
            ('Meta Ads, no Instagram e no Facebook', 'sim', 'sim', 'sim'),
            ('Google Ads, na busca', 'nao', 'sim', 'sim'),
          ]),
         ('Campanhas', [
            ('Campanhas ativas ao mesmo tempo', 'até 2', 'até 4', 'até 8'),
            ('Criativos informativos produzidos por mês', '4', '8', '14'),
            ('Otimização e ajuste de campanha', 'semanal', '2 vezes por semana', 'contínua'),
            ('Públicos por unidade e por área de atuação', 'nao', 'sim', 'sim'),
            ('Teste de público e de página de destino', 'nao', 'nao', 'sim'),
          ]),
         ('Conformidade com a norma da OAB', [
            ('Conferência de cada peça com o Provimento 205/2021', 'sim', 'sim', 'sim'),
            ('Registro do que foi ajustado em cada peça', 'sim', 'sim', 'sim'),
          ]),
         ('Medição', [
            ('Relatório de aplicação da verba', 'sim', 'sim', 'sim'),
            ('Relatório de origem das conversas', 'nao', 'sim', 'sim'),
            ('Reunião de leitura de campanha', 'nao', 'mensal', 'quinzenal'),
          ]),
         ('Verba de anúncios, paga direto à plataforma', [
            ('Faixa recomendada por mês, somando as plataformas', '800 a 1.200', '1.500 a 3.000', 'a definir'),
          ])],
        'Valores em reais, acrescidos de imposto. A verba de anúncios não passa pela Oráculo: é paga '
        'diretamente à plataforma, com relatório de aplicação todo mês. Faixas conforme tabelas públicas '
        'consultadas em 15/08/2026. O anúncio de busca segue a mesma regra do impulsionamento: leva a '
        'conteúdo informativo ou à página institucional, nunca a oferta de serviço ou a condição comercial.'))

    pagina_oab(d, 'um escritório com quatro unidades declaradas')

    # --- 9. metas
    d.pag('Metas', f'''
<h2 class="titulo">O que perseguimos nos primeiros 90 dias</h2>
<p class="lede">As metas estão separadas por vertente, para que cada contrato possa ser cobrado pelo que
entrega. Não há meta de causas fechadas nem de receita: promessa de resultado é vedada pela norma da OAB, e
o fechamento depende do atendimento do escritório.</p>
{tabela(['Indicador', 'Hoje', 'Meta em 90 dias'], [
  ('__grupo__', 'Vertente 1, tecnologia'),
  ('Perfil da Empresa da Asa Sul', 'não existe', 'verificado e completo'),
  ('Defeitos técnicos abertos na home', '6 de 6', '0 de 6'),
  ('Páginas do site que citam Brasília', '0', '4'),
  ('Telefones públicos sem padrão', '4', '1 por unidade'),
  ('Medição instalada', 'nenhuma', 'Analytics, Search Console e eventos'),
  ('__grupo__', 'Vertente 2, redes sociais'),
  ('Publicações por mês', '1,9', '12'),
  ('Maior intervalo sem publicar', '151 dias', 'nenhum acima de 14 dias'),
  ('Taxa de engajamento', '1,45%', '2,50%'),
  ('__grupo__', 'Vertente 3, tráfego pago'),
  ('Pessoas alcançadas fora da base de seguidores', '0', '20.000 a 40.000 por mês'),
  ('Conversas com origem identificada', '0', '25 a 50 por mês'),
], 'Situação atual apurada na auditoria de 12/08/2026. O ritmo de 1,9 publicação por mês vem da amostra de '
   '18 posts entre 22/10/2025 e 11/08/2026. A meta de engajamento de 2,50% é conservadora e fica abaixo dos '
   '4,35% que o próprio perfil já obtém no formato Reel. A meta de alcance pago considera a faixa de verba '
   'do plano Crescimento.', alinha={1: 'num', 2: 'num'}, compacta=True)}
''', 'A meta de busca local é curta de propósito: <span class="azul">ficha nova leva de dois a três meses para firmar posição.</span>')

    # --- 10. cronograma
    d.pag('Como começa', f'''
<h2 class="titulo">Como as três vertentes entram, e em que ordem</h2>
<p class="lede">A tecnologia vem primeiro por dois motivos: é a única vertente com prazo externo, porque a
contagem de reputação local só começa depois que a ficha existe, e é ela que instala a medição sem a qual
as outras duas não podem ser conferidas.</p>
{defs([
  ('Semana 1, vertente 1',
   'Abertura do Perfil da Empresa da Asa Sul e envio para verificação. Contratação do telefone local. '
   'Padronização das três grafias de endereço nos quatro canais. Correção do idioma do site para pt-BR e '
   'remoção das cinco páginas genéricas indexáveis.'),
  ('Mês 1, vertentes 1 e 2',
   'Página da unidade de Brasília no ar, com endereço, telefone, advogados responsáveis e áreas '
   'prioritárias. Analytics e Search Console instalados. Perfil preparado e primeira grade editorial '
   'aprovada, com recorte declarado de Brasília.'),
  ('Mês 2, vertentes 1 e 2',
   'Site profissional no ar, com página própria de cada um dos três escritórios e página por área de '
   'atuação. Atendimento no WhatsApp funcionando, com triagem por área e por unidade. Cadência de doze '
   'publicações estabilizada no perfil.'),
  ('Mês 3, vertente 3',
   'Tráfego pago entra agora, com a medição pronta e com um acervo de peças orgânicas já testado. As '
   'campanhas sobem sobre o conteúdo que teve melhor desempenho sem verba.'),
  ('Meses 4 a 6, as três',
   'Site e atendimento em manutenção, cadência mantida no perfil e campanhas otimizadas contra o '
   'relatório de origem das conversas.'),
])}
{CONDICOES}
''')

    pagina_grupo(d, 'debem')

    d.contracapa(
        'Uma conversa de 30 minutos para fechar o escopo',
        'O que precisa ser decidido antes de começar: quais vertentes entram e em que ordem, quais '
        'advogados respondem pela unidade de Brasília, qual telefone vira o público de cada unidade, quais '
        'áreas de atuação entram nas primeiras páginas do site e quem aprova a grade editorial.',
        [('Reunião', '30 minutos, presencial em Brasília ou por vídeo'),
         ('Onboarding', '7 dias, com a ficha de Brasília enviada para verificação'),
         ('Entrada', '11.100 reais pelas três vertentes, parcelável em até 12 vezes de 925'),
         ('Mensal', '5.099 reais pelas três, com os planos Crescimento nas vertentes 2 e 3')],
        'Baseado na auditoria de presença digital<br>da Debem e Santos, de 12 de agosto de 2026')

    return d.salvar(
        os.path.join(RAIZ, 'DebemSantos', 'Proposta-Comercial.html'),
        'Proposta Comercial, Debem e Santos Advogados Associados',
        'Proposta comercial da Debem e Santos em três vertentes: tecnologia (site, Google, WhatsApp e '
        'medição), gestão de redes sociais e tráfego pago. Oráculo Tecnologia, agosto de 2026.')


# ================================================================ 2. DIEGO SANTOS
def build_diego():
    d = Doc('Diego Santos, advogado')

    d.capa(
        'Diego Santos, advogado',
        'Proposta comercial: tecnologia, gestão de redes sociais e tráfego pago',
        'A auditoria de 13 de agosto de 2026 percorreu as 113 publicações do perfil, a busca pelo nome, o '
        'site do escritório e os diretórios jurídicos. Esta proposta organiza a resposta em três vertentes, '
        'cada uma com escopo e preço próprios, contratáveis juntas ou separadamente.',
        [('3', 'vertentes contratáveis'), ('3,89%', 'de engajamento em 2026'),
         ('6.100', 'reais de entrada, uma vez'), ('3.199', 'reais por mês, a partir de')])

    # --- 1. diagnostico
    d.pag('Diagnóstico', f'''
<h2 class="titulo">O que a auditoria encontrou</h2>
<p class="lede">O histórico integral do perfil foi coletado em 13 de agosto de 2026, com 113 publicações
entre 2015 e 2026, junto com a busca pelo nome, os diretórios jurídicos e o site do escritório. A última
coluna mostra qual das três vertentes resolve cada achado.</p>
{tabela(['Achado', 'O que isso custa', 'Vertente'], [
  ('Seis advogados homônimos na primeira página da busca pelo nome', 'O nome não pertence a ele no Google', 'Tecnologia'),
  ('Três grafias em circulação, sem nenhum ativo que as conecte', 'Quem procura por uma grafia não chega às outras', 'Tecnologia'),
  ('Nenhum perfil no Jusbrasil, Escavador, LinkedIn ou Previdenciarista', 'Fica fora dos diretórios que ocupam o topo da busca', 'Tecnologia'),
  ('O nome não aparece em nenhuma das cinco páginas do site do escritório', 'O sócio não existe no domínio do próprio escritório', 'Tecnologia'),
  ('Nenhum link na bio, nenhum botão de contato e nenhum WhatsApp', 'Quem se interessa não tem para onde ir', 'Redes sociais'),
  ('Duas chamadas para ação em 113 publicações', 'O interesse morre no próprio post', 'Redes sociais'),
  ('Conta pessoal, sem categoria profissional declarada', 'O perfil não se apresenta como advogado', 'Redes sociais'),
  ('Cinco dos sete destaques são de viagem e de lazer', 'O primeiro bloco que o visitante vê não prova competência', 'Redes sociais'),
  ('Seis interrupções longas desde 2025, a maior de 52 dias', 'O alcance recomeça a cada retomada', 'Redes sociais'),
  ('O perfil só alcança quem já segue', 'A audiência mais engajada da praça não cresce para público novo', 'Tráfego pago'),
], 'Auditoria de presença digital de Diego Santos, coleta de 13/08/2026: Instagram @advdiegosantos pela API '
   'interna com sessão autenticada, histórico integral de 113 publicações; Google Search em pt-BR; '
   'debemesantos.com.br e wp-sitemap.xml; Jusbrasil, Escavador, LinkedIn e listaadv.br.', compacta=True)}
<h3 class="sub">O ativo que a auditoria mediu</h3>
<p class="texto">O engajamento de 3,89% em 2026 é o mais alto da amostra de Palhoça, contra 1,14% do
@oabpalhoca e 0,53% do @advocacia.bublitz. As 13 publicações sobre o escritório têm 5,38%, contra 3,18%
das 70 de família e fé: o conteúdo profissional é o que mais engaja e é o mais raro do perfil, com 11% do
total. O carrossel entrega 5,13% contra 2,29% da imagem estática. Nada disso exige trocar o tom que
construiu a base.</p>
''', 'A atenção já foi conquistada. <span class="azul">Falta abrir a porta.</span>')

    # --- 2. as tres vertentes
    d.pag('As três vertentes', f'''
<h2 class="titulo">Três vertentes, três contratos possíveis</h2>
<p class="lede">Cada vertente tem escopo e preço próprios e pode ser contratada sozinha. Elas foram
separadas por natureza de trabalho: a primeira constrói ativos indexáveis, a segunda produz conteúdo e a
terceira compra alcance para público novo.</p>
{defs([
  ('1. Tecnologia',
   'Uma página pessoal indexável no domínio do escritório, perfis nos diretórios jurídicos e a medição que '
   'liga publicação, busca e contato. É o que disputa o nome contra os seis homônimos, e é o que fica com '
   'ele mesmo que o contrato acabe.'),
  ('2. Gestão de redes sociais',
   'Caminho de contato no perfil, destaques reorganizados e produção mensal de conteúdo jurídico útil, que '
   'é o tema de melhor desempenho medido. Fecha as seis interrupções longas desde 2025.'),
  ('3. Tráfego pago',
   'Impulsionamento de conteúdo informativo no Meta Ads, dentro da norma da OAB, para alcançar quem ainda '
   'não segue o perfil. A busca do Google entra a partir do nível Crescimento.'),
])}
{tabela(['Vertente', 'Entrada', 'Mensal'], [
  ('1. Tecnologia', '5.400', '400'),
  ('2. Gestão de redes sociais', '<span class="na">sem entrada</span>', 'a partir de 1.999'),
  ('3. Tráfego pago', '1.400', 'a partir de 1.200'),
  ('__total__', 'Contratando as três em separado', '6.800', 'a partir de 3.599'),
  ('__total__', 'As três no mesmo contrato', '<b>6.100</b>', '<b>a partir de 3.199</b>'),
], 'Valores em reais, acrescidos de imposto. O mensal das vertentes 2 e 3 varia conforme o nível '
   'escolhido, e os três níveis estão nas páginas 5 e 7. A entrada pode ser parcelada em até doze vezes, '
   'o que dá 509 reais por mês no contrato das três. A verba de anúncios é paga direto à plataforma e não '
   'está somada aqui.', alinha={1: 'num', 2: 'num'}, compacta=True)}
<h3 class="sub">Contratando duas das três</h3>
{tabela(['Combinação', 'Entrada', 'Mensal'], [
  ('Tecnologia e redes sociais', '5.100', 'a partir de 2.299'),
  ('Tecnologia e tráfego pago', '6.400', 'a partir de 1.500'),
  ('Redes sociais e tráfego pago', '1.400', 'a partir de 3.099'),
], 'Tráfego pago sem a vertente de tecnologia funciona, mas o anúncio passa a levar para o perfil do '
   'Instagram, e não para uma página que o Google possa indexar em nome dele.',
   alinha={1: 'num', 2: 'num'}, compacta=True)}
''', 'A ordem que protege o investimento é tecnologia, depois conteúdo, <span class="azul">e só então anúncio.</span>')

    # --- 3. tecnologia
    d.pag('Tecnologia', f'''
<h2 class="titulo">Vertente 1: Tecnologia</h2>
<p class="lede">Esta vertente tem duas partes. Uma é paga uma vez e constrói os ativos que hoje não
existem. A outra é mensal e serve para mantê-los vivos e medidos.</p>
{tabela(['O investimento da vertente 1', 'Valor'], [
  ('Pagamento único, a construção', '5.400'),
  ('Mensal, a sustentação', '400'),
], 'Valores em reais, acrescidos de imposto. O pagamento único pode ser parcelado em até doze vezes. '
   'No contrato das três vertentes, a entrada somada cai de 6.800 para 6.100.',
   alinha={1: 'num'}, compacta=True)}
<h3 class="sub">Pagamento único, a construção</h3>
{tabela(['Obra', 'O que inclui', 'Valor'], [
  ('Página pessoal no domínio do escritório', 'Página própria dentro de debemesantos.com.br com biografia, número de inscrição na OAB, áreas de atuação, atuação institucional na 29ª Subseção e na Câmara de Palhoça, foto profissional, JSON-LD de advogado e contato direto. É o único ativo capaz de disputar a busca pelo nome contra os homônimos. Entrega em 2 a 3 semanas.', '<b>2.700</b>'),
  ('Identidade única na busca', 'Definição de uma grafia oficial do nome e aplicação em todos os canais. Criação e verificação de perfil no Jusbrasil, no Escavador, no LinkedIn e no listaadv.br, com a mesma grafia, a mesma foto e o mesmo texto de atuação.', '<b>2.000</b>'),
  ('Rastreamento e medição', 'Link rastreável por origem, eventos de clique e de conversa e painel ligando publicação, busca pelo nome e contato recebido.', '<b>700</b>'),
  ('__total__', 'Pagamento único', '', '<b>5.400</b>'),
], 'Os seis homônimos citados foram localizados na primeira página da busca por “Diego Santos” advogado '
   'Palhoça, em 13/08/2026. A página fica no domínio que já existe, o que aproveita a autoridade dele e '
   'não gera custo de domínio novo.')}
<h3 class="sub">Mensal, a sustentação</h3>
{tabela(['O que entra todo mês', 'Detalhe', 'Valor'], [
  ('Manutenção da página pessoal', 'Atualização de currículo, de atuação institucional e de áreas, mais correção de erro', ''),
  ('Perfis em diretórios mantidos', 'Dados, foto e texto de atuação conferidos nos quatro diretórios, com a mesma grafia', ''),
  ('Relatório de busca pelo nome', 'Posição dos ativos próprios contra os homônimos, e origem do contato recebido', ''),
  ('__total__', 'Mensal', '', '<b>400</b>'),
], compacta=True)}
''', 'A página pessoal é o único ativo <span class="azul">que disputa o nome contra seis homônimos.</span>')

    # --- 4. redes, primeiro mes
    d.pag('Redes sociais, primeiro mês', f'''
<h2 class="titulo">Vertente 2: Gestão de redes sociais</h2>
<p class="lede">Antes da primeira publicação, o perfil precisa de caminho de contato e de organização. Esse
trabalho é feito no primeiro mês, sem pagamento separado. A última coluna mostra a partir de qual nível
cada entrega entra.</p>
{tabela(['Entrega do primeiro mês', 'O que inclui', 'A partir de'], [
  ('Conta profissional e contato', 'Migração para conta profissional, categoria de advogado, botão de contato, WhatsApp ligado ao perfil, e-mail público e link rastreável na bio apontando para a página pessoal', 'Essencial'),
  ('Organização do perfil', 'Bio reescrita com a inscrição na OAB, as áreas de atuação e a atuação institucional, e dados de contato conferidos', 'Essencial'),
  ('Destaques reorganizados', 'Os sete destaques atuais, hoje com cinco de viagem e de lazer, reordenados para abrir pela atuação profissional, com conteúdo técnico recuperado do feed', 'Essencial'),
  ('Arquitetura de conteúdo', 'Linhas editoriais definidas por área de atuação e por atuação institucional, com a primeira grade editorial aprovada', 'Essencial'),
  ('Sistema de design para o Instagram', 'Paleta, tipografia, grade de capas e modelos prontos de post, de carrossel e de story, para que toda peça saia no mesmo padrão visual', '<b>Crescimento</b>'),
  ('Arquivos editáveis entregues', 'Os modelos do sistema de design ficam com ele e continuam valendo se o contrato acabar', '<b>Crescimento</b>'),
], 'A organização é feita uma vez e não se repete a cada mês. No nível Essencial as peças seguem um modelo '
   'básico: o sistema de design próprio e a entrega dos arquivos editáveis entram a partir do Crescimento.')}
{nota('Esta vertente não tem pagamento de entrada',
      'Diferente da vertente de tecnologia, aqui não há valor pago à parte. A organização entra no primeiro '
      'mês do plano escolhido, e o pagamento passa a ser apenas a mensalidade a partir daí.')}
''', 'Quatro dos dez achados <span class="azul">se resolvem na primeira semana, antes de qualquer produção.</span>')

    # --- 5. redes, planos
    d.pag('Redes sociais, planos', f'''
<h2 class="titulo">Vertente 2: Gestão de redes sociais</h2>
<p class="lede">A vertente é toda mensal, em três níveis. O que separa um nível do outro é o volume
publicado por mês. Não há valor de entrada.</p>
<table class="planos">
<thead><tr><th class="rot"></th>
<th class="col">Essencial</th>
<th class="col dest"><span class="rec">Recomendado</span>Crescimento</th>
<th class="col">Autoridade</th></tr></thead>
<tbody>
<tr><td class="rot">Investimento mensal</td>
  <td class="v"><span class="preco">1.999</span><span class="un">reais por mês</span></td>
  <td class="v dest"><span class="preco az">3.199</span><span class="un">reais por mês</span></td>
  <td class="v"><span class="preco">4.999</span><span class="un">reais por mês</span></td></tr>
<tr><td class="rot">Publicações de feed por mês</td>
  <td class="v">6</td><td class="v dest">12</td><td class="v">18</td></tr>
<tr><td class="rot">Stories por mês</td>
  <td class="v">10</td><td class="v dest">20</td><td class="v">30</td></tr>
<tr><td class="rot">Reels editados por mês</td>
  <td class="v">2</td><td class="v dest">4</td><td class="v">8</td></tr>
<tr class="grupo"><td colspan="4">Feito no primeiro mês, sem custo separado</td></tr>
<tr><td class="rot">Conta profissional, contato e organização do perfil</td>
  <td class="v"><span class="sim">sim</span></td><td class="v dest"><span class="sim">sim</span></td><td class="v"><span class="sim">sim</span></td></tr>
<tr><td class="rot">Destaques reorganizados pela atuação profissional</td>
  <td class="v"><span class="sim">sim</span></td><td class="v dest"><span class="sim">sim</span></td><td class="v"><span class="sim">sim</span></td></tr>
<tr><td class="rot">Sistema de design para o Instagram</td>
  <td class="v"><span class="na">não incluído</span></td><td class="v dest"><span class="sim">sim</span></td><td class="v"><span class="sim">sim</span></td></tr>
<tr><td class="rot">Arquivos editáveis entregues</td>
  <td class="v"><span class="na">não incluído</span></td><td class="v dest"><span class="sim">sim</span></td><td class="v"><span class="sim">sim</span></td></tr>
</tbody></table>
<p class="fonte">Valores em reais, acrescidos de imposto. Sem fidelidade no primeiro mês em qualquer um dos
planos. O escopo completo de cada nível está na página seguinte.</p>
{nota('Como o volume é contado',
      'Publicação de feed é um post publicado no perfil, seja imagem única ou carrossel, com quantas telas '
      'o assunto pedir. Story é contado por tela. Reel editado é montado a partir do material gravado por '
      'ele mesmo ou pela equipe do escritório.',
      'A divisão exata entre os formatos é definida na grade editorial aprovada todo mês, e pode variar '
      'sem mudar o total contratado.')}
<h3 class="sub">Por que o plano Crescimento é o indicado</h3>
<p class="texto">O ritmo atual é de 4,4 publicações por mês, apuradas sobre as 35 de 2026 até 10/08, com
seis interrupções longas desde 2025. O Essencial já dobra esse ritmo. O Crescimento é o menor nível que
comporta uma série de conteúdo jurídico útil por mês, que é o tema de melhor desempenho medido no perfil,
com 5,38% contra 3,18% do conteúdo pessoal.</p>
''')

    # --- 6. redes, escopo
    d.pag('Redes sociais, escopo', escopo(
        'Vertente 2: o que entra em cada nível',
        'Os volumes são totais mensais do perfil @advdiegosantos. O carrossel tem prioridade porque é o '
        'formato de melhor desempenho do perfil, com 5,13% contra 2,29% da imagem estática no histórico '
        'integral.',
        [('Produção', [
            ('Publicações de feed por mês', '6', '12', '18'),
            ('Stories por mês', '10', '20', '30'),
            ('Reels editados a partir do material enviado', '2', '4', '8'),
            ('Roteiro do vídeo, com o que gravar e como', 'nao', 'sim', 'sim'),
            ('Série de conteúdo jurídico útil', 'nao', '1 por mês', '2 por mês'),
            ('Cobertura da atuação na OAB e na Câmara', '1 por mês', '2 por mês', '4 por mês'),
          ]),
         ('Estrutura e direção', [
            ('Gestão do perfil com calendário aprovado', 'sim', 'sim', 'sim'),
            ('Legenda, hashtag e localização em toda publicação', 'sim', 'sim', 'sim'),
            ('Destaques mantidos por área de atuação', 'sim', 'sim', 'sim'),
            ('Sistema de design próprio e arquivos editáveis', 'nao', 'sim', 'sim'),
            ('Conferência de cada peça com o Provimento 205/2021', 'sim', 'sim', 'sim'),
          ]),
         ('Acompanhamento', [
            ('Relatório mensal do perfil', 'sim', 'sim', 'sim'),
            ('Relatório de origem das conversas', 'nao', 'sim', 'sim'),
            ('Reunião estratégica', 'nao', 'mensal', 'quinzenal'),
          ])]) + f'''
{nota('Captação de foto e de vídeo não está incluída',
      'Nenhum dos três níveis inclui fotógrafo ou cinegrafista. O mensal cobre roteiro, edição, legenda, '
      'capa e publicação a partir do material gravado por ele mesmo ou pela equipe do escritório. Quando '
      'houver necessidade de captação profissional, a Oráculo indica e coordena o fornecedor, e o serviço '
      'é orçado e pago diretamente a ele.')}
''')

    # --- 7. trafego pago
    d.pag('Tráfego pago', planos_com_escopo(
        'Vertente 3: impulsionamento de conteúdo informativo',
        'Esta vertente compra alcance para quem ainda não segue o perfil. A entrada de 1.400 reais é paga '
        'uma vez e cobre a abertura e a verificação do Gerenciador de Negócios, o pixel e a API de '
        'conversões, os públicos por praça e por área e a estrutura inicial de campanhas.',
        ('1.200', '1.800', '2.600'),
        [('Plataformas', [
            ('Meta Ads, no Instagram e no Facebook', 'sim', 'sim', 'sim'),
            ('Google Ads, na busca', 'nao', 'sim', 'sim'),
          ]),
         ('Campanhas', [
            ('Campanhas ativas ao mesmo tempo', 'até 2', 'até 4', 'até 6'),
            ('Criativos informativos produzidos por mês', '4', '8', '12'),
            ('Otimização e ajuste de campanha', 'semanal', '2 vezes por semana', 'contínua'),
            ('Públicos por praça e por área de atuação', 'nao', 'sim', 'sim'),
          ]),
         ('Conformidade com a norma da OAB', [
            ('Conferência de cada peça com o Provimento 205/2021', 'sim', 'sim', 'sim'),
            ('Registro do que foi ajustado em cada peça', 'sim', 'sim', 'sim'),
          ]),
         ('Medição', [
            ('Relatório de aplicação da verba', 'sim', 'sim', 'sim'),
            ('Relatório de origem das conversas', 'nao', 'sim', 'sim'),
            ('Reunião de leitura de campanha', 'nao', 'mensal', 'quinzenal'),
          ]),
         ('Verba de anúncios, paga direto à plataforma', [
            ('Faixa recomendada por mês, somando as plataformas', '400 a 800', '800 a 1.500', 'a definir'),
          ])],
        'Valores em reais, acrescidos de imposto. A verba de anúncios não passa pela Oráculo: é paga '
        'diretamente à plataforma, com relatório de aplicação todo mês. O anúncio de busca segue a mesma '
        'regra do impulsionamento: leva a conteúdo informativo ou à página pessoal, nunca a oferta de '
        'serviço ou a condição comercial.'))

    pagina_oab(d, 'um advogado com marca pessoal e atuação institucional')

    # --- 9. metas
    d.pag('Metas', f'''
<h2 class="titulo">O que perseguimos nos primeiros 90 dias</h2>
<p class="lede">As metas estão separadas por vertente, para que cada contrato possa ser cobrado pelo que
entrega. Não há meta de causas fechadas nem de receita: promessa de resultado é vedada pela norma da OAB,
e o fechamento depende do atendimento do escritório.</p>
{tabela(['Indicador', 'Hoje', 'Meta em 90 dias'], [
  ('__grupo__', 'Vertente 1, tecnologia'),
  ('Ativos próprios indexados pelo nome', '1', '5'),
  ('Página própria na busca pelo nome', 'não existe', 'publicada e indexada'),
  ('Perfis em diretórios jurídicos', '0 de 4', '4 de 4'),
  ('Medição instalada', 'nenhuma', 'link rastreável e eventos'),
  ('__grupo__', 'Vertente 2, redes sociais'),
  ('Link, botão de contato e WhatsApp no perfil', 'nenhum dos três', 'os três ativos'),
  ('Publicações com chamada para ação', '2 de 113', '50% das publicações do trimestre'),
  ('Conteúdo jurídico útil no perfil', '11%', '40% das publicações do trimestre'),
  ('Publicações de feed por mês', '4,4', '12'),
  ('Maior intervalo sem publicar', '52 dias', 'nenhum acima de 14 dias'),
  ('__grupo__', 'Vertente 3, tráfego pago'),
  ('Pessoas alcançadas fora da base de seguidores', '0', '8.000 a 15.000 por mês'),
  ('Conversas com origem identificada', '0', '15 a 30 por mês'),
], 'Situação atual apurada na auditoria de 13/08/2026, sobre o histórico integral de 113 publicações. O '
   'ritmo de 4,4 por mês vem das 35 publicações de 2026 até 10/08. Indexação de página nova leva de dois a '
   'três meses, e por isso a meta de busca é de publicação e indexação, não de posição. A meta de alcance '
   'pago considera a faixa de verba do plano Crescimento.', alinha={1: 'num', 2: 'num'}, compacta=True)}
''', 'O perfil já converte atenção. <span class="azul">Em 90 dias ele passa a converter contato.</span>')

    # --- 10. cronograma
    d.pag('Como começa', f'''
<h2 class="titulo">Como as três vertentes entram, e em que ordem</h2>
<p class="lede">O caminho de contato vem primeiro porque é o único item que muda o resultado já na semana
de implantação, sem depender de produção nova. A página pessoal vem logo atrás, porque leva de dois a três
meses para aparecer na busca.</p>
{defs([
  ('Semana 1, vertente 2',
   'Migração para conta profissional, categoria de advogado, botão de contato e WhatsApp ligados. Link '
   'rastreável na bio. Definição da grafia oficial do nome, que passa a valer em todos os canais.'),
  ('Mês 1, vertentes 1 e 2',
   'Página pessoal publicada no domínio do escritório, com inscrição na OAB, áreas de atuação e atuação '
   'institucional. Perfis criados no Jusbrasil, no Escavador, no LinkedIn e no listaadv.br. Destaques '
   'reorganizados, abrindo pela atuação profissional. Primeira grade editorial aprovada.'),
  ('Mês 2, vertente 2',
   'Primeira série de conteúdo jurídico útil, em carrossel, que é o formato de melhor desempenho medido no '
   'perfil. Ritmo estabilizado em doze publicações de feed por mês. Rastreamento no ar.'),
  ('Mês 3, vertente 3',
   'Tráfego pago entra agora, com a medição pronta e com um acervo de peças orgânicas já testado. As '
   'campanhas sobem sobre o conteúdo que teve melhor desempenho sem verba.'),
  ('Meses 4 a 6, as três',
   'Consolidação da grafia do nome nos ativos indexados, cadência mantida no perfil e campanhas otimizadas '
   'contra o relatório de origem das conversas.'),
])}
{CONDICOES}
''')

    pagina_grupo(d, 'diego')

    d.contracapa(
        'Uma conversa de 30 minutos para fechar o escopo',
        'O que precisa ser decidido antes de começar: quais vertentes entram e em que ordem, qual grafia do '
        'nome vira a oficial, qual número de WhatsApp recebe o contato do perfil, se a página pessoal fica '
        'no domínio do escritório ou em domínio próprio e quem grava o material em vídeo.',
        [('Reunião', '30 minutos, presencial em Palhoça ou por vídeo'),
         ('Onboarding', '7 dias, com a conta profissional migrada e o contato no ar'),
         ('Entrada', '6.100 reais pelas três vertentes, parcelável em até 12 vezes de 509'),
         ('Mensal', 'a partir de 3.199 reais pelas três, conforme o nível escolhido')],
        'Baseado na auditoria de presença digital de Diego Santos,<br>de 13 de agosto de 2026, sobre 113 publicações')

    return d.salvar(
        os.path.join(RAIZ, 'DiegoSantos', 'Proposta-Comercial.html'),
        'Proposta Comercial, Diego Santos, advogado',
        'Proposta comercial de Diego Santos em três vertentes: tecnologia (página pessoal indexada, '
        'diretórios jurídicos e medição), gestão de redes sociais e tráfego pago. Oráculo Tecnologia, '
        'agosto de 2026.')


# ================================================================ 3. SUZIELLEN ALEIXO
def build_suziellen():
    d = Doc('Suziellen Aleixo, advogada previdenciária')

    d.capa(
        'Suziellen Aleixo, advogada previdenciária',
        'Proposta comercial: tecnologia, gestão de redes sociais e tráfego pago',
        'A auditoria de 13 de agosto de 2026 percorreu as 30 publicações do perfil, a busca pelo nome, os '
        'diretórios previdenciários e a praça de Brasília. Esta proposta organiza a resposta em três '
        'vertentes, cada uma com escopo e preço próprios, contratáveis juntas ou separadamente.',
        [('3', 'vertentes contratáveis'), ('3,12%', 'de engajamento em 79 dias'),
         ('5.100', 'reais de entrada, uma vez'), ('3.199', 'reais por mês, a partir de')])

    # --- 1. diagnostico
    d.pag('Diagnóstico', f'''
<h2 class="titulo">O que a auditoria encontrou</h2>
<p class="lede">O histórico integral do perfil foi coletado em 13 de agosto de 2026: 30 publicações em 79
dias, num ritmo de 2,7 por semana. A busca pelo nome, os diretórios e o site do escritório foram
verificados na mesma data. A última coluna mostra qual das três vertentes resolve cada achado.</p>
{tabela(['Achado', 'O que isso custa', 'Vertente'], [
  ('Nenhum homônimo na busca pelo nome, e apenas dois ativos indexados', 'Um nome que ninguém disputa, e nada próprio para ocupá-lo', 'Tecnologia'),
  ('Sem perfil no Jusbrasil, no Escavador e no Previdenciarista', 'Fora dos diretórios que ocupam o topo da busca previdenciária', 'Tecnologia'),
  ('O LinkedIn declara São José, Santa Catarina', 'A localidade diverge dos sinais recentes de mudança para Brasília', 'Tecnologia'),
  ('O nome não aparece em nenhuma das seis páginas do site do escritório', 'Nenhuma página indexável prova o vínculo profissional', 'Tecnologia'),
  ('Nenhum destaque publicado', 'O conteúdo sobre BPC/LOAS e perícia médica some do feed em 48 horas', 'Redes sociais'),
  ('14 conteúdos técnicos publicados, 12 deles em imagem estática', 'O melhor material está no formato de pior desempenho do perfil', 'Redes sociais'),
  ('Uma chamada para ação em 30 publicações', 'O link de WhatsApp existe na bio e quase nunca é apontado', 'Redes sociais'),
  ('Conta ainda pessoal, sem categoria profissional', 'O perfil não se apresenta como advogada no próprio Instagram', 'Redes sociais'),
  ('A praça de Brasília ainda não a conhece', 'A base cresceu em Santa Catarina, e a demanda a atender é de outra praça', 'Tráfego pago'),
], 'Auditoria de presença digital de Suziellen Aleixo, coleta de 13/08/2026: Instagram @dra.suziellen pela '
   'API interna com sessão autenticada, histórico integral de 30 publicações; quatro perfis de referência '
   'medidos na mesma data; Google Search em pt-BR; LinkedIn; Diário Eletrônico da OAB de 11/12/2025; '
   'debemesantos.com.br.', compacta=True)}
<h3 class="sub">O ativo que a auditoria mediu</h3>
<p class="texto">São 1.700 seguidores e 3,12% de engajamento em 79 dias, enquanto o par de 37.543
seguidores medido no mesmo dia engaja 0,15%. O Reel entrega 5,03% contra 2,26% da imagem estática neste
perfil, e a bio já declara sete linhas de serviço previdenciário com link de WhatsApp funcionando. O
posicionamento, que costuma ser a parte mais difícil, já está resolvido.</p>
''', 'Três meses de trabalho técnico <span class="azul">merecem durar mais que 48 horas.</span>')

    # --- 2. as tres vertentes
    d.pag('As três vertentes', f'''
<h2 class="titulo">Três vertentes, três contratos possíveis</h2>
<p class="lede">Cada vertente tem escopo e preço próprios e pode ser contratada sozinha. Elas foram
separadas por natureza de trabalho: a primeira constrói ativos que o Google indexa, a segunda dá
permanência ao conteúdo e a terceira compra alcance na praça nova.</p>
{defs([
  ('1. Tecnologia',
   'Página própria e páginas por benefício, perfis nos diretórios previdenciários e a medição que liga '
   'publicação, busca e contato. O nome não tem homônimo na busca, e hoje não existe nada próprio para '
   'ocupar esse espaço.'),
  ('2. Gestão de redes sociais',
   'Destaques por benefício a partir dos 14 conteúdos técnicos já publicados, conta profissional e '
   'produção mensal, com o técnico migrando para vídeo, que é o formato de melhor desempenho do perfil.'),
  ('3. Tráfego pago',
   'Impulsionamento de conteúdo informativo no Meta Ads, dentro da norma da OAB, para alcançar a praça de '
   'Brasília, onde a base ainda não existe. A busca do Google entra a partir do nível Crescimento.'),
])}
{tabela(['Vertente', 'Entrada', 'Mensal'], [
  ('1. Tecnologia', '4.200', '400'),
  ('2. Gestão de redes sociais', '<span class="na">sem entrada</span>', 'a partir de 1.999'),
  ('3. Tráfego pago', '1.400', 'a partir de 1.200'),
  ('__total__', 'Contratando as três em separado', '5.600', 'a partir de 3.599'),
  ('__total__', 'As três no mesmo contrato', '<b>5.100</b>', '<b>a partir de 3.199</b>'),
], 'Valores em reais, acrescidos de imposto. O mensal das vertentes 2 e 3 varia conforme o nível '
   'escolhido, e os três níveis estão nas páginas 5 e 7. A entrada pode ser parcelada em até doze vezes, '
   'o que dá 425 reais por mês no contrato das três. A verba de anúncios é paga direto à plataforma e não '
   'está somada aqui.', alinha={1: 'num', 2: 'num'}, compacta=True)}
<h3 class="sub">Contratando duas das três</h3>
{tabela(['Combinação', 'Entrada', 'Mensal'], [
  ('Tecnologia e redes sociais', '3.900', 'a partir de 2.299'),
  ('Tecnologia e tráfego pago', '5.200', 'a partir de 1.500'),
  ('Redes sociais e tráfego pago', '1.400', 'a partir de 3.099'),
], 'Tráfego pago sem a vertente de tecnologia funciona, mas o anúncio passa a levar para o perfil do '
   'Instagram, e não para uma página por benefício que o Google possa indexar.',
   alinha={1: 'num', 2: 'num'}, compacta=True)}
''', 'A ordem que protege o investimento é tecnologia, depois conteúdo, <span class="azul">e só então anúncio.</span>')

    # --- 3. tecnologia
    d.pag('Tecnologia', f'''
<h2 class="titulo">Vertente 1: Tecnologia</h2>
<p class="lede">Esta vertente tem duas partes. Uma é paga uma vez e constrói os ativos que hoje não
existem. A outra é mensal e serve para mantê-los vivos e medidos.</p>
{tabela(['O investimento da vertente 1', 'Valor'], [
  ('Pagamento único, a construção', '4.200'),
  ('Mensal, a sustentação', '400'),
], 'Valores em reais, acrescidos de imposto. O pagamento único pode ser parcelado em até doze vezes. '
   'No contrato das três vertentes, a entrada somada cai de 5.600 para 5.100.',
   alinha={1: 'num'}, compacta=True)}
<h3 class="sub">Pagamento único, a construção</h3>
{tabela(['Obra', 'O que inclui', 'Valor'], [
  ('Página própria e páginas por benefício', 'Página de apresentação com inscrição na OAB, formação, atuação previdenciária e contato, mais três páginas por benefício, escolhidas entre BPC/LOAS, perícia médica, salário-maternidade e negativa do INSS. JSON-LD de advogada e texto construído a partir dos conteúdos técnicos já publicados. Entrega em 3 a 4 semanas.', '<b>2.600</b>'),
  ('Diretórios e LinkedIn', 'Criação e verificação de perfil no Jusbrasil, no Escavador e no Previdenciarista, com a mesma foto e o mesmo texto de atuação. Correção da localidade declarada no LinkedIn e reescrita do título do perfil.', '<b>1.000</b>'),
  ('Rastreamento e medição', 'Link rastreável por origem no lugar do wa.me direto, eventos de clique e de conversa e painel ligando publicação, busca e contato recebido.', '<b>600</b>'),
  ('__total__', 'Pagamento único', '', '<b>4.200</b>'),
], 'A busca previdenciária de Brasília é disputada por escritórios com página dedicada a cada benefício, e '
   'não por perfil de rede social: a auditoria localizou seis deles na primeira página em 13/08/2026, '
   'todos com site próprio especializado.')}
<h3 class="sub">Mensal, a sustentação</h3>
{tabela(['O que entra todo mês', 'Detalhe', 'Valor'], [
  ('Manutenção das páginas', 'Atualização de texto, de formação e de atuação, mais correção de erro nas páginas por benefício', ''),
  ('Perfis em diretórios mantidos', 'Dados, foto e texto de atuação conferidos nos três diretórios previdenciários e no LinkedIn', ''),
  ('Relatório de busca pelo nome', 'Posição dos ativos próprios e origem do contato recebido', ''),
  ('__total__', 'Mensal', '', '<b>400</b>'),
], compacta=True)}
''', 'O nome não tem homônimo na busca. <span class="azul">Falta alguém ocupar o espaço que ele deixa livre.</span>')

    # --- 4. redes, primeiro mes
    d.pag('Redes sociais, primeiro mês', f'''
<h2 class="titulo">Vertente 2: Gestão de redes sociais</h2>
<p class="lede">Antes da primeira publicação, o acervo já produzido precisa virar ativo permanente. Esse
trabalho é feito no primeiro mês, sem pagamento separado. A última coluna mostra a partir de qual nível
cada entrega entra.</p>
{tabela(['Entrega do primeiro mês', 'O que inclui', 'A partir de'], [
  ('Seis destaques por benefício', 'Recuperação dos 14 conteúdos técnicos hoje enterrados no feed, reorganizados em seis destaques por benefício, com capas padronizadas e ordem de leitura. Nenhuma produção nova é necessária', 'Essencial'),
  ('Conta profissional e contato', 'Migração para conta profissional, categoria de advogada, botão de contato, e-mail público e troca do link direto de WhatsApp por link rastreável', 'Essencial'),
  ('Organização do perfil', 'Bio revisada com as sete linhas de serviço já declaradas, a inscrição na OAB e a praça de atendimento', 'Essencial'),
  ('Arquitetura de conteúdo', 'Linhas editoriais definidas por benefício, com a primeira grade editorial aprovada', 'Essencial'),
  ('Sistema de design para o Instagram', 'Paleta, tipografia, grade de capas e modelos prontos de post, de carrossel e de story, para que toda peça saia no mesmo padrão visual', '<b>Crescimento</b>'),
  ('Arquivos editáveis entregues', 'Os modelos do sistema de design ficam com ela e continuam valendo se o contrato acabar', '<b>Crescimento</b>'),
], 'A organização é feita uma vez e não se repete a cada mês. No nível Essencial as peças seguem um modelo '
   'básico: o sistema de design próprio e a entrega dos arquivos editáveis entram a partir do Crescimento.')}
{nota('Esta vertente não tem pagamento de entrada',
      'Diferente da vertente de tecnologia, aqui não há valor pago à parte. Os destaques e a organização '
      'entram no primeiro mês do plano escolhido, e o pagamento passa a ser apenas a mensalidade a partir '
      'daí. É a entrega mais barata desta proposta porque usa material que já foi produzido e pago.')}
''', 'O acervo técnico já existe. <span class="azul">Falta ele parar de desaparecer no feed.</span>')

    # --- 5. redes, planos
    d.pag('Redes sociais, planos', f'''
<h2 class="titulo">Vertente 2: Gestão de redes sociais</h2>
<p class="lede">A vertente é toda mensal, em três níveis. O que separa um nível do outro é o volume
publicado por mês. Não há valor de entrada.</p>
<table class="planos">
<thead><tr><th class="rot"></th>
<th class="col">Essencial</th>
<th class="col dest"><span class="rec">Recomendado</span>Crescimento</th>
<th class="col">Autoridade</th></tr></thead>
<tbody>
<tr><td class="rot">Investimento mensal</td>
  <td class="v"><span class="preco">1.999</span><span class="un">reais por mês</span></td>
  <td class="v dest"><span class="preco az">3.199</span><span class="un">reais por mês</span></td>
  <td class="v"><span class="preco">4.999</span><span class="un">reais por mês</span></td></tr>
<tr><td class="rot">Publicações de feed por mês</td>
  <td class="v">6</td><td class="v dest">12</td><td class="v">18</td></tr>
<tr><td class="rot">Stories por mês</td>
  <td class="v">10</td><td class="v dest">20</td><td class="v">30</td></tr>
<tr><td class="rot">Reels editados por mês</td>
  <td class="v">2</td><td class="v dest">4</td><td class="v">8</td></tr>
<tr class="grupo"><td colspan="4">Feito no primeiro mês, sem custo separado</td></tr>
<tr><td class="rot">Seis destaques por benefício e organização do perfil</td>
  <td class="v"><span class="sim">sim</span></td><td class="v dest"><span class="sim">sim</span></td><td class="v"><span class="sim">sim</span></td></tr>
<tr><td class="rot">Conta profissional e link rastreável no lugar do wa.me</td>
  <td class="v"><span class="sim">sim</span></td><td class="v dest"><span class="sim">sim</span></td><td class="v"><span class="sim">sim</span></td></tr>
<tr><td class="rot">Sistema de design para o Instagram</td>
  <td class="v"><span class="na">não incluído</span></td><td class="v dest"><span class="sim">sim</span></td><td class="v"><span class="sim">sim</span></td></tr>
<tr><td class="rot">Arquivos editáveis entregues</td>
  <td class="v"><span class="na">não incluído</span></td><td class="v dest"><span class="sim">sim</span></td><td class="v"><span class="sim">sim</span></td></tr>
</tbody></table>
<p class="fonte">Valores em reais, acrescidos de imposto. Sem fidelidade no primeiro mês em qualquer um dos
planos. O escopo completo de cada nível está na página seguinte.</p>
{nota('Como o volume é contado',
      'Publicação de feed é um post publicado no perfil, seja imagem única ou carrossel, com quantas telas '
      'o assunto pedir. Story é contado por tela. Reel editado é montado a partir do material gravado por '
      'ela mesma.',
      'A divisão exata entre os formatos é definida na grade editorial aprovada todo mês, e pode variar '
      'sem mudar o total contratado.')}
<h3 class="sub">Por que o plano Crescimento é o indicado</h3>
<p class="texto">O ritmo atual já é de 2,7 publicações por semana, o que dá cerca de doze por mês. O nível
Essencial, com seis, seria um recuo. O Crescimento mantém o ritmo que ela já sustenta sozinha e acrescenta
o que falta: quatro Reels editados por mês, para levar o conteúdo técnico do formato de 2,26% para o de
5,03% de engajamento, e o sistema de design que hoje não existe.</p>
''')

    # --- 6. redes, escopo
    d.pag('Redes sociais, escopo', escopo(
        'Vertente 2: o que entra em cada nível',
        'Os volumes são totais mensais do perfil @dra.suziellen. O que muda não é a quantidade, que o '
        'perfil já sustenta: é o formato e o destino do conteúdo técnico.',
        [('Produção', [
            ('Publicações de feed por mês', '6', '12', '18'),
            ('Stories por mês', '10', '20', '30'),
            ('Reels editados a partir do material enviado', '2', '4', '8'),
            ('Roteiro do vídeo, com o que gravar e como', 'nao', 'sim', 'sim'),
            ('Conteúdo técnico por benefício', '2 por mês', '4 por mês', '8 por mês'),
          ]),
         ('Permanência e estrutura', [
            ('Destaques mantidos e ampliados por benefício', 'sim', 'sim', 'sim'),
            ('Gestão do perfil com calendário aprovado', 'sim', 'sim', 'sim'),
            ('Legenda, hashtag e localização em toda publicação', 'sim', 'sim', 'sim'),
            ('Sistema de design próprio e arquivos editáveis', 'nao', 'sim', 'sim'),
            ('Conferência de cada peça com o Provimento 205/2021', 'sim', 'sim', 'sim'),
          ]),
         ('Acompanhamento', [
            ('Relatório mensal do perfil', 'sim', 'sim', 'sim'),
            ('Relatório de origem das conversas', 'nao', 'sim', 'sim'),
            ('Reunião estratégica', 'nao', 'mensal', 'quinzenal'),
          ])]) + f'''
{nota('Captação de foto e de vídeo não está incluída',
      'Nenhum dos três níveis inclui fotógrafo ou cinegrafista. O mensal cobre roteiro, edição, legenda, '
      'capa e publicação a partir do material gravado por ela mesma. Quando houver necessidade de captação '
      'profissional, a Oráculo indica e coordena o fornecedor, e o serviço é orçado e pago diretamente a '
      'ele.')}
''')

    # --- 7. trafego pago
    d.pag('Tráfego pago', planos_com_escopo(
        'Vertente 3: impulsionamento de conteúdo informativo',
        'Esta vertente compra alcance na praça onde a base ainda não existe. A entrada de 1.400 reais é '
        'paga uma vez e cobre a abertura e a verificação do Gerenciador de Negócios, o pixel e a API de '
        'conversões, os públicos por praça e por benefício e a estrutura inicial de campanhas.',
        ('1.200', '1.800', '2.600'),
        [('Plataformas', [
            ('Meta Ads, no Instagram e no Facebook', 'sim', 'sim', 'sim'),
            ('Google Ads, na busca', 'nao', 'sim', 'sim'),
          ]),
         ('Campanhas', [
            ('Campanhas ativas ao mesmo tempo', 'até 2', 'até 4', 'até 6'),
            ('Criativos informativos produzidos por mês', '4', '8', '12'),
            ('Otimização e ajuste de campanha', 'semanal', '2 vezes por semana', 'contínua'),
            ('Públicos por praça e por benefício', 'nao', 'sim', 'sim'),
          ]),
         ('Conformidade com a norma da OAB', [
            ('Conferência de cada peça com o Provimento 205/2021', 'sim', 'sim', 'sim'),
            ('Registro do que foi ajustado em cada peça', 'sim', 'sim', 'sim'),
          ]),
         ('Medição', [
            ('Relatório de aplicação da verba', 'sim', 'sim', 'sim'),
            ('Relatório de origem das conversas', 'nao', 'sim', 'sim'),
            ('Reunião de leitura de campanha', 'nao', 'mensal', 'quinzenal'),
          ]),
         ('Verba de anúncios, paga direto à plataforma', [
            ('Faixa recomendada por mês, somando as plataformas', '300 a 600', '600 a 1.200', 'a definir'),
          ])],
        'Valores em reais, acrescidos de imposto. A verba de anúncios não passa pela Oráculo: é paga '
        'diretamente à plataforma, com relatório de aplicação todo mês. O anúncio de busca segue a mesma '
        'regra do impulsionamento: leva a conteúdo informativo ou à página por benefício, nunca a oferta '
        'de serviço, a promessa de concessão nem a condição comercial.'))

    pagina_oab(d, 'uma advogada com marca pessoal em direito previdenciário')

    # --- 9. metas
    d.pag('Metas', f'''
<h2 class="titulo">O que perseguimos nos primeiros 90 dias</h2>
<p class="lede">As metas estão separadas por vertente, para que cada contrato possa ser cobrado pelo que
entrega. Não há meta de benefícios concedidos, de causas fechadas nem de receita: promessa de resultado é
vedada pela norma da OAB, e em matéria previdenciária a decisão é do INSS ou do Judiciário.</p>
{tabela(['Indicador', 'Hoje', 'Meta em 90 dias'], [
  ('__grupo__', 'Vertente 1, tecnologia'),
  ('Ativos próprios indexados pelo nome', '2', '6'),
  ('Páginas por benefício no ar', '0', '3'),
  ('Perfis em diretórios previdenciários', '0 de 3', '3 de 3'),
  ('Localidade declarada no LinkedIn', 'divergente', 'alinhada aos demais canais'),
  ('__grupo__', 'Vertente 2, redes sociais'),
  ('Destaques publicados', '0', '6, um por benefício'),
  ('Conteúdo técnico em vídeo', '2 de 14', '60% do técnico do trimestre'),
  ('Publicações com chamada para ação', '1 de 30', '50% das publicações do trimestre'),
  ('Ritmo de publicação de feed por mês', '11,6', 'mantido, com 40% em vídeo'),
  ('__grupo__', 'Vertente 3, tráfego pago'),
  ('Pessoas alcançadas fora da base de seguidores', '0', '6.000 a 12.000 por mês'),
  ('Conversas com origem identificada', '0', '20 a 40 por mês'),
], 'Situação atual apurada na auditoria de 13/08/2026, sobre o histórico integral de 30 publicações entre '
   '24/05/2026 e 11/08/2026. Indexação de página nova leva de dois a três meses, e por isso a meta de busca '
   'é de publicação e indexação, não de posição. A meta de alcance pago considera a faixa de verba do plano '
   'Crescimento.', alinha={1: 'num', 2: 'num'}, compacta=True)}
''', 'O ritmo já é bom e não precisa subir. <span class="azul">O que precisa mudar é o destino do conteúdo.</span>')

    # --- 10. cronograma
    d.pag('Como começa', f'''
<h2 class="titulo">Como as três vertentes entram, e em que ordem</h2>
<p class="lede">A ordem começa pelo que reaproveita material já produzido, porque entrega resultado no
primeiro mês sem depender de gravação nova. As páginas indexadas entram em seguida, porque levam de dois a
três meses para aparecer na busca.</p>
{defs([
  ('Semana 1, vertente 2',
   'Migração para conta profissional, categoria de advogada e botão de contato. Correção da localidade e do '
   'título no LinkedIn. Troca do link direto de WhatsApp por link rastreável.'),
  ('Mês 1, vertentes 1 e 2',
   'Seis destaques publicados a partir dos 14 conteúdos técnicos já existentes, organizados por benefício. '
   'Perfis criados no Jusbrasil, no Escavador e no Previdenciarista. Primeira grade editorial aprovada.'),
  ('Mês 2, vertentes 1 e 2',
   'Página própria no ar, com três páginas por benefício. Conteúdo técnico migrado para vídeo, no formato '
   'que já entrega 5,03% de engajamento neste perfil. Rastreamento no ar.'),
  ('Mês 3, vertente 3',
   'Tráfego pago entra agora, com a medição pronta e com um acervo de peças orgânicas já testado. As '
   'campanhas sobem sobre o conteúdo que teve melhor desempenho sem verba.'),
  ('Meses 4 a 6, as três',
   'Uma página por benefício a cada mês, cadência mantida no perfil e campanhas otimizadas contra o '
   'relatório de origem das conversas.'),
])}
{nota('Uma premissa que precisa ser confirmada antes de começar',
      'A auditoria reuniu sinais públicos de que Suziellen Aleixo é a advogada da nova unidade de Brasília: '
      'despedida de Florianópolis em 09/07/2026, Reel em Brasília em 06/08/2026 descrito como retorno à '
      'cidade natal, coassinatura do anúncio da sede da Asa Sul em 10/08/2026 e dois CNPJs em seu nome com '
      'sede em Brasília. É inferência, não dado confirmado.',
      'Se a premissa se confirmar, as páginas por benefício e os públicos das campanhas são construídos '
      'para Brasília. Se não, a mesma estrutura é construída para a praça correta, sem mudança de preço '
      'nem de prazo.')}
{CONDICOES}
''')

    pagina_grupo(d, 'suziellen')

    d.contracapa(
        'Uma conversa de 30 minutos para fechar o escopo',
        'O que precisa ser decidido antes de começar: quais vertentes entram e em que ordem, qual praça é a '
        'de atuação, se a página própria fica no domínio do escritório ou em domínio próprio, quais três '
        'benefícios entram nas primeiras páginas e qual é a rotina de gravação de vídeo.',
        [('Reunião', '30 minutos, presencial em Brasília ou por vídeo'),
         ('Onboarding', '7 dias, com a conta profissional migrada e os destaques em produção'),
         ('Entrada', '5.100 reais pelas três vertentes, parcelável em até 12 vezes de 425'),
         ('Mensal', 'a partir de 3.199 reais pelas três, conforme o nível escolhido')],
        'Baseado na auditoria de presença digital de Suziellen Aleixo,<br>de 13 de agosto de 2026, sobre 30 publicações')

    return d.salvar(
        os.path.join(RAIZ, 'SuziellenAleixo', 'Proposta-Comercial.html'),
        'Proposta Comercial, Suziellen Aleixo, advogada previdenciária',
        'Proposta comercial de Suziellen Aleixo em três vertentes: tecnologia (páginas por benefício e '
        'diretórios previdenciários), gestão de redes sociais e tráfego pago. Oráculo Tecnologia, agosto '
        'de 2026.')


# ================================================================ VALIDACAO
PALAVRAS_SEM_ACENTO = """
presenca correcao correcoes producao juridico juridica juridicos juridicas pagina paginas
proprio propria proprios proprias Oraculo escritorio escritorios socio socios Brasilia Palhoca
Florianopolis publicacao publicacoes atuacao inscricao implantacao reputacao medicao conversao
informacao divulgacao captacao conferencia padronizacao reorganizacao otimizacao verificacao
criacao definicao recuperacao migracao solicitacao avaliacao avaliacoes liberacao comprovacao
transferencia aprovacao gravacao direcao gestao reuniao sessao cadencia audiencia existencia
referencia sequencia tecnico tecnica tecnicos tecnicas estrategica estrategico relatorio
relatorios diretorio diretorios historico unico unica publicos publicas proximo
numero endereco enderecos servico servicos negocio formulario calendario video videos dominio
dominios curriculo titulacao academica participacao honorario honorarios exito beneficio
beneficios previdenciario previdenciaria previdenciarios previdenciarias pericia medica mes
tres apos sao nao alem ate nivel niveis codigo etica pratica carater judiciario decisao
inferencia residencia opcao padrao homonimo homonimos estatica organico posicao indexacao praca
botao horario prioritario prioritarias valido construcao reconstrucao reconstruido remocao
aplicacao anuncio anuncios expansao atencao conteudo conteudos interacoes colaboracoes
colaboracao estagio explicacao ninguem espaco vinculo operacao comeca comecar execucao util
dificil rastreavel parcelavel indexavel indexaveis responsavel responsaveis incluido incluida
qualificacao genericas serie familia constrular
""".split()


def validar(nome, html):
    erros = []
    corpo = re.sub(r'<style>.*?</style>', '', html, flags=re.S)
    texto = re.sub(r'<[^>]+>', ' ', corpo)
    css_only = html.split('<style>')[-1].split('</style>')[0]
    visivel_txt = texto

    for termo in ['Joana', 'ladeguste', 'Elora', 'PECBR', 'Flavia Melow', 'Sinfonya', 'sinfonya',
                  'Pedro Brand']:
        if termo.lower() in corpo.lower():
            erros.append(f'residuo de outro cliente: {termo}')
    for p in PALAVRAS_SEM_ACENTO:
        if re.search(r'\b' + re.escape(p) + r'\b', visivel_txt):
            erros.append(f'palavra sem acento no texto visivel: {p}')
    if re.findall(r'<[^>]*[“”‘’][^>]*>', corpo):
        erros.append('aspas curvas dentro de tag')
    if '&mdash;' in corpo or '—' in texto or '–' in texto:
        erros.append('travessao encontrado')
    if 'background-clip' in css_only:
        erros.append('gradient text no css')
    if [x for x in re.findall(r'border-left:\s*([\d.]+)pt', css_only) if float(x) > 0.76]:
        erros.append('border-left acima de 1px')
    if html.count('<section') != html.count('</section>'):
        erros.append('section desbalanceada')
    if html.count('<table') != html.count('</table>'):
        erros.append('table desbalanceada')
    if '<meta name="description"' not in html:
        erros.append('sem meta description')
    erros = sorted(set(erros))
    print(f'  {nome}: {len(html)/1024:.0f} KB, {html.count("<section")} paginas  |  '
          + ('validacao ok' if not erros else f'PROBLEMAS: {erros}'))
    return erros


if __name__ == '__main__':
    print('gerando propostas...')
    todos = []
    for nome, fn in [('DebemSantos', build_debem), ('DiegoSantos', build_diego),
                     ('SuziellenAleixo', build_suziellen)]:
        todos += validar(nome, fn())
    print('RESULTADO:', 'tudo ok' if not todos else sorted(set(todos)))
