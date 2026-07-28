# Link in bio — Jhei Trujillo

Página única en HTML, CSS y JavaScript planos. Sin build, sin dependencias y sin
ninguna petición a servidores de terceros. Se sube tal cual a cualquier hosting
(Netlify, Vercel, GitHub Pages, cPanel) y funciona.

Línea gráfica heredada de la guía de AIVI, **sin usar el logo ni el isotipo de
AIVI**: solo su paleta, su tipografía (Hanken Grotesk) y su lenguaje visual.

Versión sobria: la página es casi monocroma. El negro y el blanco hacen el
trabajo y el fuego de AIVI aparece solo en el aro del avatar, la baldosa de cada
icono, el filete ornamental, el filo de las cards y el titular de
colaboraciones.

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

Todo el contenido editable está en `index.html`. Los sitios pendientes llevan el
atributo `data-todo`, así que los localizas todos de golpe:

```bash
grep -n 'data-todo' index.html
```

### 1 · Los tres enlaces

| Fila | Línea del HTML | Qué poner |
|---|---|---|
| **Talleres con IA** | `href="#reemplazar-url-talleres"` | La URL de tu página de talleres o del formulario de lista de espera |
| **Conoce AIVI** | ya apunta a `https://aivi.chat` | Nada, salvo que cambie el dominio |
| **Escríbeme** | `href="#reemplazar-url-whatsapp"` | `https://wa.me/NUMERO?text=Hola%20Jhei%2C%20vengo%20de%20tu%20link%20in%20bio.%20Quiero%20hablar%20sobre` |

El número de WhatsApp va con código de país y sin `+` ni espacios. El mensaje
precargado se deja con la frase abierta a propósito: obliga a la persona a
escribir su tema y eso sube mucho la calidad de la conversación.

Al sustituir cada URL, **borra también el atributo `data-todo`** de ese enlace.

**Para añadir una cuarta fila**, duplica un `<a class="row">` entero. Solo hay
que ajustar una cosa más: los retardos de la animación de entrada están en
`css/styles.css`, buscando `.row:nth-child(`. Añade un bloque más siguiendo el
patrón (+70 ms respecto al anterior).

### 2 · La fila destacada

La clase `row--primary` es la que le pone borde dorado y resplandor a una fila.
Ahora la lleva **Talleres con IA**. Muévela a la fila que quieras destacar —
debería llevarla una sola: si todas gritan, ninguna guía.

### 3 · Los iconos

Cada fila lleva su icono como SVG dentro del HTML, así que no hay archivos que
gestionar ni peticiones extra. Son de trazo, 24×24, con juntas redondeadas para
que hablen el mismo idioma que la geometría de AIVI.

| Fila | Icono actual |
|---|---|
| Talleres | Birrete de graduación |
| AIVI | Chispa doble (IA) |
| WhatsApp | Bocadillo de conversación |

Para cambiar uno, sustituye el contenido de su `<svg>` por otro path. Mantén el
`viewBox="0 0 24 24"`, `fill="none"` y `stroke="currentColor"`: el color y el
tamaño los pone el CSS, así que el icono nuevo hereda todo automáticamente.

### 4 · La insignia "Disponible"

Es el `<span class="hero__status">` del hero. Si en algún momento no aplica,
**borra ese `<span>` entero** y no hay que tocar nada más.

### 5 · Las redes

Tres enlaces al final del HTML: TikTok, Instagram y YouTube. Cambia el `href` y
deja el `aria-label` como está — es lo que lee un lector de pantalla.

### 6 · Los datos de la bio

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

Seis cards de ejemplo en el carrusel. Para cada una: cambia el `src` de la
imagen, el `alt` y el texto de `collab__brand`. Para añadir o quitar cards,
duplica o borra un `<li class="collab">` entero — los puntos de paginación se
generan solos, no hay que tocar nada más.

**Pide permiso de uso de imagen a cada persona o marca antes de publicarla.**

---

## Las imágenes

Todas son **placeholders generados en la línea gráfica de AIVI**. Cada una está
en la ruta y el tamaño definitivos, así que basta con sobrescribir el archivo: no
hay que tocar el HTML.

| Archivo | Tamaño | Notas |
|---|---|---|
| `assets/img/jhei-avatar.png` | 480 × 480 | **La imagen principal de la página.** Cuadrada, rostro centrado, con algo de aire arriba: se recorta a círculo. |
| `assets/img/collab-1…6.png` | 420 × 640 (5:8) | El blanco y negro lo hace el CSS, así que da igual si las entregas en color. |
| `assets/img/og-image.png` | 1200 × 630 | Lo que se ve al compartir el enlace en redes. |
| `assets/img/favicon.svg` | — | El icono de la pestaña. |

Ya no hay retrato grande ni mockups de dispositivo: la estructura con avatar
circular y filas con icono no los usa.

Para regenerar los placeholders (por ejemplo si cambias la paleta):

```bash
python3 tools/make-placeholders.py
```

---

## Estructura

```
index.html            todo el contenido editable
css/tokens.css        color, tipografía, espaciado, movimiento — la marca entera
css/styles.css        layout y componentes; solo consume tokens
js/main.js            revelado al scroll, carrusel, año del footer
assets/fonts/         Hanken Grotesk variable 100–900, auto-hospedada (56 KB)
assets/img/           imágenes, favicon
tools/                generador de placeholders
docs/brand/           la línea gráfica de AIVI extraída del PDF, con referencias
docs/design/          especificaciones de UI, arquitectura CSS, movimiento y copy
docs/superpowers/     el documento de diseño aprobado
```

**Para cambiar un color de toda la página se toca un solo archivo:**
`css/tokens.css`. `styles.css` no contiene ni un hex ni un valor de espaciado
suelto.

Si algún día quieres subir o bajar el color de golpe, los dos mandos son
`opacity` en `.backdrop__glow` y en `.backdrop__glyphs`, dentro de la sección 3
de `styles.css`.

---

## Decisiones que conviene conocer antes de tocar el CSS

**Los enlaces son filas de vidrio, no botones de color.** Hubo una versión
anterior con tarjetas de degradado de fuego a todo lo ancho. Funcionaba, pero
saturaba la página: tres bloques naranjas seguidos dejan sin jerarquía a todo lo
demás. Las filas oscuras con el icono cálido consiguen el mismo peso visual con
una fracción del color, y el resplandor dorado de `row--primary` es suficiente
para señalar cuál importa más.

**Si algún día vuelves a un botón de fuego, su texto tiene que ser negro.**
Blanco sobre el dorado `#FFC252` mide 1,60:1 de contraste — un fallo grave de
accesibilidad. Negro sobre el degradado mide 5,50:1 en el extremo rojo y 11,86:1
en el dorado.

**Ni el aro del avatar ni el titular de colaboraciones llevan rojo.** Los dos
degradados van de naranja a dorado. Con el rojo dentro, esos dos elementos eran
lo más saturado de la página y rompían el registro casi monocromo.

**El carrusel no gira solo.** Contenido en movimiento de más de cinco segundos
exige un control de pausa (WCAG 2.2.2), y aquí no aportaba nada: deslizar, los
puntos y las flechas del teclado ya son la navegación completa.

**`overflow-x: clip` está en `html`, no solo en `body`.** Solo el elemento raíz
propaga su overflow al viewport. Con la regla únicamente en `body`, la geometría
del fondo generaba 50 px de desplazamiento horizontal real en móvil.

**Los títulos de las filas van en caja baja.** A ese tamaño, tres títulos
seguidos en mayúsculas de peso 900 pedían más atención que el titular de la
página y volvían pesada la lectura. Las mayúsculas quedan para el nombre, el
subtítulo y los encabezados de sección.

---

## Antes de publicar

- [ ] Las tres URLs cambiadas y sus `data-todo` borrados
- [ ] Los tres perfiles de redes cambiados
- [ ] Los cuatro datos de la bio rellenados, o la frase reescrita sin ellos
- [ ] Decidido si la insignia "Disponible" se queda
- [ ] Confirmado que respondes tú el WhatsApp (o cambiado el texto)
- [ ] Las imágenes reales sustituidas, con permiso de uso de las colaboraciones
- [ ] `grep -n 'data-todo\|reemplazar-url\|class="tbd"' index.html` no devuelve nada
- [ ] Probada en un móvil de verdad, no solo en el navegador de escritorio

---

## Comprobado en el navegador

- Sin scroll horizontal a 390 px ni a 1440 px (medido con `scrollTo`, no a ojo)
- Cero errores de consola procedentes de la página
- Un solo `<h1>`; recorrido de tabulación completo: saltar al contenido →
  3 filas → carrusel → punto activo → 3 redes
- Anillo de foco de dos tonos visible en todo lo interactivo
- Un único punto tabulable en el grupo de puntos del carrusel
- Los tres iconos y las tres flechas se renderizan al tamaño previsto
- Contraste del texto secundario de las filas sobre su fondo de vidrio: 6,06:1
- Sin JavaScript la página se ve completa y todos los enlaces funcionan
- HTML + CSS + JS: 22 KB comprimidos

## Lo que queda pendiente de verificar en dispositivo real

- Fluidez del scroll en un Android de gama media
- `prefers-reduced-motion` con la preferencia activada en el sistema: el bloque
  está escrito y revisado, pero no se ha podido forzar la preferencia del
  sistema operativo desde aquí
