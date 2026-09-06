#!/usr/bin/env python3
"""
Normaliza os telefones da base da Receita para discagem e WhatsApp.

Dois problemas na origem:
  1. Celulares gravados no formato antigo de 8 dígitos, anteriores ao nono dígito.
     Não completam a ligação. Aqui recebem o 9 na frente — marcado em `corrigido`.
  2. O telefone é o do momento do registro do CNPJ e pode estar velho. Trate como
     ponto de partida, não como verdade.
"""
import csv, re, sqlite3, sys

DB = sys.argv[1] if len(sys.argv) > 1 else "prospeccao/odonto-DF/leads.db"


def classificar(bruto):
    """-> (formatado, e164, tipo, corrigido)"""
    d = re.sub(r"\D", "", bruto or "")
    if not d:
        return "", "", "", False
    ddd, num = (d[:2], d[2:]) if len(d) >= 10 else ("61", d)
    corrigido = False
    if len(num) == 8 and num[0] in "6789":      # celular antigo -> ganha o nono dígito
        num, corrigido = "9" + num, True
    if len(num) == 9 and num[0] == "9":
        tipo = "celular"
        fmt = f"({ddd}) {num[0]} {num[1:5]}-{num[5:]}"
    elif len(num) == 8:
        tipo = "fixo"
        fmt = f"({ddd}) {num[:4]}-{num[4:]}"
    else:
        return f"({ddd}) {num}", "", "indefinido", corrigido
    return fmt, f"+55{ddd}{num}", tipo, corrigido


def exportar():
    con = sqlite3.connect(DB); con.row_factory = sqlite3.Row
    rows = con.execute("""SELECT p.propensao, COALESCE(NULLIF(l.nome_fantasia,''),l.razao_social) nome,
        l.cnpj_formatado, l.porte, l.bairro, l.idade_meses/12 idade, l.n_unidades_df un,
        l.capital_social, l.telefone, l.telefone_2, l.email, a.arquetipo, l.endereco
        FROM leads l JOIN propensao p USING(cnpj) JOIN arquetipo a USING(cnpj)
        WHERE l.desqualificado=0 ORDER BY p.propensao DESC""").fetchall()
    
    PORTE = {"1": "ME", "3": "EPP", "5": "DEMAIS"}
    saida = "prospeccao/odonto-DF/contatos.csv"
    stats = {"celular": 0, "fixo": 0, "indefinido": 0, "sem": 0, "corrigidos": 0}
    
    with open(saida, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["propensao", "nome", "cnpj", "porte", "bairro", "endereco", "idade_anos",
                    "unidades", "arquetipo", "tel_1", "tel_1_tipo", "tel_1_whatsapp",
                    "tel_1_corrigido", "tel_2", "tel_2_tipo", "tel_2_whatsapp", "email"])
        for r in rows:
            f1, e1, t1, c1 = classificar(r["telefone"])
            f2, e2, t2, _ = classificar(r["telefone_2"])
            if not f1 and not f2:
                stats["sem"] += 1
            else:
                stats[t1 or t2] = stats.get(t1 or t2, 0) + 1
            stats["corrigidos"] += c1
            w.writerow([f"{r['propensao']:.4f}", r["nome"], r["cnpj_formatado"],
                        PORTE.get(r["porte"], "?"), r["bairro"], r["endereco"], r["idade"],
                        r["un"], r["arquetipo"], f1, t1, e1, "sim" if c1 else "",
                        f2, t2, e2, r["email"] or ""])
    
    print(f"{saida}: {len(rows)} linhas")
    for k, v in stats.items():
        print(f"  {k:12} {v}")


if __name__ == "__main__":
    exportar()
