#!/usr/bin/env python3
"""
Propensão estrutural a fechar contrato com a Oráculo.

ATENÇÃO AO QUE ISTO NÃO É: não é probabilidade de fechamento. Os eixos `dor` e
`gatilho` do playbook estão NULL (estágio 2 bloqueado por falta da chave do Places).
O que se mede aqui é "quem pode pagar, tem margem para pagar e decide rápido" —
pré-qualificação, não intenção de compra. A ordem do topo muda quando o Places
e o Instagram entrarem.

Cada componente é rotulado [medido] ou [hipótese].
"""
import re, sqlite3, sys, unicodedata

DB = sys.argv[1] if len(sys.argv) > 1 else "prospeccao/odonto-DF/leads.db"

# Renda da região de captação → teto de ticket que a clínica consegue cobrar
TIER_A = {"LAGO SUL","LAGO NORTE","ASA SUL","ASA NORTE","SUDOESTE","NOROESTE","PARK WAY",
          "OCTOGONAL","JARDIM BOTANICO","VICENTE PIRES","AGUAS CLARAS","SUDOESTE/OCTOGONAL"}
TIER_B = {"TAGUATINGA","GUARA","CRUZEIRO","SOBRADINHO","NUCLEO BANDEIRANTE","RIACHO FUNDO",
          "GAMA","PLANALTINA","SAMAMBAIA"}

ALTO_TICKET = r"IMPLANT|ORTODON|ORTHO|ALINHAD|INVISALIGN|ESTETIC|HARMONIZ|FACETA|LENTE|OROFACIAL"
ESPECIALIZ  = r"ESPECIALIZ|CENTRO ODONT|INSTITUTO|CLINICA ODONT"
BAIXO_TICKET = r"POPULAR|CONVENIO|LOW COST|ACESS[IÍ]VEL|SOCIAL"


def sem_acento(s):
    return unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().upper()


def tier_regiao(bairro):
    b = sem_acento(bairro)
    if any(t in b for t in TIER_A): return "A", 1.00
    if any(t in b for t in TIER_B): return "B", 0.55
    return "C", 0.25


def avaliar(r):
    txt = sem_acento(f"{r['nome_fantasia'] or ''} {r['razao_social'] or ''}")
    comp, notas = {}, []

    # [medido] capacidade de pagar — já calculada pelo pipeline a partir do CNPJ
    comp["capacidade"] = (r["capacidade"] or 0.0, 0.40)

    # [medido] fit de ticket: especialidade de alto valor no nome
    if re.search(BAIXO_TICKET, txt):
        fit = 0.10; notas.append("nome sinaliza modelo popular/convênio (margem baixa)")
    elif re.search(ALTO_TICKET, txt):
        fit = 1.00; notas.append("especialidade de alto ticket no nome")
    elif re.search(ESPECIALIZ, txt):
        fit = 0.60; notas.append("posicionamento de clínica especializada")
    else:
        fit = 0.35
    comp["fit_ticket"] = (fit, 0.20)

    # [medido] poder aquisitivo da região de captação
    tier, v = tier_regiao(r["bairro"])
    comp["regiao"] = (v, 0.15)
    if tier == "A": notas.append(f"região de renda alta ({r['bairro']})")

    # [medido] agilidade de decisão: sociedade pequena/média decide rápido
    nj = sem_acento(r["natureza_juridica_desc"])
    un = r["n_unidades_df"] or 1
    if un >= 4:
        dec = 0.45; notas.append(f"{un} unidades — decisão possivelmente centralizada")
    elif un >= 2:
        dec = 0.90; notas.append(f"{un} unidades — precisa de padronização de marca")
    elif "INDIVIDUAL" in nj:
        dec = 0.75; notas.append("empresário individual — decide sozinho, verba menor")
    else:
        dec = 1.00
    comp["decisao"] = (dec, 0.10)

    # [HIPÓTESE] defasagem digital presumida pela maturidade.
    # Clínica madura cresceu na indicação boca a boca e costuma ter presença digital
    # atrasada. NÃO É MEDIÇÃO — só o Places/Instagram confirma.
    m = r["idade_meses"] or 0
    if 120 <= m < 300:
        dig = 1.00; notas.append("10–25 anos: perfil clássico de presença digital defasada [hipótese]")
    elif m >= 300:
        dig = 0.70; notas.append("25+ anos: consolidada, pode resistir a marketing digital [hipótese]")
    elif m >= 60:
        dig = 0.55
    else:
        dig = 0.35
    comp["digital_presumida"] = (dig, 0.15)

    score = sum(v * p for v, p in comp.values())
    return round(score, 4), comp, notas


con = sqlite3.connect(DB); con.row_factory = sqlite3.Row
con.execute("DROP TABLE IF EXISTS propensao")
con.execute("""CREATE TABLE propensao (
    cnpj TEXT PRIMARY KEY, propensao REAL, capacidade REAL, fit_ticket REAL,
    regiao REAL, decisao REAL, digital_presumida REAL, tier_regiao TEXT, motivos TEXT)""")

rows = con.execute("SELECT * FROM leads WHERE desqualificado=0").fetchall()
for r in rows:
    s, c, n = avaliar(r)
    con.execute("INSERT INTO propensao VALUES (?,?,?,?,?,?,?,?,?)",
                (r["cnpj"], s, c["capacidade"][0], c["fit_ticket"][0], c["regiao"][0],
                 c["decisao"][0], c["digital_presumida"][0], tier_regiao(r["bairro"])[0],
                 " | ".join(n)))
con.commit()

print(f"pontuados: {len(rows)}")
print("\n=== distribuição ===")
for lo, hi, rot in [(.75,1.01,"A  >=0,75  atacar primeiro"), (.65,.75,"B  0,65–0,75"),
                    (.55,.65,"C  0,55–0,65"), (0,.55,"D  <0,55")]:
    n = con.execute("SELECT COUNT(*) FROM propensao WHERE propensao>=? AND propensao<?", (lo,hi)).fetchone()[0]
    print(f"  {rot:32} {n:5}")
