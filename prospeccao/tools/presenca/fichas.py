#!/usr/bin/env python3
"""Anexa as fichas resumidas das posicoes 16-30 ao MD consolidado."""
import json, pathlib, re, sqlite3, sys
sys.path.insert(0, 'prospeccao/tools')
from telefones import classificar

CONT = re.compile(r"contab|contabil|escritorio|assessoria|conta[dt]or", re.I)
lim = lambda h: (h or "").lstrip("@").strip() or None

F = json.load(open("prospeccao/odonto-DF/data/fichas-16-30.json"))
con = sqlite3.connect("prospeccao/odonto-DF/leads.db"); con.row_factory = sqlite3.Row
leads = {r["cnpj_formatado"]: r for r in con.execute("""
    SELECT l.*, p.propensao FROM leads l JOIN propensao p USING(cnpj) WHERE l.desqualificado=0""")}
por_nome = {(r["nome_fantasia"] or r["razao_social"]).upper(): r for r in leads.values()}

socios = {}
import csv
for r in csv.DictReader(open("/tmp/socios.csv")):
    if r["qualificacao"] == "49":
        socios.setdefault(r["cnpj_basico"], []).append(r["nome"].title())

L = ["\n---\n\n# Fichas resumidas — posições 16 a 30\n",
     "Coleta leve: site, Instagram, Google e contato do decisor. **Não é auditoria completa** —",
     "sem métricas de engajamento, sem análise de SEO técnico e sem leitura de anúncios.",
     "Serve para priorizar quem merece o relatório completo na próxima rodada.\n"]

fichas = []
for r in F:
    nome = r["nome"]
    lead = None
    for k, v in por_nome.items():
        if k.startswith(nome.upper()[:16]) or nome.upper()[:16] in k: lead = v; break
    s = r.get("site") or {}; ig = r.get("instagram") or {}
    g = r.get("google") or {}; dd = r.get("instagramDecisor") or {}
    pe = (lead["propensao"] if lead else 0.85)

    # dor leve: 3 sinais binarios observaveis nesta coleta
    sinais = []
    if s.get("url") and s.get("status") != 200: sinais.append("site fora do ar")
    elif not s.get("url"): sinais.append("nenhum site localizado")
    if not ig.get("handle"): sinais.append("nenhum Instagram localizado")
    if not g.get("perfilEncontrado"): sinais.append("nenhum Perfil da Empresa localizado")
    elif (g.get("avaliacoes") or 0) < 15: sinais.append(f"apenas {g.get('avaliacoes')} avaliações no Google")
    dor = min(1.0, 0.30 + 0.23 * len(sinais))

    # desqualificador: Google marcando encerramento vale mais que qualquer score
    txt = (str(r.get("observacao","")) + " " + " ".join(str(x) for x in (r.get("limitacoes") or []))).lower()
    fechado = ("fechado" in txt or "encerrad" in txt)

    tel = wa = email = None; decisor = None; contador = False
    if lead:
        f1, e1, t1, _ = classificar(lead["telefone"]); f2, e2, _, _ = classificar(lead["telefone_2"])
        tel, wa, email = f1 or f2, e1 or e2, lead["email"]
        contador = bool(email and CONT.search(email))
        adm = socios.get(lead["cnpj_basico"], [])
        decisor = adm[0] if adm else None
    ac = 0.35*bool(decisor) + 0.30*bool(wa) + 0.20*bool(lim(dd.get("handle"))) + 0.05*bool(email)
    prob = round(min(0.95, pe * dor * (0.55 + 0.45 * min(1.0, ac))), 2)
    if fechado: prob = 0.0
    fichas.append((prob, r, lead, decisor, tel, wa, email, contador, sinais, g, ig, s, dd, fechado))

fichas.sort(key=lambda x: -x[0])
L.append("| # | Clínica | Prob. | Google | Site | Instagram |")
L.append("|---|---|---|---|---|---|")
for prob, r, lead, dec, tel, wa, email, cont, sinais, g, ig, s, dd, fechado in fichas:
    goo = f"{g.get('nota')} · {g.get('avaliacoes')} aval." if g.get("perfilEncontrado") else "não localizado"
    site = "ativo" if s.get("status") == 200 else ("**fora do ar**" if s.get("url") else "não localizado")
    rot = "**DESQUALIFICADA**" if fechado else f"{prob:.2f}"
    L.append(f"| {r['pos']} | **{r['nome']}** | {rot} | {goo} | {site} | "
             f"{('@'+lim(ig['handle'])) if lim(ig.get('handle')) else '—'} |")

L.append("\n## Detalhe\n")
for prob, r, lead, dec, tel, wa, email, cont, sinais, g, ig, s, dd, fechado in fichas:
    L.append(f"### {r['pos']}. {r['nome']}\n")
    if fechado:
        L.append("> ⛔ **O Google marca esta empresa como permanentemente fechada.** "
                 "Confirme por telefone antes de qualquer contato — pode ser encerramento real "
                 "ou ficha desatualizada, e as duas hipóteses mudam completamente a abordagem.\n")
    L.append(("**Probabilidade estimada: desqualificada por encerramento**" if fechado
              else f"**Probabilidade estimada: {prob:.2f}**")
             + (f" · {lead['bairro'].title()} · {lead['idade_meses']//12} anos" if lead else "") + "\n")
    if sinais: L.append("**O que trava:** " + "; ".join(sinais) + "\n")
    if g.get("perfilEncontrado"):
        L.append(f"- Google: {g.get('nota')} com {g.get('avaliacoes')} avaliações")
    else:
        L.append("- Google: perfil não localizado")
    L.append(f"- Site: {s.get('url') or 'não localizado'}"
             + (f" (status {s.get('status')})" if s.get("url") else ""))
    if lim(ig.get("handle")):
        L.append(f"- Instagram: @{lim(ig['handle'])}"
                 + (f" · {ig['seguidores']:,} seguidores".replace(",", ".") if ig.get("seguidores") else ""))
    else:
        L.append("- Instagram: não localizado")
    L.append("\n**Contato:**\n")
    L.append(f"- **{dec or 'decisor não identificado'}**" + (" — Sócio-Administrador" if dec else ""))
    if tel: L.append(f"- Telefone: `{tel}`" + ("  ⚠️ e-mail do CNPJ é de contador" if cont else ""))
    if wa: L.append(f"- WhatsApp: `{wa}`")
    if email: L.append(f"- E-mail: `{email}`")
    if lim(dd.get("handle")):
        L.append(f"- Instagram pessoal: **@{lim(dd['handle'])}**"
                 + (f" (confiança {dd.get('confianca')})" if dd.get("confianca") in ("media","baixa") else ""))
    else:
        L.append("- Instagram pessoal: não localizado")
    if r.get("limitacoes"):
        L.append(f"\n<details><summary>Limites ({len(r['limitacoes'])})</summary>\n")
        for x in r["limitacoes"]: L.append(f"- {str(x).rstrip('.')}.")
        L.append("\n</details>")
    L.append("\n---\n")

p = pathlib.Path("prospeccao/odonto-DF/probabilidade-fechamento.md")
base = p.read_text(encoding="utf-8").split("\n---\n\n# Fichas resumidas")[0]
p.write_text(base + "\n".join(L), encoding="utf-8")
print(f"fichas anexadas: {len(fichas)}")
for prob, r, *_ in fichas[:6]: print(f"  {r['pos']:3} {r['nome'][:38]:40} {prob:.2f}")
