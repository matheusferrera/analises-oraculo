#!/usr/bin/env python3
"""Roda a vertente tecnologia nas 15 e grava em cada presenca.json."""
import json, pathlib, sys, time
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scan_site import auditar, propensao_bot

RAIZ = pathlib.Path("prospeccao/odonto-DF/analises")
for pasta in sorted(RAIZ.iterdir()):
    fp = pasta / "data" / "presenca.json"
    if not fp.exists(): continue
    d = json.loads(fp.read_text(encoding="utf-8"))
    url = d["tecnologia"].get("site")
    nome = d["clinica"]["nome"]
    if not url:
        d["limitacoes"] = [x for x in d["limitacoes"] if "site" not in x.lower()]
        d["limitacoes"].append("Nenhum site proprio localizado por busca web — CONFIRMAR no Chrome antes de afirmar ausencia")
        print(f"  {nome[:38]:40} sem site conhecido -> marcado para conferencia")
    else:
        r = auditar(url)
        if "erro" in r:
            d["tecnologia"].update({"site": url, "httpStatus": r.get("httpStatus"),
                                    "erroColeta": r["erro"]})
            d["limitacoes"].append(f"Site {url} nao respondeu a clientes HTTP ({r['erro']}) — CONFIRMAR no Chrome")
            print(f"  {nome[:38]:40} FALHA: {r['erro'][:52]}")
        else:
            r["propensaoBot"] = propensao_bot(r)
            d["tecnologia"].update(r)
            d["fontes"].append(f"Coleta HTTP direta de {r['urlFinal']}")
            marcas = []
            if not r["https"]: marcas.append("sem HTTPS")
            if not r["jsonLdLocalBusiness"]: marcas.append("sem schema local")
            if not (r["gtm"] or r["ga4"]): marcas.append("sem analytics")
            if not (r["pixelMeta"] or r["pixelGoogleAds"]): marcas.append("sem pixel de anuncio")
            print(f"  {nome[:38]:40} {r['httpStatus']} {r['ttfbSegundos']}s "
                  f"{(r['cms'] or '?')[:20]:22} {', '.join(marcas) or 'ok'}")
        time.sleep(1.5)
    d["limitacoes"] = sorted(set(d["limitacoes"]))
    fp.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
