#!/usr/bin/env python3
"""
Varredura digital leve dos leads: site, SEO, rastros de anúncio e Instagram.

Tudo aqui é sinal público de página. Não substitui o estágio 2 (Places/Ad Library),
mas cobre site, SEO técnico e presença de pixel de anúncio sem nenhuma chave de API.
"""
import csv, json, re, ssl, sqlite3, sys, time, urllib.parse, urllib.request

ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"}

# agregadores e diretórios: aparecer só neles é sintoma, não é site próprio
DIRETORIOS = re.compile(r"guiasaudebrasil|databrasil|cnpj|econodata|solutudo|apontador|telelistas|"
                        r"hotfrog|doctoralia|boaconsulta|guiamais|encontra|listadeempresas|"
                        r"consultacnpj|empresascnpj|linkedin|facebook|instagram|youtube|twitter|"
                        r"tiktok|booking|ifood|google|maps|wikipedia|reclameaqui|gov\.br|jusbrasil")


def buscar(q, n=8):
    url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(q)
    try:
        h = urllib.request.urlopen(urllib.request.Request(url, headers=UA),
                                   timeout=20, context=ctx).read().decode("utf-8", "replace")
        vistos, out = set(), []
        for l in re.findall(r'uddg=([^&"]+)', h):
            u = urllib.parse.unquote(l)
            d = urllib.parse.urlparse(u).netloc.lower()
            if d and d not in vistos:
                vistos.add(d); out.append(u)
        return out[:n]
    except Exception:
        return []


def baixar(url):
    try:
        t0 = time.time()
        r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25, context=ctx)
        html = r.read(600_000).decode("utf-8", "replace")
        return {"url": r.geturl(), "status": r.status, "ms": int((time.time()-t0)*1000), "html": html}
    except Exception as e:
        return {"url": url, "status": 0, "erro": f"{type(e).__name__}", "html": ""}


def analisar_site(d):
    h = d["html"]; hl = h.lower()
    def acha(p): return bool(re.search(p, hl))
    title = (re.search(r"<title[^>]*>(.*?)</title>", h, re.S | re.I) or [None, ""])[1].strip()[:120]
    desc = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']*)', h, re.I)
    return {
        "site_url": d["url"], "status": d["status"], "ms": d.get("ms", 0),
        "https": d["url"].startswith("https"),
        "title": title, "title_len": len(title),
        "meta_desc": (desc.group(1).strip()[:160] if desc else ""),
        "h1": len(re.findall(r"<h1[\s>]", hl)),
        "viewport": acha(r'name=["\']viewport'),
        "schema_local": acha(r'"@type"\s*:\s*"(dentist|localbusiness|medicalbusiness|medicalclinic)'),
        "gtm": acha(r"googletagmanager\.com|gtag\(|google-analytics"),
        "fb_pixel": acha(r"connect\.facebook\.net|fbq\("),
        "google_ads": acha(r"googleadservices|aw-\d|gtag/js\?id=aw-"),
        "whatsapp": acha(r"wa\.me|api\.whatsapp|whatsapp"),
        "agendamento": acha(r"agende|agendar|marcar consulta|agendamento|booking"),
        "instagram": (re.search(r"instagram\.com/([A-Za-z0-9_.]{2,30})", h) or [None, ""])[1],
    }


def escolher_site(urls, nome):
    for u in urls:
        d = urllib.parse.urlparse(u).netloc.lower()
        if not DIRETORIOS.search(d):
            return u
    return ""


def instagram_de(urls):
    for u in urls:
        m = re.search(r"instagram\.com/([A-Za-z0-9_.]{2,30})", u)
        if m and m.group(1).lower() not in ("p", "reel", "explore", "accounts"):
            return m.group(1)
    return ""


con = sqlite3.connect("prospeccao/odonto-DF/leads.db"); con.row_factory = sqlite3.Row
alvos = con.execute("""SELECT l.cnpj_basico, COALESCE(NULLIF(l.nome_fantasia,''),l.razao_social) nome,
    l.bairro, p.propensao FROM leads l JOIN propensao p USING(cnpj)
    WHERE l.desqualificado=0 ORDER BY p.propensao DESC LIMIT 30""").fetchall()

socios = {}
for r in csv.DictReader(open("/tmp/socios.csv")):
    if r["qualificacao"] == "49":
        socios.setdefault(r["cnpj_basico"], []).append(r["nome"].title())

res = []
for i, a in enumerate(alvos, 1):
    nome = a["nome"]
    print(f"[{i}/30] {nome[:45]}", flush=True)
    urls = buscar(f"{nome} Brasília odontologia"); time.sleep(2.5)
    site = escolher_site(urls, nome)
    reg = {"nome": nome, "bairro": a["bairro"], "propensao": a["propensao"],
           "cnpj_basico": a["cnpj_basico"],
           "socio": (socios.get(a["cnpj_basico"], [""]) or [""])[0],
           "so_diretorio": bool(urls) and not site}
    reg.update({k: "" for k in ("site_url", "title", "meta_desc")})
    if site:
        reg.update(analisar_site(baixar(site))); time.sleep(1.5)

    ig = reg.get("instagram") or instagram_de(urls)
    if not ig:
        u2 = buscar(f"{nome} Brasília instagram", 6); time.sleep(2.5)
        ig = instagram_de(u2)
    reg["instagram"] = ig

    ig_socio = ""
    if reg["socio"]:
        u3 = buscar(f'"{reg["socio"]}" dentista Brasília instagram', 6); time.sleep(2.5)
        cand = instagram_de(u3)
        if cand and cand.lower() != (ig or "").lower():
            ig_socio = cand
    reg["instagram_socio"] = ig_socio
    res.append(reg)

json.dump(res, open("prospeccao/odonto-DF/data/scan-digital.json", "w"), ensure_ascii=False, indent=1)
print(f"\nOK: {len(res)} escaneados -> prospeccao/odonto-DF/data/scan-digital.json")
