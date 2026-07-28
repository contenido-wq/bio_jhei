# Motion Spec — Link in Bio · Jhei Trujillo

Capa de movimiento y micro-interacciones. HTML + CSS + JS vanilla, cero dependencias.
Fuente visual: `docs/brand/aivi-brand-extract.md`, `ref-aivi-social.png`, `ref-layout-*.png`.

---

## 0. Principios (no decorativos: se aplican en cada valor de este documento)

**La metáfora es luz, no materia.** La luz no rebota, no tiene masa, no pisa el suelo.
Por eso: **cero easings con overshoot**. Nada de `cubic-bezier` con valores fuera de
`[0,1]` en el eje Y, nada de `back`, `elastic` ni `bounce`. Si un elemento "vuelve",
está mal. La luz aparece, se propaga y se apaga.

**Cuatro reglas de las que se derivan todos los números:**

1. **Distancias cortas.** Ningún desplazamiento de entrada supera **18px**. Recorridos
   largos leen como "plantilla de portafolio"; recorridos de 12–18px leen como premium.
   Las escalas se mueven entre **0.978 y 1.045**. Nunca más.
2. **Asimetría de ignición.** Encender es rápido, apagar es lento — como una brasa.
   Entrada de estado: **160–260ms**. Salida del mismo estado: **280–360ms**.
   Implementado poniendo la `transition` corta en el estado (`:hover`) y la larga
   en la base.
3. **Solo `transform` y `opacity`** en cualquier cosa que se anime en bucle, al scroll
   o al arrastre. Los desenfoques existen pero son **estáticos** (ver §9).
4. **Un solo foco de movimiento a la vez.** El glow del hero es lo único que se mueve
   permanentemente, y se mueve tan despacio que no compite con la lectura.

### 0.1 Tokens de movimiento

```css
:root{
  /* ---------- Easings ---------- */
  /* Propagación de luz: arranca muy rápido y se asienta largo. Toda entrada. */
  --e-light:   cubic-bezier(.16, 1, .3, 1);
  /* Cambio de estado suave y sin cola. Hover, elevación, dots, cards. */
  --e-glide:   cubic-bezier(.22, .61, .36, 1);
  /* Presión: lineal-ish, para que el dedo sienta respuesta inmediata. */
  --e-press:   cubic-bezier(.4, 0, .2, 1);
  /* Respiración: sinusoidal simétrica. Sin aceleración perceptible. */
  --e-breathe: cubic-bezier(.45, 0, .55, 1);
  /* Barrido de brillo: entra acelerando, sale casi lineal. La luz "pasa". */
  --e-sweep:   cubic-bezier(.32, 0, .12, 1);
  /* Desvanecido de salida (apagado). */
  --e-fade:    cubic-bezier(.4, 0, .6, 1);

  /* ---------- Duraciones ---------- */
  --d-tap:    90ms;   /* feedback táctil — presupuesto duro <100ms */
  --d-fast:  160ms;   /* ignición de iconos, color */
  --d-base:  240ms;   /* cambios de estado, dots */
  --d-out:   320ms;   /* apagado (regla de asimetría) */
  --d-enter: 380ms;   /* entrada de bloque de texto */
  --d-hero:  520ms;   /* foto del hero */
  --d-sweep: 700ms;   /* barrido de brillo del CTA */
  --breath-a:  9000ms;
  --breath-b: 13000ms;

  /* ---------- Fuego (referencia; la paleta vive en el spec de color) ---------- */
  --fire-red:    #FF413B;
  --fire-orange: #FE803F;
  --fire-gold:   #FFC252;
  --ink:         #101010;
  --paper:       #FAFAFA;
}
```

### 0.2 Contrato de marcado

El JS no crea estructura: consume atributos. El dev de HTML debe respetar esta tabla.

| Hook | Dónde | Qué hace |
|---|---|---|
| `class="motion"` en `<html>` | inline script en `<head>` | activa la capa de movimiento; sin JS nada se oculta |
| `class="is-ready"` en `<html>` | JS de arranque | dispara la secuencia de entrada |
| `data-enter` | elementos del hero | participa en la entrada escalonada |
| `--delay`, `--dur`, `--from-y` | inline style o CSS | parámetros por elemento de la entrada |
| `data-reveal` | secciones/bloques | revelado individual al scroll |
| `data-reveal-stagger` | contenedor | revela sus hijos directos en cascada |
| `data-carousel` | el track scrollable | carrusel |
| `data-carousel-dot` | cada `<button>` de paginación | dots |
| `data-ignite` | `<button>` que envuelve la foto del hero | detalle de deleite (§8) |
| `.cta` + `.cta__shine` + `.cta__hot` + `.cta__glow` | botones-tarjeta | capas del CTA |

### 0.3 Arranque

```html
<!-- en <head>, antes del CSS: sin esto, un usuario sin JS ve todo oculto -->
<script>document.documentElement.classList.add('motion');</script>
```

```js
/* js/motion.js — arranque. Módulo único; el resto de secciones cuelga de aquí. */
export const reduce = window.matchMedia('(prefers-reduced-motion: reduce)');

function start(){
  /* doble rAF: garantiza que los estilos iniciales ya están aplicados
     antes del flip de clase, para que la animación se vea desde el frame 0 */
  requestAnimationFrame(() => requestAnimationFrame(() => {
    document.documentElement.classList.add('is-ready');
  }));
}

/* Si la webfont llega a mitad de la animación, el texto salta de métrica.
   Esperamos a las fuentes, pero con un techo de 350ms: la impaciencia manda. */
Promise.race([
  document.fonts ? document.fonts.ready : Promise.resolve(),
  new Promise(r => setTimeout(r, 350))
]).then(start);
```

> Requiere `<link rel="preload" as="font">` del único peso de Hanken Grotesk que usa
> el hero, y `font-display: swap`. Sin el preload, el race se resuelve casi siempre por
> timeout y la entrada arranca con la fuente de sistema.

---

## 1. Entrada de página

**Objetivo medible:** el nombre es legible antes de los **500ms**; el último CTA termina
de entrar a los **860ms**. Nada espera a nada más que a sí mismo.

### 1.1 Secuencia

| # | Elemento | Delay | Duración | Fin | Transform de origen |
|---|---|---|---|---|---|
| 1 | `.hero__glow` (contenedor) | 40ms | 700ms | 740 | **solo opacity** 0→1 |
| 2 | `.hero__photo` | 0ms | 520ms | 520 | `scale(1.045)` → `scale(1)` · **opacity fija en 1** |
| 3 | `h1` nombre | 170ms | 400ms | 570 | `translateY(14px)` |
| 3b | barrido de luz sobre la palabra en degradado | 320ms | 780ms | 1100 | `translateX` del `::after` |
| 4 | tagline / rol | 235ms | 380ms | 615 | `translateY(12px)` |
| 5 | CTA · TALLERES | 320ms | 400ms | 720 | `translateY(18px)` + `scale(.986)` |
| 6 | CTA · AIVI | 390ms | 400ms | 790 | ídem |
| 7 | CTA · WHATSAPP | 460ms | 400ms | 860 | ídem |
| 8 | indicador de scroll | 620ms | 400ms | 1020 | `translateY(-6px)` + opacity |

**La foto no hace fade.** Entra solo con escala, con `opacity: 1` desde el primer frame.
Razón: la foto es el candidato a **LCP**. Un elemento que arranca en `opacity: 0` retrasa
el LCP reportado tanto como su delay + parte de su duración. Con escala pura, el LCP se
registra en el primer paint real y la entrada sigue leyéndose como "la luz se asienta".
Efecto secundario deseado: durante ~170ms solo existe la foto sobre el negro, y después
la luz se propaga hacia el texto y los botones. Ese es literalmente el concepto.

**El stagger de los CTA es de 70ms**, no de 120. A 120ms se percibe como una lista
cargando; a 70ms se percibe como una corriente recorriéndolos.

### 1.2 CSS

```css
/* Sin JS (html sin .motion) nada de esto aplica: la página es estática y completa. */
html.motion [data-enter]{ opacity: 0; }

html.motion.is-ready [data-enter]{
  animation: enter-light var(--dur, var(--d-enter)) var(--e-light) both;
  animation-delay: var(--delay, 0ms);
}

@keyframes enter-light{
  from{
    opacity: 0;
    transform: translate3d(0, var(--from-y, 14px), 0) scale(var(--from-s, 1));
  }
  to{
    opacity: 1;
    transform: translate3d(0, 0, 0) scale(1);
  }
}

/* --- Parámetros por elemento --- */
.hero__photo         { --delay: 0ms;   --dur: 520ms; }
.hero__name          { --delay: 170ms; --dur: 400ms; --from-y: 14px; }
.hero__tagline       { --delay: 235ms; --dur: 380ms; --from-y: 12px; }
.cta:nth-of-type(1)  { --delay: 320ms; --dur: 400ms; --from-y: 18px; --from-s: .986; }
.cta:nth-of-type(2)  { --delay: 390ms; --dur: 400ms; --from-y: 18px; --from-s: .986; }
.cta:nth-of-type(3)  { --delay: 460ms; --dur: 400ms; --from-y: 18px; --from-s: .986; }
.scroll-hint         { --delay: 620ms; --dur: 400ms; --from-y: -6px; }

/* La foto es el LCP: escala sin fade. Override del keyframe genérico. */
html.motion .hero__photo{ opacity: 1; }
html.motion.is-ready .hero__photo{
  animation: enter-settle var(--d-hero) var(--e-light) both;
}
@keyframes enter-settle{
  from{ transform: translate3d(0,0,0) scale(1.045); }
  to  { transform: translate3d(0,0,0) scale(1); }
}
/* el contenedor recorta la escala para que no invada el layout */
.hero__photo-frame{ overflow: hidden; border-radius: 28px; }

/* El glow entra solo con opacidad (su movimiento propio vive en §4) */
html.motion .hero__glow{ opacity: 0; }
html.motion.is-ready .hero__glow{
  animation: enter-fade 700ms var(--e-glide) 40ms both;
}
@keyframes enter-fade{ from{ opacity: 0 } to{ opacity: 1 } }
```

### 1.3 El barrido sobre la palabra en degradado (1 sola vez)

La jerarquía de marca pide la última palabra en degradado de fuego (`ref-aivi-social.png`).
Ese es el único sitio del hero donde la luz "pasa" en la entrada.

No se anima `background-position` ni `mask-position` (ambas provocan repaint del texto en
cada frame). Se anima el `transform` de una banda superpuesta en modo `screen`:

```css
.hero__name em{               /* la palabra clave, ej. "VIRAL" */
  font-style: normal;
  position: relative;
  background: linear-gradient(96deg, var(--fire-red) 0%, var(--fire-orange) 46%, var(--fire-gold) 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}
.hero__name em::after{
  content: "";
  position: absolute;
  inset: -0.15em -35% -0.15em -35%;
  pointer-events: none;
  background: linear-gradient(100deg,
    transparent 38%,
    rgba(255,255,255,.00) 44%,
    rgba(255,255,255,.55) 50%,
    rgba(255,255,255,.00) 56%,
    transparent 62%);
  mix-blend-mode: screen;
  transform: translate3d(-115%, 0, 0);
  opacity: 0;
}
html.motion.is-ready .hero__name em::after{
  animation: name-sweep 780ms var(--e-sweep) 320ms 1 both;
}
@keyframes name-sweep{
  0%   { transform: translate3d(-115%,0,0); opacity: 0 }
  12%  { opacity: 1 }
  88%  { opacity: 1 }
  100% { transform: translate3d(115%,0,0);  opacity: 0 }
}
```

Se ejecuta **una sola vez**. En bucle sería un banner publicitario.

---

## 2. Revelado al scroll

Bloques que participan: título "Expertos con los que he colaborado", cards del carrusel
(en cascada, máx. 4), panel de bio, fila de iconos, footer.

### 2.1 JS completo

```js
/* js/reveal.js */
import { reduce } from './motion.js';

(function initReveal(){
  const targets = document.querySelectorAll('[data-reveal], [data-reveal-stagger]');
  if (!targets.length) return;

  const revealAll = () => targets.forEach(el => el.classList.add('is-revealed'));

  /* Sin IO o con reduced-motion: contenido visible, sin excepciones. */
  if (reduce.matches || !('IntersectionObserver' in window)) { revealAll(); return; }

  /* Índice de cascada para los hijos, sin tocar el layout. */
  document.querySelectorAll('[data-reveal-stagger]').forEach(group => {
    const cap = Number(group.dataset.revealStagger) || 6;   /* techo de cascada */
    Array.from(group.children).forEach((child, i) => {
      child.style.setProperty('--i', Math.min(i, cap));
    });
  });

  const io = new IntersectionObserver((entries) => {
    for (const entry of entries){
      if (!entry.isIntersecting) continue;
      entry.target.classList.add('is-revealed');
      io.unobserve(entry.target);          /* one-shot: nunca se re-oculta */
    }
  }, {
    /* threshold 0 a propósito: con un bloque más alto que el viewport
       (el panel de bio en móvil) un threshold de 0.15 puede no dispararse nunca.
       El retardo lo aporta el rootMargin negativo, no el ratio. */
    threshold: 0,
    rootMargin: '0px 0px -12% 0px'
  });

  targets.forEach(el => io.observe(el));

  /* Red de seguridad: si el usuario aterriza con hash (#bio) o el navegador
     restaura scroll antes de que el IO se registre, forzamos un check. */
  window.addEventListener('load', () => {
    requestAnimationFrame(() => {
      targets.forEach(el => {
        const r = el.getBoundingClientRect();
        if (r.top < window.innerHeight && r.bottom > 0) el.classList.add('is-revealed');
      });
    });
  }, { once: true });
})();
```

### 2.2 CSS

```css
html.motion [data-reveal],
html.motion [data-reveal-stagger] > *{
  opacity: 0;
  transform: translate3d(0, 18px, 0);
  transition:
    opacity   var(--d-enter) var(--e-light),
    transform var(--d-enter) var(--e-light);
}

html.motion [data-reveal].is-revealed{
  opacity: 1;
  transform: translate3d(0, 0, 0);
}

/* Cascada: el observador está en el contenedor, los hijos leen su clase. */
html.motion [data-reveal-stagger] > *{
  transition-delay: calc(var(--i, 0) * 70ms);
}
html.motion [data-reveal-stagger].is-revealed > *{
  opacity: 1;
  transform: translate3d(0, 0, 0);
}

/* Variante para el subrayado de luz bajo los títulos de sección:
   escala en X desde la izquierda. Nunca `width`. */
html.motion .section-title__rule{
  transform: scaleX(0);
  transform-origin: 0 50%;
  transition: transform 620ms var(--e-light) 120ms;
}
html.motion [data-reveal].is-revealed .section-title__rule{ transform: scaleX(1); }
```

Uso:

```html
<h2 data-reveal>Expertos con los que he colaborado
  <span class="section-title__rule" aria-hidden="true"></span>
</h2>

<div class="collab-track" data-carousel data-reveal-stagger="4"> … </div>

<section class="bio" data-reveal> … </section>
<ul class="socials" data-reveal-stagger="6"> … </ul>
```

**Notas de implementación**

- `one-shot` obligatorio (`unobserve`). Re-animar al volver a subir es la marca de
  agua del portafolio genérico y además dobla el coste.
- No se pone `will-change` en los elementos revelados. Son transiciones de un disparo:
  el navegador promociona solo y libera solo. Poner `will-change` en 15 elementos
  reserva memoria de GPU que no se recupera.
- No se anima nada texto-a-texto por carácter (ver §9, descartes).

---

## 3. CTA: hover, press y el barrido — el momento clave

### 3.1 Estructura de capas

Cinco capas para poder animar solo `transform` y `opacity`:

```html
<a class="cta" href="…">
  <span class="cta__glow"  aria-hidden="true"></span>  <!-- resplandor exterior -->
  <span class="cta__base"  aria-hidden="true"></span>  <!-- degradado en reposo -->
  <span class="cta__hot"   aria-hidden="true"></span>  <!-- degradado caliente, opacity 0 -->
  <span class="cta__shine" aria-hidden="true"></span>  <!-- banda de brillo -->
  <span class="cta__body">
    <span class="cta__kicker">Formación en vivo</span>
    <strong class="cta__label">TALLERES</strong>
    <svg class="cta__arrow" aria-hidden="true">…</svg>
  </span>
</a>
```

### 3.2 CSS

```css
.cta{
  position: relative;
  display: block;
  isolation: isolate;
  border-radius: 22px;
  overflow: hidden;                 /* recorta el barrido a la tarjeta */
  padding: 22px 24px;
  color: var(--ink);
  text-decoration: none;

  /* Capa de composición permanente. Son 3 botones: coste asumible y
     evita el hipo del primer hover/tap. */
  transform: translate3d(0, 0, 0);
  will-change: transform;

  /* Sombra ESTÁTICA. Nunca se anima: el resplandor vive en .cta__glow. */
  box-shadow:
    0 1px 0 0 rgba(255,255,255,.22) inset,
    0 10px 30px -14px rgba(255,65,59,.42);

  /* Regla de asimetría: la salida (aquí, en la base) es más lenta. */
  transition: transform var(--d-out) var(--e-glide);

  -webkit-tap-highlight-color: transparent;
  touch-action: manipulation;       /* mata el retardo de 300ms en iOS */
}

.cta__base, .cta__hot, .cta__shine, .cta__glow{
  position: absolute;
  border-radius: inherit;
  pointer-events: none;
}

.cta__base, .cta__hot{ inset: 0; z-index: -2; }

.cta__base{
  background: linear-gradient(118deg,
    var(--fire-red) 0%, var(--fire-orange) 52%, var(--fire-gold) 100%);
}

/* El degradado no cambia de stops (eso sería repaint): se cruza con otro
   degradado más caliente por opacidad. */
.cta__hot{
  background: linear-gradient(118deg,
    #FF5A46 0%, #FF9A52 38%, #FFD887 76%, #FFF3D0 100%);
  opacity: 0;
  transition: opacity var(--d-out) var(--e-fade);
}

/* Resplandor exterior. El blur es ESTÁTICO — se rasteriza una vez.
   Solo su opacity se anima, y opacity NO invalida el ráster. */
.cta__glow{
  inset: 6px 10px -8px 10px;
  z-index: -3;
  background: linear-gradient(118deg, var(--fire-red), var(--fire-orange) 55%, var(--fire-gold));
  filter: blur(20px);
  opacity: .30;
  will-change: opacity;
  transition: opacity var(--d-out) var(--e-fade);
}

/* Banda de brillo: fuera del lienzo en reposo. */
.cta__shine{
  top: -25%; bottom: -25%; left: 0;
  width: 40%;
  z-index: -1;
  background: linear-gradient(90deg,
    rgba(255,255,255,0)   0%,
    rgba(255,255,255,.06) 28%,
    rgba(255,255,255,.46) 50%,
    rgba(255,255,255,.06) 72%,
    rgba(255,255,255,0)   100%);
  mix-blend-mode: screen;
  transform: translate3d(-165%, 0, 0) skewX(-16deg);
}

.cta__arrow{
  transition: transform var(--d-out) var(--e-glide);
}

/* ======================= HOVER (solo punteros finos) ======================= */
/* El guard es obligatorio: sin él, Android/iOS dejan el hover "pegado"
   después del tap y el botón queda encendido para siempre. */
@media (hover: hover) and (pointer: fine){
  .cta:hover{
    transform: translate3d(0, -3px, 0) scale(1.012);
    transition-duration: var(--d-base);            /* entrada 240ms */
  }
  .cta:hover .cta__hot{
    opacity: 1;
    transition-duration: var(--d-base);
  }
  .cta:hover .cta__glow{
    opacity: .85;
    transition-duration: var(--d-base);
  }
  .cta:hover .cta__arrow{
    transform: translate3d(4px, 0, 0);
    transition-duration: var(--d-base);
  }
  /* El barrido es `animation`, NO `transition`. Ver nota abajo. */
  .cta:hover .cta__shine{
    animation: cta-sweep var(--d-sweep) var(--e-sweep) 1;
  }
}

@keyframes cta-sweep{
  from{ transform: translate3d(-165%, 0, 0) skewX(-16deg); }
  to  { transform: translate3d(305%, 0, 0)  skewX(-16deg); }
}

/* ======================= FOCO DE TECLADO ======================= */
/* Fuera del media query de hover: el teclado existe en cualquier dispositivo. */
.cta:focus-visible{
  outline: 2px solid var(--fire-gold);
  outline-offset: 3px;
}
.cta:focus-visible .cta__hot{ opacity: 1; transition-duration: var(--d-base); }
.cta:focus-visible .cta__glow{ opacity: .85; }
/* El foco NO mueve el botón: mover el elemento enfocado desorienta. */

/* ======================= PRESS ======================= */
/* Después de :hover en el orden de fuente → gana en igualdad de especificidad. */
.cta:active{
  transform: translate3d(0, -1px, 0) scale(.978);
  transition-duration: var(--d-tap);               /* 90ms */
  transition-timing-function: var(--e-press);
}
.cta:active .cta__hot{
  opacity: 1;
  transition-duration: var(--d-tap);
}
.cta:active .cta__glow{
  opacity: 1;
  transition-duration: var(--d-tap);
}
```

**Por qué el barrido es `animation` y no `transition`.**
Con `transition`, al salir el cursor la banda **vuelve hacia atrás**: la luz viaja en
reversa. Eso rompe la metáfora y se nota mucho. Con `animation` en `:hover`, al
retirar el cursor la animación se cancela y la banda salta a su posición base, que
está **fuera del lienzo recortado** (`-165%`) y por tanto invisible. No hay reverso
ni salto perceptible. Además, volver a entrar re-dispara el barrido desde cero.

### 3.3 Móvil: press inmediato y barrido en el tap

En táctil no hay hover, así que el barrido se dispara por `pointerdown` con la Web
Animations API. **`pointerdown`, nunca `click`**: `click` espera a `pointerup`, lo que
mete 80–250ms de latencia según cuánto tarde el dedo en levantarse.

```js
/* js/cta.js */
import { reduce } from './motion.js';

const SWEEP_KEYFRAMES = [
  { transform: 'translate3d(-165%,0,0) skewX(-16deg)' },
  { transform: 'translate3d(305%,0,0)  skewX(-16deg)' }
];
const SWEEP_OPTS = {
  duration: 700,
  easing: 'cubic-bezier(.32,0,.12,1)',
  fill: 'none'                      /* al terminar, vuelve solo a la base */
};

document.querySelectorAll('.cta').forEach(cta => {
  const shine = cta.querySelector('.cta__shine');
  if (!shine) return;

  cta.addEventListener('pointerdown', (e) => {
    if (e.pointerType === 'mouse') return;   /* en ratón ya lo hace el :hover */
    if (reduce.matches) return;
    shine.getAnimations().forEach(a => a.cancel());   /* sin acumular capas */
    shine.animate(SWEEP_KEYFRAMES, SWEEP_OPTS);
  }, { passive: true });
});
```

**Presupuesto de latencia táctil, desglosado:**

| Evento | t (ms) | Qué ve/siente el usuario |
|---|---|---|
| `pointerdown` | 0 | — |
| `:active` aplicado por el compositor | 0–16 | el botón empieza a hundirse |
| escala `.978` completa | **90** | feedback completo |
| `.cta__hot` a opacidad 1 | 90 | el degradado se calienta |
| barrido completo | 700 | confirmación estética, ya post-feedback |

El feedback obligatorio (escala + calentamiento) cierra en **90ms**, por debajo del
presupuesto de 100ms. El barrido es adorno y puede solaparse con la navegación.

**Detalles que se olvidan y rompen esto:**

- `touch-action: manipulation` en `.cta` — sin él, iOS retiene 300ms buscando doble-tap.
- `-webkit-tap-highlight-color: transparent` — el rectángulo gris del sistema aparece
  antes que nuestra animación y la contradice.
- En iOS, `:active` no se aplica a elementos que no son enlaces si no hay ningún
  listener de touch en el documento. Nuestros CTA son `<a>`, así que funciona; si
  alguno pasa a ser `<button>`, añadir
  `document.addEventListener('touchstart', () => {}, {passive:true})`.
- No usar `:hover` para nada que sea información. Todo el estado que importa vive
  también en `:focus-visible` y `:active`.

---

## 4. El glow del hero: respiración

Es lo único que se mueve de forma permanente en toda la página. Por eso es el elemento
con el presupuesto más ajustado.

### 4.1 Estructura

```html
<div class="hero__glow" aria-hidden="true">
  <span class="hero__glow-core hero__glow-core--a"></span>
  <span class="hero__glow-core hero__glow-core--b"></span>
</div>
```

### 4.2 CSS

```css
.hero__glow{
  position: absolute;
  inset: -18% -12% auto -12%;
  height: 82%;
  z-index: 0;                     /* detrás de la foto y del texto */
  pointer-events: none;
  contain: paint;                 /* aísla el repaint del resto de la página */
}

.hero__glow-core{
  position: absolute;
  border-radius: 50%;
  transform: translate3d(0, 0, 0);
  will-change: transform, opacity; /* solo 2 elementos, permanente, justificado */
}

/* SIN filter: blur(). El degradado radial ya cae a transparente de forma suave.
   Ver §9: un blur sobre una capa con scale animado invalida el ráster cada frame. */
.hero__glow-core--a{
  left: 6%; top: 0;
  width: 74%; aspect-ratio: 1 / .92;
  background: radial-gradient(closest-side at 50% 46%,
    rgba(255,208,130,.52) 0%,
    rgba(254,128,63,.34) 30%,
    rgba(255,65,59,.16)  56%,
    rgba(255,65,59,0)    78%);
  animation: breathe-a var(--breath-a) var(--e-breathe) infinite alternate;
}

.hero__glow-core--b{
  right: 2%; top: 14%;
  width: 62%; aspect-ratio: 1 / 1.1;
  background: radial-gradient(closest-side at 44% 50%,
    rgba(255,65,59,.34) 0%,
    rgba(254,128,63,.20) 38%,
    rgba(254,128,63,0)   74%);
  animation: breathe-b var(--breath-b) var(--e-breathe) infinite alternate;
  animation-delay: -3200ms;       /* arranca desfasado desde el frame 0 */
}

@keyframes breathe-a{
  from{ transform: translate3d(0, 0, 0)      scale(1);    opacity: .58; }
  to  { transform: translate3d(0, -1.6%, 0)  scale(1.06); opacity: .84; }
}
@keyframes breathe-b{
  from{ transform: translate3d(0, 0, 0)     scale(1.02); opacity: .32; }
  to  { transform: translate3d(1.2%, 1%, 0) scale(1);    opacity: .54; }
}
```

### 4.3 Por qué estos números

- **Dos ciclos primos entre sí (9s y 13s).** El patrón combinado no se repite hasta los
  **117 segundos**. Nadie está tanto tiempo en un link in bio, así que la respiración
  nunca se percibe como un loop. Un solo blob con un ciclo de 4s se detecta en 3
  repeticiones y se vuelve un tic nervioso.
- **Delta de escala 6%, delta de opacidad 26 puntos, sobre una forma muy difusa.**
  Es el umbral en el que la visión periférica registra "está vivo" pero la visión
  foveal enfocada en el texto no detecta cambio. Por encima de ~10% de escala empieza
  a tirar de la mirada.
- **`alternate` + easing simétrico (`.45,0,.55,1`)** para que no haya un "latido":
  ir y volver deben ser indistinguibles. Con un ease-out se percibe un pulso cardiaco,
  que es exactamente lo que no queremos.
- El blob `b` sube en opacidad mientras `a` está a mitad de recorrido: la luz parece
  desplazarse lateralmente, no inflarse.

### 4.4 Contraste (bloqueante)

El glow queda **detrás** del texto del hero. Medir el contraste del `h1` y del tagline
**en el frame de máxima luminancia** (`a` al 84% de opacidad y `b` al 54%
simultáneamente — puede forzarse con `animation-play-state: paused` y
`animation-delay` negativo en DevTools). Requisito: **≥ 4.5:1** para el tagline y
**≥ 3:1** para el `h1` si es ≥ 24px bold. Si no da, la solución es un velo
`linear-gradient(to top, rgba(16,16,16,.72), transparent)` estático entre el glow y el
texto — **nunca** bajar el contraste ni animar el velo.

---

## 5. Indicador de scroll

Una flecha dentro de un círculo de vidrio, como en `ref-layout-hero.png`.

**La flecha no rebota.** Cae, se apaga, y reaparece arriba ya invisible. Es una gota de
luz descendiendo, no una pelota.

```css
.scroll-hint{
  position: relative;
  display: grid;
  place-items: center;
  width: 46px; height: 46px;
  border-radius: 50%;
  background: rgba(250,250,250,.05);
  border: 1px solid rgba(250,250,250,.12);
  transition:
    opacity   var(--d-out) var(--e-fade),
    transform var(--d-out) var(--e-fade);
}

.scroll-hint__arrow{
  will-change: transform, opacity;
  animation: hint-fall 2400ms cubic-bezier(.33, 0, .67, 1) infinite;
}

/* 45% del ciclo es pausa: el movimiento aparece como un evento, no como un motor. */
@keyframes hint-fall{
  0%,  44% { transform: translate3d(0, -3px, 0); opacity: 0;   }
  54%      { transform: translate3d(0,  0px, 0); opacity: 1;   }
  82%      { transform: translate3d(0,  9px, 0); opacity: 0;   }
  100%     { transform: translate3d(0,  9px, 0); opacity: 0;   }
}

/* Cumplió su función: se va y no vuelve. */
.scroll-hint.is-done{
  opacity: 0;
  transform: translate3d(0, 8px, 0);
  pointer-events: none;
}
```

```js
/* js/scroll-hint.js */
const hint = document.querySelector('.scroll-hint');
if (hint){
  const dismiss = () => {
    hint.classList.add('is-done');
    /* la animación en bucle se detiene tras el fade: cero coste residual */
    setTimeout(() => { hint.style.animation = 'none';
                       hint.querySelector('.scroll-hint__arrow').style.animation = 'none';
                       hint.hidden = true; }, 400);
  };
  const onScroll = () => { if (window.scrollY > 40) dismiss(); };
  window.addEventListener('scroll', onScroll, { passive: true, once: false });
  /* liberamos el listener en cuanto se cumple */
  window.addEventListener('scroll', function self(){
    if (window.scrollY > 40) window.removeEventListener('scroll', self);
  }, { passive: true });
}
```

Si el indicador es clicable (recomendado — es un atajo real), hacerlo `<a href="#accesos">`
y dejar el desplazamiento a `html{ scroll-behavior: smooth }`, desactivado bajo
reduced-motion (§10).

---

## 6. Carrusel de colaboraciones

**Decisión de arquitectura: la física la pone el navegador.** `scroll-snap` nativo +
scroll táctil nativo dan momentum correcto por plataforma, en el hilo de composición,
gratis. El JS solo añade (a) arrastre con ratón en desktop, (b) proyección de flick al
soltar, (c) estado de los dots y de la card centrada. Ver §9 para por qué se descartó
una implementación de inercia propia.

### 6.1 CSS

```css
.collab-track{
  display: flex;
  gap: 14px;
  overflow-x: auto;
  overflow-y: hidden;
  scroll-snap-type: x mandatory;
  scroll-behavior: smooth;
  overscroll-behavior-x: contain;      /* no dispara el back-swipe del navegador */
  scroll-padding-inline: 50%;
  padding-inline: max(16px, calc(50% - 108px));  /* la 1ª y última card centran */
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
  cursor: grab;
}
.collab-track::-webkit-scrollbar{ display: none; }

.collab-track.is-dragging{
  cursor: grabbing;
  scroll-snap-type: none;              /* el snap pelea con el arrastre manual */
  scroll-behavior: auto;
  user-select: none;
}

.collab-card{
  flex: 0 0 216px;
  scroll-snap-align: center;
  border-radius: 20px;
  overflow: hidden;

  /* Estado de reposo = card lateral. Solo transform + opacity. */
  transform: scale(.955);
  opacity: .62;
  transition:
    transform 340ms var(--e-glide),
    opacity   340ms var(--e-glide);
}
.collab-card.is-focus{
  transform: scale(1);
  opacity: 1;
}

/* La barra de luz inferior de la card (como el degradado morado del referente)
   solo aparece en la card centrada. Escala en Y, no altura. */
.collab-card__bar{
  transform: scaleY(.25);
  transform-origin: 50% 100%;
  opacity: .4;
  transition: transform 340ms var(--e-glide), opacity 340ms var(--e-glide);
}
.collab-card.is-focus .collab-card__bar{ transform: scaleY(1); opacity: 1; }

/* No hay hover en las cards: compite con el estado "centrada" y en táctil
   no existe. La card centrada ES el estado activo. */
```

> **`transform: scale()` no afecta a las posiciones de snap**, porque el snap usa la
> caja de layout. Por eso se puede escalar la card centrada sin que el carrusel derive.
> Si se usara `flex-basis` o `width` para el mismo efecto, cada cambio recalcularía el
> layout de todo el track a 60fps. Prohibido.

### 6.2 Dots

`width` animado sería layout. El dot es una cápsula de tamaño fijo con un relleno que
escala en X desde el centro.

```html
<div class="dots" role="tablist" aria-label="Colaboraciones">
  <button class="dot" data-carousel-dot role="tab" aria-selected="true"
          aria-label="Colaboración 1 de 6">
    <span class="dot__track" aria-hidden="true">
      <span class="dot__fill"></span>
      <span class="dot__fire"></span>
    </span>
  </button>
  …
</div>
```

```css
.dots{ display: flex; gap: 2px; justify-content: center; }

.dot{
  appearance: none; border: 0; background: none; padding: 0;
  width: 34px; height: 34px;            /* diana ≥24px (WCAG 2.5.8 AA) */
  display: grid; place-items: center;
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;
}
.dot:focus-visible{ outline: 2px solid var(--fire-gold); outline-offset: 2px; border-radius: 8px; }

.dot__track{ position: relative; width: 22px; height: 6px; border-radius: 999px; }

.dot__fill, .dot__fire{
  position: absolute; inset: 0; border-radius: inherit;
  transform: scaleX(.2727);             /* 6 / 22 → círculo */
  transition: transform var(--d-base) var(--e-glide),
              opacity   var(--d-fast) linear;
}
.dot__fill{ background: rgba(250,250,250,.24); }
.dot__fire{
  background: linear-gradient(90deg, var(--fire-red), var(--fire-orange) 55%, var(--fire-gold));
  opacity: 0;
}

.dot.is-active .dot__fill{ transform: scaleX(1); opacity: 0; }
.dot.is-active .dot__fire{ transform: scaleX(1); opacity: 1; }
```

El dot activo **crece desde el centro** (240ms) mientras el fuego entra por opacidad
(160ms). El fuego llega antes que la forma: se enciende y luego se estira. Coherente
con la asimetría de ignición.

### 6.3 JS completo

```js
/* js/carousel.js */
import { reduce } from './motion.js';

(function initCarousel(){
  const track = document.querySelector('[data-carousel]');
  if (!track) return;

  const cards = Array.from(track.children);
  const dots  = Array.from(document.querySelectorAll('[data-carousel-dot]'));
  if (!cards.length) return;

  /* ---------- Geometría cacheada: NO se lee layout en cada frame de scroll ---------- */
  let centers = [];
  const measure = () => {
    centers = cards.map(c => c.offsetLeft + c.offsetWidth / 2);
  };
  measure();
  if ('ResizeObserver' in window) new ResizeObserver(measure).observe(track);
  else window.addEventListener('resize', measure, { passive: true });

  /* ---------- Sincronía de estado, throttled a un rAF ---------- */
  let rafId = 0, active = -1;

  const nearestIndex = (scrollLeft) => {
    const focus = scrollLeft + track.clientWidth / 2;
    let best = 0, bestD = Infinity;
    for (let i = 0; i < centers.length; i++){
      const d = Math.abs(centers[i] - focus);
      if (d < bestD){ bestD = d; best = i; }
    }
    return best;
  };

  const sync = () => {
    rafId = 0;
    const i = nearestIndex(track.scrollLeft);
    if (i === active) return;
    active = i;
    for (let k = 0; k < cards.length; k++){
      cards[k].classList.toggle('is-focus', k === i);
    }
    for (let k = 0; k < dots.length; k++){
      const on = k === i;
      dots[k].classList.toggle('is-active', on);
      dots[k].setAttribute('aria-selected', on ? 'true' : 'false');
      dots[k].tabIndex = on ? 0 : -1;      /* un solo tab stop en el grupo */
    }
  };
  const queueSync = () => { if (!rafId) rafId = requestAnimationFrame(sync); };

  track.addEventListener('scroll', queueSync, { passive: true });
  sync();

  /* ---------- Navegación programática ---------- */
  const goTo = (i) => {
    const idx = Math.max(0, Math.min(i, centers.length - 1));
    track.scrollTo({
      left: centers[idx] - track.clientWidth / 2,
      behavior: reduce.matches ? 'auto' : 'smooth'
    });
  };

  dots.forEach((dot, i) => dot.addEventListener('click', () => goTo(i)));

  /* ---------- Teclado ---------- */
  track.tabIndex = 0;
  track.setAttribute('role', 'group');
  track.setAttribute('aria-roledescription', 'carrusel');
  track.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight'){ e.preventDefault(); goTo(active + 1); }
    if (e.key === 'ArrowLeft' ){ e.preventDefault(); goTo(active - 1); }
    if (e.key === 'Home'){ e.preventDefault(); goTo(0); }
    if (e.key === 'End' ){ e.preventDefault(); goTo(centers.length - 1); }
  });

  /* ---------- Arrastre con ratón (en táctil manda el scroll nativo) ---------- */
  let dragging = false, startX = 0, startScroll = 0;
  let lastX = 0, lastT = 0, velocity = 0, travelled = 0, suppressClick = false;

  const FLICK_MS   = 130;   /* ms de inercia proyectada al soltar */
  const CLICK_SLOP = 6;     /* px por encima de los cuales el gesto NO es un click */

  track.addEventListener('pointerdown', (e) => {
    if (e.pointerType === 'touch') return;
    if (e.button !== 0) return;
    dragging = true;
    travelled = 0; velocity = 0;
    startX = lastX = e.clientX;
    startScroll = track.scrollLeft;
    lastT = e.timeStamp;
    track.setPointerCapture(e.pointerId);
    track.classList.add('is-dragging');
  });

  track.addEventListener('pointermove', (e) => {
    if (!dragging) return;
    const dx = e.clientX - lastX;
    const dt = Math.max(1, e.timeStamp - lastT);
    velocity = dx / dt;                       /* px/ms, en espacio de puntero */
    lastX = e.clientX;
    lastT = e.timeStamp;
    travelled += Math.abs(dx);
    /* Ratio 1:1. Cualquier multiplicador >1 se siente resbaladizo y desconecta
       el dedo/cursor del contenido. */
    track.scrollLeft = startScroll - (e.clientX - startX);
    queueSync();
  });

  const endDrag = (e) => {
    if (!dragging) return;
    dragging = false;
    track.classList.remove('is-dragging');
    if (e && e.pointerId !== undefined && track.hasPointerCapture(e.pointerId)){
      track.releasePointerCapture(e.pointerId);
    }
    suppressClick = travelled > CLICK_SLOP;

    /* Proyección de flick: el destino no es donde solté, es donde habría llegado. */
    const projected = track.scrollLeft - velocity * FLICK_MS;
    goTo(nearestIndex(projected));
  };

  track.addEventListener('pointerup', endDrag);
  track.addEventListener('pointercancel', endDrag);

  /* Un arrastre no debe abrir el enlace de la card. Fase de captura. */
  track.addEventListener('click', (e) => {
    if (!suppressClick) return;
    e.preventDefault();
    e.stopPropagation();
    suppressClick = false;
  }, true);

  /* Cierre exacto del estado cuando el scroll nativo termina de asentarse. */
  if ('onscrollend' in window) track.addEventListener('scrollend', sync);
})();
```

**Física, en números:**

| Parámetro | Valor | Por qué |
|---|---|---|
| ratio arrastre → scroll | 1 : 1 | el contenido sigue al cursor exactamente; >1 se siente barato |
| umbral de cancelación de click | 6px | por debajo es temblor de mano, no gesto |
| proyección de flick | `velocity × 130ms` | 130ms es el punto en el que un flick corto avanza 1 card y uno fuerte 2–3 |
| aterrizaje | `scrollTo({behavior:'smooth'})` | curva nativa, en el compositor, sin rAF propio |
| snap | `x mandatory` + `align: center` | mandatory porque son cards discretas; con `proximity` se queda a medias |
| transición de card | 340ms `--e-glide` | más larga que el snap para que el foco "llegue" después del movimiento |

**Enhancement opcional (fuera del hilo principal).** Donde exista scroll-driven
animation, el escalado de las cards puede salir del JS por completo:

```css
@supports (animation-timeline: view(inline)){
  html.motion .collab-card{
    animation: card-focus linear both;
    animation-timeline: view(inline);
    animation-range: entry 18% exit 82%;
    transition: none;
  }
  @keyframes card-focus{
    0%,100% { transform: scale(.955); opacity: .62 }
    50%     { transform: scale(1);    opacity: 1   }
  }
}
```

El JS sigue siendo la línea base y sigue gobernando los dots. No se elimina.

---

## 7. Iconos de redes: ignición

Dos copias del icono superpuestas: blanca y con el degradado de fuego. Se cruzan por
opacidad. Cero repaint, y el icono lleva el degradado real de marca, no un naranja plano.

```html
<!-- sprite del degradado, una vez en el documento -->
<svg width="0" height="0" aria-hidden="true" style="position:absolute">
  <defs>
    <linearGradient id="fireGrad" x1="0" y1="1" x2="1" y2="0">
      <stop offset="0"   stop-color="#FF413B"/>
      <stop offset=".55" stop-color="#FE803F"/>
      <stop offset="1"   stop-color="#FFC252"/>
    </linearGradient>
  </defs>
</svg>

<a class="social" href="…" aria-label="TikTok de Jhei Trujillo">
  <span class="social__ring" aria-hidden="true"></span>
  <svg class="social__ico social__ico--base" aria-hidden="true"><use href="#i-tiktok"/></svg>
  <svg class="social__ico social__ico--fire" aria-hidden="true"><use href="#i-tiktok"/></svg>
</a>
```

```css
.social{
  position: relative;
  display: grid; place-items: center;
  width: 48px; height: 48px;
  border-radius: 50%;
  background: rgba(250,250,250,.045);
  border: 1px solid rgba(250,250,250,.11);
  transition: transform var(--d-out) var(--e-glide);   /* salida lenta */
  -webkit-tap-highlight-color: transparent;
  touch-action: manipulation;
}

.social__ico{
  position: absolute;
  width: 20px; height: 20px;
  transition: opacity var(--d-out) var(--e-fade);      /* apagado 320ms */
}
.social__ico--base{ fill: var(--paper); opacity: .74; }
.social__ico--fire{ fill: url(#fireGrad); opacity: 0; }

/* Aro de fuego: crece desde dentro. Borde estático, solo transform+opacity. */
.social__ring{
  position: absolute; inset: -1px;
  border-radius: 50%;
  border: 1px solid var(--fire-orange);
  opacity: 0;
  transform: scale(.82);
  transition: opacity var(--d-out) var(--e-fade),
              transform var(--d-out) var(--e-glide);
}

/* --- Ignición: 160ms. Apagado: 320ms (definido en la base). --- */
@media (hover: hover) and (pointer: fine){
  .social:hover{ transform: translate3d(0, -2px, 0); transition-duration: var(--d-fast); }
  .social:hover .social__ico--base{ opacity: 0; transition-duration: var(--d-fast); }
  .social:hover .social__ico--fire{ opacity: 1; transition-duration: var(--d-fast); }
  .social:hover .social__ring{ opacity: 1; transform: scale(1); transition-duration: var(--d-fast); }
}

.social:focus-visible{ outline: 2px solid var(--fire-gold); outline-offset: 3px; }
.social:focus-visible .social__ico--base{ opacity: 0; }
.social:focus-visible .social__ico--fire{ opacity: 1; }
.social:focus-visible .social__ring{ opacity: 1; transform: scale(1); }

.social:active{
  transform: scale(.92);
  transition-duration: var(--d-tap);
  transition-timing-function: var(--e-press);
}
.social:active .social__ico--fire{ opacity: 1; transition-duration: var(--d-tap); }
.social:active .social__ico--base{ opacity: 0; transition-duration: var(--d-tap); }
```

La fila entra con la cascada de §2 (`data-reveal-stagger`, 70ms entre iconos): se
encienden de izquierda a derecha, como una guirnalda de brasas.

---

## 8. El detalle: **ignición en cascada**

**Qué es.** La foto del hero está envuelta en un `<button>`. Al pulsarla, un pulso de luz
sale de la foto y recorre los tres CTA de arriba abajo con 130ms de separación: el mismo
barrido del hover, disparado en secuencia, con un levantamiento mínimo de cada tarjeta.
Duración total **1160ms**. Una vez cada 4 segundos como máximo.

**Por qué esto y no otra cosa. Cuatro razones, en orden de peso:**

1. **Convierte un toque muerto en conversión.** La foto es el elemento con más
   affordance visual de la página y no es un enlace: hoy el toque no hace nada. La
   cascada lo transforma en un *spotlight dirigido a los tres botones que pagan la
   página*. Es el único easter egg que se me ocurre que **sube** la probabilidad de
   click en lugar de distraer de ella. Si hay que elegir un solo momento de deleite,
   que sea el que empuja al negocio.
2. **Es la metáfora de marca, ejecutada literalmente.** "Haces de luz cálida cruzando
   la oscuridad". Aquí la luz sale del autor y cruza la página. No es una broma pegada
   encima: es la tesis visual funcionando.
3. **Es comentable y capturable.** Es lo que la gente graba en pantalla y manda por
   DM: "mira lo que hace cuando le tocas la cara". Para alguien que vende **viralidad**,
   que su propio link in bio contenga un micro-momento compartible es coherencia de
   producto, no capricho.
4. **Coste ~cero.** No añade ningún asset, ningún rAF, ni una sola animación nueva de
   propiedad caras. Reutiliza la capa `.cta__shine` que ya existe y ya está promocionada
   para el hover: son tres animaciones de `transform` sobre capas que el compositor ya
   tiene en memoria. Presupuesto adicional medido: **1 nodo** (el destello de origen),
   **0 KB de assets, ~1.3KB de JS**.

**Lo que deliberadamente NO es:** no hay confeti, no hay emojis, no hay sonido, no hay
partículas, no hay konami code, no hay easter egg oculto que nadie encuentre. Un solo
detalle, en el sitio con más tráfico de atención, hecho con el vocabulario que ya
tiene la página.

### 8.1 Marcado

```html
<button class="hero__ignite" data-ignite type="button"
        aria-label="Encender los accesos">
  <span class="hero__photo-frame">
    <img class="hero__photo" src="…" alt="Jhei Trujillo"
         fetchpriority="high" decoding="async" width="…" height="…">
  </span>
  <!-- destello de origen: la luz sale de él. Único nodo que añade el efecto. -->
  <span class="hero__spark" data-ignite-spark aria-hidden="true"></span>
</button>
```

Es un `<button>` real con etiqueta real: alcanzable con teclado, anunciado con sentido
por un lector de pantalla, y no finge ser decorativo. Nada del estado cambia de forma
informativa, así que no necesita `aria-live` ni `aria-pressed`.

### 8.2 CSS

```css
.hero__ignite{
  appearance: none; border: 0; padding: 0; background: none;
  position: relative;              /* contiene a .hero__spark */
  isolation: isolate;
  display: block; cursor: pointer;
  border-radius: 28px;
  -webkit-tap-highlight-color: transparent;
  touch-action: manipulation;
  transition: transform var(--d-out) var(--e-glide);
}
.hero__ignite:focus-visible{ outline: 2px solid var(--fire-gold); outline-offset: 6px; }
.hero__ignite:active{
  transform: scale(.988);
  transition-duration: var(--d-tap);
  transition-timing-function: var(--e-press);
}
/* Destello de origen. Capa propia, opacity 0 en reposo, animada por WAAPI.
   Deliberadamente NO se toca .hero__glow-core: tiene una `animation` en bucle
   sobre `opacity`, y en la cascada CSS una animación siempre gana a una
   transición — cualquier `transition: opacity` que le pusiéramos ahí sería
   código muerto. Este es el bug clásico de "el flash no se ve". */
.hero__spark{
  position: absolute;
  inset: -14%;
  z-index: -1;
  pointer-events: none;
  border-radius: 50%;
  background: radial-gradient(closest-side at 50% 50%,
    rgba(255,243,208,.55) 0%,
    rgba(255,194,82,.34) 32%,
    rgba(254,128,63,.14) 58%,
    rgba(254,128,63,0)   78%);
  opacity: 0;
  /* Sin `will-change`: solo anima al hacer click. La WAAPI la promociona
     durante la animación y la libera al terminar. Así el presupuesto de
     capas de §9.1 se mantiene en 12. */
}
```

### 8.3 JS

```js
/* js/ignite.js */
import { reduce } from './motion.js';

(function initIgnite(){
  const btn   = document.querySelector('[data-ignite]');
  const spark = document.querySelector('[data-ignite-spark]');
  const ctas  = Array.from(document.querySelectorAll('.cta'));
  if (!btn || !ctas.length) return;

  const SWEEP = [
    { transform: 'translate3d(-165%,0,0) skewX(-16deg)' },
    { transform: 'translate3d(305%,0,0)  skewX(-16deg)' }
  ];
  const LIFT = [
    { transform: 'translate3d(0,0,0) scale(1)' },
    { transform: 'translate3d(0,-3px,0) scale(1.012)', offset: .34 },
    { transform: 'translate3d(0,0,0) scale(1)' }
  ];
  /* El destello: ignición rápida (opacity 0→1 en ~90ms del ciclo) y apagado
     largo. Misma asimetría de brasa que el resto del sistema. */
  const SPARK = [
    { opacity: 0,   transform: 'scale(.88)', offset: 0    },
    { opacity: .95, transform: 'scale(1)',   offset: .18  },
    { opacity: 0,   transform: 'scale(1.1)', offset: 1    }
  ];

  const STEP  = 130;   /* separación entre CTA */
  const HEAD  = 140;   /* la luz tarda en salir de la foto */
  const LOCK  = 4000;  /* cooldown: machacar el botón no cuesta frames */

  let lastFire = -Infinity;

  btn.addEventListener('click', () => {
    if (reduce.matches) return;                 /* respeto duro, ver §10 */
    const now = performance.now();
    if (now - lastFire < LOCK) return;
    lastFire = now;

    if (spark){
      spark.getAnimations().forEach(a => a.cancel());
      spark.animate(SPARK, {
        duration: 560,
        easing: 'cubic-bezier(.22,.61,.36,1)',
        fill: 'none'
      });
    }

    ctas.forEach((cta, i) => {
      const shine = cta.querySelector('.cta__shine');
      const delay = HEAD + i * STEP;
      if (shine){
        shine.getAnimations().forEach(a => a.cancel());
        shine.animate(SWEEP, {
          duration: 760, delay,
          easing: 'cubic-bezier(.32,0,.12,1)', fill: 'none'
        });
      }
      cta.animate(LIFT, {
        duration: 620, delay,
        easing: 'cubic-bezier(.22,.61,.36,1)', fill: 'none'
      });
    });
  });
})();
```

`fill: 'none'` es intencional: al acabar, la WAAPI libera el `transform` y el estado
vuelve a lo que diga el CSS (`:hover` incluido, si el cursor está encima). Sin eso, el
botón se quedaría congelado y el hover dejaría de funcionar.

---

## 9. Presupuesto de rendimiento

**Objetivo:** 60fps sostenidos en un Android de gama media (referencia: Snapdragon
6xx / Helio G85, 4GB, DPR 2.75) durante scroll, arrastre del carrusel y respiración
del hero simultáneos.

### 9.1 Presupuesto de capas de composición

Máximo **13 capas promocionadas** simultáneas, de las cuales solo **8 son permanentes**.
Reparto:

| Elemento | Capas | Permanente | Justificación |
|---|---|---|---|
| `.hero__glow-core` ×2 | 2 | sí | animan en bucle; `will-change: transform, opacity` |
| `.cta` ×3 | 3 | sí | solo 3; evita el hipo del primer tap |
| `.cta__glow` ×3 | 3 | sí | `will-change: opacity` |
| `.cta__shine` ×3 | 3 | al animar | promoción implícita por la animación |
| `.scroll-hint__arrow` | 1 | hasta el primer scroll | se destruye al hacer `hidden` |
| `.hero__spark` (§8) | 1 | no | solo durante los 560ms de la ignición; la WAAPI la libera |
| **Total pico** | **13** | | pico real solo si el usuario dispara la ignición antes de hacer scroll |

**Fuera del presupuesto, explícitamente:** las cards del carrusel (hasta 9) **no** se
promocionan con `will-change`. Su transición de 340ms se dispara de una en una y el
navegador promociona y libera solo. Nueve capas permanentes de 216×320px a DPR 2.75
son ~46MB de textura: es el camino directo a que el compositor empiece a descartar.

### 9.2 Reglas de propiedad

| Propiedad | En bucle / scroll / drag | En interacción puntual |
|---|---|---|
| `transform`, `opacity` | ✅ | ✅ |
| `filter: blur()` **estático**, con solo `opacity` animándose | ✅ | ✅ |
| `filter: blur()` con `transform: scale()` animándose | ❌ | ❌ |
| `box-shadow` | ❌ | ❌ (usar capa `__glow` + opacity) |
| `background-position`, `background-size` | ❌ | ❌ |
| `width`, `height`, `top/left`, `margin`, `gap`, `font-size` | ❌ | ❌ |
| `color` / `fill` | ❌ | ⚠️ solo en iconos ≤24px; preferido: cruce de dos copias |
| `backdrop-filter` | ❌ | ⚠️ solo en elementos que no se mueven ni scrollean |

Distinción importante que se malinterpreta a menudo: **un `blur` estático es barato**
(se rasteriza una vez y se cachea) siempre que lo único que se anime sobre él sea
`opacity`, que no invalida el ráster. En cambio animar `scale` sobre una capa con
`blur` **sí** invalida el ráster cada frame, porque cambia la escala de rasterización.
De ahí las dos decisiones aparentemente contradictorias del documento: `.cta__glow`
lleva `blur(20px)` (solo cambia su opacidad) y `.hero__glow-core` **no lleva blur
ninguno** (cambia su escala).

### 9.3 Qué se descartó por coste — y qué se puso en su lugar

| Descartado | Coste real | Sustituto |
|---|---|---|
| **Canvas/WebGL de brasas o partículas en el hero** | un segundo bucle rAF + fill de todo el viewport por frame; en gama media son 8–14ms/frame, o sea el frame entero. Y drena batería con la pestaña abierta | glow por degradados radiales animados con `transform`/`opacity`: 0ms de JS |
| **`filter: blur()` animado en el glow** | reraster de ~390×420px a DPR 2.75 (≈1.2M px) por frame | degradados radiales con caída suave a transparente: la difusión ya está en el gradiente, sin pase de blur |
| **`box-shadow` animado en el hover del CTA** | repaint del elemento en cada frame de la transición | capa `.cta__glow` pre-desenfocada, cruzada por `opacity` |
| **`backdrop-filter` en las cards del carrusel** | recomposición del fondo tras cada card en cada frame de scroll; es lo más caro de toda la lista | los paneles de vidrio de marca se reservan a lo **estático**: panel de bio, botones de redes, círculo del indicador. Ninguno se mueve |
| **Parallax del hero ligado al scroll** | lectura de layout en el handler de scroll y una capa a pantalla completa recompuesta; el efecto en un hero de 100vh en móvil es imperceptible | nada. La entrada escalonada ya da profundidad |
| **Inercia propia del carrusel (rAF + fricción)** | 1 bucle rAF durante todo el gesto + escrituras de `scrollLeft` en el hilo principal, que es exactamente donde aparece el jank | `scroll-snap` nativo + momentum del sistema + `scrollTo({behavior:'smooth'})`. El gesto completo corre fuera del hilo principal |
| **`feTurbulence` / grano SVG animado** | filtro SVG a pantalla completa: inaceptable incluso estático en algunos Android | PNG de grano de 128×128 tileado, `background-repeat`, **estático**, `opacity` fija |
| **Revelado texto por carácter (split text)** | 40–120 nodos y capas nuevas, y retrasa la legibilidad justo cuando el usuario tiene cero paciencia | revelado por línea/bloque. El único barrido de texto es el de la palabra en degradado, una vez (§1.3) |
| **Cursor personalizado / trail de brasas** | eventos de puntero a alta frecuencia + nodos; y no existe en móvil, que es el 90%+ del tráfico de un link in bio | nada |
| **Números que cuentan hacia arriba en la bio** | repaint de texto + reflow por cambio de anchura de dígitos | valores estáticos, con `font-variant-numeric: tabular-nums` si algún día se animan |
| **`animation-timeline: view()` como base** | soporte insuficiente para ser la única implementación | JS como línea base, `view()` bajo `@supports` como mejora (§6.1) |

### 9.4 Otras medidas

- `contain: paint` en `.hero__glow` y en cada sección de contenido: acota el área de
  invalidación.
- `content-visibility: auto` + `contain-intrinsic-size` en las secciones bajo el fold
  (carrusel, bio, footer) recorta el coste de estilo/layout inicial. **Cuidado:** hay
  que declarar `contain-intrinsic-size` con una altura realista o el scrollbar salta,
  y verificar que el IntersectionObserver del §2 sigue disparando (lo hace, pero es lo
  primero que hay que comprobar en QA si un bloque no se revela).
- Todos los listeners de `scroll` y `pointermove` con `{ passive: true }`.
- Ninguna lectura de layout dentro de un handler de scroll: la geometría del carrusel
  está cacheada y se recalcula solo en `ResizeObserver`.
- Imágenes: `width`/`height` explícitos para CLS 0. `fetchpriority="high"` solo en la
  foto del hero; `loading="lazy"` en las cards de colaboraciones.

---

## 10. `prefers-reduced-motion: reduce`

Regla de fondo: bajo reduced-motion la página no es una versión degradada, es la
**misma página sin movimiento**. Toda la información y todo el feedback siguen
existiendo: el CTA sigue reaccionando (con degradado y opacidad), el dot activo sigue
distinguiéndose, la card centrada sigue siendo legible. Lo que desaparece es el
desplazamiento y los bucles.

```css
@media (prefers-reduced-motion: reduce){

  /* ---- 1. Entradas y revelados: contenido presente, sin recorrido ---- */
  html.motion [data-enter],
  html.motion [data-reveal],
  html.motion [data-reveal-stagger] > *,
  html.motion .hero__photo,
  html.motion .hero__glow,
  html.motion .hero__name em::after,
  html.motion .section-title__rule{
    animation: none !important;
    transition: none !important;
    opacity: 1 !important;
    transform: none !important;
  }
  html.motion .hero__name em::after{ opacity: 0 !important; }   /* la banda no pinta */
  html.motion .section-title__rule{ transform: scaleX(1) !important; }

  /* ---- 2. Bucles: fuera, congelados en un estado intermedio bonito ---- */
  .hero__glow-core{
    animation: none !important;
    transform: none !important;
  }
  .hero__glow-core--a{ opacity: .68; }   /* punto medio del ciclo */
  .hero__glow-core--b{ opacity: .42; }

  .scroll-hint__arrow{
    animation: none !important;
    transform: none !important;
    opacity: 1;
  }

  /* ---- 3. CTA: el feedback sobrevive, el movimiento no ---- */
  .cta__shine{ display: none !important; }        /* el barrido ES movimiento */
  .cta,
  .cta:hover,
  .cta:focus-visible,
  .cta:active,
  .cta__arrow{
    transform: none !important;
  }
  .cta{ transition: opacity var(--d-fast) linear !important; }
  .cta:hover  .cta__hot, .cta:focus-visible .cta__hot,
  .cta:active .cta__hot{ opacity: 1; transition: opacity 120ms linear; }
  .cta:hover  .cta__glow, .cta:focus-visible .cta__glow{ opacity: .85; }
  /* Press sin escala: sigue habiendo confirmación táctil, por opacidad. */
  .cta:active{ opacity: .86; transition-duration: 60ms; }

  /* Ignición (§8): el JS ya no dispara nada. Aquí solo se neutraliza el press
     y se garantiza que el destello nunca pinte. */
  .hero__ignite, .hero__ignite:active{ transform: none !important; }
  .hero__ignite:active{ opacity: .9; transition: opacity 60ms linear; }
  .hero__spark{ display: none !important; }

  /* ---- 4. Redes: cruce de opacidad, sin aro que crece ni levantamiento ---- */
  .social, .social:hover, .social:active{ transform: none !important; }
  .social__ring{ transform: none !important; transition: opacity 120ms linear; }
  .social__ico{ transition: opacity 120ms linear; }

  /* ---- 5. Carrusel: sigue siendo un carrusel, deja de deslizarse ---- */
  html{ scroll-behavior: auto !important; }
  .collab-track{ scroll-behavior: auto !important; }
  .collab-card{
    transform: none !important;
    opacity: 1 !important;                        /* todas legibles a la vez */
    transition: none !important;
  }
  .collab-card__bar{ transform: none !important; opacity: 1 !important; }
  /* El foco se marca con un borde estático, no con escala. */
  .collab-card.is-focus{ box-shadow: 0 0 0 2px var(--fire-orange); }

  .dot__fill, .dot__fire{
    transform: scaleX(1) !important;              /* cápsulas fijas */
    transition: opacity 120ms linear !important;
  }

  /* ---- 6. Red de seguridad para cualquier animación futura no prevista ---- */
  *, *::before, *::after{
    animation-iteration-count: 1 !important;
    animation-duration: .01ms !important;
    animation-delay: 0ms !important;
  }
}
```

**Lado JS.** El CSS no basta: hay comportamiento que hay que apagar en código.
Todos los módulos importan el mismo `reduce` de `motion.js`:

| Módulo | Qué hace con `reduce.matches === true` |
|---|---|
| `reveal.js` | revela todo de golpe y no registra el IntersectionObserver |
| `cta.js` | no dispara el barrido en `pointerdown` |
| `carousel.js` | `scrollTo({behavior:'auto'})` — el scroll suave programático es movimiento |
| `ignite.js` | el botón no hace nada (sigue siendo enfocable y etiquetado; no promete un efecto que no va a ocurrir) |
| `scroll-hint.js` | funciona igual: ocultar el indicador tras el scroll no es movimiento gratuito |

**Cambios en caliente.** El usuario puede activar la preferencia con la página abierta:

```js
reduce.addEventListener('change', (e) => {
  if (!e.matches) return;
  document.getAnimations().forEach(a => a.cancel());   /* mata WAAPI en vuelo */
  document.querySelectorAll('[data-reveal], [data-reveal-stagger]')
          .forEach(el => el.classList.add('is-revealed'));
});
```

---

## 11. Tabla maestra de duraciones

| Animación | Duración | Delay | Easing | Bucle |
|---|---|---|---|---|
| Entrada · foto hero (escala) | 520ms | 0 | `.16,1,.3,1` | no |
| Entrada · glow (opacidad) | 700ms | 40ms | `.22,.61,.36,1` | no |
| Entrada · nombre | 400ms | 170ms | `.16,1,.3,1` | no |
| Entrada · barrido del nombre | 780ms | 320ms | `.32,0,.12,1` | **1 vez** |
| Entrada · tagline | 380ms | 235ms | `.16,1,.3,1` | no |
| Entrada · CTA 1/2/3 | 400ms | 320/390/460ms | `.16,1,.3,1` | no |
| Entrada · indicador scroll | 400ms | 620ms | `.16,1,.3,1` | no |
| Revelado al scroll | 380ms | `i × 70ms` | `.16,1,.3,1` | no |
| Subrayado de título (scaleX) | 620ms | 120ms | `.16,1,.3,1` | no |
| CTA · elevación (entrada) | 240ms | 0 | `.22,.61,.36,1` | no |
| CTA · elevación (salida) | 320ms | 0 | `.22,.61,.36,1` | no |
| CTA · degradado caliente | 240 / 320ms | 0 | `.4,0,.6,1` | no |
| CTA · barrido | 700ms | 0 | `.32,0,.12,1` | no |
| CTA · press | **90ms** | 0 | `.4,0,.2,1` | no |
| CTA · flecha | 240 / 320ms | 0 | `.22,.61,.36,1` | no |
| Glow hero · blob A | 9000ms | 0 | `.45,0,.55,1` | ∞ alternate |
| Glow hero · blob B | 13000ms | −3200ms | `.45,0,.55,1` | ∞ alternate |
| Indicador de scroll · caída | 2400ms | 0 | `.33,0,.67,1` | ∞ |
| Indicador de scroll · despedida | 320ms | 0 | `.4,0,.6,1` | no |
| Carrusel · card centrada | 340ms | 0 | `.22,.61,.36,1` | no |
| Carrusel · aterrizaje snap | nativa | 0 | nativa | no |
| Dot · forma | 240ms | 0 | `.22,.61,.36,1` | no |
| Dot · fuego | 160ms | 0 | `linear` | no |
| Red social · ignición | 160ms | `i × 70ms` en la entrada | `.22,.61,.36,1` | no |
| Red social · apagado | 320ms | 0 | `.4,0,.6,1` | no |
| Red social · press | 90ms | 0 | `.4,0,.2,1` | no |
| Ignición · destello de origen | 560ms | 0 | `.22,.61,.36,1` | cooldown 4s |
| Ignición · cascada de los 3 CTA | 760ms c/u · **1160ms total** | 140 + `i × 130ms` | `.32,0,.12,1` / `.22,.61,.36,1` | cooldown 4s |

---

## 12. QA

**Movimiento**
- [ ] Ningún easing con valores Y fuera de `[0,1]`. `grep -nE 'cubic-bezier\([^)]*-' css/` → 0 resultados.
- [ ] `grep -nE 'transition:.*(box-shadow|width|height|top|left|margin|background-position)' css/` → 0 resultados.
- [ ] Ninguna `@keyframes` en bucle toca otra cosa que `transform` u `opacity`.
- [ ] La palabra en degradado barre **una** vez, no en bucle.

**Rendimiento (Chrome DevTools, CPU throttling 4×, Performance panel)**
- [ ] Scroll de toda la página: ningún frame >16.7ms; barra de "Rendering" verde.
- [ ] Arrastre del carrusel: ningún `Recalculate Style` ni `Layout` dentro del gesto.
- [ ] Layers panel en reposo con el hero visible: ≤ 9 capas. Durante la ignición: ≤ 13.
- [ ] "Paint flashing" activo: la respiración del glow **no** repinta nada.
- [ ] Ningún `will-change` en las cards del carrusel.

**Táctil (dispositivo real, no emulador)**
- [ ] El CTA responde visiblemente antes de 100ms desde el contacto del dedo.
- [ ] Tras tocar un CTA y volver a la página, **ningún** botón se queda encendido
      (verifica que el guard `@media (hover: hover)` está en su sitio).
- [ ] Sin rectángulo gris de tap highlight en CTA, redes, dots ni la foto.
- [ ] Swipe horizontal en el carrusel no dispara el back-swipe del navegador.
- [ ] Arrastrar una card **no** abre su enlace; tocarla sin arrastrar **sí**.

**Accesibilidad**
- [ ] `Tab` recorre: foto (ignición) → 3 CTA → track del carrusel → dot activo →
      enlaces de las cards → redes → footer. Anillo de foco visible siempre.
- [ ] Flechas ←/→ mueven el carrusel; `Home`/`End` a los extremos.
- [ ] Un solo tab stop en el grupo de dots (`tabIndex` −1 en los inactivos).
- [ ] Con `prefers-reduced-motion: reduce` forzado: nada se mueve, todo es legible, el
      CTA sigue reaccionando al hover/press, el dot activo se distingue.
- [ ] Contraste del texto del hero medido en el frame más luminoso del glow (§4.4).
- [ ] Contraste del texto sobre el degradado de fuego del CTA ≥ 4.5:1 en el punto más
      claro del degradado caliente (`#FFF3D0`) — es el peor caso, y ocurre en hover.
- [ ] Dianas táctiles ≥ 24×24px (dots incluidos).

**Sin JS / degradado**
- [ ] Con JS desactivado: la página se ve completa, nada oculto, enlaces funcionando.
- [ ] Con webfont bloqueada: la entrada arranca a los 350ms y no salta de métrica.
