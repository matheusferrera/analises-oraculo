# -*- coding: utf-8 -*-
"""Proposta comercial de Dr. Pedro Brandão, cirurgião plástico em Brasília. Mesmo formato
editorial A4 usado nas propostas da Debem e Santos, Diego Santos e Suziellen Aleixo
(tools/auditoria-pdf/build_propostas_debem.py), reaproveitando os mesmos helpers.

Todos os números citados vêm da 2ª coleta da auditoria de presença digital, de 17/08/2026,
guardada em DrPedroBrandao/data/presenca-digital-20260817.json e no próprio
DrPedroBrandao/Analise-Presenca-Digital.html.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_propostas_debem as bp

bp.DATA = '17 de agosto de 2026'

Doc = bp.Doc
tabela = bp.tabela
defs = bp.defs
nota = bp.nota
duas_colunas = bp.duas_colunas
escopo = bp.escopo
planos_com_escopo = bp.planos_com_escopo
RAIZ = bp.RAIZ

CONDICOES_PEDRO = (
    '<h3 class="sub">Condições comerciais</h3>'
    '<p class="texto">Contrato mensal, sem fidelidade no primeiro mês nas vertentes de redes '
    'sociais e tráfego pago. O investimento da vertente de tecnologia é definido numa chamada '
    'de escopo de 30 minutos, sem custo, antes do contrato, dentro da faixa de entrada '
    'informada. A entrada de qualquer vertente pode ser parcelada em até doze vezes. Onboarding '
    'completo em 7 dias a partir da assinatura. A verba de impulsionamento e as mensalidades de '
    'ferramenta são pagas diretamente aos fornecedores, com relatório de aplicação todo mês. '
    'Valores em reais, acrescidos de imposto. Esta proposta é válida por 30 dias a partir da '
    'data de envio.</p>')

CFM_LEDE = (
    'A publicidade médica tem norma própria, ainda mais relevante em cirurgia plástica. Todas '
    'as peças produzidas nesta proposta seguem a Resolução CFM nº 2.336/2023, que atualizou as '
    'regras de publicidade na medicina em 2023 e trouxe permissões que antes não existiam, '
    'entre elas o uso de fotos de antes e depois com critério.')

CFM_PERMITE = [
    'Divulgar nome, CRM, RQE, áreas de atuação e canais de contato nas redes próprias.',
    'Fotos de antes e depois, com texto educativo, paciente não identificável, imagem sem '
    'edição e mostrando resultados satisfatórios e também os que não foram, incluindo '
    'complicações.',
    'Divulgação de valor de consulta e de formas de pagamento, e anúncio de desconto em '
    'campanha promocional, desde que sem venda casada.',
    'Repostagem de elogio de paciente, em tom sóbrio, sem adjetivo de superioridade.',
    'Conteúdo educativo sobre procedimento, indicação, recuperação e cuidado pós-operatório.',
]

CFM_VEDA = [
    'Garantir, prometer ou insinuar resultado, mesmo de forma indireta.',
    'Conteúdo sensacionalista, enganoso ou com dado estatístico adulterado.',
    'Expor imagem de consulta ou de procedimento em andamento.',
    'Manipular ou melhorar a foto de antes e depois com filtro ou edição.',
    'Ensinar técnica cirúrgica ao público leigo, ou insinuar descoberta milagrosa.',
]

CFM_NOTA = nota(
    'O que isso muda na prática',
    'O antes e depois volta a ser um ativo legítimo, mas com regra: par de fotos sem edição, '
    'paciente não identificável, texto educativo ao lado e variedade de casos, não só os '
    'melhores. O anúncio pago pode informar valor de consulta, mas nenhuma peça promete '
    'resultado, porque isso continua vedado independente da plataforma.',
    'Cada peça passa por conferência com a norma antes de ir ao ar, com registro do que foi '
    'ajustado. A responsabilidade ética permanece do médico inscrito, e a conferência da '
    'Oráculo não a substitui.')

FONTE_DIAGNOSTICO = (
    'Auditoria de presença digital do Dr. Pedro Brandão, coletas de 06 e 17/08/2026: Instagram '
    '@drpedrobrandaocp pela API interna com sessão autenticada, histórico integral de 357 '
    'publicações; Google Search e Perfil da Empresa; drpedrobrandao.com.br e '
    'l.drpedrobrandao.com.br; Doctoralia, Facebook, LinkedIn e YouTube.')

CFM_FONTE = (
    'Resolução CFM nº 2.336, de 1º de setembro de 2023, que dispõe sobre a publicidade médica '
    'e revoga a Resolução CFM nº 1.974/2011. Leitura aplicada ao caso de um cirurgião plástico '
    'com clínica própria em Brasília, sem caráter de parecer ético.')


def pagina_cfm(doc):
    corpo = (
        '<h2 class="titulo">O que a Resolução CFM 2.336/2023 permite, e o que ela veda</h2>'
        f'<p class="lede">{CFM_LEDE}</p>'
        + duas_colunas('A norma permite', CFM_PERMITE, 'A norma veda', CFM_VEDA)
        + CFM_NOTA
        + f'<p class="fonte">{CFM_FONTE}</p>'
    )
    doc.pag('Publicidade e CFM', corpo,
            'Antes e depois voltou a ser permitido, '
            '<span class="azul">com paciente não identificável e texto educativo ao lado.</span>')


def contracapa_pedro(doc, h2, lede, linhas, rodape_esq):
    """Mesma contracapa do Doc, mas sem o "destinado à Debem e Santos Advogados Associados"
    fixo no rodapé (bug do helper compartilhado, presente até no PDF já entregue do Diego
    Santos). Aqui o destinatário correto é o Dr. Pedro Brandão."""
    ls = ''.join(f'<div class="fim-linha"><b>{a}</b><span>{b}</span></div>' for a, b in linhas)
    doc.bruta(f'''<section class="pagina fim">
<div class="capa-topo">
  <img src="data:image/png;base64,{bp.LOGO}" alt="Oráculo">
  <div class="capa-meta">Próximo passo<br>Reunião de alinhamento</div>
</div>
<div style="margin-top:auto">
  <h2>{h2}</h2>
  <p class="fim-lede">{lede}</p>
  <div class="fim-linhas">{ls}</div>
</div>
<div class="fim-rodape">
  <div><b>Oráculo Tecnologia</b>{rodape_esq}</div>
  <div>Documento confidencial, destinado ao Dr. Pedro Brandão, cirurgião plástico em Brasília<br>Válido por 30 dias a partir do envio</div>
</div>
</section>''')


def build_pedro():
    d = Doc('Dr. Pedro Brandão, cirurgia plástica')

    d.capa(
        'Dr. Pedro Brandão, cirurgião plástico em Brasília',
        'Proposta comercial: tecnologia com atendimento por Inteligência Artificial, gestão '
        'de redes sociais e tráfego pago',
        'A segunda leitura da auditoria de presença digital, de 17 de agosto de 2026, avaliou '
        'a marca em 3,7 de 10 e confirmou o mesmo diagnóstico da primeira coleta: o conteúdo '
        'do Instagram já é o melhor entre quatro cirurgiões plásticos de Brasília comparados, '
        'e a estrutura que transforma essa audiência em consulta ainda não existe. Esta '
        'proposta organiza a resposta em três vertentes, cada uma com escopo próprio, '
        'contratável junto ou separadamente.',
        [('3', 'vertentes contratáveis'), ('0,831%', 'de engajamento na fase atual'),
         ('7.000 a 12.000', 'entrada da tecnologia com atendimento por IA'),
         ('a partir de 1.999', 'reais por mês, nas demais vertentes')])

    # --- 1. diagnóstico
    diagnostico_tabela = tabela(['Achado', 'O que isso custa', 'Vertente'], [
        ('A ficha do Google está na categoria Médico, não Cirurgião plástico',
         'Fica fora do pacote local de quem busca a especialidade em Brasília', 'Tecnologia'),
        ('O domínio próprio mostra a página padrão da hospedagem',
         'Dez anos de autoridade de domínio ficam presos fora do ar', 'Tecnologia'),
        ('Nenhuma legenda cita WhatsApp, o botão do perfil é Ligar e o link da bio é um Linktree',
         'Quem decide agir de noite ou no fim de semana não encontra caminho', 'Tecnologia'),
        ('A ficha do Google ganhou um link de WhatsApp entre as duas coletas, o Instagram não',
         'Prova que a correção é rápida, e mostra o que falta replicar', 'Tecnologia'),
        ('O Facebook, com cerca de 2,1 mil seguidores, aponta para o domínio fora do ar',
         'Quarto resultado da busca pelo nome encaminha para página em branco', 'Tecnologia'),
        ('A hashtag de marca está fragmentada em sete grafias, e piorou desde a primeira coleta',
         'O acervo publicado fica dividido em vez de reunido', 'Redes sociais'),
        ('Cadência de 4,5 publicações por mês, a menor entre os concorrentes medidos',
         'O melhor conteúdo do grupo tem o menor volume do grupo', 'Redes sociais'),
        ('Nenhuma publicação aos domingos, todas entre 8h e 18h',
         'O público que pesquisa cirurgia plástica costuma decidir à noite e no fim de semana',
         'Redes sociais'),
        ('Doctoralia parado desde 2022, sem agendamento online',
         'Terceiro resultado da busca pelo nome, com prova social de quatro anos atrás',
         'Redes sociais'),
        ('O alcance orgânico já é alto, mas não existe caminho pago para quem busca a especialidade',
         'A demanda de alta intenção no Google segue sendo capturada pelos concorrentes',
         'Tráfego pago'),
    ], FONTE_DIAGNOSTICO, compacta=True)

    diagnostico_corpo = (
        '<h2 class="titulo">O que a auditoria encontrou</h2>'
        '<p class="lede">O histórico integral do perfil foi coletado em duas datas, 6 e 17 de '
        'agosto de 2026, com 357 publicações desde 2016, além da busca pelo nome e pela '
        'especialidade, do Perfil da Empresa no Google, dos dois domínios do site e dos '
        'diretórios médicos. A última coluna mostra qual das três vertentes resolve cada '
        'achado.</p>'
        + diagnostico_tabela
        + '<h3 class="sub">O que já funciona</h3>'
        '<p class="texto">O engajamento da fase atual subiu de 0,784% para 0,831% entre as '
        'duas coletas, acima dos 0,68% do concorrente com 51 mil seguidores. A mediana de '
        'reproduções por Reel, 12.169, já supera dois dos três concorrentes medidos. A nota '
        'no Google é 5,0 com 18 avaliações, a maior entre os quatro perfis comparados, '
        'sustentada por credenciais fortes: Sociedade Brasileira de Cirurgia Plástica, '
        'American Society of Plastic Surgeons e fellowship no Instituto Ivo Pitanguy. Nada '
        'disso precisa ser refeito.</p>'
    )
    d.pag('Diagnóstico', diagnostico_corpo,
          'O conteúdo já converte atenção. '
          '<span class="azul">Falta a estrutura que converte contato em consulta.</span>')

    # --- 2. as três vertentes
    vertentes_defs = defs([
        ('1. Tecnologia',
         'Site próprio no domínio raiz, ficha do Google corrigida e um atendente de '
         'Inteligência Artificial no WhatsApp, disponível a qualquer hora, que qualifica o '
         'paciente e agenda ou encaminha para a equipe. Resolve cinco dos dez achados da '
         'auditoria e é o que fica com o consultório mesmo que o contrato acabe.'),
        ('2. Gestão de redes sociais',
         'Unificação da hashtag de marca, correção do calendário de publicação e produção '
         'mensal com prioridade para o formato e o tema que já engajam mais, Reel acima de 35 '
         'segundos e o par mama e segurança cirúrgica. Fecha a lacuna de domingo e horário '
         'noturno.'),
        ('3. Tráfego pago',
         'Google Ads na busca por cirurgião plástico em Brasília, onde a presença orgânica '
         'hoje é zero, somado a Meta Ads segmentado pela praça e pelo procedimento. Toda peça '
         'segue a Resolução CFM nº 2.336/2023.'),
    ])
    vertentes_tabela = tabela(['Vertente', 'Entrada', 'Mensal'], [
        ('1. Tecnologia', '7.000 a 12.000', '<span class="na">a consultar</span>'),
        ('2. Gestão de redes sociais', '<span class="na">sem entrada</span>', 'a partir de 1.999'),
        ('3. Tráfego pago', '1.400', 'a partir de 1.200'),
        ('__total__', 'Vertentes 2 e 3 combinadas', '1.400', 'a partir de 3.199'),
    ], 'Valores em reais, acrescidos de imposto. O mensal das vertentes 2 e 3 varia conforme o '
       'nível escolhido, e os três níveis estão nas páginas seguintes. A entrada da vertente 1 '
       'fica dentro da faixa mostrada, e o valor exato, junto com a mensalidade, é fechado numa '
       'chamada de escopo de 30 minutos, sem custo, antes do contrato. A entrada de qualquer '
       'vertente pode ser parcelada em até doze vezes. A verba de anúncios é paga direto à '
       'plataforma e não está somada aqui.', alinha={1: 'num', 2: 'num'}, compacta=True)

    vertentes_corpo = (
        '<h2 class="titulo">Três vertentes, três contratos possíveis</h2>'
        '<p class="lede">Cada vertente tem escopo próprio e pode ser contratada sozinha. Elas '
        'foram separadas por natureza de trabalho: a primeira constrói a infraestrutura de '
        'atendimento, a segunda produz conteúdo e a terceira compra alcance de alta intenção '
        'para o que as duas anteriores já sustentam.</p>'
        + vertentes_defs + vertentes_tabela
    )
    d.pag('As três vertentes', vertentes_corpo,
          'A ordem que protege o investimento é tecnologia, depois conteúdo, '
          '<span class="azul">e só então anúncio.</span>')

    # --- 3. tecnologia
    resumo_tec = tabela(['Entrega', 'O que inclui', 'Investimento'], [
        ('Site próprio no domínio raiz',
         'drpedrobrandao.com.br deixa de mostrar a página padrão da hospedagem e passa a ser '
         'um site indexável, com página de procedimentos, dados estruturados de médico com '
         'CRM e RQE, Analytics, Search Console e pixel da Meta.', '1.500 a 3.000'),
        ('Ficha do Google reivindicada e corrigida',
         'Categoria alterada de Médico para Cirurgião plástico, preenchimento completo de '
         'fotos, horários e serviços, aproveitando o link de WhatsApp que a ficha já ganhou '
         'entre as duas coletas desta auditoria.', '500 a 1.000'),
        ('Atendente por Inteligência Artificial no WhatsApp',
         'Substitui o Linktree e o botão de Ligar por um número de WhatsApp com atendimento '
         'automático por IA, disponível 24 horas por dia, inclusive à noite e aos domingos, '
         'quando hoje não existe nenhuma publicação nem atendimento. A IA entende o '
         'procedimento de interesse do paciente, responde às dúvidas mais comuns, oferece '
         'horários disponíveis para agendar e encaminha para a secretária quando o caso '
         'exigir atendimento humano.', '3.000 a 6.000'),
        ('Identificação de origem',
         'Cada conversa recebida no WhatsApp pela IA registra se veio do Instagram, do Google '
         'ou do site, o que hoje não existe de nenhuma forma.', '1.000'),
        ('Correção de identidade',
         'Grafia única da hashtag de marca aplicada em todos os canais, e correção do link do '
         'Facebook, que hoje aponta para o domínio fora do ar.', '1.000'),
        ('__total__', 'Entrada da vertente 1', '', '<b>7.000 a 12.000</b>'),
    ], 'Os defeitos de site e de ficha citados foram verificados em 06 e 17/08/2026, direto '
       'nos canais públicos do Dr. Pedro Brandão.')

    tecnologia_nota = nota(
        'Por que o site, a ficha e o atendente de IA variam, e a mensalidade é a consultar',
        'Site, ficha do Google e atendente de IA variam dentro da própria faixa conforme o '
        'volume de trabalho encontrado na implantação, e a soma das cinco linhas fecha entre '
        '7.000 e 12.000 reais de entrada. O item de maior peso é o atendente por Inteligência '
        'Artificial, dimensionado pelo volume de conversas esperado e pelas integrações '
        'desejadas, como agenda da clínica e convênios aceitos. O valor exato de cada item, '
        'junto com a mensalidade, é fechado numa chamada de escopo de 30 minutos, sem custo, '
        'antes do contrato.')

    tecnologia_corpo = (
        '<h2 class="titulo">Vertente 1: Tecnologia</h2>'
        '<p class="lede">O centro desta vertente é o atendente por Inteligência Artificial no '
        'WhatsApp. É ele que fecha o achado de maior custo da auditoria: 1,36 milhão de '
        'reproduções em nove meses sem nenhum caminho de contato direto.</p>'
        + resumo_tec + tecnologia_nota
        + '<h3 class="sub">O que a IA resolve, com números da própria auditoria</h3>'
        '<p class="texto">Dezenove das 41 publicações da fase atual já trazem alguma chamada '
        'para ação, mas nenhuma leva a um número, a um link direto ou a um toque só. A '
        'distribuição por dia da semana mostra sexta, segunda e quarta como os dias de '
        'publicação, e nenhuma publicação aos domingos: exatamente quando o público de '
        'cirurgia plástica costuma decidir. Um atendente disponível 24 horas responde a essa '
        'lacuna sem depender de plantão humano.</p>'
    )
    d.pag('Tecnologia', tecnologia_corpo,
          'Um atendente disponível à noite e aos domingos '
          '<span class="azul">responde ao público que hoje não encontra ninguém.</span>')

    # --- 4. redes, planos
    redes_planos_tabela = '''<table class="planos">
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
<tr><td class="rot">Unificação da hashtag e correção da bio e dos destaques</td>
  <td class="v"><span class="sim">sim</span></td><td class="v dest"><span class="sim">sim</span></td><td class="v"><span class="sim">sim</span></td></tr>
<tr><td class="rot">Sistema de design para o Instagram</td>
  <td class="v"><span class="na">não incluído</span></td><td class="v dest"><span class="sim">sim</span></td><td class="v"><span class="sim">sim</span></td></tr>
<tr><td class="rot">Arquivos editáveis entregues</td>
  <td class="v"><span class="na">não incluído</span></td><td class="v dest"><span class="sim">sim</span></td><td class="v"><span class="sim">sim</span></td></tr>
</tbody></table>
<p class="fonte">Valores em reais, acrescidos de imposto. Sem fidelidade no primeiro mês em qualquer um dos planos. O escopo completo de cada nível está na página seguinte.</p>'''

    redes_planos_nota = nota(
        'Como o volume é contado',
        'Publicação de feed é um post publicado no perfil, seja imagem única ou carrossel, '
        'com quantas telas o assunto pedir. Story é contado por tela. Reel editado é montado '
        'a partir do material gravado pela equipe do consultório.',
        'A divisão exata entre os formatos é definida na grade editorial aprovada todo mês, e '
        'pode variar sem mudar o total contratado.')

    redes_planos_corpo = (
        '<h2 class="titulo">Vertente 2: Gestão de redes sociais</h2>'
        '<p class="lede">A vertente é toda mensal, em três níveis. O que separa um nível do '
        'outro é o volume publicado por mês. Não há valor de entrada.</p>'
        + redes_planos_tabela + redes_planos_nota
        + '<h3 class="sub">Por que o plano Crescimento é o indicado</h3>'
        '<p class="texto">O ritmo atual é de 4,5 publicações por mês, apurado sobre a fase '
        'atual do perfil, com Reels acima de 35 segundos alcançando 3,1 vezes mais '
        'reproduções que os curtos. Doze publicações de feed por mês é o menor volume que '
        'sustenta essa cadência e ainda comporta uma série temática por mês.</p>'
    )
    d.pag('Redes sociais, planos', redes_planos_corpo)

    # --- 5. redes, escopo
    redes_escopo_corpo = escopo(
        'Vertente 2: o que entra em cada nível',
        'Os volumes são totais mensais do perfil @drpedrobrandaocp. O Reel acima de 35 '
        'segundos tem prioridade porque é o formato de melhor alcance medido na auditoria.',
        [('Produção', [
            ('Publicações de feed por mês', '6', '12', '18'),
            ('Stories por mês', '10', '20', '30'),
            ('Reels editados a partir do material enviado', '2', '4', '8'),
            ('Roteiro do Reel acima de 35 segundos', 'nao', 'sim', 'sim'),
            ('Conversão de carrossel em roteiro de Reel', 'nao', '1 por mês', '2 por mês'),
            ('Série sobre mama e segurança cirúrgica', 'nao', '1 por mês', '2 por mês'),
          ]),
         ('Estrutura e direção', [
            ('Gestão do perfil com calendário aprovado', 'sim', 'sim', 'sim'),
            ('Publicação também aos domingos e à noite', 'nao', 'sim', 'sim'),
            ('Sistema de design próprio e arquivos editáveis', 'nao', 'sim', 'sim'),
            ('Legenda, hashtag única e localização em toda publicação', 'sim', 'sim', 'sim'),
            ('Conferência de cada peça com a Resolução CFM nº 2.336/2023', 'sim', 'sim', 'sim'),
          ]),
         ('Acompanhamento', [
            ('Relatório mensal do perfil', 'sim', 'sim', 'sim'),
            ('Relatório de origem das conversas atendidas pela IA', 'nao', 'sim', 'sim'),
            ('Reunião estratégica', 'nao', 'mensal', 'quinzenal'),
          ])])

    redes_escopo_nota = nota(
        'Captação de foto e de vídeo não está incluída',
        'Nenhum dos três níveis inclui fotógrafo ou cinegrafista de sala de cirurgia. O '
        'mensal cobre roteiro, edição, legenda, capa e publicação a partir do material '
        'gravado pela própria equipe do consultório. Quando houver necessidade de captação '
        'profissional, a Oráculo indica e coordena o fornecedor, e o serviço é orçado e pago '
        'diretamente a ele.')

    d.pag('Redes sociais, escopo', redes_escopo_corpo + redes_escopo_nota)

    # --- 6. tráfego pago
    trafego_corpo = planos_com_escopo(
        'Vertente 3: busca de alta intenção e alcance segmentado',
        'Esta vertente ataca o achado mais caro da auditoria fora do Instagram: zero posições '
        'na primeira página de cirurgião plástico Brasília. A entrada de 1.400 reais é paga '
        'uma vez e cobre a abertura e a verificação do Gerenciador de Negócios, o pixel e a '
        'API de conversões, os públicos por procedimento e por praça e a estrutura inicial de '
        'campanhas.',
        ('1.200', '1.800', '2.600'),
        [('Plataformas', [
            ('Meta Ads, no Instagram e no Facebook', 'sim', 'sim', 'sim'),
            ('Google Ads, na busca por cirurgião plástico Brasília', 'nao', 'sim', 'sim'),
          ]),
         ('Campanhas', [
            ('Campanhas ativas ao mesmo tempo', 'até 2', 'até 4', 'até 6'),
            ('Criativos informativos produzidos por mês', '4', '8', '12'),
            ('Otimização e ajuste de campanha', 'semanal', '2 vezes por semana', 'contínua'),
            ('Públicos por procedimento e por praça, incluindo paciente de fora', 'nao', 'sim', 'sim'),
          ]),
         ('Conformidade com a norma do CFM', [
            ('Conferência de cada peça com a Resolução CFM nº 2.336/2023', 'sim', 'sim', 'sim'),
            ('Registro do que foi ajustado em cada peça', 'sim', 'sim', 'sim'),
          ]),
         ('Medição', [
            ('Relatório de aplicação da verba', 'sim', 'sim', 'sim'),
            ('Relatório de origem das conversas atendidas pela IA', 'nao', 'sim', 'sim'),
            ('Reunião de leitura de campanha', 'nao', 'mensal', 'quinzenal'),
          ]),
         ('Verba de anúncios, paga direto à plataforma', [
            ('Faixa recomendada por mês, somando as plataformas', '800 a 1.200', '1.500 a 3.000', 'a definir'),
          ])],
        'Valores em reais, acrescidos de imposto. A verba de anúncios não passa pela Oráculo: '
        'é paga diretamente à plataforma, com relatório de aplicação todo mês. Faixas '
        'conforme tabelas públicas dos fornecedores, consultadas em 17/08/2026. Sob a '
        'Resolução CFM nº 2.336/2023, o anúncio pode informar valor de consulta, mas nenhuma '
        'peça promete resultado.')
    d.pag('Tráfego pago', trafego_corpo)

    # --- 7. cfm
    pagina_cfm(d)

    # --- 8. metas
    metas_tabela = tabela(['Indicador', 'Hoje', 'Meta em 90 dias'], [
        ('__grupo__', 'Vertente 1, tecnologia'),
        ('Site próprio no domínio raiz', 'página padrão da hospedagem', 'indexável e no ar'),
        ('Categoria da ficha do Google', 'Médico', 'Cirurgião plástico'),
        ('Atendimento fora do horário comercial', 'nenhum', 'IA disponível 24 horas'),
        ('Conversas com origem identificada', '0', '100% das atendidas pela IA'),
        ('__grupo__', 'Vertente 2, redes sociais'),
        ('Grafias da hashtag de marca', '7', '1'),
        ('Publicações por mês', '4,5', '12'),
        ('Publicação aos domingos ou à noite', '0', 'pelo menos 4 por mês'),
        ('__grupo__', 'Vertente 3, tráfego pago'),
        ('Posição na busca paga por cirurgião plástico Brasília', 'nenhuma', 'ativa e otimizada'),
        ('Pessoas alcançadas fora da base de seguidores', '0 por mídia paga', '15.000 a 30.000 por mês'),
    ], 'Situação atual apurada na segunda coleta da auditoria, de 17/08/2026. Indexação de '
       'site novo e firmamento de posição no Google levam de dois a três meses, e por isso a '
       'meta de busca paga é de campanha ativa e otimizada, não de posição específica.',
       alinha={1: 'num', 2: 'num'}, compacta=True)

    metas_corpo = (
        '<h2 class="titulo">O que perseguimos nos primeiros 90 dias</h2>'
        '<p class="lede">As metas estão separadas por vertente, para que cada contrato possa '
        'ser cobrado pelo que entrega. Não há meta de cirurgias fechadas nem de receita: '
        'promessa de resultado é vedada pela Resolução CFM nº 2.336/2023, e o fechamento '
        'depende do atendimento da clínica.</p>'
        + metas_tabela
    )
    d.pag('Metas', metas_corpo,
          'O atendimento é a primeira meta '
          '<span class="azul">porque é o único item que muda o resultado já na semana de implantação.</span>')

    # --- 9. cronograma
    cronograma_defs = defs([
        ('Semana 1, vertente 1',
         'Chamada de escopo da vertente 1. Reivindicação da ficha do Google e correção da '
         'categoria. Número de WhatsApp definido e configurado para o atendimento por IA.'),
        ('Mês 1, vertentes 1 e 2',
         'Atendente de IA no ar, respondendo 24 horas por dia. Site próprio publicado no '
         'domínio raiz, com página de procedimentos e dados estruturados. Hashtag de marca '
         'unificada e bio corrigida. Primeira grade editorial aprovada.'),
        ('Mês 2, vertente 2',
         'Cadência estabilizada em doze publicações de feed por mês, com prioridade para '
         'Reel acima de 35 segundos e para os temas mama e segurança cirúrgica. Publicação '
         'passa a cobrir domingo e horário noturno.'),
        ('Mês 3, vertente 3',
         'Tráfego pago entra agora, com a medição pronta e com um acervo de peça orgânica já '
         'testado. Google Ads sobe sobre a busca por cirurgião plástico Brasília, ausente '
         'hoje.'),
        ('Meses 4 a 6, as três',
         'Site e atendimento por IA em manutenção, cadência mantida no perfil e campanhas '
         'otimizadas contra o relatório de origem das conversas.'),
    ])
    cronograma_corpo = (
        '<h2 class="titulo">Como as três vertentes entram, e em que ordem</h2>'
        '<p class="lede">O atendente de IA vem primeiro porque é o único item que muda o '
        'resultado já na semana de implantação, sem depender de produção nova. O tráfego '
        'pago vem por último, para subir sobre uma base já medida.</p>'
        + cronograma_defs + CONDICOES_PEDRO
    )
    d.pag('Como começa', cronograma_corpo)

    contracapa_pedro(
        d,
        'Uma conversa de 30 minutos para fechar o escopo',
        'O que precisa ser decidido antes de começar: qual número de WhatsApp recebe o '
        'atendimento da IA, quais integrações de agenda e de convênio ela precisa ter, qual '
        'categoria e quais fotos entram na ficha do Google, e quem aprova a grade editorial '
        'mensal.',
        [('Reunião', '30 minutos, presencial em Brasília ou por vídeo'),
         ('Onboarding', '7 dias, com o atendente de IA e o WhatsApp no ar'),
         ('Entrada', '7.000 a 12.000 reais na vertente 1, e 1.400 reais na vertente 3'),
         ('Mensal', 'a partir de 3.199 reais nas vertentes 2 e 3, mais a vertente 1 após o escopo')],
        'Baseado na auditoria de presença digital do<br>Dr. Pedro Brandão, de 17 de agosto de '
        '2026, sobre 357 publicações')

    return d.salvar(
        os.path.join(RAIZ, 'DrPedroBrandao', 'Proposta-Comercial.html'),
        'Proposta Comercial, Dr. Pedro Brandão',
        'Proposta comercial do Dr. Pedro Brandão em três vertentes: tecnologia com atendente '
        'de Inteligência Artificial no WhatsApp, gestão de redes sociais e tráfego pago. '
        'Oráculo Tecnologia, agosto de 2026.')


def validar(nome, html):
    erros = []
    corpo = re.sub(r'<style>.*?</style>', '', html, flags=re.S)
    texto = re.sub(r'<[^>]+>', ' ', corpo)
    css_only = html.split('<style>')[-1].split('</style>')[0]

    for termo in ['Debem', 'Diego Santos', 'Suziellen', 'Sinfonya', 'sinfonya', 'Joana',
                  'ladeguste', 'PECBR', 'Elora', 'Flavia Melow']:
        if termo.lower() in corpo.lower():
            erros.append(f'residuo de outro cliente: {termo}')
    for p in bp.PALAVRAS_SEM_ACENTO:
        if re.search(r'\b' + re.escape(p) + r'\b', texto):
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
    if re.search(r"'\n", corpo):
        erros.append('possivel aspa solta de concatenacao quebrada')
    erros = sorted(set(erros))
    print(f'  {nome}: {len(html)/1024:.0f} KB, {html.count("<section")} paginas  |  '
          + ('validacao ok' if not erros else f'PROBLEMAS: {erros}'))
    return erros


if __name__ == '__main__':
    print('gerando proposta do Dr. Pedro Brandao...')
    html = build_pedro()
    validar('DrPedroBrandao', html)
