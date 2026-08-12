"""CSS do documento editorial A4 da Oraculo. Reconstruido a partir do PDF da
Auditoria de Marketing (Fira Sans, A4 595x842pt, capa #2a4dd0)."""

CSS = r"""
*, *::before, *::after { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }

:root {
  --azul:    #2a4dd0;
  --tinta:   #16181f;
  --corpo:   #3f4450;
  --suave:   #6b7180;
  --fraco:   #9aa0ad;
  --regua:   #e3e5ea;
  --reguaf:  #16181f;
  --barra:   #ccd3e4;
}

body {
  font-family: 'Fira Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  color: var(--corpo);
  background: #8a8f99;
  -webkit-font-smoothing: antialiased;
  text-rendering: geometricPrecision;
}

@page { size: A4; margin: 0; }

.pagina {
  width: 210mm; height: 297mm;
  padding: 16mm 19mm 13mm;
  position: relative;
  background: #fff;
  page-break-after: always;
  break-after: page;
  overflow: hidden;
}
.pagina:last-child { page-break-after: auto; break-after: auto; }

/* ---------- capa e contracapa ---------- */
.capa {
  background: var(--azul);
  color: #fff;
  padding: 20mm 19mm 18mm;
  display: flex; flex-direction: column;
}
.capa-topo { display: flex; justify-content: space-between; align-items: flex-start; }
.capa-topo img { width: 42mm; height: auto; display: block; }
.capa-meta { text-align: right; font-size: 7.6pt; line-height: 1.55; color: rgba(255,255,255,.82); }
.capa-corpo { margin-top: auto; }
.capa-kicker { font-size: 8.4pt; font-weight: 600; color: rgba(255,255,255,.8); margin-bottom: 5mm; }
.capa h1 {
  font-size: 24pt; font-weight: 700; line-height: 1.15;
  margin: 0 0 7mm; color: #fff; max-width: 156mm; letter-spacing: -.2pt;
}
.capa-lede { font-size: 9.6pt; line-height: 1.62; color: rgba(255,255,255,.9); max-width: 122mm; margin: 0; }
.capa-rodape { margin-top: auto; padding-top: 6mm; border-top: .6pt solid rgba(255,255,255,.35); display: flex; gap: 6mm; }
.capa-stat { flex: 1; }
.capa-stat b { display: block; font-size: 13pt; font-weight: 700; color: #fff; margin-bottom: 1.4mm; }
.capa-stat span { font-size: 7.2pt; line-height: 1.4; color: rgba(255,255,255,.78); display: block; }

.fim { background: var(--azul); color: #fff; padding: 20mm 19mm 18mm; display: flex; flex-direction: column; }
.fim h2 { font-size: 21pt; font-weight: 700; line-height: 1.16; margin: 0 0 6mm; color: #fff; max-width: 132mm; letter-spacing: -.2pt; }
.fim-lede { font-size: 9.6pt; line-height: 1.62; color: rgba(255,255,255,.9); max-width: 122mm; margin: 0 0 10mm; }
.fim-linhas { border-top: .6pt solid rgba(255,255,255,.35); }
.fim-linha { display: flex; gap: 8mm; padding: 3.6mm 0; border-bottom: .6pt solid rgba(255,255,255,.2); }
.fim-linha b { flex: 0 0 32mm; font-size: 8.6pt; font-weight: 600; color: #fff; }
.fim-linha span { flex: 1; font-size: 8.6pt; line-height: 1.5; color: rgba(255,255,255,.88); }
.fim-rodape { margin-top: auto; display: flex; justify-content: space-between; gap: 10mm; font-size: 7.2pt; line-height: 1.5; color: rgba(255,255,255,.75); }
.fim-rodape b { display: block; color: #fff; font-weight: 600; margin-bottom: 1mm; }
.fim-rodape div:last-child { text-align: right; }

/* ---------- cabecalho e rodape de pagina ---------- */
.cab { display: flex; justify-content: space-between; align-items: baseline;
       font-size: 7.2pt; padding-bottom: 2.6mm; border-bottom: .6pt solid var(--regua); margin-bottom: 9mm; }
.cab-esq { color: var(--fraco); }
.cab-dir { color: var(--tinta); font-weight: 600; }
.rod { position: absolute; left: 19mm; right: 19mm; bottom: 8mm;
       display: flex; justify-content: space-between; font-size: 7pt; color: var(--fraco); }

/* ---------- tipografia de conteudo ---------- */
h2.titulo { font-size: 17.5pt; font-weight: 700; line-height: 1.2; color: var(--tinta);
            margin: 0 0 5mm; max-width: 137mm; letter-spacing: -.15pt; }
p.lede { font-size: 9.4pt; line-height: 1.62; color: var(--corpo); max-width: 138mm; margin: 0 0 8mm; }
p.texto { font-size: 8.8pt; line-height: 1.62; color: var(--corpo); max-width: 152mm; margin: 0 0 4mm; }
h3.sub { font-size: 9pt; font-weight: 700; color: var(--tinta); margin: 7mm 0 3mm; }
b, strong { font-weight: 600; color: var(--tinta); }
.azul { color: var(--azul); font-weight: 600; }

/* ---------- tabelas ---------- */
table.t { width: 100%; border-collapse: collapse; margin: 0 0 3mm; }
table.t th { font-size: 7.2pt; font-weight: 600; color: var(--tinta); text-align: left;
             padding: 0 4mm 2.2mm 0; border-bottom: .9pt solid var(--reguaf); vertical-align: bottom; }
table.t td { font-size: 8.2pt; line-height: 1.48; color: var(--corpo);
             padding: 2.9mm 4mm 2.9mm 0; border-bottom: .5pt solid var(--regua); vertical-align: top; }
table.t td:last-child, table.t th:last-child { padding-right: 0; }
table.t td.forte { font-weight: 600; color: var(--tinta); }
table.t td.num, table.t th.num { text-align: right; font-variant-numeric: tabular-nums; }
table.t tr.grupo td { font-weight: 600; color: var(--azul); font-size: 7.6pt; padding-top: 4mm; border-bottom: none; }
table.t.compacta td { padding: 2.2mm 4mm 2.2mm 0; font-size: 7.9pt; }
.fonte { font-size: 6.9pt; line-height: 1.5; color: var(--fraco); margin: 2mm 0 6.5mm; max-width: 160mm; }

/* ---------- blocos de definicao ---------- */
.defs { border-top: .9pt solid var(--reguaf); margin: 0 0 3mm; }
.def { display: flex; gap: 7mm; padding: 3.6mm 0; border-bottom: .5pt solid var(--regua); }
.def-r { flex: 0 0 46mm; font-size: 8.2pt; font-weight: 600; color: var(--tinta); line-height: 1.42; }
.def-d { flex: 1; font-size: 8.2pt; line-height: 1.55; color: var(--corpo); }

/* ---------- grafico de barras ---------- */
.gr { margin: 2mm 0 3mm; }
.gr-area { display: flex; align-items: flex-end; gap: 5mm; height: 40mm; padding: 0 2mm; }
.gr-col { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: flex-end; height: 100%; }
.gr-val { font-size: 8.2pt; font-weight: 700; color: var(--tinta); margin-bottom: 1.4mm; }
.gr-bar { width: 100%; background: var(--barra); min-height: .8mm; }
.gr-bar.on { background: var(--azul); }
.gr-rot { margin-top: 2mm; text-align: center; font-size: 7.4pt; font-weight: 600; color: var(--tinta); }
.gr-sub { text-align: center; font-size: 6.8pt; color: var(--fraco); line-height: 1.35; margin-top: .5mm; }
.gr-eixo { display: flex; gap: 5mm; padding: 0 2mm; }
.gr-eixo > div { flex: 1; }

/* ---------- fecho de pagina ---------- */
.fecho { position: absolute; left: 19mm; right: 19mm; bottom: 14mm;
         font-size: 12.4pt; font-weight: 700; line-height: 1.32; color: var(--tinta);
         max-width: 150mm; letter-spacing: -.1pt; }
.fecho .azul { color: var(--azul); font-weight: 700; }

/* ---------- caixa de alerta discreta ---------- */
.nota { border-left: .75pt solid var(--azul); padding: 0 0 0 5mm; margin: 5mm 0 4mm; }
.nota > b { display: block; font-size: 8.2pt; font-weight: 700; color: var(--tinta); margin-bottom: 1.6mm; }
.nota p b { display: inline; font-size: inherit; font-weight: 600; color: var(--tinta); margin: 0; }
.nota p { font-size: 8.2pt; line-height: 1.58; color: var(--corpo); margin: 0 0 2mm; max-width: 150mm; }
.nota p:last-child { margin-bottom: 0; }

@media print {
  body { background: #fff; }
  .pagina { margin: 0; box-shadow: none; }
}
@media screen {
  body { padding: 12mm 0; }
  .pagina { margin: 0 auto 8mm; box-shadow: 0 2mm 8mm rgba(0,0,0,.28); }
}
"""
