# -*- coding: utf-8 -*-
"""Proposta comercial de Juliana Arantes, MOVE & Connect, Brasilia.

Segue o padrao decidido em 20/08/2026 (build_proposta_modelo.py): duas decisoes, nao tres
vertentes. A base construida uma vez, com pagamento unico, e a operacao mensal em tres
pacotes que ja somam conteudo, anuncio e sustentacao.

Duas escolhas do usuario em 09/09/2026, que afastam este documento da regua padrao:
  1. a escada mensal e 2.000 / 2.500 / 3.000, e os tres niveis cobrem as tres contas
     (@moveeconnect, @juharantes_ e @kalecozinhasensorial). O que muda entre eles e o
     volume publicado, o alcance pago e a profundidade do acompanhamento.
  2. a base e enxuta, 2.900 em vez dos 7.500 da regua, porque a auditoria mostrou que o que
     falta aqui e dominio, medicao e ficha do Google, e nao um site institucional completo.

Todos os numeros citados vem da auditoria de presenca digital de 04/09/2026, guardada em
JulianaArantes/data/juharantes_-scan.json e em JulianaArantes/Analise-Presenca-Digital.html.

Reaproveita os helpers de build_propostas_debem.py e a classe DocModelo do modelo.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_propostas_debem as bp
import build_proposta_modelo as bm

bp.DATA = '9 de setembro de 2026'

tabela = bp.tabela
defs = bp.defs
nota = bp.nota
duas_colunas = bp.duas_colunas
planos_com_escopo = bp.planos_com_escopo
escopo = bp.escopo
RAIZ = bp.RAIZ

# ---------------------------------------------------------------- blocos de texto
FONTE_AUDITORIA = (
    'Auditoria de presença digital de 04/09/2026: 144 das 289 publicações de @juharantes_ lidas uma '
    'a uma pela API interna do Instagram com sessão autenticada, as 16 pastas de destaque, os perfis '
    '@moveeconnect e @kalecozinhasensorial e sete contas de networking do Distrito Federal medidas '
    'pelo mesmo método e na mesma data; Google Search em pt-BR; consulta ao registro.br; e o código '
    'da página do evento no Sympla.')

FONTE_PACOTES = (
    'Valores em reais, acrescidos de imposto, sem valor de entrada. Os três níveis cobrem as três '
    'contas. O que muda entre eles é o volume publicado, o alcance pago e a profundidade do '
    'acompanhamento. A verba de anúncios é da contratante, fica na conta da contratante e não passa '
    'pela Oráculo. Esta faixa de preço é menor que a praticada pela Oráculo em contratos de marca '
    'única, e vale enquanto as três contas forem conduzidas na mesma operação, com a mesma grade '
    'editorial e o mesmo relatório.')

FONTE_ESCOPO = (
    'Story é contado por tela e publicação de feed é um post no perfil, imagem única ou carrossel, '
    'com quantas telas o assunto pedir. Reel editado é montado a partir do material gravado pela '
    'equipe da contratante. Publicação em colaboração conta uma vez no volume e aparece nas duas '
    'contas ao mesmo tempo. Nenhum dos três pacotes inclui fotógrafo ou cinegrafista no dia do '
    'evento.')

CONDICOES = (
    'A base é paga uma vez, na assinatura, e é parcelável em até doze vezes de 242 reais. O pacote '
    'mensal é contrato mensal, sem fidelidade no primeiro mês, com vencimento no mesmo dia de cada '
    'mês contado a partir da assinatura, e cancelamento com aviso de 30 dias, sem multa. A troca de '
    'pacote pode ser feita a qualquer momento, para cima ou para baixo, valendo no mês seguinte. '
    'Onboarding completo em 7 dias a partir da assinatura. A verba de anúncios e as mensalidades de '
    'ferramenta são pagas diretamente aos fornecedores, com relatório de aplicação todo mês. Valores '
    'em reais, acrescidos de imposto. Esta proposta é válida por 30 dias a partir da data de envio.')


def build_juliana():
    d = bm.DocModelo('MOVE & Connect', destinatario='a Juliana Arantes')

    # ---------------------------------------------------------------- capa
    d.capa(
        'Juliana Arantes, MOVE &amp; Connect',
        'Proposta comercial: a base construída uma vez, e as três contas numa operação só',
        'A auditoria de presença digital de 4 de setembro avaliou a presença em 2,9 de 10 e mostrou '
        'onde está a perda: a audiência de 19.348 seguidores está inteira no perfil pessoal, enquanto '
        'a conta que vende o ingresso tem 423. Esta proposta responde a isso com duas decisões, e só '
        'duas: construir a base, que é paga uma vez, e escolher o pacote mensal que conduz as três '
        'contas. A página seguinte resume o documento inteiro.',
        [('2', 'decisões a tomar'), ('2.900', 'reais de entrada, uma vez'),
         ('2.500', 'reais por mês, no pacote recomendado'), ('3', 'contas na mesma operação')])

    # ---------------------------------------------------------------- 1. resumo
    d.pag('Resumo', f'''
<h2 class="titulo">A proposta em uma página</h2>
<p class="lede">Esta página responde às quatro perguntas que aparecem na primeira leitura de qualquer
proposta. As páginas seguintes existem para detalhar cada uma delas, e podem ser lidas depois ou junto
com a equipe.</p>
{defs([
    ('O que propomos',
     'Primeiro a base: domínio próprio, uma página do MOVE que guarde a prova das edições, a medição '
     'instalada na página de venda e a ficha do Google. Depois a operação: um pacote mensal que conduz '
     '@moveeconnect, @juharantes_ e @kalecozinhasensorial com uma grade editorial só, um contrato só e '
     'um relatório só.'),
    ('Quanto custa',
     '2.900 reais de entrada, pagos uma vez e parceláveis em até doze vezes de 242, mais o pacote '
     'mensal escolhido, de 2.000 a 3.000 reais. O pacote recomendado é o Crescimento, de 2.500 por '
     'mês. A verba de anúncios é paga direto à plataforma e não passa pela Oráculo.'),
    ('Quando começa',
     'Reunião de escopo de 30 minutos, sem custo, antes do contrato. Onboarding completo em 7 dias a '
     'partir da assinatura. O primeiro ciclo é de 90 dias, com leitura de resultado todo mês.'),
    ('O que fica com a contratante',
     'Domínio, página do MOVE, ficha do Google, pixel, conta de anúncios, lista de espera e arquivos '
     'editáveis ficam registrados no nome da contratante e continuam valendo se o contrato acabar.'),
])}
{tabela(['O que se contrata', 'Entrada', 'Mensal'], [
    ('__grupo__', 'Decisão 1, paga uma vez'),
    ('A base: domínio e página do MOVE, medição na página de venda e ficha do Google',
     '<b>2.900</b>', '<span class="na">sem mensal próprio</span>'),
    ('__grupo__', 'Decisão 2, o pacote que conduz as três contas'),
    ('Pacote Essencial', '<span class="na">sem entrada</span>', '2.000'),
    ('__destaque__', 'Pacote Crescimento, recomendado', '<span class="na">sem entrada</span>',
     '<b>2.500</b>'),
    ('Pacote Autoridade', '<span class="na">sem entrada</span>', '3.000'),
], 'Valores em reais, acrescidos de imposto. A sustentação da página e da medição está dentro do '
   'pacote mensal, sem cobrança à parte.',
   alinha={1: 'num', 2: 'num'}, compacta=True)}
{nota('Por que a base vem primeiro',
      'É a única parte com prazo externo. O público de remarketing só começa a existir depois que o '
      'pixel estiver instalado, e ele se forma com quem visita a página de venda: quem entrou antes '
      'da instalação não volta. A ficha do Google leva de dois a três meses para firmar posição. E a '
      'página do MOVE é o único lugar onde a prova das edições pode ficar de forma verificável, fora '
      'de uma legenda de Instagram.')}
''', 'Duas decisões, dois números. <span class="azul">O resto do documento é a prova.</span>')

    # ---------------------------------------------------------------- 2. diagnostico
    d.pag('Diagnóstico', f'''
<h2 class="titulo">De onde saiu cada recomendação deste documento</h2>
<p class="lede">Nenhum item desta proposta foi escolhido em reunião de briefing. Todos saíram da
auditoria de presença digital entregue em 4 de setembro, que leu 144 publicações uma a uma, as três
contas, os destaques, a busca no Google, o registro do domínio e o código da página de venda. A tabela
abaixo liga cada achado à parte da proposta que responde por ele.</p>
{tabela(['O que a auditoria apurou', 'O que isso significa', 'Onde entra'], [
    ('@moveeconnect tem 423 seguidores, contra 19.348 do perfil pessoal, e é marcada em 10% das '
     'publicações',
     'A conta que vende o ingresso é também a que o patrocinador abre para avaliar o evento. Hoje ela '
     'vale 2,2% da audiência que já foi construída.', '<b>Pacote</b>'),
    ('A mediana de um Reel é de 1.473 reproduções, 7,6% da base, e caiu 44% desde a primeira quinzena '
     'de junho',
     'Publicar mais parou de funcionar: no mesmo intervalo a cadência subiu de 1,19 para 1,53 '
     'publicação por dia. O que falta não é volume, é direção e alcance pago.', '<b>Pacote</b>'),
    ('A página de venda no Sympla não tem pixel da Meta, Google Analytics nem tag de conversão',
     'Cada edição passa sem deixar dado. Quem abriu a página e não comprou não pode ser reimpactado, '
     'e a edição seguinte recomeça do zero.', '<b>Base</b>'),
    ('Não existe domínio próprio, e moveeconnect.com.br estava livre no registro.br no dia da coleta',
     'Os 147 presentes da 1ª edição, os patrocinadores e a imprensa não têm onde morar de forma '
     'verificável. A busca pela marca devolve, na quarta posição, o site de outra empresa.',
     '<b>Base</b>'),
], FONTE_AUDITORIA)}
{nota('A auditoria é um documento separado',
      'O relatório de presença digital acompanha esta proposta, com a metodologia, as fontes, a data '
      'de cada coleta, a curva de alcance quinzena a quinzena e o comparativo com sete contas de '
      'networking do Distrito Federal medidas na mesma praça. Esta proposta cita apenas os quatro '
      'achados que definem o escopo, para não repetir o que já está lá.')}
''', 'A proposta não começou numa reunião. <span class="azul">Começou na leitura dos dados públicos das três contas.</span>')

    # ---------------------------------------------------------------- 3. a base
    d.pag('A base', f'''
<h2 class="titulo">Decisão 1: a base, construída uma vez</h2>
<p class="lede">Esta é a parte paga uma única vez. Ela constrói os três ativos que hoje não existem e
que nenhum pacote mensal consegue substituir. Tudo o que é construído aqui fica registrado no nome da
contratante e continua valendo se o contrato acabar.</p>
{tabela(['Obra', 'O que inclui', 'Valor'], [
    ('__grupo__', 'A base recomendada'),
    ('Domínio e página do MOVE',
     'Registro de moveeconnect.com.br e uma página única com o que é o MOVE, as edições já realizadas '
     'com o número de presentes, os patrocinadores, a imprensa e um formulário de lista de espera '
     'ligado ao WhatsApp. Título, meta description, Open Graph e dados estruturados configurados. '
     'Entrega em 3 semanas.', '1.800'),
    ('Medição na página de venda',
     'Pixel da Meta com API de conversões, Google Analytics 4 e tag de conversão instalados no painel '
     'do Sympla e na página do MOVE, com os seis eventos de compra ligados. É o que cria o público de '
     'remarketing e permite conferir o que cada edição gerou.', '700'),
    ('Perfil da Empresa no Google',
     'Abertura da ficha do MOVE na categoria de organizador de eventos, com área de atendimento em '
     'Brasília, fotos das edições, horários, link da página e cadastro nos diretórios de evento que '
     'aparecem na busca da praça.', '900'),
    ('__total__', 'Somando os três itens', '', '3.400'),
    ('__total__', 'Contratados juntos, a entrada é', '', '<b>2.900</b>'),
    ('__grupo__', 'Item da mesma etapa, contratável quando fizer sentido'),
    ('Atendimento no WhatsApp',
     'Conta oficial liberada, comprovação da empresa junto à Meta, primeira resposta automática, '
     'triagem por assunto e transferência com a ficha preenchida. Substitui o botão de ligação que '
     'hoje é o único contato oferecido pelo perfil.', '3.200'),
], 'Valores em reais, acrescidos de imposto, parceláveis em até doze vezes. A manutenção do que é '
   'construído aqui já está dentro do pacote mensal, sem cobrança separada. Esta base é menor que a '
   'praticada pela Oráculo em outros contratos porque a auditoria não encontrou necessidade de site '
   'institucional: o que falta é endereço próprio, medição e ficha de busca.')}
''', 'O que foi construído fica no nome da contratante <span class="azul">e continua valendo se o contrato acabar.</span>')

    # ---------------------------------------------------------------- 4. os pacotes
    d.pag('Os três pacotes', planos_com_escopo(
        'Decisão 2: o pacote que conduz as três contas',
        'Os três níveis cobrem @moveeconnect, @juharantes_ e @kalecozinhasensorial, com uma grade '
        'editorial só e um relatório só. O que separa um nível do outro é o volume publicado, o '
        'alcance pago e a profundidade do acompanhamento. Esta página traz as linhas que decidem a '
        'escolha, e a seguinte abre o escopo item a item.',
        ('2.000', '2.500', '3.000'),
        [('Conteúdo publicado por mês, somando as três contas', [
            ('Publicações de feed', '6', '10', '14'),
            ('Stories', '12', '20', '30'),
            ('Reels editados', '2', '4', '6'),
          ]),
         ('Anúncios', [
            ('Meta Ads, no Instagram e no Facebook', 'nao', 'sim', 'sim'),
            ('Campanhas ativas ao mesmo tempo', 'nao', 'até 3', 'até 6'),
            ('Criativos de anúncio por mês', 'nao', '6', '10'),
          ]),
         ('Acompanhamento', [
            ('Relatório de conteúdo e de campanha', 'mensal', 'mensal', 'quinzenal'),
            ('Reunião estratégica', 'nao', 'mensal', 'quinzenal'),
            ('Origem das conversas de WhatsApp', 'nao', 'sim', 'sim'),
          ]),
         ('Verba de anúncios, paga direto à plataforma', [
            ('Faixa recomendada por mês', 'nao', '600 a 1.200', '1.200 a 2.500'),
          ])],
        FONTE_PACOTES),
        'Uma grade, um contrato, um relatório. <span class="azul">Três contas deixam de ser três conversas.</span>')

    # ---------------------------------------------------------------- 5. escopo
    d.pag('Escopo', escopo(
        'O que entra em cada pacote, item a item',
        'A página anterior traz o que decide a escolha. Esta abre o restante do escopo, inclusive como '
        'o volume se divide entre as três contas, para que não reste dúvida sobre o que está '
        'contratado. Nenhuma entrega deste documento existe fora desta tabela.',
        [('Feito no primeiro mês, sem custo separado', [
            ('Bio e botão de contato refeitos nas três contas', 'sim', 'sim', 'sim'),
            ('Destaques reordenados, com as pastas de negócio na frente', 'sim', 'sim', 'sim'),
            ('Contagem de curtidas reativada nas peças de venda', 'sim', 'sim', 'sim'),
            ('Linhas editoriais e grade do mês', 'sim', 'sim', 'sim'),
            ('Sistema de design próprio do MOVE', 'nao', 'sim', 'sim'),
            ('Arquivos editáveis entregues', 'nao', 'sim', 'sim'),
          ]),
         ('Como as publicações de feed se dividem entre as contas', [
            ('No @moveeconnect, a conta que vende', '3', '5', '7'),
            ('No @juharantes_, a conta que tem a audiência', '2', '3', '5'),
            ('No @kalecozinhasensorial, a experiência do evento', '1', '2', '2'),
            ('Dessas, publicadas em colaboração, que aparecem em duas contas', '2', '4', '6'),
          ]),
         ('Rotina de produção', [
            ('Roteiro, edição, legenda e capa', 'sim', 'sim', 'sim'),
            ('Grade do mês proposta até o dia 25', 'sim', 'sim', 'sim'),
            ('Resposta a comentário e a mensagem', 'nao', 'sim', 'sim'),
          ]),
         ('Operação de cada edição do MOVE', [
            ('Sequência de venda do ingresso, do anúncio ao último dia', 'sim', 'sim', 'sim'),
            ('Roteiro de captação combinado antes do dia do evento', 'sim', 'sim', 'sim'),
            ('Público de remarketing de quem visitou e não comprou', 'nao', 'sim', 'sim'),
            ('Página própria da edição, publicada no domínio', 'nao', 'nao', 'sim'),
          ]),
         ('Campanhas', [
            ('Públicos por interesse e por lista de participantes', 'nao', 'sim', 'sim'),
            ('Otimização e ajuste', 'nao', 'semanal', '2 vezes por semana'),
            ('Relatório de aplicação da verba', 'nao', 'sim', 'sim'),
          ]),
         ('Sustentação da base, quando ela for contratada', [
            ('Atualização, cópia de segurança e disponibilidade da página', 'sim', 'sim', 'sim'),
            ('Manutenção da ficha do Google e da medição', 'sim', 'sim', 'sim'),
          ])],
        FONTE_ESCOPO),
        'Uma tabela só, três colunas. <span class="azul">Nada é prometido fora dela.</span>')

    # ---------------------------------------------------------------- 6. ciclo de 90 dias
    d.pag('Primeiros 90 dias', f'''
<h2 class="titulo">O que acontece nos primeiros 90 dias</h2>
<p class="lede">Este é o único cronograma do documento, e cada linha diz a partir de qual pacote ela
entra. Quem contrata o Essencial recebe exatamente o que está marcado como Essencial, e nada além disso
é prometido aqui.</p>
{defs([
    ('Antes de 19 de setembro, se houver tempo hábil',
     'Pixel da Meta e Google Analytics instalados no painel do Sympla antes da última semana de venda, '
     'botão do perfil trocado para WhatsApp, contagem de curtidas reativada nas peças do evento, três '
     'publicações fixadas no topo e roteiro de captação combinado para o dia. A instalação do pixel faz '
     'parte da <b>base</b>; o restante entra em qualquer pacote.'),
    ('Primeiros 7 dias, onboarding',
     'Acessos das três contas e do Sympla recebidos, contrato assinado, reunião de abertura e primeira '
     'grade editorial aprovada. Ficha do Google aberta no mesmo prazo. Entra em qualquer pacote.'),
    ('Mês 1, a marca ganha corpo',
     'Bio, botão e destaques refeitos nas três contas, com as pastas de negócio na frente. Domínio no ar '
     'com a página do MOVE, as duas edições e a lista de espera. O sistema de design próprio e a entrega '
     'dos arquivos editáveis entram a partir do pacote <b>Crescimento</b>.'),
    ('Mês 2, a audiência migra',
     'Toda publicação de marca passa a sair em colaboração, para aparecer no perfil pessoal e na conta do '
     'MOVE ao mesmo tempo, que é o caminho mais barato de tirar a marca dos 423 seguidores. As campanhas '
     'e os públicos por lista de participantes entram a partir do pacote <b>Crescimento</b>.'),
    ('Mês 3, a próxima edição começa a ser vendida',
     'Lista de espera transformada na primeira leva de compradores, remarketing sobre quem visitou a '
     'página e não comprou, e leitura do que cada peça gerou. A página própria da edição entra no pacote '
     '<b>Autoridade</b>.'),
    ('Depois dos 90 dias',
     'Ficha do Google firmando posição na busca por networking empresarial em Brasília, conteúdo de busca '
     'na página do MOVE e base própria de participantes para recompra e indicação.'),
])}
{nota('O que não é prometido neste documento',
      'Todas as metas do primeiro ciclo são de alcance, de formação de lista e de estrutura instalada. A '
      'Oráculo não promete número de ingressos vendidos nem faturamento de edição, porque o fechamento '
      'depende do preço, da data, do formato e da operação comercial da contratante. O que é medido e '
      'cobrado é o que está na tabela de escopo.')}
''', 'Um cronograma só, com o pacote marcado em cada linha. <span class="azul">Sem promessa fora do que foi contratado.</span>')

    # ---------------------------------------------------------------- 7. como funciona
    d.pag('Como funciona', f'''
<h2 class="titulo">Como o trabalho acontece no dia a dia</h2>
<p class="lede">A parte que mais atrasa um contrato de marketing não é a produção, é a aprovação. Por
isso o que cabe a cada lado está escrito aqui, antes da assinatura.</p>
{duas_colunas(
    'O que a Oráculo faz',
    ['Propõe a grade editorial do mês até o dia 25 do mês anterior, com tema, formato, conta de destino '
     'e objetivo comercial de cada peça.',
     'Produz roteiro, arte, edição, legenda e capa a partir do material bruto gravado pela equipe.',
     'Publica nas três contas no calendário aprovado, sem depender de nova confirmação a cada peça.',
     'Gere as campanhas, acompanha a verba diariamente e ajusta público, criativo e orçamento, nos '
     'pacotes que incluem anúncio.',
     'Entrega um relatório único das três contas até o dia 10, e conduz a reunião de leitura nos pacotes '
     'que a incluem.'],
    'O que esperamos da contratante',
    ['Um ponto focal único para aprovar a grade e responder dúvidas, com resposta em até 3 dias úteis.',
     'Envio do material bruto combinado: gravações do dia a dia, bastidores das edições, novidades de '
     'patrocinador e as datas das próximas edições com antecedência de 60 dias.',
     'Acesso às três contas de Instagram, ao Facebook, ao Google, ao painel do Sympla e ao domínio, '
     'todos no nome da própria contratante.',
     'Atendimento das conversas geradas dentro do horário comercial, que é onde a campanha vira ingresso '
     'vendido.',
     'Trinta minutos por mês para a reunião de leitura, quando o pacote contratado a inclui.'])}
{nota('Aprovação por silêncio',
      'A grade editorial enviada e não respondida em 3 dias úteis é considerada aprovada. A regra existe '
      'para proteger o calendário: publicação atrasada por falta de resposta custa alcance, e o algoritmo '
      'não devolve o que se perdeu no intervalo. Em semana de edição do MOVE o prazo cai para 1 dia útil, '
      'porque a janela de venda é curta.')}
''', 'Nenhum contrato de marketing funciona sem contrapartida. <span class="azul">A daqui cabe em cinco linhas.</span>')

    # ---------------------------------------------------------------- 8. condicoes
    d.pag('Condições', f'''
<h2 class="titulo">Condições comerciais e custos que não passam pela Oráculo</h2>
<p class="lede">Esta página existe para que nenhuma pergunta de contrato precise ser feita por mensagem
depois. Tudo o que é cobrado, por quem e quando está aqui.</p>
<h3 class="sub">Condições comerciais</h3>
<p class="texto">{CONDICOES}</p>
<h3 class="sub">Pago diretamente ao fornecedor</h3>
{tabela(['Item', 'Quanto', 'Quando se aplica'], [
    ('Verba de anúncios, paga à plataforma', '600 a 2.500 por mês',
     'A partir do pacote Crescimento, conforme o nível'),
    ('Registro do domínio no Registro.br', 'cerca de 40 por ano', 'Na contratação da base'),
    ('Hospedagem e e-mail no domínio próprio', 'cerca de 150 por mês', 'A partir da entrega da página'),
    ('Taxa do Sympla sobre cada ingresso', '10% do valor do ingresso',
     'Já em vigor hoje, cobrada pela plataforma'),
    ('Sistema de atendimento no WhatsApp', 'cerca de 500 por mês', 'Se o atendimento for contratado'),
], 'Valores em reais. Faixas conforme as tabelas públicas dos fornecedores, consultadas em 09/09/2026. '
   'A taxa do Sympla foi lida na própria página do evento em 04/09/2026. Nenhum destes itens passa pela '
   'Oráculo, e todos ficam registrados no nome da contratante.', compacta=True)}
{nota('O que o pacote mensal não cobre',
      'Fotógrafo e cinegrafista no dia da edição, produção de página nova fora do escopo da base, '
      'locução profissional, licença de banco de imagens e cachê de convidado são orçados à parte quando '
      'houver necessidade. A Oráculo indica e coordena o fornecedor, e o serviço é pago diretamente a '
      'ele.')}
''', 'Preço fechado, contrapartida escrita <span class="azul">e nenhuma linha em aberto.</span>')

    # ---------------------------------------------------------------- contracapa
    d.contracapa(
        'O próximo passo é uma reunião de 30 minutos',
        'A reunião serve para ajustar o escopo ao caso concreto, confirmar prioridades e definir a data '
        'de início. Não há custo e não há compromisso de contratação.',
        [('Reunião', '30 minutos, presencial em Brasília ou por vídeo'),
         ('Onboarding', '7 dias a partir da assinatura'),
         ('A base', '2.900 reais, pagos uma vez, parceláveis em até 12 vezes de 242'),
         ('O pacote', '2.500 reais por mês no Crescimento, de 2.000 a 3.000 conforme o nível')],
        'Baseado na auditoria de presença digital<br>entregue em 4 de setembro de 2026')

    return d.salvar(
        os.path.join(RAIZ, 'JulianaArantes', 'Proposta-Comercial.html'),
        'Proposta Comercial, Juliana Arantes e MOVE &amp; Connect, Oráculo Tecnologia',
        'Proposta comercial da Oráculo Tecnologia para Juliana Arantes e a marca MOVE &amp; Connect, de '
        'Brasília: a base construída uma vez e a operação mensal das três contas em três pacotes, a '
        'partir da auditoria de presença digital de 4 de setembro de 2026.')


if __name__ == '__main__':
    print('gerando proposta de Juliana Arantes...')
    erros = bp.validar('JulianaArantes', build_juliana())
    print('RESULTADO:', 'tudo ok' if not erros else erros)
