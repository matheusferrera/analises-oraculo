# -*- coding: utf-8 -*-
"""Proposta comercial do Dr. Adriano Borges, cirurgiao plastico em Brasilia.

Segue o padrao decidido em 20/08/2026 (tools/auditoria-pdf/build_proposta_modelo.py):
duas decisoes, nao tres vertentes. A base construida uma vez, com pagamento unico, e a
operacao mensal em tres pacotes que ja somam conteudo, anuncio e sustentacao.

Reaproveita a classe DocModelo (contracapa com destinatario configuravel) do modelo e a
pagina de publicidade medica (Resolucao CFM 2.336/2023) da proposta do outro cirurgiao,
sem duplicar codigo.

Todos os numeros citados vem da auditoria de presenca digital de 17/08/2026, guardada em
DrAdrianoBorges/data/presenca-digital-20260817.json e em
DrAdrianoBorges/Analise-Presenca-Digital.html.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_propostas_debem as bp
import build_proposta_modelo as bm
import build_proposta_pedro as bpd

bp.DATA = '30 de agosto de 2026'

# a fonte da pagina do CFM vem da outra proposta e falava em clinica propria
bpd.CFM_FONTE = (
    'Resolução CFM nº 2.336, de 1º de setembro de 2023, que dispõe sobre a publicidade médica e '
    'revoga a Resolução CFM nº 1.974/2011. Leitura aplicada ao caso de um cirurgião plástico com '
    'consultório próprio em Brasília, sem caráter de parecer ético.')

tabela = bp.tabela
defs = bp.defs
nota = bp.nota
duas_colunas = bp.duas_colunas
planos_com_escopo = bp.planos_com_escopo
escopo = bp.escopo
RAIZ = bp.RAIZ

# ---------------------------------------------------------------- blocos de texto
FONTE_AUDITORIA = (
    'Auditoria de presença digital do Dr. Adriano Borges, coleta de 17/08/2026: Instagram '
    '@dr.adrianoborges pela API interna com sessão autenticada, 268 das 269 publicações do perfil; '
    'os perfis @drricardocintra, @dr.andrejardim e @drtristaomauricio pela mesma via, na mesma data; '
    'Google Search e Google Maps em pt-BR; dradrianoborges.com.br lido por requisição direta, com '
    'cabeçalhos, HTML e mapa do site; linktr.ee/dr.adrianoborges; Doctoralia e Facebook por '
    'navegação direta.')

FONTE_PACOTES = (
    'Valores em reais, acrescidos de imposto, sem valor de entrada. O pacote soma o que antes era '
    'cobrado em separado: gestão de conteúdo, gestão de anúncios e sustentação da base. Somados '
    'item a item, os mesmos escopos custariam 3.799, 5.599 e 8.199. A verba de anúncios é do '
    'contratante, fica na conta do contratante e não passa pela Oráculo. Quem não pretende anunciar '
    'não deve contratar por aqui: nesse caso a gestão de conteúdo é contratada sozinha, por 1.999, '
    '3.199 ou 4.999 por mês.')

CONDICOES = (
    'A base é paga uma vez, na assinatura, e é parcelável em até doze vezes de 625 reais. O pacote '
    'mensal é contrato mensal, sem fidelidade no primeiro mês, com vencimento no mesmo dia de cada '
    'mês contado a partir da assinatura, e cancelamento com aviso de 30 dias, sem multa. A troca de '
    'pacote pode ser feita a qualquer momento, para cima ou para baixo, valendo no mês seguinte. '
    'Onboarding completo em 7 dias a partir da assinatura. A verba de anúncios e as mensalidades de '
    'ferramenta são pagas diretamente aos fornecedores, com relatório de aplicação todo mês. '
    'Valores em reais, acrescidos de imposto. Esta proposta é válida por 30 dias a partir da data '
    'de envio.')


def build_adriano():
    d = bm.DocModelo('Dr. Adriano Borges', destinatario='ao Dr. Adriano Borges')

    # ---------------------------------------------------------------- capa
    d.capa(
        'Dr. Adriano Borges, cirurgião plástico, CRM-DF 16513 / RQE 15481 e 15482',
        'Proposta comercial: a base construída uma vez, e a operação mensal em três pacotes',
        'Esta proposta responde à auditoria de presença digital entregue em 17 de agosto de 2026, '
        'que mediu 268 publicações do perfil, o site próprio, a busca no Google e os diretórios, e '
        'comparou o resultado com três cirurgiões que disputam a mesma praça. São duas decisões, e '
        'só duas: construir a base, que é paga uma vez, e escolher o pacote mensal que conduz a '
        'operação. A página seguinte resume o documento inteiro, e quem parar nela já tem o '
        'necessário para decidir.',
        [('2', 'decisões a tomar'), ('7.500', 'reais de entrada, uma vez'),
         ('4.999', 'reais por mês, no pacote recomendado'), ('90', 'dias do primeiro ciclo')])

    # ---------------------------------------------------------------- 1. resumo
    d.pag('Resumo', f'''
<h2 class="titulo">A proposta em uma página</h2>
<p class="lede">Esta página responde às quatro perguntas que aparecem na primeira leitura de qualquer
proposta. As páginas seguintes existem para detalhar cada uma delas, e podem ser lidas depois ou
junto com a equipe do consultório.</p>
{defs([
    ('O que propomos',
     'Primeiro a base: site próprio reconstruído no domínio que já ocupa o primeiro lugar orgânico '
     'na busca pelo nome, consolidação das três fichas hoje ativas no Google, medição de ponta a '
     'ponta e a estrutura de anúncios, que ainda não existe. Depois a operação: um pacote mensal '
     'que já reúne conteúdo, anúncio e sustentação, sem contratos separados para cada frente.'),
    ('Quanto custa',
     '7.500 reais de entrada, pagos uma vez e parceláveis em até doze vezes, mais o pacote mensal '
     'escolhido, de 3.499 a 7.499 reais. O pacote recomendado é o Crescimento, de 4.999 por mês. A '
     'verba de anúncios é paga direto à plataforma e não passa pela Oráculo.'),
    ('Quando começa',
     'Reunião de escopo de 30 minutos, sem custo, antes do contrato. Onboarding completo em 7 dias '
     'a partir da assinatura. O primeiro ciclo é de 90 dias, com leitura de resultado todo mês.'),
    ('O que fica com o contratante',
     'Site, domínio, ficha do Google, conta de anúncios, número de WhatsApp e arquivos editáveis do '
     'sistema de design ficam no nome do Dr. Adriano Borges e continuam valendo se o contrato acabar.'),
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
], 'Valores em reais, acrescidos de imposto. A sustentação do site e da medição está dentro do '
   'pacote mensal, sem cobrança à parte. Sem a construção da base, o pacote não tem o que sustentar '
   'e o mensal cai 600 reais em qualquer um dos três níveis.',
   alinha={1: 'num', 2: 'num'}, compacta=True)}
{nota('Por que a base vem primeiro',
      'É a única parte com prazo externo. A contagem de reputação da ficha do Google só começa '
      'depois que existe uma ficha única, e leva de dois a três meses para firmar posição na busca '
      'da praça. É também a base que instala a medição sem a qual nada do pacote mensal pode ser '
      'conferido: hoje o site tem Google Analytics e Gerenciador de Tags no ar, mas nenhum evento '
      'de clique ou de conversa configurado, e nenhum pixel da Meta.')}
''', 'Duas decisões, dois números. <span class="azul">O resto do documento é a prova.</span>')

    # ---------------------------------------------------------------- 2. diagnostico
    d.pag('Diagnóstico', f'''
<h2 class="titulo">De onde saiu cada recomendação deste documento</h2>
<p class="lede">Nenhum item desta proposta foi escolhido em reunião de briefing. Todos saíram da
auditoria de 17 de agosto, que mediu quatro pilares: a busca no Google, o site, o Instagram e os
diretórios. A nota geral foi 4,3 de 10, e os quatro achados abaixo são os que definem o escopo. A
tabela liga cada um à parte da proposta que responde por ele.</p>
{tabela(['O que a auditoria apurou', 'O que isso significa', 'Onde entra'], [
    ('A cadência triplicou e o engajamento caiu junto. De setembro de 2025 a abril de 2026 foram '
     '31 publicações, de 1 a 7 por mês, com 0,659% de engajamento. De maio a agosto de 2026 foram '
     '55 publicações, de 14 a 19 por mês, com 0,415%. Nas 12 últimas, 0,174%',
     'Publicar mais deixou de trazer retorno. A audiência atual já está saturada, e o alcance '
     'adicional teria que vir de público novo, que hoje depende do acaso da distribuição.',
     '<b>Pacote</b>'),
    ('Três fichas do Perfil da Empresa no Google respondem pelo mesmo cirurgião. A principal tem '
     'nota 4,8 com 29 avaliações, mas está classificada como Médico. As outras duas têm a '
     'categoria correta de Cirurgião plástico e nenhuma avaliação',
     'Nenhuma das três reúne categoria certa e reputação, e por isso nenhuma aparece no bloco de '
     'mapas da busca por cirurgião plástico facelift em Brasília, onde os quatro nomes exibidos '
     'têm de 18 a 159 avaliações.', '<b>Base</b>'),
    ('O site é o primeiro resultado orgânico na busca pelo nome, mas tem 4 endereços reais '
     'publicados, nenhuma meta description, nenhuma marcação de Open Graph, nenhum dado '
     'estruturado de médico e o texto padrão de instalação do WordPress ainda no ar',
     'A busca pelo nome é vencida, e a busca por procedimento é perdida por falta de página que '
     'responda por ela. Cada procedimento anunciado precisa de um destino próprio para receber o '
     'clique.', '<b>Base</b>'),
    ('A bio do perfil aponta para um agregador de links gratuito que exibe cerca de 25 ofertas de '
     'afiliados alheias ao consultório, entre elas serviços de streaming e de assinatura, na mesma '
     'página do link de agendamento',
     'O caminho entre a publicação e a conversa passa por uma página que a Oráculo não controla e '
     'que anuncia outras marcas. O perfil também está com o botão de ação desativado, e o método '
     'de contato configurado é ligação.', '<b>Base e pacote</b>'),
], FONTE_AUDITORIA)}
{nota('O engajamento não é o problema',
      'Na janela comparável, o perfil registrou 0,503% de engajamento com 19.900 seguidores, à '
      'frente de @drtristaomauricio (96.714 seguidores, 0,358%) e de @drricardocintra (52.864 '
      'seguidores, 0,072%), atrás apenas de @dr.andrejardim (51.181 seguidores, 0,636%). O que '
      'separa o perfil dos concorrentes é alcance: a mediana de exibições dos reels é de 3.065, '
      'contra 16.316 do perfil que anuncia no Google. O conteúdo já converte quem chega. Falta '
      'fazer chegar mais gente.')}
''', 'A proposta não começou numa reunião. <span class="azul">Começou na leitura de 268 publicações e de três fichas do Google.</span>')

    # ---------------------------------------------------------------- 3. a base
    d.pag('A base', f'''
<h2 class="titulo">Decisão 1: a base, construída uma vez</h2>
<p class="lede">Esta é a parte paga uma única vez. Ela corrige os ativos que existem pela metade e
constrói os que ainda não existem. Tudo o que é construído aqui fica registrado no nome do Dr.
Adriano Borges e continua valendo se o contrato acabar.</p>
{tabela(['Obra', 'O que inclui', 'Valor'], [
    ('__grupo__', 'A base recomendada'),
    ('Site profissional',
     'Site novo no domínio dradrianoborges.com.br, preservando a posição orgânica já conquistada '
     'na busca pelo nome. De 5 a 7 páginas, com uma por procedimento principal, página do '
     'cirurgião com CRM e RQE visíveis e formulário ligado ao WhatsApp. Título, meta description, '
     'Open Graph e dados estruturados de médico configurados, itens hoje ausentes em todas as '
     'páginas. Retirada do conteúdo padrão de instalação do WordPress. Entrega em 4 a 6 semanas.',
     '3.500'),
    ('Perfil da Empresa no Google',
     'Consolidação das três fichas hoje ativas numa só, preservando as 29 avaliações da principal '
     'e corrigindo a categoria de Médico para Cirurgião plástico. Fotos, horários, área de '
     'atendimento, serviços listados e cadastro nos diretórios que aparecem na busca da praça. '
     'Retomada da rotina de avaliação na Doctoralia, parada desde 30 de novembro de 2021.',
     '2.000'),
    ('Medição de ponta a ponta',
     'Eventos de clique e de conversa no site, que hoje tem Google Analytics e Gerenciador de Tags '
     'instalados sem nenhum evento configurado. Search Console verificado e painel único ligando '
     'busca, site, perfil e WhatsApp. É o que permite conferir tudo o que o pacote mensal entrega.',
     '1.400'),
    ('Estrutura de anúncios',
     'Gerenciador de Negócios aberto e verificado, pixel da Meta e API de conversões instalados, '
     'nenhum dos dois presente hoje. Públicos por procedimento e por região de Brasília e a '
     'primeira estrutura de campanhas montada.', '1.400'),
    ('__total__', 'Soma dos quatro itens', '', '8.300'),
    ('__total__', 'Contratados juntos', '', '<b>7.500</b>'),
    ('__grupo__', 'Itens da mesma etapa, contratáveis quando fizer sentido'),
    ('Atendimento no WhatsApp',
     'Conta oficial liberada, comprovação junto à Meta, primeira resposta automática, triagem por '
     'procedimento e transferência para a secretária com a ficha preenchida. Substitui a ligação '
     'como método de contato principal do perfil.', '3.200'),
    ('Padronização de endereço e telefones',
     'Uma só grafia de endereço e um telefone público, aplicados no site, no Google, no Instagram e '
     'nos diretórios. Hoje as três fichas do Google trazem três endereços e dois telefones '
     'diferentes.', '900'),
], 'Valores em reais, acrescidos de imposto, parceláveis em até doze vezes. A manutenção do que é '
   'construído aqui já está dentro do pacote mensal, sem cobrança separada. A situação atual de cada '
   'item foi verificada na auditoria de 17/08/2026.')}
''', 'O que for construído fica no nome do médico <span class="azul">e continua valendo se o contrato acabar.</span>')

    # ---------------------------------------------------------------- 4. os pacotes
    d.pag('Os três pacotes', planos_com_escopo(
        'Decisão 2: o pacote que conduz a operação',
        'Um pacote só, com conteúdo, anúncio e sustentação da base no mesmo contrato e no mesmo '
        'valor. O que separa um nível do outro é o volume publicado, o alcance pago e a '
        'profundidade do acompanhamento. Vale notar o volume: o pacote recomendado prevê 12 '
        'publicações de feed por mês, menos do que as 14 a 19 publicadas hoje, e foi justamente na '
        'fase de maior volume que o engajamento caiu para 0,174%. A proposta é publicar menos e '
        'colocar verba por trás de cada peça, para que o alcance deixe de depender de quem já segue '
        'o perfil.',
        ('3.499', '4.999', '7.499'),
        [('Conteúdo publicado por mês', [
            ('Publicações de feed', '6', '12', '18'),
            ('Stories', '10', '20', '30'),
            ('Reels editados', '2', '4', '8'),
          ]),
         ('Anúncios', [
            ('Meta Ads, no Instagram e no Facebook', 'sim', 'sim', 'sim'),
            ('Google Ads, na busca por procedimento', 'nao', 'sim', 'sim'),
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
        'A página anterior traz o que decide a escolha. Esta abre o restante do escopo. Nenhuma '
        'entrega deste documento existe fora desta tabela.',
        [('Feito no primeiro mês, sem custo separado', [
            ('Organização do perfil, nova bio, botão de ação e página própria de links no domínio',
             'sim', 'sim', 'sim'),
            ('Destaques reorganizados por procedimento e por etapa da decisão', 'sim', 'sim', 'sim'),
            ('Linhas editoriais e grade do mês', 'sim', 'sim', 'sim'),
            ('Sistema de design próprio do perfil', 'nao', 'sim', 'sim'),
            ('Arquivos editáveis entregues', 'nao', 'sim', 'sim'),
          ]),
         ('Rotina de produção', [
            ('Roteiro, edição, legenda e capa', 'sim', 'sim', 'sim'),
            ('Grade do mês proposta até o dia 25', 'sim', 'sim', 'sim'),
            ('Conferência de cada peça com a Resolução CFM nº 2.336/2023', 'sim', 'sim', 'sim'),
            ('Resposta a comentário e a mensagem', 'nao', 'sim', 'sim'),
          ]),
         ('Campanhas', [
            ('Públicos por procedimento e por região de Brasília', 'nao', 'sim', 'sim'),
            ('Otimização e ajuste', 'semanal', '2 vezes por semana', 'contínua'),
            ('Teste de público e de página de destino', 'nao', 'nao', 'sim'),
            ('Relatório de aplicação da verba', 'sim', 'sim', 'sim'),
          ]),
         ('Sustentação da base, quando ela for contratada', [
            ('Atualização, cópia de segurança e disponibilidade do site', 'sim', 'sim', 'sim'),
            ('Manutenção da ficha do Google, da medição e das avaliações', 'sim', 'sim', 'sim'),
          ])],
        'Story é contado por tela, e publicação de feed é um post no perfil, imagem única, carrossel '
        'ou reel, com quantas telas o assunto pedir. Reel editado é montado a partir do material '
        'gravado no consultório. Nenhum dos três pacotes inclui fotógrafo ou cinegrafista. Na fase '
        'atual do perfil o reel rende 0,619% de engajamento contra 0,256% do carrossel, e a grade '
        'proposta respeita essa diferença.'),
        'Uma tabela só, três colunas. <span class="azul">Nada é prometido fora dela.</span>')

    # ---------------------------------------------------------------- 6. publicidade medica
    bpd.pagina_cfm(d)

    # ---------------------------------------------------------------- 7. ciclo de 90 dias
    d.pag('Primeiros 90 dias', f'''
<h2 class="titulo">O que acontece nos primeiros 90 dias</h2>
<p class="lede">Este é o único cronograma do documento, e cada linha diz a partir de qual pacote ela
entra. Quem contrata o Essencial recebe exatamente o que está marcado como Essencial, e nada além
disso é prometido aqui.</p>
{defs([
    ('Primeiros 7 dias, onboarding',
     'Acessos recebidos, contrato assinado, reunião de abertura com a equipe do consultório e '
     'primeira grade editorial aprovada. Reivindicação das três fichas do Google iniciada no mesmo '
     'prazo, porque a consolidação depende de prazo de verificação do próprio Google. Entra em '
     'qualquer pacote.'),
    ('Mês 1, fundação',
     'Perfil organizado, bio reescrita, botão de ação ativado e destaques reordenados por '
     'procedimento. A bio passa a apontar para uma página de links no próprio domínio, encerrando '
     'a exposição das ofertas de afiliados do agregador gratuito. Medição instalada. O sistema de '
     'design próprio e a entrega dos arquivos editáveis entram a partir do pacote <b>Crescimento</b>.'),
    ('Mês 2, alcance',
     'Grade editorial em ritmo pleno, primeira leva de criativos no ar e campanhas de alcance '
     'ativadas, com prioridade para reel, o formato de melhor desempenho na fase atual. Anúncio de '
     'busca no Google e públicos segmentados por procedimento entram a partir do pacote '
     '<b>Crescimento</b>.'),
    ('Mês 3, conversão',
     'Caminho rastreável entre a publicação e a conversa no WhatsApp, roteiro de atendimento por '
     'tipo de procedimento e primeiro relatório ligando peça publicada, clique e conversa aberta. '
     'O relatório de origem das conversas entra a partir do pacote <b>Crescimento</b>.'),
    ('Depois dos 90 dias, escala',
     'Ampliação dos formatos e dos públicos que provaram resultado, teste de página de destino por '
     'procedimento e base própria de pacientes para retorno e indicação. O teste de página de '
     'destino entra no pacote <b>Autoridade</b>.'),
])}
{nota('O que não é prometido neste documento',
      'Todas as metas do primeiro ciclo são de alcance, de qualificação de contato e de estrutura '
      'instalada. A Oráculo não promete número de cirurgias nem faturamento, porque o fechamento '
      'depende da consulta e da operação do consultório. Além disso, prometer resultado em '
      'publicidade médica é vedado pela Resolução CFM nº 2.336/2023. O que é medido e cobrado é o '
      'que está na tabela de escopo.')}
''', 'Um cronograma só, com o pacote marcado em cada linha. <span class="azul">Sem promessa fora do que foi contratado.</span>')

    # ---------------------------------------------------------------- 8. como funciona
    d.pag('Como funciona', f'''
<h2 class="titulo">Como o trabalho acontece no dia a dia</h2>
<p class="lede">A parte que mais atrasa um contrato de marketing não é a produção, é a aprovação. Em
consultório médico isso pesa ainda mais, porque cada peça depende de agenda cirúrgica e de
autorização de uso de imagem. Por isso o que cabe a cada lado está escrito aqui, antes da
assinatura.</p>
{duas_colunas(
    'O que a Oráculo faz',
    ['Propõe a grade editorial do mês até o dia 25 do mês anterior, com tema, formato e objetivo '
     'de cada peça.',
     'Produz roteiro, arte, edição, legenda e capa a partir do material bruto e das informações do '
     'consultório.',
     'Confere cada peça com a Resolução CFM nº 2.336/2023 antes de publicar, com registro do que '
     'foi ajustado.',
     'Gere as campanhas, acompanha a verba diariamente e ajusta público, criativo e orçamento.',
     'Entrega um relatório único de conteúdo e de campanha até o dia 10, e conduz a reunião de '
     'leitura nos pacotes que a incluem.'],
    'O que esperamos do contratante',
    ['Um ponto focal único para aprovar a grade e responder dúvidas, com resposta em até 3 dias '
     'úteis.',
     'Envio do material bruto combinado: gravações de consultório e de centro cirúrgico, casos '
     'novos e datas importantes do mês.',
     'Autorização de uso de imagem assinada por paciente, obrigatória para qualquer peça com antes '
     'e depois.',
     'Acesso às contas de Instagram, Facebook, Google e ao domínio dradrianoborges.com.br, no nome '
     'do próprio médico.',
     'Atendimento das conversas geradas dentro do horário comercial, que é onde a campanha vira '
     'consulta marcada.'])}
{nota('Aprovação por silêncio',
      'A grade editorial enviada e não respondida em 3 dias úteis é considerada aprovada, com '
      'exceção de qualquer peça que envolva imagem de paciente, que nunca é publicada sem '
      'aprovação expressa. A regra existe para proteger o calendário: publicação atrasada por falta '
      'de resposta custa alcance, e o algoritmo não devolve o que se perdeu no intervalo.')}
''', 'Nenhum contrato de marketing funciona sem contrapartida. <span class="azul">A daqui cabe em cinco linhas.</span>')

    # ---------------------------------------------------------------- 9. condicoes
    d.pag('Condições', f'''
<h2 class="titulo">Condições comerciais e custos que não passam pela Oráculo</h2>
<p class="lede">Esta página existe para que nenhuma pergunta de contrato precise ser feita por
mensagem depois. Tudo o que é cobrado, por quem e quando está aqui.</p>
<h3 class="sub">Condições comerciais</h3>
<p class="texto">{CONDICOES}</p>
<h3 class="sub">Pago diretamente ao fornecedor</h3>
{tabela(['Item', 'Quanto', 'Quando se aplica'], [
    ('Verba de anúncios, paga à plataforma', '800 a 6.000 por mês',
     'Em qualquer pacote, conforme o nível'),
    ('Sistema de atendimento no WhatsApp', 'cerca de 500 por mês',
     'Se o atendimento for contratado'),
    ('Hospedagem e e-mail no domínio próprio', 'cerca de 150 por mês',
     'A partir da entrega do site'),
    ('Renovação do domínio no Registro.br', 'cerca de 40 por ano',
     'O domínio dradrianoborges.com.br já está registrado'),
], 'Valores em reais. Faixas conforme as tabelas públicas dos fornecedores, consultadas em '
   '30/08/2026. Nenhum destes itens passa pela Oráculo, e todos ficam registrados no nome do '
   'contratante.', compacta=True)}
{nota('O que o pacote mensal não cobre',
      'Captação profissional de foto e de vídeo, produção de página nova fora do escopo do site, '
      'locução profissional e licença de banco de imagens são orçados à parte quando houver '
      'necessidade. A Oráculo indica e coordena o fornecedor, e o serviço é pago diretamente a ele.')}
''', 'Preço fechado, contrapartida escrita <span class="azul">e nenhuma linha em aberto.</span>')

    # ---------------------------------------------------------------- contracapa
    d.contracapa(
        'O próximo passo é uma reunião de 30 minutos',
        'A reunião serve para ajustar o escopo ao caso concreto, confirmar prioridades e definir a '
        'data de início. Não há custo e não há compromisso de contratação.',
        [('Reunião', '30 minutos, presencial em Brasília ou por vídeo'),
         ('Onboarding', '7 dias a partir da assinatura'),
         ('A base', '7.500 reais, pagos uma vez, parceláveis em até 12 vezes de 625'),
         ('O pacote', '4.999 reais por mês no Crescimento, de 3.499 a 7.499 conforme o nível')],
        'Baseado na auditoria de presença digital<br>entregue em 17 de agosto de 2026')

    return d.salvar(
        os.path.join(RAIZ, 'DrAdrianoBorges', 'Proposta-Comercial.html'),
        'Proposta Comercial, Dr. Adriano Borges, Oráculo Tecnologia',
        'Proposta comercial da Oráculo Tecnologia para o Dr. Adriano Borges, cirurgião plástico em '
        'Brasília: a base construída uma vez e a operação mensal em três pacotes, a partir da '
        'auditoria de presença digital de 17 de agosto de 2026.')


if __name__ == '__main__':
    print('gerando proposta do Dr. Adriano Borges...')
    erros = bp.validar('DrAdrianoBorges', build_adriano())
    print('RESULTADO:', 'tudo ok' if not erros else erros)
