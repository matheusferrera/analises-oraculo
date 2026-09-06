#!/usr/bin/env python3
"""Cria a pasta e o presenca.json semeado de cada uma das 15 clínicas."""
import csv, json, re, sqlite3, sys, unicodedata, pathlib, copy
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from schema import MODELO

RAIZ = pathlib.Path("prospeccao/odonto-DF/analises")
QUAL = {"49": "Sócio-Administrador", "22": "Sócio", "65": "Titular", "05": "Administrador"}
PORTE = {"1": "ME", "3": "EPP", "5": "DEMAIS"}

# site/instagram já confirmados por busca manual (18/08). "" = não localizado.
CONHECIDO = {
 "renove-estetica-e-implantes-orais":      ("", ""),
 "implantomed":                            ("https://www.implantomed.com.br/", "implantomed"),
 "vital-implantes-e-tratamentos-dentarios":("https://www.vitalimplantes.com.br/", "vitalimplantes"),
 "osteo-implante":                         ("https://osteoimplante.com.br/", ""),
 "patricia-pizzo-ortodontia":              ("https://patriciapizzo.com.br/", "odontopatriciapizzo"),
 "instituto-de-ortodontia-machado-e-audicao": ("", ""),
 "everface-odontologia-especializada":     ("", "everface_odontologia"),
 "orthos-taguatinga":                      ("", "orthosbrasilia"),
 "fabula-odontopediatria-e-ortodontia":    ("https://fabulaodonto.com.br/", "fabulaodonto"),
 "faces-odontologia-estetica-ltda":        ("", "facesodontologia"),
 "ibi-instituto-brasiliense-de-implantodontia": ("", ""),
 "crie-odontologia":                       ("https://www.crieodontologia.com.br/", "crieodontologia"),
 "sallum-odontologia-estetica":            ("https://www.sallumodontologia.com.br/", "sallumodontologia"),
 "claudio-pinho-odontologia":              ("http://www.drclaudiopinho.com.br/", ""),
 "wv-implantodontia":                      ("", ""),
}
IG_PESSOAL = {"claudio-pinho-odontologia": "claudio_pinho"}


def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s)).strip("-")


socios = {}
for r in csv.DictReader(open("/tmp/socios.csv")):
    socios.setdefault(r["cnpj_basico"], []).append((r["nome"].title(), r["qualificacao"]))

contatos = {}
for r in csv.DictReader(open("prospeccao/odonto-DF/contatos.csv")):
    contatos[r["nome"]] = r

con = sqlite3.connect("prospeccao/odonto-DF/leads.db"); con.row_factory = sqlite3.Row
rows = con.execute("""SELECT l.*, p.propensao FROM leads l JOIN propensao p USING(cnpj)
                      WHERE l.desqualificado=0 ORDER BY p.propensao DESC LIMIT 15""").fetchall()

for i, r in enumerate(rows, 1):
    nome = r["nome_fantasia"] or r["razao_social"]
    sl = slug(nome)
    d = copy.deepcopy(MODELO)
    d["cnpj"] = r["cnpj_formatado"]; d["slug"] = sl
    d["clinica"].update({
        "nome": nome.title(), "razaoSocial": r["razao_social"].title(),
        "cnaeDescricao": r["cnae_descricao"], "fundacao": r["data_inicio_atividade"],
        "idadeAnos": (r["idade_meses"] or 0)//12, "porte": PORTE.get(r["porte"], "?"),
        "regiao": (r["bairro"] or "").title(), "endereco": r["endereco"],
        "unidades": r["n_unidades_df"]})
    s = socios.get(r["cnpj_basico"], [])
    admins = [x for x in s if x[1] == "49"] or s
    if admins:
        d["decisor"].update({"nome": admins[0][0],
                             "qualificacao": QUAL.get(admins[0][1], admins[0][1]),
                             "decisaoCompartilhada": len(admins) > 1})
    c = contatos.get(nome)
    if c:
        d["decisor"].update({"telefone": c["tel_1"] or c["tel_2"],
                             "telefoneTipo": c["tel_1_tipo"] or c["tel_2_tipo"],
                             "whatsapp": c["tel_1_whatsapp"] or c["tel_2_whatsapp"],
                             "email": c["email"] or None})
    site, ig = CONHECIDO.get(sl, ("", ""))
    d["tecnologia"]["site"] = site or None
    d["instagram"]["handle"] = ig or None
    d["decisor"]["instagramPessoal"] = IG_PESSOAL.get(sl)
    d["fontes"] = ["Receita Federal via BigQuery basedosdados.br_me_cnpj (snapshot 2026-01-11)",
                   "Quadro societário (tabela socios, mesmo snapshot)"]
    d["limitacoes"] = ["Coleta de Google, Instagram, site e anúncios pendente"]

    p = RAIZ / f"{i:02d}-{sl}" / "data"
    p.mkdir(parents=True, exist_ok=True)
    (p / "presenca.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"  {i:02d} {sl:46} decisor={d['decisor']['nome'] or '—'}")

print(f"\n{len(rows)} pastas semeadas em {RAIZ}")
