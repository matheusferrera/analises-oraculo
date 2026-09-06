#!/usr/bin/env python3
"""
Transforma presenca.json na redação das 13 seções.

Não é preenchimento de lacuna: cada bloco ramifica conforme o dado. Uma clínica
com 84 dias de hiato lê diferente de uma que publica 54 vezes por trimestre.
"""
import json

def n(v, casas=None, suf="", fb="—"):
    if v is None: return fb
    if casas is not None: return f"{v:.{casas}f}".replace(".", ",") + suf
    if isinstance(v, (int, float)) and v == int(v): return f"{int(v):,}".replace(",", ".") + suf
    return str(v) + suf

def pct(v, fb="—"): return fb if v is None else f"{v:.2f}".replace(".", ",") + "%"


def notas(d):
    """Pontua os 6 pilares 0-10 a partir do dado coletado. Sem dado -> None."""
    t, ig, g, ads = d["tecnologia"], d["instagram"], d["google"], d["ads"]
    p = {}

    # site próprio
    if t.get("httpStatus") == 200:
        s = 5.0
        s += 1.0 if t.get("https") else -2.0
        s += 0.8 if t.get("viewportMobile") else -1.0
        s += 1.2 if t.get("jsonLdLocalBusiness") else 0
        s += 0.6 if t.get("metaDescription") else -0.6
        s += 0.5 if t.get("agendamentoOnline") else -0.5
        s += 0.5 if t.get("whatsappNoSite") else -0.5
        if (t.get("ttfbSegundos") or 0) > 3: s -= 1.0
        p["site"] = max(0.0, min(10.0, round(s, 1)))
    elif t.get("site"):
        p["site"] = 0.5   # existe domínio, mas não abre
    else:
        p["site"] = 0.0

    # instagram (engajamento e alcance)
    if ig.get("erAmostra") is not None:
        er = ig.get("er90d") if ig.get("er90d") is not None else ig["erAmostra"]
        s = min(8.0, er * 4.0)                       # 2% -> 8
        if (ig.get("seguidores") or 0) > 8000: s += 0.8
        if (ig.get("medianaPlaysReel") or 0) > 1500: s += 0.6
        p["instagram"] = max(0.0, min(10.0, round(s, 1)))
    else:
        p["instagram"] = None

    # cadência
    h, p90 = ig.get("hiatoDias"), ig.get("postsUlt90d")
    if h is not None:
        s = 9.0 if h <= 3 else 7.5 if h <= 7 else 5.5 if h <= 14 else 3.0 if h <= 30 else 1.0
        if p90 is not None:
            s = min(s, 2.0 if p90 <= 3 else 4.5 if p90 <= 8 else 7.0 if p90 <= 15 else 9.0)
        p["cadencia"] = round(s, 1)
    else:
        p["cadencia"] = None

    # google
    if g.get("perfilEncontrado") is True:
        s = 4.0
        av = g.get("avaliacoes") or 0
        s += 3.0 if av >= 100 else 2.0 if av >= 40 else 1.0 if av >= 10 else 0
        if (g.get("nota") or 0) >= 4.7: s += 1.0
        if g.get("respostasDoProprietario"): s += 1.0
        if g.get("fichasDuplicadas"): s -= 2.0
        if g.get("categoriaCorreta") is False: s -= 1.0
        if av == 0: s -= 2.0                     # ficha existe e nao acumula reputacao
        if g.get("reivindicada") is False: s -= 1.5
        p["google"] = max(0.0, min(10.0, round(s, 1)))
    elif g.get("perfilEncontrado") is False:
        p["google"] = 0.5
    else:
        p["google"] = None

    # reputação e diretórios
    dirs = d.get("diretorios") or {}
    achados = sum(1 for k, v in dirs.items() if v and k != "outros")
    s = min(7.0, 2.0 + achados * 1.2)
    if (dirs.get("doctoraliaOpinioes") or 0) >= 50: s += 2.0
    p["reputacaoEDiretorios"] = round(min(10.0, s), 1)

    # conversão
    s = 3.0
    if t.get("whatsappNoSite"): s += 1.5
    if t.get("agendamentoOnline"): s += 1.5
    if t.get("formulario"): s += 0.5
    if t.get("gtm") or t.get("ga4"): s += 1.5
    if ig.get("ctaPctFaseAtual") is not None:
        c = ig["ctaPctFaseAtual"]
        s += 2.0 if c >= 25 else 1.0 if c >= 12 else 0 if c >= 5 else -1.5
    p["conversao"] = max(0.0, min(10.0, round(s, 1)))

    vals = [v for v in p.values() if v is not None]
    geral = round(sum(vals) / len(vals), 1) if vals else None
    return p, geral


def veredito(geral, d):
    ig, t = d["instagram"], d["tecnologia"]
    if geral is None: return "Coleta incompleta", "Faltam pilares para fechar a nota."
    h = ig.get("hiatoDias")
    tem_ig = ig.get("handle") is not None
    tem_site = t.get("httpStatus") == 200

    # o caso mais grave primeiro: nenhum ativo proprio
    if not tem_ig and not tem_site:
        return ("Nenhum canal próprio localizado",
                "Sem site e sem perfil, a clínica só existe onde terceiros decidem mostrá-la.")
    if t.get("site") and not tem_site:
        return ("O site existe no papel e não abre para ninguém",
                "Enquanto o domínio não responder, todo investimento em conteúdo devolve o paciente para o concorrente.")
    if not tem_ig:
        return ("Site no ar, vitrine social ausente",
                "Em odontologia estética a decisão passa por ver caso tratado, e não há onde ver.")
    if h is not None and h > 40:
        return (f"A conta parou há {h} dias",
                "Alcance orgânico é cumulativo: cada semana parada custa entrega que não volta sozinha.")
    if ig.get("ctaPctFaseAtual") is not None and ig["ctaPctFaseAtual"] < 5:
        return ("Publica com constância e quase nunca pede a consulta",
                "A audiência existe, o caminho para virar agendamento não.")
    if geral >= 6.5: return ("Base sólida, faltam as peças de conversão",
                             "O trabalho aqui é de ajuste fino, não de reconstrução.")
    return ("Estrutura espalhada, sem eixo",
            "Os canais existem isolados e nenhum sustenta o outro.")


def kpis(d):
    ig, t, g, c = d["instagram"], d["tecnologia"], d["google"], d["clinica"]
    out = []
    out.append((n(ig.get("seguidores")), "Seguidores no Instagram",
                "Base construída em " + n(ig.get("publicacoesTotal")) + " publicações"))
    h = ig.get("hiatoDias")
    out.append((n(h, suf=" dias") if h is not None else "—", "Desde a última publicação",
                "Conta ativa" if (h or 99) <= 7 else "Sinal de abandono do canal"))
    out.append((pct(ig.get("er90d")), "Engajamento nos últimos 90 dias",
                "Saudável acima de 1%" ))
    out.append((pct(ig.get("ctaPctFaseAtual")), "Posts que pedem alguma ação",
                "Cada post sem chamada é alcance que não vira consulta"))
    site = "Fora do ar" if (t.get("site") and t.get("httpStatus") != 200) else ("Ativo" if t.get("httpStatus")==200 else "Não localizado")
    out.append((site, "Site próprio",
                (t.get("cms") or "—") if t.get("httpStatus")==200 else "Sem página que a clínica controle"))
    return out[:5]


if __name__ == "__main__":
    import sys
    d = json.load(open(sys.argv[1]))
    p, g = notas(d)
    print(json.dumps({"pilares": p, "geral": g, "veredito": veredito(g, d)}, ensure_ascii=False, indent=1))


def _motivo(t):
    e = (t.get("erroColeta") or "").lower()
    if "nodename" in e or "dns" in e or "resolve" in e: return "O DNS do domínio não resolve"
    if "tls" in e or "ssl" in e: return "O servidor recusa a conexão segura"
    if "timed out" in e or "timeout" in e: return "O servidor não respondeu no tempo limite"
    return "A conexão falha"


def derivar_dores(d):
    """Deriva as dores do dado medido, cada uma amarrada a uma vertente comercial."""
    t, ig, g = d["tecnologia"], d["instagram"], d["google"]
    D = []
    A = lambda ti, ev, cu, ve: D.append({"titulo": ti, "evidencia": ev, "custo": cu, "vertente": ve})

    if t.get("site") and t.get("httpStatus") != 200:
        A("O site não abre", f"O domínio {t['site']} não responde. {_motivo(t)}, verificado em três clientes independentes",
          "Todo clique vindo da busca cai numa porta fechada", "tecnologia")
    elif not t.get("site"):
        A("Nenhum site próprio", "Nenhuma página no domínio da clínica foi localizada",
          "A presença inteira depende de perfis e diretórios de terceiros", "tecnologia")
    else:
        if not t.get("https"):
            A("Site sem HTTPS", "A home responde em HTTP puro",
              "O navegador marca como não seguro e o Google rebaixa na busca", "tecnologia")
        if not t.get("jsonLdLocalBusiness"):
            A("Sem schema de negócio local", "Nenhum JSON-LD de LocalBusiness ou Dentist na home",
              "Perde rich result na busca local, onde o paciente de implante procura", "tecnologia")
        if not (t.get("gtm") or t.get("ga4")):
            A("O site não mede nada", "Sem GA4 e sem Tag Manager no HTML",
              "Impossível saber de onde vem paciente, logo impossível investir com critério", "tecnologia")
        if not t.get("agendamentoOnline"):
            A("Sem agendamento na página", "Nenhum caminho de agendamento na home",
              "Toda marcação depende de alguém atender no horário comercial", "tecnologia")

    if g.get("perfilEncontrado") is False:
        A("Sem Perfil da Empresa no Google", "Nenhuma ficha localizada na busca nem no Maps",
          "A clínica não entra no pacote local, que é onde a busca por dentista começa", "tecnologia")
    else:
        if g.get("fichasDuplicadas"):
            A("Fichas duplicadas no Google", (f"{len(g['fichasDuplicadas'])} fichas concorrentes" if len(g['fichasDuplicadas'])>1 else "Uma segunda ficha concorrente") + " para o mesmo negócio",
              "O Google divide avaliações e autoridade, e nenhuma acumula o suficiente", "tecnologia")
        if (g.get("avaliacoes") or 0) == 0:
            A("Ficha sem nenhuma avaliação", "O Perfil da Empresa existe e não tem avaliação alguma",
              "Reputação zero na vitrine que mais pesa na decisão local", "tecnologia")
        if g.get("respostasDoProprietario") is False:
            A("Avaliações sem resposta", "Nenhuma resposta do proprietário nas avaliações visíveis",
              "Resposta do dono é sinal de cuidado e pesa no ranqueamento local", "tecnologia")
        if g.get("categoriaCorreta") is False:
            A("Categoria errada no Google", f"Categoria declarada: {g.get('categoria')}",
              "A ficha deixa de aparecer nas buscas do procedimento que a clínica de fato vende", "tecnologia")

    if not ig.get("handle"):
        A("Sem Instagram localizado", "Nenhum perfil encontrado para a clínica",
          "Em odontologia estética ninguém fecha sem ver caso tratado", "social")
    else:
        h = ig.get("hiatoDias") or 0
        if h > 30:
            A("Conta parada", f"{h} dia desde a última publicação" if h == 1 else f"{h} dias desde a última publicação",
              "O algoritmo reduz entrega de quem some, e recuperar custa mais que manter", "social")
        er = ig.get("er90d")
        if er is not None and er < 0.5:
            A("Engajamento no chão", f"{str(er).replace('.',',')}% de engajamento nos últimos 90 dias",
              "A maior parte dos seguidores já não vê o que é publicado", "social")
        cta = ig.get("ctaPctFaseAtual")
        if cta is not None and cta < 8:
            A("Publica sem pedir a consulta", f"Apenas {str(cta).replace('.',',')}% dos posts tem chamada para ação",
              "Audiência construída sem caminho para virar agendamento", "social")
        mix = (ig.get("faseAtual") or {}).get("mixFormatos") or {}
        if mix:
            tot = sum(mix.values()) or 1
            if mix.get("imagem", 0) / tot > 0.45:
                A("Mix de formatos invertido", f"{mix['imagem']} dos {tot} posts da amostra são imagem estática",
                  "O maior volume de esforço vai para o formato de menor entrega", "social")
        p90 = ig.get("postsUlt90d")
        if p90 is not None and p90 <= 6:
            A("Cadência insuficiente", f"{p90} publicação em 90 dias" if p90 == 1 else f"{p90} publicações em 90 dias",
              "Abaixo do mínimo para o algoritmo manter entrega estável", "social")

    if not (t.get("pixelMeta") or t.get("pixelGoogleAds")):
        A("Não anuncia, ou anuncia sem rastrear", "Nenhum pixel da Meta nem tag do Google Ads no site",
          "Alcance limitado ao orgânico, que já está caindo", "trafego")
    elif not (t.get("gtm") or t.get("ga4")):
        A("Anuncia sem medir retorno", "Há pixel de anúncio, mas não há analytics próprio",
          "Dá para gastar, não dá para provar que voltou", "trafego")
    return D
