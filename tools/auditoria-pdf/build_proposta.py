# -*- coding: utf-8 -*-
"""Proposta de presenca digital do Grupo Sinfonya: o que esta errado e quanto custa arrumar.
Valores de gestao e anuncios vem da Proposta Comercial de 05/08/2026. Os demais sao propostos aqui."""
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
    _n[0] += 1
    f = f'<div class="fecho">{fecho}</div>' if fecho else ''
    paginas.append(
        f'<section class="pagina">'
        f'<div class="cab"><span class="cab-esq">Grupo Sinfonya &middot; Or&aacute;culo Tecnologia</span>'
        f'<span class="cab-dir">{secao}</span></div>{corpo}{f}'
        f'<div class="rod"><span>Presen&ccedil;a digital, plano e investimento</span><span>{_n[0]}</span></div>'
        f'</section>')


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
        tds = ''
        for i, c in enumerate(l):
            k = []
            if i == 0: k.append('forte')
            if alinha.get(i) == 'num': k.append('num')
            cl = f' class="{" ".join(k)}"' if k else ''
            tds += f'<td{cl}>{c}</td>'
        tr += f'<tr>{tds}</tr>'
    f = f'<p class="fonte">{fonte}</p>' if fonte else ''
    return f'<table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>{f}'


def defs(itens):
    d = ''.join(f'<div class="def"><div class="def-r">{r}</div><div class="def-d">{t}</div></div>'
                for r, t in itens)
    return f'<div class="defs">{d}</div>'


def nota(titulo, *ps):
    return f'<div class="nota"><b>{titulo}</b>{"".join(f"<p>{x}</p>" for x in ps)}</div>'


# ============================================================ CAPA
paginas.append(f'''<section class="pagina capa">
<div class="capa-topo">
  <img src="data:image/png;base64,{LOGO}" alt="Or&aacute;culo">
  <div class="capa-meta">Documento confidencial<br>{DATA}</div>
</div>
<div class="capa-corpo">
  <div class="capa-kicker">Grupo Sinfonya Turismo e Formaturas</div>
  <h1>O que est&aacute; errado na presen&ccedil;a digital, e quanto custa arrumar</h1>
  <p class="capa-lede">Auditamos tudo que existe sobre a Sinfonya na internet e encontramos onze problemas.
  Este documento lista cada um deles, diz qual servi&ccedil;o resolve e qual o investimento. S&atilde;o seis
  frentes: gest&atilde;o das redes sociais, tr&aacute;fego pago, presen&ccedil;a no Google, site, cadastro de
  clientes e atendimento automatizado no WhatsApp.</p>
</div>
<div class="capa-rodape">
  <div class="capa-stat"><b>11</b><span>problemas encontrados na auditoria</span></div>
  <div class="capa-stat"><b>6</b><span>frentes de trabalho propostas</span></div>
  <div class="capa-stat"><b>22.900</b><span>reais de entrada, uma vez</span></div>
  <div class="capa-stat"><b>6.900</b><span>reais por m&ecirc;s, tudo incluso</span></div>
</div>
</section>''')

# ============================================================ 2. O QUE ENCONTRAMOS
pag('O diagn&oacute;stico', f'''
<h2 class="titulo">Os onze problemas que a auditoria encontrou</h2>
<p class="lede">Cada linha abaixo &eacute; um achado verificado em 6 de agosto de 2026, com a fonte registrada
no documento completo da auditoria. A coluna da direita diz o que aquilo custa hoje para a Sinfonya.</p>
{tabela(['O que encontramos', 'O que isso custa'], [
  ('Os quatro endere&ccedil;os de site da marca nunca foram comprados', 'Um concorrente pode levar o endere&ccedil;o que o Google anuncia como o site oficial da Sinfonya'),
  ('A ficha da empresa no Google tem nota 4,6 e 55 avalia&ccedil;&otilde;es, e ningu&eacute;m assumiu', 'A empresa n&atilde;o responde nenhuma avalia&ccedil;&atilde;o e n&atilde;o controla o que aparece'),
  ('A empresa n&atilde;o aparece em nenhuma das cinco buscas que vendem viagem', 'Quem procura excurs&atilde;o ou formatura no Google encontra o concorrente'),
  ('O Reclame Aqui tem 16 reclama&ccedil;&otilde;es e 5 sem resposta, com m&eacute;dia de 20 dias', '&Eacute; o segundo resultado do Google para o nome da marca'),
  ('N&atilde;o existe site', 'Nenhuma p&aacute;gina pr&oacute;pria para provar quinze anos de opera&ccedil;&atilde;o antes da compra'),
  ('Sete n&uacute;meros de WhatsApp em circula&ccedil;&atilde;o, sem hist&oacute;rico comum', 'Cliente que volta pelo n&uacute;mero errado recome&ccedil;a a conversa do zero'),
  ('Pergunta de pre&ccedil;o leva 4,6 horas para ser respondida', 'Elogio &eacute; respondido em 0,7 hora. A prioridade est&aacute; invertida'),
  ('Duas das cinco contas est&atilde;o paradas, somando 42 mil seguidores', 'Audi&ecirc;ncia grande e sem pauta, inclusive a vertical de maior ticket'),
  ('A conta que vende Israel 2027 n&atilde;o tem link, e-mail nem telefone', 'O produto mais caro do grupo n&atilde;o tem por onde comprar'),
  ('A conta de casamentos converte por um formul&aacute;rio do Google', '16.438 seguidores de ticket alto atendidos por um formul&aacute;rio gratuito'),
  ('O Linktree tem dois dos cinco links quebrados', 'Um deles &eacute; o bot&atilde;o do site e o outro &eacute; a conta crist&atilde;'),
], 'Auditoria de presen&ccedil;a digital do Grupo Sinfonya, coleta de 6 de agosto de 2026. O documento completo traz a fonte de cada n&uacute;mero.', compacta=True)}
''', 'Nenhum desses problemas &eacute; de produto ou de pre&ccedil;o. <span class="azul">S&atilde;o todos de estrutura digital.</span>')

# ============================================================ 3. PAGINA MESTRA
pag('Plano e pre&ccedil;o', f'''
<h2 class="titulo">O que resolve cada problema, e quanto custa</h2>
<p class="lede">Seis frentes cobrem os onze problemas. Quatro delas s&atilde;o obras de entrada, pagas uma vez.
Duas s&atilde;o trabalho cont&iacute;nuo, pagas por m&ecirc;s.</p>
{tabela(['Frente', 'Que problema resolve', 'Investimento'], [
  ('__grupo__', 'Entrada, pagamento &uacute;nico'),
  ('Cria&ccedil;&atilde;o de site', 'Falta de site, aus&ecirc;ncia nas buscas, bot&atilde;o quebrado do Google, prova de exist&ecirc;ncia', '12.000'),
  ('Atendimento no WhatsApp', 'As 4,6 horas de espera e a pergunta de pre&ccedil;o sem resposta', '7.500'),
  ('Cadastro de clientes', 'Os sete n&uacute;meros sem hist&oacute;rico comum e o cliente que recome&ccedil;a do zero', '5.500'),
  ('Google e reputa&ccedil;&atilde;o, instala&ccedil;&atilde;o', 'Ficha sem dono, 5 reclama&ccedil;&otilde;es abertas, endere&ccedil;os de site livres', '1.800'),
  ('Rastreamento e automa&ccedil;&atilde;o', 'Nenhuma conversa de WhatsApp com origem conhecida', '500'),
  ('__grupo__', 'Mensal'),
  ('Gest&atilde;o das redes e tr&aacute;fego pago', 'Contas paradas, links quebrados, contas sem contato, alcance travado', '5.500'),
  ('SEO e presen&ccedil;a no Google', 'Aus&ecirc;ncia nas cinco buscas e reputa&ccedil;&atilde;o sem acompanhamento', '2.500'),
], 'Valores em reais, acrescidos de imposto. A gest&atilde;o das redes e o tr&aacute;fego pago seguem o plano Crescimento da proposta de 5 de agosto de 2026. As demais frentes s&atilde;o precificadas neste documento.')}
{nota('Fechando as seis frentes juntas',
 'Entrada: <b>22.900 reais</b> em vez de 27.300, uma economia de 4.400. Mensal: <b>6.900 reais</b> em vez de 8.000, '
 'uma economia de 1.100 por m&ecirc;s, ou 13.200 no ano.',
 'A entrada pode ser parcelada em at&eacute; doze vezes, o que d&aacute; 1.908 reais por m&ecirc;s.')}
''', 'Sete dos onze problemas <span class="azul">se resolvem na primeira semana, antes de qualquer produ&ccedil;&atilde;o de conte&uacute;do.</span>')

# ============================================================ 4. REDES SOCIAIS
pag('Redes sociais', f'''
<h2 class="titulo">Gest&atilde;o das redes sociais</h2>
<p class="lede">O grupo mant&eacute;m cinco contas e sustenta duas. A conta de turismo publica dois posts por
dia para uma base que reage como se tivesse 1.300 pessoas. A de formaturas engaja vinte e tr&ecirc;s vezes mais
e parou de publicar.</p>
{defs([
  ('O que est&aacute; errado hoje',
   'Duas contas paradas somando 42 mil seguidores, cinco perfis sem cidade e endere&ccedil;o preenchidos, a conta de maior ticket sem nenhum link, '
   'a de casamentos convertendo por formul&aacute;rio do Google e dois links quebrados no Linktree.'),
  ('O que entregamos',
   'Gest&atilde;o das contas com calend&aacute;rio aprovado, configura&ccedil;&atilde;o completa dos perfis, reescrita das bios, destaques reorganizados, '
   '28 publica&ccedil;&otilde;es de feed por m&ecirc;s, 12 Reels gravados e editados, 5 stories por semana em cada perfil, uma cobertura ao vivo por m&ecirc;s '
   'e uma parceria com creator por temporada.'),
  ('Como medimos',
   'Relat&oacute;rio mensal consolidado, relat&oacute;rio de convers&atilde;o com origem das conversas e reuni&atilde;o estrat&eacute;gica mensal.'),
])}
{tabela(['Plano', 'Por m&ecirc;s', 'O que muda'], [
  ('Essencial', '3.500', 'Arruma a base e devolve dire&ccedil;&atilde;o editorial, sem an&uacute;ncio e sem rastreio'),
  ('Crescimento', '<b>5.500</b>', 'Plano indicado. Executa o ciclo inteiro, com an&uacute;ncio e caminho medido at&eacute; o or&ccedil;amento'),
  ('Autoridade', '7.500', 'Entra depois que o ciclo provar resultado, com TikTok, contas sat&eacute;lite e painel'),
], 'Valores da Proposta Comercial de 5 de agosto de 2026, cobrindo as duas contas principais no mesmo contrato. Contratadas em separado, sairiam por 4.000, 7.000 e 10.000.')}
<p class="texto">Produ&ccedil;&atilde;o extra de v&iacute;deo, quando houver embarque ou famtour fora do
calend&aacute;rio, custa <b>800 reais por pacote</b> de edi&ccedil;&atilde;o.</p>
''', 'A conta de formaturas j&aacute; provou o que funciona. <span class="azul">Falta religar e repetir na conta de turismo.</span>')

# ============================================================ 5. TRAFEGO PAGO
pag('Tr&aacute;fego pago', f'''
<h2 class="titulo">Tr&aacute;fego pago</h2>
<p class="lede">Hoje a Sinfonya n&atilde;o anuncia, e tamb&eacute;m n&atilde;o teria para onde mandar o clique.
Por isso o an&uacute;ncio entra depois do site e do rastreamento, e n&atilde;o antes.</p>
{defs([
  ('Por que n&atilde;o come&ccedil;a agora',
   'Sem site e sem ficha do Google assumida, o an&uacute;ncio entrega gente numa caixa de mensagem que responde em horas. '
   'Investir m&iacute;dia nessa condi&ccedil;&atilde;o paga para perder contato.'),
  ('O que entregamos',
   'Meta Ads no Instagram e no Facebook, at&eacute; quatro campanhas ativas ao mesmo tempo, otimiza&ccedil;&atilde;o semanal, '
   'seis criativos produzidos por m&ecirc;s e segmenta&ccedil;&atilde;o por regi&atilde;o de sa&iacute;da e por escola.'),
  ('O que isso ataca',
   'A aus&ecirc;ncia da marca nas buscas de excurs&atilde;o e formatura, e a falta de origem conhecida das conversas de WhatsApp.'),
])}
{tabela(['Item', 'Valor', 'Como funciona'], [
  ('Gest&atilde;o das campanhas', 'inclusa no plano Crescimento', 'N&atilde;o h&aacute; cobran&ccedil;a &agrave; parte de gest&atilde;o de m&iacute;dia'),
  ('Verba de an&uacute;ncios', '1.500 a 3.000 por m&ecirc;s', 'Paga diretamente &agrave; plataforma, com relat&oacute;rio de aplica&ccedil;&atilde;o todo m&ecirc;s'),
  ('Criativos extras', '800 por pacote', 'Quando a temporada pedir mais que os seis criativos do plano'),
], 'Valores da Proposta Comercial de 5 de agosto de 2026. A verba de an&uacute;ncios n&atilde;o passa pela Or&aacute;culo.')}
{nota('A verba come&ccedil;a baixa de prop&oacute;sito',
 'Os primeiros 1.500 reais por m&ecirc;s servem para descobrir qual destino, qual formato e qual regi&atilde;o de sa&iacute;da respondem. '
 'S&oacute; depois disso faz sentido subir. A decis&atilde;o de aumentar sai do relat&oacute;rio de convers&atilde;o, n&atilde;o de calend&aacute;rio.')}
''')

# ============================================================ 6. SEO
pag('Google', f'''
<h2 class="titulo">SEO e presen&ccedil;a no Google</h2>
<p class="lede">Testamos cinco buscas que correspondem ao que a Sinfonya vende. A marca n&atilde;o apareceu em
nenhuma. Quase todo concorrente que ocupa o topo dessas buscas tem site pr&oacute;prio com p&aacute;gina do
destino.</p>
{defs([
  ('O que est&aacute; errado hoje',
   'Aus&ecirc;ncia total em cinco buscas comerciais. A ficha da empresa no Google existe, tem nota 4,6 com 55 avalia&ccedil;&otilde;es e '
   'ningu&eacute;m assumiu. O Reclame Aqui &eacute; o segundo resultado para o nome da marca, com cinco reclama&ccedil;&otilde;es sem resposta.'),
  ('Entrada, uma vez',
   'Compra dos quatro endere&ccedil;os de site da marca, tomada de posse da ficha do Google com valida&ccedil;&atilde;o de endere&ccedil;o, '
   'corre&ccedil;&atilde;o dos cadastros p&uacute;blicos divergentes, verifica&ccedil;&atilde;o do perfil no Reclame Aqui e resposta &agrave;s cinco reclama&ccedil;&otilde;es abertas.'),
  ('Mensal',
   'P&aacute;gina de destino nova ou reescrita a cada m&ecirc;s, acompanhamento de posi&ccedil;&atilde;o nas buscas que vendem, publica&ccedil;&otilde;es e fotos na ficha do Google, '
   'resposta &agrave;s avalia&ccedil;&otilde;es e ao Reclame Aqui, e relat&oacute;rio de onde a marca aparece.'),
])}
{tabela(['Item', 'Valor'], [
  ('Instala&ccedil;&atilde;o, uma vez', '1.800'),
  ('Acompanhamento mensal', '2.500 por m&ecirc;s'),
  ('Endere&ccedil;os de site, custo direto', 'cerca de 40 reais por endere&ccedil;o ao ano, pagos ao Registro.br'),
], 'Valores propostos neste documento. O custo do Registro.br &eacute; repassado sem margem.', compacta=True)}
''', 'Assumir a ficha do Google leva dias <span class="azul">e devolve &agrave; empresa 55 avalia&ccedil;&otilde;es que j&aacute; existem.</span>')

# ============================================================ 7. SITE
pag('Site', f'''
<h2 class="titulo">Cria&ccedil;&atilde;o do site</h2>
<p class="lede">O site resolve tr&ecirc;s problemas de uma vez: a prova de que a empresa existe, a entrada nas
buscas do Google e o bot&atilde;o quebrado da ficha do Google. N&atilde;o precisa ser grande, precisa existir e
ser encontrado.</p>
{defs([
  ('P&aacute;gina inicial',
   'Quinze anos de opera&ccedil;&atilde;o, 500 mil passageiros, CNPJ, os dois endere&ccedil;os f&iacute;sicos, o v&iacute;nculo com a ABAV-DF e as avalia&ccedil;&otilde;es do Google. '
   '&Eacute; a p&aacute;gina que responde &agrave; d&uacute;vida de quem nunca comprou.'),
  ('Uma p&aacute;gina por destino',
   'Caldas Novas, Rio Quente, Porto Seguro, Fortaleza, Natal, Gramado, Foz, Madri e Israel 2027, com sa&iacute;das do m&ecirc;s, pre&ccedil;o, '
   'parcelamento e o que est&aacute; inclu&iacute;do. &Eacute; a p&aacute;gina que disputa a busca.'),
  ('Uma p&aacute;gina por linha',
   'Formaturas, casamentos, turismo crist&atilde;o e a filial de Patos de Minas. Resolve a fragmenta&ccedil;&atilde;o das cinco contas num endere&ccedil;o s&oacute;.'),
  ('Formul&aacute;rio ligado ao cadastro',
   'O pedido de or&ccedil;amento cai direto no cadastro de clientes, com destino, data e cidade de sa&iacute;da j&aacute; preenchidos.'),
])}
{tabela(['Op&ccedil;&atilde;o', 'Valor', 'O que inclui'], [
  ('Site essencial', '1.000', 'Uma landing page: p&aacute;gina &uacute;nica com a prova de exist&ecirc;ncia e o bot&atilde;o de WhatsApp. N&atilde;o disputa a busca'),
  ('Site completo', '<b>12.000</b>', 'Op&ccedil;&atilde;o indicada. Acrescenta nove p&aacute;ginas de destino, que s&atilde;o as que disputam a busca'),
  ('Hospedagem e e-mail', '150 por m&ecirc;s', 'Inclui as caixas de e-mail no endere&ccedil;o pr&oacute;prio, no lugar do gmail'),
], 'Valores propostos neste documento. Prazo de entrega de 4 a 7 semanas conforme a op&ccedil;&atilde;o.')}
''', 'O site &eacute; o &uacute;nico ativo registrado no nome da empresa <span class="azul">e o &uacute;nico que sobrevive a uma mudan&ccedil;a de rede social.</span>')

# ============================================================ 8. CRM
pag('Cadastro de clientes', f'''
<h2 class="titulo">Cadastro de clientes, o CRM</h2>
<p class="lede">A empresa tem sete n&uacute;meros de WhatsApp em circula&ccedil;&atilde;o e nenhum lugar onde o
hist&oacute;rico do cliente fique guardado. Quem atendeu &eacute; quem lembra, e o hist&oacute;rico mora no
aparelho.</p>
{defs([
  ('Uma caixa, v&aacute;rios atendentes',
   'Os n&uacute;meros continuam existindo, mas as conversas caem todas na mesma tela. Qualquer atendente v&ecirc; o hist&oacute;rico completo do cliente, '
   'independente de por qual n&uacute;mero ele entrou.'),
  ('Cada conversa vira ficha',
   'Destino, data, quantas pessoas, cidade de sa&iacute;da e respons&aacute;vel. O que hoje est&aacute; na cabe&ccedil;a do atendente passa a ser campo preenchido.'),
  ('Ningu&eacute;m depende da pr&oacute;pria mem&oacute;ria',
   'Or&ccedil;amento enviado e sem resposta em 48 horas vira tarefa para algu&eacute;m cobrar. &Eacute; onde mais se perde venda numa opera&ccedil;&atilde;o de pacote parcelado.'),
  ('Vender de novo para quem j&aacute; viajou',
   'Com cliente cadastrado por destino e data, fica poss&iacute;vel oferecer a pr&oacute;xima viagem na hora certa e montar um programa de indica&ccedil;&atilde;o. '
   '&Eacute; o p&uacute;blico mais barato que a empresa tem.'),
])}
{tabela(['Item', 'Valor'], [
  ('Implanta&ccedil;&atilde;o, uma vez', '5.500'),
  ('Mensalidade da ferramenta', 'cerca de 320 por m&ecirc;s para quatro atendentes, paga ao fornecedor'),
  ('Acompanhamento', 'incluso no contrato mensal'),
], 'A implanta&ccedil;&atilde;o &eacute; proposta neste documento e cobre juntar os n&uacute;meros num lugar s&oacute;, carregar os clientes j&aacute; atendidos, montar as etapas da venda, conectar Instagram e WhatsApp e treinar a equipe. A mensalidade da ferramenta segue o pre&ccedil;o de tabela do fornecedor escolhido, consultado em 06/08/2026.', compacta=True)}
''')

# ============================================================ 9. BOT
pag('WhatsApp', f'''
<h2 class="titulo">Atendimento automatizado no WhatsApp</h2>
<p class="lede">Medimos o tempo entre a pergunta e a resposta da empresa nos coment&aacute;rios. Pergunta de
pre&ccedil;o espera 4,6 horas. Elogio espera 0,7 hora. O atendimento autom&aacute;tico existe para tirar essa
espera do caminho de quem quer comprar.</p>
{nota('Responder na hora n&atilde;o custa mensagem',
 'Quando o cliente manda mensagem para a empresa, abre-se uma janela de 24 horas em que toda resposta &eacute; gratuita. '
 'A Meta confirma isso na documenta&ccedil;&atilde;o oficial. O custo por mensagem s&oacute; aparece quando &eacute; a empresa que inicia a conversa.')}
{defs([
  ('O que o atendimento autom&aacute;tico faz',
   'Responde na hora, identifica de qual conta ou an&uacute;ncio a pessoa veio, pergunta destino, data, quantas pessoas e cidade de sa&iacute;da, '
   'entrega pre&ccedil;o e parcelamento do que j&aacute; &eacute; p&uacute;blico e passa a conversa para o atendente com a ficha preenchida.'),
  ('E depois da venda',
   'Lembrete de parcela, documenta&ccedil;&atilde;o da viagem, hor&aacute;rio de embarque e pesquisa depois do retorno. &Eacute; o tipo de mensagem mais barato '
   'e o que mais reduz a queixa de falta de contato que aparece no Reclame Aqui.'),
])}
{tabela(['Item', 'Valor'], [
  ('Implanta&ccedil;&atilde;o, uma vez', '7.500'),
  ('Sistema de atendimento', 'cerca de 350 por m&ecirc;s, pago ao fornecedor'),
  ('Mensagens de resposta', 'gratuitas, dentro das 24 horas'),
  ('Lembretes e p&oacute;s-venda', 'R$ 0,04 a R$ 0,05 por mensagem enviada'),
  ('Campanha de oferta', 'R$ 0,31 a R$ 0,38 por mensagem enviada'),
], 'A implanta&ccedil;&atilde;o &eacute; proposta neste documento. As faixas por mensagem seguem as tabelas p&uacute;blicas de parceiros brasileiros do WhatsApp em 06/08/2026 e s&atilde;o pagas &agrave; plataforma, n&atilde;o &agrave; Or&aacute;culo.', compacta=True)}
<p class="texto">Para liberar a conta oficial, a Meta exige CNPJ ativo e nome, endere&ccedil;o e telefone batendo
entre si. <b>Isso depende de resolver antes o CNPJ inapto e a diverg&ecirc;ncia de endere&ccedil;o</b>, que
est&atilde;o na frente de instala&ccedil;&atilde;o do Google.</p>
''', 'Atender quem chega <span class="azul">n&atilde;o custa mensagem. Custa configurar uma vez.</span>')

# ============================================================ 10. INVESTIMENTO
pag('Investimento', f'''
<h2 class="titulo">O investimento, somado</h2>
<p class="lede">A coluna da esquerda &eacute; o que cada frente custaria contratada isoladamente. A da direita
&eacute; o valor fechando as seis juntas, que &eacute; como recomendamos come&ccedil;ar.</p>
{tabela(['', 'Por frente', 'Pacote &uacute;nico'], [
  ('__grupo__', 'Entrada, uma vez'),
  ('Cria&ccedil;&atilde;o de site, op&ccedil;&atilde;o completa', '12.000', ''),
  ('Atendimento no WhatsApp', '7.500', ''),
  ('Cadastro de clientes', '5.500', ''),
  ('Google e reputa&ccedil;&atilde;o', '1.800', ''),
  ('Rastreamento e automa&ccedil;&atilde;o', '500', ''),
  ('Total de entrada', '<b>27.300</b>', '<b>22.900</b>'),
  ('__grupo__', 'Mensal, com a Or&aacute;culo'),
  ('Gest&atilde;o das redes e tr&aacute;fego pago', '5.500', ''),
  ('SEO e presen&ccedil;a no Google', '2.500', ''),
  ('Total mensal', '<b>8.000</b>', '<b>6.900</b>'),
], alinha={1: 'num', 2: 'num'}, compacta=True)}
<h3 class="sub">O que &eacute; pago a terceiros, e n&atilde;o &agrave; Or&aacute;culo</h3>
{tabela(['Item', 'Quanto'], [
  ('Ferramenta de cadastro de clientes', 'cerca de 320'),
  ('Sistema de atendimento no WhatsApp', 'cerca de 350'),
  ('Hospedagem e e-mail no endere&ccedil;o pr&oacute;prio', 'cerca de 150'),
  ('Verba de an&uacute;ncios, direto &agrave; plataforma', '1.500 a 3.000'),
  ('Endere&ccedil;os de site, no Registro.br', 'cerca de 160 por ano, somados os quatro'),
], 'Valores em reais, acrescidos de imposto onde couber. Os itens acima s&atilde;o pagos diretamente aos fornecedores, com relat&oacute;rio de aplica&ccedil;&atilde;o todo m&ecirc;s.', compacta=True)}
{nota('O que a economia do pacote representa',
 'Na entrada, <b>4.400 reais</b>. No mensal, <b>1.100 reais por m&ecirc;s</b>, ou 13.200 no primeiro ano. '
 'A entrada pode ser parcelada em at&eacute; doze vezes, o que d&aacute; 1.908 reais por m&ecirc;s.')}
''')

# ============================================================ 11. CRONOGRAMA E CONDICOES
pag('Como come&ccedil;a', f'''
<h2 class="titulo">Como as seis frentes entram, e em que ordem</h2>
<p class="lede">A ordem n&atilde;o &eacute; por tamanho de entrega. &Eacute; pelo que trava mais neg&oacute;cio
com menos trabalho, e pelo que uma frente exige da outra para funcionar.</p>
{defs([
  ('Semana 1',
   'Compra dos quatro endere&ccedil;os de site, tomada de posse da ficha do Google, corre&ccedil;&atilde;o dos dois links quebrados do Linktree, '
   'contato na bio da conta crist&atilde;, troca do formul&aacute;rio do Google na conta de casamentos, cidade e endere&ccedil;o preenchidos nas cinco contas '
   'e migra&ccedil;&atilde;o da conta de formaturas para conta de empresa. <b>Sete dos onze problemas se resolvem aqui.</b>'),
  ('M&ecirc;s 1',
   'Verifica&ccedil;&atilde;o do perfil no Reclame Aqui e resposta &agrave;s cinco reclama&ccedil;&otilde;es abertas. In&iacute;cio da gest&atilde;o das redes com calend&aacute;rio aprovado. '
   'Instala&ccedil;&atilde;o do rastreamento. Come&ccedil;a a constru&ccedil;&atilde;o do site.'),
  ('M&ecirc;s 2',
   'Site no ar com as p&aacute;ginas de destino. Cadastro de clientes implantado, com os sete n&uacute;meros unificados e a base antiga carregada. '
   'Primeira p&aacute;gina de destino otimizada para busca.'),
  ('M&ecirc;s 3',
   'Atendimento autom&aacute;tico no WhatsApp ligado, j&aacute; conectado ao cadastro. Entrada do tr&aacute;fego pago, agora com site e rastreio prontos. '
   'Primeiro relat&oacute;rio ligando publica&ccedil;&atilde;o, clique e conversa.'),
])}
<h3 class="sub">Condi&ccedil;&otilde;es comerciais</h3>
<p class="texto">Contrato mensal, sem fidelidade no primeiro m&ecirc;s. Entrada parcel&aacute;vel em at&eacute;
doze vezes. A verba de an&uacute;ncios e as mensalidades de ferramenta s&atilde;o pagas diretamente aos
fornecedores, com relat&oacute;rio de aplica&ccedil;&atilde;o todo m&ecirc;s. Valores em reais, acrescidos de
imposto. Esta proposta &eacute; v&aacute;lida por 30 dias a partir da data de envio.</p>
''', 'A primeira semana n&atilde;o depende de contrato longo <span class="azul">nem de produzir uma &uacute;nica pe&ccedil;a de conte&uacute;do.</span>')

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
  oficial e quem responde as cinco reclama&ccedil;&otilde;es abertas.</p>
  <div class="fim-linhas">
    <div class="fim-linha"><b>Reuni&atilde;o</b><span>30 minutos, presencial em Bras&iacute;lia ou por v&iacute;deo</span></div>
    <div class="fim-linha"><b>Primeira semana</b><span>Sete dos onze problemas resolvidos, sem produzir conte&uacute;do</span></div>
    <div class="fim-linha"><b>Entrada</b><span>22.900 reais, parcel&aacute;vel em at&eacute; 12 vezes de 1.908</span></div>
    <div class="fim-linha"><b>Mensal</b><span>6.900 reais, com as seis frentes no mesmo contrato</span></div>
  </div>
</div>
<div class="fim-rodape">
  <div><b>Or&aacute;culo Tecnologia</b>Baseado na auditoria de presen&ccedil;a digital<br>de 6 de agosto de 2026</div>
  <div>Documento confidencial, destinado ao Grupo Sinfonya<br>V&aacute;lido por 30 dias a partir do envio</div>
</div>
</section>''')

# ============================================================ MONTAGEM
html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Presen&ccedil;a Digital, Plano e Investimento, Grupo Sinfonya</title>
<meta name="description" content="O que esta errado na presenca digital do Grupo Sinfonya e quanto custa arrumar: gestao de redes, trafego pago, SEO, site, CRM e atendimento no WhatsApp. Oraculo Tecnologia, agosto de 2026.">
<style>{FIRA}</style>
<style>{CSS}</style>
</head>
<body>
{''.join(paginas)}
</body>
</html>'''

destino = os.path.join(RAIZ, 'SinfonyaGrupo', 'Proposta-Presenca-Digital.html')
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
if corpo.count('&mdash;') or '—' in re.sub(r'<[^>]+>', ' ', corpo): erros.append('travessao encontrado')
if 'class="kpis"' in corpo: erros.append('KPI strip no corpo')
if [x for x in re.findall(r'border-left:\s*([\d.]+)pt', css_only) if float(x) > 0.76]: erros.append('border-left acima de 1px')
if html.count('<section') != html.count('</section>'): erros.append('section desbalanceada')
print('VALIDACAO:', 'ok, sem problemas' if not erros else erros)
