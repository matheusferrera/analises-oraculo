#!/usr/bin/env python3
"""
Gera Analise-Presenca-Digital.html a partir de um presenca.json.

Reusa o design system canônico (DrPedroBrandao / DrAdrianoBorges, 17/08): CSS de
12.071 bytes copiado sem edição, fontes Bricolage Grotesque + Petrona, sem <details>,
bloco de insight ao fim de cada seção com header em texto puro (sem SVG — isso é
específico dos relatórios de presença digital).

Determinístico: mesma entrada, mesma saída.
"""
import html, json, pathlib, sys

BASE = pathlib.Path(__file__).parent / "presenca"
CSS = (BASE / "presenca.css").read_text(encoding="utf-8")
FONTS = (BASE / "head-fonts.html").read_text(encoding="utf-8")

SECOES = [("essencial","Essencial"),("diagnostico","Diagnóstico"),("google","Google"),
          ("site","Site e tecnologia"),("instagram","Instagram"),("ads","Anúncios"),
          ("conteudo","Conteúdo"),("diretorios","Diretórios"),("concorrencia","Concorrência"),
          ("conversao","Conversão"),("swot","SWOT"),("recomendacoes","180 dias"),("resumo","Resumo")]

VERDICT = {"good":"▲ Bom","warn":"▶ Atenção","bad":"▶ Atenção","purple":"★ Visão","":"★ Destaque"}
PILAR_ROT = {"google":"Google","site":"Site próprio","instagram":"Instagram",
             "cadencia":"Cadência","reputacaoEDiretorios":"Reputação e diretórios",
             "conversao":"Conversão"}
e = lambda s: html.escape(str(s), quote=True) if s is not None else ""


def insight(classe, texto):
    c = ("insight " + classe).strip()
    return (f'<div class="{c}"><div class="insight-header">O que isso significa para você</div>'
            f'<div class="insight-body"><span class="verdict">{VERDICT.get(classe,"★ Destaque")}</span>'
            f'<p>{texto}</p></div></div>')


def callout(titulo, texto):
    return f'<div class="callout"><strong>{e(titulo)}</strong><p>{texto}</p></div>'


def card(eyebrow, h3, p):
    t = f'<p class="eyebrow">{e(eyebrow)}</p>'
    if h3: t += f"<h3>{h3}</h3>"
    return f'<div class="card">{t}<p>{p}</p></div>'


def secao(sid, titulo, sub, corpo, ins):
    return (f'<section id="{sid}"><div class="sec-head"><h2>{titulo}</h2><p>{sub}</p></div>'
            f'{corpo}{ins}</section>')


def num(v, suf="", casas=None, fallback="—"):
    if v is None: return fallback
    if casas is not None: return f"{v:.{casas}f}".replace(".", ",") + suf
    if isinstance(v, int): return f"{v:,}".replace(",", ".") + suf
    return str(v) + suf


def score_block(ng):
    val = ng.get("valor")
    v = num(val, casas=1) if val is not None else "—"
    itens = ""
    for k, rot in PILAR_ROT.items():
        n = (ng.get("pilares") or {}).get(k)
        larg = 0 if n is None else int(round(n * 10))
        itens += (f'<div class="score-item"><div class="score-item-head"><span>{rot}</span>'
                  f'<span>{num(n, casas=1)}</span></div><div class="score-track">'
                  f'<div class="score-fill" style="width:{larg}%"></div></div></div>')
    return (f'<div class="score"><div><div class="score-number"><span class="score-val">{v}</span>'
            f'<span class="score-den">/ 10</span></div></div>'
            f'<p class="score-verdict"><b>{e(ng.get("veredito",""))}</b><br/>{ng.get("explicacao","")}</p></div>'
            f'<div class="score-grid">{itens}</div>')


def diag_cols(sit, imp, resp):
    col = lambda t, its: (f'<div class="diag-col"><p class="eyebrow">{t}</p><ul>'
                          + "".join(f"<li>{x}</li>" for x in its) + "</ul></div>")
    return f'<div class="diag">{col("Situação",sit)}{col("Impacto",imp)}{col("Resposta",resp)}</div>'


def tabela(cabs, linhas):
    th = "".join(f"<th>{e(c)}</th>" for c in cabs)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in l) + "</tr>" for l in linhas)
    return f'<div class="tabela-wrap"><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


def construir(d, textos):
    """textos: dict com a redação por seção, produzida pelo redator (redigir.py)."""
    c, t, ig, ads, g = d["clinica"], d["tecnologia"], d["instagram"], d["ads"], d["google"]
    nome, slug = c["nome"], d["slug"]
    nav = "".join(f'<a href="#{i}">{r}</a>' for i, r in SECOES)
    kpis = "".join(
        f'<div class="kpi"><div class="kpi-val">{v}</div><div class="kpi-label">{l}</div>'
        f'<div class="kpi-note">{n}</div></div>' for v, l, n in textos["kpis"])

    corpo = ""
    for sid, _ in SECOES:
        b = textos["secoes"][sid]
        corpo += secao(sid, b["h2"], b["sub"], b["corpo"], insight(b.get("insight_classe",""), b["insight"]))

    return f"""<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Análise de Presença Digital: {e(nome)} | Oráculo</title>
<meta name="description" content="{e(textos['meta_description'])}"/>
<meta property="og:type" content="website"/>
<meta property="og:title" content="Análise de Presença Digital: {e(nome)} | Oráculo"/>
<meta property="og:description" content="{e(textos['meta_description'])}"/>
<meta property="og:image" content="https://analises-oraculo.vercel.app/{slug}/og-presenca.png"/>
<meta property="og:image:width" content="1200"/><meta property="og:image:height" content="630"/>
<meta property="og:url" content="https://analises-oraculo.vercel.app/{slug}/Analise-Presenca-Digital.html"/>
<meta property="og:site_name" content="Oráculo Tecnologia"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:image" content="https://analises-oraculo.vercel.app/{slug}/og-presenca.png"/>
{FONTS}
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>{CSS}</style>
<header class="cover"><div class="cover-inner">
<div class="cover-mark"><b>Oráculo Tecnologia</b> · Auditoria de presença digital</div>
<h1>{textos['manchete']}</h1>
<p class="cover-sub">{textos['cover_sub']}</p>
<div class="cover-rule"></div>
<div class="cover-foot"><span><b>{e(nome)}</b></span><span>{e(textos['cover_foot'])}</span></div>
</div></header>
<div class="kpi-band"><div class="kpi-row">{kpis}</div></div>
<nav class="nav" aria-label="Seções da análise">{nav}</nav>
<main class="page">{corpo}</main>
<div class="closing"><div class="closing-inner"><h2>{textos['fecho_titulo']}</h2>
<p>{textos['fecho']}</p>
<div class="closing-meta">Oráculo Tecnologia · Presença digital · 1ª coleta · Agosto de 2026</div>
</div></div>
<footer><span>Oráculo Tecnologia © 2026</span><span>{e(textos['footer_fontes'])}</span></footer>
<script>{textos['charts']}</script>"""


def validar(h, nome_cliente):
    """Regras do CLAUDE.md: sem resíduo de template, sem aspas curvas em tags, com meta description."""
    import re
    p = []
    for termo in ("Debem", "Santos Advogados", "Adriano Borges", "Pedro Brandão",
                  "drpedrobrandaocp", "dr.adrianoborges", "Joana"):
        if termo.lower() in h.lower() and termo.lower() not in nome_cliente.lower():
            p.append(f"residuo de template: {termo}")
    if re.search(r'<[^>]*[”“][^>]*>', h): p.append("aspas curvas dentro de tag")
    if 'name="description"' not in h: p.append("falta meta description")
    if "<details" in h: p.append("usa <details> (padrao mudou em 17/08)")
    # contar so no corpo: o proprio CSS menciona .insight-header
    corpo = h.split("</style>", 1)[-1]
    n_ins = len(re.findall(r'<div class="insight[ "]', corpo))
    if n_ins != len(SECOES):
        p.append(f"insights: {n_ins} para {len(SECOES)} secoes")
    n_sec = len(re.findall(r'<section id=', corpo))
    if n_sec != len(SECOES):
        p.append(f"secoes: {n_sec} para {len(SECOES)} esperadas")
    return p


if __name__ == "__main__":
    print("modulo de build — usado por gerar.py")
