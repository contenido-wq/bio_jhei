# Arquitectura CSS — Link in Bio · Jhei Trujillo

> Fuente de verdad visual: `docs/brand/aivi-brand-extract.md` + `ref-aivi-social.png` + `ref-aivi-web.png`.
> Arquitectura de referencia (ritmo y estructura, no color): `ref-layout-hero.png` + `ref-layout-bio.png`.
> Stack: HTML + CSS + JS vanilla. Sin frameworks, sin build, sin dependencias externas, sin CDN.

---

## 0. Topología de archivos y orden de carga

```
/index.html
/assets/fonts/hkgrotesk-var-latin.woff2      ← único archivo de fuente
/assets/img/…                                 ← AVIF + fallback WebP
/css/
  tokens.css        ← §1  custom properties. NO contiene selectores más allá de :root
  reset.css         ← §3.1 reset + base elements
  background.css    ← §2  el sistema de fondo, aislado y autocontenido
  layout.css        ← §3  grid, contenedores, ritmo vertical
  components.css    ← botones, tarjetas glass, carrusel, socials, footer
  utilities.css     ← helpers (.visually-hidden, .u-fire-text, .u-bleed)
/js/
  theme.js          ← (ver §7: este proyecto es dark-only por marca; ver nota)
  carousel.js
  main.js
```

Orden obligatorio en `<head>` (la cascada depende de él):

```html
<link rel="stylesheet" href="/css/tokens.css">
<link rel="stylesheet" href="/css/reset.css">
<link rel="stylesheet" href="/css/background.css">
<link rel="stylesheet" href="/css/layout.css">
<link rel="stylesheet" href="/css/components.css">
<link rel="stylesheet" href="/css/utilities.css">
```

**Regla de arquitectura:** `tokens.css` es la única capa que declara valores literales.
Ningún otro archivo puede escribir un hex, un `px` de espaciado ni un `cubic-bezier`.
Excepción única y documentada: `background.css`, donde los gradientes decorativos
necesitan `rgba()` con alpha calculada en sitio (§2.9 explica por qué).

**Criterio de nombres:** `--<categoría>-<rol>[-<variante>]`, siempre por rol, nunca por apariencia.
`--surface-glass`, no `--gris-claro`. `--text-secondary`, no `--text-b8b8b8`.
Los tres colores de marca sí conservan nombre de color (`--brand-orange`) porque en esta
marca el color *es* el rol — así lo declara la guía AIVI ("tonos de acción").

---

## 1. `css/tokens.css` — archivo completo

```css
/* ============================================================================
   tokens.css — Link in Bio · Jhei Trujillo
   Capa de tokens. Única fuente de valores literales del sistema.
   Paleta heredada de la guía de uso AIVI (docs/brand/aivi-brand-extract.md).
   ========================================================================= */

:root {
  color-scheme: dark;

  /* ── 1. Marca ────────────────────────────────────────────────────────────
     Los 5 valores oficiales de la guía. Prohibido añadir un 6º color.        */
  --brand-black:  #101010;   /* "inteligencia y control" */
  --brand-white:  #FAFAFA;   /* "simplicidad y entendimiento" */
  --brand-orange: #FE803F;   /* acción — primario */
  --brand-gold:   #FFC252;   /* acción — acento / foco */
  --brand-red:    #FF413B;   /* acción — énfasis */

  /* Componentes RGB, para construir alphas sin repetir literales.
     Uso: rgb(var(--rgb-white) / 12%)                                         */
  --rgb-black:  16 16 16;
  --rgb-white:  250 250 250;
  --rgb-orange: 254 128 63;
  --rgb-gold:   255 194 82;
  --rgb-red:    255 65 59;

  /* ── 2. Fondos y superficies ─────────────────────────────────────────────
     Escala de elevación sobre negro: cada nivel es blanco a alpha creciente.
     Nunca gris opaco (regla de la guía: "nunca cajas opacas grises").        */
  --bg-base:            var(--brand-black);
  --bg-sunken:          #0A0A0A;                        /* pozos, tracks */
  --surface-glass:      rgb(var(--rgb-white) / 5%);     /* tarjeta reposo   ≈#1C1C1C */
  --surface-glass-hi:   rgb(var(--rgb-white) / 8%);     /* tarjeta hover    ≈#222 */
  --surface-glass-lo:   rgb(var(--rgb-white) / 3%);     /* fondos pasivos */
  --surface-inset:      rgb(var(--rgb-black) / 40%);    /* pozos sobre glass */

  /* ── 3. Bordes ───────────────────────────────────────────────────────────
     El borde de 1px translúcido es firma de la marca. Tres intensidades:
     -subtle  → separadores decorativos (no informativos)
     -default → bordes de tarjeta glass
     -strong  → mínimo que alcanza 3:1 sobre --bg-base (ver §5.4). Úsalo
                cuando el borde ES la única señal visual de un control.       */
  --border-subtle:  rgb(var(--rgb-white) / 7%);
  --border-default: rgb(var(--rgb-white) / 12%);
  --border-strong:  rgb(var(--rgb-white) / 34%);
  --border-fire:    rgb(var(--rgb-orange) / 45%);
  --border-width:   1px;

  /* ── 4. Texto ────────────────────────────────────────────────────────────
     Ratios verificados sobre --bg-base en §5.4.                              */
  --text-primary:   var(--brand-white);              /* 18.23:1 */
  --text-secondary: rgb(var(--rgb-white) / 72%);     /*  9.59:1 */
  --text-tertiary:  rgb(var(--rgb-white) / 56%);     /*  6.19:1 */
  --text-faint:     rgb(var(--rgb-white) / 44%);     /*  4.25:1 — SOLO decorativo,
                                                        no apto para texto AA */
  --text-on-fire:   var(--brand-black);              /* texto sobre botón degradado */
  --text-accent:    var(--brand-orange);             /*  7.59:1 */
  --text-emphasis:  var(--brand-red);                /*  5.50:1 */
  --text-highlight: var(--brand-gold);               /* 11.86:1 */
  --text-link:      var(--brand-gold);

  /* ── 5. Degradados ───────────────────────────────────────────────────────
     --grad-fire es EL degradado de marca: rojo → naranja → dorado.
     El ángulo 96deg replica la inclinación de las piezas AIVI.               */
  --grad-fire:
    linear-gradient(96deg,
      var(--brand-red)    0%,
      var(--brand-orange) 54%,
      var(--brand-gold)  100%);

  --grad-fire-hover:
    linear-gradient(96deg,
      #FF5A54  0%,
      #FF9455 54%,
      #FFCE71 100%);

  /* Para background-clip:text. Invertido: el ojo lee rojo→dorado de izq a der
     igual que "Únete a AIVI" en la pieza social.                            */
  --grad-text-fire:
    linear-gradient(92deg,
      var(--brand-red)    0%,
      var(--brand-orange) 45%,
      var(--brand-gold)   95%);

  /* Superficie glass: la luz entra por arriba-izquierda, como en las piezas. */
  --grad-surface-glass:
    linear-gradient(158deg,
      rgb(var(--rgb-white) / 8.5%) 0%,
      rgb(var(--rgb-white) / 3.5%) 46%,
      rgb(var(--rgb-white) / 2%)  100%);

  /* Borde degradado para tarjetas destacadas (vía mask, ver components.css). */
  --grad-border-glass:
    linear-gradient(158deg,
      rgb(var(--rgb-white) / 22%) 0%,
      rgb(var(--rgb-white) / 6%)  40%,
      rgb(var(--rgb-white) / 14%)100%);

  --grad-border-fire:
    linear-gradient(96deg,
      rgb(var(--rgb-red) / 70%),
      rgb(var(--rgb-gold) / 70%));

  /* Núcleo de haz de luz — usado por background.css. Casi blanco cálido. */
  --beam-core:  255 244 224;

  /* ── 6. Tipografía ───────────────────────────────────────────────────────*/
  --font-sans:
    "Hanken Grotesk",
    "Hanken Fallback",              /* ← @font-face con métricas ajustadas, §4 */
    system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;

  /* Pesos declarados por la guía AIVI: Thin, Light, Bold, Black.
     Añadimos 400/500 porque un link-in-bio necesita cuerpo legible.          */
  --fw-thin:    100;
  --fw-light:   300;
  --fw-regular: 400;
  --fw-medium:  500;
  --fw-bold:    700;
  --fw-black:   900;

  /* Escala fluida. Base 16px → 375px móvil, techo ~1066–1200px.
     Sin media queries: clamp() cubre todo el rango.                          */
  --step--2: clamp(0.6875rem, 0.675rem + 0.06vw, 0.75rem);   /* 11 → 12 */
  --step--1: clamp(0.8125rem, 0.79rem  + 0.12vw, 0.875rem);  /* 13 → 14 */
  --step-0:  clamp(1rem,      0.96rem  + 0.2vw,  1.0625rem); /* 16 → 17 */
  --step-1:  clamp(1.125rem,  1.05rem  + 0.38vw, 1.3125rem); /* 18 → 21 */
  --step-2:  clamp(1.375rem,  1.22rem  + 0.75vw, 1.75rem);   /* 22 → 28 */
  --step-3:  clamp(1.75rem,   1.45rem  + 1.5vw,  2.5rem);    /* 28 → 40 */
  --step-4:  clamp(2.25rem,   1.70rem  + 2.7vw,  3.5rem);    /* 36 → 56 */
  --step-5:  clamp(2.75rem,   1.80rem  + 4.7vw,  4.75rem);   /* 44 → 76 */

  --lh-tight:   1.05;   /* display 900 */
  --lh-snug:    1.18;   /* titulares */
  --lh-normal:  1.35;   /* subtítulos, botones */
  --lh-relaxed: 1.62;   /* párrafos de bio */

  --ls-tighter: -0.03em;  /* display grande */
  --ls-tight:   -0.015em;
  --ls-normal:  0em;
  --ls-wide:    0.04em;
  --ls-widest:  0.14em;   /* eyebrow / kicker en mayúsculas */

  --measure: 42ch;        /* ancho óptimo de lectura de la bio */

  /* ── 7. Espaciado — base 4px ─────────────────────────────────────────────*/
  --space-0:   0;
  --space-px:  1px;
  --space-1:   0.25rem;   /*  4 */
  --space-2:   0.5rem;    /*  8 */
  --space-3:   0.75rem;   /* 12 */
  --space-4:   1rem;      /* 16 */
  --space-5:   1.25rem;   /* 20 */
  --space-6:   1.5rem;    /* 24 */
  --space-8:   2rem;      /* 32 */
  --space-10:  2.5rem;    /* 40 */
  --space-12:  3rem;      /* 48 */
  --space-16:  4rem;      /* 64 */
  --space-20:  5rem;      /* 80 */
  --space-24:  6rem;      /* 96 */

  /* Espaciado fluido — el ritmo vertical del documento (§3.4) */
  --space-section:    clamp(3.5rem, 2rem + 7vw, 7rem);    /* 56 → 112 */
  --space-block:      clamp(1.5rem, 1.1rem + 2vw, 2.5rem);/* 24 → 40  */
  --space-stack:      clamp(0.75rem, 0.6rem + 0.8vw, 1.25rem);
  --gutter:           clamp(1.25rem, 1rem + 3vw, 2rem);   /* 20 → 32  */

  /* ── 8. Layout ───────────────────────────────────────────────────────────*/
  --w-content: 34rem;   /* 544px — columna principal del link-in-bio */
  --w-prose:   30rem;   /* 480px — bloques de texto largo */
  --w-wide:    64rem;   /* 1024px — carrusel y bleed controlado */
  --tap-min:   44px;    /* objetivo táctil mínimo (WCAG 2.5.8 / HIG) */

  /* Breakpoints: NO son utilizables dentro de @media (las custom properties
     no se evalúan ahí). Se declaran para consumo desde JS
     (getComputedStyle) y como documentación del contrato. Toda @media del
     proyecto debe usar el literal en rem, y solo estos dos valores.          */
  --bp-md: 48rem;   /* 768px */
  --bp-lg: 64rem;   /* 1024px */

  /* ── 9. Radios ───────────────────────────────────────────────────────────*/
  --r-xs:     6px;
  --r-sm:     10px;
  --r-md:     14px;
  --r-lg:     20px;
  --r-xl:     28px;
  --r-2xl:    36px;
  --r-pill:   999px;
  --r-circle: 50%;

  /* ── 10. Sombras y glows ────────────────────────────────────────────────
     Sobre #101010 una sombra negra casi no se lee: la elevación se comunica
     con el highlight interno superior (--ring-top) y, en los CTA, con glow.  */
  --shadow-e1: 0 1px 2px rgb(0 0 0 / 55%);
  --shadow-e2: 0 4px 16px -4px rgb(0 0 0 / 65%);
  --shadow-e3: 0 16px 40px -12px rgb(0 0 0 / 78%);

  --ring-top:     inset 0 var(--border-width) 0 rgb(var(--rgb-white) / 10%);
  --ring-top-hi:  inset 0 var(--border-width) 0 rgb(var(--rgb-white) / 16%);

  --glow-fire:        0 8px 28px -8px rgb(var(--rgb-orange) / 42%);
  --glow-fire-strong: 0 12px 40px -8px rgb(var(--rgb-red) / 52%);
  --glow-gold:        0 0 0 1px rgb(var(--rgb-gold) / 30%),
                      0 6px 24px -8px rgb(var(--rgb-gold) / 35%);

  /* ── 11. Movimiento ─────────────────────────────────────────────────────*/
  --dur-instant: 90ms;
  --dur-fast:    160ms;
  --dur-base:    240ms;
  --dur-slow:    400ms;
  --dur-slower:  640ms;
  --dur-ambient: 24s;    /* deriva del fondo, si se activa (§2.8) */

  --ease-out:    cubic-bezier(0.22, 1, 0.36, 1);      /* salidas, entradas UI */
  --ease-in:     cubic-bezier(0.64, 0, 0.78, 0);
  --ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);
  --ease-spring: cubic-bezier(0.34, 1.42, 0.64, 1);   /* press de botón */
  --ease-linear: linear;                              /* solo para grain/ambient */

  /* ── 12. Z-index ────────────────────────────────────────────────────────
     Escala global del documento. Las capas internas del fondo NO usan esta
     escala: viven aisladas dentro de .bg (§2.7).                             */
  --z-backdrop: 0;
  --z-content:  1;
  --z-raised:   10;
  --z-sticky:   100;
  --z-header:   200;
  --z-overlay:  300;
  --z-modal:    400;
  --z-toast:    500;

  /* ── 13. Foco ───────────────────────────────────────────────────────────*/
  --focus-ring-color:  var(--brand-gold);   /* 11.86:1 sobre --bg-base */
  --focus-ring-width:  2px;
  --focus-ring-offset: 3px;
  --focus-halo-color:  var(--bg-base);      /* separa el anillo del fondo cálido */
}
```

**Sobre el toggle de tema:** la identidad AIVI es negro-sobre-cálido por definición
("el negro representa inteligencia y control") y la paleta no tiene equivalente claro.
Un modo claro obligaría a inventar colores fuera de la guía. Decisión: el sitio es
**dark-only**, se declara `color-scheme: dark` para que los controles nativos y el
scrollbar coincidan, y no se envía `theme.js`. La estructura de tokens ya está
preparada por si el cliente pide modo claro después: bastaría redefinir el bloque
2–4 bajo `[data-theme="light"]` sin tocar ningún componente.

---

## 2. El sistema de fondo — `css/background.css`

### 2.1 Descomposición del referente

Analizando `ref-aivi-social.png`, el fondo son 5 fenómenos independientes. Cada uno
tiene una técnica óptima distinta, y mezclarlas es el error clásico:

| # | Fenómeno | Técnica | Por qué esa y no otra |
|---|---|---|---|
| 1 | Base `#101010` + caída a negro en bordes | `background-color` + `radial-gradient` de viñeta | Coste cero. Nunca imagen. |
| 2 | Resplandor cálido entrando por la esquina superior derecha | 3 × `radial-gradient` en un solo elemento, mezclados con `background-blend-mode: screen` | `screen` suma luz como en la realidad; un `rgba` apilado en `normal` la apaga. |
| 3 | Haces diagonales naranja→rojo→dorado con núcleo casi blanco | `linear-gradient` con stops muy próximos, dentro de un contenedor rotado, y `mask-image` radial en un wrapper sin rotar | El "difuminado" del borde del haz lo dan los stops del gradiente. **No** `filter: blur()`. |
| 4 | Chevrones / hexágonos de esquina redondeada, gran escala, recortados por el viewport | `mask-image` con SVG inline en data-URI (`stroke-linejoin: round`) + `background` degradado glass | `clip-path: polygon()` **no puede** redondear vértices. El SVG stroke-round sí, y pesa ~250 bytes. |
| 5 | Grano fino sobre todo | SVG `feTurbulence` en data-URI, **teselado** a 128 px, `mix-blend-mode: overlay` | Teselar hace que el navegador rasterice un tile pequeño una vez y lo repita. Generarlo a pantalla completa es 20–60 ms de rasterizado en móvil. |

**Lo que NO se puede reproducir con CSS y hay que aceptar:** la cinta de luz de la
pieza social se curva de forma orgánica (parece un render 3D). Un `linear-gradient`
produce una banda recta de ancho uniforme. La versión CSS es una interpretación
estilizada, no una copia. Si el cliente exige la curvatura exacta, la **única**
concesión raster admisible es un AVIF de 1200 px de ancho conteniendo *solo* la cinta
sobre transparencia, como una capa `background-image` más, con presupuesto de 24 KB
(§6.1). No se convierte todo el fondo en imagen.

### 2.2 Marcado HTML — exacto

El fondo es un hermano de `<main>`, no un ancestro. Esto es lo que impide que los
`mix-blend-mode` y las capas contaminen el contenido.

```html
<body>
  <a class="skip-link" href="#main">Ir al contenido</a>

  <!-- Fondo decorativo. aria-hidden + sin foco + sin eventos. -->
  <div class="bg" aria-hidden="true">
    <div class="bg__glow"></div>

    <div class="bg__glyphs">
      <span class="bg__glyph bg__glyph--hex-a"></span>
      <span class="bg__glyph bg__glyph--hex-b"></span>
      <span class="bg__glyph bg__glyph--chevron"></span>
    </div>

    <div class="bg__beams-wrap">
      <div class="bg__beams"></div>
    </div>

    <div class="bg__vignette"></div>
    <div class="bg__grain"></div>
  </div>

  <main id="main" class="layout">…</main>
</body>
```

### 2.3 Raíz del fondo: aislamiento y contención

```css
/* ── background.css ──────────────────────────────────────────────────────── */

.bg {
  position: fixed;
  inset: 0;
  z-index: var(--z-backdrop);          /* 0 */
  overflow: hidden;                     /* recorta glifos por el viewport */
  pointer-events: none;
  background-color: var(--bg-base);

  /* CLAVE 1 — aísla el grupo de composición. Sin esto, el
     mix-blend-mode del grano intentaría mezclarse con el <body> y, en
     algunos motores, con el contenido pintado después. */
  isolation: isolate;

  /* CLAVE 2 — contención. layout+paint+style acotan invalidaciones al
     subárbol. NO añadir `size`: el elemento se dimensiona por `inset`. */
  contain: layout paint style;

  /* CLAVE 3 — NO poner will-change, translateZ(0) ni backface-visibility.
     Ver §2.8: eso convertiría 5 capas en 5 texturas GPU de pantalla completa. */
}

/* Todas las capas comparten geometría y no generan contexto de apilamiento
   propio salvo donde se indica. */
.bg > * {
  position: absolute;
  inset: 0;
}
```

`position: fixed` con `inset: 0` usa el bloque contenedor inicial, que en iOS Safari
corresponde al *large viewport*: el fondo **no** se redimensiona cuando la barra de
URL se colapsa. Por eso `inset: 0` es preferible a `height: 100dvh` aquí — `dvh`
provocaría un reflow y repintado del fondo en cada scroll.

### 2.4 Capa 1 — resplandor de esquina superior derecha

```css
.bg__glow {
  z-index: 1;

  background-image:
    /* Núcleo dorado, muy pegado a la esquina */
    radial-gradient(42% 34% at 96% 2%,
      rgb(var(--rgb-gold) / 38%) 0%,
      rgb(var(--rgb-gold) / 14%) 42%,
      rgb(var(--rgb-gold) / 0%)  72%),

    /* Cuerpo naranja: el volumen del resplandor */
    radial-gradient(74% 58% at 100% 0%,
      rgb(var(--rgb-orange) / 40%) 0%,
      rgb(var(--rgb-orange) / 16%) 34%,
      rgb(var(--rgb-orange) / 0%)  70%),

    /* Halo rojo profundo, se derrama hacia el centro-izquierda */
    radial-gradient(105% 78% at 92% -6%,
      rgb(var(--rgb-red) / 26%) 0%,
      rgb(var(--rgb-red) / 8%)  40%,
      rgb(var(--rgb-red) / 0%)  78%),

    /* Rescoldo inferior izquierdo — cierra la composición (visible en el
       mockup web: el degradado sube desde abajo) */
    radial-gradient(96% 52% at 4% 106%,
      rgb(var(--rgb-red) / 15%) 0%,
      rgb(var(--rgb-orange) / 6%) 38%,
      rgb(var(--rgb-red) / 0%)  74%);

  /* La luz SUMA. `screen` reproduce el comportamiento físico; apilar en
     `normal` daría un lavado sucio y apagado. `normal` en la última capa
     porque es la que se asienta sobre el color base. */
  background-blend-mode: screen, screen, screen, normal;
}
```

### 2.5 Capa 2 — glifos (chevrones y hexágonos redondeados)

**El problema:** `clip-path: polygon()` no admite radio en los vértices, y `border`
no se aplica a una forma recortada. **La solución:** un SVG en data-URI usado como
`mask-image`, donde la forma se dibuja como *trazo* con `stroke-linejoin="round"`.
Eso produce exactamente la geometría del isotipo AIVI (hexágono y chevron de esquinas
redondeadas), y como es una máscara, el relleno puede ser cualquier degradado — así
el glifo "recoge" la luz como el vidrio de las piezas.

```css
/* ── Definición de los glifos como máscaras SVG ────────────────────────────
   Hexágono relleno con vértices redondeados: fill + stroke del mismo color y
   stroke-linejoin:round. El trazo de 28 u expande la forma 14 u hacia fuera,
   por eso el path va inset dentro del viewBox 200×174.                      */
.bg__glyphs {
  z-index: 2;

  --mask-hex:
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 174'%3E%3Cpath d='M64 26H136L172 87L136 148H64L28 87Z' fill='%23fff' stroke='%23fff' stroke-width='28' stroke-linejoin='round'/%3E%3C/svg%3E");

  /* Contorno del mismo hexágono (para el borde de 1px translúcido).
     stroke-width en unidades de viewBox: el hairline visible en px es
     stroke-width × (tamañoRenderizadoPx / 200).
     A 720 px de render, 0.45 u ≈ 1.6 px. Ajustar si cambia --glyph-size.     */
  --mask-hex-edge:
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 174'%3E%3Cpath d='M64 26H136L172 87L136 148H64L28 87Z' fill='none' stroke='%23fff' stroke-width='0.45' stroke-linejoin='round'/%3E%3C/svg%3E");

  /* Chevron: la "flecha" del isotipo. Polilínea gruesa con juntas y extremos
     redondeados — es literalmente la forma AIVI. */
  --mask-chevron:
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 120 180'%3E%3Cpath d='M28 26L88 90L28 154' fill='none' stroke='%23fff' stroke-width='38' stroke-linejoin='round' stroke-linecap='round'/%3E%3C/svg%3E");
}

.bg__glyph {
  position: absolute;
  display: block;

  /* Relleno vidrio: el glifo es una superficie apenas más clara que el fondo,
     iluminada desde arriba-izquierda. Nunca gris opaco. */
  background-image: linear-gradient(158deg,
    rgb(var(--rgb-white) / 6.5%) 0%,
    rgb(var(--rgb-white) / 2.2%) 44%,
    rgb(var(--rgb-white) / 4%)  100%);

  mask-image: var(--glyph-mask);
  mask-repeat: no-repeat;
  mask-size: 100% 100%;
  -webkit-mask-image: var(--glyph-mask);
  -webkit-mask-repeat: no-repeat;
  -webkit-mask-size: 100% 100%;
}

/* El borde translúcido de 1px: misma máscara en versión contorno,
   sobre un pseudoelemento. Un solo nodo extra por glifo. */
.bg__glyph::after {
  content: "";
  position: absolute;
  inset: 0;
  background: rgb(var(--rgb-white) / 26%);
  mask-image: var(--glyph-mask-edge);
  mask-repeat: no-repeat;
  mask-size: 100% 100%;
  -webkit-mask-image: var(--glyph-mask-edge);
  -webkit-mask-repeat: no-repeat;
  -webkit-mask-size: 100% 100%;
}

/* ── Instancias. Solo TRES. Cada glifo adicional es otra máscara que
   rasterizar; el techo en móvil son 3. Todas se recortan por el viewport
   (overflow:hidden en .bg) → posiciones negativas a propósito.
   Inclinación 20–25° según la guía.                                        */

.bg__glyph--hex-a {
  --glyph-mask: var(--mask-hex);
  --glyph-mask-edge: var(--mask-hex-edge);
  width: clamp(20rem, 62vmax, 52rem);
  aspect-ratio: 200 / 174;
  top: -14vmax;
  right: -18vmax;
  rotate: -22deg;
}

.bg__glyph--hex-b {
  --glyph-mask: var(--mask-hex);
  --glyph-mask-edge: var(--mask-hex-edge);
  width: clamp(17rem, 52vmax, 44rem);
  aspect-ratio: 200 / 174;
  top: 34vmax;
  right: -26vmax;
  rotate: -22deg;
  opacity: 0.72;
}

.bg__glyph--chevron {
  --glyph-mask: var(--mask-chevron);
  --glyph-mask-edge: var(--mask-chevron);   /* el chevron no lleva borde propio */
  width: clamp(11rem, 34vmax, 26rem);
  aspect-ratio: 120 / 180;
  bottom: -8vmax;
  left: -12vmax;
  rotate: 24deg;
  opacity: 0.5;
}
.bg__glyph--chevron::after { display: none; }
```

Se usa `vmax` (no `vw` ni `vh`) para que en móvil vertical el glifo escale con la
altura y no quede una mancha diminuta arriba a la derecha, y se usa la propiedad
individual `rotate` en lugar de `transform` para no colisionar con una posible
animación de `transform` posterior.

### 2.6 Capa 3 — haces de luz diagonales (la parte difícil)

Dos elementos, cada uno con una responsabilidad:

- **`.bg__beams`** (rotado): dibuja las bandas de luz con `linear-gradient`. Los
  bordes suaves y el núcleo casi blanco son *stops* del gradiente.
- **`.bg__beams-wrap`** (sin rotar): aplica la `mask-image` radial que hace que la
  luz "entre" desde la esquina superior derecha y se disipe. Está separado porque
  una máscara se resuelve en el sistema de coordenadas **local** del elemento: si
  estuviera en el elemento rotado, `at 100% 0%` no sería la esquina del viewport.

```css
.bg__beams-wrap {
  z-index: 3;
  overflow: hidden;               /* reduce el área de pintado */

  /* La luz nace en la esquina superior derecha y muere hacia el centro-abajo.
     Esta máscara es lo que convierte bandas infinitas en "haces que entran". */
  --beam-falloff: radial-gradient(128% 104% at 100% -4%,
      rgb(0 0 0 / 100%)  0%,
      rgb(0 0 0 / 92%)  24%,
      rgb(0 0 0 / 52%)  50%,
      rgb(0 0 0 / 16%)  72%,
      rgb(0 0 0 / 0%)   92%);

  mask-image: var(--beam-falloff);
  -webkit-mask-image: var(--beam-falloff);
}

.bg__beams {
  --beam-angle: -23deg;           /* dentro del rango 20–25° de la guía */

  position: absolute;
  /* Sobredimensionado para que el rectángulo rotado cubra el viewport
     completo en cualquier relación de aspecto. 220% ≥ √2 × 100% + margen. */
  top: -60%;
  left: -60%;
  width: 220%;
  height: 220%;
  transform: rotate(var(--beam-angle));
  transform-origin: 62% 38%;

  /* Cada linear-gradient(90deg,…) es UN haz. Los % son fracciones del ancho
     del elemento rotado. El difuminado del borde = distancia entre stops.
     ⚠️ Aquí NO hay filter: blur(). Es lo que hace que esto sea viable en móvil. */
  background-image:
    /* ── Haz 1 — el principal, con núcleo especular casi blanco ───────── */
    linear-gradient(90deg,
      transparent                          0%,
      rgb(var(--rgb-red) / 0%)            40.0%,
      rgb(var(--rgb-red) / 34%)           45.2%,
      rgb(var(--rgb-orange) / 68%)        47.6%,
      rgb(var(--beam-core) / 92%)         49.1%,
      rgb(var(--beam-core) / 98%)         49.7%,
      rgb(var(--rgb-gold) / 74%)          50.6%,
      rgb(var(--rgb-orange) / 30%)        53.0%,
      rgb(var(--rgb-red) / 0%)            58.0%,
      transparent                        100%),

    /* ── Haz 2 — secundario ancho y difuso, da volumen ────────────────── */
    linear-gradient(90deg,
      transparent                          0%,
      rgb(var(--rgb-orange) / 0%)         50.0%,
      rgb(var(--rgb-orange) / 26%)        58.0%,
      rgb(var(--rgb-gold) / 40%)          62.0%,
      rgb(var(--rgb-orange) / 18%)        67.0%,
      rgb(var(--rgb-red) / 0%)            76.0%,
      transparent                        100%),

    /* ── Haz 3 — filo dorado fino, muy separado: rompe la simetría ────── */
    linear-gradient(90deg,
      transparent                          0%,
      rgb(var(--rgb-gold) / 0%)           32.0%,
      rgb(var(--rgb-gold) / 30%)          35.4%,
      rgb(var(--beam-core) / 46%)         36.2%,
      rgb(var(--rgb-orange) / 22%)        37.6%,
      rgb(var(--rgb-red) / 0%)            42.0%,
      transparent                        100%),

    /* ── Sombra de contacto: oscurece justo al lado del haz principal.
          Sin esto la luz flota; con esto parece atravesar el vidrio. ───── */
    linear-gradient(90deg,
      transparent                          0%,
      rgb(0 0 0 / 0%)                     58.0%,
      rgb(0 0 0 / 34%)                    63.0%,
      rgb(0 0 0 / 0%)                     72.0%,
      transparent                        100%);

  /* screen para los tres haces (suman luz), multiply para la sombra. */
  background-blend-mode: screen, screen, screen, multiply;
}
```

**Por qué los stops están tan juntos (0.6 %–2 %):** ahí está el truco. Un
`linear-gradient` con stops a 0.6 % de distancia produce una transición de ~4–8 px
en pantalla — indistinguible de un `blur` pequeño, y se rasteriza en el mismo pase
que el resto del fondo, con coste ~0. Un `filter: blur(40px)` sobre un elemento de
pantalla completa cuesta, en un móvil de gama media, entre 15 y 50 ms **por
repintado** y fuerza una capa de composición aparte.

### 2.7 Capas 4 y 5 — viñeta y grano

```css
/* Caída a negro en los bordes: "fondo casi negro, nunca negro puro, con
   caída a negro en los bordes" (guía AIVI). Va DESPUÉS de los haces para
   que también los apague en las esquinas. */
.bg__vignette {
  z-index: 4;
  background-image:
    radial-gradient(124% 92% at 50% 42%,
      rgb(0 0 0 / 0%)    38%,
      rgb(0 0 0 / 26%)   72%,
      rgb(0 0 0 / 62%)  100%);
}

/* Grano. feTurbulence en data-URI, TESELADO.
   - stitchTiles='stitch' → el tile es continuo al repetirse, sin costuras.
   - feColorMatrix saturate 0 → ruido monocromo (el color lo dan las capas
     de abajo a través del blend).
   - background-size fijo y pequeño → el navegador rasteriza 128×128 px una
     vez y lo repite. Generarlo a tamaño de viewport es el error caro. */
.bg__grain {
  z-index: 5;
  background-image:
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='128' height='128'%3E%3Cfilter id='n' x='0' y='0' width='100%25' height='100%25'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.82' numOctaves='2' stitchTiles='stitch' seed='7'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='128' height='128' filter='url(%23n)'/%3E%3C/svg%3E");
  background-repeat: repeat;
  background-size: 128px 128px;

  /* overlay conserva los negros y aviva los medios tonos: el grano se ve
     sobre el degradado cálido y casi desaparece en las zonas negras,
     igual que en la pieza original. */
  mix-blend-mode: overlay;
  opacity: 0.055;
}
```

Ajuste de `baseFrequency`: 0.82 da un grano fino apropiado a 2×–3× DPR. Si en un
monitor 1× se ve demasiado marcado, bajar `background-size` a 96 px antes que subir
`baseFrequency` (mismo resultado visual, tile más pequeño = menos rasterizado).

### 2.8 Apilamiento: por qué esto no rompe el contenido

Tres reglas y una explicación:

```css
/* 1. El contenido vive en su propio nivel, por encima del fondo. */
main,
header,
footer {
  position: relative;
  z-index: var(--z-content);   /* 1 */
}
```

2. `.bg` tiene `isolation: isolate`. Eso crea un *stacking context* y, más
   importante, un **grupo de aislamiento de composición**: el `mix-blend-mode:
   overlay` del grano solo puede mezclarse con sus hermanos dentro de `.bg`. Sin
   `isolation`, el grano buscaría el *backdrop* más cercano y en la práctica
   arrastraría al `<body>` a un grupo de composición común — que es la causa
   habitual de "el texto se ve raro / grisáceo / se recorta" en fondos de este tipo.

3. Los `z-index` de las capas del fondo (1…5) son **locales** a `.bg` y no compiten
   con `--z-sticky`, `--z-modal`, etc. Por eso los tokens de la §12 empiezan en
   `--z-content: 1` y el siguiente salto es 10: el rango 1–9 está reservado a
   subárboles aislados como este.

4. Ningún componente de contenido puede declarar `mix-blend-mode`, `filter`, ni
   `opacity < 1` sobre un contenedor grande: cualquiera de las tres crea un contexto
   de apilamiento y, si envuelve texto, lo saca del pase de subpixel-antialiasing
   (el texto se ve más fino y borroso sobre fondo oscuro). Para atenuar un bloque,
   atenuar los hijos, no el contenedor.

**Promoción a capas GPU — la regla dura.** El fondo debe tener **exactamente cero
capas compositadas propias**. Ninguna de las 5 capas lleva `will-change`,
`translateZ(0)`, `backface-visibility` ni animación de `transform`/`opacity`. El
`rotate()` estático de `.bg__beams` no promueve nada. Resultado: el navegador pinta
las 5 capas en **una sola** textura de pantalla completa, una vez, y al hacer scroll
solo la desplaza (de hecho no la desplaza: es `fixed`). Si se añade `will-change:
transform` a las capas, pasan a ser 5 texturas RGBA de viewport completo: en un
teléfono de 1290×2790 son ~14 MB cada una, ~70 MB de memoria de GPU, y en gamas
medias eso provoca reciclado de texturas y caídas a 20 fps.

**Movimiento ambiente (opcional, desactivado por defecto).** Si se quiere una deriva
lenta de la luz, es la única excepción y va con tres candados:

```css
/* Solo en punteros finos (≈ desktop), solo si el usuario no pidió menos
   movimiento, y solo animando `translate` del contenedor de haces. */
@media (prefers-reduced-motion: no-preference) and (hover: hover) and (pointer: fine) {
  .bg__beams {
    animation: beam-drift var(--dur-ambient) var(--ease-in-out) infinite alternate;
    will-change: transform;   /* aquí SÍ, porque sí se anima */
  }
  /* Al animar los haces, el grano de encima con mix-blend-mode obligaría a
     recomponer la mezcla en cada frame. Se cambia a opacidad plana. */
  .bg__grain {
    mix-blend-mode: normal;
    opacity: 0.04;
  }
}

@keyframes beam-drift {
  from { transform: rotate(var(--beam-angle)) translate3d(0, 0, 0); }
  to   { transform: rotate(var(--beam-angle)) translate3d(-3%, 1.5%, 0); }
}
```

Recomendación: **dejarlo fuera de la v1.** El fondo estático ya lee como las piezas
AIVI, y una capa animada de pantalla completa es el mayor riesgo de INP/fps del
proyecto.

### 2.9 Excepción documentada: literales en `background.css`

Las 4 capas usan `rgb(var(--rgb-*) / N%)` con alphas literales. Tokenizar 40 alphas
decorativas (`--beam1-stop3-alpha`) sería peor: nadie las reutiliza, y el degradado
solo tiene sentido leído entero. El contrato se cumple igual porque **los componentes
RGB sí vienen de tokens**: cambiar `--rgb-orange` recolorea todo el fondo.

### 2.10 Coste en móvil: qué usar y qué evitar

| Evitar | Coste | Alternativa que sí se usa |
|---|---|---|
| `filter: blur()` sobre elemento a pantalla completa | 15–50 ms por repintado + capa compositada extra + `blur` es una propiedad **no** compositable en muchos casos | stops de `linear-gradient` muy próximos (§2.6) |
| `backdrop-filter: blur()` en el fondo o en varias tarjetas | Lee el backdrop, lo desenfoca y lo recompone **cada frame** en el que algo cambie encima. En Safari iOS con 8 tarjetas glass ≈ scroll a 25–35 fps | `--grad-surface-glass` + borde translúcido + `--ring-top`. Visualmente equivalente sobre un fondo oscuro y de coste ~0 |
| `feTurbulence` a tamaño de viewport | Rasterizado de 20–60 ms y ~10 MB de bitmap | tile de 128 px con `stitchTiles="stitch"` |
| PNG de fondo de pantalla completa | 300–900 KB, decodificación 40–120 ms | gradientes CSS (0 bytes de red) |
| `will-change` en capas del fondo | 5 × ~14 MB de textura GPU | ninguna promoción (§2.8) |
| Animar `background-position` / `background-size` | Repinta la capa entera cada frame | animar `transform` del contenedor |
| `box-shadow` animado | Repinta | `opacity` de un `::after` que ya tiene la sombra |

**Presupuesto de `backdrop-filter`:** máximo **un** elemento en toda la página, de
área pequeña (< 15 % del viewport), y tras `@supports`:

```css
/* Único uso permitido: la píldora de nav/header si llega a existir. */
@supports ((backdrop-filter: blur(8px)) or (-webkit-backdrop-filter: blur(8px))) {
  .nav-pill {
    -webkit-backdrop-filter: blur(10px) saturate(130%);
    backdrop-filter: blur(10px) saturate(130%);
    background: rgb(var(--rgb-black) / 55%);
  }
}
```

### 2.11 Suelo de contraste garantizado

Los haces llevan un núcleo casi blanco. Si un titular blanco cayera encima, el
contraste bajaría a ~1.1:1. Se garantiza estructuralmente, no por suerte:

1. La máscara `--beam-falloff` confina la luz intensa al **cuadrante superior
   derecho**, donde por diseño solo hay glifos decorativos.
2. `.bg__vignette` apaga los bordes donde vive el texto.
3. La columna de contenido lleva su propio velo, y el titular del hero uno extra:

```css
/* Velo local bajo el titular. Garantiza que el sustrato del texto no supere
   ~#262626 (→ blanco ≥ 12:1) aunque el haz se acerque. */
.hero__headline {
  position: relative;
  isolation: isolate;          /* el velo no afecta a nada externo */
}
.hero__headline::before {
  content: "";
  position: absolute;
  inset: -8% -12%;
  z-index: -1;
  background: radial-gradient(78% 116% at 24% 56%,
    rgb(var(--rgb-black) / 74%) 0%,
    rgb(var(--rgb-black) / 42%) 52%,
    rgb(var(--rgb-black) / 0%)  78%);
  pointer-events: none;
}
```

Verificación obligatoria antes de cerrar: capturar el hero en 375×667, 390×844 y
1440×900, y muestrear con un medidor de contraste **3 puntos** por captura —
esquina superior izquierda del titular, centro y última línea.

---

## 3. Estrategia de layout — `css/layout.css`

### 3.1 Reset y base (`css/reset.css`)

```css
*, *::before, *::after { box-sizing: border-box; }

* { margin: 0; }

html {
  -webkit-text-size-adjust: 100%;
  text-size-adjust: 100%;
  scroll-behavior: smooth;
  /* Compensa cabeceras sticky y hace que los anclajes no queden pegados. */
  scroll-padding-block-start: var(--space-8);
  /* Evita el salto horizontal cuando aparece/desaparece el scrollbar. */
  scrollbar-gutter: stable;
}

body {
  min-height: 100svh;
  background-color: var(--bg-base);
  color: var(--text-primary);
  font-family: var(--font-sans);
  font-size: var(--step-0);
  font-weight: var(--fw-regular);
  line-height: var(--lh-relaxed);
  letter-spacing: var(--ls-normal);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-rendering: optimizeLegibility;
  overflow-x: clip;             /* nunca scroll horizontal por los glifos */
}

img, picture, svg, video, canvas {
  display: block;
  max-width: 100%;
  height: auto;
}
/* Todo <img> DEBE llevar width/height en el HTML: CLS = 0. */

input, button, textarea, select { font: inherit; color: inherit; }

h1, h2, h3, h4 {
  font-weight: var(--fw-black);
  line-height: var(--lh-snug);
  letter-spacing: var(--ls-tight);
  text-wrap: balance;           /* titulares sin viudas */
}

p, li { text-wrap: pretty; }

ul[role="list"], ol[role="list"] { list-style: none; padding: 0; }

a { color: var(--text-link); text-decoration-thickness: 1px; text-underline-offset: 0.18em; }

:target { scroll-margin-block-start: var(--space-10); }
```

### 3.2 El grid maestro: full-bleed sin una sola media query

Una única cuadrícula con columnas nombradas resuelve contenedor, gutters y sangrado
completo. Es la pieza que elimina la mayoría de las media queries.

```css
.layout {
  display: grid;
  grid-template-columns:
    [full-start]
      minmax(var(--gutter), 1fr)
    [wide-start]
      minmax(0, calc((var(--w-wide) - var(--w-content)) / 2))
    [content-start]
      min(var(--w-content), 100% - var(--gutter) * 2)
    [content-end]
      minmax(0, calc((var(--w-wide) - var(--w-content)) / 2))
    [wide-end]
      minmax(var(--gutter), 1fr)
    [full-end];

  /* El ritmo vertical del documento (§3.4) */
  row-gap: var(--space-section);
  align-content: start;
  padding-block: var(--space-section) var(--space-12);
}

/* Por defecto TODO va a la columna de contenido. Cero clases necesarias. */
.layout > * { grid-column: content; }

/* Tres escapes explícitos */
.layout > .u-wide  { grid-column: wide; }   /* carrusel, grid de tarjetas */
.layout > .u-full  { grid-column: full; }   /* bandas de color, separadores */

/* Un hijo que necesita sangrar solo hacia un lado */
.layout > .u-bleed-end   { grid-column: content-start / full-end; }
.layout > .u-bleed-start { grid-column: full-start / content-end; }
```

Comportamiento resultante, sin ninguna `@media`:

| Viewport | Columna de contenido | Gutter efectivo |
|---|---|---|
| 320 px | 320 − 2×20 = 280 px | 20 px |
| 375 px | 375 − 2×21 = 333 px | ~21 px |
| 600 px | 544 px (tope `--w-content`) | 28 px |
| 1024 px | 544 px, centrada | resto |
| 1440 px | 544 px, `.u-wide` = 1024 px | resto |

`min(var(--w-content), 100% - var(--gutter) * 2)` es el núcleo: por debajo del punto
en que caben 544 px + gutters, la columna se encoge sola respetando el gutter.

### 3.3 Grid intrínseco para las colecciones

Ni una media query en las rejillas de contenido:

```css
/* Iconos de redes: se acomodan solos, 1 fila en móvil, siguen centrados. */
.socials {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: var(--space-3);
}
.socials__link {
  display: grid;
  place-items: center;
  inline-size: max(var(--tap-min), 3rem);
  block-size: max(var(--tap-min), 3rem);
}

/* Tarjetas / logros: auto-fit + minmax con min() interno para que nunca
   desborde por debajo de 320 px. */
.card-grid {
  display: grid;
  gap: var(--space-4);
  grid-template-columns: repeat(auto-fit, minmax(min(15rem, 100%), 1fr));
}

/* Botones de enlace (el corazón del link-in-bio): pila de 1 columna siempre.
   No se convierten en 2 columnas ni en desktop — es un link-in-bio, la
   columna única es la decisión de diseño, no una limitación. */
.link-stack {
  display: grid;
  gap: var(--space-3);
}

/* Carrusel: scroll-snap nativo, cero JS para el desplazamiento.
   OJO: no aplicar content-visibility ni contain:paint a un scroller. */
.carousel {
  display: grid;
  grid-auto-flow: column;
  grid-auto-columns: clamp(11rem, 42vw, 15rem);
  gap: var(--space-4);
  overflow-x: auto;
  overscroll-behavior-inline: contain;
  scroll-snap-type: inline mandatory;
  scroll-padding-inline: var(--gutter);
  padding-inline: var(--gutter);
  scrollbar-width: none;
}
.carousel::-webkit-scrollbar { display: none; }
.carousel > * { scroll-snap-align: center; }
```

### 3.4 Ritmo vertical

Tres escalas, y nada más. Todo el espaciado vertical del documento sale de aquí:

| Nivel | Token | 375 px | 1440 px | Uso |
|---|---|---|---|---|
| Entre secciones | `--space-section` | 56 px | 112 px | `row-gap` del `.layout` |
| Entre bloques dentro de sección | `--space-block` | 24 px | 40 px | título → contenido |
| Entre elementos de un bloque | `--space-stack` | 12 px | 20 px | párrafo → párrafo |

```css
/* El gap del grid maestro ya separa secciones: prohibido añadir
   margin-block a las secciones. Un solo mecanismo. */
.section {
  display: grid;
  row-gap: var(--space-block);
  align-content: start;
}
.stack { display: grid; row-gap: var(--space-stack); }

/* Bloques de prosa: ancho de lectura + centrado, sin contenedor extra. */
.prose {
  max-inline-size: var(--measure);
  margin-inline: auto;
  color: var(--text-secondary);
  text-align: center;    /* según ref-layout-bio.png */
}
.prose > * + * { margin-block-start: 1em; }
```

### 3.5 Inventario completo de media queries

El proyecto entero tiene **exactamente 5** bloques `@media`. Cualquier añadido
requiere justificar por qué `clamp()` o el grid intrínseco no bastan.

| # | Query | Qué hace | Archivo |
|---|---|---|---|
| 1 | `(prefers-reduced-motion: reduce)` | §5.1 | `reset.css` |
| 2 | `(prefers-contrast: more)` | §5.5 | `reset.css` |
| 3 | `(prefers-reduced-transparency: reduce)` | §5.5 | `background.css` |
| 4 | `(hover: hover) and (pointer: fine)` | encierra **todos** los `:hover` | `components.css` |
| 5 | `(min-width: 48rem)` | única de ancho: bio en 2 columnas (avatar \| texto) | `layout.css` |

```css
/* Media query #4 — los :hover solo existen donde hay puntero.
   Evita el "hover pegado" en táctil. */
@media (hover: hover) and (pointer: fine) {
  .btn-fire:hover { transform: translateY(-2px); box-shadow: var(--glow-fire-strong); }
  .link-card:hover { background-image: var(--grad-surface-glass); }
}

/* Media query #5 — la única de ancho en todo el proyecto. */
@media (min-width: 48rem) {
  .bio {
    grid-template-columns: auto 1fr;
    column-gap: var(--space-6);
    align-items: center;
    text-align: start;
  }
  .bio .prose { text-align: start; margin-inline: 0; }
}
```

---

## 4. Tipografía Hanken Grotesk

### 4.1 Auto-hospedar vs Google Fonts — comparativa

| Criterio | Google Fonts (`fonts.googleapis.com`) | Auto-hospedado en `assets/fonts/` |
|---|---|---|
| Conexiones de red | 2 orígenes extra (`googleapis` + `gstatic`): DNS + TCP + TLS. En 4G ≈ **150–350 ms** antes del primer byte de la fuente | 0. Reutiliza la conexión ya abierta y calentada |
| Cadena de peticiones | CSS → (parse) → woff2. **Dos saltos serializados** en la ruta crítica | Un salto, y `preload` lo arranca junto al HTML |
| Caché entre sitios | Eliminada. Todos los navegadores modernos particionan la caché HTTP por sitio: el "ya lo tiene cacheado de otra web" **ya no existe** desde 2020 | Irrelevante |
| `preload` fiable | Frágil: la URL del woff2 la decide el CSS remoto y puede cambiar | Trivial y estable |
| Peso | Subset `latin` que decide Google | Controlamos el subset exacto |
| Dependencias externas | Rompe el requisito explícito "sin dependencias externas" | Cumple |
| Privacidad / RGPD | Petición a Google con IP del visitante en cada carga | Ninguna |
| Fallo del tercero | Bloquea el render de la fuente | Imposible |

**Recomendación: auto-hospedar.** No es una preferencia estética — en este proyecto
elimina el único origen de red de terceros y quita dos saltos serializados del
camino crítico del LCP, que en un link-in-bio *es* un titular de texto.

### 4.2 Preparación del archivo

Un solo archivo: variable, upright (sin cursiva), subset latin + latin-ext.

```bash
pip install "fonttools[woff]" brotli

# Fuente: descargar HankenGrotesk[wght].ttf del repo oficial de Google Fonts
pyftsubset HankenGrotesk\[wght\].ttf \
  --output-file=assets/fonts/hkgrotesk-var-latin.woff2 \
  --flavor=woff2 \
  --layout-features='kern,liga,calt,ccmp,locl,mark,mkmk' \
  --unicodes='U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+2074,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD' \
  --desubroutinize --no-hinting \
  --variations='wght=100:900'
```

Incluye `U+00C1 Á U+00D1 Ñ U+00FA ú U+00BF ¿ U+00A1 ¡` (dentro de `0000-00FF`):
imprescindible para el copy en español. Tamaño esperado: **26–34 KB**.

### 4.3 `@font-face` y anti-CLS

```css
/* ── tokens.css, al final del archivo ───────────────────────────────────── */

@font-face {
  font-family: "Hanken Grotesk";
  src: url("/assets/fonts/hkgrotesk-var-latin.woff2") format("woff2-variations");
  font-weight: 100 900;          /* rango del eje wght → font-weight funciona */
  font-style: normal;
  font-display: swap;
  unicode-range:
    U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC,
    U+0304, U+0308, U+0329, U+2000-206F, U+2074, U+20AC, U+2122, U+2191,
    U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
}

/* ── Fuente de respaldo con métricas ajustadas ─────────────────────────────
   Esto es lo que hace que el swap NO mueva el layout: el fallback ocupa
   exactamente el mismo alto de línea y casi el mismo ancho que Hanken.
   ⚠️ VALORES A VERIFICAR contra el binario antes de cerrar (§4.4).           */
@font-face {
  font-family: "Hanken Fallback";
  src: local("Helvetica Neue"), local("Arial"), local("Roboto");
  ascent-override:   97.2%;   /* hhea.ascender  / unitsPerEm */
  descent-override:  23.2%;   /* |hhea.descender| / unitsPerEm */
  line-gap-override: 0%;
  size-adjust:       100%;    /* xHeight(Hanken)/upm ÷ xHeight(Arial)/upm */
}
```

Y en `<head>`, **antes** de cualquier `<link rel="stylesheet">`:

```html
<link rel="preload" href="/assets/fonts/hkgrotesk-var-latin.woff2"
      as="font" type="font/woff2" crossorigin>
```

`crossorigin` es obligatorio incluso en el mismo origen: las fuentes se piden en
modo CORS-anónimo y sin el atributo el navegador descarga el archivo **dos veces**.

### 4.4 Verificación de las métricas (no opcional)

Los tres valores de `ascent-override`/`descent-override`/`size-adjust` deben salir
del binario, no de memoria. Extraerlos así:

```bash
python - <<'PY'
from fontTools.ttLib import TTFont
f = TTFont("HankenGrotesk[wght].ttf")
upm = f["head"].unitsPerEm
print("unitsPerEm     ", upm)
print("hhea ascender  ", f["hhea"].ascent,  "->", round(100*f["hhea"].ascent/upm, 1), "%")
print("hhea descender ", f["hhea"].descent, "->", round(100*abs(f["hhea"].descent)/upm, 1), "%")
print("hhea lineGap   ", f["hhea"].lineGap)
print("OS/2 sxHeight  ", f["OS/2"].sxHeight, "->", round(f["OS/2"].sxHeight/upm, 4))
PY
```

`size-adjust` = `xHeightRatio(Hanken) / xHeightRatio(fallback)` × 100.
Referencias del fallback: Arial `sxHeight/upm = 0.5186`, Helvetica Neue `0.517`.

**Comprobación final del CLS:** en DevTools, panel Rendering → *Layout Shift Regions*,
recargar con la caché de fuentes vacía y verificar que no se dibuja ninguna región
sobre el titular. Objetivo: CLS = 0.00.

### 4.5 Aplicación de la escala

```css
.text-display { font-size: var(--step-5); font-weight: var(--fw-black);
                line-height: var(--lh-tight); letter-spacing: var(--ls-tighter); }
.text-h1      { font-size: var(--step-4); font-weight: var(--fw-black);
                line-height: var(--lh-tight); letter-spacing: var(--ls-tighter); }
.text-h2      { font-size: var(--step-3); font-weight: var(--fw-bold);
                line-height: var(--lh-snug);  letter-spacing: var(--ls-tight); }
.text-h3      { font-size: var(--step-2); font-weight: var(--fw-bold);
                line-height: var(--lh-snug); }
.text-lead    { font-size: var(--step-1); font-weight: var(--fw-light);
                line-height: var(--lh-normal); color: var(--text-secondary); }
.text-body    { font-size: var(--step-0); line-height: var(--lh-relaxed); }
.text-small   { font-size: var(--step--1); color: var(--text-tertiary); }
.text-kicker  { font-size: var(--step--1); font-weight: var(--fw-bold);
                letter-spacing: var(--ls-widest); text-transform: uppercase;
                color: var(--text-highlight); }

/* Jerarquía de marca: última línea / palabra clave en el degradado de fuego
   ("Únete a AIVI" en la pieza social). Se aplica a un <span>, nunca al bloque
   completo, y el texto sigue siendo texto real seleccionable. */
.u-fire-text {
  background-image: var(--grad-text-fire);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  /* Sin esto, Safari recorta descendentes de g/j/y */
  padding-block-end: 0.06em;
  margin-block-end: -0.06em;
}
@supports not ((background-clip: text) or (-webkit-background-clip: text)) {
  .u-fire-text { color: var(--brand-orange); background-image: none; }
}
```

Contraste del texto degradado sobre `#101010`: el extremo más débil es el rojo,
**5.50:1** → cumple WCAG AA a cualquier tamaño. El extremo dorado, 11.86:1. Es
seguro usarlo, aunque por jerarquía se reserva a `--step-3` y superiores.

---

## 5. Accesibilidad y movimiento

### 5.1 `prefers-reduced-motion`

```css
/* reset.css — al final, para ganar por orden */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
  html { scroll-behavior: auto; }

  /* El fondo ya es estático: no hay nada que apagar. Solo el carrusel. */
  .carousel { scroll-snap-type: none; scroll-behavior: auto; }
}
```

`0.01ms` en lugar de `none`: mantiene el disparo de `transitionend` /
`animationend`, del que suele depender el JS de un carrusel. Con `none` esos
eventos no llegan y el componente se queda colgado.

Además, en JS (obligatorio, el CSS no basta):

```js
// carousel.js
const noMotion = matchMedia('(prefers-reduced-motion: reduce)');
let autoplay = null;

function sync() {
  if (noMotion.matches) { clearInterval(autoplay); autoplay = null; }
  else if (!autoplay)   { autoplay = setInterval(next, 6000); }
}
noMotion.addEventListener('change', sync);
sync();

// El autoplay se pausa además con foco dentro, hover, y
// document.visibilityState === 'hidden' (WCAG 2.2.2).
```

### 5.2 `:focus-visible`

El fondo tiene zonas cálidas y claras, así que un anillo de un solo color puede
desaparecer. Se usa un **anillo doble**: halo del color del fondo + anillo dorado.

```css
/* Se elimina el outline por defecto SOLO cuando se va a reemplazar. */
:focus { outline: none; }

:focus-visible {
  outline: var(--focus-ring-width) solid var(--focus-ring-color);
  outline-offset: var(--focus-ring-offset);
  /* Halo oscuro entre el elemento y el anillo: garantiza separación
     también sobre un haz de luz. */
  box-shadow: 0 0 0 var(--focus-ring-offset) var(--focus-halo-color);
  border-radius: inherit;
}

/* Elementos con esquinas propias: el anillo las respeta vía outline
   (los navegadores modernos siguen el border-radius del elemento). */

/* Botón de fuego: el anillo dorado sobre naranja no contrasta.
   Se invierte: halo negro + anillo blanco. */
.btn-fire:focus-visible {
  outline-color: var(--brand-white);
  box-shadow: 0 0 0 var(--focus-ring-offset) var(--brand-black),
              var(--glow-fire);
}

/* Nunca ocultar el foco dentro del carrusel: al tabular a una tarjeta
   fuera de vista el scroller la trae sola. */
.carousel > *:focus-visible { scroll-snap-align: center; }

/* Skip link */
.skip-link {
  position: absolute;
  inset-inline-start: var(--gutter);
  inset-block-start: var(--space-2);
  z-index: var(--z-toast);
  padding: var(--space-2) var(--space-4);
  border-radius: var(--r-pill);
  background: var(--brand-white);
  color: var(--brand-black);
  font-weight: var(--fw-bold);
  translate: 0 -200%;
  transition: translate var(--dur-fast) var(--ease-out);
}
.skip-link:focus-visible { translate: 0 0; }
```

### 5.3 Orden de tabulación

Contrato, verificable con `document.querySelectorAll(':is(a,button,[tabindex]):not([tabindex="-1"])')`:

1. `.skip-link`
2. Enlaces del `.link-stack`, **en orden DOM = orden visual**
3. Controles del carrusel: el track (`tabindex="0"`, `role="region"`,
   `aria-roledescription="carrusel"`, `aria-label`) y después los botones
   prev/next, que van en el DOM **después** del track
4. Enlaces de redes (`<ul role="list">`, cada `<a>` con nombre accesible textual —
   `<span class="visually-hidden">Instagram</span>`, no solo el icono)
5. Enlaces del footer

Reglas duras:
- **Cero `tabindex` positivos.** Solo `0` y `-1`.
- Ninguna reordenación visual con `order`, `row-reverse` o `grid-area` que desalinee
  DOM y pantalla. El grid maestro (§3.2) reordena columnas, nunca el flujo.
- Toda capa decorativa (`.bg` y descendientes) es `aria-hidden="true"`, no contiene
  nada focusable y lleva `pointer-events: none`.
- Objetivo táctil mínimo `var(--tap-min)` = 44 px en todo lo interactivo, incluidos
  los iconos de redes y los puntos del carrusel (los puntos son 8 px visualmente,
  pero con un `::before { inset: -18px }` de área activa).

```css
.visually-hidden {
  position: absolute !important;
  width: 1px; height: 1px;
  margin: -1px; padding: 0;
  overflow: hidden;
  clip-path: inset(50%);
  white-space: nowrap;
  border: 0;
}
```

### 5.4 Verificación de contraste — ratios calculados sobre `#101010`

Luminancia relativa de `#101010` (WCAG 2.x, sRGB): **L = 0.005182**.

| Token | Color efectivo | Ratio vs `#101010` | AA texto normal (4.5) | AA grande (3.0) | AAA (7.0) | Uso permitido |
|---|---|---|---|---|---|---|
| `--text-primary` | `#FAFAFA` | **18.23 : 1** | ✅ | ✅ | ✅ | cualquiera |
| `--text-highlight` / `--brand-gold` | `#FFC252` | **11.86 : 1** | ✅ | ✅ | ✅ | cualquiera, enlaces, anillo de foco |
| `--text-secondary` | `rgba(250,250,250,.72)` → `#B8B8B8` | **9.59 : 1** | ✅ | ✅ | ✅ | cuerpo, bio |
| `--text-accent` / `--brand-orange` | `#FE803F` | **7.59 : 1** | ✅ | ✅ | ✅ | acentos, iconos |
| `--text-tertiary` | `rgba(250,250,250,.56)` → `#939393` | **6.19 : 1** | ✅ | ✅ | ❌ | metadatos, captions ≥ 14 px |
| `--text-emphasis` / `--brand-red` | `#FF413B` | **5.50 : 1** | ✅ | ✅ | ❌ | palabra clave en titulares |
| `--text-faint` | `rgba(250,250,250,.44)` → `#777777` | **4.25 : 1** | ❌ | ✅ | ❌ | **solo decorativo o texto ≥ 24 px**. Nunca copy informativo |
| `--border-default` | `rgba(250,250,250,.12)` → `#2C2C2C` | **1.36 : 1** | — | — | — | solo decorativo. **No** como única señal de un control |
| `--border-strong` | `rgba(250,250,250,.34)` → `#606060` | **3.03 : 1** | — | ✅ (UI 3:1) | — | mínimo válido para borde de control (WCAG 1.4.11) |
| `--brand-black` sobre `--grad-fire` | `#101010` sobre `#FE803F` | **7.59 : 1** | ✅ | ✅ | ✅ | texto del botón de fuego |

Sobre `--surface-glass` (compuesto ≈ `#1C1C1C`, L = 0.011624):

| Texto | Ratio vs glass |
|---|---|
| `--text-primary` | **16.32 : 1** |
| `--text-secondary` | **8.59 : 1** |
| `--text-accent` | **6.79 : 1** |
| `--text-emphasis` | **4.93 : 1** |
| `--text-tertiary` | **4.73 : 1** — límite, no bajar de aquí |

**Consecuencias que se codifican, no se recuerdan:**
- El texto del botón de fuego es **negro** (`--text-on-fire`), no blanco: blanco
  sobre `#FFC252` da 1.54:1 y es un fallo grave. El botón principal del mockup web
  lleva texto claro sobre naranja saturado — se corrige a negro.
- `--text-faint` no puede aparecer en `.prose`, `.text-body` ni `.text-small`.
- Cualquier borde que sea la **única** pista de un control usa `--border-strong`.

### 5.5 Preferencias adicionales

```css
/* reset.css — Media query #2 */
@media (prefers-contrast: more) {
  :root {
    --text-secondary: rgb(var(--rgb-white) / 88%);
    --text-tertiary:  rgb(var(--rgb-white) / 76%);
    --text-faint:     rgb(var(--rgb-white) / 66%);
    --border-default: rgb(var(--rgb-white) / 40%);
    --border-subtle:  rgb(var(--rgb-white) / 28%);
    --surface-glass:  rgb(var(--rgb-white) / 10%);
    --glow-fire: none;
    --glow-fire-strong: none;
  }
  .u-fire-text { color: var(--brand-gold); background-image: none; }
}

/* background.css — Media query #3.
   Menos transparencia = menos ruido visual bajo el texto. */
@media (prefers-reduced-transparency: reduce) {
  .bg__glow    { opacity: 0.55; }
  .bg__beams-wrap { opacity: 0.35; }
  .bg__grain   { display: none; }
  .bg__glyphs  { opacity: 0.4; }
}

/* Modo de contraste forzado (Windows HCM): los fondos decorativos
   desaparecen solos, pero hay que devolver bordes reales. */
@media (forced-colors: active) {
  .bg { display: none; }
  .link-card, .btn-fire { border: 1px solid ButtonText; }
  .u-fire-text { color: LinkText; background-image: none; }
  :focus-visible { outline: 3px solid Highlight; }
}
```

---

## 6. Rendimiento

### 6.1 Presupuesto — cifras vinculantes

Medido en transferencia comprimida (Brotli), primera visita, caché vacía.

| Recurso | Presupuesto | Nota |
|---|---|---|
| `index.html` | **≤ 8 KB** | CSS crítico inline opcional dentro de este límite |
| CSS total (6 archivos) | **≤ 14 KB** | tokens 2.5 · reset 1.5 · background 3.5 · layout 1.5 · components 4 · utilities 1 |
| JS total (3 archivos) | **≤ 5 KB** | sin polyfills, sin librerías, `type="module"`, `defer` |
| Fuente (1 woff2 variable) | **≤ 34 KB** | §4.2 |
| Avatar | **≤ 18 KB** | AVIF, 2 densidades (160/320 px), `width`/`height` en el HTML |
| Miniaturas del carrusel | **≤ 22 KB** cada una, **≤ 130 KB** el total | AVIF + `<source type="image/webp">` de respaldo, `loading="lazy"` salvo la primera |
| Iconos de redes | **0 KB de red** | SVG inline en el HTML, ~180 B cada uno |
| Imagen opcional de la cinta de luz (§2.1) | **≤ 24 KB** | AVIF con alfa, solo si el cliente exige la curvatura exacta |
| Peticiones totales | **≤ 12** | 1 HTML · 6 CSS · 3 JS · 1 fuente · imágenes |
| **Total primera vista** | **≤ 230 KB** | |

Métricas objetivo, en Moto G Power / 4G simulado (Lighthouse mobile):

| Métrica | Objetivo | Límite |
|---|---|---|
| LCP | ≤ 1.6 s | 2.0 s |
| CLS | **0.00** | 0.02 |
| INP | ≤ 90 ms | 150 ms |
| TBT | ≤ 120 ms | 200 ms |
| FCP | ≤ 1.1 s | 1.5 s |
| Lighthouse Performance | ≥ 98 | 95 |
| Lighthouse Accessibility | **100** | 100 |
| fps durante scroll | 60 sostenido | ningún frame > 16.7 ms |

El LCP será el titular del hero → depende de la fuente. Ese es el motivo real de
`preload` + auto-hospedado + `font-display: swap` + métricas de fallback ajustadas:
el texto se pinta con el fallback en el primer frame (FCP bajo), y el swap no
desplaza nada (CLS 0).

Verificación de los archivos CSS en cada commit:

```bash
for f in css/*.css; do
  printf '%-24s %6s B raw  %6s B br\n' "$f" \
    "$(wc -c < "$f")" "$(brotli -q 11 -c "$f" | wc -c)"
done
```

### 6.2 Qué se anima y qué no

**Solo se animan `transform` y `opacity`.** Son las dos únicas propiedades que el
compositor resuelve sin volver a hacer layout ni pintar.

```css
/* ✅ Correcto: transición explícita, propiedad a propiedad. */
.link-card {
  transition:
    transform  var(--dur-base) var(--ease-out),
    opacity    var(--dur-fast) var(--ease-out);
}
.link-card:active { transform: scale(0.985); }

/* ✅ box-shadow / background aparentemente animados: se pre-pintan en un
   ::after y se anima SU opacidad. Cero repintados. */
.link-card { position: relative; isolation: isolate; }
.link-card::after {
  content: "";
  position: absolute;
  inset: 0;
  z-index: -1;
  border-radius: inherit;
  background-image: var(--grad-surface-glass);
  box-shadow: var(--glow-fire), var(--ring-top-hi);
  opacity: 0;
  transition: opacity var(--dur-base) var(--ease-out);
  pointer-events: none;
}
@media (hover: hover) and (pointer: fine) {
  .link-card:hover::after { opacity: 1; }
}
```

**Lista negra — nunca animar ni transicionar:**

| Propiedad | Qué desencadena |
|---|---|
| `width`, `height`, `inline-size`, `block-size` | layout + paint + composite |
| `top`, `right`, `bottom`, `left`, `inset` | layout |
| `margin-*`, `padding-*`, `gap` | layout |
| `font-size`, `line-height`, `letter-spacing` | layout + re-shaping de texto |
| `border-width` | layout |
| `box-shadow`, `text-shadow` | paint de área grande |
| `background-color` en superficies grandes | paint del área completa |
| `background-position`, `background-size` | paint |
| `border-radius` | paint |
| `filter`, `backdrop-filter` | paint costoso, a menudo no compositable |
| `clip-path` | paint (excepción tolerada: áreas < 100×100 px) |
| `transition: all` | **prohibido siempre**: transiciona propiedades que no sabes |

### 6.3 `content-visibility`

Aplicar **solo** a las secciones que empiezan fuera del viewport y que no son
scrollers ni destinos de anclaje frecuentes:

```css
.section--deferred {
  content-visibility: auto;
  /* Obligatorio: sin esto la sección mide 0 px de alto mientras está saltada
     y la barra de scroll salta → CLS. El valor es el alto real medido. */
  contain-intrinsic-size: auto 640px;
}
```

Reglas:
- Máximo **2** secciones (bio larga y footer). Por debajo de ~3 secciones diferidas
  el beneficio es ruido y el riesgo de CLS crece.
- `contain-intrinsic-size` con la palabra clave `auto`: el navegador recuerda el
  tamaño real tras el primer render y ya no vuelve a estimar.
- **Nunca** en `.carousel` ni en ningún ancestro suyo: `content-visibility`
  implica `contain: paint size layout`, y eso rompe el `scroll-snap` y el
  desplazamiento inline.
- **Nunca** en una sección con `id` usada como destino de `#ancla`: el salto puede
  aterrizar antes de que se materialice el contenido.
- Comprobar `Ctrl+F` (find-in-page) tras aplicarlo: es correcto en motores actuales
  pero es el primer síntoma si algo va mal.

### 6.4 `will-change`

**Política: `will-change` no aparece en ningún archivo CSS estático**, con una única
excepción (`.bg__beams`, y solo dentro del bloque de movimiento ambiente, que va
desactivado en v1 — §2.8).

Motivo: `will-change` promueve el elemento a capa de composición **de forma
permanente**, reservando memoria de GPU incluso cuando nada se mueve. Con 8–10
tarjetas declarándolo, el consumo de GPU en un móvil se dispara y el efecto es el
contrario al buscado.

Cuando de verdad haga falta (una transición larga y compleja), se añade y se quita
desde JS, alrededor del gesto:

```js
// main.js — patrón obligatorio si algún día se necesita
function boost(el) {
  el.style.willChange = 'transform';
  el.addEventListener('transitionend', function off() {
    el.style.willChange = '';                 // liberar SIEMPRE
    el.removeEventListener('transitionend', off);
  }, { once: true });
}
```

Alternativas preferidas antes de recurrir a `will-change`:
- Duraciones cortas (`--dur-fast`/`--dur-base`): con < 250 ms el coste de la
  promoción tardía es imperceptible.
- Animar `transform`/`opacity`, que ya se resuelven en el compositor sin necesidad
  de un aviso previo.
- `transform: translate3d(0,0,0)` como truco de promoción: **también prohibido**,
  por el mismo motivo.

### 6.5 Otras decisiones de carga

```html
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="dark">
  <meta name="theme-color" content="#101010">

  <!-- 1º la fuente: es la ruta crítica del LCP -->
  <link rel="preload" href="/assets/fonts/hkgrotesk-var-latin.woff2"
        as="font" type="font/woff2" crossorigin>

  <!-- 2º el CSS, en orden de cascada (§0) -->
  <link rel="stylesheet" href="/css/tokens.css">
  <!-- … -->

  <!-- 3º el JS, siempre diferido -->
  <script type="module" src="/js/main.js" defer></script>
</head>
```

- Los 6 CSS son **6 peticiones**. Sobre HTTP/2/3 con un origen ya conectado el coste
  es marginal y la separación vale la claridad. Si el hosting es HTTP/1.1, y solo
  entonces, concatenar en un único `styles.css` conservando el orden de §0.
- Cero `@import` en CSS: serializa las descargas.
- Imágenes: siempre `<picture>` con AVIF → WebP, `width`/`height` explícitos,
  `loading="lazy"` + `decoding="async"` salvo el avatar (`fetchpriority="high"`).
- `Cache-Control: public, max-age=31536000, immutable` para `assets/fonts/` y
  `assets/img/`; hash en el nombre del archivo al versionar el CSS.

---

## 7. Contrato de entrega para el implementador

Se puede considerar terminado cuando **todo** esto es cierto:

- [ ] `tokens.css` es idéntico a §1. Ningún otro CSS contiene un hex, un `px` de
      espaciado ni un `cubic-bezier` (excepto §2.9).
- [ ] `.bg` está fuera de `<main>`, con `aria-hidden`, `isolation: isolate`,
      `contain: layout paint style`, `pointer-events: none`.
- [ ] `grep -rn "will-change\|translateZ\|backdrop-filter\|filter: *blur" css/`
      devuelve solo las excepciones autorizadas (§2.10, §6.4).
- [ ] `grep -c "@media" css/*.css` suma **5** (§3.5).
- [ ] `grep -rn "transition: *all" css/` no devuelve nada.
- [ ] Los 3 valores de `ascent-override`/`descent-override`/`size-adjust` se han
      extraído del binario con el script de §4.4.
- [ ] CLS = 0.00 con caché de fuentes vacía (Layout Shift Regions).
- [ ] Tabulación completa de la página con teclado: anillo visible en cada paso,
      orden = orden visual, nada focusable dentro de `.bg`.
- [ ] Los 3 puntos de muestreo de contraste del hero (§2.11) pasan a 375, 390 y
      1440 px de ancho.
- [ ] CSS total ≤ 14 KB Brotli, total de primera vista ≤ 230 KB.
- [ ] Lighthouse mobile: Performance ≥ 98, Accessibility = 100.
- [ ] Scroll a 60 fps en un dispositivo real de gama media (no solo en el emulador).
```
