# -*- coding: utf-8 -*-
"""Proposta comercial modelo para candidaturas.

Mesma arquitetura de duas decisoes do modelo comercial (build_proposta_modelo.py):
a base da candidatura, paga uma vez, e o pacote mensal que conduz a operacao. O que
muda numa campanha, e por isso ganhou pagina propria:

  1. o volume: campanha publica muito mais, e os pacotes sao 18, 30 e 60 publicacoes
     de feed por mes, com preco a partir de 7.499
  2. os pacotes sao fases, e a candidatura sobe de nivel conforme a urna se aproxima
  3. a norma eleitoral limita o que pode ser publicado e impulsionado, e quando
  4. todo gasto com impulsionamento entra na prestacao de contas

Prazos legais conferidos na Resolucao TSE no 23.760/2026 (calendario eleitoral de
2026) em 18/08/2026. Reconferir a cada ciclo: a resolucao e refeita toda eleicao.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_propostas_debem as bp
from build_proposta_modelo import DocModelo

bp.DATA = '20 de agosto de 2026'

tabela = bp.tabela
defs = bp.defs
nota = bp.nota
duas_colunas = bp.duas_colunas
RAIZ = bp.RAIZ

NIVEIS = ('Essencial', 'Ampliada', 'Intensiva')


# ---------------------------------------------------------------- helpers com colunas proprias
def _celula(v):
    if v == 'sim':
        return '<span class="sim">sim</span>'
    if v == 'nao':
        return '<span class="na">não incluído</span>'
    return v


def _cabecalho(destaque_rec=True):
    a, b, c = NIVEIS
    rec = '<span class="rec">Recomendado</span>' if destaque_rec else ''
    return (f'<thead><tr><th class="rot"></th><th class="col">{a}</th>'
            f'<th class="col dest">{rec}{b}</th>'
            f'<th class="col">{c}</th></tr></thead>')


def _linhas(blocos):
    linhas = ''
    for grupo, itens in blocos:
        linhas += f'<tr class="grupo"><td colspan="4">{grupo}</td></tr>'
        for rot, x, y, z in itens:
            linhas += (f'<tr><td class="rot">{rot}</td>'
                       f'<td class="v">{_celula(x)}</td>'
                       f'<td class="v dest">{_celula(y)}</td>'
                       f'<td class="v">{_celula(z)}</td></tr>')
    return linhas


def pacotes(titulo, lede, precos, blocos, fonte=None):
    a, b, c = precos
    preco = ('<tr><td class="rot">Investimento mensal</td>'
             f'<td class="v"><span class="preco">{a}</span><span class="un">reais por mês</span></td>'
             f'<td class="v dest"><span class="preco az">{b}</span><span class="un">reais por mês</span></td>'
             f'<td class="v"><span class="preco">{c}</span><span class="un">reais por mês</span></td></tr>')
    f = f'<p class="fonte">{fonte}</p>' if fonte else ''
    return (f'<h2 class="titulo">{titulo}</h2><p class="lede">{lede}</p>'
            f'<table class="planos esc">{_cabecalho()}'
            f'<tbody>{preco}{_linhas(blocos)}</tbody></table>{f}')


def escopo(titulo, lede, blocos, fonte=None):
    f = f'<p class="fonte">{fonte}</p>' if fonte else ''
    a, b, c = NIVEIS
    cab = (f'<thead><tr><th class="rot">Entrega</th><th class="col">{a}</th>'
           f'<th class="col dest">{b}</th><th class="col">{c}</th></tr></thead>')
    return (f'<h2 class="titulo">{titulo}</h2><p class="lede">{lede}</p>'
            f'<table class="planos esc">{cab}<tbody>{_linhas(blocos)}</tbody></table>{f}')


# ---------------------------------------------------------------- textos fixos
FONTE_MODELO = (
    'Documento modelo. A candidatura citada é fictícia e os valores são os praticados pela Oráculo '
    'em agosto de 2026. Numa proposta real, cada linha de diagnóstico cita o número apurado no '
    'repositório do Tribunal Superior Eleitoral e a data da coleta.')

FONTE_PACOTES = (
    'Valores em reais, acrescidos de imposto, sem valor de entrada. O custo por peça de feed cai '
    'conforme o volume sobe: 417, 400 e 333 reais, e nesse valor já entram stories, cortes, '
    'cobertura de agenda e a gestão do impulsionamento. O nível é escolhido para a campanha inteira '
    'e pode ser trocado a qualquer momento, valendo no mês seguinte, sem custo de mudança.')

LEI_PERMITE = [
    'Propaganda eleitoral na internet a partir de 16 de agosto do ano da eleição.',
    'Impulsionamento de conteúdo eleitoral, identificado como tal e contratado exclusivamente por '
    'candidato, partido, federação ou coligação, com o CNPJ da campanha.',
    'Conteúdo de pré-campanha antes de 16 de agosto, com posicionamento e agenda, desde que sem '
    'pedido explícito de voto.',
    'Transmissão ao vivo da candidatura, que equivale a ato de campanha e é contabilizada como tal.',
    'Divulgação de currículo, mandato, propostas, agenda pública e apoio declarado.',
]

LEI_VEDA = [
    'Qualquer propaganda eleitoral paga na internet fora do impulsionamento previsto em lei, e '
    'impulsionamento contratado por pessoa física ou por empresa que não seja a campanha.',
    'Impulsionamento pago depois de 1º de outubro, três dias antes da votação.',
    'Disparo em massa de mensagens, em qualquer momento do calendário.',
    'Publicação de enquete a partir de 16 de agosto.',
    'Publicação e republicação de conteúdo sintético gerado por inteligência artificial nas 72 '
    'horas antes e nas 24 horas depois da votação.',
    'Propaganda de qualquer tipo no dia da votação, fora do que a norma autoriza expressamente.',
]

LEI_FONTE = (
    'Lei nº 9.504/1997, artigo 57-C, combinada com a Resolução TSE nº 23.760/2026, que fixou o '
    'calendário eleitoral de 2026. Prazos conferidos na fonte em 24 de agosto de 2026. O '
    'descumprimento da regra de impulsionamento sujeita a campanha a multa, nos termos do parágrafo '
    '2º do mesmo artigo. Leitura aplicada ao escopo desta proposta, sem caráter de parecer jurídico: '
    'a palavra final é sempre da advocacia da campanha.')

CONDICOES_POL = (
    'A base é paga uma vez, na assinatura, e é parcelável em até seis vezes, prazo menor que o '
    'padrão porque o ciclo eleitoral é curto. O pacote mensal é contrato mensal, sem fidelidade, '
    'e a troca de nível pode ser feita a qualquer momento, valendo no mês seguinte. O contrato se '
    'encerra automaticamente no dia seguinte ao da votação, salvo renovação escrita para o mandato. '
    'A Oráculo emite nota fiscal de todo valor recebido e entrega o relatório de aplicação da verba '
    'no formato exigido pela prestação de contas, mês a mês. A verba de impulsionamento é contratada '
    'e paga pelo CNPJ da campanha, diretamente à plataforma, e nunca pela Oráculo. Valores em reais, '
    'acrescidos de imposto. Esta proposta é válida por 30 dias a partir da data de envio.')


def build_modelo_politico():
    d = DocModelo('Candidatura', destinatario='à Candidatura')

    # ---------------------------------------------------------------- capa
    d.capa(
        'Candidatura',
        'Proposta comercial: a base da candidatura, e a operação de campanha em três níveis',
        'Esta proposta responde à análise de cenário eleitoral feita antes de qualquer conversa '
        'comercial, com os dados do repositório do Tribunal Superior Eleitoral e a leitura das redes '
        'da candidatura. São duas decisões: construir a base, que é paga uma vez, e escolher o nível '
        'de operação, que acompanha a fase da campanha.',
        [('2', 'decisões a tomar'), ('8.500', 'reais de entrada, uma vez'),
         ('7.499', 'reais por mês, no nível de entrada'), ('60', 'publicações de feed na reta final')])

    # ---------------------------------------------------------------- 1. resumo
    d.pag('Resumo', f'''
<h2 class="titulo">A proposta em uma página</h2>
<p class="lede">Esta página responde às quatro perguntas que aparecem na primeira leitura. As páginas
seguintes existem para detalhar cada uma delas, e podem ser lidas depois ou junto com a coordenação
de campanha.</p>
{defs([
    ('O que propomos',
     'Primeiro a base: identidade da candidatura, página declarada à Justiça Eleitoral, estrutura de '
     'anúncios no CNPJ da campanha e medição por município, construídas uma vez. Depois a operação: '
     'um nível mensal que reúne conteúdo, impulsionamento e acompanhamento no mesmo contrato.'),
    ('Quanto custa',
     '8.500 reais de entrada, pagos uma vez, mais o nível mensal escolhido, de 7.499 a 19.999 reais. '
     'A verba de impulsionamento é contratada e paga pelo CNPJ da campanha, direto à plataforma, e '
     'entra na prestação de contas.'),
    ('Quando começa',
     'Reunião de escopo de 30 minutos com a coordenação, sem custo. Onboarding completo em 7 dias a '
     'partir da assinatura. O contrato se encerra no dia seguinte ao da votação, salvo renovação.'),
    ('O que fica com a candidatura',
     'Página, domínio, contas de anúncio, perfis, banco de conteúdo e arquivos editáveis ficam no nome '
     'da candidatura ou do partido, e continuam valendo depois da eleição.'),
])}
{tabela(['O que se contrata', 'Entrada', 'Mensal'], [
    ('__grupo__', 'Decisão 1, paga uma vez'),
    ('A base: identidade, página, estrutura de anúncios e medição', '<b>8.500</b>',
     '<span class="na">sem mensal próprio</span>'),
    ('__grupo__', 'Decisão 2, o nível que conduz a operação'),
    ('Campanha Essencial, 18 publicações de feed por mês', '<span class="na">sem entrada</span>', '7.499'),
    ('__destaque__', 'Campanha Ampliada, 30 publicações de feed por mês', '<span class="na">sem entrada</span>',
     '<b>11.999</b>'),
    ('Campanha Intensiva, 60 publicações de feed por mês', '<span class="na">sem entrada</span>', '19.999'),
], 'Valores em reais, acrescidos de imposto. A sustentação da página e da medição está dentro do nível '
   'mensal, sem cobrança à parte. O nível vale para a campanha inteira e é escolhido pelo ritmo de '
   'publicação que a candidatura consegue sustentar, não pela fase do calendário.',
   alinha={1: 'num', 2: 'num'}, compacta=True)}
{nota('Por que a base vem primeiro',
      'A página da candidatura é o endereço que a Justiça Eleitoral reconhece, e é para ela que todo '
      'impulsionamento aponta. A estrutura de anúncios precisa estar aberta e verificada no CNPJ da '
      'campanha antes da primeira peça paga, e essa verificação leva dias que a campanha não tem para '
      'perder em agosto.')}
''', 'Duas decisões, dois números. <span class="azul">O resto do documento é a prova.</span>')

    # ---------------------------------------------------------------- 2. diagnostico
    d.pag('Diagnóstico', f'''
<h2 class="titulo">De onde saiu cada recomendação deste documento</h2>
<p class="lede">Nenhum item desta proposta foi escolhido em reunião. Todos saíram da análise de cenário
eleitoral, que cruza a votação da legenda e dos concorrentes no repositório do Tribunal Superior
Eleitoral com a leitura das redes da candidatura, município a município.</p>
{tabela(['O que a análise apurou', 'O que isso significa', 'Onde entra'], [
    ('A legenda ficou abaixo do quociente eleitoral na última disputa proporcional',
     'Numa eleição proporcional o voto pessoal não elege sozinho. Se o partido não atinge o quociente, '
     'a votação da candidatura não vira cadeira, e a campanha precisa ser desenhada sabendo disso.',
     '<b>Base</b>'),
    ('A base geográfica declarada produz menos votos do que o último eleito precisou',
     'A conta de votos disponíveis por município tem que estar na mesa antes de decidir onde a campanha '
     'gasta agenda, deslocamento e verba de impulsionamento.', '<b>Pacote</b>'),
    ('O perfil passou meses sem publicar e o endereço declarado à Justiça Eleitoral está fora do ar',
     'Alcance orgânico perdido não volta em semanas, e o endereço declarado é a única página oficial '
     'que a Justiça Eleitoral reconhece como da candidatura.', '<b>Base</b>'),
], FONTE_MODELO)}
{nota('A análise de cenário é um documento separado',
      'O relatório vai junto desta proposta, com a aritmética do quociente, o mapa de votos por '
      'município, a comparação com os concorrentes da mesma legenda e a leitura das redes. Esta '
      'proposta cita apenas os três achados que definem o escopo, para não repetir o que já está lá.')}
''', 'A proposta não começou numa reunião. <span class="azul">Começou na urna da eleição passada.</span>')

    # ---------------------------------------------------------------- 3. a base
    d.pag('A base', f'''
<h2 class="titulo">Decisão 1: a base da candidatura, construída uma vez</h2>
<p class="lede">Esta é a parte paga uma única vez, e ela precisa estar pronta antes da primeira peça
paga ir ao ar. Tudo o que é construído aqui fica registrado no nome da candidatura ou do partido.</p>
{tabela(['Obra', 'O que inclui', 'Valor'], [
    ('__grupo__', 'A base recomendada'),
    ('Identidade da candidatura',
     'Número, legenda e paleta aplicados em molduras de feed, capas de story, kit de peças para '
     'apoiadores, adesivo digital e modelo de card de agenda. Tudo entregue também em arquivo '
     'editável.', '3.500'),
    ('Página da candidatura',
     'Página oficial com propostas, biografia, agenda e canal de contato, no endereço que é declarado '
     'à Justiça Eleitoral e para onde todo impulsionamento aponta. Entrega em 2 a 3 semanas.', '2.500'),
    ('Estrutura de anúncios eleitorais',
     'Gerenciador de Negócios aberto, verificação de anunciante eleitoral concluída no CNPJ da campanha, '
     'públicos por município da base geográfica e primeira estrutura de campanhas montada.', '1.900'),
    ('Medição por município',
     'Painel que acompanha alcance, engajamento e verba aplicada município a município, cruzado com a '
     'votação da eleição anterior. É o que permite decidir onde reforçar e onde parar de gastar.',
     '1.400'),
    ('__total__', 'Somando os quatro itens', '', '9.300'),
    ('__total__', 'Contratados juntos, a entrada é', '', '<b>8.500</b>'),
    ('__grupo__', 'Itens da mesma etapa, contratáveis quando fizer sentido'),
    ('Dia de captação com a candidatura',
     'Um dia de gravação para formar banco de conteúdo: falas de proposta, cortes curtos, fotos de '
     'agenda e material para 30 a 45 dias de publicação.', '2.800'),
    ('Atendimento no WhatsApp da campanha',
     'Conta oficial liberada, triagem por assunto e encaminhamento para a equipe, dentro do que a '
     'norma permite. Não inclui e nunca incluirá disparo em massa, que é vedado.', '3.200'),
], 'Valores em reais, acrescidos de imposto, parceláveis em até seis vezes. A manutenção do que é '
   'construído aqui já está dentro do nível mensal, sem cobrança separada.')}
''', 'A verificação de anunciante eleitoral leva dias. <span class="azul">É por isso que a base não espera agosto.</span>')

    # ---------------------------------------------------------------- 4. os niveis
    d.pag('Os três níveis', pacotes(
        'Decisão 2: o nível que conduz a operação',
        'Um contrato só, com conteúdo, impulsionamento e acompanhamento no mesmo valor. Os três níveis '
        'valem para a campanha inteira: o que separa um do outro é o volume publicado por mês e a '
        'intensidade do acompanhamento. A escolha depende do ritmo que a candidatura consegue sustentar '
        'em material, agenda e decisão, e pode ser revista a qualquer momento.',
        ('7.499', '11.999', '19.999'),
        [('Conteúdo publicado por mês', [
            ('Publicações de feed', '18', '30', '60'),
            ('Stories', '40', '90', '180'),
            ('Cortes e Reels editados', '8', '20', '45'),
            ('Dias de cobertura de agenda', '2', '6', '15'),
          ]),
         ('Impulsionamento', [
            ('Campanhas ativas ao mesmo tempo', 'até 4', 'até 10', 'até 20'),
            ('Criativos de anúncio por mês', '8', '20', '40'),
            ('Públicos por município da base', 'nao', 'sim', 'sim'),
          ]),
         ('Acompanhamento', [
            ('Monitoramento de menções', 'nao', 'diário', 'contínuo'),
            ('Plantão de crise', 'nao', 'horário comercial', '7 dias por semana'),
            ('Reunião com a coordenação', 'quinzenal', 'semanal', 'diária'),
            ('Relatório de campanha', 'mensal', 'semanal', 'diário'),
          ])],
        FONTE_PACOTES),
        'Um contrato, um valor, um relatório. <span class="azul">Conteúdo e impulsionamento deixam de ser duas conversas.</span>')

    # ---------------------------------------------------------------- 5. escopo
    d.pag('Escopo', escopo(
        'O que entra em cada nível, item a item',
        'A página anterior traz o que decide a escolha. Esta abre o restante do escopo, para que não '
        'reste dúvida sobre o que está contratado. Nenhuma entrega deste documento existe fora desta '
        'tabela.',
        [('Feito no primeiro mês, sem custo separado', [
            ('Perfil organizado com número e legenda', 'sim', 'sim', 'sim'),
            ('Destaques por bandeira e por região', 'sim', 'sim', 'sim'),
            ('Linhas editoriais e primeira grade', 'sim', 'sim', 'sim'),
            ('Kit de peças para apoiadores', 'nao', 'sim', 'sim'),
            ('Arquivos editáveis entregues', 'nao', 'sim', 'sim'),
          ]),
         ('Rotina de produção', [
            ('Roteiro, edição, legenda e capa', 'sim', 'sim', 'sim'),
            ('Grade da semana proposta na sexta', 'sim', 'sim', 'sim'),
            ('Corte de agenda no mesmo dia', 'nao', 'sim', 'sim'),
            ('Resposta a comentário e a mensagem', 'nao', 'sim', 'sim'),
          ]),
         ('Impulsionamento e conformidade', [
            ('Conferência de cada peça com a norma eleitoral', 'sim', 'sim', 'sim'),
            ('Relatório no formato da prestação de contas', 'sim', 'sim', 'sim'),
            ('Teste de público e de peça', 'nao', 'nao', 'sim'),
          ]),
         ('Sustentação da base, quando ela for contratada', [
            ('Página da candidatura no ar e atualizada', 'sim', 'sim', 'sim'),
            ('Painel de acompanhamento por município', 'nao', 'sim', 'sim'),
          ])],
        'Story é contado por tela. Publicação de feed é um post no perfil, imagem única ou carrossel, '
        'com quantas telas o assunto pedir. Corte é um vídeo curto editado a partir de live, agenda ou '
        'material gravado pela equipe da campanha.'),
        'Uma tabela só, três colunas. <span class="azul">Nada é prometido fora dela.</span>')

    # ---------------------------------------------------------------- 6. calendario
    d.pag('Calendário', f'''
<h2 class="titulo">O calendário até a urna</h2>
<p class="lede">Campanha tem prazo externo e inegociável. Este é o único cronograma do documento, e
cada data abaixo é prazo legal, não escolha de agência. As datas são as do calendário de 2026 e devem
ser reconferidas a cada ciclo, porque a resolução é refeita a cada eleição.</p>
{defs([
    ('Até 15 de agosto, pré-campanha',
     'Construção da base, banco de conteúdo, organização do perfil e publicação de posicionamento e '
     'agenda, sem pedido explícito de voto. É a janela em que a estrutura de anúncios é aberta e '
     'verificada, e ela não pode ser feita com pressa depois.'),
    ('16 de agosto, propaganda liberada',
     'Primeiro dia de propaganda eleitoral na internet e de impulsionamento pago. A partir desta data '
     'também fica vedada a publicação de enquete.'),
    ('De 28 de agosto a 1º de outubro, horário gratuito',
     'Período do horário eleitoral gratuito em rádio e televisão. O conteúdo das redes passa a ser '
     'produzido em conversa com o material do horário, para não competir com ele.'),
    ('Até 1º de outubro, último impulsionamento',
     'Último dia em que a campanha pode impulsionar conteúdo, três dias antes da votação. Toda a verba '
     'precisa estar planejada para caber nesta janela.'),
    ('Até as 22h de 3 de outubro',
     'Prazo final para material gráfico e carreata. A partir de 1º de outubro, e até 24 horas depois da '
     'votação, também é vedada a publicação e a republicação de conteúdo gerado por inteligência '
     'artificial.'),
    ('4 de outubro, votação',
     'Primeiro turno. O contrato se encerra no dia seguinte, salvo renovação escrita para o mandato.'),
])}
{nota('O que não é prometido neste documento',
      'Nenhuma meta desta proposta é de votos, de posição em pesquisa ou de resultado na urna. O que é '
      'contratado, medido e cobrado é alcance, volume publicado, verba aplicada e conformidade com a '
      'norma. Prometer resultado eleitoral seria desonesto, e o voto depende de fatores que nenhuma '
      'agência controla.')}
''', 'A urna não adia. <span class="azul">Todo prazo deste documento é contado de trás para frente.</span>')

    # ---------------------------------------------------------------- 7. legislacao
    d.pag('Norma eleitoral', f'''
<h2 class="titulo">O que a norma eleitoral permite, e o que ela veda</h2>
<p class="lede">Propaganda eleitoral tem regra própria, e ela muda o que se pode publicar, o que se
pode impulsionar e em que data. Por isso está escrita aqui, antes de qualquer produção, e não numa
conversa depois que a peça já foi ao ar.</p>
{duas_colunas('A norma permite', LEI_PERMITE, 'A norma veda', LEI_VEDA)}
{nota('O que isso muda na prática',
      'Toda peça passa por conferência com a norma antes de ir ao ar, com registro do que foi ajustado. '
      'Todo impulsionamento é contratado no CNPJ da campanha, nunca em conta de pessoa física e nunca '
      'em conta da Oráculo, e o relatório de aplicação sai no formato que a prestação de contas exige. '
      'A responsabilidade eleitoral permanece da candidatura e do partido, e a conferência da Oráculo '
      'não a substitui.')}
<p class="fonte">{LEI_FONTE}</p>
''', 'Peça fora da norma custa mais caro que peça ruim. <span class="azul">Uma some, a outra vira multa.</span>')

    # ---------------------------------------------------------------- 8. como funciona
    d.pag('Como funciona', f'''
<h2 class="titulo">Como o trabalho acontece no dia a dia</h2>
<p class="lede">Campanha erra por falta de decisão, não por falta de ideia. Por isso o que cabe a cada
lado está escrito aqui, antes da assinatura.</p>
{duas_colunas(
    'O que a Oráculo faz',
    ['Propõe a grade da semana toda sexta, com tema, formato e objetivo de cada peça.',
     'Produz roteiro, arte, edição, legenda e capa a partir do material da agenda e do banco de conteúdo.',
     'Publica no calendário aprovado, sem depender de nova confirmação a cada peça.',
     'Gere o impulsionamento por município, acompanha a verba diariamente e ajusta público e criativo.',
     'Entrega o relatório no ritmo do nível contratado, já no formato da prestação de contas.'],
    'O que esperamos da campanha',
    ['Um ponto focal único na coordenação, com poder de decidir e resposta em até 24 horas.',
     'Agenda da semana enviada com antecedência, para que a cobertura seja planejada e não improvisada.',
     'Material bruto da agenda no mesmo dia: fotos, vídeos e falas gravadas pela equipe em campo.',
     'Acesso às contas de rede social, ao domínio e ao CNPJ da campanha para a verificação de anunciante.',
     'Decisão da candidatura sobre tema sensível, sempre por escrito, antes da publicação.'])}
{nota('Aprovação por silêncio, e o motivo',
      'A grade enviada e não respondida em 24 horas é considerada aprovada. Em campanha esse prazo é '
      'mais curto que o comercial de propósito: peça publicada fora do dia perde o assunto, e a janela '
      'de impulsionamento tem data para fechar. A regra existe para proteger o calendário, e qualquer '
      'peça pode ser derrubada a qualquer momento por pedido da coordenação.')}
''', 'A campanha decide, a Oráculo executa. <span class="azul">O que trava não é a produção, é a resposta.</span>')

    # ---------------------------------------------------------------- 9. condicoes
    d.pag('Condições', f'''
<h2 class="titulo">Condições comerciais e custos que não passam pela Oráculo</h2>
<p class="lede">Esta página existe para que nenhuma pergunta de contrato precise ser feita por
mensagem depois, e para que a prestação de contas encontre tudo no lugar.</p>
<h3 class="sub">Condições comerciais</h3>
<p class="texto">{CONDICOES_POL}</p>
<h3 class="sub">Pago diretamente ao fornecedor, pelo CNPJ da campanha</h3>
{tabela(['Item', 'Quanto', 'Quando se aplica'], [
    ('Verba de impulsionamento, paga à plataforma', 'definida pela campanha',
     'Em qualquer nível, dentro do limite de gastos'),
    ('Hospedagem e domínio da página da candidatura', 'cerca de 150 por mês',
     'A partir da entrega da página'),
    ('Sistema de atendimento no WhatsApp', 'cerca de 500 por mês', 'Se o atendimento for contratado'),
], 'Valores em reais. Faixas conforme as tabelas públicas dos fornecedores, consultadas em 20/08/2026. '
   'Nenhum destes itens passa pela Oráculo, e todos precisam de nota fiscal em nome da campanha para '
   'entrar na prestação de contas.', compacta=True)}
{nota('O que o nível mensal não cobre',
      'Fotografia e cinematografia profissionais em agenda, produção de evento, jingle, locução, '
      'pesquisa de opinião registrada, assessoria de imprensa e material gráfico impresso são orçados '
      'à parte quando houver necessidade. A Oráculo indica e coordena o fornecedor, e o serviço é '
      'contratado e pago diretamente pela campanha.')}
''', 'Preço fechado, nota emitida <span class="azul">e relatório no formato da prestação de contas.</span>')

    # ---------------------------------------------------------------- contracapa
    d.contracapa(
        'O próximo passo é uma reunião de 30 minutos',
        'A reunião serve para ajustar o escopo ao caso concreto, confirmar a base geográfica e as '
        'prioridades de agenda e definir a data de início. Não há custo e não há compromisso de '
        'contratação.',
        [('Reunião', '30 minutos com a coordenação, presencial ou por vídeo'),
         ('Onboarding', '7 dias a partir da assinatura'),
         ('A base', '8.500 reais, pagos uma vez, parceláveis em até 6 vezes'),
         ('O nível', 'de 7.499 a 19.999 reais por mês, conforme a fase da campanha')],
        'Baseado na análise de cenário eleitoral<br>feita antes do primeiro contato comercial')

    return d.salvar(
        os.path.join(RAIZ, 'Modelo', 'Proposta-Comercial-Modelo-Politico.html'),
        'Proposta Comercial Modelo, Candidatura',
        'Proposta comercial modelo da Oráculo Tecnologia para candidaturas: a base da candidatura '
        'e a operação de campanha em três níveis, de 18 a 60 publicações de feed por mês.')


if __name__ == '__main__':
    print('gerando proposta modelo politica...')
    erros = bp.validar('ModeloPolitico', build_modelo_politico())
    print('RESULTADO:', 'tudo ok' if not erros else erros)
