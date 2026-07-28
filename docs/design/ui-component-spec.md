# Jhei Trujillo — Link in Bio · Especificación de componentes UI

**Versión:** 1.0 · **Fecha:** 2026-07-28
**Stack objetivo:** HTML + CSS + JS vanilla. Sin frameworks, sin dependencias, sin build.
**Estrategia:** mobile-first. Breakpoint base 360px, tope de escalado 1440px.
**Fuente de verdad de marca:** `docs/brand/aivi-brand-extract.md`.

> **RESTRICCIÓN DURA HEREDADA:** no se usa el logo ni el isotipo de AIVI en ningún
> componente. Se hereda únicamente **paleta, tipografía (Hanken Grotesk) y lenguaje
> visual** (fondo casi negro, haces de luz cálida, chevrones redondeados, paneles de
> vidrio, grano fino). Los chevrones de este documento son geometría propia descrita
> aquí con coordenadas, no un archivo de AIVI.

Este documento es implementable al pie de la letra. Cada valor es final. Donde
aparece un número no hay margen de interpretación.

---

## 0. Índice

1. [Tokens: color](#1-tokens-color)
2. [Tokens: tipografía y escala fluida](#2-tokens-tipografía-y-escala-fluida)
3. [Tokens: espaciado, radios, sombras, movimiento, z-index](#3-tokens-espaciado-radios-sombras-movimiento-z-index)
4. [Fundamentos globales: fondo, grano, chevrón, foco, layout](#4-fundamentos-globales)
5. [Componente 1 — Hero](#5-componente-1--hero)
6. [Componente 2 — Botón-tarjeta CTA](#6-componente-2--botón-tarjeta-cta)
7. [Componente 3 — Card de colaboración](#7-componente-3--card-de-colaboración)
8. [Componente 4 — Carrusel](#8-componente-4--carrusel)
9. [Componente 5 — Bloque bio](#9-componente-5--bloque-bio)
10. [Componente 6 — Icono de red social](#10-componente-6--icono-de-red-social)
11. [Componente 7 — Footer](#11-componente-7--footer)
12. [Accesibilidad: tabla de contraste medido y reglas](#12-accesibilidad)
13. [prefers-reduced-motion: contrato completo](#13-prefers-reduced-motion-contrato-completo)
14. [Assets: nomenclatura y especificación de export](#14-assets)
15. [Checklist de QA de implementación](#15-checklist-de-qa)

---

## 1. Tokens: color

### 1.1 Paleta base (heredada, sin alterar)

| Token | HEX | Uso |
|---|---|---|
| `--c-ink` | `#101010` | Fondo canónico de la página. Nunca `#000`. |
| `--c-ink-deep` | `#060606` | Caída a negro en bordes del viewport. |
| `--c-ink-warm` | `#1A1310` | Núcleo cálido del fondo, zona superior. |
| `--c-paper` | `#FAFAFA` | Texto primario y glifos. |
| `--c-orange` | `#FE803F` | Tono de acción principal. |
| `--c-gold` | `#FFC252` | Tono de acción / foco / remate. |
| `--c-red` | `#FF413B` | Tono de acción / inicio del fuego. |

### 1.2 Derivados de fuego (calculados para este proyecto)

Necesarios porque los tres tonos puros de la guía son demasiado luminosos para
sostener texto pequeño blanco encima. Son oscurecimientos del mismo hue, no colores
nuevos.

| Token | HEX | Origen |
|---|---|---|
| `--c-fire-900` | `#8A1F0A` | `--c-red` a L≈24% |
| `--c-fire-800` | `#A8280C` | `--c-red` a L≈29% |
| `--c-fire-700` | `#C4380F` | mezcla rojo/naranja a L≈41% |
| `--c-fire-600` | `#E2601F` | `--c-orange` a L≈50% |
| `--c-fire-400` | `#FF9A4A` | `--c-orange` aclarado |
| `--c-fire-200` | `#FFECD6` | núcleo casi blanco del haz de luz |

### 1.3 Superficies de vidrio y escrim

| Token | Valor | Color resultante sobre `#101010` |
|---|---|---|
| `--s-glass` | `rgba(250,250,250,0.045)` | `#1B1B1B` |
| `--s-glass-hover` | `rgba(250,250,250,0.085)` | `#252525` |
| `--s-glass-fire` | `rgba(254,128,63,0.14)` | `#312017` |
| `--s-border` | `rgba(250,250,250,0.12)` | `#2C2C2C` |
| `--s-border-strong` | `rgba(250,250,250,0.20)` | `#3E3E3E` |
| `--s-border-fire` | `rgba(254,128,63,0.42)` | `#583D25` |
| `--s-scrim` | `#0C0806` | base del escrim del CTA |
| `--s-hairline` | `rgba(250,250,250,0.10)` | `#282828` |

### 1.4 Texto

| Token | Valor | Contraste sobre `#101010` |
|---|---|---|
| `--t-primary` | `#FAFAFA` | **18.23:1** |
| `--t-secondary` | `rgba(250,250,250,0.88)` | **14.15:1** |
| `--t-body` | `rgba(250,250,250,0.82)` | **12.33:1** |
| `--t-muted` | `rgba(250,250,250,0.56)` | **6.19:1** |
| `--t-on-fire` | `#FFFFFF` | ver §12.2 |

`--t-muted` es el valor mínimo permitido en toda la página. **No existe texto por
debajo de 6:1.** Prohibido `rgba(250,250,250,0.40)` o inferior para cualquier glifo.

### 1.5 Degradados

```css
/* Fuego brillante — SOLO elementos no textuales y texto ≥26px Black
   (dots activos, anillo del avatar, hairlines, texto con background-clip) */
--grad-fire: linear-gradient(96deg, #FF413B 0%, #FE803F 46%, #FFC252 100%);

/* Fuego profundo — fondo de las tarjetas CTA. Base sobre la que va el escrim. */
--grad-fire-deep: linear-gradient(112deg,
  #8A1F0A 0%,
  #C4380F 34%,
  #E2601F 64%,
  #FF9A4A 100%);

/* Núcleo de luz: la zona casi blanca donde el haz es más intenso.
   Se coloca SIEMPRE en el lado del mockup, nunca bajo texto. */
--grad-core: radial-gradient(130% 190% at 88% 6%,
  rgba(255,236,214,0.44) 0%,
  rgba(255,154,74,0.16) 26%,
  rgba(255,154,74,0.00) 58%);

/* Escrim de legibilidad del CTA — dirección: de la esquina del texto hacia el mockup */
--grad-scrim: linear-gradient(90deg,
  rgba(12,8,6,0.88) 0%,
  rgba(12,8,6,0.78) 38%,
  rgba(12,8,6,0.46) 66%,
  rgba(12,8,6,0.00) 88%);

/* Pie de la card de colaboración */
--grad-collab-foot: linear-gradient(to top,
  #A8280C 0%,
  rgba(196,56,15,0.88) 26%,
  rgba(254,128,63,0.34) 62%,
  rgba(254,128,63,0.00) 100%);

/* Glow del hero */
--grad-hero-glow: radial-gradient(closest-side at 50% 46%,
  rgba(255,140,64,0.55) 0%,
  rgba(255,65,59,0.30) 42%,
  rgba(255,65,59,0.00) 72%);

/* Hairline decorativa (footer, separadores) */
--grad-hairline: linear-gradient(90deg,
  rgba(254,128,63,0.00) 0%,
  rgba(254,128,63,0.55) 50%,
  rgba(254,128,63,0.00) 100%);

/* Anillo del avatar */
--grad-ring: conic-gradient(from 212deg,
  #FF413B 0%, #FE803F 28%, #FFC252 52%, #FE803F 74%, #FF413B 100%);
```

### 1.6 Regla de gobernanza del color cálido

Naranja, dorado y rojo son **tonos de acción**, no colores de texto de lectura.

| Permitido | Prohibido |
|---|---|
| Titulares y palabras clave ≥26px con peso 800/900 | Párrafos de bio |
| Etiquetas ≥16px con peso ≥600 (ej. el handle) | Cualquier texto <16px |
| Iconos, dots, anillos, hairlines, glows, bordes | Microcopy del CTA |
| Foco visible (dorado) | Texto del footer |

Los tres tonos superan AA sobre `#101010` incluso a tamaño pequeño (§12.1). La
restricción es de **jerarquía y fatiga de lectura**, no de contraste: si todo brilla,
nada llama a la acción.

---

## 2. Tokens: tipografía y escala fluida

### 2.1 Familia

**Hanken Grotesk**, variable 100–900, self-hosted en `assets/fonts/`. Sin tipografía
secundaria. Sin fuente de código.

```css
@font-face {
  font-family: 'Hanken Grotesk';
  src: url('../assets/fonts/hanken-grotesk-var.woff2') format('woff2-variations');
  font-weight: 100 900;
  font-style: normal;
  font-display: swap;
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+2000-206F,
                 U+2074, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215;
}

:root {
  --font: 'Hanken Grotesk', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
  --w-light: 300;
  --w-regular: 400;
  --w-semi: 600;
  --w-bold: 800;
  --w-black: 900;
}

html {
  font-family: var(--font);
  font-optical-sizing: auto;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-rendering: optimizeLegibility;
}
```

Precarga obligatoria en `<head>`:
```html
<link rel="preload" href="assets/fonts/hanken-grotesk-var.woff2"
      as="font" type="font/woff2" crossorigin>
```

### 2.2 Escala fluida — clamp() de 360px a 1440px

Cada `clamp()` está resuelto para que a **exactamente 360px** dé el valor mínimo y a
**exactamente 1440px** dé el máximo. Pendiente = (max − min) / 1080 px por px,
expresada en `vw`.

```css
:root {
  /* nombre        360px  →  1440px */
  --fs-display: clamp(2.5rem,    1.4167rem + 4.8148vw, 5.75rem);   /* 40 → 92 */
  --fs-h1:      clamp(2rem,      1.5rem    + 2.2222vw, 3.5rem);    /* 32 → 56 */
  --fs-h2:      clamp(1.625rem,  1.25rem   + 1.6667vw, 2.75rem);   /* 26 → 44 */
  --fs-h3:      clamp(1.25rem,   1.0833rem + 0.7407vw, 1.75rem);   /* 20 → 28 */
  --fs-body-lg: clamp(1.0625rem, 1rem      + 0.2778vw, 1.25rem);   /* 17 → 20 */
  --fs-body:    clamp(1rem,      0.9583rem + 0.1852vw, 1.125rem);  /* 16 → 18 */
  --fs-small:   clamp(0.875rem,  0.8542rem + 0.0926vw, 0.9375rem); /* 14 → 15 */
  --fs-micro:   clamp(0.6875rem, 0.6458rem + 0.1852vw, 0.8125rem); /* 11 → 13 */
  --fs-eyebrow: clamp(0.6875rem, 0.6042rem + 0.3704vw, 0.9375rem); /* 11 → 15 */
}
```

### 2.3 Roles tipográficos completos

Cada rol es una clase utilitaria única. No se redefinen tamaños dentro de los
componentes: los componentes **consumen** estos roles.

| Rol | `font-size` | `font-weight` | `line-height` | `letter-spacing` | `text-transform` | Color |
|---|---|---|---|---|---|---|
| `.ty-display` | `--fs-display` | 900 | `0.88` | `-0.042em` | `uppercase` | `--t-primary` |
| `.ty-h1` | `--fs-h1` | 900 | `0.94` | `-0.032em` | `uppercase` | `--t-primary` |
| `.ty-h2` | `--fs-h2` | 900 | `1.02` | `-0.026em` | `uppercase` | `--t-primary` |
| `.ty-h3` | `--fs-h3` | 800 | `1.12` | `-0.018em` | `none` | `--t-primary` |
| `.ty-eyebrow` | `--fs-eyebrow` | 800 | `1.35` | `+0.16em` | `uppercase` | `--t-secondary` |
| `.ty-body-lg` | `--fs-body-lg` | 400 | `1.60` | `-0.002em` | `none` | `--t-body` |
| `.ty-body` | `--fs-body` | 400 | `1.65` | `0` | `none` | `--t-body` |
| `.ty-label` | `--fs-small` | 700 | `1.30` | `+0.06em` | `uppercase` | `--t-secondary` |
| `.ty-small` | `--fs-small` | 400 | `1.50` | `0` | `none` | `--t-body` |
| `.ty-micro` | `--fs-micro` | 700 | `1.40` | `+0.12em` | `uppercase` | `--t-muted` |

Notas obligatorias:
- Todo lo que sea `uppercase` con peso 900 lleva tracking **negativo**. Todo lo que
  sea `uppercase` con peso ≤800 y tamaño ≤15px lleva tracking **positivo**. No se
  invierte esta regla en ningún componente.
- `line-height` nunca por debajo de `0.88`. El display a `0.88` es intencional: los
  ascendentes de "JHEI TRUJILLO" no colisionan porque no hay descendentes.
- Máximo de línea en párrafos: `max-width: 46ch`.
- `text-wrap: balance` en `.ty-display`, `.ty-h1`, `.ty-h2`. `text-wrap: pretty` en
  párrafos.
- Prohibido `hyphens: auto` (parte los términos de marca).

### 2.4 Texto con degradado (palabra clave en fuego)

```css
.ty-fire {
  background: var(--grad-fire);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  -webkit-text-fill-color: transparent;
}
@supports not ((-webkit-background-clip: text) or (background-clip: text)) {
  .ty-fire { color: #FFC252; background: none; -webkit-text-fill-color: currentColor; }
}
```
Permitido **solo** en `.ty-display`, `.ty-h1`, `.ty-h2`. Nunca en texto <26px.

---

## 3. Tokens: espaciado, radios, sombras, movimiento, z-index

### 3.1 Escala de espaciado — base 4px

```css
:root {
  --sp-0:  0;
  --sp-1:  0.25rem;  /*   4px */
  --sp-2:  0.5rem;   /*   8px */
  --sp-3:  0.75rem;  /*  12px */
  --sp-4:  1rem;     /*  16px */
  --sp-5:  1.25rem;  /*  20px */
  --sp-6:  1.5rem;   /*  24px */
  --sp-7:  2rem;     /*  32px */
  --sp-8:  2.5rem;   /*  40px */
  --sp-9:  3rem;     /*  48px */
  --sp-10: 3.5rem;   /*  56px */
  --sp-11: 4rem;     /*  64px */
  --sp-12: 5rem;     /*  80px */
  --sp-13: 6rem;     /*  96px */
  --sp-14: 8rem;     /* 128px */
}
```

Solo estos catorce valores. Cualquier margen o padding fuera de la escala es un bug,
con dos excepciones documentadas: los offsets ópticos negativos de los mockups del CTA
(§6.5) y el `padding` de 3px del anillo del avatar (§9.2).

### 3.2 Espaciado fluido (secciones y gutter)

```css
:root {
  /* separación vertical entre secciones: 56 → 112px */
  --sp-section: clamp(3.5rem, 2.3333rem + 5.1852vw, 7rem);
  /* padding lateral del shell: 20 → 40px */
  --sp-gutter:  clamp(1.25rem, 0.8333rem + 1.8519vw, 2.5rem);
  /* separación entre tarjetas CTA: 16 → 24px */
  --sp-stack:   clamp(1rem, 0.8333rem + 0.7407vw, 1.5rem);
}
```

### 3.3 Anchos de layout

```css
:root {
  --w-col:  38.75rem;  /* 620px — columna de contenido: CTA, bio, footer */
  --w-wide: 70rem;     /* 1120px — carrusel y arte del hero */
  --w-read: 34rem;     /* 544px — párrafos de bio */
}
```

### 3.4 Radios

```css
:root {
  --r-xs:   0.5rem;   /*  8px — chips, dots pill */
  --r-sm:   0.75rem;  /* 12px — inputs, elementos pequeños */
  --r-md:   1rem;     /* 16px — mockups, thumbs */
  --r-lg:   1.375rem; /* 22px — card de colaboración */
  --r-cta:  1.5rem;   /* 24px — tarjeta CTA en móvil */
  --r-cta-d:1.75rem;  /* 28px — tarjeta CTA ≥600px */
  --r-full: 999px;    /* círculos y pills */
}
```

### 3.5 Sombras

```css
:root {
  --sh-1: 0 1px 2px rgba(0,0,0,0.40);
  --sh-2: 0 6px 18px -6px rgba(0,0,0,0.55);
  --sh-3: 0 18px 40px -14px rgba(0,0,0,0.70);
  --sh-4: 0 28px 64px -20px rgba(0,0,0,0.78);

  --sh-fire:       0 10px 30px -12px rgba(255,88,32,0.35);
  --sh-fire-hover: 0 16px 44px -14px rgba(255,88,32,0.52);
  --sh-fire-soft:  0 8px 24px -10px rgba(255,88,32,0.28);

  --sh-lip:   inset 0 1px 0 rgba(255,255,255,0.22);
  --sh-lip-b: inset 0 -1px 0 rgba(0,0,0,0.28);
  --sh-glass: inset 0 1px 0 rgba(255,255,255,0.10);
}
```

### 3.6 Movimiento

```css
:root {
  --t-1: 120ms;  /* press / feedback inmediato */
  --t-2: 180ms;  /* color, opacidad, borde */
  --t-3: 260ms;  /* transform de hover */
  --t-4: 420ms;  /* desplazamiento de degradado, escala del mockup */
  --t-5: 700ms;  /* entradas y reveals */

  --e-out:    cubic-bezier(0.22, 0.61, 0.36, 1);   /* salida estándar */
  --e-inout:  cubic-bezier(0.65, 0.05, 0.36, 1);   /* bucles */
  --e-spring: cubic-bezier(0.34, 1.40, 0.64, 1);   /* rebote contenido */
  --e-snap:   cubic-bezier(0.16, 1, 0.30, 1);      /* snap del carrusel */
}
```

Regla: **el color usa `--t-2`, el transform usa `--t-3`, el press usa `--t-1`.** Nunca
se anima `all`; siempre se listan las propiedades.

### 3.7 z-index

```css
:root {
  --z-bg:      0;   /* fondo radial fijo */
  --z-grain:   1;   /* capa de grano, pointer-events:none */
  --z-art:     2;   /* halo de chevrones, glow */
  --z-content: 3;   /* texto y componentes */
  --z-raised:  4;   /* mockups que sobresalen del CTA */
  --z-overlay: 5;   /* nada por ahora; reservado */
}
```

---

## 4. Fundamentos globales

### 4.1 Reset mínimo relevante

```css
*, *::before, *::after { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; scroll-behavior: smooth; }
body {
  margin: 0;
  min-height: 100dvh;
  background: var(--c-ink);
  color: var(--t-body);
  font-size: var(--fs-body);
  line-height: 1.65;
  overflow-x: clip;               /* obligatorio: los mockups sobresalen */
}
img, svg, picture { display: block; max-width: 100%; }
button { font: inherit; color: inherit; background: none; border: 0; }
a { color: inherit; text-decoration: none; }
:where(a, button, [tabindex]) { -webkit-tap-highlight-color: transparent; }
```

`overflow-x: clip` en `body` es obligatorio y no negociable: los mockups del CTA y el
halo de chevrones del hero rebasan sus contenedores por diseño.

### 4.2 Fondo de página

Dos capas fijas, ambas `pointer-events: none`.

```css
.bg {
  position: fixed;
  inset: 0;
  z-index: var(--z-bg);
  pointer-events: none;
  background:
    radial-gradient(120% 78% at 50% -6%,
      #1A1310 0%, #141110 34%, #101010 62%, #0A0A0A 100%);
}
```
Vignette de caída a negro en los bordes, como capa aparte para no ensuciar el radial:
```css
.bg::after {
  content: '';
  position: absolute;
  inset: 0;
  background:
    radial-gradient(140% 100% at 50% 50%,
      rgba(6,6,6,0) 52%, rgba(6,6,6,0.55) 84%, rgba(6,6,6,0.85) 100%);
}
```

### 4.3 Grano fino

SVG inline como data-URI. `feTurbulence` con `baseFrequency="0.9"`, `numOctaves="3"`,
teselado a 180×180px.

```css
.grain {
  position: fixed;
  inset: 0;
  z-index: var(--z-grain);
  pointer-events: none;
  opacity: 0.045;
  mix-blend-mode: overlay;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='180' height='180'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='180' height='180' filter='url(%23n)'/%3E%3C/svg%3E");
  background-size: 180px 180px;
}
```
`opacity` final: **0.045**. Por encima de 0.06 el texto pequeño pierde nitidez; por
debajo de 0.03 no se percibe. No animar el grano.

### 4.4 Chevrón — geometría canónica

Único primitivo geométrico del sistema. SVG con juntas redondeadas (no `clip-path`,
que no admite radios).

```html
<svg class="chev" viewBox="0 0 34 44" aria-hidden="true" focusable="false">
  <path d="M9 7 L26 22 L9 37"
        fill="none" stroke="currentColor"
        stroke-width="13" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
```

- `viewBox` fijo `0 0 34 44` · relación 17:22.
- `stroke-width: 13` · `stroke-linecap/linejoin: round` (esto produce las esquinas
  redondeadas del lenguaje AIVI).
- Inclinación canónica de uso decorativo: **`rotate(22deg)`** (rango permitido 20–25°).
- Nunca se rellena (`fill: none`). Nunca lleva color plano brillante en tamaño grande
  sobre el fondo: opacidad máxima decorativa **0.20**.

### 4.5 Foco visible — anillo de dos tonos, global

Un único tratamiento para todo lo interactivo. Es de dos tonos para garantizar 3:1
contra **cualquier** fondo, incluida la tarjeta CTA naranja.

```css
:where(a, button, [tabindex]:not([tabindex="-1"])):focus { outline: none; }

:where(a, button, [tabindex]:not([tabindex="-1"])):focus-visible {
  outline: none;
  box-shadow:
    0 0 0 2px #101010,          /* separador oscuro */
    0 0 0 5px #FFC252,          /* anillo dorado, 11.86:1 sobre #101010 */
    0 0 0 9px rgba(255,194,82,0.18);
  border-radius: inherit;
  transition: box-shadow var(--t-2) var(--e-out);
}
```

- Nunca `outline-offset` como único indicador: en la tarjeta CTA el offset se comería
  el borde redondeado. El `box-shadow` de tres capas es el estándar del proyecto.
- El anillo **nunca** se elimina en `prefers-reduced-motion`; solo se le quita la
  transición.
- El orden del DOM es el orden de tabulación. No hay `tabindex` positivos.

### 4.6 Shell y ritmo de sección

```css
.shell {
  width: 100%;
  max-width: var(--w-col);
  margin-inline: auto;
  padding-inline: var(--sp-gutter);
}
.shell--wide { max-width: var(--w-wide); }

.section { padding-block: var(--sp-section); }
.section--hero { padding-block: 0; }         /* el hero gestiona su propia altura */
.section + .section { padding-block-start: 0; } /* --sp-section del anterior manda */
```

Orden vertical de la página y separaciones exactas:

| # | Bloque | Separación superior |
|---|---|---|
| 1 | Hero | — (100dvh gestionado, §5.1) |
| 2 | Stack de 3 CTA | `--sp-section` (56→112px) |
| 3 | Título "expertos" + carrusel | `--sp-section` |
| 4 | Bloque bio | `--sp-section` |
| 5 | Fila de redes sociales | 40px (`--sp-8`) desde el último párrafo |
| 6 | Footer | 56px (`--sp-10`) |

---

## 5. Componente 1 — Hero

### 5.1 Estructura y caja

```html
<header class="hero">
  <div class="hero__art" aria-hidden="true">
    <div class="hero__glow"></div>
    <div class="hero__halo"><!-- 12 × svg.chev --></div>
  </div>
  <img class="hero__photo" src="assets/img/jhei-hero.webp"
       alt="Jhei Trujillo" width="820" height="1000" fetchpriority="high">
  <div class="hero__text shell">
    <h1 class="ty-display hero__name">Jhei Trujillo</h1>
    <p class="ty-eyebrow hero__tagline">
      Viralidad <span class="hero__dot">·</span>
      Creación de contenido <span class="hero__dot">·</span>
      Inteligencia artificial
    </p>
  </div>
  <a class="scroll-cue" href="#enlaces" aria-label="Ir a los enlaces">…</a>
</header>
```

El texto va en minúsculas/capitalizado en el HTML y se pasa a mayúsculas con CSS
(`text-transform: uppercase`), para que los lectores de pantalla no lo lean letra por
letra.

| Propiedad | <600px | 600–1023px | ≥1024px |
|---|---|---|---|
| `min-height` | `100svh` | `100svh` | `min(100svh, 900px)` |
| `padding-block-start` | `40px` | `48px` | `56px` |
| `padding-block-end` | `24px` | `32px` | `40px` |
| `display` | `grid` | `grid` | `grid` |
| `grid-template-rows` | `1fr auto auto` | `1fr auto auto` | `1fr auto auto` |
| `align-items` | `end` | `end` | `end` |
| `text-align` | `center` | `center` | `center` |
| `position` | `relative` | `relative` | `relative` |
| `isolation` | `isolate` | `isolate` | `isolate` |

Fila 1 = foto + arte. Fila 2 = texto. Fila 3 = indicador de scroll.

### 5.2 Foto recortada

Recorte con fondo eliminado (PNG/WebP con alfa), ver §14.

| Propiedad | <600px | 600–1023px | ≥1024px |
|---|---|---|---|
| `width` | `min(86vw, 340px)` | `min(70vw, 460px)` | `520px` |
| `height` | `auto` | `auto` | `auto` |
| `margin-inline` | `auto` | `auto` | `auto` |
| `margin-block-end` | `-8px` | `-12px` | `-16px` |
| `z-index` | `var(--z-content)` | igual | igual |

Tratamiento fijo en todos los tamaños:
```css
.hero__photo {
  filter:
    drop-shadow(0 18px 34px rgba(0,0,0,0.55))
    drop-shadow(0 0 42px rgba(255,110,50,0.22));
  transform: translateZ(0);
}
```
El margen inferior negativo hace que el nombre "muerda" la base de la foto, igual que
en el layout de referencia.

### 5.3 Glow naranja

```css
.hero__glow {
  position: absolute;
  left: 50%;
  top: 50%;
  translate: -50% -54%;
  width: min(112vw, 720px);
  aspect-ratio: 1 / 1;
  background: var(--grad-hero-glow);
  filter: blur(28px);
  opacity: 0.85;
  z-index: var(--z-art);
}
```

| Propiedad | <600px | ≥600px | ≥1024px |
|---|---|---|---|
| `width` | `min(112vw, 420px)` | `min(90vw, 560px)` | `720px` |
| `filter: blur()` | `22px` | `26px` | `28px` |
| `opacity` | `0.78` | `0.82` | `0.85` |

Animación de respiración (solo ≥600px, se desactiva con reduced-motion):
```css
@keyframes glow-breathe {
  0%,100% { opacity: 0.82; scale: 1;    }
  50%     { opacity: 0.92; scale: 1.04; }
}
.hero__glow { animation: glow-breathe 7s var(--e-inout) infinite; }
```

### 5.4 Halo de chevrones

12 chevrones (§4.4) distribuidos en círculo, cada uno rotado tangencialmente.

```css
.hero__halo {
  position: absolute;
  left: 50%;
  top: 50%;
  translate: -50% -52%;
  width: var(--halo-d);
  aspect-ratio: 1 / 1;
  z-index: var(--z-art);
  animation: halo-spin 48s linear infinite;
}
.hero__halo .chev {
  position: absolute;
  left: 50%;
  top: 50%;
  width: var(--chev-w);
  height: auto;
  color: var(--c-orange);
  transform-origin: 50% 50%;
  /* i = 0..11 → rotate(calc(i * 30deg)) translateY(calc(var(--halo-d)/-2)) rotate(22deg) */
}
@keyframes halo-spin { to { rotate: 360deg; } }
```

| Propiedad | <600px | 600–1023px | ≥1024px |
|---|---|---|---|
| `--halo-d` (diámetro) | `420px` | `600px` | `820px` |
| `--chev-w` | `26px` | `34px` | `44px` |
| Nº de chevrones visibles | 8 (se ocultan los índices 3,4,8,9) | 12 | 12 |
| `opacity` alterna | `0.07 / 0.13` | `0.08 / 0.16` | `0.09 / 0.20` |

La opacidad alterna por índice par/impar para dar profundidad. Máximo absoluto **0.20**.
El halo se recorta por el viewport: eso es intencional ("geometría a gran escala
recortada por el lienzo"). El `body { overflow-x: clip }` lo garantiza sin scroll
horizontal.

### 5.5 Nombre "JHEI TRUJILLO"

```css
.hero__name {
  font-size: var(--fs-display);      /* 40 → 92px */
  font-weight: 900;
  line-height: 0.88;
  letter-spacing: -0.042em;
  text-transform: uppercase;
  color: #FAFAFA;                    /* 18.23:1 */
  text-wrap: balance;
  margin: 0;
  text-shadow: 0 2px 18px rgba(0,0,0,0.45);
}
```

| Breakpoint | Tamaño resuelto | Tracking | Nº de líneas objetivo |
|---|---|---|---|
| 360px | 40px | −1.68px | 2 (JHEI / TRUJILLO) |
| 600px | 51.56px | −2.17px | 1 |
| 1024px | 71.96px | −3.02px | 1 |
| 1440px | 92px | −3.86px | 1 |

A 360px se fuerzan dos líneas con `<br>` no — se usa `max-width: 8ch; margin-inline:
auto` en `<600px` para que el quiebre caiga entre las dos palabras de forma estable.

### 5.6 Subtítulo

```css
.hero__tagline {
  font-size: var(--fs-eyebrow);      /* 11 → 15px */
  font-weight: 800;
  line-height: 1.45;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: rgba(250,250,250,0.88);     /* 14.15:1 */
  margin: 12px 0 0;                  /* --sp-3 */
  max-width: 30ch;
  margin-inline: auto;
  text-wrap: balance;
}
.hero__dot {
  color: #FE803F;                    /* 7.59:1 — separador, no texto de lectura */
  padding-inline: 4px;               /* --sp-1 */
  font-weight: 900;
}
```
En `<600px` el subtítulo cae en 2 o 3 líneas: es correcto y esperado. No se reduce
tracking para forzar una línea.

### 5.7 Indicador de scroll animado

Botón/enlace real, focusable, con nombre accesible.

| Propiedad | Valor |
|---|---|
| `width` / `height` | `44px` / `44px` (área táctil mínima cumplida) |
| `border-radius` | `--r-full` |
| `background` | `rgba(250,250,250,0.045)` |
| `border` | `1px solid rgba(250,250,250,0.12)` |
| `backdrop-filter` | `blur(10px)` |
| `box-shadow` | `--sh-glass` |
| `display` | `grid` + `place-items: center` |
| `margin` | `32px auto 0` (`--sp-7`) |
| Glifo | chevrón §4.4 rotado `90deg`, `width: 12px`, `color: rgba(250,250,250,0.88)` |

```css
@keyframes cue-bob {
  0%, 100% { translate: 0 0;   opacity: 0.72; }
  50%      { translate: 0 6px; opacity: 1;    }
}
.scroll-cue { animation: cue-bob 1800ms var(--e-inout) infinite; }
```

Estados:

| Estado | Cambios | Transición |
|---|---|---|
| default | tal cual arriba | — |
| hover *(solo `@media (hover:hover)`)* | `background: rgba(254,128,63,0.14)`; `border-color: rgba(254,128,63,0.42)`; glifo → `#FE803F`; `box-shadow: var(--sh-fire-soft)` | `background/border-color/color var(--t-2) var(--e-out)`, `box-shadow var(--t-3) var(--e-out)` |
| active | `scale: 0.94` | `scale var(--t-1) var(--e-out)` |
| focus-visible | anillo global §4.5 + `animation-play-state: paused` | `box-shadow var(--t-2) var(--e-out)` |

---

## 6. Componente 2 — Botón-tarjeta CTA

**El componente clave del sitio.** Tres instancias, en este orden:

| # | Título | Microcopy | Mockup | Variante |
|---|---|---|---|---|
| 1 | TALLERES | `CLICK AQUÍ PARA VER LOS TALLERES` | laptop con la landing de talleres | `cta--art-end` |
| 2 | AIVI | `CLICK AQUÍ PARA CONOCER AIVI` | laptop/tablet con la web de AIVI | `cta--art-start` |
| 3 | HABLEMOS POR WHATSAPP | `CLICK AQUÍ PARA ESCRIBIRME` | dos móviles con un chat | `cta--art-end` |

Alternancia: **end → start → end** (derecha, izquierda, derecha).

### 6.1 Markup canónico

```html
<a class="cta cta--art-end" href="…">
  <span class="cta__text">
    <span class="cta__title">Talleres</span>
    <span class="cta__micro">Click aquí para ver los talleres</span>
  </span>
  <span class="cta__art" aria-hidden="true">
    <img src="assets/img/mock-talleres.webp" alt="" width="640" height="440"
         loading="lazy" decoding="async">
  </span>
</a>
```

Un solo `<a>` es la zona clicable completa. No hay elementos interactivos anidados.
El `alt=""` del mockup es correcto: la información ya está en el título y el microcopy.

### 6.2 Caja y capas

```css
.cta {
  position: relative;
  display: grid;
  isolation: isolate;
  border-radius: var(--r-cta);
  background: var(--grad-fire-deep);
  background-size: 180% 180%;
  background-position: 0% 50%;
  box-shadow: var(--sh-fire), var(--sh-3), var(--sh-lip);
  color: #FFFFFF;
  overflow: hidden;              /* móvil: el mockup NO puede salir */
  will-change: transform;
}
.cta::before {                   /* núcleo de luz, lado del mockup */
  content: '';
  position: absolute; inset: 0;
  border-radius: inherit;
  background: var(--grad-core);
  z-index: 1;
  pointer-events: none;
}
.cta::after {                    /* escrim de legibilidad, lado del texto */
  content: '';
  position: absolute; inset: 0;
  border-radius: inherit;
  background: var(--grad-scrim);
  z-index: 2;
  pointer-events: none;
  transition: opacity var(--t-3) var(--e-out);
}
.cta__text { position: relative; z-index: 3; }
.cta__art  { position: relative; z-index: 4; }
```

Variante espejada:
```css
.cta--art-start::before { scale: -1 1; }
.cta--art-start::after  { scale: -1 1; }
```
`scale: -1 1` en los pseudoelementos invierte tanto el núcleo de luz como el escrim,
de modo que el escrim siempre queda **debajo del texto** y la luz siempre en el lado
del mockup, sin duplicar degradados.

### 6.3 Dimensiones por breakpoint

| Propiedad | <600px | 600–899px | ≥900px |
|---|---|---|---|
| `min-height` | `128px` | `156px` | `176px` |
| `border-radius` | `24px` | `28px` | `28px` |
| `padding` | `20px 20px 20px 22px` | `24px 24px 24px 28px` | `28px 28px 28px 34px` |
| `overflow` | `hidden` | `visible` | `visible` |
| `grid-template-columns` | `1fr` (una sola columna) | `1fr 168px` | `1fr 232px` |
| `column-gap` | `0` | `16px` | `20px` |
| `align-items` | `center` | `center` | `center` |
| Separación entre tarjetas | `16px` | `20px` | `24px` |

Para la variante `--art-start` en ≥600px: `grid-template-columns: 168px 1fr` (o
`232px 1fr`) y `.cta__text { grid-column: 2 }`, `.cta__art { grid-column: 1 }`. No se
usa `direction: rtl`.

### 6.4 Texto del CTA

```css
.cta__title {
  display: block;
  font-size: var(--fs-h2);       /* 26 → 44px */
  font-weight: 900;
  line-height: 1.0;
  letter-spacing: -0.026em;
  text-transform: uppercase;
  color: #FFFFFF;
  text-wrap: balance;
  text-shadow: 0 1px 12px rgba(0,0,0,0.40);
}
.cta__micro {
  display: block;
  margin-block-start: 8px;       /* --sp-2 */
  font-size: var(--fs-micro);    /* 11 → 13px */
  font-weight: 700;
  line-height: 1.35;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: rgba(255,255,255,0.90);
}
```

Ajustes por instancia (solo estos, y solo en `<600px`):
- Tarjeta 3 ("HABLEMOS POR WHATSAPP"): `--fs-h2` sustituido por
  `clamp(1.375rem, 1.0417rem + 1.4815vw, 2.5rem)` (22 → 40px) porque son 21
  caracteres. Es la única excepción de tamaño en todo el sistema y va documentada en
  la clase `.cta--long`.
- `max-width` del bloque de texto en `<600px`: `100%`. En ≥600px: `24ch`.

### 6.5 Mockup — y el problema del móvil

**Regla dura: en `<600px` el mockup no ocupa una celda de grid. No le quita ni un
píxel de ancho al texto.** Pasa a ser una capa ambiental recortada por el borde de la
tarjeta.

#### `<600px` — mockup ambiental

```css
@media (max-width: 599.98px) {
  .cta { grid-template-columns: 1fr; }
  .cta__text { grid-area: 1 / 1; width: 100%; }      /* ancho completo */
  .cta__art {
    grid-area: 1 / 1;                                 /* misma celda, superpuesto */
    justify-self: end;
    align-self: end;
    width: 176px;
    margin: 0 -34px -18px 0;                          /* excepción óptica documentada */
    opacity: 0.38;
    filter: saturate(0.85) contrast(1.05);
    pointer-events: none;
  }
  .cta--art-start .cta__art {
    justify-self: start;
    margin: 0 0 -18px -34px;
  }
  .cta::after { background: linear-gradient(90deg,
      rgba(12,8,6,0.90) 0%, rgba(12,8,6,0.86) 46%,
      rgba(12,8,6,0.66) 74%, rgba(12,8,6,0.34) 100%); }
}
```

Por qué funciona:
- El texto dispone del **100%** del ancho interior. A 360px de viewport eso son
  `360 − 40 (gutter) − 42 (padding H) = 278px` para el título. "HABLEMOS POR WHATSAPP"
  a 22px Black entra en 2 líneas.
- El mockup se lee como textura de fuego, no como objeto. `overflow: hidden` lo recorta
  contra el radio de 24px y **no puede generar scroll horizontal**.
- El escrim sube a `0.86–0.90` de alfa: el blanco sobre el mockup mide **15.9:1**
  (§12.2). El mockup nunca compromete la legibilidad.

#### `≥600px` — mockup con celda propia y desborde

```css
@media (min-width: 600px) {
  .cta { overflow: visible; }
  .cta__art {
    width: 100%;
    opacity: 1;
    filter: drop-shadow(0 14px 26px rgba(0,0,0,0.45));
    transform-origin: 50% 60%;
    transition: scale var(--t-4) var(--e-out), translate var(--t-3) var(--e-out);
  }
  .cta__art img { width: 118%; max-width: none; }   /* desborda 18% de su celda */
  .cta--art-end   .cta__art img { margin-inline-start: 0;    }
  .cta--art-start .cta__art img { margin-inline-start: -18%; }
}
```

Reglas del desborde:
- Desborde máximo hacia fuera de la tarjeta: **24px**. Ni un píxel más.
- El desborde vertical superior máximo es **18px**; el inferior, **10px**.
- La sección contenedora **no** lleva `overflow: hidden` (rompería el desborde); el
  control de scroll horizontal lo hace `body { overflow-x: clip }`.

Escalas del mockup: `1` en reposo, `1.045` en hover, `1.015` en active.

### 6.6 Estados

Todos los hover van envueltos en `@media (hover: hover) and (pointer: fine)`.

| Estado | Propiedades exactas | Transición |
|---|---|---|
| **default** | `translate: 0 0`; `background-position: 0% 50%`; `box-shadow: var(--sh-fire), var(--sh-3), var(--sh-lip)`; `.cta__art { scale: 1 }` | — |
| **hover** | `translate: 0 -3px`; `background-position: 100% 50%`; `box-shadow: var(--sh-fire-hover), var(--sh-4), var(--sh-lip)`; `.cta__art { scale: 1.045; translate: 0 -2px }`; `.cta::after { opacity: 0.94 }` | `translate var(--t-3) var(--e-out)`, `box-shadow var(--t-3) var(--e-out)`, `background-position var(--t-4) var(--e-out)`, `scale var(--t-4) var(--e-out)` |
| **active** | `translate: 0 -1px`; `scale: 0.994`; `box-shadow: var(--sh-fire-soft), var(--sh-2), var(--sh-lip-b)`; `.cta__art { scale: 1.015 }` | `translate var(--t-1) var(--e-out)`, `scale var(--t-1) var(--e-out)`, `box-shadow var(--t-1) var(--e-out)` |
| **focus-visible** | anillo global §4.5 (`0 0 0 2px #101010, 0 0 0 5px #FFC252, 0 0 0 9px rgba(255,194,82,0.18)`) **concatenado** con las sombras de reposo | `box-shadow var(--t-2) var(--e-out)` |
| **visited** | sin cambio visual (es navegación externa, no contenido leído) | — |

Nota de implementación del focus: como el anillo y las sombras comparten
`box-shadow`, se declara la lista completa en `:focus-visible`:
```css
.cta:focus-visible {
  box-shadow:
    0 0 0 2px #101010,
    0 0 0 5px #FFC252,
    0 0 0 9px rgba(255,194,82,0.18),
    var(--sh-fire), var(--sh-3), var(--sh-lip);
}
```

`transition-property` declarada, nunca `all`:
```css
.cta {
  transition:
    translate var(--t-3) var(--e-out),
    scale var(--t-1) var(--e-out),
    box-shadow var(--t-3) var(--e-out),
    background-position var(--t-4) var(--e-out);
}
```

---

## 7. Componente 3 — Card de colaboración

Slide del carrusel. Retrato vertical en blanco y negro, degradado de fuego al pie,
logo de la marca sobre el degradado.

### 7.1 Markup

```html
<li class="collab" role="group" aria-label="Colaboración con Zirquit">
  <img class="collab__photo" src="assets/img/collab-01.webp" alt="Retrato de …"
       width="440" height="704" loading="lazy" decoding="async">
  <span class="collab__foot" aria-hidden="true"></span>
  <img class="collab__logo" src="assets/img/logo-zirquit.svg" alt="Zirquit"
       width="120" height="28" loading="lazy">
</li>
```

### 7.2 Caja

| Propiedad | <600px | 600–1023px | ≥1024px |
|---|---|---|---|
| `width` | `62vw` (min 196px, max 240px) | `232px` | `256px` |
| `aspect-ratio` | `5 / 8` | `5 / 8` | `5 / 8` |
| `border-radius` | `18px` | `20px` | `22px` (`--r-lg`) |
| `border` | `1px solid rgba(250,250,250,0.10)` | igual | igual |
| `box-shadow` | `--sh-2` | `--sh-3` | `--sh-3` |
| `overflow` | `hidden` | igual | igual |
| `position` | `relative` | igual | igual |
| `isolation` | `isolate` | igual | igual |
| `background` | `#141414` (color de carga) | igual | igual |

Dimensiones resueltas: 240×384px máximo en móvil, 232×371px en tablet, 256×410px en
desktop.

### 7.3 Retrato

```css
.collab__photo {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: 50% 22%;                 /* la cara arriba, no centrada */
  filter: grayscale(1) contrast(1.08) brightness(0.96);
  transition: filter var(--t-4) var(--e-out), scale var(--t-4) var(--e-out);
}
```
`object-position: 50% 22%` es obligatorio: con `50% 50%` en formato 5:8 el rostro
queda demasiado bajo y el degradado se lo come.

### 7.4 Degradado de fuego al pie

```css
.collab__foot {
  position: absolute;
  inset: auto 0 0 0;
  height: 46%;
  background: var(--grad-collab-foot);
  z-index: 2;
  pointer-events: none;
}
.collab__foot::after {                       /* barra de fuego del canto inferior */
  content: '';
  position: absolute;
  inset: auto 0 0 0;
  height: 3px;
  background: var(--grad-fire);
}
```

| Propiedad | Valor |
|---|---|
| `height` del degradado | `46%` de la altura de la card |
| Banda opaca inferior | `0%–26%` del degradado, `#A8280C` → `rgba(196,56,15,0.88)` |
| Barra de canto | `3px`, `--grad-fire` |
| `mix-blend-mode` | ninguno (evita virar el gris del retrato) |

### 7.5 Logo de la marca

| Propiedad | <600px | ≥600px |
|---|---|---|
| `max-height` | `24px` | `28px` |
| `max-width` | `72%` | `70%` |
| Posición | `bottom: 13%`, centrado horizontal | `bottom: 12%` |
| `filter` | `brightness(0) invert(1) drop-shadow(0 2px 6px rgba(0,0,0,0.55))` | igual |
| `z-index` | `3` | `3` |
| `object-fit` | `contain` | `contain` |

El `bottom: 13%` sitúa el logo dentro de la banda opaca del degradado (0%–26% de un
46% ⇒ 0%–12% de la card): el blanco del logo mide **6.77:1** sobre `#A8280C` (§12.2).
`brightness(0) invert(1)` normaliza cualquier logo (color, negro o blanco) a blanco
puro, requisito para que la especificación de contraste se cumpla con logos que aún no
existen.

### 7.6 Estados

La card no es interactiva por sí misma (no enlaza). Si en el futuro enlaza, se le
aplica el anillo global §4.5 y estos estados; hoy solo el hover decorativo del
carrusel.

| Estado | Cambios | Transición |
|---|---|---|
| default | tal cual arriba | — |
| hover *(hover:hover)* | `.collab__photo { filter: grayscale(0.72) contrast(1.10) brightness(1.02); scale: 1.035 }`; `box-shadow: var(--sh-4)`; `border-color: rgba(254,128,63,0.28)` | `filter var(--t-4) var(--e-out)`, `scale var(--t-4) var(--e-out)`, `box-shadow var(--t-3) var(--e-out)`, `border-color var(--t-2) var(--e-out)` |
| slide activo (centrado) | `border-color: rgba(254,128,63,0.28)`; `box-shadow: var(--sh-3), var(--sh-fire-soft)` | `var(--t-3) var(--e-out)` |
| slide inactivo | `opacity: 0.72` en <600px; `1` en ≥600px | `opacity var(--t-3) var(--e-out)` |

---

## 8. Componente 4 — Carrusel

Scroll-snap nativo + JS mínimo para dots, autoplay y arrastre con puntero.
**Cero dependencias. Funciona sin JS** (queda como scroller horizontal con snap).

### 8.1 Markup y semántica

```html
<section class="section" aria-labelledby="collabs-h">
  <h2 class="ty-h2 carousel__title" id="collabs-h">
    Expertos con los que he tenido<br>
    <span class="ty-fire">la oportunidad de colaborar</span>
  </h2>

  <div class="carousel" role="group" aria-roledescription="carrusel"
       aria-label="Colaboraciones">
    <ul class="carousel__track" tabindex="0" aria-label="Lista de colaboraciones">
      <li class="collab">…</li>
    </ul>
    <div class="carousel__dots" role="tablist" aria-label="Ir a la colaboración">
      <button class="dot" role="tab" aria-selected="true"
              aria-label="Colaboración 1 de 9"></button>
    </div>
  </div>
</section>
```

- `aria-roledescription="carrusel"` en el contenedor.
- El track es `tabindex="0"`: recibe foco y responde a `←`/`→`/`Home`/`End` de forma
  nativa por ser un contenedor con scroll. Al recibir foco muestra el anillo global.
- Los dots son `role="tab"` con `aria-selected`. Solo el dot activo es tabulable
  (`tabindex="0"`), el resto `tabindex="-1"` — navegación entre ellos con flechas.
- El título usa `<br>` + `.ty-fire` para replicar la jerarquía AIVI: primera línea en
  blanco, línea clave en degradado de fuego.

### 8.2 Track

```css
.carousel__track {
  display: flex;
  gap: var(--gap);
  margin: 0;
  padding: 0 0 4px;
  list-style: none;
  overflow-x: auto;
  overflow-y: hidden;
  scroll-snap-type: x mandatory;
  scroll-behavior: smooth;
  overscroll-behavior-x: contain;
  scroll-padding-inline: var(--edge);
  padding-inline: var(--edge);
  scrollbar-width: none;
  -ms-overflow-style: none;
  cursor: grab;
}
.carousel__track::-webkit-scrollbar { display: none; }
.carousel__track.is-dragging { cursor: grabbing; scroll-snap-type: none; }
.collab { flex: 0 0 auto; scroll-snap-align: var(--snap); }
```

| Variable | <600px | 600–1023px | ≥1024px |
|---|---|---|---|
| `--gap` | `12px` | `16px` | `20px` |
| `--edge` (padding lateral) | `calc((100vw - 62vw) / 2)` centrado | `var(--sp-gutter)` | `calc((100vw - var(--w-wide)) / 2 + var(--sp-gutter))` |
| `--snap` | `center` | `start` | `start` |
| Slides visibles | 1 + asomos laterales | 3 | 4 |
| `mask` de desvanecido lateral | no | sí | sí |

Desvanecido de bordes en ≥600px (indica que hay más contenido):
```css
@media (min-width: 600px) {
  .carousel__track {
    mask-image: linear-gradient(90deg,
      transparent 0, #000 40px, #000 calc(100% - 40px), transparent 100%);
  }
}
```

### 8.3 Comportamiento

| Aspecto | Especificación |
|---|---|
| Scroll táctil | Nativo. Sin JS. `overscroll-behavior-x: contain` para no disparar el swipe-back del navegador. |
| Arrastre con ratón | JS: `pointerdown` → umbral de **6px** antes de activar `is-dragging`; `pointermove` aplica `scrollLeft -= dx`; `pointerup` quita la clase y reactiva el snap tras `50ms`. `setPointerCapture`. |
| Prevención de clic fantasma | Si el desplazamiento total supera 6px, `preventDefault()` en el `click` posterior. |
| Autoplay | Intervalo **4500ms**. Avanza un slide (`scrollBy` del ancho de slide + gap). Al llegar al final vuelve a `scrollLeft = 0`. |
| Pausa del autoplay | En `pointerenter`, `focusin`, `pointerdown`, `visibilitychange` (documento oculto) y cuando el carrusel sale del viewport (`IntersectionObserver`, `threshold: 0.35`). Reanuda **1200ms** después de que cesa la interacción. |
| Sincronía de dots | `scroll` event con `requestAnimationFrame` (no `setTimeout`); el índice activo es el slide cuyo centro está más cerca del centro del viewport del track. |
| Teclado | Flechas nativas en el track. En los dots: `←`/`→` mueven el dot activo y hacen `scrollIntoView({ block:'nearest', inline: snapMode })`; `Home`/`End` al primero/último. |
| Reduced motion | Autoplay **desactivado por completo**; `scroll-behavior: auto`. Ver §13. |

### 8.4 Dots de paginación

Contenedor:

| Propiedad | Valor |
|---|---|
| `display` | `flex` |
| `justify-content` | `center` |
| `align-items` | `center` |
| `gap` | `6px` (`--sp-1` + 2px; el gap visual real es 10px por el padding del botón) |
| `margin-block-start` | `24px` (`--sp-6`) |
| `min-height` | `44px` |

Botón dot — **el área táctil es 44×44px, el punto visible es 8px**:

```css
.dot {
  position: relative;
  width: 20px;
  height: 44px;                 /* alto táctil completo */
  padding: 0;
  border: 0;
  background: none;
  cursor: pointer;
  border-radius: var(--r-full);
  display: grid;
  place-items: center;
}
.dot::after {                   /* el punto visible */
  content: '';
  width: 8px;
  height: 8px;
  border-radius: var(--r-full);
  background: rgba(250,250,250,0.24);
  transition:
    width var(--t-3) var(--e-spring),
    background var(--t-2) var(--e-out),
    box-shadow var(--t-2) var(--e-out);
}
```

Estados del dot:

| Estado | `::after` | Transición |
|---|---|---|
| default (inactivo) | `width: 8px`; `background: rgba(250,250,250,0.24)` | — |
| hover *(hover:hover)* | `background: rgba(250,250,250,0.48)`; `width: 10px` | `var(--t-2)` / `var(--t-3)` |
| active (pressed) | `scale: 0.86` | `scale var(--t-1) var(--e-out)` |
| **seleccionado** (`[aria-selected="true"]`) | `width: 22px`; `background: var(--grad-fire)`; `box-shadow: 0 0 12px -2px rgba(255,128,60,0.55)` | `width var(--t-3) var(--e-spring)` |
| focus-visible | anillo global §4.5 aplicado al `<button>` (no al `::after`), `border-radius: 12px` | `box-shadow var(--t-2) var(--e-out)` |

El dot seleccionado pasa de círculo de 8px a pill de 22px: la forma cambia además del
color, así que la selección no depende solo del color (WCAG 1.4.1).

Con 9 slides el ancho total de la fila de dots es
`9 × 20px + 8 × 6px = 228px` — cabe en 360px con holgura.

---

## 9. Componente 5 — Bloque bio

### 9.1 Estructura

```html
<section class="section bio shell">
  <div class="bio__head">
    <span class="bio__avatar">
      <img src="assets/img/jhei-avatar.webp" alt="Jhei Trujillo"
           width="208" height="208" loading="lazy">
    </span>
    <span class="bio__id">
      <span class="ty-h3 bio__name">Jhei Trujillo</span>
      <span class="bio__handle">@jheitrujillo</span>
    </span>
  </div>
  <div class="bio__copy">
    <p class="ty-body">…</p>
    <p class="ty-body">…</p>
    <p class="ty-body">…</p>
  </div>
</section>
```

### 9.2 Avatar con anillo de fuego

Técnica: caja exterior con `conic-gradient` + `padding` de 3px + imagen con borde
`#101010` de 2px, que crea el hueco entre anillo y foto.

```css
.bio__avatar {
  display: block;
  width: var(--av);
  height: var(--av);
  padding: 3px;                                /* excepción documentada de la escala */
  border-radius: var(--r-full);
  background: var(--grad-ring);
  box-shadow: 0 0 26px -8px rgba(255,120,50,0.45);
  flex: 0 0 auto;
  animation: ring-spin 9s linear infinite;
}
.bio__avatar img {
  width: 100%;
  height: 100%;
  border-radius: var(--r-full);
  object-fit: cover;
  border: 2px solid #101010;
  background: #141414;
  animation: ring-spin 9s linear infinite reverse;  /* contrarrota: la foto no gira */
}
@keyframes ring-spin { to { rotate: 360deg; } }
```

| Propiedad | <600px | ≥600px |
|---|---|---|
| `--av` | `84px` | `104px` |
| `padding` (grosor del anillo) | `3px` | `3px` |
| `border` interior | `2px solid #101010` | `2px solid #101010` |
| `box-shadow` | `0 0 22px -8px rgba(255,120,50,0.42)` | `0 0 26px -8px rgba(255,120,50,0.45)` |

Si el implementador prefiere evitar la doble animación contrarrotada, el anillo estático
es aceptable: `animation: none` en ambos. La rotación es un detalle, no un requisito.

### 9.3 Cabecera (avatar + identidad)

| Propiedad | <600px | ≥600px |
|---|---|---|
| `display` | `flex` | `flex` |
| `align-items` | `center` | `center` |
| `justify-content` | `center` | `center` |
| `gap` | `14px` | `16px` (`--sp-4`) |
| `margin-block-end` | `24px` (`--sp-6`) | `32px` (`--sp-7`) |
| `text-align` del bloque `.bio__id` | `start` | `start` |

```css
.bio__name {
  display: block;
  font-size: var(--fs-h3);        /* 20 → 28px */
  font-weight: 900;
  line-height: 1.1;
  letter-spacing: -0.02em;
  text-transform: uppercase;
  color: #FAFAFA;                 /* 18.23:1 */
}
.bio__handle {
  display: block;
  margin-block-start: 2px;
  font-size: clamp(0.9375rem, 0.9167rem + 0.0926vw, 1rem);  /* 15 → 16px */
  font-weight: 600;
  letter-spacing: 0.01em;
  color: #FFC252;                 /* 11.86:1 — etiqueta ≥15px/600, permitido §1.6 */
}
```

### 9.4 Párrafos

| Propiedad | Valor |
|---|---|
| `max-width` | `--w-read` (544px) y a la vez `46ch` — se aplica `min()` de ambos |
| `margin-inline` | `auto` |
| `text-align` | `center` |
| `font-size` | `--fs-body` (16 → 18px) |
| `line-height` | `1.65` |
| `color` | `rgba(250,250,250,0.82)` — **12.33:1** |
| `text-wrap` | `pretty` |
| Separación entre párrafos | `20px` (`--sp-5`) |
| Primer párrafo (`:first-child`) | `font-size: var(--fs-body-lg)`; `color: rgba(250,250,250,0.88)`; `font-weight: 500` |

Palabras clave dentro de los párrafos: **blanco `#FAFAFA` con `font-weight: 700`**.
Prohibido resaltar en naranja o dorado dentro de un párrafo (§1.6).

### 9.5 Fila de redes

| Propiedad | <600px | ≥600px |
|---|---|---|
| `display` | `flex` | `flex` |
| `justify-content` | `center` | `center` |
| `gap` | `12px` (`--sp-3`) | `14px` |
| `margin-block-start` | `40px` (`--sp-8`) | `40px` |
| `flex-wrap` | `wrap` | `nowrap` |

---

## 10. Componente 6 — Icono de red social

Círculo de vidrio que se enciende naranja al hover.

### 10.1 Markup

```html
<a class="social" href="…" target="_blank" rel="noopener noreferrer"
   aria-label="Instagram de Jhei Trujillo">
  <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">…</svg>
</a>
```
El nombre accesible va en `aria-label`, siempre con la red **y** el titular. El SVG
lleva `aria-hidden="true"` y `focusable="false"`.

### 10.2 Caja

| Propiedad | <600px | ≥600px |
|---|---|---|
| `width` / `height` | `48px` / `48px` | `52px` / `52px` |
| `border-radius` | `--r-full` | `--r-full` |
| `background` | `rgba(250,250,250,0.045)` | igual |
| `border` | `1px solid rgba(250,250,250,0.12)` | igual |
| `backdrop-filter` | `blur(12px) saturate(120%)` | `blur(14px) saturate(120%)` |
| `box-shadow` | `--sh-glass`, `--sh-1` | igual |
| `display` | `grid` + `place-items: center` | igual |
| Tamaño del glifo | `20px` | `21px` |
| Color del glifo | `#FAFAFA` (**16.50:1** sobre el vidrio) | igual |
| `overflow` | `hidden` | igual |
| `position` | `relative` | igual |
| `isolation` | `isolate` | igual |

48px cumple el mínimo táctil de 44px sin necesidad de pseudoelemento expansor. El
`gap` de 12px garantiza separación entre objetivos.

Capa de encendido (se anima la opacidad, no el `background`, para no repintar el blur):
```css
.social::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background:
    radial-gradient(120% 120% at 50% 118%,
      rgba(255,194,82,0.30) 0%, rgba(254,128,63,0.00) 62%),
    rgba(254,128,63,0.14);
  opacity: 0;
  transition: opacity var(--t-2) var(--e-out);
  z-index: -1;
}
```

### 10.3 Estados

| Estado | Propiedades exactas | Transición |
|---|---|---|
| **default** | `background: rgba(250,250,250,0.045)`; `border-color: rgba(250,250,250,0.12)`; glifo `#FAFAFA`; `::before { opacity: 0 }`; `translate: 0 0` | — |
| **hover** *(`@media (hover:hover) and (pointer:fine)`)* | `::before { opacity: 1 }`; `border-color: rgba(254,128,63,0.42)`; glifo `#FE803F`; `box-shadow: var(--sh-fire-soft), var(--sh-glass)`; `translate: 0 -2px` | `opacity var(--t-2) var(--e-out)`, `border-color var(--t-2) var(--e-out)`, `color var(--t-2) var(--e-out)`, `box-shadow var(--t-3) var(--e-out)`, `translate var(--t-3) var(--e-out)` |
| **active** | `translate: 0 0`; `scale: 0.93`; `::before { opacity: 1 }`; glifo `#FFC252`; `box-shadow: var(--sh-1)` | `scale var(--t-1) var(--e-out)`, `translate var(--t-1) var(--e-out)` |
| **focus-visible** | anillo global §4.5 + estado visual de hover (`::before { opacity: 1 }`, glifo `#FE803F`) para que teclado y ratón vean lo mismo | `box-shadow var(--t-2) var(--e-out)` |

Contrastes verificados en hover: glifo `#FE803F` sobre el vidrio encendido `#312017`
= **6.21:1** (mínimo requerido para un icono no textual: 3:1). Cumple con margen.

---

## 11. Componente 7 — Footer

### 11.1 Markup

```html
<footer class="footer">
  <span class="footer__rule" aria-hidden="true"></span>
  <div class="shell footer__inner">
    <p class="footer__legal">
      Jhei Trujillo · Todos los derechos reservados · <span>2026</span>
    </p>
    <p class="footer__meta">
      Viralidad · Creación de contenido · Inteligencia artificial
    </p>
  </div>
</footer>
```

### 11.2 Caja

| Propiedad | <600px | ≥600px |
|---|---|---|
| `margin-block-start` | `56px` (`--sp-10`) | `64px` (`--sp-11`) |
| `padding-block` | `28px 40px` | `32px 48px` |
| `padding-block-end` extra | `+ env(safe-area-inset-bottom)` | igual |
| `text-align` | `center` | `center` |
| `position` | `relative` | igual |

Hairline superior — 1px de fuego que se desvanece a los lados:
```css
.footer__rule {
  display: block;
  height: 1px;
  width: min(100% - 2 * var(--sp-gutter), var(--w-col));
  margin: 0 auto 28px;
  background: var(--grad-hairline);
}
```

### 11.3 Texto

| Elemento | Rol tipográfico | Tamaño | Peso | Tracking | Color | Contraste |
|---|---|---|---|---|---|---|
| `.footer__legal` | `.ty-micro` | 11 → 13px | 700 | `+0.12em` | `rgba(250,250,250,0.56)` | **6.19:1** |
| `.footer__meta` | `.ty-micro` | 11 → 13px | 600 | `+0.14em` | `rgba(250,250,250,0.40)` → **elevar a `0.56`** | ver nota |

**Nota obligatoria:** el segundo párrafo del footer usa `rgba(250,250,250,0.56)`, igual
que el primero, y se diferencia por `font-weight: 600` (frente a 700) y por
`margin-block-start: 8px`. No se baja de `0.56` para crear jerarquía: la jerarquía se
hace con peso y espacio, no bajando el contraste.

| Propiedad | Valor |
|---|---|
| Separación entre los dos párrafos | `8px` (`--sp-2`) |
| `text-transform` | `uppercase` |
| `max-width` | `40ch`, `margin-inline: auto` |

### 11.4 Enlaces del footer (si se añaden)

```css
.footer a {
  color: rgba(250,250,250,0.72);            /* 9.0:1 */
  text-decoration: underline;
  text-decoration-color: rgba(254,128,63,0.45);
  text-decoration-thickness: 1px;
  text-underline-offset: 3px;
  transition: color var(--t-2) var(--e-out),
              text-decoration-color var(--t-2) var(--e-out);
}
```

| Estado | Cambios |
|---|---|
| hover | `color: #FAFAFA`; `text-decoration-color: #FE803F` |
| active | `color: rgba(250,250,250,0.82)` |
| focus-visible | anillo global §4.5, `border-radius: 4px` |

El subrayado existe en reposo: los enlaces del footer no se identifican solo por color.

---

## 12. Accesibilidad

### 12.1 Contraste medido — texto y glifos sobre `#101010`

Todos los valores calculados con la fórmula WCAG 2.1 (luminancia relativa, sRGB).

| Color de primer plano | Ratio | AA normal (4.5) | AA large (3.0) | Uso autorizado |
|---|---|---|---|---|
| `#FAFAFA` | **18.23:1** | ✅ | ✅ | todo |
| `rgba(250,250,250,0.88)` → `#DEDEDE` | **14.15:1** | ✅ | ✅ | subtítulos, nombre de bio |
| `rgba(250,250,250,0.82)` → `#D0D0D0` | **12.33:1** | ✅ | ✅ | párrafos |
| `rgba(250,250,250,0.72)` → `#B8B8B8` | **9.59:1** | ✅ | ✅ | enlaces de footer |
| `rgba(250,250,250,0.56)` → `#939393` | **6.19:1** | ✅ | ✅ | footer (mínimo del sistema) |
| `#FFC252` (dorado) | **11.86:1** | ✅ | ✅ | handle, foco, texto grande |
| `#FE803F` (naranja) | **7.59:1** | ✅ | ✅ | separadores, iconos, texto grande |
| `#FF413B` (rojo) | **5.50:1** | ✅ | ✅ | inicio de degradados, texto ≥26px |

Los tres tonos cálidos superan AA incluso para texto normal. La restricción de §1.6 es
de **jerarquía**, no de contraste, y así debe entenderse: el sistema no depende de una
excepción de accesibilidad.

### 12.2 Contraste sobre superficies de fuego (el caso crítico)

Blanco puro sobre el degradado de fuego **sin escrim** no pasa AA. Medido:

| Fondo | Blanco `#FFFFFF` encima | Veredicto |
|---|---|---|
| `#FFC252` (dorado puro) | 1.54:1 | ❌ prohibido |
| `#FE803F` (naranja puro) | 2.40:1 | ❌ prohibido |
| `#FF413B` (rojo puro) | 3.31:1 | ⚠️ solo texto ≥24px o ≥18.7px bold |
| `#E2601F` (`--c-fire-600`) | 3.39:1 | ⚠️ solo texto grande |
| `#A8280C` (`--c-fire-800`) | **6.77:1** | ✅ |

**De ahí el escrim.** Valores medidos del escrim `#0C0806` sobre el degradado:

| Alfa del escrim | Sobre | Color resultante | Blanco encima |
|---|---|---|---|
| `0.88` | `#FE803F` | `#2E190E` | **15.95:1** |
| `0.78` | `#FE803F` | `#502A16` | **11.95:1** |
| `0.62` | `#FF9A4A` | `#683F20` | **8.67:1** |
| `0.55` | `#FFC252` (peor caso) | `#795C28` | **5.96:1** |

Regla derivada, obligatoria: **cualquier texto de la tarjeta CTA debe estar sobre un
punto del escrim con alfa ≥ 0.55.** Los stops de `--grad-scrim` están definidos para
que el bloque de texto (que en ≥600px ocupa como máximo el 62% del ancho de la
tarjeta) quede íntegramente en la zona `0.46–0.88`. En `<600px`, donde el texto ocupa
el 100%, el escrim móvil se redefine a `0.90 → 0.34` con `0.86` al 46% (§6.5) y el
`.cta__micro` nunca rebasa el 74% del ancho.

Verificación manual requerida en QA: capturar la tarjeta 3 a 360px y medir el píxel
más claro bajo la última letra del microcopy. Debe dar ≥4.5:1 contra `#FFFFFF`.

Otros elementos sobre fuego:
- Logo blanco de colaboración sobre `#A8280C`: **6.77:1** ✅
- Anillo de foco dorado `#FFC252` sobre `#E2601F`: 2.21:1 — **por eso el anillo lleva
  el separador oscuro `#101010` de 2px** (§4.5), que mide 5.37:1 contra `#E2601F` y
  11.86:1 contra el dorado. El indicador de foco cumple 3:1 contra ambos vecinos.

### 12.3 Objetivos táctiles

| Elemento | Tamaño real | Cumple 44×44 |
|---|---|---|
| Tarjeta CTA | ≥128px de alto × ancho completo | ✅ |
| Indicador de scroll | 48×48 (44 mínimo + área) | ✅ |
| Icono de red | 48×48 / 52×52 | ✅ |
| Dot del carrusel | 20×44 (punto visible 8px) | ✅ alto; ancho 20px con `gap` de 6px ⇒ paso de 26px |
| Enlace de footer | `padding-block: 6px` para llegar a 32px de alto útil | ⚠️ excepción de enlace en línea de texto, permitida por WCAG 2.5.8 |

Los dots miden 20px de ancho: por debajo del ideal de 44, amparado por la excepción de
"controles equivalentes" de WCAG 2.5.8 — el mismo destino se alcanza deslizando el
track o con las flechas del teclado. Se documenta como decisión consciente.

### 12.4 Estructura semántica

- Un solo `<h1>`: "Jhei Trujillo" en el hero.
- `<h2>` para "Expertos con los que he tenido la oportunidad de colaborar".
- El nombre de la bio es un `<span>` con estilo `.ty-h3`, **no** un heading: no
  introduce una sección nueva.
- Las tarjetas CTA son `<a>`, no `<div role="button">`.
- Enlaces externos: `target="_blank" rel="noopener noreferrer"` y el `aria-label`
  indica el destino ("Ir a WhatsApp", "Ver los talleres").
- `lang="es"` en `<html>`. Los signos `·` decorativos van dentro de `<span
  aria-hidden="true">` cuando separan ítems de una lista visual.
- `prefers-contrast: more`: `--s-border` sube a `rgba(250,250,250,0.28)`,
  `--t-muted` sube a `rgba(250,250,250,0.72)`, el escrim del CTA sube `+0.06` de alfa
  en todos sus stops.

---

## 13. `prefers-reduced-motion`: contrato completo

Bloque único al final de la hoja de estilos. **No se apagan las transiciones de color**
(no son movimiento y sí son feedback útil); se apagan traslaciones, escalas,
rotaciones y bucles.

```css
@media (prefers-reduced-motion: reduce) {

  /* 1 · bucles decorativos: fuera */
  .hero__halo,
  .hero__glow,
  .scroll-cue,
  .bio__avatar,
  .bio__avatar img {
    animation: none !important;
  }

  /* 2 · scroll instantáneo */
  html, .carousel__track { scroll-behavior: auto !important; }

  /* 3 · sin desplazamiento ni escala en hover/active */
  .cta,
  .cta__art,
  .collab__photo,
  .social,
  .scroll-cue,
  .dot::after {
    transition-property: background-color, border-color, color, box-shadow,
                         opacity, background-position, filter !important;
  }
  .cta:hover, .cta:active,
  .social:hover, .social:active,
  .scroll-cue:hover, .scroll-cue:active {
    translate: 0 0 !important;
    scale: 1 !important;
  }
  .cta:hover .cta__art, .cta:active .cta__art,
  .collab:hover .collab__photo {
    scale: 1 !important;
    translate: 0 0 !important;
  }

  /* 4 · el dot activo cambia solo de color y de forma estática */
  .dot::after { transition: background var(--t-2) linear, width 1ms linear !important; }

  /* 5 · el anillo de foco NUNCA se toca; solo pierde la transición */
  :where(a, button, [tabindex]):focus-visible {
    transition: none !important;
  }
}
```

Además, en JavaScript:

```js
const reduce = matchMedia('(prefers-reduced-motion: reduce)');
// autoplay del carrusel: no se inicia si reduce.matches === true
// se re-evalúa con reduce.addEventListener('change', …)
// los scrollTo/scrollBy pasan behavior: reduce.matches ? 'auto' : 'smooth'
```

Compensación obligatoria de lo que se pierde:
- Sin la animación del indicador de scroll, este mantiene su borde y su glifo: sigue
  siendo identificable.
- Sin la respiración del glow, este permanece en `opacity: 0.85` (el punto medio).
- Sin autoplay, los dots y el arrastre siguen siendo la vía completa de navegación del
  carrusel.

---

## 14. Assets

### 14.1 Nomenclatura

```
assets/
  fonts/
    hanken-grotesk-var.woff2
  img/
    jhei-hero.webp            recorte del hero, fondo transparente
    jhei-hero@2x.webp
    jhei-avatar.webp          avatar cuadrado
    mock-talleres.webp        mockup CTA 1
    mock-aivi.webp            mockup CTA 2
    mock-whatsapp.webp        mockup CTA 3
    collab-01.webp … collab-09.webp
    logo-collab-01.svg … logo-collab-09.svg
```

### 14.2 Especificación de export

| Asset | Formato | Dimensiones (1×) | Alfa | Peso máx. | Notas |
|---|---|---|---|---|---|
| `jhei-hero` | WebP lossy q82 + AVIF | 820 × 1000 | sí | 180 KB | `fetchpriority="high"`, sin `loading="lazy"`. Recorte con borde limpio; una pluma de 1px evita el halo de matte. |
| `jhei-avatar` | WebP q85 | 208 × 208 | no | 24 KB | encuadre de rostro centrado, 12% de aire arriba |
| `mock-*` | WebP q82 | 640 × 440 | sí | 120 KB c/u | `loading="lazy"`, sombra propia **no** incluida (la pone CSS) |
| `collab-*` | WebP q80 | 440 × 704 (5:8) | no | 90 KB c/u | exportar **en color**; el B/N lo hace CSS (`filter: grayscale(1)`) para poder revelarlo en hover |
| `logo-collab-*` | SVG optimizado | alto normalizado a 28 | sí | 8 KB c/u | trazo convertido a path, `viewBox` presente, sin `width`/`height` fijos, sin `<style>` interno |

Todo `<img>` lleva `width` y `height` explícitos para reservar el espacio y evitar CLS.
Todo `<img>` decorativo lleva `alt=""`. Cero imágenes de fondo en CSS para contenido.

### 14.3 Presupuesto de rendimiento

| Métrica | Objetivo |
|---|---|
| CSS total (minificado) | ≤ 22 KB |
| JS total (minificado) | ≤ 6 KB |
| Fuente | 1 archivo variable, ≤ 40 KB con `unicode-range` latino |
| Peticiones antes del LCP | ≤ 4 (HTML, CSS, fuente, foto del hero) |
| LCP objetivo (móvil 4G) | ≤ 2.0 s |
| CLS | 0 |

---

## 15. Checklist de QA

Cada punto se verifica midiendo, no mirando.

**Tokens**
- [ ] Ningún valor de `padding`/`margin` fuera de la escala §3.1, salvo las dos
      excepciones documentadas (`-34px/-18px` del mockup móvil, `3px` del anillo).
- [ ] Ninguna `transition: all` en toda la hoja.
- [ ] Ningún color hardcodeado fuera de `:root` salvo los del anillo de foco.

**Tipografía**
- [ ] A 360px exactos: display = 40px, h2 = 26px, micro = 11px (medir en DevTools).
- [ ] A 1440px exactos: display = 92px, h2 = 44px, micro = 13px.
- [ ] Todo `uppercase` 900 tiene tracking negativo; todo `uppercase` ≤15px lo tiene
      positivo.
- [ ] Ningún párrafo supera 46ch.

**CTA**
- [ ] A 360px: "HABLEMOS POR WHATSAPP" ocupa ≤2 líneas y el mockup no le resta ancho.
- [ ] A 360px: no existe scroll horizontal (comprobar `document.documentElement.scrollWidth === clientWidth`).
- [ ] A 900px: el mockup desborda la tarjeta ≤24px y no genera scroll.
- [ ] Píxel más claro bajo el microcopy: ≥4.5:1 contra `#FFFFFF` en las 3 tarjetas.
- [ ] La alternancia es end → start → end.
- [ ] El anillo de foco es visible sobre el naranja (dos tonos presentes).

**Carrusel**
- [ ] Funciona con JS desactivado (scroll con snap).
- [ ] El dot activo cambia de **forma** (8px → 22px), no solo de color.
- [ ] Autoplay se pausa con hover, con foco, al salir del viewport y con la pestaña
      oculta.
- [ ] `←`/`→` navegan desde el track y desde los dots.
- [ ] Con `prefers-reduced-motion` el autoplay no arranca.

**Accesibilidad**
- [ ] Recorrido completo con `Tab` sin ratón: hero-cue → CTA1 → CTA2 → CTA3 → track →
      dot activo → 4 redes → enlaces de footer. Todo con anillo visible.
- [ ] Ningún `:focus { outline: none }` sin `:focus-visible` que lo reponga.
- [ ] Un solo `<h1>`.
- [ ] Todo objetivo táctil ≥44px salvo los dots (excepción documentada §12.3).
- [ ] Zoom de texto al 200% en móvil: sin recortes ni solapamientos.
- [ ] Todos los `aria-label` de redes nombran la red y al titular.

**Marca**
- [ ] No aparece el logo ni el isotipo de AIVI en ningún asset ni en ningún SVG.
- [ ] Los chevrones usados son la geometría de §4.4.
- [ ] Ningún morado en ninguna parte del CSS (`grep -i "purple\|#7\|#8b5\|violet"`).
- [ ] El grano está presente a `opacity: 0.045` y no se anima.

---

**Documento cerrado.** Cualquier valor no listado aquí es una decisión no tomada y
debe escalarse antes de implementarse, no improvisarse.
