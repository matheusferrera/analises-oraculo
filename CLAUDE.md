# Oráculo — Guia de Criação de Relatórios

## Visão geral

Este projeto gera relatórios de análise de Instagram (e YouTube) para clientes da Oráculo Tecnologia, mais proposta comercial associada. Quando o usuário pedir uma análise, siga este guia do início ao fim.

---

## Passo a passo para um novo relatório de Instagram

### 1. Criar pasta do cliente

```
mkdir <NomeCliente>
```

Use PascalCase sem espaços. Ex: `JoanaTavares`, `PECBR`, `DrCarlosAlves`.

### 2. Coletar dados do perfil

**Usar o MCP do Playwright** para navegar e extrair os dados diretamente do perfil público.

Sequência obrigatória:
1. `browser_navigate` → `https://www.instagram.com/<handle>/`
2. Fechar modais de login/aviso com `browser_click` se aparecerem
3. Rolar a página várias vezes com `browser_press_key` (End) ou `browser_scroll` para carregar mais posts
4. `browser_snapshot` para capturar o estado completo da página (bio, seguidores, destaques, grid)
5. `browser_take_screenshot` para salvar screenshot do perfil
6. Para cada post relevante (top ~27): `browser_navigate` → URL do post → `browser_snapshot` para extrair curtidas, comentários, data e legenda
7. Salvar todos os dados extraídos em `<NomeCliente>/data/<handle>-body.txt` (texto bruto) e `<NomeCliente>/data/<handle>-scan.json` (estrutura JSON com postDetails)

> O script `tools/instagram-scan.mjs` existe como referência de lógica, mas a coleta deve ser feita via MCP do Playwright para aproveitar a sessão já autenticada do browser e ter controle interativo sobre modais e bloqueios.

### 3. Analisar os dados coletados

Ler os dois arquivos gerados antes de escrever qualquer HTML:
- `<NomeCliente>/data/<handle>-body.txt` — texto bruto da página (seguidores, bio, nomes de destaques, legendas)
- `<NomeCliente>/data/<handle>-scan.json` — estrutura JSON com postDetails (curtidas, comentários, datas, títulos)

Extrair:
- Contagem de seguidores, posts, seguindo
- Bio completa
- Lista de destaques
- Top posts por curtidas (ordenar `postDetails` por likes)
- ER médio da amostra: `(soma das curtidas + comentários) / (n_posts × seguidores) × 100`
- Padrão de formatos (Reels vs. carrossel vs. estático)
- Temas recorrentes nas legendas
- Comentários com intenção de compra

### 4. Criar `Analise-Instagram.html`

Usar `JoanaTavares/Analise-Instagram.html` como template base. Substituir todos os dados pelo cliente novo.

**Estrutura obrigatória da página (na ordem):**

| # | ID | Título |
|---|---|---|
| — | `diagnostico` | Diagnóstico Executivo (score block + sit/help + diag-wrap) |
| — | KPI strip | 5 KPIs: Seguidores, Posts, Posts Analisados, Maior Post em Likes, ER Recente |
| 1 | `visao-geral` | Identidade e Posicionamento |
| 2 | `metricas` | Métricas Principais |
| 3 | `conteudo` | Estratégia de Conteúdo |
| 4 | `engajamento` | Engajamento e Posts Mais Curtidos |
| 5 | `collabs` | Destaques, Prova Social e Conversão |
| 6 | — | Temas, Palavras-Chave e CTAs |
| 7 | `audiencia` | Análise de Audiência |
| 8 | `swot` | Análise SWOT |
| 9 | `comparativo` | Comparativo (ex: Fixados vs. Recentes, ou vs. outro canal) |
| 10 | `recomendacoes` | Recomendações Estratégicas (Curto / Médio / Longo prazo) |
| 11 | `resumo` | Resumo Executivo e Pontuação |

**Ao final de cada seção**, incluir obrigatoriamente o bloco insight:

```html
<div class="insight [good|warn|bad|info|purple]">
  <div class="insight-header">
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>
    O que isso significa para você
  </div>
  <div class="insight-body">
    <span class="verdict">[&#9650; Bom | &#9654; Atenção | &#9733; Destaque]</span>
    <p>Texto personalizado para o cliente explicando o impacto prático daquela seção.</p>
  </div>
</div>
```

Escolha da classe do insight:
- `good` (verde) — ponto forte, resultado positivo
- `warn` (âmbar) — atenção, situação mista ou oportunidade clara
- `bad` (azul escuro) — problema ou diagnóstico importante
- `info` (azul) — oportunidade estratégica ou informação contextual
- `purple` — reservado para insights de longo prazo ou visão consolidada

**Variáveis a personalizar:**
- `--ig-grad` no `:root` pode variar conforme a identidade do cliente, mas o `--primary: #1d4ed8` é sempre o azul Oráculo
- Título da página, OG tags, URL canônica, handle, nome da conta, data de análise
- Todos os números, textos e gráficos (Chart.js) são específicos do cliente

**5 gráficos obrigatórios (Chart.js):**
1. `chartAudiencia` — comparativo de ER ou audiência (bar)
2. `chartFormatos` — mix de formatos (doughnut)
3. `chartEngajamento` — top posts (bar com curtidas e comentários)
4. `chartAudienciaSegmentos` — segmentos de audiência (bar horizontal)
5. `chartComparativo` — comparativo da seção 9 (bar ou radar)

### 5. Criar `Proposta-Comercial.html`

Usar `JoanaTavares/Proposta-Comercial.html` como template.

Personalizar:
- Nome do cliente, handle, nicho e dores específicas levantadas na análise
- Planos e preços (confirmar com o usuário antes de colocar valores)
- Seção "O que entregamos" baseada nos gaps identificados na análise
- Depoimentos e provas sociais da Oráculo (manter os existentes no template)

### 6. Criar `Banners-OG.html` e gerar as imagens OG

Usar `JoanaTavares/Banners-OG.html` como template. Ajustar textos e cores para o cliente.

Abrir no browser e tirar screenshot de cada banner para gerar:
- `og-instagram.png` — 1200×630px
- `og-proposta.png` — 1200×630px

### 7. Atualizar OG tags

Nas duas páginas HTML, atualizar:
- `og:image` com a URL Vercel correta (`https://analises-oraculo.vercel.app/<NomeCliente>/...`)
- `og:url` com a URL da página

---

## Design system — regras que nunca mudam

| Token | Valor |
|---|---|
| `--primary` | `#1d4ed8` (azul Oráculo) |
| `--green` | `#16a34a` |
| `--amber` | `#d97706` |
| `--blue` | `#3b82f6` |
| `--purple` | `#7c3aed` |
| Font | `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto` |
| Border radius | `12px` |

**Nunca usar vermelho ou laranja como cor principal da UI.** O `--primary` é sempre o azul.

---

## Estrutura de arquivos de um cliente completo

```
<NomeCliente>/
  Analise-Instagram.html
  Proposta-Comercial.html
  Banners-OG.html
  og-instagram.png
  og-proposta.png
  data/
    <handle>-scan.json
    <handle>-body.txt
  screenshots/
    <handle>-profile.png
```

---

## Comandos rápidos

```bash
# Servir localmente para revisar o resultado
python3 -m http.server 8765
# Abrir: http://localhost:8765/<NomeCliente>/Analise-Instagram.html
```

A coleta de dados é feita via **MCP do Playwright** (ver passo 2), não por linha de comando.

---

## O que o usuário precisa fornecer

Para criar um relatório completo basta:
1. **Handle do Instagram** — ex: `@drajoanatavares`
2. **Nome da pasta** — ex: `JoanaTavares`
3. **Nicho/contexto** — ex: cirurgiã rinoplastia, consultoria agropecuária

Tudo mais é derivado da análise dos dados coletados.
