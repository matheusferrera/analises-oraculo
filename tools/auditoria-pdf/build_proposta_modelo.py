# -*- coding: utf-8 -*-
"""Proposta comercial modelo da Oraculo Tecnologia.

Documento generico, com o cliente chamado literalmente de Cliente, que serve a dois
propositos: mostrar a media de preco praticada e servir de molde para as proximas propostas.

Estrutura decidida em 20/08/2026, depois da leitura da proposta do Grupo Sinfonya Turismo,
que estava confusa para o cliente. Duas decisoes, nao tres:
  1. a base, construida uma vez, com pagamento unico
  2. a operacao mensal, em tres pacotes que ja somam conteudo, anuncio e sustentacao

Isso elimina as nove combinacoes possiveis do formato anterior, que tinha tres niveis de
redes sociais e tres niveis de trafego pago contratados em separado. Os valores sao os
mesmos do combo antigo: entrada 7.500 e mensal 4.999 no nivel recomendado.

Reaproveita os helpers de build_propostas_debem.py.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_propostas_debem as bp

bp.DATA = '20 de agosto de 2026'

tabela = bp.tabela
defs = bp.defs
nota = bp.nota
duas_colunas = bp.duas_colunas
planos_com_escopo = bp.planos_com_escopo
escopo = bp.escopo
RAIZ = bp.RAIZ


class DocModelo(bp.Doc):
    """Mesma classe da Debem, com a contracapa generica e destinatario configuravel."""

    def __init__(self, cabecalho, destinatario='ao Cliente'):
        super().__init__(cabecalho)
        self.destinatario = destinatario

    def contracapa(self, h2, lede, linhas, rodape_esq):
        ls = ''.join(f'<div class="fim-linha"><b>{a}</b><span>{b}</span></div>' for a, b in linhas)
        self.bruta('<section class="pagina fim">'
                   '<div class="capa-topo">'
                   f'<img src="data:image/png;base64,{bp.LOGO}" alt="Oráculo">'
                   '<div class="capa-meta">Próximo passo<br>Reunião de alinhamento</div>'
                   '</div>'
                   '<div style="margin-top:auto">'
                   f'<h2>{h2}</h2><p class="fim-lede">{lede}</p>'
                   f'<div class="fim-linhas">{ls}</div></div>'
                   '<div class="fim-rodape">'
                   f'<div><b>Oráculo Tecnologia</b>{rodape_esq}</div>'
                   f'<div>Documento confidencial, destinado exclusivamente {self.destinatario}<br>'
                   'Válido por 30 dias a partir do envio</div></div></section>')


# ---------------------------------------------------------------- blocos de texto
CONDICOES_MODELO = (
    'A base é paga uma vez, na assinatura, e é parcelável em até doze vezes. O pacote mensal é '
    'contrato mensal, sem fidelidade no primeiro mês, com vencimento no mesmo dia de cada mês '
    'contado a partir da assinatura, e cancelamento com aviso de 30 dias, sem multa. A troca de '
    'pacote pode ser feita a qualquer momento, para cima ou para baixo, valendo no mês seguinte. '
    'Onboarding completo em 7 dias a partir da assinatura. A verba de anúncios e as mensalidades '
    'de ferramenta são pagas diretamente aos fornecedores, com relatório de aplicação todo mês. '
    'Valores em reais, acrescidos de imposto. Esta proposta é válida por 30 dias a partir da data '
    'de envio.')

FONTE_MODELO = (
    'Documento modelo. O cliente citado é fictício e os valores são os efetivamente praticados '
    'pela Oráculo em agosto de 2026. Numa proposta real, cada linha de diagnóstico cita o número '
    'apurado e a data da coleta.')

FONTE_PACOTES = (
    'Valores em reais, acrescidos de imposto, sem valor de entrada. O pacote soma o que antes era '
    'cobrado em separado: gestão de conteúdo, gestão de anúncios e sustentação da base. Somados '
    'item a item, os mesmos escopos custariam 3.799, 5.599 e 8.199. A verba de anúncios é do '
    'Cliente, fica na conta do Cliente e não passa pela Oráculo. Quem não pretende anunciar não '
    'deve contratar por aqui: nesse caso a gestão de conteúdo é contratada sozinha, por 1.999, '
    '3.199 ou 4.999 por mês.')


def build_modelo():
    d = DocModelo('Cliente')

    # ---------------------------------------------------------------- capa
    d.capa(
        'Cliente',
        'Proposta comercial: a base construída uma vez, e a operação mensal em três pacotes',
        'Esta proposta responde à auditoria de presença digital feita antes de qualquer conversa '
        'comercial. São duas decisões, e só duas: construir a base, que é paga uma vez, e escolher '
        'o pacote mensal que conduz a operação. A página seguinte resume o documento inteiro, e '
        'quem parar nela já tem o necessário para decidir.',
        [('2', 'decisões a tomar'), ('7.500', 'reais de entrada, uma vez'),
         ('4.999', 'reais por mês, no pacote recomendado'), ('90', 'dias do primeiro ciclo')])

    # ---------------------------------------------------------------- 1. resumo
    d.pag('Resumo', f'''
<h2 class="titulo">A proposta em uma página</h2>
<p class="lede">Esta página responde às quatro perguntas que aparecem na primeira leitura de qualquer
proposta. As páginas seguintes existem para detalhar cada uma delas, e podem ser lidas depois ou junto
com a equipe.</p>
{defs([
    ('O que propomos',
     'Primeiro a base: site, ficha do Google, medição e a estrutura de anúncios, construídos uma vez e '
     'registrados no nome do Cliente. Depois a operação: um pacote mensal que já reúne conteúdo, '
     'anúncio e sustentação, sem contratos separados para cada frente.'),
    ('Quanto custa',
     '7.500 reais de entrada, pagos uma vez e parceláveis em até doze vezes, mais o pacote mensal '
     'escolhido, de 3.499 a 7.499 reais. O pacote recomendado é o Crescimento, de 4.999 por mês. A '
     'verba de anúncios é paga direto à plataforma e não passa pela Oráculo.'),
    ('Quando começa',
     'Reunião de escopo de 30 minutos, sem custo, antes do contrato. Onboarding completo em 7 dias a '
     'partir da assinatura. O primeiro ciclo é de 90 dias, com leitura de resultado todo mês.'),
    ('O que fica com o Cliente',
     'Site, domínio, ficha do Google, conta de anúncios, número de WhatsApp e arquivos editáveis do '
     'sistema de design ficam no nome do Cliente e continuam valendo se o contrato acabar.'),
])}
{tabela(['O que se contrata', 'Entrada', 'Mensal'], [
    ('__grupo__', 'Decisão 1, paga uma vez'),
    ('A base: site, ficha do Google, medição e estrutura de anúncios', '<b>7.500</b>',
     '<span class="na">sem mensal próprio</span>'),
    ('__grupo__', 'Decisão 2, o pacote que conduz a operação'),
    ('Pacote Essencial', '<span class="na">sem entrada</span>', '3.499'),
    ('__destaque__', 'Pacote Crescimento, recomendado', '<span class="na">sem entrada</span>',
     '<b>4.999</b>'),
    ('Pacote Autoridade', '<span class="na">sem entrada</span>', '7.499'),
], 'Valores em reais, acrescidos de imposto. A sustentação do site e da medição está dentro do pacote '
   'mensal, sem cobrança à parte. Sem a construção da base, o pacote não tem o que sustentar e o mensal '
   'cai 600 reais em qualquer um dos três níveis.',
   alinha={1: 'num', 2: 'num'}, compacta=True)}
{nota('Por que a base vem primeiro',
      'É a única parte com prazo externo: a contagem de reputação da ficha do Google só começa depois '
      'que ela existe, e leva de dois a três meses para firmar posição. É também a base que instala a '
      'medição sem a qual nada do pacote mensal pode ser conferido.')}
''', 'Duas decisões, dois números. <span class="azul">O resto do documento é a prova.</span>')

    # ---------------------------------------------------------------- 2. diagnostico
    d.pag('Diagnóstico', f'''
<h2 class="titulo">De onde saiu cada recomendação deste documento</h2>
<p class="lede">Nenhum item desta proposta foi escolhido em reunião de briefing. Todos saíram da
auditoria de presença digital feita antes do primeiro contato comercial, que mede quatro pilares: a
busca no Google, o site, o Instagram e os diretórios locais. A tabela abaixo liga cada achado à parte
da proposta que responde por ele.</p>
{tabela(['O que a auditoria apurou', 'O que isso significa', 'Onde entra'], [
    ('A busca pelo nome da marca devolve ficha incompleta, sem categoria correta e sem avaliação recente',
     'Quem procura pelo nome já decidiu comparar. A ficha é a primeira impressão, e hoje ela está vazia '
     'diante de concorrentes com centenas de avaliações.', '<b>Base</b>'),
    ('O perfil publica sem cadência definida e nenhum caminho de contato é rastreável',
     'O conteúdo existe, mas não gera conversa identificável. É impossível responder quanto o Instagram '
     'trouxe de oportunidade no mês.', '<b>Pacote</b>'),
    ('Todo o alcance atual vem de quem já segue a marca',
     'Sem alcance pago, o público novo depende do acaso da distribuição, e o crescimento fica preso ao '
     'tamanho da base atual.', '<b>Pacote</b>'),
], FONTE_MODELO)}
{nota('A auditoria é um documento separado',
      'O relatório de presença digital vai junto desta proposta, com a metodologia, as fontes, a data '
      'de cada coleta e o comparativo com os concorrentes medidos na mesma praça. Esta proposta cita '
      'apenas os três achados que definem o escopo, para não repetir o que já está lá.')}
''', 'A proposta não começou numa reunião. <span class="azul">Começou na leitura dos dados públicos da marca.</span>')

    # ---------------------------------------------------------------- 3. a base
    d.pag('A base', f'''
<h2 class="titulo">Decisão 1: a base, construída uma vez</h2>
<p class="lede">Esta é a parte paga uma única vez. Ela constrói os ativos que hoje não existem e que
nenhum pacote mensal consegue substituir. Tudo o que é construído aqui fica registrado no nome do
Cliente e continua valendo se o contrato acabar.</p>
{tabela(['Obra', 'O que inclui', 'Valor'], [
    ('__grupo__', 'A base recomendada'),
    ('Site profissional',
     'Site de 5 a 7 páginas, com página por serviço, página institucional e formulário ligado ao '
     'WhatsApp. Título, meta description, Open Graph e dados estruturados configurados. Entrega em '
     '4 a 6 semanas.', '3.500'),
    ('Perfil da Empresa no Google',
     'Abertura ou recuperação da ficha, categoria principal e secundárias, fotos, horários, área de '
     'atendimento, serviços listados e cadastro nos diretórios que aparecem na busca da praça.',
     '2.000'),
    ('Medição de ponta a ponta',
     'Google Analytics, Search Console, eventos de clique e de conversa e painel único ligando busca, '
     'site, perfil e WhatsApp. É o que permite conferir tudo o que o pacote mensal entrega.', '1.400'),
    ('Estrutura de anúncios',
     'Gerenciador de Negócios aberto e verificado, pixel e API de conversões instalados, públicos por '
     'praça e por serviço e a primeira estrutura de campanhas montada.', '1.400'),
    ('__total__', 'Somando os quatro itens', '', '8.300'),
    ('__total__', 'Contratados juntos, a entrada é', '', '<b>7.500</b>'),
    ('__grupo__', 'Itens da mesma etapa, contratáveis quando fizer sentido'),
    ('Atendimento no WhatsApp',
     'Conta oficial liberada, comprovação da empresa junto à Meta, primeira resposta automática, '
     'triagem por assunto e transferência para a pessoa certa com a ficha preenchida.', '3.200'),
    ('Padronização de endereço e telefones',
     'Uma só grafia de endereço e um telefone público por unidade, aplicados no site, no Google, no '
     'Instagram e nos diretórios.', '900'),
], 'Valores em reais, acrescidos de imposto, parceláveis em até doze vezes. A manutenção do que é '
   'construído aqui já está dentro do pacote mensal, sem cobrança separada.')}
''', 'O que foi construído fica no nome do Cliente <span class="azul">e continua valendo se o contrato acabar.</span>')

    # ---------------------------------------------------------------- 4. os pacotes
    d.pag('Os três pacotes', planos_com_escopo(
        'Decisão 2: o pacote que conduz a operação',
        'Um pacote só, com conteúdo, anúncio e sustentação da base no mesmo contrato e no mesmo valor. '
        'O que separa um nível do outro é o volume publicado, o alcance pago e a profundidade do '
        'acompanhamento. Esta página traz as linhas que decidem a escolha, e a seguinte abre o escopo '
        'item a item.',
        ('3.499', '4.999', '7.499'),
        [('Conteúdo publicado por mês', [
            ('Publicações de feed', '6', '12', '18'),
            ('Stories', '10', '20', '30'),
            ('Reels editados', '2', '4', '8'),
          ]),
         ('Anúncios', [
            ('Meta Ads, no Instagram e no Facebook', 'sim', 'sim', 'sim'),
            ('Google Ads, na busca', 'nao', 'sim', 'sim'),
            ('Campanhas ativas ao mesmo tempo', 'até 2', 'até 4', 'até 8'),
            ('Criativos de anúncio por mês', '4', '8', '14'),
          ]),
         ('Acompanhamento', [
            ('Relatório mensal de conteúdo e de campanha', 'sim', 'sim', 'sim'),
            ('Origem das conversas de WhatsApp', 'nao', 'sim', 'sim'),
            ('Reunião estratégica', 'nao', 'mensal', 'quinzenal'),
          ]),
         ('Verba de anúncios, paga direto à plataforma', [
            ('Faixa recomendada por mês, somando as plataformas', '800 a 1.200', '1.500 a 3.000',
             '3.000 a 6.000'),
          ])],
        FONTE_PACOTES),
        'Um contrato, um valor, um relatório. <span class="azul">Conteúdo e anúncio deixam de ser duas conversas.</span>')

    # ---------------------------------------------------------------- 5. escopo
    d.pag('Escopo', escopo(
        'O que entra em cada pacote, item a item',
        'A página anterior traz o que decide a escolha. Esta abre o restante do escopo, para que não '
        'reste dúvida sobre o que está contratado. Nenhuma entrega deste documento existe fora desta '
        'tabela.',
        [('Feito no primeiro mês, sem custo separado', [
            ('Organização do perfil e nova bio', 'sim', 'sim', 'sim'),
            ('Destaques reorganizados por jornada', 'sim', 'sim', 'sim'),
            ('Linhas editoriais e grade do mês', 'sim', 'sim', 'sim'),
            ('Sistema de design próprio do perfil', 'nao', 'sim', 'sim'),
            ('Arquivos editáveis entregues', 'nao', 'sim', 'sim'),
          ]),
         ('Rotina de produção', [
            ('Roteiro, edição, legenda e capa', 'sim', 'sim', 'sim'),
            ('Grade do mês proposta até o dia 25', 'sim', 'sim', 'sim'),
            ('Resposta a comentário e a mensagem', 'nao', 'sim', 'sim'),
          ]),
         ('Campanhas', [
            ('Públicos por praça e por serviço', 'nao', 'sim', 'sim'),
            ('Otimização e ajuste', 'semanal', '2 vezes por semana', 'contínua'),
            ('Teste de público e de página de destino', 'nao', 'nao', 'sim'),
            ('Relatório de aplicação da verba', 'sim', 'sim', 'sim'),
          ]),
         ('Sustentação da base, quando ela for contratada', [
            ('Atualização, cópia de segurança e disponibilidade do site', 'sim', 'sim', 'sim'),
            ('Manutenção da ficha do Google e da medição', 'sim', 'sim', 'sim'),
          ])],
        'Story é contado por tela, e publicação de feed é um post no perfil, imagem única ou carrossel, '
        'com quantas telas o assunto pedir. Reel editado é montado a partir do material gravado pela '
        'equipe do Cliente. Nenhum dos três pacotes inclui fotógrafo ou cinegrafista.'),
        'Uma tabela só, três colunas. <span class="azul">Nada é prometido fora dela.</span>')

    # ---------------------------------------------------------------- 6. ciclo de 90 dias
    d.pag('Primeiros 90 dias', f'''
<h2 class="titulo">O que acontece nos primeiros 90 dias</h2>
<p class="lede">Este é o único cronograma do documento, e cada linha diz a partir de qual pacote ela
entra. Quem contrata o Essencial recebe exatamente o que está marcado como Essencial, e nada além
disso é prometido aqui.</p>
{defs([
    ('Primeiros 7 dias, onboarding',
     'Acessos recebidos, contrato assinado, reunião de abertura com a equipe do Cliente e primeira grade '
     'editorial aprovada. Ficha do Google aberta ou reivindicada no mesmo prazo. Entra em qualquer pacote.'),
    ('Mês 1, fundação',
     'Perfil organizado, bio reescrita, destaques reordenados por jornada de compra e medição instalada. '
     'O sistema de design próprio e a entrega dos arquivos editáveis entram a partir do pacote '
     '<b>Crescimento</b>.'),
    ('Mês 2, alcance',
     'Grade editorial em ritmo pleno, primeira leva de criativos no ar e campanhas de alcance ativadas. '
     'Anúncio de busca no Google e públicos segmentados por praça entram a partir do pacote '
     '<b>Crescimento</b>.'),
    ('Mês 3, conversão',
     'Caminho rastreável entre a publicação e a conversa no WhatsApp, scripts de atendimento por tipo de '
     'pedido e primeiro relatório ligando peça publicada, clique e conversa aberta. O relatório de origem '
     'das conversas entra a partir do pacote <b>Crescimento</b>.'),
    ('Depois dos 90 dias, escala',
     'Ampliação dos formatos e dos públicos que provaram resultado, teste de página de destino e base '
     'própria de clientes para recompra e indicação. O teste de página de destino entra no pacote '
     '<b>Autoridade</b>.'),
])}
{nota('O que não é prometido neste documento',
      'Todas as metas do primeiro ciclo são de alcance, de qualificação de contato e de estrutura '
      'instalada. A Oráculo não promete número de vendas nem faturamento, porque o fechamento depende '
      'do atendimento e da operação comercial do Cliente. O que é medido e cobrado é o que está na '
      'tabela de escopo.')}
''', 'Um cronograma só, com o pacote marcado em cada linha. <span class="azul">Sem promessa fora do que foi contratado.</span>')

    # ---------------------------------------------------------------- 7. como funciona
    d.pag('Como funciona', f'''
<h2 class="titulo">Como o trabalho acontece no dia a dia</h2>
<p class="lede">A parte que mais atrasa um contrato de marketing não é a produção, é a aprovação. Por
isso o que cabe a cada lado está escrito aqui, antes da assinatura.</p>
{duas_colunas(
    'O que a Oráculo faz',
    ['Propõe a grade editorial do mês até o dia 25 do mês anterior, com tema, formato e objetivo '
     'comercial de cada peça.',
     'Produz roteiro, arte, edição, legenda e capa a partir do material bruto e das informações do '
     'Cliente.',
     'Publica no calendário aprovado, sem depender de nova confirmação a cada peça.',
     'Gere as campanhas, acompanha a verba diariamente e ajusta público, criativo e orçamento.',
     'Entrega um relatório único de conteúdo e de campanha até o dia 10, e conduz a reunião de leitura '
     'nos pacotes que a incluem.'],
    'O que esperamos do Cliente',
    ['Um ponto focal único para aprovar a grade e responder dúvidas, com resposta em até 3 dias úteis.',
     'Envio do material bruto combinado: fotos e vídeos da operação, novidades, casos e datas '
     'importantes do mês.',
     'Acesso às contas de Instagram, Facebook, Google e ao domínio, no nome da própria empresa.',
     'Atendimento das conversas geradas dentro do horário comercial, que é onde a campanha vira venda.',
     'Trinta minutos por mês para a reunião de leitura, quando o pacote contratado a inclui.'])}
{nota('Aprovação por silêncio',
      'A grade editorial enviada e não respondida em 3 dias úteis é considerada aprovada. A regra existe '
      'para proteger o calendário: publicação atrasada por falta de resposta custa alcance, e o algoritmo '
      'não devolve o que se perdeu no intervalo.')}
''', 'Nenhum contrato de marketing funciona sem contrapartida. <span class="azul">A daqui cabe em cinco linhas.</span>')

    # ---------------------------------------------------------------- 8. condicoes
    d.pag('Condições', f'''
<h2 class="titulo">Condições comerciais e custos que não passam pela Oráculo</h2>
<p class="lede">Esta página existe para que nenhuma pergunta de contrato precise ser feita por
mensagem depois. Tudo o que é cobrado, por quem e quando está aqui.</p>
<h3 class="sub">Condições comerciais</h3>
<p class="texto">{CONDICOES_MODELO}</p>
<h3 class="sub">Pago diretamente ao fornecedor</h3>
{tabela(['Item', 'Quanto', 'Quando se aplica'], [
    ('Verba de anúncios, paga à plataforma', '800 a 6.000 por mês', 'Em qualquer pacote, conforme o nível'),
    ('Sistema de atendimento no WhatsApp', 'cerca de 500 por mês', 'Se o atendimento for contratado'),
    ('Hospedagem e e-mail no domínio próprio', 'cerca de 150 por mês', 'A partir da entrega do site'),
    ('Registro do domínio no Registro.br', 'cerca de 40 por ano', 'Se o domínio for novo'),
], 'Valores em reais. Faixas conforme as tabelas públicas dos fornecedores, consultadas em 20/08/2026. '
   'Nenhum destes itens passa pela Oráculo, e todos ficam registrados no nome do Cliente.', compacta=True)}
{nota('O que o pacote mensal não cobre',
      'Captação profissional de foto e de vídeo, produção de página nova fora do escopo do site, '
      'tradução, locução profissional e licença de banco de imagens são orçados à parte quando houver '
      'necessidade. A Oráculo indica e coordena o fornecedor, e o serviço é pago diretamente a ele.')}
''', 'Preço fechado, contrapartida escrita <span class="azul">e nenhuma linha em aberto.</span>')

    # ---------------------------------------------------------------- contracapa
    d.contracapa(
        'O próximo passo é uma reunião de 30 minutos',
        'A reunião serve para ajustar o escopo ao caso concreto, confirmar prioridades e definir a data '
        'de início. Não há custo e não há compromisso de contratação.',
        [('Reunião', '30 minutos, presencial em Brasília ou por vídeo'),
         ('Onboarding', '7 dias a partir da assinatura'),
         ('A base', '7.500 reais, pagos uma vez, parceláveis em até 12 vezes de 625'),
         ('O pacote', '4.999 reais por mês no Crescimento, de 3.499 a 7.499 conforme o nível')],
        'Baseado na auditoria de presença digital<br>feita antes do primeiro contato comercial')

    return d.salvar(
        os.path.join(RAIZ, 'Modelo', 'Proposta-Comercial-Modelo.html'),
        'Proposta Comercial Modelo, Oráculo Tecnologia',
        'Proposta comercial modelo da Oráculo Tecnologia: a base construída uma vez e a operação '
        'mensal em três pacotes, com os valores praticados em agosto de 2026.')


if __name__ == '__main__':
    print('gerando proposta modelo...')
    erros = bp.validar('Modelo', build_modelo())
    print('RESULTADO:', 'tudo ok' if not erros else erros)
