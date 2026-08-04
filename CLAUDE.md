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

**Usar o MCP do Playwright** com a **API interna do Instagram** (método validado na análise da La Deguste Buffet). É muito mais confiável e rápido do que abrir post por post, e é a **única forma de obter curtidas/comentários quando a conta oculta a contagem** (a maioria das contas business oculta).

#### 2.1 Garantir sessão autenticada (pré-requisito)
1. `browser_navigate` → `https://www.instagram.com/<handle>/`
2. Se o cabeçalho mostrar **"Entrar"/"Cadastre-se"**, a sessão está **deslogada** → curtidas e comentários ficam ocultos e a API retorna vazio. **Pare e peça ao usuário para logar** na janela do Playwright (`browser_navigate` → `https://www.instagram.com/accounts/login/`). Quando logado, o título da aba mostra algo como `(N) Instagram`.
3. Se aparecer modal de cadastro, fechar com `browser_press_key` → `Escape`.
4. `browser_take_screenshot` → salvar screenshot do perfil em `screenshots/<handle>-profile.png`.

#### 2.2 Puxar dados via API interna (preferencial)
Com a sessão logada, usar `browser_evaluate` em qualquer página `instagram.com` (mesma origem, cookies inclusos). Header obrigatório: `x-ig-app-id: 936619743392459`.

**a) Perfil + user_id:**
```js
await fetch('/api/v1/users/web_profile_info/?username=<handle>', {
  headers: { 'x-ig-app-id': '936619743392459' }, credentials: 'include'
}).then(r => r.json())
// → data.user: id, full_name, category_name, biography, external_url,
//   edge_followed_by.count (seguidores), edge_follow.count (seguindo),
//   edge_owner_to_timeline_media.count (posts), bio_links, highlight_reel_count
```

**b) Amostra de posts (paginada) — usar o `user.id` do passo a):**
```js
// loop com max_id; ~5 páginas de 30 = até ~150 posts. 60 é uma boa amostra.
let url = `/api/v1/feed/user/${uid}/?count=30` + (maxId ? `&max_id=${maxId}` : '');
const j = await fetch(url, { headers:{'x-ig-app-id':'936619743392459'}, credentials:'include' }).then(r=>r.json());
// cada item: code, media_type (1=img,2=vídeo/reel,8=carrossel), product_type,
//   like_count, comment_count, play_count/ig_play_count (Reels),
//   carousel_media_count, taken_at (epoch s), caption.text
// j.more_available + j.next_max_id controlam a paginação
```
Salvar o resultado com `browser_evaluate({ filename: 'ladeguste-feed.json' })` (vai para `.playwright-mcp/`).

> **Detalhe do scroll deslogado:** sem login, o Instagram bloqueia o scroll infinito (mostra "Mostrar mais posts" + login wall) e o snapshot do grid só traz ~12 posts. Por isso o método via API logada é o padrão.
> **Post único (fallback):** o media id numérico está no `<meta property="al:ios:url" content="instagram://media?id=NUMERO">`; com ele, `GET /api/v1/media/<id>/info/` retorna os mesmos campos.

#### 2.3 Gerar os arquivos de dados
Processar o JSON cru com Python e salvar:
- `<NomeCliente>/data/<handle>-scan.json` — estrutura com cabeçalho do perfil + `postDetails` (tipo, data, likes, comentarios, plays, tags, tema, legenda)
- `<NomeCliente>/data/<handle>-body.txt` — texto bruto legível (perfil + lista de posts)
- (opcional) manter o feed cru como `<handle>-feed-raw.json`

> O script `tools/instagram-scan.mjs` existe como referência de lógica, mas a coleta deve ser feita via MCP do Playwright para aproveitar a sessão autenticada e a API interna.

### 3. Analisar os dados coletados

Ler os dois arquivos gerados antes de escrever qualquer HTML:
- `<NomeCliente>/data/<handle>-body.txt` — texto bruto da página (seguidores, bio, nomes de destaques, legendas)
- `<NomeCliente>/data/<handle>-scan.json` — estrutura JSON com postDetails (curtidas, comentários, datas, títulos)

Extrair (processar o JSON com Python, não a olho):
- Contagem de seguidores, posts, seguindo + bio completa + lista de destaques
- Top posts por curtidas (ordenar `postDetails` por likes)
- ER médio da amostra: `(soma das curtidas + comentários) / (n_posts × seguidores) × 100`
- **ER recente** (últimos ~12 posts) vs ER da amostra completa — revela queda/alta de tração
- **ER por formato** (Reel vs carrossel vs imagem) — quase sempre revela qual formato performa melhor e embasa a seção 9 (comparativo) e a recomendação de mix
- Mix de formatos (contagem por tipo) + média de `plays` dos Reels
- Cadência de postagem (posts/mês) a partir de `taken_at`
- Hashtags mais usadas e **@menções recorrentes** (parceiros/fornecedores — viram ângulo de co-marketing)
- % de posts com CTA (regex por "link na bio", "wa.me", "whats", "orçamento", "agende", etc.)
- Temas recorrentes e comentários/legendas com intenção de compra

### 4. Criar `Analise-Instagram.html`

Usar `JoanaTavares/Analise-Instagram.html` como template base. Substituir todos os dados pelo cliente novo.

> **Técnica de build (recomendada):** o `<style>` é enorme (~30 KB) e nunca muda. Em vez de editá-lo, extraia o bloco `<style>…</style>` do template e reaproveite-o; monte o `<head>`, cover, seções e o `<script>` dos gráficos como strings em um script Python e concatene. Isso evita corromper o CSS e mantém o design system intacto. Ajuste só `--ig-grad` no `:root` (override) para a identidade do cliente — `--primary` segue sempre o azul Oráculo `#1d4ed8`. **Antes de salvar, valide com Python:** zero resquícios do cliente-template (ex: `Joana`, handle antigo, telefone, termos do nicho antigo) e zero aspas curvas dentro de tags (`<[^>]*[”“][^>]*>` deve dar 0; aspas curvas só no texto visível). O mesmo vale para a Proposta e os Banners — lembre da `<meta name="description">` no head, fácil de esquecer.

> **⚠️ Não abrir o HTML gerado no Playwright para conferir o visual.** O Playwright é só para a coleta de dados do Instagram (passo 2). Depois de salvar o HTML e passar na validação em Python, o trabalho está encerrado — nada de servir em `localhost`, tirar screenshot da página ou revisar o layout no browser. O valor do entregável está na **profundidade da análise do perfil**, não na inspeção visual do HTML; o design system do template já é conhecido e estável. Cuidados de markup que a validação Python deve cobrir (aprendidos na análise da Sinfonya Turismo):
> - `.sithelp-list li` é `display:flex` — um `<strong>` solto vira flex-item e quebra a linha. Envolva o conteúdo de cada `<li>` desses cartões em um `<span>`.
> - `.callout strong` é o **título** do bloco (`display:block`, caixa alta). Negrito no corpo do callout precisa ser `<b>`, senão vira um segundo cabeçalho no meio do texto.

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

Servir o projeto localmente e capturar cada card **pelo id** (`#og-instagram` e `#og-proposta`) com o Playwright — screenshot de elemento, não de viewport. O card renderiza 1201 px por arredondamento de subpixel; recortar para o tamanho exato com `sips -c 630 1200 <arquivo>.png` (o macOS não tem PIL instalado). Resultado:
- `og-instagram.png` — 1200×630px
- `og-proposta.png` — 1200×630px

> Esta é a **única** etapa pós-build em que o Playwright abre o HTML gerado. Não aproveite a janela aberta para revisar o layout das páginas.

### 7. Atualizar OG tags

Nas duas páginas HTML, atualizar:
- `og:image` com a URL Vercel correta (`https://analises-oraculo.vercel.app/<NomeCliente>/...`)
- `og:url` com a URL da página

### 8. Adicionar o cliente ao `index.html` (obrigatório)

**Todo relatório novo tem que entrar na central de análises em `index.html`.** Sem isso o material fica invisível na raiz do projeto.

Duplicar um `<article class="client-card">` existente e ajustar:
- `data-client="<Nome do Cliente> <NomePasta>"` — alimenta a busca; inclua as duas formas
- `style="--order: N"` — próximo número livre na sequência
- Capa: `<div class="client-cover"><img src="<NomePasta>/og-instagram.png" alt="<Nome do Cliente>" loading="lazy"><span class="folder-badge"><NomePasta></span></div>`
  - Sem banner OG ainda, usar `<div class="client-cover no-image" data-monogram="XX">` com as iniciais
- `<p class="client-number">Cliente NN</p>` e `<h2><Nome do Cliente></h2>`
- Um `<a class="client-action">` por documento, com `data-type="analise"` ou `data-type="proposta"` — é o que os filtros do topo usam
  - Enquanto os arquivos não existirem: `<span class="client-empty">Documentos em preparação</span>`

O contador de clientes do topo é calculado em JS a partir dos cards; não precisa mexer nele.

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
