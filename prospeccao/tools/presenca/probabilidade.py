#!/usr/bin/env python3
"""
Gera probabilidade-fechamento.md: probabilidade de fechar, dor por vertente e contato.

Sobre "probabilidade": a Oráculo tem ~13 clientes e nenhuma base de negócios perdidos.
Não há dado histórico para calibrar percentual — "72% de chance" seria número inventado.
Entregamos faixa + pontuação + a conta aberta. Vira regressão logística quando houver
histórico de ganhos e perdas.
"""
import json, pathlib, sqlite3, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from redigir import notas, veredito

R = pathlib.Path("prospeccao/odonto-DF/analises")
VERT = {"tecnologia": "Tecnologia (site, Google e atendente de IA no WhatsApp)",
        "social": "Gestão de redes sociais", "trafego": "Tráfego pago"}


def acessibilidade(d):
    dec = d["decisor"]; s, por = 0.0, []
    if dec.get("nome"): s += 0.35; por.append("nome do sócio-administrador conhecido")
    if dec.get("whatsapp"): s += 0.30; por.append("WhatsApp direto")
    elif dec.get("telefone"): s += 0.20; por.append("telefone")
    if dec.get("instagramPessoal"): s += 0.20; por.append("Instagram pessoal identificado")
    if dec.get("email"): s += 0.05
    if dec.get("decisaoCompartilhada") is False: s += 0.10; por.append("decisão de uma pessoa só")
    elif dec.get("decisaoCompartilhada"): por.append("decisão compartilhada entre dois sócios")
    return min(1.0, round(s, 2)), por


def dor(geral):
    """Nota baixa = dor alta. Piso em 0,15: nota péssima com capacidade zero não vira venda."""
    if geral is None: return None
    return round(max(0.15, min(1.0, (10 - geral) / 8)), 2)


def faixa(p):
    # calibrado sobre a distribuicao real das 15 (0,35 a 0,84) para a faixa priorizar de fato
    return ("Muito alta" if p >= 0.70 else "Alta" if p >= 0.50 else
            "Média" if p >= 0.40 else "Baixa")


con = sqlite3.connect("prospeccao/odonto-DF/leads.db"); con.row_factory = sqlite3.Row
prop = {r["cnpj_formatado"]: r["propensao"] for r in
        con.execute("SELECT l.cnpj_formatado, p.propensao FROM leads l JOIN propensao p USING(cnpj)")}

fichas = []
for pasta in sorted(x for x in R.iterdir() if x.is_dir()):
    d = json.loads((pasta/"data"/"presenca.json").read_text(encoding="utf-8"))
    pil, geral = notas(d); v = veredito(geral, d)
    pe = prop.get(d["cnpj"], 0.5)
    dd = dor(geral) or 0.5
    ac, porque = acessibilidade(d)
    # orcamento provado: anuncio ativo na Meta e o sinal mais forte de capacidade de pagar
    al = (d.get("ads") or {}).get("metaAdLibrary") or {}
    anuncia = bool(al.get("conseguiuLer") and (al.get("anunciosAtivos") or 0) > 0)
    orc = 1.18 if anuncia else 1.0
    if anuncia: porque.append(f"orçamento provado: {al.get('criativos')} criativos ativos na Meta")
    p = round(min(0.95, pe * dd * (0.55 + 0.45 * ac) * orc), 3)   # acessibilidade modula, nao zera
    fichas.append({"d": d, "pilares": pil, "geral": geral, "veredito": v, "propEstrut": pe,
                   "dor": dd, "acesso": ac, "porque": porque, "prob": p, "faixa": faixa(p),
                   "pasta": pasta.name})

fichas.sort(key=lambda x: -x["prob"])

L = []
L.append("# Probabilidade de fechamento — Top 15 odonto DF\n")
L.append("Coleta de 18 e 19/08/2026. Fonte de cada número declarada em `analises/<clinica>/data/presenca.json`.\n")
L.append("## Como ler a probabilidade\n")
L.append("**Não é um percentual calibrado.** A Oráculo tem cerca de 13 clientes e nenhuma base de")
L.append("negócios perdidos — não existe histórico para calibrar. Qualquer \"72% de chance\" seria")
L.append("precisão inventada. O que há aqui é uma pontuação com a conta aberta:\n")
L.append("```\nprobabilidade = propensão estrutural  ×  dor digital medida  ×  acessibilidade do decisor\n```\n")
L.append("- **Propensão estrutural** — capacidade de pagar, ticket do nicho, região, porte, maturidade (já calculada na fila)")
L.append("- **Dor digital medida** — inverso da nota de presença digital, com piso: nota ruim sem capacidade não vira venda")
L.append("- **Acessibilidade** — nome do decisor, WhatsApp, Instagram pessoal, decisão única ou compartilhada")
L.append("- **Orçamento provado** — quem já mantém anúncio ativo na Meta ganha 18%: é o sinal mais forte")
L.append("  de capacidade de pagar que existe, porque não depende de estimativa\n")
L.append("Quando houver 50 a 100 negócios rotulados como ganhos ou perdidos, isso vira regressão")
L.append("logística e aí sim sai percentual honesto.\n")

L.append("## Ranking\n")
L.append("| # | Clínica | Prob. | Faixa | Nota digital | O que trava |")
L.append("|---|---|---|---|---|---|")
for i, f in enumerate(fichas, 1):
    g = f["geral"]
    L.append(f"| {i} | **{f['d']['clinica']['nome']}** | {f['prob']:.2f} | {f['faixa']} | "
             f"{('%.1f' % g).replace('.',',') if g else '—'}/10 | {f['veredito'][0]} |")

L.append("\n---\n## Ficha por clínica\n")
for i, f in enumerate(fichas, 1):
    d, dec = f["d"], f["d"]["decisor"]; c = d["clinica"]; ig = d["instagram"]; t = d["tecnologia"]
    L.append(f"### {i}. {c['nome']}\n")
    L.append(f"**Probabilidade: {f['prob']:.2f} — {f['faixa']}**  ·  Nota digital "
             f"{('%.1f' % f['geral']).replace('.',',') if f['geral'] else '—'}/10  ·  "
             f"{c['porte']} · {c['regiao']} · {c['idadeAnos']} anos\n")
    L.append(f"> {f['veredito'][0]}. {f['veredito'][1]}\n")

    al = (d.get("ads") or {}).get("metaAdLibrary") or {}
    anuncia = bool(al.get("conseguiuLer") and (al.get("anunciosAtivos") or 0) > 0)
    conta = "**A conta:** propensão estrutural {:.2f} × dor {:.2f} × acessibilidade {:.2f}".format(
        f["propEstrut"], f["dor"], f["acesso"])
    if anuncia: conta += " × orçamento provado 1,18"
    L.append(conta + " = **{:.2f}**\n".format(f["prob"]))
    if anuncia:
        L.append(f"> **Já investe em anúncio:** {al.get('criativos')} criativos ativos na Meta"
                 + (f", no ar há {str(al.get('mesesNoAr')).replace('.',',')} meses" if al.get("mesesNoAr") else "")
                 + ". Não é preciso convencer que marketing vale — a verba já existe e já é gasta.\n")

    if d.get("dores"):
        L.append("**Dores mapeadas, por vertente:**\n")
        for v in ("tecnologia", "social", "trafego"):
            ds = [x for x in d["dores"] if x.get("vertente") == v]
            if ds:
                L.append(f"*{VERT[v]}*\n")
                for x in ds:
                    L.append(f"- **{x['titulo']}** — {x['evidencia']}. {x.get('custo','')}")
                L.append("")

    L.append("**Números medidos:**\n")
    L.append("| | |")
    L.append("|---|---|")
    if ig.get("handle"):
        L.append(f"| Instagram | @{ig['handle']} · {ig.get('seguidores'):,} seguidores".replace(",", ".") + " |")
        L.append(f"| Última publicação | há {ig.get('hiatoDias')} dias |")
        L.append(f"| Engajamento 90 dias | {str(ig.get('er90d')).replace('.',',')}% |")
        L.append(f"| Posts nos últimos 90 dias | {ig.get('postsUlt90d')} |")
        L.append(f"| Posts com chamada para ação | {str(ig.get('ctaPctFaseAtual')).replace('.',',')}% |")
    else:
        L.append("| Instagram | nenhum perfil localizado |")
    if t.get("httpStatus") == 200:
        falhas = []
        if not t.get("https"): falhas.append("sem HTTPS")
        if not t.get("jsonLdLocalBusiness"): falhas.append("sem schema local")
        if not (t.get("gtm") or t.get("ga4")): falhas.append("sem analytics")
        if not (t.get("pixelMeta") or t.get("pixelGoogleAds")): falhas.append("sem pixel de anúncio")
        L.append(f"| Site | {t.get('site')} · {t.get('cms') or 'stack não identificada'} |")
        L.append(f"| Falhas do site | {', '.join(falhas) if falhas else 'nenhuma relevante'} |")
    elif t.get("site"):
        L.append(f"| Site | **{t.get('site')} não abre** — {t.get('erroColeta','falha de conexão')} |")
    else:
        L.append("| Site | nenhum site próprio localizado |")
    L.append("")

    L.append("**Como chegar no decisor:**\n")
    L.append(f"- **{dec.get('nome') or 'não identificado'}** — {dec.get('qualificacao') or '—'}")
    if dec.get("decisaoCompartilhada"):
        L.append("- Decisão **compartilhada** entre dois sócios-administradores: alinhe os dois")
    if dec.get("telefone"): L.append(f"- Telefone: `{dec['telefone']}` ({dec.get('telefoneTipo') or '—'})")
    if dec.get("whatsapp"): L.append(f"- WhatsApp: `{dec['whatsapp']}`")
    if dec.get("email"): L.append(f"- E-mail: `{dec['email']}`")
    if dec.get("instagramPessoal"):
        conf = dec.get("instagramPessoalConfianca")
        L.append(f"- Instagram pessoal: **@{dec['instagramPessoal']}**"
                 + (f" (confiança {conf} — confirme antes de usar)" if conf == "media" else ""))
    else:
        L.append("- Instagram pessoal: não localizado")
    L.append(f"- Endereço: {c.get('endereco') or '—'}")
    L.append("")
    if d.get("limitacoes"):
        L.append("<details><summary><b>Limites desta coleta</b> "
                 f"({len(d['limitacoes'])} ressalvas)</summary>\n")
        for x in d["limitacoes"]:
            L.append(f"- {x.rstrip('.')}.")
        L.append("\n</details>\n")
    L.append("---\n")

pathlib.Path("prospeccao/odonto-DF/probabilidade-fechamento.md").write_text("\n".join(L), encoding="utf-8")
print(f"gerado: probabilidade-fechamento.md ({len(L)} linhas)")
print(f"\n{'#':3}{'clinica':34}{'prob':>7}  faixa")
for i, f in enumerate(fichas, 1):
    print(f"{i:3}{f['d']['clinica']['nome'][:32]:34}{f['prob']:7.2f}  {f['faixa']}")
