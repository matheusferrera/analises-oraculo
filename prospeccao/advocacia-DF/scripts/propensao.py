#!/usr/bin/env python3
"""Propensão estrutural da advocacia-DF. Capacidade já vem do build_db (sócios manda)."""
import sqlite3, unicodedata, pathlib

DB = pathlib.Path("prospeccao/advocacia-DF/leads.db")
# renda da regiao: em advocacia isso e proxy do cliente que o escritorio atende
TIER_A = {"LAGO SUL","LAGO NORTE","SETOR DE HABITACOES INDIVIDUAIS","SHIS","ASA SUL","ASA NORTE",
          "SUDOESTE","NOROESTE","PARK WAY","SETOR COMERCIAL SUL","ST COML NORTE","SETOR COMERCIAL NORTE",
          "SETOR BANCARIO SUL","SETOR BANCARIO NORTE","SETOR HOTELEIRO SUL","SETOR DE AUTARQUIAS SUL",
          "ST DE HABITACOES INDIVIDUAIS SUL","SETOR DE RADIO E TV SUL","SETOR DE INDUSTRIAS GRAFICAS"}
TIER_B = {"AGUAS CLARAS","TAGUATINGA","GUARA","CRUZEIRO","OCTOGONAL","SUDOESTE/OCTOGONAL","ZONA INDUSTRIAL"}
sa = lambda s: unicodedata.normalize("NFKD", s or "").encode("ascii","ignore").decode().upper()

con = sqlite3.connect(DB); con.row_factory = sqlite3.Row
con.execute("DROP TABLE IF EXISTS propensao")
con.execute("""CREATE TABLE propensao (cnpj_basico TEXT PRIMARY KEY, propensao REAL,
               capacidade REAL, regiao REAL, decisao REAL, tier TEXT, motivos TEXT)""")

for r in con.execute("SELECT * FROM leads WHERE desqualificado=0").fetchall():
    b = sa(r["bairro"])
    if any(t in b for t in TIER_A): tier, reg = "A", 1.00
    elif any(t in b for t in TIER_B): tier, reg = "B", 0.60
    else: tier, reg = "C", 0.30

    ns, na = r["n_socios"] or 0, r["n_administradores"] or 0
    motivos = []
    # decisao: 2 a 5 socios decide rapido; muitos socios vira comite
    if ns <= 1: dec = 0.80
    elif ns <= 5: dec = 1.00; motivos.append("sociedade enxuta, decisão rápida")
    elif ns <= 12: dec = 0.85
    elif ns <= 25: dec = 0.65; motivos.append("decisão provavelmente colegiada")
    else: dec = 0.45; motivos.append("comitê de sócios: ciclo de venda longo")
    if tier == "A": motivos.append(f"endereço de alta renda ({r['bairro']})")
    if (r["n_unidades_df"] or 1) > 1: motivos.append(f"{r['n_unidades_df']} unidades")
    if r["idade_meses"] and r["idade_meses"] >= 240:
        motivos.append(f"{r['idade_meses']//12} anos: reputação consolidada, digital provavelmente atrasado")

    p = round(r["capacidade"] * (0.45 + 0.35*reg + 0.20*dec), 4)
    con.execute("INSERT INTO propensao VALUES (?,?,?,?,?,?,?)",
                (r["cnpj_basico"], p, r["capacidade"], reg, dec, tier, " · ".join(motivos)))
con.commit()

print("distribuição:")
for lo, hi, rot in [(.60,1.01,"A  >=0,60"),(.48,.60,"B  0,48-0,60"),(.35,.48,"C  0,35-0,48"),(0,.35,"D  <0,35")]:
    n = con.execute("SELECT COUNT(*) FROM propensao WHERE propensao>=? AND propensao<?", (lo,hi)).fetchone()[0]
    print(f"  {rot:16} {n:5}")
