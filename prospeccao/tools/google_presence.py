#!/usr/bin/env python3
"""
Cruza os leads do CNPJ com o Google Places (API New) em dois passes separados.

    presenca  -> "tem ficha no Google?"           SKU Pro         5.000 grátis/mês
    metricas  -> nota + volume de avaliações      SKU Enterprise  1.000 grátis/mês

Os passes são separados de propósito: pedir `rating`/`userRatingCount` promove a
chamada inteira ao SKU Enterprise. Rodar tudo junto nos ~3.600 leads de odonto-DF
custaria ~US$126; separado, os dois cabem na cota gratuita.

Casamento em duas chaves: telefone (decisivo — também é campo Pro, sai de graça no
pass barato) e, como desempate, similaridade de nome. Sem telefone o falso negativo
sobe muito, porque a razão social raramente é o nome da fachada.

Uso:
    export GOOGLE_PLACES_API_KEY=...
    python3 prospeccao/tools/google_presence.py presenca --db prospeccao/odonto-DF/leads.db
    python3 prospeccao/tools/google_presence.py metricas --db prospeccao/odonto-DF/leads.db --top 600

Resumível: relê o que já foi consultado e continua de onde parou.
"""
import argparse, json, os, re, sqlite3, sys, time, unicodedata, urllib.error, urllib.request

ENDPOINT = "https://places.googleapis.com/v1/places:searchText"

# Máscaras por SKU — NÃO misture. Ver docstring.
CAMPOS_PRESENCA = ("places.id,places.displayName,places.formattedAddress,"
                   "places.businessStatus,places.nationalPhoneNumber")
CAMPOS_METRICAS = ("places.id,places.rating,places.userRatingCount,"
                   "places.websiteUri,places.nationalPhoneNumber")

CUSTO = {"presenca": (5000, 32.0), "metricas": (1000, 35.0)}  # (grátis/mês, US$/1000)
LIMIAR_NOME = 0.34


def normalizar(s):
    if not s:
        return ""
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-z0-9 ]", " ", s.lower())
    # ruído societário que atrapalha o casamento com o nome de fachada
    s = re.sub(r"\b(ltda|me|epp|eireli|sa|s a|cia|comercio|servicos)\b", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def similaridade(a, b):
    """Jaccard sobre tokens. Simples e suficiente para triagem."""
    ta, tb = set(normalizar(a).split()), set(normalizar(b).split())
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def so_digitos(t):
    d = re.sub(r"\D", "", t or "")
    return d[-8:] if len(d) >= 8 else ""   # ignora DDD/DDI, compara o assinante


def consultar(query, campos, chave):
    corpo = {"textQuery": query, "languageCode": "pt-BR",
             "regionCode": "BR", "maxResultCount": 3}
    for tentativa in range(4):
        req = urllib.request.Request(
            ENDPOINT, data=json.dumps(corpo).encode(),
            headers={"Content-Type": "application/json",
                     "X-Goog-Api-Key": chave, "X-Goog-FieldMask": campos})
        try:
            with urllib.request.urlopen(req, timeout=25) as r:
                return json.loads(r.read()).get("places", [])
        except urllib.error.HTTPError as e:
            if e.code == 429 or e.code >= 500:
                time.sleep(2 ** tentativa)
                continue
            sys.stderr.write(f"  HTTP {e.code}: {e.read()[:300].decode(errors='replace')}\n")
            return None
        except Exception:
            time.sleep(2 ** tentativa)
    return None


def preparar(con):
    con.execute("""CREATE TABLE IF NOT EXISTS google_presenca (
        cnpj TEXT PRIMARY KEY, status TEXT, place_id TEXT, nome_google TEXT,
        endereco_google TEXT, business_status TEXT, score_match REAL, casou_por TEXT,
        rating REAL, total_avaliacoes INTEGER, website TEXT, telefone_google TEXT,
        consultado_em TEXT)""")
    con.commit()


def registrar_sinal(con, cnpj, tipo, valor):
    try:
        con.execute("INSERT INTO sinais (lead_id, tipo, valor, fonte, coletado_em) "
                    "VALUES (?,?,?,?,datetime('now'))",
                    (cnpj, tipo, str(valor), "google_places_api"))
    except sqlite3.OperationalError:
        pass  # tabela sinais é criada pelo pipeline principal


def montar_consulta(con, passe, top):
    """O schema do leads.db vem do pipeline principal — não assuma colunas."""
    cols = {r[1] for r in con.execute("PRAGMA table_info(leads)")}
    faltando = {"cnpj", "nome_fantasia", "razao_social"} - cols
    if faltando:
        sys.exit(f"ERRO: leads.db não tem as colunas obrigatórias: {sorted(faltando)}")
    if "telefone" not in cols:
        print("AVISO: leads sem coluna 'telefone' — casamento cai só no nome, "
              "com bem mais falso negativo.", file=sys.stderr)

    opcionais = [c for c in ("bairro", "cep", "municipio", "telefone") if c in cols]
    sel = ", ".join(["l.cnpj", "l.nome_fantasia", "l.razao_social"] + [f"l.{c}" for c in opcionais])
    ordem = "COALESCE(l.score,0) DESC" if "score" in cols else "l.cnpj"
    desq = "COALESCE(l.desqualificado,0)=0 AND " if "desqualificado" in cols else ""

    if passe == "presenca":
        return (f"SELECT {sel} FROM leads l "
                f"LEFT JOIN google_presenca g ON g.cnpj = l.cnpj "
                f"WHERE {desq}g.cnpj IS NULL")
    sql = (f"SELECT {sel} FROM leads l JOIN google_presenca g ON g.cnpj = l.cnpj "
           f"WHERE g.status='encontrado' AND g.total_avaliacoes IS NULL ORDER BY {ordem}")
    return sql + (f" LIMIT {top}" if top else "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("passe", choices=["presenca", "metricas"])
    ap.add_argument("--db", required=True)
    ap.add_argument("--top", type=int, default=0, help="limita aos N melhores (use no pass metricas)")
    ap.add_argument("--rps", type=float, default=8.0, help="requests por segundo")
    ap.add_argument("--dry-run", action="store_true", help="só estima chamadas e custo")
    args = ap.parse_args()

    chave = os.environ.get("GOOGLE_PLACES_API_KEY")
    if not chave and not args.dry_run:
        sys.exit("ERRO: defina GOOGLE_PLACES_API_KEY (ou use --dry-run)")

    con = sqlite3.connect(args.db)
    con.row_factory = sqlite3.Row
    preparar(con)

    leads = con.execute(montar_consulta(con, args.passe, args.top)).fetchall()
    gratis, preco = CUSTO[args.passe]
    excedente = max(0, len(leads) - gratis)
    print(f"pass={args.passe}  leads pendentes={len(leads)}  cota grátis={gratis}")
    print(f"custo estimado: US$ {excedente / 1000 * preco:.2f}" +
          ("  (dentro da cota gratuita)" if not excedente
           else f"  ({excedente} chamadas acima da cota)"))
    if args.dry_run:
        return
    if excedente and input("Excede a cota gratuita. Continuar? [s/N] ").strip().lower() != "s":
        return

    campos = CAMPOS_PRESENCA if args.passe == "presenca" else CAMPOS_METRICAS
    intervalo = 1.0 / args.rps
    achados = ausentes = ambiguos = falhas = 0

    for i, l in enumerate(leads, 1):
        k = l.keys()
        nome = (l["nome_fantasia"] or l["razao_social"] or "").strip()
        if not nome:
            continue
        partes = [nome,
                  l["bairro"] if "bairro" in k else None,
                  (l["municipio"] if "municipio" in k else None) or "Distrito Federal"]
        res = consultar(" ".join(p for p in partes if p), campos, chave)
        agora = time.strftime("%Y-%m-%d %H:%M:%S")

        if res is None:
            falhas += 1
        elif not res:
            ausentes += 1
            con.execute("INSERT OR REPLACE INTO google_presenca "
                        "(cnpj,status,consultado_em) VALUES (?,?,?)",
                        (l["cnpj"], "nao_encontrado", agora))
            registrar_sinal(con, l["cnpj"], "google_ausente", "sem ficha correspondente no Places")
        else:
            tel_rf = so_digitos(l["telefone"] if "telefone" in k else "")

            def nota(p):
                base = similaridade(nome, (p.get("displayName") or {}).get("text", ""))
                # telefone igual é prova de identidade: domina o nome
                if tel_rf and so_digitos(p.get("nationalPhoneNumber")) == tel_rf:
                    return 1.0 + base
                return base

            melhor = max(res, key=nota)
            bruto = nota(melhor)
            casou_tel = bruto >= 1.0
            sc = 1.0 if casou_tel else bruto
            status = "encontrado" if (casou_tel or sc >= LIMIAR_NOME) else "ambiguo"
            achados += status == "encontrado"
            ambiguos += status == "ambiguo"

            if args.passe == "presenca":
                con.execute(
                    "INSERT OR REPLACE INTO google_presenca (cnpj,status,place_id,nome_google,"
                    "endereco_google,business_status,score_match,casou_por,consultado_em) "
                    "VALUES (?,?,?,?,?,?,?,?,?)",
                    (l["cnpj"], status, melhor.get("id"),
                     (melhor.get("displayName") or {}).get("text"),
                     melhor.get("formattedAddress"), melhor.get("businessStatus"),
                     round(sc, 3), "telefone" if casou_tel else "nome", agora))
            else:
                con.execute(
                    "UPDATE google_presenca SET rating=?, total_avaliacoes=?, website=?, "
                    "telefone_google=?, consultado_em=? WHERE cnpj=?",
                    (melhor.get("rating"), melhor.get("userRatingCount"),
                     melhor.get("websiteUri"), melhor.get("nationalPhoneNumber"),
                     agora, l["cnpj"]))
                registrar_sinal(con, l["cnpj"], "google_avaliacoes", melhor.get("userRatingCount"))

        if i % 50 == 0:
            con.commit()
            print(f"  {i}/{len(leads)}  encontrados={achados} ausentes={ausentes} "
                  f"ambíguos={ambiguos} falhas={falhas}")
        time.sleep(intervalo)

    con.commit()
    print(f"\nFIM: encontrados={achados}  NÃO ENCONTRADOS={ausentes}  "
          f"ambíguos={ambiguos}  falhas={falhas}")
    print("\nATENÇÃO: 'não encontrado' NÃO é o mesmo que 'não tem Google'. Nome de fachada\n"
          "diferente da razão social e nome_fantasia vazio na base da Receita geram falso\n"
          "negativo. Confira ~20 à mão antes de tratar o número como definitivo.\n"
          "Veja a coluna casou_por: quem casou por 'nome' é menos confiável que por 'telefone'.")


if __name__ == "__main__":
    main()
