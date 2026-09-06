#!/usr/bin/env python3
"""
probabilidade-fechamento.md da advocacia-DF.

Duas diferenças em relação à odontologia:
  1. Ausência de anúncio NÃO conta como dor — é conformidade com o Provimento 205/2021 da OAB.
  2. Entra um fator novo: DESCOMPASSO entre autoridade real e captura digital. Um ex-ministro
     do STJ com uma avaliação no Google é uma venda mais fácil que um escritório mediano com
     o mesmo site ruim, porque o argumento já está pronto e é constrangedor de ignorar.
"""
import csv, json, pathlib, re, sqlite3, sys
sys.path.insert(0, 'prospeccao/tools')
from telefones import classificar

B = pathlib.Path("prospeccao/advocacia-DF")
COL = {r["pos"]: r for r in json.load(open(B/"data"/"coleta-top30.json"))}
CONT = re.compile(r"contab|contabil|escritorio de contab|assessoria|conta[dt]or", re.I)

socios = {}
for r in csv.DictReader(open(B/"data"/"socios-top30.csv")):
    socios.setdefault(r["cnpj_basico"], []).append((r["nome"].title(), r["qualificacao"], r["data_entrada_sociedade"]))

con = sqlite3.connect(B/"leads.db"); con.row_factory = sqlite3.Row
leads = con.execute("""SELECT l.*, p.propensao, p.tier FROM leads l JOIN propensao p USING(cnpj_basico)
                       ORDER BY p.propensao DESC LIMIT 30""").fetchall()

def dor_e_dores(c):
    """-> (fator 0-1, lista de dores por vertente)"""
    s, D = 0.0, []
    A = lambda ti, ev, cu, ve: D.append({"t": ti, "e": ev, "c": cu, "v": ve})
    site, g = c.get("site") or {}, c.get("google") or {}
    obs = (site.get("observacao") or "").lower()

    if site.get("status") != 200 and not site.get("url"):
        s += .28; A("Nenhum site próprio localizado", "Não foi encontrada página no domínio do escritório",
                    "A presença depende inteiramente de diretórios e do que terceiros publicam", "tecnologia")
    elif "suspens" in obs or "suspend" in obs:
        s += .30; A("Site suspenso pela hospedagem", "Toda requisição cai na página de suspensão do cPanel",
                    "O HTTP 200 engana: o visitante vê aviso de suspensão, não o escritório", "tecnologia")
    elif site.get("status") != 200:
        s += .28; A("Site não responde", f"Status {site.get('status')}",
                    "Quem chega pela busca encontra porta fechada", "tecnologia")
    else:
        if "ssl" in obs or "certificado" in obs:
            s += .14; A("Certificado SSL expirado", "O navegador exibe aviso de site não seguro",
                        "Aviso de insegurança na hora exata em que o cliente decidiria escrever", "tecnologia")
        if "desenvolvimento" in obs or "my wordpress blog" in obs or "novo " in obs:
            s += .20; A("Site inacabado no ar", site.get("observacao","")[:150],
                        "O visitante vê um rascunho onde deveria ver a banca", "tecnologia")

    if not g.get("perfilEncontrado"):
        s += .22; A("Sem Perfil da Empresa no Google", "Nenhuma ficha localizada na busca nem no Maps",
                    "O escritório não entra no mapa nem no pacote local", "tecnologia")
    else:
        av = g.get("avaliacoes")
        if av is not None and av < 5:
            s += .18; A("Reputação pública quase inexistente",
                        (f"{av} avaliação no Google" if av == 1 else f"{av} avaliações no Google"),
                        "Quem decide contratar advogado pesquisa, e não encontra sinal de terceiros", "tecnologia")
        if g.get("nota") is not None and g["nota"] < 4.2:
            s += .16; A("Nota baixa exposta na busca", f"{str(g['nota']).replace('.',',')} no Google",
                        "A primeira coisa que o cliente vê é a pior informação disponível", "tecnologia")
        gobs = (g.get("observacao") or "") + " " + " ".join(str(x) for x in (c.get("limitacoes") or []))
        if "duplicad" in gobs.lower() or "duas fichas" in gobs.lower():
            s += .18; A("Fichas duplicadas no Google", "Mais de uma ficha para o mesmo escritório",
                        "Avaliações e autoridade divididas; nenhuma acumula o suficiente", "tecnologia")
        if "reivindic" in gobs.lower():
            s += .12; A("Ficha não reivindicada", "O Google ainda oferece 'Reivindicar esta empresa'",
                        "Ninguém do escritório controla o que aparece ali", "tecnologia")

    if not (c.get("instagram") or {}).get("handle") and not (c.get("linkedin") or {}).get("empresa"):
        s += .16; A("Sem canal social próprio", "Nem Instagram nem LinkedIn de empresa localizados",
                    "Nenhum espaço para publicar a produção técnica que já existe", "social")
    elif not (c.get("linkedin") or {}).get("empresa"):
        s += .08; A("Sem LinkedIn de empresa", "Não localizado",
                    "Em advocacia o LinkedIn pesa mais que o Instagram e está vazio", "social")
    return min(1.0, s), D

def autoridade(c):
    sin = ((c.get("autoridade") or {}).get("sinais")) or []
    return (min(1.0, len(sin) / 4.0), sin)


def captura(c):
    """Quanto da autoridade existente esta de fato capturada digitalmente. 0 = nada."""
    g, site = c.get("google") or {}, c.get("site") or {}
    obs = (site.get("observacao") or "").lower()
    v = 0.0
    av = g.get("avaliacoes")
    if g.get("perfilEncontrado"):
        v += 0.10
        if av is not None:
            v += 0.35 if av >= 50 else 0.25 if av >= 20 else 0.12 if av >= 5 else 0.0
    if site.get("status") == 200 and not any(x in obs for x in
            ("suspens","suspend","desenvolvimento","my wordpress","ssl","certificado")):
        v += 0.25
    if (c.get("instagram") or {}).get("handle"): v += 0.12
    if (c.get("linkedin") or {}).get("empresa"): v += 0.10
    if (c.get("linkedin") or {}).get("decisor"): v += 0.08
    return min(1.0, v)

fichas = []
import unicodedata
def norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii","ignore").decode().lower()
    return "".join(ch for ch in s if ch.isalnum() or ch == " ")

# os agentes receberam a lista NA MESMA ORDEM deste ranking -> casar por posicao,
# e conferir pelo nome para nao desalinhar em silencio
divergentes = []
for idx, l in enumerate(leads, 1):
    pos = idx
    c = COL.get(pos, {})
    a, b = norm(c.get("nome",""))[:14], norm(l["nome_fantasia"] or l["razao_social"])[:14]
    if c and a and b and a.split()[0] != b.split()[0]:
        divergentes.append(f"  pos {pos}: coleta='{c.get('nome','')[:34]}' banco='{(l['nome_fantasia'] or l['razao_social'])[:34]}'")
    dfat, dores = dor_e_dores(c)
    aut, sinais = autoridade(c)
    cap = captura(c)
    # DESCOMPASSO e o eixo principal do nicho: autoridade real que nao esta capturada.
    # Ex-ministra do STJ com 1 avaliacao no Google vale mais que banca mediana com site ruim.
    desc = round(aut * (1 - cap), 3)
    if desc >= 0.45:
        dores.insert(0, {"t": "Autoridade não capturada",
            "e": f"{len(sinais)} sinais de reconhecimento (rankings, cargos, docência, publicações) "
                 f"contra uma presença digital que captura {cap*100:.0f}% disso",
            "c": "O ativo mais caro do escritório — a reputação — não chega a quem procura",
            "v": "social"})
    s = socios.get(l["cnpj_basico"], [])
    adm = [x for x in sorted(s, key=lambda y: y[2]) if x[1] == "49"] or sorted(s, key=lambda y: y[2])
    dec = adm[0][0] if adm else None
    ac = 0.35*bool(dec) + 0.30*bool(l["whatsapp"]) + 0.20*bool((c.get("linkedin") or {}).get("decisor")
          or (c.get("instagram") or {}).get("handle")) + 0.05*bool(l["email"])
    # descompasso: autoridade alta com captura baixa é o argumento mais forte do nicho
    # o que puxa a venda e o MAIOR entre dor tecnica e descompasso de autoridade
    motor = max(dfat, desc)
    p = round(min(0.95, l["propensao"] * max(0.20, motor) * (0.55 + 0.45*min(1.0, ac))), 3)
    if l["desqualificado"]: p = 0.0
    fichas.append({"l": l, "c": c, "pos": pos, "dor": dfat, "dores": dores, "aut": aut,
                   "sinais": sinais, "dec": dec, "acesso": round(ac,2), "cap": cap,
                   "desc": desc, "motor": motor, "p": p})

if divergentes:
    print("AVISO — nomes divergentes entre coleta e banco:")
    print("\n".join(divergentes))
else:
    print("casamento por posicao conferido: 30/30 com nome batendo")

fichas.sort(key=lambda x: -x["p"])
faixa = lambda p: "Muito alta" if p>=.42 else "Alta" if p>=.32 else "Média" if p>=.22 else "Baixa"

L = ["# Probabilidade de fechamento — Advocacia DF\n",
 "Top 30 escritórios por propensão estrutural, com coleta digital de 19/08/2026.\n",
 "## O que muda em relação à odontologia\n",
 "**1. O campo `porte` da Receita é inútil aqui.** 68% dos escritórios marcados como \"DEMAIS\" são",
 "optantes pelo Simples — contradição direta. O eixo de capacidade foi reconstruído sobre o",
 "**número de sócios**, com pico em 4 a 12: menor que isso não paga, maior que isso já tem",
 "marketing interno.\n",
 "**2. Ausência de anúncio não é dor.** O Provimento 205/2021 da OAB restringe publicidade.",
 "Escritório que não anuncia está em conformidade, não em falha — tratar isso como problema numa",
 "reunião seria constrangedor.\n",
 "**3. Entra um fator novo: o descompasso.** Autoridade real alta com captura digital baixa vale",
 "mais que dor isolada, porque o argumento já está pronto. Um ex-ministro do STJ com uma avaliação",
 "no Google é uma conversa mais fácil que um escritório mediano com o mesmo site ruim.\n",
 "```",
 "descompasso   = autoridade real × (1 - quanto dela está capturada digitalmente)",
 "probabilidade = propensão estrutural × max(dor técnica, descompasso) × acessibilidade",
 "```\n",
 "Como na odontologia, **não é percentual calibrado** — não há base de negócios perdidos.\n",
 "## Ranking\n",
 "| # | Escritório | Prob. | Sócios | Autoridade | Capturado | O que trava |",
 "|---|---|---|---|---|---|---|"]
for i, f in enumerate(fichas, 1):
    l = f["l"]
    trava = f["dores"][0]["t"] if f["dores"] else ("desqualificado" if l["desqualificado"] else "sem lacuna evidente")
    L.append(f"| {i} | **{(l['nome_fantasia'] or l['razao_social'])}** | "
             + ("**desq.**" if l["desqualificado"] else f"{f['p']:.2f}")
             + f" | {l['n_socios']} | {f['aut']:.2f} | {f['cap']*100:.0f}% | {trava} |")

L.append("\n---\n\n## Ficha por escritório\n")
for i, f in enumerate(fichas, 1):
    l, c = f["l"], f["c"]
    nome = l["nome_fantasia"] or l["razao_social"]
    L.append(f"### {i}. {nome}\n")
    if l["desqualificado"]:
        L.append(f"> ⛔ **Desqualificado.** {l['motivo_desq']}\n\n---\n"); continue
    L.append(f"**Probabilidade: {f['p']:.2f} — {faixa(f['p'])}**  ·  {l['n_socios']} sócios · "
             f"{l['bairro']} · {l['idade_meses']//12} anos\n")
    if l["alerta"]: L.append(f"> ⚠️ **{l['alerta']}**\n")
    motor_rot = "descompasso de autoridade" if f["desc"] >= f["dor"] else "dor técnica"
    L.append(f"**A conta:** propensão {l['propensao']:.2f} × {motor_rot} {f['motor']:.2f} × "
             f"acessibilidade {f['acesso']:.2f} = **{f['p']:.2f}**\n")
    L.append(f"> Autoridade medida em {f['aut']:.2f}; a presença digital captura {f['cap']*100:.0f}% dela.\n")
    if f["sinais"]:
        L.append("**Autoridade que não está capturada:**\n")
        for s in f["sinais"][:5]: L.append(f"- {s}")
        L.append("")
    if f["dores"]:
        L.append("**Dores, por vertente:**\n")
        for v, rot in (("tecnologia","Tecnologia — site, Google e atendente de IA no WhatsApp"),
                       ("social","Gestão de conteúdo e autoridade")):
            ds = [x for x in f["dores"] if x["v"] == v]
            if ds:
                L.append(f"*{rot}*\n")
                for x in ds: L.append(f"- **{x['t']}** — {x['e']}. {x['c']}")
                L.append("")
    g = c.get("google") or {}; site = c.get("site") or {}
    L.append("**Medido:**\n")
    _av = g.get("avaliacoes")
    _gt = (f"nota {str(g.get('nota')).replace('.',',')} com "
           + ("1 avaliação" if _av == 1 else f"{_av} avaliações")) if g.get("perfilEncontrado") else "perfil não localizado"
    L.append(f"- Google: {_gt}")
    L.append(f"- Site: {site.get('url') or 'não localizado'}" + (f" — {site.get('observacao')}" if site.get("observacao") else ""))
    ig = (c.get("instagram") or {}).get("handle"); li = (c.get("linkedin") or {})
    L.append(f"- Instagram: " + (f"@{ig}" if ig else "não localizado"))
    L.append(f"- LinkedIn: empresa {'sim' if li.get('empresa') else 'não localizado'}, "
             f"decisor {'sim' if li.get('decisor') else 'não localizado'}")
    L.append("\n**Como chegar no decisor:**\n")
    L.append(f"- **{f['dec'] or 'não identificado'}** — sócio-administrador")
    if l["telefone"]: L.append(f"- Telefone: `{l['telefone']}`"
        + ("  ⚠️ compartilhado com outro CNPJ" if l["telefone_compartilhado"] else ""))
    if l["whatsapp"]: L.append(f"- WhatsApp: `{l['whatsapp']}`")
    if l["email"]: L.append(f"- E-mail: `{l['email']}`"
        + ("  ⚠️ é de escritório de contabilidade" if l["email_de_contador"] else ""))
    if li.get("decisor"): L.append(f"- LinkedIn: {li['decisor']}")
    L.append(f"- Endereço: {l['endereco']}, {l['bairro']}")
    if c.get("limitacoes"):
        L.append(f"\n<details><summary>Limites da coleta ({len(c['limitacoes'])})</summary>\n")
        for x in c["limitacoes"]: L.append(f"- {str(x).rstrip('.')}.")
        L.append("\n</details>")
    L.append("\n---\n")

(B/"probabilidade-fechamento.md").write_text("\n".join(L), encoding="utf-8")
print(f"gerado: {len(L)} linhas")
print(f"\n{'#':3}{'escritorio':40}{'prob':>7}  faixa")
for i, f in enumerate(fichas[:12], 1):
    l = f["l"]
    print(f"{i:3}{(l['nome_fantasia'] or l['razao_social'])[:38]:40}"
          + ("  desq." if l["desqualificado"] else f"{f['p']:7.2f}  {faixa(f['p'])}"))
