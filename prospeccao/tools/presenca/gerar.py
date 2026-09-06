#!/usr/bin/env python3
"""Compõe o HTML de presença digital de cada clínica a partir do presenca.json."""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from redigir import notas, veredito, kpis, n, pct
import build_presenca as B

R = pathlib.Path("prospeccao/odonto-DF/analises")
VERT = {"tecnologia":"Tecnologia","social":"Redes sociais","trafego":"Tráfego pago"}


def manchete(d, ger, ver):
    c, ig, t = d["clinica"], d["instagram"], d["tecnologia"]
    nome = c["nome"]
    if t.get("site") and t.get("httpStatus") != 200:
        return (f"O domínio da {nome} não abre para ninguém. "
                f"<em>E o Google continua mandando paciente para lá.</em>")
    if not ig.get("handle") and t.get("httpStatus") != 200:
        return (f"{c['idadeAnos']} anos de operação e nenhum canal próprio na internet. "
                f"<em>Quem procura a clínica encontra o que terceiros decidiram publicar.</em>")
    if (ig.get("hiatoDias") or 0) > 40:
        return (f"A conta parou há {ig['hiatoDias']} dias, com {n(ig.get('seguidores'))} seguidores esperando. "
                f"<em>O alcance que some não volta sozinho.</em>")
    if ig.get("ctaPctFaseAtual") is not None and ig["ctaPctFaseAtual"] < 5:
        return (f"{n(ig.get('seguidores'))} seguidores e {pct(ig.get('ctaPctFaseAtual'))} dos posts pedem alguma ação. "
                f"<em>A audiência existe; o caminho até a cadeira, não.</em>")
    if not ig.get("handle"):
        return (f"O site está no ar e a vitrine social não existe. "
                f"<em>Em odontologia estética, ninguém fecha sem ver caso tratado.</em>")
    er = ig.get("er90d")
    if er is not None and er < 0.5:
        return (f"{n(ig.get('seguidores'))} seguidores e {pct(er)} de engajamento. "
                f"<em>A base foi construída e hoje quase ninguém vê o que é publicado.</em>")
    if er is not None and er < 1.0:
        return (f"{n(ig.get('seguidores'))} seguidores, {pct(er)} de engajamento. "
                f"<em>O canal respira, mas está abaixo do que a audiência comportaria.</em>")
    return (f"{n(ig.get('seguidores'))} seguidores, {pct(er)} de engajamento. "
            f"<em>O canal funciona; falta transformar atenção em agendamento.</em>")


def charts(d, pil, ger):
    ig, g = d["instagram"], d["google"]
    mix = (ig.get("faseAtual") or {}).get("mixFormatos") or {}
    cad = ig.get("cadenciaMensal") or {}
    conc = d.get("concorrentes") or []
    j = json.dumps
    s = ["const ink='#1b2e73',primary='#1d4ed8',soft='#b3c0ea',rule='#dfe1ec',good='#15803d',purple='#6d28d9';",
         "Chart.defaults.font.family=\"'Bricolage Grotesque',system-ui,sans-serif\";",
         "Chart.defaults.color='#6b7186';Chart.defaults.plugins.legend.labels.usePointStyle=true;",
         "Chart.defaults.plugins.legend.labels.boxWidth=7;const grid={color:'#ebedf4'};",
         "const mk=(id,cfg)=>{const el=document.getElementById(id);if(el)new Chart(el,cfg);};"]
    if ger is not None:
        s.append(f"mk('chartScore',{{type:'doughnut',data:{{datasets:[{{data:[{ger},{round(10-ger,1)}],"
                 f"backgroundColor:[primary,'#ebedf4'],borderWidth:0}}]}},options:{{cutout:'72%',"
                 f"plugins:{{legend:{{display:false}}}}}}}});")
    if mix:
        s.append(f"mk('chartFormatos',{{type:'doughnut',data:{{labels:{j(list(mix.keys()))},"
                 f"datasets:[{{data:{j(list(mix.values()))},backgroundColor:[primary,soft,purple],borderWidth:0}}]}},"
                 f"options:{{cutout:'58%'}}}});")
    if cad:
        s.append(f"mk('chartCadencia',{{type:'bar',data:{{labels:{j(list(cad.keys()))},"
                 f"datasets:[{{label:'Posts no mês',data:{j(list(cad.values()))},backgroundColor:primary}}]}},"
                 f"options:{{scales:{{y:{{grid}},x:{{grid:{{display:false}}}}}},plugins:{{legend:{{display:false}}}}}}}});")
    if conc:
        s.append(f"mk('chartConcorrentes',{{type:'bar',data:{{labels:{j([c['nome'][:22] for c in conc])},"
                 f"datasets:[{{label:'Avaliações no Google',data:{j([c.get('avaliacoes') or 0 for c in conc])},"
                 f"backgroundColor:soft}}]}},options:{{indexAxis:'y',scales:{{x:{{grid}}}},plugins:{{legend:{{display:false}}}}}}}});")
    pl = {k: v for k, v in pil.items() if v is not None}
    if pl:
        s.append(f"mk('chartRadar',{{type:'radar',data:{{labels:{j([B.PILAR_ROT[k] for k in pl])},"
                 f"datasets:[{{label:'Nota',data:{j(list(pl.values()))},borderColor:primary,"
                 f"backgroundColor:'rgba(29,78,216,.12)'}}]}},options:{{scales:{{r:{{min:0,max:10}}}}}}}});")
    return "\n".join(s)


def secoes(d, pil, ger, ver):
    c, ig, t, g, ads = d["clinica"], d["instagram"], d["tecnologia"], d["google"], d["ads"]
    dores = d.get("dores") or []
    dv = lambda v: [x for x in dores if x.get("vertente") == v]
    li = lambda xs: "<ul>" + "".join(f"<li>{x}</li>" for x in xs) + "</ul>"
    S = {}

    trava = ver[0]
    S["essencial"] = {"h2":"O essencial em dois minutos",
      "sub":"O que a presença atual comunica, onde ela perde força e qual movimento muda o cenário.",
      "corpo": f'<div class="essential"><div class="essential-main"><p class="eyebrow">Leitura central</p>'
               f'<p class="lede">{ver[1]}</p></div><div class="card"><p class="eyebrow">Decisão prioritária</p>'
               f'<p>{(dores[0]["titulo"] + ": " + dores[0]["evidencia"]) if dores else "Fechar a coleta dos pilares pendentes."}</p></div></div>'
               f'<div class="grid-3" style="margin-top:1rem">'
               + B.card("O que funciona", _forte(d), _forte_txt(d))
               + B.card("O que trava", trava, ver[1])
               + B.card("O que destrava", _destrava(d)[0], _destrava(d)[1]) + "</div>",
      "insight_classe":"warn", "insight": ver[1]}

    S["diagnostico"] = {"h2":"Diagnóstico executivo", "sub":"Nota por pilar, com a origem de cada número declarada.",
      "corpo": B.score_block({"valor":ger,"pilares":pil,"veredito":ver[0],"explicacao":ver[1]})
               + B.diag_cols([x["evidencia"] for x in dores[:3]] or ["Coleta parcial"],
                             [x.get("custo","") for x in dores[:3]] or ["—"],
                             [_resposta(x) for x in dores[:3]] or ["—"]),
      "insight_classe":"bad" if (ger or 10) < 5 else "warn",
      "insight": f"A nota de {n(ger,1)} não é um juízo de valor sobre a clínica, é a distância entre o que ela já é e o que a internet mostra dela."}

    S["google"] = {"h2":"Google: busca e Perfil da Empresa", "sub":"Onde o paciente começa a procurar.",
      "corpo": _bloco_google(g),
      "insight_classe":"warn" if g.get("perfilEncontrado") else "bad",
      "insight": _insight_google(g)}

    S["site"] = {"h2":"Site, SEO e tecnologia", "sub":"A única página que a clínica controla por inteiro.",
      "corpo": _bloco_site(t) + (li([f"<b>{x['titulo']}</b> — {x['evidencia']}" for x in dv("tecnologia")]) if dv("tecnologia") else ""),
      "insight_classe":"bad" if t.get("httpStatus") != 200 else "warn",
      "insight": _insight_site(t)}

    S["instagram"] = {"h2":"Instagram: alcance, cadência e conversão", "sub":"O canal onde odontologia estética é decidida.",
      "corpo": _bloco_ig(ig),
      "insight_classe":"bad" if (ig.get("hiatoDias") or 0) > 40 else ("good" if (ig.get("er90d") or 0) >= 1 else "warn"),
      "insight": _insight_ig(ig)}

    S["ads"] = {"h2":"Anúncios: o que está no ar hoje", "sub":"Meta Ad Library e rastros de pixel no site.",
      "corpo": _bloco_ads(ads, t),
      "insight_classe":"info", "insight": _insight_ads(ads, t)}

    S["conteudo"] = {"h2":"Formato, tema e cadência", "sub":"O que é publicado, e o que isso devolve.",
      "corpo": _bloco_conteudo(ig), "insight_classe":"warn", "insight": _insight_conteudo(ig)}

    S["diretorios"] = {"h2":"Diretórios e redes secundárias", "sub":"Onde a clínica aparece sem controlar a narrativa.",
      "corpo": _bloco_dir(d.get("diretorios") or {}), "insight_classe":"info",
      "insight":"Diretório traz paciente, mas cobra pedágio e não constrói ativo. Serve como complemento, nunca como base."}

    S["concorrencia"] = {"h2":"Comparativo na mesma praça", "sub":"Quem disputa a mesma busca.",
      "corpo": _bloco_conc(d.get("concorrentes") or []), "insight_classe":"warn",
      "insight": _insight_conc(d.get("concorrentes") or [], g)}

    S["conversao"] = {"h2":"O caminho entre o interesse e a cadeira", "sub":"Onde a jornada quebra.",
      "corpo": _bloco_conv(t, ig), "insight_classe":"warn", "insight": _insight_conv(t, ig)}

    S["swot"] = {"h2":"Análise SWOT", "sub":"Leitura consolidada dos quatro pilares.",
      "corpo": _bloco_swot(d, pil, ver), "insight_classe":"purple",
      "insight":"Nenhuma das fraquezas listadas exige recomeçar. Todas exigem organizar o que já existe."}

    S["recomendacoes"] = {"h2":"Plano estratégico de 180 dias", "sub":"Ordem importa: tecnologia, depois conteúdo, e só então anúncio.",
      "corpo": _bloco_plano(d, dores), "insight_classe":"good",
      "insight":"A sequência não é arbitrária. Anunciar antes de ter para onde mandar o clique é pagar para perder paciente mais rápido."}

    S["resumo"] = {"h2":"Resumo executivo e pontuação", "sub":"O que fica desta primeira leitura.",
      "corpo": f'<div class="grid-2"><div><p class="lede">{ver[1]}</p><p>{_resumo_txt(d, ger)}</p></div>'
               f'<div class="chart sm"><canvas id="chartScore"></canvas></div></div>'
               f'<div class="grid-3" style="margin-top:1rem">'
               + B.card("Herdar", _forte(d), _forte_txt(d))
               + B.card("Construir", _destrava(d)[0], _destrava(d)[1])
               + B.card("Escalar", "Tráfego pago com medição", "Só depois que site e conteúdo estiverem de pé, o anúncio multiplica em vez de vazar.")
               + '</div><div class="chart sm" style="margin-top:1rem"><canvas id="chartRadar"></canvas></div>',
      "insight_classe":"purple", "insight": f"Nota geral de {n(ger,1)} em 10. {ver[1]}"}
    return S


# ---- blocos auxiliares -------------------------------------------------
def _forte(d):
    ig, t, c = d["instagram"], d["tecnologia"], d["clinica"]
    if (ig.get("er90d") or 0) >= 1: return "Engajamento acima da média do setor"
    if t.get("httpStatus") == 200 and t.get("agendamentoOnline"): return "Site com caminho de agendamento"
    if (ig.get("seguidores") or 0) > 8000: return "Audiência já construída"
    if c.get("idadeAnos", 0) >= 15: return f"{c['idadeAnos']} anos de reputação local"
    return "Capacidade instalada"

def _forte_txt(d):
    ig, c = d["instagram"], d["clinica"]
    if (ig.get("seguidores") or 0) > 8000:
        return f"{n(ig['seguidores'])} pessoas já escolheram acompanhar a clínica. Esse ativo não precisa ser comprado de novo."
    return f"{c['idadeAnos']} anos de operação em {c['regiao']} constroem uma base de indicação que o digital pode amplificar, não substituir."

def _destrava(d):
    ig, t = d["instagram"], d["tecnologia"]
    if t.get("site") and t.get("httpStatus") != 200:
        return ("Colocar o domínio de pé", "Antes de qualquer conteúdo: um site que não abre transforma toda divulgação em desperdício.")
    if not t.get("site"): return ("Um site próprio", "Página no domínio da clínica, com agendamento e prova de casos — o único ativo que fica.")
    if (ig.get("hiatoDias") or 0) > 40: return ("Retomar a publicação", "Cadência regular recupera entrega em semanas, não em meses.")
    if (ig.get("ctaPctFaseAtual") or 100) < 5: return ("Pedir a consulta", "Chamada para ação em cada post e atendente de IA no WhatsApp para responder na hora.")
    return ("Medição de origem", "Sem saber de onde vem paciente, não há como decidir onde investir.")

def _resposta(dor):
    return {"tecnologia":"Corrigir na vertente de tecnologia","social":"Reestruturar a gestão de conteúdo",
            "trafego":"Ativar tráfego pago com medição"}.get(dor.get("vertente"), "Tratar no plano de 180 dias")

def _bloco_google(g):
    if g.get("perfilEncontrado") is None:
        return B.callout("Limite da medição", "O Perfil da Empresa não foi coletado nesta rodada. Sem chave da Places API, a leitura depende da tela de busca e ficou pendente.")
    if g.get("perfilEncontrado") is False:
        return B.callout("Sem perfil localizado", "Nenhum Perfil da Empresa foi encontrado para a clínica. Na prática, ela não existe no mapa nem no pacote local — que é onde a busca por dentista começa.")
    linhas = [["Nota", n(g.get("nota"),1)], ["Avaliações", n(g.get("avaliacoes"))],
              ["Categoria", g.get("categoria") or "—"], ["Site vinculado", g.get("siteVinculado") or "—"]]
    extra = ""
    if g.get("fichasDuplicadas"):
        extra = B.callout("Fichas duplicadas", f"Foram encontradas {len(g['fichasDuplicadas'])} fichas para a mesma clínica. O Google divide avaliações e autoridade entre elas, e nenhuma acumula reputação suficiente.")
    return B.tabela(["Item","Observado"], linhas) + extra

def _insight_google(g):
    if g.get("perfilEncontrado") is None: return "Pilar pendente de coleta. Nenhuma conclusão sobre o Google deve ser tirada deste relatório ainda."
    if g.get("perfilEncontrado") is False: return "Não aparecer no Google não é detalhe: é a diferença entre ser considerado e nem entrar na lista."
    av = g.get("avaliacoes") or 0
    if av < 20: return f"{av} avaliações é pouco para o porte da clínica. Volume de avaliação é o que decide posição no pacote local."
    return "O perfil existe e tem tração. O trabalho é de manutenção e resposta, não de construção."

def _bloco_site(t):
    if t.get("site") and t.get("httpStatus") != 200:
        return B.callout("Site fora do ar", f"O endereço {t['site']} não respondeu. {t.get('erroColeta','')}. Verificado em mais de um cliente HTTP.")
    if not t.get("site"):
        return B.callout("Sem site próprio", "Nenhuma página no domínio da clínica foi localizada. Toda a presença depende de perfis e diretórios de terceiros.")
    sim = lambda b: "sim" if b else "não"
    return B.tabela(["Item","Observado"], [
        ["Endereço", t.get("site")], ["Stack", t.get("cms") or "não identificada"],
        ["HTTPS", sim(t.get("https"))], ["Adaptado a celular", sim(t.get("viewportMobile"))],
        ["Tempo de resposta", n(t.get("ttfbSegundos"),2,"s")],
        ["Meta description", sim(t.get("metaDescription"))],
        ["Schema de negócio local", sim(t.get("jsonLdLocalBusiness"))],
        ["Agendamento na página", sim(t.get("agendamentoOnline"))],
        ["WhatsApp na página", sim(t.get("whatsappNoSite"))],
        ["Analytics instalado", sim(t.get("gtm") or t.get("ga4"))]])

def _insight_site(t):
    if t.get("site") and t.get("httpStatus") != 200:
        return "Um domínio que não abre é pior que domínio nenhum: o Google continua indexando o endereço e mandando gente para uma porta fechada."
    if not t.get("site"):
        return "Sem site, a clínica aluga toda a sua presença. Quando a plataforma muda a regra, ela perde o canal e não leva nada consigo."
    faltas = []
    if not t.get("jsonLdLocalBusiness"): faltas.append("schema de negócio local")
    if not (t.get("gtm") or t.get("ga4")): faltas.append("qualquer medição")
    if not t.get("https"): faltas.append("HTTPS")
    if faltas: return "O site existe e carrega, mas está sem " + ", sem ".join(faltas) + ". São correções de dias, não de meses."
    return "O site cobre o básico. O ganho agora vem de conteúdo por procedimento e prova de casos."

def _bloco_ig(ig):
    if not ig.get("handle"):
        return B.callout("Sem perfil localizado", "Nenhuma conta no Instagram foi encontrada para a clínica.")
    return B.tabela(["Métrica","Medido"], [
        ["Perfil", "@" + ig["handle"]], ["Seguidores", n(ig.get("seguidores"))],
        ["Publicações no histórico", n(ig.get("publicacoesTotal"))],
        ["Amostra lida", n(ig.get("amostraColetada")) + " posts"],
        ["Dias desde a última publicação", n(ig.get("hiatoDias"))],
        ["Engajamento na amostra", pct(ig.get("erAmostra"))],
        ["Engajamento nos últimos 90 dias", pct(ig.get("er90d"))],
        ["Publicações nos últimos 90 dias", n(ig.get("postsUlt90d"))],
        ["Mediana de reproduções por Reel", n(ig.get("medianaPlaysReel"))],
        ["Posts com chamada para ação", pct(ig.get("ctaPctFaseAtual"))]]) + \
        '<div class="grid-2" style="margin-top:1rem"><div class="chart sm"><canvas id="chartCadencia"></canvas></div>' \
        '<div class="chart sm"><canvas id="chartFormatos"></canvas></div></div>'

def _insight_ig(ig):
    if not ig.get("handle"): return "Em odontologia estética, o paciente quer ver caso tratado antes de marcar. Sem perfil, essa prova não existe."
    h = ig.get("hiatoDias") or 0
    if h > 40: return f"São {h} dias sem publicar. O algoritmo reduz entrega de quem some, então retomar custa mais caro do que teria custado manter."
    er = ig.get("er90d")
    if er is not None and er < 0.5: return f"Engajamento de {pct(er)} significa que a maior parte dos seguidores não vê mais o que é publicado. Volume não resolve; formato e recorte, sim."
    cta = ig.get("ctaPctFaseAtual")
    if cta is not None and cta < 5: return f"Só {pct(cta)} dos posts pedem alguma ação. A conta informa bem e vende pouco, e isso é ajuste de roteiro, não de investimento."
    return "O canal está saudável. O próximo ganho vem de transformar alcance em agendamento medido."

def _bloco_ads(ads, t):
    al = ads.get("metaAdLibrary") or {}
    if not al.get("conseguiuLer"):
        return B.callout("Limite da medição", "A Meta Ad Library não pôde ser lida nesta coleta. O que segue vale apenas para os rastros de pixel encontrados no site.") + _tab_pixel(t)
    ativos = al.get("anunciosAtivos")
    txt = (f"Nenhum anúncio ativo encontrado na biblioteca pública da Meta."
           if not ativos else f"{ativos} anúncio(s) ativo(s), {al.get('criativos') or '—'} criativo(s).")
    return f"<p>{txt}</p>" + _tab_pixel(t)

def _tab_pixel(t):
    sim = lambda b: "sim" if b else "não"
    return B.tabela(["Rastro no site","Presente"], [
        ["Pixel da Meta", sim(t.get("pixelMeta"))], ["Google Ads", sim(t.get("pixelGoogleAds"))],
        ["Google Tag Manager", sim(t.get("gtm"))], ["GA4", sim(t.get("ga4"))]])

def _insight_ads(ads, t):
    tem_pixel = t.get("pixelMeta") or t.get("pixelGoogleAds")
    tem_med = t.get("gtm") or t.get("ga4")
    if not tem_pixel and not tem_med:
        return "Sem pixel e sem analytics, não há como saber de onde vem paciente. Investir em anúncio nessa condição é apostar, não comprar."
    if tem_pixel and not tem_med:
        return "Há pixel de anúncio mas não há medição própria. Dá para anunciar, não dá para provar retorno."
    return "A base de medição existe. Falta ligá-la a campanhas com intenção de busca."

def _bloco_conteudo(ig):
    fa = ig.get("faseAtual") or {}
    mix = fa.get("mixFormatos") or {}
    if not mix: return B.callout("Limite da medição", "Mix de formatos não coletado.")
    tot = sum(mix.values()) or 1
    linhas = [[k.capitalize(), f"{v} posts", f"{v/tot*100:.0f}%".replace(".", ",")] for k, v in
              sorted(mix.items(), key=lambda x: -x[1])]
    return B.tabela(["Formato","Volume","Participação"], linhas)

def _insight_conteudo(ig):
    fa = ig.get("faseAtual") or {}
    mix = fa.get("mixFormatos") or {}
    if not mix: return "Sem amostra de formatos, nenhuma recomendação de mix se sustenta."
    dom = max(mix, key=mix.get); tot = sum(mix.values()) or 1
    if dom == "imagem" and mix[dom]/tot > 0.5:
        return f"Imagem estática é {mix[dom]/tot*100:.0f}% do que se publica e é o formato que menos entrega. Inverter o mix é a mudança de maior efeito e menor custo.".replace(".0%","%")
    return "O mix já privilegia formato de alcance. O ganho agora está no roteiro e na chamada final."

def _bloco_dir(dirs):
    achados = [(k, v) for k, v in dirs.items() if v and k not in ("outros",)]
    if not achados: return B.callout("Nenhum diretório localizado", "A clínica não foi encontrada nos diretórios consultados.")
    return B.tabela(["Canal","Endereço"], [[k.capitalize(), str(v)[:90]] for k, v in achados])

def _bloco_conc(conc):
    if not conc: return B.callout("Limite da medição", "O comparativo com concorrentes não foi coletado nesta rodada.")
    return B.tabela(["Concorrente","Nota","Avaliações","Região"],
                    [[c.get("nome",""), n(c.get("nota"),1), n(c.get("avaliacoes")), c.get("local","")] for c in conc]) + \
           '<div class="chart sm" style="margin-top:1rem"><canvas id="chartConcorrentes"></canvas></div>'

def _insight_conc(conc, g):
    if not conc: return "Sem benchmark, o número isolado da clínica não diz se ela está à frente ou atrás na disputa local."
    av = [c.get("avaliacoes") or 0 for c in conc]
    if g.get("avaliacoes") and av and g["avaliacoes"] < max(av)/2:
        return f"O líder da praça tem {max(av)} avaliações contra {g['avaliacoes']} da clínica. Essa distância decide quem aparece primeiro no mapa."
    return "A disputa local é decidida por volume de avaliação recente, não por tempo de casa."

def _bloco_conv(t, ig):
    sim = lambda b: "sim" if b else "não"
    return B.tabela(["Etapa da jornada","Existe hoje"], [
        ["Post pede alguma ação", pct(ig.get("ctaPctFaseAtual"))],
        ["Link na bio leva a página própria", sim(t.get("httpStatus") == 200)],
        ["WhatsApp acessível", sim(t.get("whatsappNoSite"))],
        ["Agendamento sem falar com atendente", sim(t.get("agendamentoOnline"))],
        ["Origem do contato é medida", sim(t.get("gtm") or t.get("ga4"))]])

def _insight_conv(t, ig):
    quebras = []
    if (ig.get("ctaPctFaseAtual") or 100) < 5: quebras.append("o post não pede")
    if t.get("httpStatus") != 200: quebras.append("não há página para onde mandar")
    if not t.get("agendamentoOnline"): quebras.append("marcar depende de alguém atender")
    if not (t.get("gtm") or t.get("ga4")): quebras.append("ninguém mede o que aconteceu")
    if quebras: return "A jornada quebra em mais de um ponto: " + ", ".join(quebras) + ". Cada um deles é barato de corrigir isoladamente."
    return "A jornada está fechada. O ganho agora é de volume, não de estrutura."

def _bloco_swot(d, pil, ver):
    ig, t, c = d["instagram"], d["tecnologia"], d["clinica"]
    forcas = [f"{c['idadeAnos']} anos de operação em {c['regiao']}", f"Porte {c['porte']}"]
    if (ig.get("seguidores") or 0) > 5000: forcas.append(f"{n(ig['seguidores'])} seguidores já conquistados")
    if t.get("httpStatus") == 200: forcas.append("Site próprio no ar")
    fraq = [x["titulo"] for x in (d.get("dores") or [])][:4] or ["Coleta parcial"]
    opor = ["Concorrentes locais com a mesma lacuna de schema e medição",
            "Ticket alto do nicho paga o investimento com poucos casos recuperados"]
    ameac = ["Clínicas novas que nascem com operação digital estruturada",
             "Dependência de indicação, que não escala e envelhece com a base"]
    col = lambda t_, xs: f'<div class="card"><p class="eyebrow">{t_}</p><ul>' + "".join(f"<li>{x}</li>" for x in xs) + "</ul></div>"
    return ('<div class="grid-2">' + col("Forças", forcas) + col("Fraquezas", fraq) + "</div>"
            '<div class="grid-2" style="margin-top:1rem">' + col("Oportunidades", opor) + col("Ameaças", ameac) + "</div>")

def _bloco_plano(d, dores):
    t, ig = d["tecnologia"], d["instagram"]
    f30 = []
    if t.get("site") and t.get("httpStatus") != 200: f30.append("Restabelecer o domínio e apontar o DNS")
    elif not t.get("site"): f30.append("Publicar site próprio no domínio da clínica")
    else:
        if not t.get("jsonLdLocalBusiness"): f30.append("Instalar schema de negócio local")
        if not (t.get("gtm") or t.get("ga4")): f30.append("Instalar GA4 e Tag Manager")
        if not t.get("https"): f30.append("Migrar para HTTPS")
    f30.append("Reivindicar e corrigir o Perfil da Empresa no Google")
    f90 = ["Atendente de IA no WhatsApp para qualificar e agendar 24 horas"]
    if ig.get("handle"):
        if (ig.get("hiatoDias") or 0) > 30: f90.append("Retomar cadência com calendário fixo")
        if (ig.get("ctaPctFaseAtual") or 100) < 10: f90.append("Chamada para ação em todo post de caso")
        f90.append("Inverter o mix para o formato de maior entrega")
    else:
        f90.append("Abrir e estruturar o perfil no Instagram com prova de casos")
    f180 = ["Google Ads na busca de alta intenção", "Meta Ads segmentado por região de captação",
            "Rotina mensal de solicitação de avaliação no Google"]
    col = lambda t_, xs: f'<div class="card"><p class="eyebrow">{t_}</p><ul>' + "".join(f"<li>{x}</li>" for x in xs) + "</ul></div>"
    return '<div class="grid-3">' + col("Primeiros 30 dias", f30) + col("Até 90 dias", f90) + col("Até 180 dias", f180) + "</div>"

def _resumo_txt(d, ger):
    c = d["clinica"]
    return (f"A {c['nome']} tem {c['idadeAnos']} anos de operação, porte {c['porte']} e "
            f"{'mais de uma unidade' if (c.get('unidades') or 1) > 1 else 'uma unidade'} em {c['regiao']}. "
            f"A capacidade instalada não é o problema — a distância entre ela e o que a internet mostra é.")


def gerar(pasta):
    fp = pasta / "data" / "presenca.json"
    d = json.loads(fp.read_text(encoding="utf-8"))
    pil, ger = notas(d); ver = veredito(ger, d)
    d["notaGeral"] = {"valor": ger, "escala": 10, "pilares": pil}
    fp.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")

    textos = {"manchete": manchete(d, ger, ver),
      "cover_sub": f"Auditoria dos quatro pilares que sustentam a captação de uma clínica odontológica em {d['clinica']['regiao']}: "
                   f"site e tecnologia, Instagram, anúncios e presença no Google. "
                   + (f"{n(d['instagram'].get('amostraColetada'))} publicações foram lidas uma a uma. "
                      if d['instagram'].get('amostraColetada') else "")
                   + "Cada número deste relatório declara de onde veio.",
      "cover_foot": f"{d['clinica']['porte']} · {d['clinica']['regiao']} · {d['clinica']['idadeAnos']} anos · CNPJ {d['cnpj']}",
      "meta_description": f"Auditoria de presença digital da {d['clinica']['nome']}: Google, site, Instagram e anúncios, com nota por pilar e plano de 180 dias.",
      "kpis": kpis(d), "secoes": secoes(d, pil, ger, ver),
      "fecho_titulo": _destrava(d)[0] + ". O resto já existe.",
      "fecho": ver[1] + " " + _resumo_txt(d, ger),
      "footer_fontes": "Fontes públicas coletadas em 18 e 19/08/2026 · " + "; ".join(d.get("fontes", [])[:3]),
      "charts": charts(d, pil, ger)}

    h = B.construir(d, textos)
    probs = B.validar(h, d["clinica"]["nome"])
    out = pasta / "Analise-Presenca-Digital.html"
    out.write_text(h, encoding="utf-8")
    return out, len(h), probs


if __name__ == "__main__":
    alvos = [pathlib.Path(sys.argv[1])] if len(sys.argv) > 1 else sorted(x for x in R.iterdir() if x.is_dir())
    for p in alvos:
        if not (p / "data" / "presenca.json").exists(): continue
        out, tam, probs = gerar(p)
        st = "OK" if not probs else "PROBLEMAS: " + "; ".join(probs)
        print(f"  {p.name[:44]:46} {tam/1024:6.1f} KB  {st}")
