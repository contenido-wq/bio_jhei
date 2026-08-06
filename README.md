# Link in bio — Jhei Trujillo

Página única en HTML, CSS y JavaScript planos. Sin build, sin dependencias y sin
ninguna petición a servidores de terceros. Se sube tal cual a cualquier hosting
(Netlify, Vercel, GitHub Pages, cPanel) y funciona.

Línea gráfica heredada de la guía de AIVI, **sin usar el logo ni el isotipo de
AIVI**: su tipografía (Hanken Grotesk) y su lenguaje visual.

**Todo el decorado es neutro.** Filos, resplandores, filetes y flechas van en
grises fríos sobre un negro azulado (`#080b12`, no gris neutro: se midió sobre
la referencia gráfica). El fuego de AIVI sigue declarado en los tokens y sigue
disponible como relleno de fila (`row--fire`), pero no decora nada.

El color aparece en **tres sitios y solo tres**, cada uno con un oficio:

| Color | Dónde | Qué dice |
|---|---|---|
| Teal y verde | Rellenan las dos filas de taller | "Esto es lo que se vende" |
| Azul `#9dbbf7` | Una palabra dentro de un titular | "Este es el concepto de la frase" |
| — | Todo lo demás | Nada: es decorado |

No chocan porque no comparten sitio ni oficio: el azul solo vive dentro de una
frase, los otros dos solo rellenan una fila. Y una señal solo funciona si es
escasa — cuando el naranja estaba repartido por filos, fondos y titulares, los
talleres no destacaban por tener color sino a pesar de que lo tenía todo el
mundo.

**Las etiquetas micro van en monoespaciada y versales** —`IA · VIRALIDAD ·
NEGOCIOS`, `CASOS DE ÉXITO`— con un resplandor que asoma por encima de la
píldora. Es la única excepción a la prohibición de mayúscula sostenida de la
página, y está vigilada: ver "Versales" más abajo.

**Los titulares bajaron de peso 900 a 600.** Es el cambio que más separaba
esta página de una premium: el negro de 900 lee como cartel de oferta. A 600
el titular pesa igual en la jerarquía y cambia de registro entero.

---

## Cómo verla en local

```bash
cd link_in_bio
python3 -m http.server 8777
# abre http://127.0.0.1:8777
```

Ábrela con un servidor, no con doble clic: la tipografía va auto-hospedada y el
navegador bloquea las fuentes cargadas desde `file://`.

---

## Lo único que tienes que cambiar

Todo el contenido editable está en `index.html`. Cualquier sitio que quede
pendiente lleva el atributo `data-todo`, así que los localizas todos de golpe:

```bash
grep -n 'data-todo' index.html
```

Hoy no devuelve nada: los cuatro enlaces y las tres redes ya apuntan a su
destino real.

### 1 · Los cuatro enlaces

Todos apuntan ya a su destino real. No queda ningún `data-todo`.

| Fila | Destino |
|---|---|
| **Taller: Vuélvete VIRAL y llena tu agenda** | `wa.me` con el mensaje de reserva de cupo precargado |
| **Taller: Contenido que V3NDE con IA** | `https://jheitrujillo.com/pv-bio-ig/` |
| **Conoce AIVI** | `https://aivinetwork.com` |
| **¿Dudas o soporte?** | `https://go.aivi.chat/soporte-bio` |

El número de WhatsApp va con código de país y sin `+` ni espacios, y el mensaje
precargado va URL-encoded (`%20` por espacio, `%C3%A9` por `é`). Si lo editas a
mano y dejas un espacio o una tilde sin codificar, WhatsApp corta el texto en
ese punto sin avisar.

**Para añadir una quinta fila**, duplica un `<a class="row stroke">` entero.
Solo hay que ajustar una cosa más: los retardos de entrada están en
`css/styles.css`, buscando `.row:nth-of-type(`. Añade un bloque más siguiendo
el patrón (+70 ms respecto al anterior).

### 2 · Qué filas van rellenas

Hay dos tratamientos y la diferencia es deliberada:

**Las cuatro filas son la misma pieza**: vidrio oscuro con trazo en degradado
(`stroke`). Lo que separa a las de taller es el color de ese trazo.

| Clases | Qué cambia | Quién la lleva |
|---|---|---|
| `row stroke row--aesthetic` | Trazo teal, tinte, glifo y halo | Taller VIRAL |
| `row stroke row--sales` | Trazo verde, tinte, glifo y halo | Taller V3NDE |
| `row stroke` | Trazo de plata | AIVI, soporte |

El modificador de color **no declara ni una propiedad**: solo reapunta seis
tokens que `.row` y `.stroke` ya consumían. Por eso una fila de taller y una de
plata se comportan idéntico en hover, foco y pulsación sin repetir una sola
regla, y añadir un tercer color son seis líneas.

**Hubo una versión que rellenaba las dos filas de taller con color a plena
opacidad y texto negro.** Se descartó, y conviene saber por qué antes de
proponerlo otra vez: dos bloques saturados seguidos vuelven a tapar el resto de
la página, que es exactamente el problema que tenía el naranja al principio. La
referencia gráfica que fija el registro de esta página no llena de color
ninguna de sus tarjetas — su color aparece en un filo, un punto de estado o una
palabra suelta, nunca en un fondo.

**El color entra en la fila por cuatro sitios, todos periféricos:** el trazo,
un tinte de superficie del 9% al 2%, el glifo del icono y el halo. El texto se
queda blanco. Si algún día uno de los cuatro empieza a pesar más que el texto,
es que el tinte subió demasiado.

**En estas dos filas el trazo es la señal principal**, no un adorno: por eso
sus tres paradas se miden con el mismo mínimo de 3:1 que las de plata y ninguna
tiene permiso para bajar. `check-contrast.py` mide las nueve, una por una.

### 3 · Los iconos

Cada fila lleva su icono como SVG dentro del HTML, así que no hay archivos que
gestionar ni peticiones extra. Son de trazo, 24×24, con juntas redondeadas para
que hablen el mismo idioma que la geometría de AIVI.

| Fila | Icono | Color del glifo |
|---|---|---|
| Taller VIRAL | Birrete de graduación | Teal, como su trazo |
| Taller V3NDE | Pizarra con curva al alza | Verde, como su trazo |
| AIVI | Chispa doble (IA) | Plata |
| Soporte | Auriculares con micrófono | Plata |

**Los glifos van sueltos, sin baldosa.** Tuvieron un cuadrado redondeado de
52 px con relleno y filo; se retiró porque un icono metido en su cajita es la
convención de un menú de aplicaciones, no la de una página de producto. Dentro
de una fila rellena el glifo pasa a negro solo, lo hace
`.row--fill .row__icon`.

El `.row__icon` conserva un ancho fijo (30 px en móvil, 34 en escritorio)
aunque ya no dibuje nada: es lo que mantiene los cuatro títulos arrancando en
la misma vertical. Sin él cada glifo mediría lo suyo y la columna de texto
bailaría de fila en fila.

Los dos talleres llevan iconos de educación **distintos** a propósito: dos
birretes seguidos se leen como el mismo taller repetido, y lo que cambia entre
ellos es el tema, no el formato.

Para cambiar uno, sustituye el contenido de su `<svg>` por otro path. Mantén el
`viewBox="0 0 24 24"`, `fill="none"` y `stroke="currentColor"`: el color y el
tamaño los pone el CSS, así que el icono nuevo hereda todo automáticamente.

### 3 bis · Los colores de acento

Son la **única excepción** a la regla de "cinco colores de marca y ni uno más", y
existen por una sola razón: hay dos talleres distintos en la lista y con el
mismo tratamiento se leían como el mismo producto duplicado.

Cada acento tiene cuatro tonos en `css/tokens.css`. `-deep` y `-lit` son
oscurecimiento y aclarado del mismo hue, no colores nuevos — la misma lógica
que `--fire-800` y `--fire-glare` tienen con el fuego:

```css
--accent-aesthetic-deep:  #3da79e;   /* parada oscura del relleno */
--accent-aesthetic:       #4fb8ae;   /* el color */
--accent-aesthetic-lit:   #6ac8bf;   /* parada clara */
--accent-aesthetic-glare: #85d5cd;   /* remate del estado hover */
--rgb-aesthetic: 79 184 174;         /* componentes, para las sombras */
```

**Van apagados a propósito.** La primera versión usaba el hue casi a
saturación plena (teal al 70%, verde al 98%) y leía como neón: el color puro y
brillante es señal de barato, no de caro. Al 42% y 40% cada taller se sigue
identificando de un vistazo y deja de gritar. Si algún día los subes de
saturación, ese es el efecto que vuelve.

Bajar la saturación manteniendo la luz **sube** el contraste, no lo baja: el
peor punto pasó de 4,75:1 a 4,95:1. Desaturar hacia el gris a la misma
luminosidad nunca oscurece; lo que oscurece es bajar la luz.

**Si cambias un tono, `--rgb-*` tiene que seguir cuadrando con el hex**: son el
mismo color escrito de dos formas y nada los sincroniza solos.

**La parada `-deep` es la que manda en accesibilidad.** Es el punto de menor
contraste de todo el relleno y por tanto la que decide si el texto negro se
lee. Ya no hay que calcularlo a mano: `tools/check-contrast.py` mide las seis
parejas nuevas y falla si alguna baja de 4,5:1. Los valores actuales van de
4,95:1 (subtítulo sobre el verde profundo, el más justo) a 12,76:1.

### 4 · Las redes

Tres enlaces al final del HTML: TikTok, Instagram y YouTube. Cambia el `href` y
deja el `aria-label` como está — es lo que lee un lector de pantalla.

### 5 · Los datos de la bio

Cuatro marcadores, señalados en la página con un borde a rayas para que no se te
escape ninguno:

| Marcador | Qué es |
|---|---|
| `USUARIO` | Tu handle principal, sin la `@` |
| `AÑOS` | Años publicando en internet |
| `VISTAS` | Vistas acumuladas, redondeadas hacia abajo ("más de 50 millones de") |
| `ALUMNOS` | Personas formadas en talleres y programas |

Cada uno está envuelto en `<span class="tbd">`. Sustituye el texto y quita el
`<span>` entero, incluido el `class="tbd"`.

**Si no tienes un dato, no lo aproximes: reescribe la frase sin el número.**
En `docs/design/copy.md` está una versión del segundo párrafo ya redactada sin
cifras, lista para pegar.

Una cosa más para decidir antes de publicar: el texto de WhatsApp dice *"Te
contesto yo por WhatsApp, no un bot"*. Solo publícalo si de verdad respondes en
persona. Si hay asistente o automatización, cámbialo por *"Cuéntame tu idea por
WhatsApp"*.

### 7 · Las colaboraciones

Nueve cards en una cinta que se recorre en horizontal a mano —rueda, dedo o
flechas—, sin movimiento automático. Cada una lleva la portada arriba y, debajo,
las visualizaciones y el nicho.

Para cambiar una: sustituye el archivo `assets/img/collab-NN.jpg` y edita el
número y el nicho en su `<li class="collab">`. Para añadir o quitar, duplica o
borra un `<li>` entero dentro de `.ribbon__set`.

El `alt` de las portadas va **vacío a propósito**: la imagen ilustra y el dato
que importa ya está en texto al lado. Un alt descriptivo haría que un lector de
pantalla repitiera lo mismo dos veces en cada card.

Las cifras están escritas a mano en el HTML y no se actualizan solas. Redondea a
lo que te sirva a medio plazo, no al número exacto de hoy.

**Pide permiso de uso de imagen a cada persona o marca antes de publicarla.**

---

## Las imágenes

Todas son **placeholders generados en la línea gráfica de AIVI**. Cada una está
en la ruta y el tamaño definitivos, así que basta con sobrescribir el archivo: no
hay que tocar el HTML.

| Archivo | Tamaño | Notas |
|---|---|---|
| `assets/img/jhei-hero.jpg` | 1920 × 1072 (16:9) | **Hero de ESCRITORIO.** Banner apaisado, sujeto a la derecha y tercio izquierdo oscuro. Ver "Imagen del hero" más abajo. |
| `assets/img/jhei-hero-mobile.jpg` | 1200 × 1000 (6:5) | **Hero de MÓVIL.** Sujeto centrado. Es otra foto, no la misma recortada. |
| `assets/img/jhei-avatar.png` | 480 × 480 | Solo se usa como icono de acceso directo (`apple-touch-icon`), no aparece dentro de la página. Cuadrada, rostro centrado. |
| `assets/img/collab-01…09.jpg` | 3:4, mínimo 480 px de ancho | Portadas de los videos, en color. Recórtalas SIN el contador de TikTok ni la etiqueta "Anclado": esos datos los dibuja la página. |
| `assets/img/og-image.png` | 1200 × 630 | Lo que se ve al compartir el enlace en redes. |
| `assets/img/favicon.svg` | — | El icono de la pestaña. |

No hay mockups de dispositivo ni una foto de perfil en círculo en la página: la tarjeta del
hero es rectangular a propósito (ver más abajo) y las redes son círculos de
icono, no fotos.

Para regenerar los placeholders (por ejemplo si cambias la paleta):

```bash
python3 tools/make-placeholders.py
```

---

## Móvil: todo centrado

En móvil la página es una sola columna centrada — hero, botones y bio. En
escritorio vuelve a alinearse a la izquierda. No es una incoherencia: son dos
composiciones distintas y cada una se alinea con lo que tiene al lado. En una
pantalla estrecha no hay nada a la derecha del bloque y el eje central es el
único que existe; en escritorio el texto del hero se superpone al tercio
izquierdo del banner y centrarlo lo pondría encima del sujeto.

Los cortes no son todos iguales, y cada componente cambia cuando su propio
contenido lo pide:

| Bloque | Centrado hasta | Por qué ahí |
|---|---|---|
| Hero y botones | `60rem` | Es donde el hero pasa a banner con texto superpuesto |
| Bio | `56rem` | Es donde la bio pasa a dos columnas |

**Los tres bloques comparten eje**: hero, botones y bio arrancan en el mismo
píxel. El hero iba a sangre y se le puso `margin-inline` para meterlo en fila
con el resto; con todo centrado, una tarjeta redondeada tocando el filo de la
pantalla se lee como un error y no como una decisión.

El párrafo de la bio centrado se lee algo peor que alineado a la izquierda —el
ojo pierde el arranque de cada línea— pero en una columna estrecha la pérdida
es pequeña. Si algún día pesa más la lectura que la simetría, se cambia una
línea: `text-align` en `.bio`.

---

## Imagen del hero

**Son dos fotos distintas, no la misma recortada por CSS**, y se sirven con
`<picture>`. Ningún `object-position` convierte un banner con el sujeto a la
derecha en un retrato con el sujeto centrado.

`assets/img/jhei-hero.jpg` es el de **escritorio**: banner apaisado de
1920 × 1072 px (16:9), 143 KB, con el sujeto en el tercio derecho y el
izquierdo en negro, que es donde se superpone el texto.

`assets/img/jhei-hero-mobile.jpg` es el de **móvil**: 1200 × 1000 px (6:5),
121 KB, sujeto centrado y sin texto encima. 1200 px de ancho cubre un móvil de
390 px a densidad 3x con margen.

**El 6:5 tiene un motivo por arriba y otro por abajo, y los dos son duros.**

Por arriba: es lo más alta que puede ser sin echar el primer botón fuera de
pantalla. Empezó en 1:1, subió a 4:5 buscando presencia y ahí medía 436 px en
un móvil de 390 — el primer botón caía por debajo del pliegue. En un link in
bio ese es el error caro: la foto es decoración y los botones son la página.
A 6:5 mide 291 px y el primer botón entra entero.

Por abajo: es lo más corta que puede ser sin partir la composición. Los iconos
flotantes de abajo —YouTube a la izquierda, el bocadillo a la derecha—
terminan sobre y≈1400 de la foto original. Cortando en 1300 quedaban partidos
por la mitad.

Si cambias la foto, el recorte se rehace con esos dos límites, no a ojo:
**baja hasta que el primer botón entre, y para en cuanto empiece a cortar algo.**

El `<img>` lleva la de móvil como valor por defecto y es el `<source>` quien
pide la de escritorio. Al revés, un navegador sin soporte de `<picture>`
descargaría en un teléfono el banner de 1920 px, que además está mal
encuadrado para esa pantalla. Las dos se precargan con su `media`, la misma
condición que su `<source>`: sin ese atributo el navegador precarga siempre la
misma y el teléfono se baja las dos.

**En escritorio** va como una tarjeta de 1120px centrada, con esquinas
redondeadas y el mismo trazo en degradado que los botones — a sangre completa
era el único elemento de la página con bordes duros y terminaba en un corte
recto que no conectaba con nada. El texto va encima, sobre un velo en degradado
que garantiza el contraste. **En móvil no se
superpone nada**: el texto va arriba y la imagen debajo, recortada en cuadrado
sobre el sujeto — a 390px de ancho, un 16:9 dejaría la cara en unos 90px.

Para cambiarla, sobrescribe el archivo con otro apaisado y no hay que tocar el
HTML. Dos cosas que sí hay que revisar si la nueva foto es muy distinta:

- **El encuadre.** `object-position` en la regla `.hero__media img` de
  `css/styles.css` — hay un valor para móvil y otro para escritorio.
- **El contraste del texto.** El velo (`.hero__scrim`) está calibrado para
  ESTA foto: se midió componiendo sus píxeles reales con el degradado, y da
  12.71:1 en el nombre, 10.53:1 en la frase, 13.69:1 en el chip y 7.33:1 en la
  palabra clave con brillo. Este último bajó desde los 8.55:1 que daba en
  dorado: la plata es un punto más oscura que el oro. Sigue muy por encima del
  mínimo, y no se remidió sobre la foto — se derivó de la luminancia de fondo
  que ya daba la medición original, que es el mismo fondo. Con una
  foto más clara en la mitad izquierda esos números bajan y hay que reforzar el
  velo. Es la única parte de la página cuyo contraste depende de un archivo de
  imagen y no solo de los tokens, así que `tools/check-contrast.py` no puede
  vigilarlo.

**Ancho de render objetivo:** es la imagen precargada con mayor prioridad
(`fetchpriority="high"`, candidata a LCP). 1920px cubre un escritorio de
1470px con margen; no conviene subir mucho de ahí.

---

## Estructura

```
index.html            todo el contenido editable
css/tokens.css        color, tipografía, espaciado, movimiento — la marca entera
css/styles.css        layout y componentes; solo consume tokens
js/main.js            revelado al scroll, cinta en bucle, año del footer
assets/fonts/         Hanken Grotesk variable 100–900, auto-hospedada (56 KB)
assets/img/           imágenes, favicon
tools/                generador de placeholders y comprobaciones estáticas de diseño y contraste
docs/brand/           la línea gráfica de AIVI extraída del PDF, con referencias
docs/design/          especificaciones de UI, arquitectura CSS, movimiento y copy
docs/superpowers/     el documento de diseño aprobado
```

**Para cambiar un color de toda la página se toca un solo archivo:**
`css/tokens.css`. `styles.css` no contiene ni un hex ni un valor de espaciado
suelto.

---

## Versales

La página prohibía la mayúscula sostenida sin excepciones, y `check-rules.py`
lo vigilaba. La regla existía por una razón real: hubo una lista blanca para
una insignia del hero, la insignia se retiró, la excepción sobrevivió apuntando
a un selector que ya no existía, y ese permiso muerto dejó pasar una regresión.

Al adoptar el lenguaje de la referencia gráfica —cuyas etiquetas son todas
monoespaciadas y en versales— la regla se **acotó, no se retiró**.

La lección de aquel bug no fue "las versales son malas", fue "un permiso que
nombra un selector deja de proteger en cuanto el selector cambia de nombre".
Así que el permiso nuevo **no nombra selectores**: describe la forma
tipográfica en la que las versales hacen un trabajo real, y exige las tres
condiciones a la vez y en el mismo bloque:

```css
font-family: var(--font-mono);      /* monoespaciada        */
font-size: var(--fs-micro);         /* el escalón más chico */
letter-spacing: var(--ls-widest);   /* o --ls-wider         */
text-transform: uppercase;
```

Un titular en versales no puede colarse porque no puede cumplirlas. En cuanto
alguien sube el cuerpo o quita el tracking, el bloque falla y el script dice
exactamente cuál de las tres falta.

Las tres juntas no son celo: cuerpo pequeño sin tracking da un amasijo
ilegible, tracking sin monoespaciada no cambia de registro, y monoespaciada a
cuerpo grande es justo el titular en versales que la regla existe para impedir.

La monoespaciada es la **del sistema** (`ui-monospace`), no auto-hospedada: son
cuatro etiquetas de once píxeles y bajar un segundo archivo de fuente por ellas
costaría más que todo el CSS de la página.

---

## Verificación

Dos scripts, solo librería estándar de Python, sin dependencias que instalar.
Córrelos después de tocar `css/styles.css` o `css/tokens.css`, y siempre antes
de publicar.

```bash
python3 tools/check-rules.py
python3 tools/check-contrast.py
```

**`check-rules.py`** garantiza cinco reglas del sistema de diseño: versales
solo en la forma de etiqueta micro (ver arriba), cero color de marca escrito
como hex literal, cero capa GPU propia en el fondo (`will-change` o
`translateZ(0)` dentro de `.backdrop`), que si se usa `mask-composite` existe
su bloque `@supports not (...)` de reserva, y **comentarios CSS bien
cerrados**. Sale con código 1 y detalla cada línea si algo falla.

La última es la más aburrida y la que más ha pagado. Un `*/` de más deja la
prosa suelta en la hoja, y CSS no avisa: descarta en silencio hasta el
siguiente punto y coma, así que **el token que viene justo después se queda
vacío**. Pasó dos veces. La primera se llevó el relleno de una fila entera; la
segunda dejó invisible la palabra clave del hero, porque su color es
`transparent` y el degradado que la pintaba había desaparecido. Ninguna otra
comprobación lo ve, y en pantalla se manifiesta como "algo no se pinta", que
manda a buscar a cualquier otro sitio. Esta regla mira los DOS archivos CSS.

**`check-contrast.py`** lee los tokens reales de `css/tokens.css` — nunca una
copia hardcodeada, así que si alguien cambia un color el script se entera — y
calcula dos familias de contraste WCAG. Textual (1.4.3, mínimo 4,5:1): 17
parejas texto/fondo — texto principal, de cuerpo, atenuado, la plata de
acento, las dos paradas del titular con brillo, y el texto y el subtítulo
sobre los tres rellenos (fuego, teal, verde). No textual (1.4.11, mínimo
3:1): las tres paradas de `--grad-stroke` —el filo metálico de las redes, las
filas de vidrio, las cards de colaboraciones y el retrato del hero— contra
`--ink`, que es el fondo real sobre el que se pinta. Sale con código 1 si
alguna pareja no llega a su mínimo.

Ambos deben salir con código 0 antes de cualquier commit que toque CSS.

Si algún día quieres subir o bajar la luz ambiente de golpe, los dos mandos
son `opacity` en `.backdrop__glow` y en `.backdrop__glyphs`, dentro de la
sección 3 de `styles.css`.

---

## Decisiones que conviene conocer antes de tocar el CSS

**El decorado es neutro para que el color signifique algo.** Hubo dos versiones
antes de esta: una con las filas en degradado de fuego a todo lo ancho, y otra
con el fuego repartido en filos, fondos y titulares. La primera saturaba —tres
bloques naranjas seguidos dejan sin jerarquía a todo lo demás—; la segunda dejó
la página con color en todas partes, y los talleres no destacaban por tener
color sino a pesar de que lo tenía todo el mundo.

La regla que quedó: **el decorado en gris, y color solo en lo que se vende.**
Hoy son los dos talleres. El día que se rellenen las cuatro filas, o que
vuelva el naranja a los filos, dejará de funcionar por la misma razón las dos
veces.

**Cualquier fila rellena lleva texto negro, sea del color que sea.** Blanco
sobre el dorado `#FFC252` mide 1,54:1, sobre el teal 1,86:1 y sobre el verde
1,49:1 — los tres, fallos graves. El componente `row--fill` ya lo impone, y
`tools/check-contrast.py` falla si algún relleno futuro no llega a 4,5:1.

**El trazo va de claro a apagado a claro, no de un color a otro.** Es lo que lo
hace leer como canto de metal biselado en vez de como una línea gris. Y el
punto apagado va en MEDIO: puesto en un extremo, el filo parece mal impreso.
Su parada central es además la que fija el mínimo — por debajo del 34% de
alpha deja de cumplir 1.4.11 y el script falla.

**El titular con brillo se mueve poco a propósito.** `--grad-text-shine` va de
plata apagada a casi blanco, no de gris oscuro a blanco: un degradado de gris
más abierto se lee como texto mal renderizado, no como un reflejo. Arranca en
`--steel-soft` y no más abajo porque ese mismo token pinta la palabra clave del
hero, que va sobre el velo de la FOTO y no sobre negro plano.

**Los enlaces no llevan número.** Los tuvieron (01, 02, 03) en una columna
propia a la izquierda. Numerar cuatro enlaces sugiere un orden que hay que
seguir y aquí no lo hay: cada fila es una puerta independiente. Sin ellos la
lista se centra y gana aire, que es la mitad de lo que hace que algo se lea
caro.

**Se quitan filos donde son decoración, no donde son affordance.** Las nueve
cards de colaboraciones perdieron el suyo: una foto ya tiene su propio límite y
nueve filos seguidos son nueve líneas más en pantalla. El hero y las filas de
vidrio lo conservan porque ahí el filo separa el bloque del fondo.

En `.social` **no se toca**: allí el trazo es la única señal de que el círculo
es un control —el vidrio de fondo mide 1,10:1 contra `--ink`—, así que quitarlo
sería un fallo de 1.4.11, no una decisión de estilo. Es la línea que separa las
dos cosas.

**El aire de las filas es parte del diseño, no relleno sobrante.** Padding de
24 px en móvil y 32 en escritorio, con 20 px entre filas. Eran 16 y 20. Menos
líneas más más espacio es toda la fórmula; si alguien aprieta esto para que
«quepa más arriba del pliegue», se pierde justo lo que se estaba comprando.

**La cinta de colaboraciones sí gira sola.** Contenido en movimiento de más de
cinco segundos exige un control de pausa (WCAG 2.2.2). Pausar solo al pasar el
cursor no cumple: no existe para teclado, táctil ni tecnología de apoyo. Por
eso hay un botón real (`[data-ribbon-toggle]`) que el JS revela y que
alterna el movimiento.

**`overflow-x: clip` está en `html`, no solo en `body`.** Solo el elemento raíz
propaga su overflow al viewport. Con la regla únicamente en `body`, la geometría
del fondo generaba 50 px de desplazamiento horizontal real en móvil.

**Los títulos de las filas van en caja baja.** A ese tamaño, tres títulos
seguidos en mayúsculas de peso 900 pedían más atención que el titular de la
página y volvían pesada la lectura. Las mayúsculas quedan para el nombre, el
subtítulo y los encabezados de sección.

---

## Antes de publicar

- [x] Las cuatro URLs cambiadas y sus `data-todo` borrados
- [ ] Los tres perfiles de redes cambiados
- [ ] Los dos enlaces de WhatsApp/soporte probados desde un móvil: que el
      mensaje precargado llegue entero y sin caracteres rotos
- [ ] Los cuatro datos de la bio rellenados, o la frase reescrita sin ellos
- [ ] Confirmado que respondes tú el WhatsApp (o cambiado el texto)
- [ ] Las imágenes reales sustituidas, con permiso de uso de las colaboraciones
- [ ] `grep -n 'data-todo\|reemplazar-url\|class="tbd"' index.html` no devuelve nada
- [ ] Probada en un móvil de verdad, no solo en el navegador de escritorio

---

## Comprobado en el navegador

- Sin scroll horizontal a 390 px ni a 1440 px (medido con `scrollTo`, no a ojo)
- Cero errores de consola procedentes de la página
- Un solo `<h1>`; recorrido de tabulación completo: saltar al contenido →
  4 filas → cinta de tarjetas de colaboraciones → botón de pausa de la cinta →
  3 redes
- Anillo de foco de dos tonos visible en todo lo interactivo
- Los cuatro iconos y las cuatro flechas se renderizan al tamaño previsto
- Las cuatro baldosas resuelven su color: teal, verde, oro y oro — comprobado
  leyendo el estilo computado, no la hoja de estilos
- Contraste del texto secundario de las filas sobre su fondo de vidrio: 6,06:1
- Sin JavaScript la página se ve completa y todos los enlaces funcionan
- HTML + CSS + JS: 22 KB comprimidos

## Lo que queda pendiente de verificar en dispositivo real

- Fluidez del scroll en un Android de gama media
- `prefers-reduced-motion` con la preferencia activada en el sistema: el bloque
  está escrito y revisado, pero no se ha podido forzar la preferencia del
  sistema operativo desde aquí
