# Copy final — Link in bio · Jhei Trujillo

Español neutro LatAm. Voz activa, frases cortas, cero relleno.
Todo lo de abajo está listo para pegar. Las decisiones ya están tomadas: donde hay
`ALT` es una alternativa opcional, nunca una tarea pendiente.
Los marcadores tipo `[ASÍ]` están listados al final del documento.

---

## 1. Hero

**Nombre (H1)**

```
JHEI TRUJILLO
```

**Subtítulo (bajo el nombre) — 47 caracteres**

```
Viralidad · Creación de contenido · IA aplicada
```

> `ALT` (59 caracteres, versión larga):
> `Viralidad · Creación de contenido · Inteligencia Artificial`

Por qué esta y no la base: "IA aplicada" dice que la usa para producir, no que le
interesa el tema. Y ahorra 12 caracteres, que en móvil se traducen en una sola línea
con tipografía más grande.

**Nota de diseño:** última unidad (`IA aplicada`) en el degradado de fuego; las dos
primeras en blanco. Los separadores `·` al 60 % de opacidad.

---

## 2. Botones CTA

Orden en pantalla: Talleres → AIVI → WhatsApp.
Va de "aprende conmigo" a "usa mi producto" a "hablemos". De menor a mayor compromiso
sin cortar la lectura.

### Botón 1 — Talleres

| Elemento | Texto | Caracteres |
|---|---|---|
| Título | `TALLERES CON IA` | 15 / 22 |
| Microcopy | `Mira el próximo taller y cómo entrar` | 36 / 45 |

> `ALT` título: `FORMACIONES EN IA` (17)

Destino: `[URL_TALLERES]`

### Botón 2 — AIVI

| Elemento | Texto | Caracteres |
|---|---|---|
| Título | `CONOCE AIVI` | 11 / 22 |
| Microcopy | `Abre aivi.chat y mira cómo funciona` | 35 / 45 |

> `ALT` título: `ENTRA A AIVI` (12)

Destino: `https://aivi.chat`
El microcopy nombra el dominio a propósito: se queda en la memoria aunque la persona
no haga clic hoy.

### Botón 3 — WhatsApp

| Elemento | Texto | Caracteres |
|---|---|---|
| Título | `ESCRÍBEME` | 9 / 22 |
| Microcopy | `Te contesto yo por WhatsApp, no un bot.` | 39 / 45 |

> `ALT` título: `HABLEMOS` (8)

Destino: `[URL_WHATSAPP]` (formato `https://wa.me/[NUMERO]?text=...`)

**Mensaje precargado sugerido para el enlace de WhatsApp:**

```
Hola Jhei, vengo de tu link in bio. Quiero hablar sobre
```

Se deja la frase abierta a propósito: obliga a la persona a escribir su tema y eso
sube muchísimo la calidad de la conversación.

---

## 3. Título de la sección de colaboraciones

Dos líneas, en mayúsculas, centrado:

```
MARCAS Y CREADORES
CON LOS QUE HE TRABAJADO
```

> `ALT`:
> `CREADORES Y MARCAS`
> `QUE YA CONFIARON EN MÍ`

La autoridad la cargan las caras y los logos del carrusel, no el titular. Por eso el
texto es plano y factual: si el titular presume, la prueba social se debilita.

**Nota de diseño:** segunda línea en el degradado de fuego, primera en blanco.

---

## 4. Bio

**Bloque de identidad (sobre los párrafos)**

```
JHEI TRUJILLO
@[USUARIO_PRINCIPAL]
```

**Párrafo 1 — quién es y qué hace**

```
Soy Jhei Trujillo. Estudio por qué un video explota y otro no, y convierto esa
respuesta en pasos que cualquiera puede repetir. Creo contenido, enseño a crearlo
y construyo herramientas de IA para producirlo más rápido.
```

**Párrafo 2 — qué ha logrado y por qué le creen**

```
Llevo [AÑOS] años publicando en internet. Mis videos acumulan [VISTAS] vistas y he
formado a [ALUMNOS] personas en talleres y programas. Nada de lo que enseño es
teoría: lo pruebo primero en mis propias cuentas y recién después lo comparto.
```

**Párrafo 3 — su misión y a quién ayuda**

```
Mi misión es que nadie se quede invisible por no saber usar las herramientas que ya
tiene a mano. Ayudo a creadores, emprendedores y equipos de marketing a publicar con
constancia y a usar la IA como aliada, no como atajo. Tú traes la idea; yo te doy el
sistema.
```

El cierre del párrafo 3 conecta directo con el claim de AIVI ("convierte tus ideas en
contenido") sin repetirlo palabra por palabra. Prepara el clic al botón de AIVI incluso
si la persona bajó primero a leer la bio.

---

## 5. Microcopy de apoyo

### Indicador de scroll

| Elemento | Texto |
|---|---|
| Texto visible | `DESLIZA` |
| `aria-label` del botón/ancla | `Bajar a los enlaces` |

Si el indicador es solo la flecha sin texto, igual necesita el `aria-label`.

### Iconos de redes (`aria-label`)

| Icono | `aria-label` | Destino |
|---|---|---|
| TikTok | `Jhei Trujillo en TikTok` | `[URL_TIKTOK]` |
| Instagram | `Jhei Trujillo en Instagram` | `[URL_INSTAGRAM]` |
| YouTube | `Jhei Trujillo en YouTube` | `[URL_YOUTUBE]` |

Los tres enlaces con `target="_blank"` y `rel="noopener"`. Si el equipo quiere avisar
que se abre fuera, usar: `Jhei Trujillo en TikTok (abre en una pestaña nueva)`.

### Footer

Dos líneas, la de arriba más pequeña:

```
Sé visto. Sé recordado.
© [AÑO] Jhei Trujillo · Todos los derechos reservados
```

### `<title>` y `meta description`

```html
<title>Jhei Trujillo | Viralidad, creación de contenido e IA</title>
<meta name="description" content="Talleres de contenido con IA, mi sistema AIVI y contacto directo. Aprende a crear contenido que la gente ve, recuerda y comparte. Todo en un solo enlace.">
```

| Campo | Caracteres | Límite |
|---|---|---|
| `title` | 53 | ≤ 60 |
| `description` | 153 | ≤ 155 |

---

## 6. Open Graph

```html
<meta property="og:title" content="Jhei Trujillo — Viralidad, contenido e IA">
<meta property="og:description" content="Talleres, AIVI y contacto directo. Todo lo que hago para que tu contenido se vea y se recuerde.">
<meta property="og:image:alt" content="Jhei Trujillo sobre fondo negro con haces de luz naranja y dorada">
```

| Campo | Caracteres | Límite práctico |
|---|---|---|
| `og:title` | 41 | ≤ 60 |
| `og:description` | 95 | ≤ 110 (se corta en móvil) |

Mismos textos para Twitter/X (`twitter:title`, `twitter:description`) con
`twitter:card="summary_large_image"`.

---

## Marcadores que debe rellenar el cliente

Ninguna cifra, cliente, premio ni credencial de este documento está inventada. Todo lo
que requiere un dato real quedó como marcador:

| Marcador | Dónde aparece | Qué se necesita |
|---|---|---|
| `[AÑOS]` | Bio, párrafo 2 | Años publicando contenido (número entero) |
| `[VISTAS]` | Bio, párrafo 2 | Vistas acumuladas, redondeadas hacia abajo (ej. "más de 50 millones de") |
| `[ALUMNOS]` | Bio, párrafo 2 | Personas formadas en talleres/programas (número entero) |
| `[USUARIO_PRINCIPAL]` | Bloque de identidad de la bio | Handle sin `@` |
| `[URL_TALLERES]` | Botón 1 | Página de talleres o formulario de lista de espera |
| `[URL_WHATSAPP]` | Botón 3 | `https://wa.me/[NUMERO]?text=` + mensaje precargado |
| `[NUMERO]` | Enlace de WhatsApp | Número con código de país, sin `+` ni espacios |
| `[URL_TIKTOK]` | Iconos de redes | Perfil de TikTok |
| `[URL_INSTAGRAM]` | Iconos de redes | Perfil de Instagram |
| `[URL_YOUTUBE]` | Iconos de redes | Canal de YouTube |
| `[AÑO]` | Footer | Año en curso (2026) |
| `[LISTA_COLABORACIONES]` | Carrusel de colaboraciones | Nombre, foto y logo de cada persona/marca, **con permiso de uso** |

### Dos cosas para confirmar antes de publicar

1. **"Te contesto yo por WhatsApp, no un bot."** — solo se publica si Jhei responde
   personalmente. Si hay asistente o automatización, se cambia por
   `Cuéntame tu idea por WhatsApp` (30 caracteres).
2. **`[URL_TALLERES]`** — si en este momento no hay taller con fecha abierta, el
   microcopy del Botón 1 pasa a `Entra a la lista del próximo taller` (35 caracteres)
   para no prometer algo que la página no cumple.

### Si falta un dato de la bio

No se rellena con una cifra aproximada. Se reescribe la frase sin el número. Ejemplo
para el párrafo 2 sin `[VISTAS]` ni `[ALUMNOS]`:

```
Llevo [AÑOS] años publicando en internet y enseñando lo que aprendo en el camino.
Nada de lo que comparto es teoría: lo pruebo primero en mis propias cuentas y recién
después lo llevo a un taller.
```
