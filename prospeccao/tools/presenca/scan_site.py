#!/usr/bin/env python3
"""
Vertente TECNOLOGIA: audita o site de uma clínica a partir da URL conhecida.

Sem buscador no meio — foi o buscador que derrubou a tentativa anterior. Recebe a
URL, mede, e relata falha como falha (nunca como "não tem site").
"""
import json, re, ssl, sys, time, urllib.error, urllib.parse, urllib.request

ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
      "Accept-Language": "pt-BR,pt;q=0.9"}


def pegar(url, timeout=25):
    t0 = time.time()
    req = urllib.request.Request(url, headers=UA)
    r = urllib.request.urlopen(req, timeout=timeout, context=ctx)
    corpo = r.read(1_200_000)
    return {"url_final": r.geturl(), "status": r.status,
            "ttfb": round(time.time() - t0, 3), "bytes": len(corpo),
            "html": corpo.decode("utf-8", "replace"), "headers": dict(r.headers)}


def auditar(url):
    out = {"site": url}
    try:
        d = pegar(url)
    except urllib.error.HTTPError as e:
        return {**out, "httpStatus": e.code, "erro": f"HTTP {e.code}"}
    except Exception as e:
        return {**out, "httpStatus": 0, "erro": f"{type(e).__name__}: {e}"}

    h, hl = d["html"], d["html"].lower()
    tem = lambda p: bool(re.search(p, hl))
    title = re.search(r"<title[^>]*>(.*?)</title>", h, re.S | re.I)
    desc = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']*)', h, re.I)
    gen = re.search(r'<meta[^>]+name=["\']generator["\'][^>]+content=["\']([^"\']*)', h, re.I)

    cms = None
    for pat, nome in [(r"wp-content|wp-includes", "WordPress"), (r"cdn\.shopify", "Shopify"),
                      (r"wix\.com|wixstatic", "Wix"), (r"squarespace", "Squarespace"),
                      (r"webflow", "Webflow"), (r"elementor", "WordPress + Elementor")]:
        if tem(pat): cms = nome
    if gen and not cms: cms = gen.group(1)

    out.update({
        "httpStatus": d["status"], "urlFinal": d["url_final"],
        "https": d["url_final"].startswith("https://"),
        "ttfbSegundos": d["ttfb"], "tamanhoBytes": d["bytes"], "cms": cms,
        "titulo": (title.group(1).strip()[:140] if title else None),
        "metaDescription": (desc.group(1).strip()[:200] if desc else None),
        "viewportMobile": tem(r'name=["\']viewport'),
        "h1": len(re.findall(r"<h1[\s>]", hl)),
        "openGraph": tem(r'property=["\']og:'),
        "jsonLdLocalBusiness": tem(r'"@type"\s*:\s*"(dentist|localbusiness|medicalbusiness|medicalclinic|dentalclinic)'),
        "formulario": tem(r"<form"),
        "whatsappNoSite": tem(r"wa\.me|api\.whatsapp|whatsapp"),
        "agendamentoOnline": tem(r"agendar|agende|marcar consulta|agendamento|book"),
        "avisoCookies": tem(r"cookie|lgpd"),
        # rastros de anúncio -> alimentam a vertente de tráfego
        "pixelMeta": tem(r"connect\.facebook\.net|fbq\("),
        "pixelGoogleAds": tem(r"googleadservices|/aw-|gtag/js\?id=aw-"),
        "gtm": tem(r"googletagmanager\.com/gtm"),
        "ga4": tem(r"gtag/js\?id=g-|googletagmanager\.com/gtag"),
    })

    # sitemap e resíduo de CMS
    base = f"{urllib.parse.urlparse(d['url_final']).scheme}://{urllib.parse.urlparse(d['url_final']).netloc}"
    for caminho in ("/sitemap.xml", "/wp-sitemap.xml", "/sitemap_index.xml"):
        try:
            s = pegar(base + caminho, 15)
            if s["status"] == 200 and "<" in s["html"]:
                locs = re.findall(r"<loc>([^<]+)</loc>", s["html"])
                # sitemap index: os <loc> apontam para outros sitemaps, nao para paginas
                if "<sitemapindex" in s["html"].lower():
                    paginas = []
                    for sub in locs[:8]:
                        try:
                            ss = pegar(sub, 15)
                            paginas += re.findall(r"<loc>([^<]+)</loc>", ss["html"])
                        except Exception:
                            continue
                        time.sleep(0.4)
                    locs = paginas
                out["sitemap"] = base + caminho
                out["paginasReais"] = locs[:60]
                out["residuoCMS"] = [l for l in locs
                                     if re.search(r"hello-world|sample-page|uncategorized|/\?p=", l)]
                break
        except Exception:
            continue
    out.setdefault("sitemap", None); out.setdefault("paginasReais", [])
    out.setdefault("residuoCMS", [])
    return out


def propensao_bot(t):
    """Sinais de que um atendente de IA no WhatsApp resolveria dor real."""
    sinais, nota = [], 0
    if not t.get("agendamentoOnline"):
        sinais.append("sem agendamento online: toda marcação passa por atendente humano"); nota += 30
    if t.get("whatsappNoSite"):
        sinais.append("WhatsApp já é canal declarado — o volume existe, falta automatizar"); nota += 25
    else:
        sinais.append("WhatsApp não aparece no site: canal principal do setor está fora da jornada"); nota += 20
    if t.get("formulario") and not t.get("whatsappNoSite"):
        sinais.append("captação só por formulário, que responde em horas em vez de segundos"); nota += 15
    if not t.get("https"):
        sinais.append("site sem HTTPS reduz confiança justamente na hora de deixar contato"); nota += 10
    return {"nota": min(nota, 100), "sinais": sinais}


if __name__ == "__main__":
    r = auditar(sys.argv[1])
    if "erro" not in r:
        r["propensaoBot"] = propensao_bot(r)
    print(json.dumps(r, ensure_ascii=False, indent=1))
