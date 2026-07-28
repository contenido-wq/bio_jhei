# Rediseño de diferenciación — Link in bio · Jhei Trujillo

**Fecha:** 2026-07-28
**Estado:** aprobado, pendiente de plan de implementación
**Sustituye parcialmente a:** `2026-07-28-link-in-bio-jhei-design.md`

---

## 1 · Problema

La página actual funciona, es accesible y es rápida, pero **es la arquitectura de
Jhonny Lubo repintada de naranja**. Sección por sección coincide con
`docs/brand/ref-layout-hero.png` y `ref-layout-bio.png`:

| Referente (Lubo) | Página actual |
|---|---|
| Avatar circular centrado | Avatar circular centrado |
| Nombre en mayúscula sostenida | Nombre en mayúscula sostenida |
| Botones apilados a ancho completo | Tres filas apiladas a ancho completo |
| Carrusel de retratos verticales B/N con marca al pie + dots | Idéntico |
| "Expertos con los que he tenido la oportunidad de colaborar" | "Marcas y creadores con los que he trabajado" |
| Bio centrada + 4 redes en círculo | Bio centrada + 3 redes en círculo |
| Footer de una línea | Footer de una línea |

El propio `docs/brand/aivi-brand-extract.md` lo declara como intención:
*"Se replica su **arquitectura y ritmo**, no su color"*. **Esa premisa queda
anulada por este documento.** El referente sirvió para entender qué bloques
necesita un link-in-bio; no para definir cómo se ven.

Segundo problema, independiente: la **mayúscula sostenida**. Hay cinco
`text-transform: uppercase` en `css/styles.css` (líneas 428, 447, 653, 825,
1063). La mayúscula condensada es un rasgo de Lubo. En las cinco capturas de
`asistente.aivi.chat` que aportó el cliente, AIVI **no usa mayúscula sostenida
en ningún titular**: resuelve la jerarquía con peso tipográfico y con una frase
clave en degradado naranja.

Tercer problema: los botones. Hoy son vidrio con borde plano de 1px a blanco 12%.
El cliente los describe como "muy sobrios". AIVI usa dos tratamientos —relleno en
degradado con glow, y trazo— y ninguno de los dos está en la página.

---

## 2 · Objetivo

Que la página deje de ser reconocible como derivada del referente y pase a ser
reconocible como **familia de `aivi.chat`**, sin perder ninguna de las
propiedades técnicas ya conseguidas.

### Criterios de éxito

1. Ningún bloque conserva simultáneamente la posición, el eje de alineación y el
   tratamiento del bloque equivalente en el referente.
2. Cero `text-transform: uppercase` fuera de la excepción declarada en §3.
3. Los tres enlaces usan trazo o relleno en degradado; ninguno usa borde plano.
4. Los tres recursos firmantes de AIVI que hoy faltan están presentes: columnas
   de luz vertical, chips-etiqueta y cinta de texto en bucle.
5. No se degrada ninguna garantía existente: contraste, foco, movimiento
   reducido, colores forzados, cero peticiones a terceros.

### Fuera de alcance (YAGNI)

- Cambiar la paleta, la tipografía o la arquitectura de `tokens.css`.
- Añadir dependencias, build o módulos ES.
- Reescribir el copy de la bio.
- Modo claro.

---

## 3 · Sistema tipográfico

### 3.1 · Fin de la mayúscula sostenida

Se eliminan los cinco `text-transform: uppercase` actuales:

| Línea | Selector | Pasa a |
|---|---|---|
| 428 | `.hero__name` | Caja baja, peso 900 |
| 447 | `.hero__tagline` | Desaparece: lo sustituye el chip (§3.2) |
| 653 | `.collabs__title` | Caja baja, peso 800 |
| 825 | `.collab__brand` | Caja baja, peso 700 |
| 1063 | `.foot__claim` / `.foot__legal` | Caja baja, peso 500 |

**Única excepción permitida:** micro-insignias por debajo de 11px. En la página
eso significa exclusivamente `.hero__status` ("Disponible"). Es el mismo criterio
que AIVI aplica a `MÁS POPULAR` y `SOLO LATAM` en su bloque de precios.

Esta excepción se documenta como comentario en `styles.css` junto a la regla, para
que no se reintroduzca la mayúscula por descuido en otro sitio.

### 3.2 · Chips-etiqueta

Componente nuevo `.chip`, que ocupa el lugar comunicativo que tenían las líneas
en mayúscula. Equivale a `Tu agencia de bolsillo` / `Planes AIVI` / `FAQ` en
`aivi.chat`.

- Píldora (`--r-full`), fondo `--surface-glass`, borde `--border-soft`,
  `box-shadow: var(--sh-glass)`.
- Texto en caja baja, `--fs-small`, `--fw-medium`, tracking `--ls-chip` (0.01em).
- Color `--text-secondary`, con un punto dorado de 5px como prefijo.
- Alineado a la izquierda en hero, enlaces y colaboraciones; nunca centrado, para
  reforzar el eje asimétrico.

Chips previstos: `Viralidad · Contenido · IA aplicada` (hero), `Empieza por aquí`
(enlaces), `Colaboraciones` (cinta), `Sobre mí` (bio).

### 3.3 · Frase clave en degradado

Se mantiene `.fire-text` tal cual está, incluido su `@supports` de reserva y su
corrección de descendentes en Safari. Se aplica a una frase por titular, nunca a
un titular entero, y solo por encima de 26px (regla ya vigente).

---

## 4 · Botones

### 4.1 · Trazo en degradado — construcción

`border-image` queda **descartado**: no respeta `border-radius`, que es
justamente lo que necesitan las píldoras. La construcción es un pseudo-elemento
enmascarado:

```css
.row::before {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: inherit;
  padding: var(--sw-stroke);          /* 1.5px */
  background-image: var(--grad-stroke);
  -webkit-mask: linear-gradient(#000 0 0) content-box,
                linear-gradient(#000 0 0);
  -webkit-mask-composite: xor;
          mask-composite: exclude;
  pointer-events: none;
}
```

El estado caliente es un **segundo** pseudo (`::after`) idéntico pero con
`--grad-stroke-hot`, en `opacity: 0`, que sube a 1 en `:hover` y
`:focus-visible`. Solo se anima opacidad: es lo único que el compositor resuelve
sin repintar el trazo en cada frame.

**Reserva obligatoria.** Si el navegador no soporta la composición de máscara, el
trazo cae a un borde plano dorado, que es lo que la página ya tiene hoy:

```css
@supports not ((mask-composite: exclude) or (-webkit-mask-composite: xor)) {
  .row::before, .row::after { display: none; }
  .row { border: 1px solid var(--border-gold); }
}
```

### 4.2 · Jerarquía de los tres enlaces

| # | Enlace | Tratamiento |
|---|---|---|
| 01 | Talleres con IA | **Relleno** `--grad-fire`, texto en negro, glow `--sh-fire` |
| 02 | Conoce AIVI | **Trazo** en degradado sobre vidrio oscuro |
| 03 | Escríbeme | **Trazo** en degradado sobre vidrio oscuro |

La clase `row--primary` deja de significar "borde dorado + glow" y pasa a
significar "relleno". Sigue siendo movible a otra fila y sigue debiendo llevarla
una sola.

### 4.3 · Contraste sobre el relleno

El texto sobre el degradado de fuego va en **negro**, nunca en blanco: blanco
sobre `#FFC252` da 1.54:1. El token `--text-on-fire` (= `--ink`) ya existe y ya
está justificado en `tokens.css`.

Para el subtítulo de la fila (`.row__note`) hace falta un tono más suave sin
perder AA. Se añade:

```css
--text-on-fire-soft: rgb(var(--rgb-ink) / 84%);
```

Medido en el punto peor del degradado (el extremo rojo `#FF413B`, donde arranca):
**4.67:1**. Cumple AA para texto normal. Este valor **debe volver a medirse en
implementación**; si el degradado cambia de ángulo o de stops, se recalcula antes
de dar el trabajo por cerrado.

La baldosa del icono dentro de la fila rellena invierte: fondo
`rgb(var(--rgb-ink) / 12%)`, borde `rgb(var(--rgb-ink) / 22%)`, icono en
`--ink`. La baldosa cálida actual sobre naranja sería invisible.

### 4.4 · Alcance del trazo

El mismo trazo se hereda, con menor intensidad, en la tarjeta del retrato del
hero, en las cards de colaboración y en los círculos de redes. Es lo que
convierte el efecto en un sistema en vez de en un adorno de un componente.

---

## 5 · Hero asimétrico

Se rompe el eje centrado, **incluido en móvil**. Un link-in-bio se consume casi
por completo en móvil: si la asimetría solo existe en escritorio, el rediseño no
existe.

### Estructura

```
[chip] Viralidad · Contenido · IA aplicada

Jhei                         ┌──────────┐
Trujillo                     │          │
─────────                    │ retrato  │
Hago que te vean             │   4:5    │
y que te recuerden.          └──────────┘
```

- **Alineación:** izquierda en todos los tamaños. Nada centrado en el hero.
- **Nombre:** dos líneas, `--fs-h1`, peso 900, caja baja, tracking `--ls-h1`.
- **Declaración:** `--fs-lead`, con la frase clave en `.fire-text`.
- **Retrato:** tarjeta vertical 4:5, `--r-lg`, trazo en degradado, con máscara de
  fundido en el borde inferior para que se disuelva en el fondo. **Nunca un
  círculo:** el avatar circular es la firma más literal del referente.
- **Insignia "Disponible":** se conserva, anclada a la esquina inferior izquierda
  de la tarjeta, no centrada bajo un círculo.
- **Escritorio (≥60rem):** dos columnas, texto a la izquierda, retrato a la
  derecha.
- **Móvil:** retrato arriba a ~70% del ancho alineado a la izquierda, texto
  debajo. La asimetría se mantiene.

### Retrato: asset

`assets/img/jhei-avatar.png` (480×480) es un placeholder cuadrado. Se genera un
placeholder **vertical 4:5** con `tools/make-placeholders.py` para poder ver el
layout real, y se documenta en el README que el cliente debe sustituirlo por un
retrato 4:5 de medio cuerpo. El `<img>` lleva `width`/`height` correctos y
`object-fit: cover`, así que una foto de proporción ligeramente distinta no rompe
el layout.

El aro cónico (`--grad-ring`) y el halo respirante del avatar circular
desaparecen con él. La animación `halo-breathe` se elimina.

### Enlaces numerados

`01 / 02 / 03` en el margen izquierdo, **fuera** de la píldora, en
`--text-gold`, `--fs-micro`, `font-variant-numeric: tabular-nums`. La sección
`.links` pasa a `grid-template-columns: 2.25rem 1fr`.

Los números son decorativos (`aria-hidden="true"`): el orden ya lo comunica el
DOM, y un lector de pantalla no debe leer "cero uno" antes de cada enlace.

---

## 6 · Fondo: columnas de luz vertical

Es el recurso más reconocible de AIVI ausente hoy en la página: columnas cálidas
que suben desde el borde inferior del lienzo (capturas 2 y 4 del cliente).

**Restricción dura, ya vigente en el archivo:** cero capas GPU nuevas. Las
columnas se añaden como capas adicionales de `background-image` **dentro del
`.backdrop__glow` que ya existe**. No se crea ni un elemento nuevo, no se añade
`will-change` ni `translateZ(0)` a ninguna capa del fondo.

- Cuatro columnas de anchos distintos, con `linear-gradient` vertical de
  naranja/dorado a transparente, situadas con `background-position` en
  porcentajes que no coincidan con el centro de la columna de contenido.
- `background-blend-mode: screen`, coherente con las capas de resplandor que ya
  hay: la luz se suma, no se apila en `normal`.
- La opacidad de `.backdrop__glyphs` baja de 0.5 a ~0.3 para que la luz vertical
  mande sobre los hexágonos.
- El bloque `@media (prefers-reduced-transparency: reduce)` existente cubre estas
  capas sin cambios, porque actúa sobre `.backdrop__glow` completo.

---

## 7 · Cintas en bucle

### 7.1 · Banda de texto

Separador entre los enlaces y las colaboraciones, con filete arriba y abajo:
`Talleres · Guiones · Virales · IA aplicada ·` corriendo en bucle.

- Contenido duplicado en el DOM; **la copia lleva `aria-hidden="true"`** para que
  no se lea dos veces.
- Animación por `transform: translate3d(-50%, 0, 0)` sobre el track, `linear`,
  `infinite`. Nunca `left` ni `margin`.

### 7.2 · Cinta de tarjetas

Sustituye al carrusel. Las 6 fotos corriendo en bucle continuo, sin dots y sin
snap, con el mismo tratamiento monocromo que ya tienen (`grayscale(1)`) y trazo
en degradado en el canto.

### 7.3 · Control de pausa — requisito, no adorno

WCAG 2.2.2 exige un mecanismo de pausa para contenido en movimiento de más de 5
segundos. **El pausado por `:hover` no cumple**: no existe para teclado, táctil ni
tecnología de apoyo. El comentario del bloque 3 de `js/main.js` ya razonaba esto
correctamente y es la razón por la que hoy no hay autoplay.

Por tanto:

- Un **botón visible de pausa/reproducción**, con texto accesible
  (`aria-pressed`), colocado donde estaban los dots.
- Alterna una clase en `<html>` que detiene **las dos** cintas a la vez.
- Además, y como comodidad: pausa al `:hover` y al `:focus-within`.
- Con `prefers-reduced-motion: reduce`, las dos cintas arrancan **detenidas**: la
  banda queda estática y la cinta de tarjetas vuelve a ser un contenedor con
  scroll horizontal normal, navegable con el dedo y con el teclado.
- El estado inicial (en movimiento) se aplica solo si `prefers-reduced-motion` no
  está activo.

### 7.4 · Impacto en `js/main.js`

El bloque 3 (`carousel`, líneas 123–323: dots, geometría cacheada, roving
tabindex, arrastre con puntero, supresión de click) **se elimina completo** y se
sustituye por un bloque `ribbons` mucho más pequeño: solo el botón de pausa y la
duplicación del contenido de las cintas.

Los bloques 1 (arranque), 2 (revelado al scroll) y 4 (año) se conservan sin
cambios, salvo el retiro de las referencias a `.hero__avatar` en el bloque de
movimiento de `styles.css`.

Se retiran también de `styles.css` los estilos `.dot`, `.dot__track` y
`.carousel__dots`, y sus reglas dentro de `prefers-reduced-motion`.

---

## 8 · Copy

| Dónde | Ahora | Pasa a |
|---|---|---|
| Titular colabs | "Marcas y creadores con los que he trabajado" | chip `Colaboraciones` + "Gente y marcas con las que **he construido cosas**" |
| Tagline hero | tres palabras sueltas en mayúscula | chip `Viralidad · Contenido · IA aplicada` + declaración "Hago que te vean **y que te recuerden**" |
| Claim footer | "SÉ VISTO. SÉ RECORDADO." | "Sé visto. Sé recordado." (caja baja) |

El titular actual de colaboraciones es la traducción literal del de Lubo
("Expertos con los que he tenido la oportunidad de colaborar") y por eso se
cambia. El resto del copy de la bio no se toca.

Los marcadores `data-todo` y la clase `.tbd` se conservan tal cual: son
deliberados y el cliente los localiza de un vistazo.

---

## 9 · Tokens

### Se añaden a `tokens.css`

```
--grad-stroke        Degradado del trazo en reposo (rojo→naranja→dorado, alpha media)
--grad-stroke-hot    Degradado del trazo encendido (alpha plena + destello)
--sw-stroke          1.5px — grosor del trazo. EXCEPCION documentada: fuera de la escala de 4px
--text-on-fire-soft  rgb(var(--rgb-ink) / 84%) — 4.67:1 en el extremo rojo
--ls-chip            0.01em
--d-ribbon-text      Duración del bucle de la banda de texto
--d-ribbon-cards     Duración del bucle de la cinta de tarjetas
```

### Se retiran

`--grad-ring` (aro del avatar circular), `--d-breath-b` si no queda ninguna otra
respiración en la página.

### No se tocan

Los cinco colores de marca, la escala tipográfica, la escala de espaciado, los
radios, las sombras, las curvas de easing, los z-index y el sistema de foco.
`tokens.css` sigue siendo la fuente única de valores literales y `styles.css`
sigue sin contener ni un hex ni un px de espaciado.

---

## 10 · Garantías que no se degradan

Estas ya están conseguidas y el rediseño **no** puede romperlas. Se verifican
antes de dar el trabajo por terminado:

1. **Contraste.** Todo texto ≥4.5:1; el trazo, cuando es la única señal de que
   algo es un control, ≥3:1 (WCAG 1.4.11). El punto crítico nuevo es §4.3.
2. **Foco.** El anillo de dos tonos (`--focus-shadow`) se aplica a los elementos
   nuevos: chips si son interactivos, botón de pausa, cinta de tarjetas.
3. **`prefers-reduced-motion`.** Las dos cintas detenidas, sin traslaciones ni
   escalas; se conservan las transiciones de color y opacidad, que son feedback y
   no movimiento.
4. **`prefers-contrast: more`.** El trazo en degradado cae a borde sólido de alto
   contraste; los glows se apagan.
5. **`forced-colors: active`.** El fondo desaparece y los controles recuperan
   `border: 1px solid ButtonText`. Los pseudo-elementos de trazo se ocultan: en
   HCM no se pintan degradados.
6. **Sin JS la página se ve completa.** La clase `motion` la pone el script inline
   del `<head>`; las cintas sin JS quedan estáticas y legibles, no vacías.
7. **Cero peticiones a terceros.** Fuentes auto-hospedadas, fondo en CSS puro,
   sin imágenes nuevas más allá del placeholder del retrato.
8. **Sin capas GPU nuevas en el fondo** (§6).

---

## 11 · Riesgos

| Riesgo | Mitigación |
|---|---|
| `mask-composite` sin soporte | `@supports` de reserva a borde plano (§4.1) |
| El trazo de 1.5px se pierde en pantallas de baja densidad | Se verifica a 1× además de a 2× antes de cerrar |
| Dos cintas en bucle + fondo fijo = jank en móvil de gama baja | Solo `transform` en las cintas; cero capas nuevas en el fondo; se mide en el navegador, no se supone |
| El retrato definitivo llega con otra proporción | `object-fit: cover` + `object-position` ajustable en un solo token |
| `--text-on-fire-soft` falla si cambian los stops del degradado | Recalcular obligatorio en implementación (§4.3) |

---

## 12 · Nota de control de versiones

El proyecto **no es un repositorio git** (`git rev-parse` falla en
`/Users/diegojheilab/Proyecto/link_in_bio`). Este documento no se puede commitear.
Si se quiere historial del rediseño, hay que ejecutar `git init` primero.

---

## 13 · Actualización pendiente de la documentación

Al cerrar la implementación hay que corregir `docs/brand/aivi-brand-extract.md`,
cuyo último párrafo todavía instruye replicar la arquitectura del referente. Debe
pasar a decir que los `ref-layout-*` son material histórico y que la arquitectura
la define este spec.

También quedan desactualizados y hay que revisarlos:
`docs/design/ui-component-spec.md`, `docs/design/motion-spec.md`,
`docs/design/css-architecture.md` y `docs/design/copy.md`.
