#!/usr/bin/env python3
"""
Contrato de dados do relatório de presença digital (odonto DF).

Baseado em DrAdrianoBorges/data/presenca-digital-20260817.json — o schema mais
maduro do repo, único com `notaGeral.pilares` estruturado — e estendido com as
quatro vertentes comerciais da Oráculo.

REGRA INEGOCIÁVEL: campo não coletado fica None e entra em `limitacoes`.
Nunca preencher por inferência. Um número sem origem é ficção.
"""

# Cada pilar vira uma barra no score-grid do relatório e uma linha no MD final.
PILARES = ["google", "site", "instagram", "cadencia", "reputacaoEDiretorios", "conversao"]

# Vertente comercial que cada achado alimenta — é o elo com a proposta
# (a p.1 da Proposta-Comercial tem coluna "Vertente" ligando achado -> contrato).
VERTENTES = {
    "tecnologia": "Site próprio, ficha do Google e atendente de IA no WhatsApp",
    "social": "Gestão de redes sociais",
    "trafego": "Tráfego pago (Google Ads + Meta Ads)",
}

MODELO = {
    "coletadoEm": None,                     # YYYY-MM-DD
    "cnpj": None, "slug": None,
    "clinica": {
        "nome": None, "razaoSocial": None, "cnaeDescricao": None,
        "fundacao": None, "idadeAnos": None, "porte": None,
        "regiao": None, "endereco": None, "unidades": None,
    },
    "decisor": {
        "nome": None, "qualificacao": None, "decisaoCompartilhada": None,
        "telefone": None, "telefoneTipo": None, "whatsapp": None,
        "email": None, "instagramPessoal": None,
    },
    # VERTENTE 1 — tecnologia
    "tecnologia": {
        "site": None, "httpStatus": None, "cms": None, "https": None,
        "ttfbSegundos": None, "tempoTotalSegundos": None, "tamanhoBytes": None,
        "viewportMobile": None, "h1": None, "metaDescription": None,
        "openGraph": None, "jsonLdLocalBusiness": None,
        "sitemap": None, "paginasReais": [], "residuoCMS": [],
        "formulario": None, "whatsappNoSite": None, "agendamentoOnline": None,
        "avisoCookies": None, "dominiosDuplicados": [],
        "propensaoBot": {"nota": None, "sinais": []},
    },
    # VERTENTE 2 — gestão de redes sociais
    "instagram": {
        "handle": None, "uid": None, "seguidores": None, "seguindo": None,
        "publicacoesTotal": None, "amostraColetada": None, "verificado": None,
        "businessContactMethod": None, "ctaAtivado": None, "bio": None,
        "linkBio": None, "destaques": [], "primeiroPost": None, "ultimoPost": None,
        "hiatoDias": None, "cadenciaMensal": {},
        "faseAtual": {"desde": None, "posts": None, "engajamentoPct": None,
                       "mixFormatos": {}, "erPorFormato": {}, "medianaPlaysReel": None},
        "tendenciaEngajamento": [], "ctaPctFaseAtual": None,
        "topHashtags": [], "topMencoes": [],
    },
    # VERTENTE 3 — tráfego pago
    "ads": {
        "metaAdLibrary": {"anunciosAtivos": None, "criativos": None,
                           "mesesNoAr": None, "formatos": []},
        "pixelMeta": None, "pixelGoogleAds": None, "gtm": None, "ga4": None,
        "leitura": None,
    },
    # VERTENTE 4 — presença consolidada
    "google": {
        "perfilEncontrado": None, "nome": None, "categoria": None,
        "categoriaCorreta": None, "nota": None, "avaliacoes": None,
        "recenciaUltimaAvaliacao": None, "respostasDoProprietario": None,
        "fichasDuplicadas": [], "fotos": None, "siteVinculado": None,
        "buscaMarca": None, "buscaSemMarca": None, "pacoteLocal": [],
    },
    "diretorios": {"doctoralia": None, "facebook": None, "linkedin": None,
                    "youtube": None, "tiktok": None, "outros": []},
    "consistenciaNAP": {"google": None, "site": None, "instagram": None,
                         "receita": None, "divergencias": []},
    "concorrentes": [],   # [{nome, nota, avaliacoes, local, instagram, seguidores}]
    "notaGeral": {"valor": None, "escala": 10, "pilares": {p: None for p in PILARES}},
    "dores": [],          # [{titulo, evidencia, custo, vertente}]
    "fontes": [],
    "limitacoes": [],
}


def validar(d, strict=True):
    """Retorna lista de problemas. Vazia = ok."""
    p = []
    for k in ("coletadoEm", "cnpj", "slug", "clinica", "decisor", "notaGeral"):
        if not d.get(k):
            p.append(f"campo obrigatorio ausente ou vazio: {k}")
    if d.get("clinica", {}).get("nome") in (None, ""):
        p.append("clinica.nome vazio")
    ng = d.get("notaGeral") or {}
    if ng.get("valor") is None:
        p.append("notaGeral.valor ausente")
    # pilar nulo e aceitavel quando o canal nao existe — desde que declarado em limitacoes
    lim_txt = " ".join(d.get("limitacoes") or []).lower()
    sem_ig = (d.get("instagram") or {}).get("handle") is None
    for pil in PILARES:
        if (ng.get("pilares") or {}).get(pil) is None:
            if pil in ("instagram", "cadencia") and sem_ig and ("instagram" in lim_txt or "perfil" in lim_txt):
                continue
            p.append(f"pilar sem nota: {pil}")
    if not d.get("fontes"):
        p.append("fontes vazio - todo dado precisa de origem")
    for i, dor in enumerate(d.get("dores") or []):
        if dor.get("vertente") not in VERTENTES:
            p.append(f"dores[{i}].vertente invalida: {dor.get('vertente')!r}")
        if not dor.get("evidencia"):
            p.append(f"dores[{i}] sem evidencia")
    # coerencia: campo nulo em bloco coletado deve estar declarado em limitacoes
    if strict:
        lim = " ".join(d.get("limitacoes") or []).lower()
        if (d.get("google") or {}).get("perfilEncontrado") is None and "google" not in lim:
            p.append("google nao coletado e nao declarado em limitacoes")
        if (d.get("instagram") or {}).get("handle") is None and "instagram" not in lim:
            p.append("instagram nao coletado e nao declarado em limitacoes")
    return p


if __name__ == "__main__":
    import json, sys
    if len(sys.argv) > 1:
        d = json.load(open(sys.argv[1]))
        probs = validar(d)
        print("OK" if not probs else "\n".join("  - " + x for x in probs))
        sys.exit(1 if probs else 0)
    print(json.dumps(MODELO, ensure_ascii=False, indent=1))
