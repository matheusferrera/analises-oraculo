#!/usr/bin/env python3
"""Transforma o scan digital em diagnóstico por clínica, com problemas e gancho."""
import json, sys

D = json.load(open("prospeccao/odonto-DF/data/scan-digital.json"))


def diagnosticar(r):
    """-> (lista de problemas, severidade 0-100)"""
    p, sev = [], 0
    tem_site = bool(r.get("site_url"))

    if not tem_site:
        p.append(("site", "**Sem site próprio.** Só aparece em diretórios de terceiros — "
                          "não controla a própria narrativa nem captura o paciente que pesquisa.")); sev += 30
    else:
        if r.get("status", 0) == 0:
            p.append(("site", "Site não respondeu à requisição — pode estar fora do ar.")); sev += 28
        else:
            if not r.get("https"):
                p.append(("site", "Sem HTTPS. Navegador marca como 'não seguro' e o Google rebaixa.")); sev += 12
            if not r.get("viewport"):
                p.append(("site", "Sem meta viewport: **quebra no celular**, de onde vem a maioria das buscas por dentista.")); sev += 15
            if r.get("ms", 0) > 3000:
                p.append(("site", f"Carregamento lento ({r['ms']/1000:.1f}s). Acima de 3s a desistência dispara.")); sev += 8

        if not r.get("meta_desc"):
            p.append(("seo", "Sem meta description — o Google inventa o texto do resultado de busca.")); sev += 10
        if not r.get("title") or r.get("title_len", 0) < 25:
            p.append(("seo", "Title curto ou ausente: perde as palavras-chave que trazem busca local.")); sev += 10
        if r.get("h1", 0) == 0:
            p.append(("seo", "Nenhum H1 na página — estrutura semântica ausente.")); sev += 6
        elif r.get("h1", 0) > 1:
            p.append(("seo", f"{r['h1']} H1 na mesma página, diluindo o tema principal.")); sev += 4
        if not r.get("schema_local"):
            p.append(("seo", "Sem schema.org de negócio local. Perde rich result e reforço de SEO local.")); sev += 9
        if not r.get("agendamento"):
            p.append(("site", "Sem caminho claro de agendamento na home.")); sev += 8
        if not r.get("whatsapp"):
            p.append(("site", "Sem WhatsApp — principal canal de conversão do setor.")); sev += 10

    if tem_site:
        if not r.get("gtm"):
            p.append(("anuncios", "**Sem tag de analytics.** Não mede nada, então não sabe de onde vem paciente.")); sev += 12
        if not r.get("fb_pixel") and not r.get("google_ads"):
            p.append(("anuncios", "Nenhum pixel de anúncio (Meta ou Google Ads): **não anuncia**, "
                                  "ou anuncia sem rastrear conversão.")); sev += 10
        elif r.get("fb_pixel") and not r.get("google_ads"):
            p.append(("anuncios", "Pixel da Meta presente, sem Google Ads. Não disputa a busca por intenção."))
            sev += 5

    if not r.get("instagram"):
        p.append(("instagram", "**Instagram não localizado.** Para odontologia estética, é a vitrine principal.")); sev += 22
    if not r.get("instagram_socio") and r.get("socio"):
        p.append(("instagram", f"Sem perfil pessoal identificado de {r['socio'].split()[0]} — "
                               "a autoridade do profissional não está capturada."))
        sev += 6
    return p, min(sev, 100)


saida = []
for r in D:
    probs, sev = diagnosticar(r)
    saida.append({**r, "problemas": probs, "severidade": sev})
saida.sort(key=lambda x: -x["severidade"])
json.dump(saida, open("prospeccao/odonto-DF/data/diagnostico-digital.json", "w"),
          ensure_ascii=False, indent=1)

print(f"{'clínica':38} {'sev':>4}  {'site':>5} {'IG':>4} problemas")
for r in saida:
    print(f"  {r['nome'][:36]:38} {r['severidade']:4}  "
          f"{'sim' if r.get('site_url') else 'NÃO':>5} {'sim' if r.get('instagram') else 'NÃO':>4} "
          f"{len(r['problemas'])}")

n_sem_site = sum(1 for r in saida if not r.get("site_url"))
n_sem_ig = sum(1 for r in saida if not r.get("instagram"))
n_sem_gtm = sum(1 for r in saida if r.get("site_url") and not r.get("gtm"))
n_ads = sum(1 for r in saida if r.get("fb_pixel") or r.get("google_ads"))
print(f"\nsem site próprio: {n_sem_site}/30 | sem Instagram: {n_sem_ig}/30 | "
      f"site sem analytics: {n_sem_gtm} | com pixel de anúncio: {n_ads}")
