# Link in bio — Jhei Trujillo

Página única en HTML, CSS y JavaScript planos. Sin build, sin dependencias y sin
ninguna petición a servidores de terceros. Se sube tal cual a cualquier hosting
(Netlify, Vercel, GitHub Pages, cPanel) y funciona.

Línea gráfica heredada de la guía de AIVI: su tipografía (Hanken Grotesk) y su
lenguaje visual. **El isotipo de AIVI aparece en un solo sitio** —el icono de la
fila que enlaza a la plataforma, y su marca de agua— y en ningún otro. Durante
mucho tiempo no apareció en absoluto; se incorporó con el archivo original
(`AV-Logo_2.svg`) cuando esa fila pasó a ser la destacada.

**Todo el decorado es neutro.** Filos, resplandores, filetes y flechas van en
grises fríos sobre un negro azulado (`#080b12`, no gris neutro: se midió sobre
la referencia gráfica).

**Queda UN solo color en toda la página**, y ni siquiera rellena nada:

| Color | Dónde | Qué dice |
|---|---|---|
| Azul `#9dbbf7` | Una palabra dentro de un titular | "Este es el concepto de la frase" |
| — | Todo lo demás | Nada: es decorado |

La fila destacada no se separa por matiz: se separa por **luz**. Se rellena con
la rampa de acero —el mismo gris claro que ya dibuja filos y filetes— y su
texto se invierte a tinta. Tres píldoras de cristal casi negro y una de metal
claro se distinguen por el valor, que es la señal más fuerte que hay en una
página oscura.

**Aquí hubo dos intentos fallidos y los dos enseñan algo.** Primero un teal y
un verde que marcaban cuál de las cuatro filas era un taller: eso era una
TAXONOMÍA —"estas dos son de la misma familia"— y en una lista de cuatro
botones la familia no es una pregunta que nadie esté haciendo. Después un
naranja de brasa sacado del hue de `--fire-orange`, con el argumento de que los
tonos de fuego de AIVI llevaban sin consumidor desde que la página se volvió
neutra y aquello los devolvía a su oficio.

Ese segundo argumento salía de **leer `tokens.css`, no de mirar la pantalla**.
En pantalla esta página es fría: acero, cristal oscuro y una palabra en azul.
Un bloque cálido ahí no destacaba, chirriaba. Que un token esté declarado y sin
usar no es una razón para usarlo — a veces es la prueba de que el diseño ya
decidió prescindir de él.

Y una señal solo funciona si es escasa: cuando el naranja estaba repartido por
filos, fondos y titulares, nada destacaba por tener color sino a pesar de que
lo tenía todo el mundo.

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

Hoy no devuelve nada: los dos enlaces y las tres redes ya apuntan a su
destino real.

### 1 · Los enlaces

Todos apuntan ya a su destino real. No queda ningún `data-todo`.

| Fila | Destino |
|---|---|
| **Conoce AIVI** (destacada) | `https://aivinetwork.com` |
| **¿Dudas o soporte?** | `https://go.aivi.chat/soporte-bio` |

**Eran cuatro.** Las dos filas de taller —Vuélvete VIRAL y Contenido que
V3NDE— se retiraron el 2026-08-22 porque los dos talleres ya se dieron. El
marcado está en el historial, y en `index.html` queda una nota con lo único
que costaría rehacer de memoria: el formato del enlace de WhatsApp con mensaje
precargado y qué iconos llevaban.

**El enlace de WhatsApp**, para cuando vuelva un taller: el número va con
código de país y sin `+` ni espacios, y el mensaje va URL-encoded (`%20` por
espacio, `%2C` por coma, `%C3%A9` por `é`). Si lo editas a mano y dejas un
espacio o una tilde sin codificar, WhatsApp corta el texto en ese punto sin
avisar.

**Para añadir una fila**, duplica el `<a class="row stroke">` de soporte y
cámbiale icono, texto y `href`. Los retardos de entrada ya están puestos hasta
cuatro filas en `css/styles.css` (busca `.row:nth-of-type(`), así que las dos
siguientes entran escalonadas sin tocar nada; de la quinta en adelante hay que
añadir un bloque más siguiendo el patrón, +70 ms respecto al anterior.

**Si la fila nueva tiene que destacar**, llévale `row--featured` a ELLA y
quítaselo a AIVI. En cuanto dos filas lo llevan, ninguna destaca.

### 2 · Cuál es la fila destacada

**Tres filas son la misma pieza**: vidrio oscuro con trazo de plata. **La
cuarta se lo lleva todo, y va PRIMERA.**

| Clases | Qué cambia | Quién la lleva |
|---|---|---|
| `row stroke row--featured` | Relleno de acero claro, texto invertido a tinta, halo blanco y un reflejo que gira | AIVI |
| `row stroke` | Nada: es la base | Soporte |

**La posición es la otra mitad de la jerarquía.** Estuvo la tercera, y destacar
la tercera obliga al ojo a recorrer dos filas que no importan antes de llegar a
la que sí. Un botón destacado en mitad de una lista compite con su propio
orden de lectura.

**El texto se invierte con el fondo, y eso tiene una trampa que ya mordió dos
veces.** Todo lo que fije su propio color deja de heredar, así que
`color: var(--ink)` en la fila no basta.

La primera vez fue el título en reposo: `.row__title` declaraba
`--text-primary` y seguía saliendo blanco sobre el metal. La segunda fue peor
porque estaba en un ESTADO y no se veía sin pasar el ratón — `--tile-glyph-hi`
seguía valiendo `var(--paper)` de cuando el relleno era naranja oscuro, así que
al pasar el cursor el glifo, la flecha y el aro se volvían blancos sobre fondo
casi blanco y **desaparecían justo en el estado que existe para confirmar que
algo responde**.

Por eso el título, el subtítulo, la flecha, el glifo, la marca de agua, el
reflejo, el relleno del aro y el tono encendido de todos ellos pasan por un
token que el modificador reapunta. La regla que queda: **al cambiar el fondo de
un componente hay que repasar todos sus estados, no solo el de reposo.**

**Para mover el destacado**, llévate la clase `row--featured` y el `<span>` del
reflejo. La marca de agua la llevan todas, así que esa se queda. No hay
que tocar CSS. Pero muévelo, no lo dupliques: **en cuanto dos filas lleven el
modificador, ninguna de las dos destaca.**

El modificador **casi no declara propiedades**: reapunta los tokens que `.row`
y `.stroke` ya consumían. Por eso la fila destacada y las de vidrio se
comportan idéntico en hover, foco y pulsación sin repetir una sola regla.

**Los contrastes van holgadísimos** — título 14,03:1, subtítulo 8,31:1, flecha
6,42:1, glifo 11,66:1, y el relleno 14,03:1 contra el fondo. Con el naranja que
hubo antes ese último iba a 3,13:1 sobre un mínimo de 3. Invertir el valor en
vez de cambiar el matiz no solo destaca más: deja de ir justo.

El relleno es un degradado, así que manda su parada más **oscura**
(`--steel-lit`) — al revés que en un relleno oscuro, porque aquí el texto es el
oscuro. Es fácil calibrar contra la parada equivocada sin darse cuenta.

### 2 bis · Lo que llevan TODAS las filas

Tres tratamientos que no distinguen unas de otras: hacen que la lista entera
deje de parecer una lista.

**La marca de agua.** El icono de la propia fila a tamaño de cartel, asomando
por el borde derecho por debajo del texto. Es el MISMO dibujo que el glifo
pequeño de la izquierda, instanciado con `<use href="#glyph-…">` en vez de
duplicado: los trazos viven una sola vez en el archivo.

Que sea su propio icono y no una geometría genérica es lo que **da identidad a
cada fila ahora que ninguna tiene color propio**. Antes las separaba el teal y
el verde; al retirarlos hacía falta algo que ocupara ese trabajo.

El truco está en `stroke-width`. Los iconos lo llevan como ATRIBUTO
(`stroke-width="1.6"`), y a diez aumentos eso es un trazo de 16px: una mancha.
La declaración de CSS gana —en SVG, CSS siempre gana a un atributo de
presentación— y además **se hereda dentro del árbol del `<use>`**, que es la
única forma de alcanzar ahí dentro. A 0.5 el dibujo pasa de mancha a plano
técnico.

**Y lo atenúa `opacity`, no un alfa dentro del color.** No es lo mismo, y la
diferencia se ve. Con el alfa metido en el color cada trazo se pinta por
separado, así que allí donde dos se cruzan —y en estos dibujos se cruzan
constantemente— los alfas se SUMAN: el resultado eran nudos más claros en cada
intersección, un dibujo con la densidad a manchas. `opacity` sobre el elemento
obliga a componer todo el SVG en una sola capa y a atenuarla después, así que
los cruces ya no acumulan.

Es una trampa que reaparece en cualquier dibujo translúcido que se pise a sí
mismo, y no se ve venir leyendo el CSS: los dos escriben "4%".

`.row` lleva `overflow: hidden` por esto. Sin él el dibujo se sale por los
cuatro lados y se ve flotando encima de las filas de al lado. No recorta nada
más: el filo y el reflejo van con `inset: 0`, y el halo y el anillo de foco son
`box-shadow`, que el overflow del propio elemento que la proyecta no toca.

**El barrido especular.** Una banda de luz cruza la fila al pasar el cursor. No
es un resplandor que se enciende: es un reflejo que **se desplaza**, y esa
diferencia es la que hace que la píldora se lea como una superficie física.

Son dos capas de `background-image` — el barrido encima del relleno — y lo que
se anima es `background-position`. Tres detalles que no son estilo:

- Va en su **propia duración** (`--d-sweep`, 700ms) y no en los 160ms del resto
  del hover. Un barrido rápido no se lee como un reflejo, se lee como un
  parpadeo.
- Al salir vuelve a su sitio **sin transición**. Verlo desandar el camino rompe
  la ilusión: se va, y reaparece por la derecha la próxima vez.
- En la fila destacada lo que cruza es una **sombra**, no una luz: un reflejo
  blanco sobre metal claro no existe. Mismo gesto, valor invertido, como el
  texto.

**Las esquinas desiguales.** Las cuatro esquinas de cada píldora tienen radios
distintos: `12px 36px 24px 24px`. Cuatro píldoras idénticas apiladas se leen
como una tabla; con las esquinas desiguales cada una es una forma, y la lista
deja de parecer una lista.

El reparto tiene una lógica, y conviene respetarla al tocarlo:

| Esquina | Radio | Por qué |
|---|---|---|
| Superior izquierda | 12 px | Es por donde entra la lectura; un canto vivo ahí ancla el bloque |
| Superior derecha | 36 px | Es la esquina que queda libre, sin texto ni icono: es donde la curva se ve |
| Las dos de abajo | 24 px | El valor de siempre. Hacen de base estable |

Invertirlo —abierta arriba a la izquierda, cerrada arriba a la derecha— lee como
un error de maquetación: la curva grande choca justo contra el arranque del
texto.

Va en un solo token con las cuatro (`--r-row`) y no en cuatro tokens, porque lo
que define la silueta es la **relación** entre ellas. `.stroke` y la baldosa
heredan de esa declaración, así que el filo en degradado sigue la misma silueta
sin una línea más.

**La flecha, en un disco con resplandor.** Era una flecha fina flotando en el
borde derecho —la convención de un elemento de lista— y ahora es un control con
su propia caja. El círculo no es un invento: la página ya tiene tres, los de
redes. El aro va en `currentColor`, así que la fila destacada no necesita ni una
regla — hereda su tinta y sale oscuro sobre el metal, igual que sale plata sobre
el vidrio.

Dentro lleva **tinta translúcida**, no un relleno opaco: sobre el vidrio de la
fila apenas se nota como color y lo que hace es AHONDAR el círculo, que es lo
que separa una flecha apoyada en algo de una flecha flotando. Al pasar el cursor
el disco ahonda MÁS, no se aclara — aclararlo lo devolvía a parecer un aro vacío
justo cuando más tiene que parecer un botón.

**El alfa del disco no es el mismo en todas las filas, y no puede serlo.**
Sobre vidrio oscuro un 38% se hunde y ya está; sobre el metal claro de la
destacada ese mismo 38% pinta un disco gris que se come la flecha —4,39:1, por
debajo del mínimo—, así que allí baja al 14%. `check-contrast.py` mide la flecha
contra el DISCO y no contra el relleno de la fila, porque el disco es el fondo
real que tiene detrás.

Alrededor, un resplandor de **tres sombras apiladas**: una sola sombra
difuminada tiene un solo borde de caída y se lee como un aro borroso; con el
desenfoque creciendo y el alfa cayendo —9%, 6%, 3%— la caída se suaviza y pasa a
leerse como luz. Su alcance máximo es 22px, y ese número lo fija el recorte, no
el gusto: `.row` corta lo que sale de la píldora y el hueco hasta el borde
derecho es el relleno de la fila, **24px en móvil**, que es el que manda. Más
ancho y el resplandor se corta en seco contra el filo.

### 2 ter · La ranura de contexto

Un chip mono corto que se mete en cualquier fila: `<span class="row__slot">
Demo</span>`. Hoy lo lleva la destacada.

**Es un eje distinto de la jerarquía, y conviene no mezclarlos.** La fila
destacada dice "pulsa esta primero"; la ranura dice qué tipo de cosa es o
cuándo caduca — `GRATIS`, `6 CUPOS`, `NUEVO`. Puede ir en cualquier fila.
**En cuanto se use solo en la destacada, deja de ser información y pasa a ser
decoración.**

**Que sea CORTA no es estilo, es presupuesto.** El chip comparte fila con el
título: con `PLATAFORMA` medía 120px y partía el subtítulo en tres líneas. Con
`Demo` mide 64 y no parte nada. Cuatro o cinco caracteres.

**La colocación es progresiva y el orden importa.** La base —debajo del texto—
no necesita `:has()` ni una columna de más, así que sale en cualquier navegador
y a cualquier ancho. El chip pegado al borde derecho es la mejora, y vive dentro
de `@media (min-width: 30rem)` con `:has()`. Si `:has()` fuera la base, donde no
hubiera soporte el cuarto hijo caería en una fila implícita de la rejilla. Es la
misma lección que ya estaba escrita en el anillo de foco de la cinta.

### 3 · Los iconos

Cada fila lleva su icono como SVG dentro del HTML, así que no hay archivos que
gestionar ni peticiones extra. Son de trazo, 24×24, con juntas redondeadas para
que hablen el mismo idioma que la geometría de AIVI.

| Fila | Icono | Color del glifo |
|---|---|---|
| AIVI (destacada, 1ª) | El isotipo de AIVI, de relleno | Tinta, sobre el metal claro |
| Soporte | Auriculares con micrófono | Plata |

**Cada icono se dibuja DOS veces y se escribe una.** El glifo pequeño de la
izquierda vive dentro de un `<g id="glyph-…">`, y la marca de agua del fondo lo
instancia con `<use>`. Cambiar un icono sigue siendo cambiar un solo `<path>`.

**El de AIVI es la excepción y va de RELLENO, no de trazo.** Es un logo, no un
pictograma dibujado para esta lista, y contornearlo lo rompería. Del archivo
original se cambian dos cosas: se quita el bloque `<style>` con su
`fill: #fbfbfb` y se pone `fill="currentColor"` en el grupo. Sin eso el logo
saldría siempre blanco y no se enteraría de que en su fila el color es tinta.

Su `viewBox` tampoco es `0 0 24 24` como el de los demás, sino
`0 0 478.9 473.06`, el del archivo. **El `<svg>` de la marca de agua tiene que
llevar el mismo**, o el `<use>` dibuja el logo a la escala equivocada.

Y su marca de agua va **más apagada** que las otras tres (3,5% contra 4%): una
masa sólida y un contorno al mismo alfa no pesan lo mismo ni de lejos, porque
el contorno deja pasar el fondo entre las líneas y la masa no.

**Los glifos van dentro de una baldosa de cristal**, 48 px en móvil y 54 en
escritorio, con el dibujo a 24 px centrado.

Esto **revierte** una decisión anterior del proyecto —los glifos estuvieron
sueltos porque "un icono metido en su cajita es la convención de un menú de
aplicaciones"— y conviene saber qué cambió para que ahora funcione. Aquella
baldosa era un cuadrado **opaco con relleno de color y filo**, y sí parecía el
icono de una app. Esta no tiene relleno propio: es vidrio, el mismo material
del que está hecha la fila que la contiene, con la luz entrando por arriba.

**Lo que la hace leer como cristal son tres sombras a la vez**, y quitar
cualquiera la desarma:

| Token | Qué hace |
|---|---|
| `--sh-2` | La proyectada, que despega la baldosa de la fila |
| `--sh-lip` | El filo interior SUPERIOR: el canto que recoge la luz |
| `--sh-lip-in` | El filo interior inferior: la sombra del canto opuesto |

Van juntas en un solo token, `--sh-tile`, precisamente porque el efecto lo
hacen las tres — separadas invitaban a tocar una sola. Los tres llevaban
declarados y sin consumir desde el rediseño.

En la fila destacada la baldosa **se invierte** con el resto de su fila:
`--tile-surface` pasa a `--grad-glass-ink` y `--sh-tile` a su versión de fondo
claro, donde el filo de arriba es blanco casi opaco y la sombra proyectada se
acorta — sobre una superficie clara una sombra larga se lee como suciedad, no
como profundidad. El glifo va en tinta, por `--tile-glyph`.

La baldosa lleva **tamaño fijo** (`flex: none`): es lo que mantiene los cuatro
títulos arrancando en la misma vertical. Sin él cada glifo mediría lo suyo y la
columna de texto bailaría de fila en fila.

Al crecer en escritorio, la baldosa gana **aire alrededor del dibujo**, no un
dibujo más grande: el glifo se queda en 24 px. Es lo que hace que se lea como
una pieza de cristal con algo dentro y no como un icono con marco.

Cuando había dos filas de taller llevaban iconos de educación **distintos** a
propósito —un birrete y una pizarra— porque dos birretes seguidos se leen como
el mismo taller repetido, y lo que cambia entre ellos es el tema, no el
formato. Si vuelven los talleres, esa regla sigue en pie: con el color
retirado, el icono es la única señal de que son dos cosas distintas.

Para cambiar uno, sustituye el contenido de su `<svg>` por otro path. Mantén el
`viewBox="0 0 24 24"`, `fill="none"` y `stroke="currentColor"`: el color y el
tamaño los pone el CSS, así que el icono nuevo hereda todo automáticamente.

### 3 bis · Por qué el destacado no tiene color

**No hay ningún token de acento en el proyecto.** La fila destacada se rellena
con `--steel-glare` → `--steel-lit`, dos escalones de la rampa de acero que ya
existía para filos y filetes. Cero colores nuevos.

Aquí vivieron dos intentos —un teal con un verde, y después un naranja de
brasa— y el porqué de retirar los tres está arriba, en la sección de la línea
gráfica. Lo que queda por decir es la parte técnica:

```css
/* No hay tokens de color. El relleno se monta con la rampa que ya estaba: */
--grad-row-featured: linear-gradient(160deg,
  var(--steel-glare) 0%, var(--steel-lit) 78%, var(--steel-lit) 100%);

/* Y los oscuros de dentro, que son los mínimos para 4.5:1 sobre --steel-lit */
--row-note-featured:  rgb(var(--rgb-ink) / 78%);   /*  8.31:1 */
--row-arrow-featured: rgb(var(--rgb-ink) / 70%);   /*  6.42:1 */
--tile-glyph-featured: rgb(var(--rgb-ink) / 90%);  /* 11.66:1 */
```

**El filo de esta fila va en TINTA y no está en la lista de contrastes**, y las
dos cosas son la misma decisión. Sobre un relleno claro un filo claro no
existe; y en cuanto la fila se rellena, el filo deja de cargar con 1.4.11
porque el límite del control lo marca el propio relleno, que mide 14,03:1
contra el fondo. Un filo solo entra en la lista de `check-contrast.py` cuando
es la **única** señal — que es el caso de `.social`, no el de esta fila.

**Si subes o bajas la luz de `--steel-lit`, los cuatro contrastes de la fila se
mueven a la vez.** Es la parada que manda.

### 4 · Las redes

Tres enlaces al final del HTML: TikTok, Instagram y YouTube. Cambia el `href` y
deja el `aria-label` como está — es lo que lee un lector de pantalla.

### 5 · Las cifras de autoridad

Tres, y viven **en el hero**, no en una bio al final:

| Cifra | Qué es |
|---|---|
| `8+` | Años de experiencia |
| `5,500+` | Estudiantes formados |
| `700+` | Negocios asesorados |

Para cambiar una, edita solo el número. **El `+` va dentro del mismo `<span>` a
propósito**, para que no se separe en un salto de línea.

**Están arriba porque una cifra que respalda a quien habla solo trabaja si se
lee ANTES de decidir.** Abajo del todo llegaban cuando el visitante ya había
pulsado o se había ido.

**Si no tienes un dato, no lo aproximes: quita esa `<li>` entera.** Dos cifras
ciertas valen más que tres con una inventada, y la rejilla se reparte sola.

Una cosa más para decidir antes de publicar: el texto de WhatsApp dice *"Te
contesto yo por WhatsApp, no un bot"*. Solo publícalo si de verdad respondes en
persona. Si hay asistente o automatización, cámbialo por *"Cuéntame tu idea por
WhatsApp"*.

### 6 · La bio está OCULTA

La sección "Sobre mí" —foto, titular, arroba y dos párrafos— **no se borró: está
comentada** dentro de `index.html`, justo debajo de las redes, con su texto
intacto.

Para devolverla, el comentario de ahí explica los dos pasos: descomentar el
bloque y ponerlo encima del `<nav>`, y devolverle a la sección su
`aria-labelledby="bio-title"`, que perdió al ocultarse.

**Dos cosas NO se fueron con ella, y las dos importan:**

- **Las tres cifras** subieron al hero (arriba). Si algún día devuelves la bio y
  las quieres allí, **muévelas, no las copies**: duplicadas dejan de ser un dato
  y pasan a ser ruido.
- **Las redes se quedaron.** Vivían dentro de la sección de la bio, así que
  ocultar la sección entera se habría llevado por delante los tres únicos
  enlaces a TikTok, Instagram y YouTube de la página.

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

**Y se ve al instante.** `_headers` sirve `/assets/img/*` con `no-cache`, que no
significa "no guardes" sino "guarda, pero pregunta antes de usarlo": el
navegador comprueba en cada visita y descarga solo si el archivo cambió.

Estuvo en `max-age=86400` y ese día costaba caro: `max-age` sin `no-cache`
significa que el navegador **ni pregunta** durante ese tiempo, así que una foto
nueva no es que tardara en verse — es que quien acababa de publicarla seguía
viendo la vieja, sin forma de diagnosticarlo desde fuera (`curl` no usa caché y
responde con el archivo nuevo). Si algún día pesa más la velocidad, la solución
no es volver a subir el `max-age`: es ponerle hash al nombre y cachear un año.

| Archivo | Tamaño | Notas |
|---|---|---|
| `assets/img/jhei-hero.jpg` | 2752 × 1536 (16:9) | **Hero, la ÚNICA.** Apaisada, a pantalla completa, sujeto a la derecha y lado izquierdo en penumbra. Sirve para móvil y escritorio: el encuadre lo resuelve `object-position`. Ver "Imagen del hero" más abajo. |
| `assets/img/jhei-avatar.png` | 480 × 480 | Solo se usa como icono de acceso directo (`apple-touch-icon`), no aparece dentro de la página. Cuadrada, rostro centrado. |
| `assets/img/collab-01…09.jpg` | 3:4, mínimo 480 px de ancho | Portadas de los videos, en color. Recórtalas SIN el contador de TikTok ni la etiqueta "Anclado": esos datos los dibuja la página. |
| `assets/img/og-image.png` | 1200 × 630 | Lo que se ve al compartir el enlace en redes. |
| `assets/img/favicon.svg` | — | El icono de la pestaña. |

No hay mockups de dispositivo ni una foto de perfil en círculo en la página: el
hero ocupa la pantalla entera y a sangre (ver más abajo) y las redes son
círculos de icono, no fotos.

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
único que existe; en escritorio el texto del hero se superpone al lado en
penumbra de la foto y centrarlo lo pondría encima del sujeto.

Los cortes no son todos iguales, y cada componente cambia cuando su propio
contenido lo pide:

| Bloque | Centrado hasta | Por qué ahí |
|---|---|---|
| Hero y botones | `60rem` | Es donde el texto del hero se va a la izquierda |
| Bio | `56rem` | Es donde la bio pasa a dos columnas |

**El hero ya no comparte eje con el resto**, y es la única excepción. Botones,
colaboraciones, bio y footer siguen arrancando en el mismo píxel —el eje de
620 px—, pero el texto del hero usa uno propio de 1120 px y entra mucho más a
la izquierda. El porqué está en "El eje del hero NO es el de la página", más
abajo.

El párrafo de la bio centrado se lee algo peor que alineado a la izquierda —el
ojo pierde el arranque de cada línea— pero en una columna estrecha la pérdida
es pequeña. Si algún día pesa más la lectura que la simetría, se cambia una
línea: `text-align` en `.bio`.

---

## Imagen del hero

**Una sola foto para todos los tamaños**, a sangre por los cuatro lados y
ocupando el 70% del alto de la ventana, con el texto superpuesto y un degradado
inferior que la funde con los botones.

El 70% (`--h-hero`) estuvo en 100 y bajó por una razón concreta: a pantalla
completa no entraba ni un botón sobre el pliegue, y en un link in bio la foto
es decoración y los botones son la página. **Cambiar ese número obliga a
revisar otras tres cosas** —el `object-position` en X, el mismo en Y y el
fundido inferior— porque las tres se calibraron contra esta altura. Está
explicado en cada sitio.

`assets/img/jhei-hero.jpg` es 2752 × 1536 px (16:9), 324 KB. Apaisada, el
sujeto en el tercio derecho y el izquierdo ocupado por una pizarra en penumbra,
que es donde se superpone el texto en escritorio.

Fueron dos archivos —uno por breakpoint— hasta que esta foto los hizo
innecesarios. La razón de que fueran dos era buena y sigue siendo cierta como
principio: ningún `object-position` convierte una composición en otra. Lo que
cambió es que aquí no hace falta convertir nada, porque el sujeto está lo
bastante cerca del borde derecho como para que el recorte lateral lo centre
solo.

### El encuadre: 95% en X, 7% en Y

Son los dos números de los que depende toda la maqueta responsive, y los únicos
que no se pueden tocar a ojo.

**La X (95%).** `object-fit: cover` en una caja más estrecha que la foto
recorta por los **lados**, y `object-position` decide por dónde. Anclar al
100% —"pegado a la derecha", que es lo que suena bien— es justo lo que no
funciona: el sujeto no está pegado a ese borde, está en torno al **78% del
ancho del archivo**, así que al anclar al 100% la cara sale despedida contra el
filo izquierdo del recorte y en un teléfono queda cortada.

El número sale de despejar la posición que deja la cara centrada:

```
p = (f·W − C/2) / (W − C)
```

con `f` = 0.785 (la cara, en fracción del ancho del archivo), `W` el ancho de
la foto ya escalada a la altura de la CAJA y `C` el ancho de la pantalla. Con
un teléfono de 390 × 844 y el hero al 70%, da 0.951.

Fue 88% mientras el hero llenaba la pantalla. Al bajarlo hubo que rehacerlo, y
el motivo no es evidente: **en una caja más baja `cover` escala la foto más
pequeña**, así que cabe más ancho de archivo dentro del mismo teléfono y el
sujeto se corre hacia el centro-derecha. Con el 88% viejo la cara se quedaba en
el 67% del encuadre en vez de en el 50%.

En **escritorio la X ya no influye**: con el hero tan apaisado, `cover` escala
por el ancho y se ve la foto entera de lado a lado, así que no hay recorte
lateral que posicionar. Solo manda en móvil y tableta.

**La Y (7%).** Al bajar el hero de 100svh a 70svh el recorte vertical se
multiplicó por tres, y repartido a partes iguales —que es lo que hace el 50%—
se comía el pelo: en la foto solo hay **87px de aire por encima de la
coronilla**, un 5,7% de la altura del archivo. Al 7% el recorte se lo lleva
casi entero el borde de abajo, que es donde solo hay penumbra, y arriba quedan
entre 25 y 34px de aire según la pantalla.

El caso más apretado no es el más pequeño sino el más **apaisado**: cuanto más
ancha y baja la ventana, más alto se escala la foto y más se recorta arriba.
Por eso la cuenta se comprobó hasta 2560 × 1080.

**Si cambias la foto o la altura del hero, estos dos números se recalculan, no
se heredan.** Mide dónde caen la cara y la coronilla en el archivo nuevo, mete
`f` en la fórmula y comprueba el resultado con `tools/check-hero-contrast.py`,
que imprime el encuadre y la altura que está leyendo del CSS.

### El degradado de abajo

No es decoración: es lo que sustituye al borde. Llega a `--ink` **opaco** antes
del final —no justo en el borde—, y `--ink` es exactamente el color de fondo de
la página, así que no hay costura posible entre el final de la foto y el
principio de los botones.

Los dos registros usan degradados distintos, y no solo con paradas distintas:
con **unidades** distintas.

**En escritorio va en porcentajes.** El texto está arriba y a la izquierda, así
que aquí abajo solo hace falta lo justo para empalmar; arranca en el 46%. Lleva
dos paradas de cola —89% y 94%— que parecen relleno y no lo son: el filo que se
veía en el borde inferior no salía de que el degradado fuera corto, sino de que
llegaba al final **con un salto**, de tinta al 92% a tinta plana. Ese último
tramo de pizarra a medio apagar contra un negro liso se lee como un corte recto
aunque la diferencia de color sea de quince niveles. Alargar la cola cuesta
mucha menos luz que adelantar el degradado entero.

**En móvil va en PÍXELES, y medidos desde el borde de abajo** (`0deg`, no
`180deg`). Es la decisión menos obvia del archivo y la que más problemas
resolvió de golpe.

El fundido de móvil tiene un trabajo concreto: sostener un bloque de texto que
mide **258px** y vive pegado al borde inferior. Ese bloque mide lo mismo en un
teléfono donde el hero ocupa 591px que en uno donde ocupa 398. En porcentaje,
un velo calibrado para el corto deja el largo casi negro entero, y uno
calibrado para el largo deja el corto ilegible — se probaron los dos y **no hay
ningún juego de paradas en % que cumpla en los dos sin apagar la foto**.

Anclado en píxeles se ajusta solo: los primeros 265px desde abajo van oscuros y
por encima de 440px la foto no se toca, sea cual sea la altura del hero.

**Estas cifras se mueven con el bloque, y ya lo han hecho tres veces:**

| Cuándo | Bloque | Fundido |
|---|---|---|
| Antes de subir las cifras | 200 px | 215 px |
| Con las cifras y 56 px de hueco abajo | 290 px | 292 px |
| Con el hueco bajado a 24 | 258 px | 265 px |

La segunda vez **tiró las seis pantallas móviles por debajo del mínimo a la
vez** — a 320 px llegó a 1,04:1. La tercera hizo lo contrario: acercar el texto
al borde lo mete en la zona que ya era oscura, así que sobró velo más arriba y
la foto recuperó luz.

Cambiar contenido **o separación** del hero recalibra este degradado entero, y
no hay forma de enterarse mirando — el texto se sigue viendo, lo que baja es el
contraste contra la pizarra que asoma por detrás. Lo caza
`check-hero-contrast.py` en cuanto se le actualiza `TEXT_BLOCK_PX`.

El peor caso es un teléfono de 320 × 568: ahí el hero mide 398px, así que el
bloque de texto ocupa casi tres cuartas partes de él y `cover` recorta la foto
mucho más ancha, metiendo pizarra clara justo por detrás. En esa pantalla el
fundido llega arriba del todo con un 14% de tinta; en una de 844 deja 131px de
foto intacta.

### Dónde va el texto

| | Posición | Sobre qué se apoya |
|---|---|---|
| Escritorio (≥ 60rem) | izquierda, por encima del centro | la penumbra de la foto + la caída lateral del velo |
| Móvil | abajo, centrado | el fundido inferior, que ahí ya es casi negro |

No es una incoherencia: es la misma decisión —poner el texto donde la imagen
está oscura— aplicada a dos recortes distintos. Al estrecharse la pantalla el
lado izquierdo se va fuera del encuadre y la única zona oscura que queda es la
de abajo, que es la que fabrica el propio degradado.

En escritorio la columna de texto lleva un tope duro de `28rem`. Hoy no recorta
nada —el titular mide 369 px en su tamaño máximo y la frase unos 300— y está
para que no lo haga nunca: el velo lateral solo es opaco de verdad hasta el 62%
del ancho, y el día que alguien alargue el reclamo, sin ese tope la línea se
metería debajo de la cara, donde el contraste medido ya no vale.

### El eje del hero NO es el de la página

Es la única excepción al eje único, y conviene saberla antes de tocar nada.

`.hero__text` lleva la clase `.shell` como todo lo demás, pero en escritorio se
le sube el tope de 620 px a `--w-wide` (1120 px). Lo que mueve no es el ancho:
es el **borde izquierdo**, que es donde arranca el titular.

| | Entra por | |
|---|---|---|
| Texto del hero | **14,6%** del ancho | eje propio, 1120 px |
| Botones, colaboraciones, bio, footer | 31,5% del ancho | eje de la página, 620 px |

Los dos números salen de medir la referencia gráfica contra una captura de la
página, no de estimarlos. La referencia pone su titular en el 14,55%.

**Esto rompe el eje único, y se acepta a sabiendas.** El motivo es que desde
que el hero ocupa el viewport entero las dos cosas ya no se ven a la vez: hay
que hacer scroll para pasar del titular a los botones, y en ningún momento hay
dos arranques distintos en pantalla pidiendo alinearse. El eje único sigue
mandando de los botones hacia abajo, que es donde la página se lee como
columna. Si algún día el hero deja de ser de pantalla completa, esta excepción
deja de estar justificada y hay que devolverla a `.shell`.

La posición vertical también se midió: el bloque va centrado en el **41,5%** de
la altura del hero, no en el 50%. Lo hace `margin-block-end: 17svh`, que se
apoya en que `align-self: center` centra la caja CON sus márgenes — un margen
inferior de M sube el contenido M/2. Va en `svh` y no en `%` porque los
márgenes en porcentaje se resuelven contra el ANCHO, también los verticales.
Centrado del todo, el titular quedaba a la altura del pecho del sujeto en vez
de a la de la cara.

### El brillo que gira en el chip

El chip del hero —`IA · VIRALIDAD · NEGOCIOS`— lleva un reflejo que recorre su
trazo, una vuelta cada **11 segundos** (`--d-chip-orbit`). Lento a propósito:
por debajo de unos 8s deja de leerse como un reflejo que pasa y empieza a
leerse como un cargador dando vueltas.

Es un **degradado cónico enmascarado al anillo del borde**, la misma técnica
que `.stroke`. Lo que gira no es la caja —rotarla deformaría la píldora, que no
es cuadrada— sino el ángulo de origen del degradado; la caja no se mueve ni un
píxel. Vive en el `::before` del chip, que en el hero estaba libre porque su
punto inicial va apagado.

Tres cosas que hay que saber si se toca:

- **Necesita `@property`.** Sin declarar el tipo de `--chip-angle`, para el
  navegador es una cadena de texto y entre dos cadenas no hay interpolación: el
  ángulo saltaría de 0 a 360 de golpe en vez de recorrerlo. Donde no haya
  soporte, el reflejo se queda quieto; no se rompe nada.
- **Es decorativo y va ENCIMA del borde de 1px del chip, no en su lugar.** Si
  el reflejo fuera el único trazo, el chip se quedaría sin límite visible
  durante la mayor parte del ciclo.
- **Se para con `prefers-reduced-motion`**, y sin composición de máscara se
  apaga entero — si no, el cónico pintaría la píldora entera en vez de su
  anillo: una mancha girando detrás del texto.

### El titular de los enlaces

`Enlaces que te pueden ayudar` usa `--fs-h3`, no `--fs-h2` como el titular de
colaboraciones. Los dos son rótulos de sección pero no hacen el mismo trabajo:
aquel es una frase que afirma algo, este es una etiqueta que nombra una lista.
A `--fs-h2` partía en dos líneas dentro de la columna de 620px y sumaba 67px
justo por encima de los botones, que es lo contrario de lo que se buscaba al
acortar el hero.

Sustituye al `aria-label` que llevaba la sección, y no es lo mismo: un
`aria-label` solo existe para quien navega con lector de pantalla, y este
bloque necesitaba el rótulo también en pantalla — al acortarse el hero, lo
primero que asoma bajo la foto es este titular, y es lo que dice que la página
sigue.

El escalonado de entrada no se rompió al meterlo porque las filas se cuentan
con `nth-of-type` y no con `nth-child`: cuenta solo los `<a>`, así que un `<h2>`
en medio le da igual. Esa precaución llevaba ahí desde antes y hoy pagó.

### El cuerpo del titular

`.hero__name` usa `--fs-display`, no `--fs-h1`. El escalón se retuvo de
40 → 92 px a **36 → 76 px** para igualar la referencia, y el 76 no es un número
redondo porque no se eligió: se midió.

En la referencia la mayúscula del titular ocupa el **3,65% del ancho de la
pantalla**. La altura de mayúscula real de Hanken Grotesk es 0,707 del cuerpo
—medida dibujando la letra en un `<canvas>` y contando filas con tinta, no
estimada de una tabla—, así que el cuerpo que da ese 3,65% es 76 px. Comprobado
después en el navegador: 3,67%.

`--fs-h1` se queda declarado y sin consumidores, que es exactamente lo que era
`--fs-display` hasta que el hero lo estrenó.

### El contraste sí se puede comprobar

Es el único punto de la página cuyo contraste depende de un archivo de imagen y
no solo de los tokens, y durante un tiempo eso significó que no había forma de
vigilarlo. Ahora la hay:

```bash
python3 tools/check-hero-contrast.py
```

Recorta la foto como lo haría el navegador, compone encima las capas de
`.hero__scrim` —leyendo las paradas del CSS, no copiándolas— y busca el píxel
más claro de la banda donde cae el texto en once tamaños de pantalla. El peor
caso actual da **14.23:1** en el nombre, **10.94:1** en la frase y **4.84:1**
en la palabra clave en degradado.

El script lee del CSS el `object-position`, la altura del hero (`--h-hero`), el
eje (`--w-wide`), el tope de 28rem y las paradas de las dos capas del velo, así
que se entera solo de cualquier cambio en la geometría. Entiende paradas en `%`
y en `px`, y en los tres sentidos que usa la página: hacia la derecha, hacia
abajo y hacia arriba.

**Una advertencia que salió cara.** El alto del bloque de texto en móvil
(`TEXT_BLOCK_PX`) estuvo en 240 "por si acaso" cuando lo medido eran 197-200.
Esos cuarenta píxeles de banda inventada empujaban al velo a ser mucho más
oscuro de lo necesario para protegerla, y el resultado fue una foto apagada que
hubo que diagnosticar por separado. **Un margen de seguridad en el sitio
equivocado no es prudencia: es una decisión de diseño tomada por accidente.**

Hoy vale **258**. **Es el número que hay que actualizar cada vez que cambie el
bloque de texto del hero** —su contenido o su separación—, y de él cuelga la
calibración entera del fundido inferior.

El tercero es el que manda: la palabra en azul arranca en
`--accent-blue-deep`, el color más flojo que la página pone sobre texto, y aquí
encima va sobre una foto y no sobre negro plano. Las dos capas del velo se
calibran juntas — al suavizar el fundido inferior de escritorio una sola
versión, el azul cayó a 4.30:1 y hubo que devolvérselo a la capa lateral.

Necesita Pillow (`pip3 install Pillow`). Es la única herramienta del proyecto
que no va con la librería estándar, porque no hay forma razonable de decodificar
un JPEG sin ella; si no está instalada lo dice y se salta la comprobación en vez
de fallar.

### Peso y prioridad

Es la imagen precargada con mayor prioridad (`fetchpriority="high"`) y la
candidata segura a LCP: ocupa la pantalla entera. Va a calidad 90 y no más
baja, que es más de lo habitual, y el motivo es la mitad izquierda: es una
rampa oscura, muy lisa y muy grande, justo el material donde el JPEG hace
bandas. A calidad 84 pesaba 217 KB y las bandas aparecían al amplificar; a 90
son indistinguibles del original con el mismo aumento.

La precarga ya no lleva `media`. Con dos archivos era obligatorio —sin él, el
teléfono se bajaba los dos—; con uno solo no hay nada que elegir y cualquier
condición ahí solo podría equivocarse.

---

## Estructura

```
index.html            todo el contenido editable
css/tokens.css        color, tipografía, espaciado, movimiento — la marca entera
css/styles.css        layout y componentes; solo consume tokens
js/main.js            revelado al scroll, cinta en bucle, año del footer
assets/fonts/         Hanken Grotesk variable 100–900, auto-hospedada (56 KB)
assets/img/           imágenes, favicon
tools/                generador de placeholders y comprobaciones de diseño, contraste y encuadre del hero
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

Tres scripts. Córrelos después de tocar `css/styles.css` o `css/tokens.css`, y
siempre antes de publicar.

```bash
python3 tools/check-rules.py
python3 tools/check-contrast.py
python3 tools/check-hero-contrast.py
```

Los dos primeros van con la librería estándar de Python y no hay nada que
instalar. El tercero necesita Pillow, porque tiene que abrir un JPEG.

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
calcula dos familias de contraste WCAG.

Textual (1.4.3, mínimo 4,5:1): texto principal, de cuerpo, atenuado, la plata
de acento, las dos paradas del titular con brillo, y las cuatro cosas que la
fila destacada pinta encima de su relleno de acero — título, subtítulo, flecha
y glifo. Esas cuatro se miden contra `--steel-lit` y no contra `--ink`, porque
es el único sitio de la página donde el texto no cae sobre negro.

No textual (1.4.11, mínimo 3:1): las tres paradas de `--grad-stroke` —el filo
metálico de las redes y de las filas de enlace— y el propio
relleno de la fila destacada contra el fondo, para que la fila se lea como un
bloque distinto y no solo tenga texto legible dentro. Todas contra `--ink`, que
es el vecino de fuera.

El filo de la fila destacada **no** está en la lista, y el script lo dice en un
comentario para que nadie lo "arregle": va en tinta sobre un relleno claro, así
que medirlo contra `--ink` no diría nada útil, y ahí el filo dejó de ser la
señal del control en cuanto la fila se rellenó.

Sale con código 1 si alguna pareja no llega a su mínimo.

**`check-hero-contrast.py`** hace lo que los otros dos no pueden: mide el
texto del hero contra la FOTO. Recorta `assets/img/jhei-hero.jpg` como lo haría
`object-fit: cover` con el `object-position` que declara el CSS, compone encima
las capas de `.hero__scrim` leyendo sus paradas del propio CSS, y busca el
píxel más claro de la banda donde cae el texto en once tamaños de pantalla, de
un móvil de 320 a un escritorio de 1920. Ese píxel es el peor caso y el único
que decide. Sale con código 1 si algún tamaño baja de 4,5:1.

Es la única comprobación que depende de un archivo de imagen, y por eso es la
única que hay que volver a correr **cuando se cambia la foto sin tocar una sola
línea de CSS**. Si Pillow no está instalada lo dice y se salta la
comprobación en vez de fallar: eso significa que un `check` verde sin Pillow
no prueba nada sobre el hero.

Los tres deben salir con código 0 antes de cualquier commit que toque CSS —y el
tercero, también antes de cualquier commit que toque la foto del hero.

Si algún día quieres subir o bajar la luz ambiente de golpe, los dos mandos
son `opacity` en `.backdrop__glow` y en `.backdrop__glyphs`, dentro de la
sección 3 de `styles.css`.

---

## Decisiones que conviene conocer antes de tocar el CSS

**El decorado es neutro para que la jerarquía signifique algo.** Hubo cuatro
versiones antes de esta, y las cuatro fallaron por el mismo sitio: las filas en
degradado de fuego a todo lo ancho, el fuego repartido en filos y titulares, el
teal y el verde marcando talleres, y una brasa naranja rellenando la destacada.

La regla que quedó: **el decorado en gris, y una sola pieza distinta en toda la
página.** Hoy esa pieza es la primera fila, y se distingue por LUZ, no por
matiz. El día que se destaquen dos, dejará de funcionar.

**Destacar invirtiendo el valor es más fuerte y más barato que destacar con
color.** Un relleno de color obliga a elegir entre bajarle mucho la luz o poner
el texto en negro: blanco sobre el dorado `#FFC252` mide 1,54:1 y sobre el
naranja de marca 2,40:1, los dos fallos graves. El naranja que hubo aquí acabó
al 36% de luz para sostener texto blanco, y aun así el relleno solo daba 3,13:1
contra el fondo, con el mínimo en 3.

El acero claro no tiene ese problema: 14,03:1 contra el fondo y 14,03:1 con el
texto en tinta. En una página oscura, un bloque claro es la señal más fuerte
que hay, y no gasta ni un color.

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

**Se quitan filos donde son decoración, no donde son affordance.** El hero
perdió el suyo al pasar a ocupar casi la ventana: dejó de tener bordes que
rematar — su límite inferior es un degradado que se disuelve y los otros tres
son el filo de la pantalla. Las filas de vidrio lo conservan porque ahí el filo
sí separa el bloque del fondo.

**Las nueve cards de colaboraciones son el caso intermedio, y tardaron dos
intentos.** Perdieron el trazo en degradado por una razón buena —una foto ya
trae su propio límite, y nueve filos metálicos seguidos son nueve líneas
compitiendo con nueve fotos— pero acabaron siendo lo ÚNICO de la página sin
ningún filo, y se leían como piezas sueltas.

Ahora llevan un **filo de pelo**: blanco al 10%, no el trazo en degradado. Las
ata al sistema sin volver al problema original. Va como sombra INTERIOR y no
como `border`, y la diferencia importa en una tarjeta con foto: un `border`
ocupa sitio y encogería la imagen o le rompería la proporción 3/4, mientras que
un `inset` se pinta encima siguiendo el `border-radius` exacto, sin tocar el
layout.

La lección que dejó: **una decisión de quitar algo puede seguir siendo correcta
y volverse incorrecta si cambia lo que hay alrededor.** El filo de las cards se
quitó cuando la página tenía menos filos; al ganar baldosas, discos y aros, la
excepción empezó a leerse como un olvido.

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

- [x] Las URLs cambiadas y sus `data-todo` borrados
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
- El hero ocupa el 70% de la ventana y su degradado inferior empalma con los
  botones sin costura visible — comprobado a 1470 × 687 con zoom sobre el borde,
  y el recorte de la foto a 320, 360, 390, 430, 768, 834, 960, 1024, 1280, 1440
  y 1920 componiendo los píxeles reales (`tools/check-hero-contrast.py`)
- El titular de los enlaces entra en una línea y la primera fila asoma sobre el
  pliegue: 92% de la fila a 1470 × 687, 120% a 390 × 844 y 70% a 360 × 640
- Las tres cifras arrancan en el mismo píxel que el titular del hero (215px a
  1470) y terminan en el 49,5% del ancho, dentro del 62% que el velo mantiene
  opaco; en móvil se centran y caben sin scroll a 390 y 360
- La bio está fuera del DOM (comentada) y las tres redes siguen ahí: 3 enlaces
- El reflejo del chip gira de verdad: `--chip-angle` leído dos veces con cuatro
  segundos de diferencia da 207,7° y 305,9°, y el brillo se ve pasar del borde
  inferior al superior en dos capturas
- El titular del hero entra por el 14,63% del ancho y su mayúscula ocupa el
  3,67% — la referencia gráfica marca 14,55% y 3,65%. Medido sobre el DOM y con
  la letra dibujada en un `<canvas>`, no sobre una captura escalada
- El titular cabe en UNA línea de 320 a 1920 px: en su peor caso mide 369 px
  contra un tope de 448, y en el más estrecho 175 px contra 280 disponibles
- Cero errores de consola procedentes de la página
- Un solo `<h1>`; recorrido de tabulación completo: saltar al contenido →
  2 filas → cinta de tarjetas de colaboraciones → botón de pausa de la cinta →
  3 redes
- Anillo de foco de dos tonos visible en todo lo interactivo
- Los iconos y las flechas se renderizan al tamaño previsto
- Una sola fila lleva `row--featured`, va PRIMERA, y cero llevan los
  modificadores de taller retirados — comprobado contando en el DOM
- Los elementos de la fila invertida resuelven a tinta EN REPOSO Y EN HOVER:
  título, subtítulo, ranura, flecha, glifo, marca de agua y sus tonos
  encendidos — el estado de reposo leyendo el estilo computado, y el hover con
  el ratón encima de verdad, que es la única forma de cazar el fallo del glifo
  blanco sobre fondo blanco
- El isotipo de AIVI resuelve `fill="currentColor"` con sus cinco paths, y su
  marca de agua comparte `viewBox` con el glifo
- Las marcas de agua quedan recortadas dentro de su píldora, y los
  cuatro `<use>` apuntan a un `<g id>` que existe y es único
- La ranura cae en la columna 3 en escritorio y bajo el texto a 390 y 360 px
- Las esquinas resuelven a `12px 36px 24px 24px` y la baldosa a 48 px en móvil
  y 54 en escritorio, con el glifo fijo en 24 — leyendo el estilo computado
- Contraste del texto secundario de las filas sobre su fondo de vidrio: 6,06:1
- Sin JavaScript la página se ve completa y todos los enlaces funcionan
- HTML + CSS + JS: 22 KB comprimidos

## Lo que queda pendiente de verificar en dispositivo real

- Fluidez del scroll en un Android de gama media
- `prefers-reduced-motion` con la preferencia activada en el sistema: el bloque
  está escrito y revisado, pero no se ha podido forzar la preferencia del
  sistema operativo desde aquí
