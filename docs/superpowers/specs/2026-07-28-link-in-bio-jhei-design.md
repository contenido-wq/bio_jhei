# Link in bio — Jhei Trujillo

**Fecha:** 2026-07-28
**Estado:** aprobado por el cliente, en implementación

## Propósito

Una página única que concentra el tráfico de las redes de Jhei Trujillo (TikTok,
Instagram, YouTube) y lo reparte hacia tres destinos de negocio. Jhei es experto en
Viralidad, Creación de Contenido e Inteligencia Artificial.

El éxito se mide en una sola cosa: **el porcentaje de visitantes que hace clic en uno
de los tres CTAs.** Todo lo demás en la página existe para hacer creíble ese clic.

## Contexto y restricciones

- Replica la **arquitectura** del referente de Jhonny Lubo (`docs/brand/ref-layout-*.png`),
  no su color: el morado se sustituye por la paleta de fuego de AIVI.
- Hereda la línea gráfica de AIVI documentada en `docs/brand/aivi-brand-extract.md`.
- **No se usa el logo ni el isotipo de AIVI.** Solo paleta, tipografía y lenguaje visual.
- El tráfico es casi enteramente móvil. Mobile-first no es una preferencia, es el caso base.
- Las imágenes arrancan como placeholders con rutas finales ya definidas, para que el
  cliente sustituya archivos sin tocar código.
- La bio y el copy los redacta el proyecto; el cliente aporta las URLs y las métricas reales.

## Sistema visual

Tokens derivados de la guía de AIVI:

| Token | Valor |
|---|---|
| `--ink` | `#101010` |
| `--paper` | `#FAFAFA` |
| `--fire-red` | `#FF413B` |
| `--fire-orange` | `#FE803F` |
| `--fire-gold` | `#FFC252` |
| `--gradient-fire` | `135deg, red → orange → gold` |

Tipografía **Hanken Grotesk** variable (100–900), auto-hospedada en
`assets/fonts/` — 34 KB para el subconjunto latino completo, con `font-display: swap`
y pila de reserva del sistema. No depende de ningún CDN.

Titulares en peso 900, mayúsculas, tracking negativo. Cuerpo en peso 300.
Escala fluida con `clamp()` de 360px a 1440px, sin media queries para tamaño de texto.

El fondo reproduce las piezas de AIVI con CSS puro, en capas: base `#101010`, gradiente
radial cálido desde la esquina superior derecha, haces de luz diagonales con núcleo casi
blanco, chevrones de esquinas redondeadas a gran escala y baja opacidad, y grano fino en
SVG. Sin imágenes raster de fondo.

Las superficies son paneles tipo vidrio: apenas más claras que el fondo, borde translúcido
de 1px. Nunca cajas grises opacas.

## Arquitectura

```
link_in_bio/
├── index.html          documento único, semántico
├── css/tokens.css      única fuente de verdad del sistema visual
├── css/styles.css      layout y componentes, consume tokens
├── js/main.js          carrusel, revelado al scroll, scroll suave
├── assets/fonts/       Hanken Grotesk variable, auto-hospedada
├── assets/img/         placeholders con las rutas finales
├── docs/brand/         extracto de la línea gráfica AIVI y referencias
├── docs/design/        especificaciones de los agentes de diseño
└── README.md           dónde cambiar cada link, imagen y color
```

Cada archivo tiene un propósito único y una frontera clara:

- **`tokens.css`** no contiene ni un selector: solo custom properties. Cambiar la marca
  entera es cambiar este archivo.
- **`styles.css`** no contiene ni un valor literal de color ni de espaciado: solo consume
  tokens. Se puede leer sin conocer los valores.
- **`main.js`** se organiza en módulos independientes (carrusel, revelado, scroll), cada
  uno con una única responsabilidad y sin estado compartido. Cada módulo se degrada solo:
  si el JS falla o no carga, la página sigue siendo completamente legible y todos los
  enlaces siguen funcionando.
- **`index.html`** concentra todo el contenido editable. Cambiar un link o un texto nunca
  requiere abrir CSS ni JS.

## Secciones

1. **Hero** — foto recortada de Jhei con glow naranja y halo de chevrones. `JHEI TRUJILLO`
   en peso 900 mayúsculas. Subtítulo con las tres áreas de expertise. Indicador de scroll.
2. **Los tres CTAs** — botones-tarjeta grandes con degradado de fuego y mockup alternando
   izquierda/derecha: **TALLERES**, **AIVI** (aivi.chat) y **WHATSAPP**. Cada uno con
   microcopy que anticipa qué pasa al hacer clic. En móvil el mockup cede espacio al texto.
3. **Colaboraciones** — carrusel de cards verticales, retrato en blanco y negro con
   degradado de fuego al pie y logo de la marca. Swipe táctil, dots de paginación.
4. **Bio** — avatar con anillo de fuego, handle, tres párrafos en primera persona, e iconos
   de TikTok, Instagram y YouTube en círculos de vidrio.
5. **Footer** — firma.

## Movimiento

La metáfora es fuego y luz: el movimiento se siente como luz que respira y se propaga,
no como elementos que rebotan. Entrada escalonada del hero, revelado al scroll con
IntersectionObserver, y un brillo que recorre los CTAs al hover.

Solo se animan `transform` y `opacity`. Objetivo: 60fps en un móvil de gama media.

## Accesibilidad

- Contraste AA sobre `#101010`. El naranja y el dorado solo en texto grande o en elementos
  no textuales; el cuerpo del texto siempre en `--paper`.
- `prefers-reduced-motion: reduce` desactiva todo movimiento no esencial y deja la página
  perfectamente usable.
- `:focus-visible` visible en todo lo interactivo, con orden de tabulación lógico.
- HTML semántico, un solo `h1`, `aria-label` descriptivo en los iconos de redes.
- Los enlaces externos abren en pestaña nueva con `rel="noopener"`.

## Rendimiento

Cero dependencias externas y cero peticiones a terceros. El JS no bloquea el render.
Las imágenes llevan `width`/`height` explícitos para no provocar saltos de layout, y
`loading="lazy"` en todo lo que está bajo el pliegue.

## Verificación

La implementación se considera terminada cuando:

1. La página se ve correcta a 360px, 768px y 1440px de ancho.
2. Los tres CTAs son alcanzables y activables solo con teclado, con foco visible.
3. Con `prefers-reduced-motion: reduce` activo no hay movimiento y todo sigue legible.
4. Con el JS deshabilitado, el contenido completo sigue visible y los enlaces funcionan.
5. El carrusel responde a swipe táctil y a teclado.
6. Ningún color de texto de cuerpo baja de 4.5:1 de contraste sobre el fondo.
7. No hay ni una petición a un dominio externo.

## Fuera de alcance

Analítica, formularios, backend, CMS, multi-idioma y A/B testing. Si más adelante hacen
falta, el paso natural es migrar a Astro conservando `tokens.css` intacto.

## Revisión: versión sobria con filas de icono

El cliente revisó la primera implementación y pidió dos cambios: menos color y
enlaces con icono en lugar de botones. Aportó como referencia un link in bio
monocromo en negro y dorado con avatar circular y filas de vidrio.

Lo que cambió:

- **El hero.** Fuera el retrato rectangular grande, el halo de chevrones y el
  glow naranja. Entra un **avatar circular** con aro cónico de naranja a dorado,
  una insignia "Disponible" apoyada en su borde inferior, y un filete ornamental
  (línea · rombo · línea) que separa el hero de los enlaces. El nombre baja un
  paso de tamaño: sin el retrato grande, a 92px pesaba más que los enlaces, que
  son lo que convierte.
- **Los enlaces.** Las tarjetas de degradado de fuego pasan a **filas de vidrio
  oscuro**: fondo apenas más claro que la página, borde de 1px, icono de trazo en
  su baldosa cálida a la izquierda, título en caja baja, microcopy en gris y
  flecha a la derecha. Una sola fila lleva `row--primary`, con borde dorado y
  resplandor. Los mockups de dispositivo desaparecen.
- **El fondo.** Fuera el haz de luz diagonal, que era la mayor fuente de color.
  Quedan el resplandor cálido tenue de la esquina superior, la geometría de AIVI
  al 50% de opacidad, la viñeta y el grano.
- **El rojo sale de los acentos grandes.** El aro del avatar y el titular de
  colaboraciones pasan a degradados de naranja a dorado. Con el rojo dentro eran
  lo más saturado de la página. El rojo sobrevive solo en el rombo de 8px del
  filete, el filo de 2px de las cards y la píldora del punto activo.
- **Las fotos de colaboración son monocromas siempre.** Antes revelaban color en
  la card activa; ahora la activa se distingue por brillo, borde y filo.
- **Se retiran el indicador de scroll y la ignición en cascada.** El hero es
  ahora corto y los enlaces se ven casi sin desplazar, así que el indicador
  sobraba. La ignición estaba montada sobre el barrido de luz de los botones de
  degradado, que ya no existen; su nodo, sus tres animaciones y su JS se van con
  ellos. El movimiento permanente de la página queda en un único elemento: la
  respiración del halo del avatar.

Consecuencia medible: el JavaScript baja de 17,7 KB a 12,4 KB, el CSS de 58,5 KB
a 40,7 KB, el total comprimido de 28 KB a 22 KB, y las imágenes de 1 MB a 596 KB
al desaparecer el retrato grande y los tres mockups.

## Decisiones tomadas durante la implementación

Cinco puntos donde la implementación se separó del diseño inicial o de lo que
propusieron las especificaciones de `docs/design/`. Todas están razonadas aquí
para que nadie las revierta por error.

**1 · El texto de los CTA es negro sobre fuego brillante.** Los tres agentes de
diseño detectaron de forma independiente que blanco sobre el degradado de fuego
no pasa AA: 1,60:1 sobre el dorado. Había dos salidas — oscurecer el degradado y
mantener el texto blanco, o mantener el degradado y poner el texto negro. Se
eligió la segunda: mide 5,50:1 en el peor extremo del degradado y, contra una
página casi negra, la tarjeta brillante domina la pantalla, que es exactamente
lo que se le pide a un CTA. También elimina el escrim y los pseudoelementos
espejados que exigía la otra opción.

**2 · Sin autoplay en el carrusel.** La especificación de UI lo pedía a 4500ms.
Se descartó: contenido en movimiento de más de cinco segundos exige un control
de pausa (WCAG 2.2.2) y aquí no aporta nada, porque deslizar, los puntos y las
flechas ya son la navegación completa. Además elimina un temporizador
permanente.

**3 · `overflow-x: clip` va en el elemento raíz.** Las tres especificaciones lo
ponían solo en `body`. Medido en el navegador, la página seguía desplazándose
50px en horizontal en móvil: solo el overflow del elemento raíz propaga al
viewport.

**4 · La palabra clave del subtítulo va en dorado plano, no en degradado.** El
subtítulo mide 11–15px y el degradado de fuego se reserva a titulares de 26px o
más. El dorado plano mide 11,86:1 y mantiene el lenguaje de marca sin el coste
de legibilidad. El degradado sí se usa en el titular de colaboraciones.

**5 · El retrato del hero es un botón que lleva a los enlaces.** El detalle de
deleite propuesto era un botón puramente decorativo que lanzaba un pulso de luz
sobre los tres CTA. Se mantuvo el pulso, pero el botón hace además algo útil
—desplazar la vista a los enlaces— para que su etiqueta sea honesta también
cuando el usuario ha pedido menos movimiento y el pulso no se ejecuta.

## Datos pendientes del cliente

- URL de talleres
- URL de AIVI (se asume `https://aivi.chat`)
- Número de WhatsApp y mensaje pre-cargado
- Handles de TikTok, Instagram y YouTube
- Foto del hero, avatar, mockups de los CTAs y logos de colaboraciones
- Las métricas reales que el copy deja marcadas como pendientes
