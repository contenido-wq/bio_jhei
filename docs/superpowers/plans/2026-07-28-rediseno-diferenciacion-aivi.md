# Rediseño de diferenciación AIVI — Plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Que el link-in-bio de Jhei Trujillo deje de ser reconocible como derivado de la página de Jhonny Lubo y pase a leerse como familia de `aivi.chat`, sin degradar ninguna garantía técnica ya conseguida.

**Architecture:** Página estática de tres archivos (`index.html`, `css/tokens.css` + `css/styles.css`, `js/main.js`), sin build y sin dependencias. `tokens.css` es la fuente única de valores literales; `styles.css` solo los consume. El rediseño se hace por capas: primero el arnés de verificación, luego los tokens, luego cada componente. El trazo en degradado se construye con pseudo-elementos enmascarados (`mask-composite: exclude`) porque `border-image` ignora el `border-radius`.

**Tech Stack:** HTML5, CSS3 (custom properties, `mask-composite`, `scroll-snap`), JavaScript ES5 sin módulos, Python 3 (librería estándar) para los placeholders y los scripts de verificación.

**Spec:** `docs/superpowers/specs/2026-07-28-rediseno-diferenciacion-aivi-design.md`

**Línea base:** commit `a3cf4d6`. Para descartar todo el rediseño: `git reset --hard a3cf4d6`.

## Global Constraints

Estas reglas aplican a **todas** las tareas. Están tomadas literalmente del spec y de las cabeceras de los archivos existentes.

- **Cero dependencias, cero build, cero módulos ES.** `js/main.js` debe seguir funcionando abriendo `index.html` directamente desde disco.
- **Cero peticiones a terceros.** Ninguna fuente, script, imagen ni hoja de estilo externa.
- **`styles.css` no contiene ni un hex de marca ni un valor de espaciado literal.** Todo sale de `tokens.css`. Las excepciones se marcan con la palabra `EXCEPCION` y su motivo, en comentario, en la línea anterior.
- **Cero `text-transform: uppercase`** salvo en `.hero__status` (micro-insignia <11px). Es la única excepción permitida.
- **Cero capas GPU nuevas en el fondo.** Ninguna regla bajo `.backdrop` puede llevar `will-change` ni `translateZ(0)`.
- **Solo se animan `transform` y `opacity`.** Nunca `width`, `height`, `left`, `margin` ni `background-image`.
- **Contraste:** todo texto ≥4.5:1. Un trazo que sea la única señal de que algo es un control, ≥3:1 (WCAG 1.4.11).
- **Todo `@media (hover: hover) and (pointer: fine)`.** Fuera de ese guard, Android e iOS dejan el hover pegado tras el primer tap.
- **Idioma:** todos los comentarios de código y el copy visible, en español.
- **Cada tarea termina en commit.** Mensajes en español, en imperativo.

**Comandos que se repiten en varias tareas:**

```bash
# Arnés de verificación (creado en la Tarea 1)
python3 tools/check-rules.py
python3 tools/check-contrast.py

# Servidor local para verificación visual
python3 -m http.server 8080 --directory . &
# → http://localhost:8080
```

---

## Estructura de archivos

| Archivo | Responsabilidad | Tareas |
|---|---|---|
| `tools/check-rules.py` | **Nuevo.** Guardas estáticas sobre CSS y HTML: mayúsculas, hex de marca, `will-change` en el fondo, reserva de `mask-composite` | 1 |
| `tools/check-contrast.py` | **Nuevo.** Calcula ratios WCAG reales leyendo `tokens.css` | 1 |
| `tools/make-placeholders.py` | Añadir el retrato vertical 4:5 | 6 |
| `css/tokens.css` | Alta de los tokens de trazo, chip y cintas; baja del aro del avatar | 2, 6 |
| `css/styles.css` | Todo el trabajo visual | 3–9 |
| `index.html` | Estructura nueva: chips, hero asimétrico, cintas, botón de pausa | 4–9 |
| `js/main.js` | Sustituir el bloque `carousel` por `ribbons` | 8 |
| `assets/img/jhei-portrait.png` | **Nuevo.** Placeholder 4:5 | 6 |
| `docs/brand/aivi-brand-extract.md` | Corregir la instrucción de replicar la arquitectura del referente | 9 |
| `README.md` | Documentar el retrato 4:5 y el arnés de verificación | 9 |

---

## Tarea 1: Arnés de verificación

Sin esto, todo lo demás se verifica a ojo. Los dos scripts deben **fallar** contra el código actual: ahí está la prueba de que miden algo.

**Files:**
- Create: `tools/check-rules.py`
- Create: `tools/check-contrast.py`

**Interfaces:**
- Consumes: nada.
- Produces: dos ejecutables que salen con código 0 (verde) o 1 (rojo) e imprimen cada comprobación con `OK` o `FALLA`. Todas las tareas siguientes los usan como criterio de aceptación.

- [ ] **Step 1: Escribir `tools/check-contrast.py`**

```python
#!/usr/bin/env python3
"""Verifica los contrastes WCAG declarados en css/tokens.css.

Lee los valores REALES del archivo, nunca copias hardcodeadas: si alguien
cambia un token, este script se entera. Solo librería estándar.

Uso:  python3 tools/check-contrast.py
Sale con 1 si alguna pareja incumple su mínimo.
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKENS = os.path.join(ROOT, "css", "tokens.css")

# (descripción, token del texto, token del fondo, mínimo exigido)
# El fondo tiene que ser OPACO: es contra lo que se compone el alpha del texto.
CHECKS = [
    ("texto principal sobre el fondo", "--text-primary", "--ink", 4.5),
    ("texto de cuerpo sobre el fondo", "--text-body", "--ink", 4.5),
    ("texto atenuado sobre el fondo", "--text-muted", "--ink", 4.5),
    ("dorado sobre el fondo", "--text-gold", "--ink", 4.5),
    ("naranja sobre el fondo", "--text-orange", "--ink", 4.5),
    ("texto sobre el relleno, extremo rojo", "--text-on-fire", "--fire-red", 4.5),
    ("texto sobre el relleno, extremo naranja", "--text-on-fire", "--fire-orange", 4.5),
    ("texto sobre el relleno, extremo dorado", "--text-on-fire", "--fire-gold", 4.5),
    ("subtítulo sobre el relleno, extremo rojo", "--text-on-fire-soft", "--fire-red", 4.5),
    ("subtítulo sobre el relleno, extremo dorado", "--text-on-fire-soft", "--fire-gold", 4.5),
]


def read_source():
    with open(TOKENS, encoding="utf-8") as fh:
        return fh.read()


def raw_token(src, name):
    """Devuelve el valor declarado de un token, sin resolver."""
    m = re.search(r"^\s*" + re.escape(name) + r"\s*:\s*([^;]+);", src, re.M)
    return m.group(1).strip() if m else None


def resolve(src, name, depth=0):
    """Resuelve un token a (r, g, b, alpha). Sigue indirecciones var().

    Formatos soportados, que son los únicos que usa el proyecto:
      #rrggbb
      var(--otro)
      rgb(var(--rgb-x) / NN%)
    """
    if depth > 8:
        raise ValueError("indirección de var() demasiado profunda en " + name)

    value = raw_token(src, name)
    if value is None:
        raise KeyError("token no encontrado en tokens.css: " + name)

    m = re.fullmatch(r"#([0-9a-fA-F]{6})", value)
    if m:
        h = m.group(1)
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 1.0)

    m = re.fullmatch(r"var\((--[\w-]+)\)", value)
    if m:
        return resolve(src, m.group(1), depth + 1)

    m = re.fullmatch(r"rgb\(\s*var\((--[\w-]+)\)\s*/\s*([\d.]+)%\s*\)", value)
    if m:
        comps = raw_token(src, m.group(1))
        if comps is None:
            raise KeyError("token de componentes no encontrado: " + m.group(1))
        parts = [int(p) for p in comps.split()]
        return (parts[0], parts[1], parts[2], float(m.group(2)) / 100.0)

    raise ValueError("formato no soportado en " + name + ": " + value)


def to_linear(channel):
    c = channel / 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def luminance(rgb):
    r, g, b = (to_linear(c) for c in rgb[:3])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def composite(fg, bg):
    """Compone fg (con alpha) sobre bg opaco. Sin redondear: el navegador
    tampoco redondea a enteros antes de calcular el contraste."""
    a = fg[3]
    return tuple(a * fg[i] + (1 - a) * bg[i] for i in range(3))


def contrast(fg, bg):
    lo, hi = sorted((luminance(fg), luminance(bg)))
    return (hi + 0.05) / (lo + 0.05)


def main():
    src = read_source()
    failures = 0
    print("Contraste WCAG · css/tokens.css\n")

    for label, fg_name, bg_name, minimum in CHECKS:
        try:
            fg = resolve(src, fg_name)
            bg = resolve(src, bg_name)
        except (KeyError, ValueError) as err:
            print("  FALLA  %-44s  %s" % (label, err))
            failures += 1
            continue

        if bg[3] != 1.0:
            print("  FALLA  %-44s  el fondo %s no es opaco" % (label, bg_name))
            failures += 1
            continue

        ratio = contrast(composite(fg, bg), bg)
        ok = ratio >= minimum
        print("  %-5s  %-44s  %5.2f:1  (mínimo %.1f)"
              % ("OK" if ok else "FALLA", label, ratio, minimum))
        if not ok:
            failures += 1

    print("")
    if failures:
        print("%d comprobación(es) de contraste FALLAN." % failures)
        return 1
    print("Todos los contrastes cumplen.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Ejecutarlo para verificar que falla**

Run: `python3 tools/check-contrast.py`

Expected: FALLA. Las dos líneas de `--text-on-fire-soft` salen con
`token no encontrado en tokens.css: --text-on-fire-soft`, porque ese token se
crea en la Tarea 2. El resto sale OK — eso confirma que el cálculo es correcto
contra los valores ya medidos en los comentarios de `tokens.css`
(5.50:1 sobre el rojo, 7.59:1 sobre el naranja, 11.86:1 sobre el dorado).

Si alguna de esas tres NO coincide con el comentario del archivo, la fórmula
está mal y hay que arreglarla antes de seguir.

- [ ] **Step 3: Escribir `tools/check-rules.py`**

```python
#!/usr/bin/env python3
"""Guardas estáticas del sistema de diseño.

Cuatro reglas que el rediseño no puede romper. Solo librería estándar.

Uso:  python3 tools/check-rules.py
Sale con 1 si alguna regla se incumple.
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STYLES = os.path.join(ROOT, "css", "styles.css")

# Único selector donde se permite la mayúscula sostenida: la micro-insignia
# "Disponible", por debajo de 11px. Mismo criterio que MÁS POPULAR en aivi.chat.
UPPERCASE_ALLOWED = ".hero__status"

# Los cinco colores de marca. styles.css los consume por token, nunca por hex.
BRAND_HEXES = ["#101010", "#fafafa", "#ff413b", "#fe803f", "#ffc252"]


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def enclosing_selector(lines, index):
    """Último selector abierto antes de la línea `index` (0-based)."""
    for i in range(index, -1, -1):
        stripped = lines[i].strip()
        if stripped.endswith("{"):
            return stripped[:-1].strip()
    return "(desconocido)"


def rule_uppercase(src):
    """1 · Cero mayúscula sostenida fuera de la excepción declarada."""
    lines = src.splitlines()
    offenders = []
    for i, line in enumerate(lines):
        if "text-transform" not in line or "uppercase" not in line:
            continue
        selector = enclosing_selector(lines, i)
        if UPPERCASE_ALLOWED not in selector:
            offenders.append("línea %d, selector %s" % (i + 1, selector))
    return offenders


def rule_no_brand_hex(src):
    """2 · Ningún hex de marca literal en styles.css."""
    offenders = []
    for i, line in enumerate(src.splitlines()):
        low = line.lower()
        for hex_value in BRAND_HEXES:
            if hex_value in low:
                offenders.append("línea %d contiene %s" % (i + 1, hex_value))
    return offenders


def rule_backdrop_no_gpu(src):
    """3 · Ninguna capa del fondo pide capa GPU propia."""
    lines = src.splitlines()
    offenders = []
    for i, line in enumerate(lines):
        low = line.lower()
        if "will-change" not in low and "translatez(0)" not in low:
            continue
        selector = enclosing_selector(lines, i)
        if ".backdrop" in selector:
            offenders.append("línea %d, selector %s" % (i + 1, selector))
    return offenders


def rule_mask_fallback(src):
    """4 · Si se usa mask-composite, existe su reserva @supports."""
    if "mask-composite" not in src:
        return []
    has_fallback = re.search(
        r"@supports\s+not\s*\(\(?\s*(-webkit-)?mask-composite", src
    )
    if has_fallback:
        return []
    return ["se usa mask-composite sin bloque @supports not de reserva"]


RULES = [
    ("Cero mayúscula sostenida (salvo %s)" % UPPERCASE_ALLOWED, rule_uppercase),
    ("Cero hex de marca literal en styles.css", rule_no_brand_hex),
    ("Cero capas GPU propias en el fondo", rule_backdrop_no_gpu),
    ("Reserva @supports para mask-composite", rule_mask_fallback),
]


def main():
    src = read(STYLES)
    failures = 0
    print("Reglas del sistema de diseño · css/styles.css\n")

    for label, check in RULES:
        offenders = check(src)
        if offenders:
            failures += 1
            print("  FALLA  %s" % label)
            for offender in offenders:
                print("           · %s" % offender)
        else:
            print("  OK     %s" % label)

    print("")
    if failures:
        print("%d regla(s) incumplida(s)." % failures)
        return 1
    print("Todas las reglas se cumplen.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Ejecutarlo para verificar que falla**

Run: `python3 tools/check-rules.py`

Expected: FALLA la regla 1 con exactamente cinco infractores — líneas 428
(`.hero__name`), 447 (`.hero__tagline`), 653 (`.collabs__title`), 825
(`.collab__brand`) y 1063 (`.foot__claim, .foot__legal`).

Las reglas 2, 3 y 4 deben salir OK contra el código actual. Si la 2 falla,
hay un hex de marca ya colado en `styles.css` y hay que reportarlo antes de
seguir, porque significa que la línea base ya incumplía su propia cabecera.

- [ ] **Step 5: Commit**

```bash
git add tools/check-rules.py tools/check-contrast.py
git commit -m "Añadir arnés de verificación de contraste y reglas de diseño"
```

---

## Tarea 2: Tokens del trazo en degradado

**Files:**
- Modify: `css/tokens.css` — bloque 3 (bordes) y bloque 5 (degradados)

**Interfaces:**
- Consumes: `--rgb-red`, `--rgb-orange`, `--rgb-gold`, `--rgb-ink`, `--fire-*`, `--fire-glare` (ya existen).
- Produces: `--grad-stroke`, `--grad-stroke-hot`, `--sw-stroke`, `--text-on-fire-soft`, `--ls-chip`, `--d-ribbon-text`, `--d-ribbon-cards`. Los consumen las tareas 4, 5, 6 y 8.

- [ ] **Step 1: Añadir los tokens de trazo al bloque 5 de `css/tokens.css`**

Insertar justo después del bloque `--grad-fire-hot` (alrededor de la línea 119):

```css
  /* ── Trazo en degradado ───────────────────────────────────────────────────
     El trazo se pinta con un pseudo-elemento enmascarado, NO con border-image:
     border-image ignora el border-radius y todas estas píldoras son redondas.
     El estado en reposo lleva alpha para que el trazo acompañe sin gritar; el
     caliente va a alpha plena y remata en el destello. */
  --grad-stroke: linear-gradient(135deg,
    rgb(var(--rgb-red) / 55%) 0%,
    rgb(var(--rgb-orange) / 75%) 46%,
    rgb(var(--rgb-gold) / 60%) 100%);

  --grad-stroke-hot: linear-gradient(135deg,
    var(--fire-red) 0%,
    var(--fire-orange) 42%,
    var(--fire-gold) 78%,
    var(--fire-glare) 100%);

  /* Fundido del canto inferior del retrato del hero: la tarjeta se disuelve en
     la página en vez de terminar en un corte recto. Hermano de
     --grad-collab-foot, y por el mismo motivo vive aquí y no en styles.css:
     styles.css no contiene valores de color literales. */
  --grad-portrait-foot: linear-gradient(to top,
    rgb(6 6 6 / 92%) 0%,
    rgb(6 6 6 / 46%) 52%,
    rgb(16 16 16 / 0%) 100%);
```

- [ ] **Step 2: Añadir el grosor del trazo al bloque 9 (radios), al final**

```css
  /* EXCEPCION: 1.5px queda fuera de la escala de 4px. Es el grosor mínimo al
     que un trazo en degradado se sigue leyendo COMO degradado a 1x; a 1px el
     antialiasing se come los stops intermedios y queda un borde naranja plano. */
  --sw-stroke: 1.5px;
```

- [ ] **Step 3: Añadir el token de texto sobre relleno al bloque 4**

Insertar inmediatamente después de `--text-on-fire` (alrededor de la línea 110):

```css
  /* Subtítulo sobre el relleno de fuego. Medido en el extremo ROJO (#FF413B),
     que es el peor punto del degradado: 4.67:1 — AA para texto normal. No
     bajar del 84%: al 82% cae a 4.54:1 y el margen desaparece.
     Lo verifica tools/check-contrast.py. */
  --text-on-fire-soft: rgb(var(--rgb-ink) / 84%);
```

- [ ] **Step 4: Añadir el tracking del chip al bloque 6**

Junto a los demás `--ls-*`:

```css
  --ls-chip: 0.01em;
```

- [ ] **Step 5: Añadir las duraciones de las cintas al bloque 11**

```css
  /* Cintas en bucle. Largas a propósito: por debajo de ~30s el movimiento
     compite con la lectura en lugar de acompañarla. */
  --d-ribbon-text: 38s;
  --d-ribbon-cards: 64s;
```

- [ ] **Step 6: Verificar el contraste**

Run: `python3 tools/check-contrast.py`

Expected: PASS, todas las líneas OK. En concreto:
- `subtítulo sobre el relleno, extremo rojo` → **4.67:1**
- `subtítulo sobre el relleno, extremo dorado` → aproximadamente 10.0:1

Si el extremo rojo no da 4.67:1, el token está mal escrito. No seguir.

- [ ] **Step 7: Commit**

```bash
git add css/tokens.css
git commit -m "Añadir tokens de trazo en degradado, chip y cintas"
```

---

## Tarea 3: Fin de la mayúscula sostenida

**Files:**
- Modify: `css/styles.css` — líneas 428, 447, 653, 825, 1063 y la regla `.hero__status` (línea 389)

**Interfaces:**
- Consumes: `--ls-chip` (Tarea 2).
- Produces: `styles.css` sin mayúscula sostenida fuera de `.hero__status`. La Tarea 4 sustituye `.hero__tagline` por el chip.

- [ ] **Step 1: Quitar la mayúscula de `.hero__name` (línea ~428)**

Borrar la línea `text-transform: uppercase;`. El nombre pasa a caja baja con peso 900. Sustituir además el comentario del bloque, que ya no describe lo que hace la regla:

```css
/* ── Nombre ────────────────────────────────────────────────────────────────
   Caja baja y peso 900. La mayúscula sostenida es un rasgo del referente, no
   de AIVI: en aivi.chat no hay un solo titular en versales. La jerarquía la
   carga el peso y el tracking negativo, no la caja. */
.hero__name {
  font-size: var(--fs-h1);
  font-weight: var(--fw-black);
  line-height: var(--lh-tight);
  letter-spacing: var(--ls-h1);
  color: var(--text-primary);
  text-wrap: balance;
}
```

(El `margin-block-start` y la alineación los reescribe la Tarea 6; aquí solo se
quita la caja.)

- [ ] **Step 2: Quitar la mayúscula de `.collabs__title` (línea ~653)**

Borrar `text-transform: uppercase;` y bajar el peso de `--fw-black` a
`--fw-bold`: a peso 900 en caja baja el titular pesa más que los enlaces, que
son lo que convierte.

- [ ] **Step 3: Quitar la mayúscula de `.collab__brand` (línea ~825)**

Borrar `text-transform: uppercase;`, cambiar `--fw-black` por `--fw-bold` y
`--ls-wide` por `--ls-none`: el tracking abierto solo tiene sentido en versales.

- [ ] **Step 4: Quitar la mayúscula del footer (línea ~1063)**

En `.foot__claim, .foot__legal`: borrar `text-transform: uppercase;` y cambiar
`--ls-wider` por `--ls-none`. Subir `--fs-micro` a `--fs-small`: en caja baja,
13px con tracking abierto se lee peor que 15px sin él.

En `.foot__claim`, cambiar `--fw-bold` por `--fw-semi`.

- [ ] **Step 5: Documentar la excepción en `.hero__status` (línea ~389)**

Añadir al comentario existente del bloque:

```css
/* ── Insignia de disponibilidad ─────────────────────────────────────────────
   Fondo opaco a propósito: se apoya sobre la foto y el texto tiene que leerse
   sin depender de lo que haya debajo.

   EXCEPCION — mayúscula sostenida. Es el ÚNICO sitio de la página donde se
   permite, porque va por debajo de 11px. Es el mismo criterio que AIVI aplica
   a MÁS POPULAR y SOLO LATAM en su bloque de precios. No replicar en ningún
   otro selector: lo vigila tools/check-rules.py. */
```

- [ ] **Step 6: Dejar `.hero__tagline` intacta de momento**

`.hero__tagline` (línea ~447) conserva su `text-transform: uppercase` **solo
hasta la Tarea 4**, que borra la regla entera y su marcado. Para que
`check-rules.py` pueda pasar ya en esta tarea, se borra aquí también la
declaración `text-transform: uppercase;` de `.hero__tagline`. La regla completa
desaparece en la Tarea 4.

- [ ] **Step 7: Verificar las reglas**

Run: `python3 tools/check-rules.py`

Expected: PASS. Las cuatro reglas en OK. Si la regla 1 sigue reportando algún
infractor, queda un `uppercase` sin quitar.

- [ ] **Step 8: Verificación visual**

```bash
python3 -m http.server 8080 --directory . &
```

Abrir `http://localhost:8080` y confirmar: nombre, subtítulo, titular de
colaboraciones, marca de cada card y footer están en caja baja. La insignia
"Disponible" sigue en versales.

- [ ] **Step 9: Commit**

```bash
git add css/styles.css
git commit -m "Eliminar la mayúscula sostenida salvo en la micro-insignia"
```

---

## Tarea 4: Componente chip

**Files:**
- Modify: `css/styles.css` — sección 2 (utilidades), añadir `.chip`; sección 5, borrar `.hero__tagline`
- Modify: `index.html` — sustituir `.hero__tagline` por un chip

**Interfaces:**
- Consumes: `--surface-glass`, `--border-soft`, `--sh-glass`, `--fs-small`, `--fw-medium`, `--ls-chip`, `--text-secondary`, `--grad-fire`.
- Produces: la clase `.chip`, que usan las tareas 6, 8 y 9. Marcado esperado: `<p class="chip">texto</p>` — el punto dorado lo pone el `::before`, no el HTML.

- [ ] **Step 1: Añadir `.chip` a la sección 2 de `css/styles.css`**

Insertar después del bloque `.fire-text` y su `@supports`:

```css
/* ── Chip-etiqueta ─────────────────────────────────────────────────────────
   Ocupa el lugar comunicativo que tenían las líneas en versales. Es el mismo
   recurso que AIVI usa antes de cada titular ("Tu agencia de bolsillo",
   "Planes AIVI", "FAQ"). Caja baja siempre.

   El punto dorado va como ::before y no en el marcado: es decoración pura y
   un lector de pantalla no debe anunciarlo. */
.chip {
  display: inline-flex;
  align-items: center;
  gap: var(--sp-2);
  padding: var(--sp-2) var(--sp-4);
  border-radius: var(--r-full);
  background-color: var(--surface-glass);
  border: 1px solid var(--border-soft);
  box-shadow: var(--sh-glass);
  font-size: var(--fs-small);
  font-weight: var(--fw-medium);
  line-height: var(--lh-normal);
  letter-spacing: var(--ls-chip);
  color: var(--text-secondary);
}

.chip::before {
  content: "";
  flex: none;
  width: 5px;
  height: 5px;
  border-radius: var(--r-full);
  background-image: var(--grad-fire);
}
```

- [ ] **Step 2: Borrar `.hero__tagline` de `css/styles.css`**

Eliminar la regla `.hero__tagline` completa y su regla hermana
`.hero__tagline span:not(:last-child)::after` (líneas ~438–455). El chip las
sustituye.

Eliminar también el bloque de movimiento `.hero__tagline { --delay; --dur;
--from-y; }` de la sección 10 (línea ~1109) y sustituirlo por el mismo bloque
apuntando a `.hero__chip`:

```css
.hero__chip {
  --delay: 210ms;
  --dur: 380ms;
  --from-y: 12px;
}
```

- [ ] **Step 3: Sustituir el marcado en `index.html`**

Reemplazar el bloque actual (líneas 89–91):

```html
    <p class="hero__tagline" data-enter>
      <span>Viralidad</span><span>Creación de contenido</span><span>IA aplicada</span>
    </p>
```

por:

```html
    <p class="chip hero__chip" data-enter>Viralidad · Contenido · IA aplicada</p>
```

- [ ] **Step 4: Verificación visual**

Abrir `http://localhost:8080`. Esperado: donde había tres palabras en versales
doradas separadas por puntos, ahora hay una píldora de vidrio con un punto
dorado a la izquierda y el texto en caja baja. La animación de entrada del chip
sigue ocurriendo a los 210ms, igual que antes.

- [ ] **Step 5: Verificar las reglas**

Run: `python3 tools/check-rules.py`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add css/styles.css index.html
git commit -m "Añadir el chip-etiqueta y retirar la tagline en versales"
```

---

## Tarea 5: Trazo en degradado y jerarquía de botones

El núcleo del pedido del cliente. Es la tarea más delicada del plan.

**Files:**
- Modify: `css/styles.css` — sección 6 completa; sección 11 (`prefers-contrast`, `forced-colors`)
- Modify: `index.html` — clases de las tres filas

**Interfaces:**
- Consumes: `--grad-stroke`, `--grad-stroke-hot`, `--sw-stroke`, `--text-on-fire`, `--text-on-fire-soft`, `--grad-fire`, `--grad-fire-hot`, `--sh-fire` (Tarea 2 y tokens existentes).
- Produces: la utilidad `.stroke`, reutilizada por las tareas 6 y 8 en la tarjeta del retrato, las cards de colaboración y los círculos de redes. Contrato: `.stroke` exige que el elemento tenga `border-radius` propio (el pseudo hereda con `border-radius: inherit`).

- [ ] **Step 1: Añadir la utilidad `.stroke` a la sección 2 de `css/styles.css`**

```css
/* ── Trazo en degradado ────────────────────────────────────────────────────
   border-image queda descartado: ignora el border-radius, y todas las píldoras
   de esta página son redondas. La construcción es un pseudo-elemento con dos
   máscaras compuestas en `exclude`, que recorta el centro y deja solo el filo.

   Son DOS pseudos, no uno: el ::before es el trazo en reposo y el ::after el
   caliente, en opacity 0. Cruzar por opacidad es lo único que el compositor
   resuelve sin repintar el degradado en cada frame — cambiar background-image
   en :hover repintaría el filo completo 60 veces por segundo.

   z-index -1 con isolation:isolate en el padre: el pseudo se pinta por encima
   del fondo del elemento y por debajo de su contenido. */
.stroke {
  position: relative;
  isolation: isolate;
}

.stroke::before,
.stroke::after {
  content: "";
  position: absolute;
  inset: 0;
  z-index: -1;
  border-radius: inherit;
  padding: var(--sw-stroke);
  pointer-events: none;
  -webkit-mask:
    linear-gradient(#000 0 0) content-box,
    linear-gradient(#000 0 0);
  -webkit-mask-composite: xor;
  mask:
    linear-gradient(#000 0 0) content-box,
    linear-gradient(#000 0 0);
  mask-composite: exclude;
}

.stroke::before {
  background-image: var(--grad-stroke);
}

.stroke::after {
  background-image: var(--grad-stroke-hot);
  opacity: 0;
  transition: opacity var(--d-out) var(--e-fade);
}

.stroke.is-hot::after,
.stroke:focus-visible::after {
  opacity: 1;
  transition-duration: var(--d-fast);
}

@media (hover: hover) and (pointer: fine) {
  .stroke:hover::after {
    opacity: 1;
    transition-duration: var(--d-fast);
  }
}

/* Reserva obligatoria. Sin composición de máscara no hay trazo en degradado:
   se cae al borde dorado plano, que es exactamente lo que la página tenía
   antes de este rediseño. Nadie ve una caja rota. */
@supports not ((mask-composite: exclude) or (-webkit-mask-composite: xor)) {
  .stroke::before,
  .stroke::after {
    display: none;
  }

  .stroke {
    border: 1px solid var(--border-gold);
  }
}
```

- [ ] **Step 2: Reescribir `.row` en la sección 6 de `css/styles.css`**

Sustituir la regla `.row` actual (líneas ~495–515). Cambia: desaparece el
`border` plano y el `background-image: var(--grad-row)` se conserva solo en las
filas de trazo.

```css
.row {
  position: relative;
  isolation: isolate;
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: var(--sp-4);
  padding: var(--sp-4);
  border-radius: var(--r-cta);
  background-color: var(--surface-row);
  background-image: var(--grad-row);
  box-shadow: var(--sh-glass);
  color: var(--text-primary);
  touch-action: manipulation;

  /* Asimetría de ignición: la salida (aquí, en la base) es la lenta, como una
     brasa que se apaga. La entrada corta vive en :hover. */
  transition: transform var(--d-out) var(--e-glide),
    background-color var(--d-out) var(--e-fade),
    box-shadow var(--d-out) var(--e-fade);
}
```

- [ ] **Step 3: Reescribir `.row--primary` como fila de relleno**

Sustituir la regla actual (líneas ~518–521):

```css
/* ── Fila destacada: relleno de fuego ──────────────────────────────────────
   Debería llevarla una sola fila: si todas gritan, ninguna guía.

   El texto va en NEGRO, no en blanco. Blanco sobre #FFC252 da 1.54:1, un fallo
   grave; negro da entre 5.50:1 y 11.86:1 en todo el recorrido del degradado.
   Lo verifica tools/check-contrast.py. */
.row--primary {
  background-color: transparent;
  background-image: var(--grad-fire);
  box-shadow: var(--sh-fire);
  color: var(--text-on-fire);
}

/* El estado caliente cruza por opacidad, igual que el trazo y por el mismo
   motivo: mover los stops de un degradado es repaint. */
.row--primary::after {
  content: "";
  position: absolute;
  inset: 0;
  z-index: -1;
  border-radius: inherit;
  background-image: var(--grad-fire-hot);
  opacity: 0;
  pointer-events: none;
  transition: opacity var(--d-out) var(--e-fade);
}

.row--primary .row__title {
  color: var(--text-on-fire);
}

.row--primary .row__note,
.row--primary .row__arrow {
  color: var(--text-on-fire-soft);
}

/* La baldosa cálida sería invisible sobre naranja: se invierte a negro. */
.row--primary .row__icon {
  background-image: none;
  background-color: rgb(var(--rgb-ink) / 12%);
  border-color: rgb(var(--rgb-ink) / 22%);
  color: var(--text-on-fire);
}

@media (hover: hover) and (pointer: fine) {
  .row--primary:hover::after {
    opacity: 1;
    transition-duration: var(--d-fast);
  }
}

.row--primary:focus-visible::after {
  opacity: 1;
}
```

- [ ] **Step 4: Ajustar los estados de hover, foco y active de `.row`**

Sustituir el bloque de estados actual (líneas ~593–641). El hover ya no toca
`border-color`, porque ya no hay borde:

```css
@media (hover: hover) and (pointer: fine) {
  .row:hover {
    transform: translate3d(0, -2px, 0);
    background-color: var(--surface-row-hi);
    box-shadow: var(--sh-glass), var(--sh-gold-hi);
    transition-duration: var(--d-fast);
  }

  /* La fila rellena ya tiene su propio glow: se intensifica, no se sustituye. */
  .row--primary:hover {
    box-shadow: var(--sh-fire), var(--sh-gold-hi);
  }

  .row:hover .row__icon {
    background-image: var(--grad-tile-hi);
    border-color: var(--border-gold-hi);
    transition-duration: var(--d-fast);
  }

  /* La baldosa invertida no se enciende: sobre naranja no hay a qué encender. */
  .row--primary:hover .row__icon {
    background-image: none;
    border-color: rgb(var(--rgb-ink) / 34%);
  }

  .row:hover .row__arrow {
    transform: translate3d(4px, 0, 0);
    color: var(--text-gold);
    transition-duration: var(--d-fast);
  }

  .row--primary:hover .row__arrow {
    color: var(--text-on-fire);
  }
}

/* El teclado existe en cualquier dispositivo: fuera del guard de hover. El
   foco no desplaza la fila — mover el elemento enfocado desorienta. */
.row:focus-visible {
  box-shadow: var(--focus-shadow), var(--sh-glass);
}

.row:focus-visible .row__icon {
  background-image: var(--grad-tile-hi);
  border-color: var(--border-gold-hi);
}

.row:focus-visible .row__arrow {
  color: var(--text-gold);
}

.row--primary:focus-visible .row__icon {
  background-image: none;
}

.row--primary:focus-visible .row__arrow {
  color: var(--text-on-fire);
}

/* Después de :hover en el orden del archivo → gana a igual especificidad. */
.row:active {
  transform: scale(0.985);
  transition-duration: var(--d-tap);
  transition-timing-function: var(--e-press);
}

.row:not(.row--primary):active {
  background-color: var(--surface-row-hi);
}

.row:not(.row--primary):active .row__icon {
  background-image: var(--grad-tile-hi);
}

.row--primary:active::after {
  opacity: 1;
  transition-duration: var(--d-tap);
}
```

- [ ] **Step 5: Aplicar las clases en `index.html`**

- Fila 1 (Talleres, línea ~109): `class="row row--primary"` — sin `.stroke`.
- Fila 2 (AIVI, línea ~132): `class="row stroke"`.
- Fila 3 (WhatsApp, línea ~153): `class="row stroke"`.

Actualizar además el comentario del bloque (líneas 98–105), que todavía dice
que `row--primary` pone "borde dorado y resplandor":

```html
  <!-- ══════════════════════════════════════════════════════════════════════
       2 · LOS TRES ENLACES
       ─────────────────────────────────────────────────────────────────────
       CAMBIA AQUÍ LOS ENLACES. Los `href` marcados con data-todo son
       placeholders: sustitúyelos por la URL real y borra el atributo.

       `row--primary` = relleno de fuego con glow. `stroke` = trazo en
       degradado sobre vidrio oscuro. Solo UNA fila debería llevar
       `row--primary`: si todas gritan, ninguna guía. Para destacar otra,
       mueve la clase y ponle `stroke` a esta.
       ══════════════════════════════════════════════════════════════════════ -->
```

- [ ] **Step 6: Actualizar `prefers-contrast: more` en la sección 11**

Añadir dentro del bloque existente:

```css
  /* El degradado del trazo pierde en alto contraste: filo sólido. */
  .stroke::before {
    background-image: none;
    background-color: var(--fire-gold);
  }

  .stroke::after {
    display: none;
  }
```

- [ ] **Step 7: Actualizar `forced-colors: active` en la sección 11**

En HCM no se pintan degradados. Añadir al bloque existente:

```css
  .stroke::before,
  .stroke::after,
  .row--primary::after {
    display: none;
  }

  .row--primary {
    background-image: none;
    forced-color-adjust: none;
    background-color: ButtonFace;
    color: ButtonText;
  }
```

**Mantener** `.row` en el selector agrupado que ya aplica
`border: 1px solid ButtonText`: en HCM los degradados no se pintan y ese borde
real pasa a ser la única señal de que la fila es un control.

- [ ] **Step 8: Verificar las reglas**

Run: `python3 tools/check-rules.py`

Expected: PASS, incluida la regla 4 (`Reserva @supports para mask-composite`),
que hasta ahora pasaba por vacía y a partir de aquí comprueba algo real.

- [ ] **Step 9: Verificación visual y de contraste**

Run: `python3 tools/check-contrast.py` → PASS.

En `http://localhost:8080` comprobar:
1. La fila 01 tiene relleno rojo→dorado, texto negro y glow cálido.
2. Las filas 02 y 03 tienen un filo fino en degradado que recorre el contorno
   redondeado completo, sin cortes en las esquinas.
3. Al pasar el cursor sobre 02 y 03, el filo se enciende.
4. **A 1x, no solo a 2x:** el trazo tiene que seguir leyéndose como degradado.
   Si a 1x se ve como un borde naranja plano, subir `--sw-stroke` a 2px y
   anotarlo.

Verificar también con DevTools que en `:hover` no aparece un evento de *Paint*
sobre la fila — solo *Composite Layers*.

- [ ] **Step 10: Commit**

```bash
git add css/styles.css index.html
git commit -m "Añadir el trazo en degradado y el relleno de fuego a los enlaces"
```

---

## Tarea 6: Hero asimétrico y retrato vertical

**Files:**
- Modify: `tools/make-placeholders.py` — añadir el generador del retrato 4:5
- Create: `assets/img/jhei-portrait.png` (generado)
- Modify: `css/styles.css` — sección 5 completa, sección 6 (`.links`), sección 10 (movimiento)
- Modify: `css/tokens.css` — baja de `--grad-ring`, `--d-breath-a`, `--d-breath-b`
- Modify: `index.html` — hero completo, numeración de los enlaces

**Interfaces:**
- Consumes: `.chip` (Tarea 4), `.stroke` (Tarea 5).
- Produces: `.hero__portrait` (la tarjeta 4:5) y `.links` con `grid-template-columns: 2.25rem 1fr`. La Tarea 8 no depende de esto.

- [ ] **Step 1: Añadir el generador del retrato a `tools/make-placeholders.py`**

Añadir esta función después de `avatar()`:

```python
def portrait(x, y, w, h):
    """Retrato vertical 4:5 del hero: silueta de medio cuerpo sobre un
    resplandor cálido, con caída a negro por abajo para que el fundido del CSS
    tenga con qué fundirse.

    Sin recorte circular, a diferencia de avatar(): la tarjeta del hero es
    rectangular con esquinas redondeadas y el círculo es justo el rasgo del
    referente que este rediseño elimina.
    """
    nx, ny = x / w, y / h
    beam = light_beam(x, y, w, h, angle=-18, center=0.62, width_=0.62)
    base = lerp(INK, fire_ramp(0.22 + beam * 0.55), beam * 0.42)

    head_dx, head_dy = (nx - 0.52) / 0.17, (ny - 0.27) / 0.15
    body_dx, body_dy = (nx - 0.52) / 0.40, (ny - 0.92) / 0.48
    if head_dx ** 2 + head_dy ** 2 < 1.0 or (body_dx ** 2 + body_dy ** 2 < 1.0 and ny > 0.36):
        base = (13, 13, 13)

    # Caída a negro en el tercio inferior.
    if ny > 0.66:
        fade = (ny - 0.66) / 0.34
        base = lerp(base, INK, min(1.0, fade ** 1.6))

    n = grain(x, y, 10)
    return tuple(round(c + n) for c in base)
```

- [ ] **Step 2: Registrar el retrato en `main()` de `tools/make-placeholders.py`**

Insertar después de la línea que genera el avatar:

```python
    # Retrato del hero. 4:5, se sirve a 420px de ancho como máximo, así que
    # 840px cubre pantallas de 2x. El cliente lo sustituye por una foto real
    # de medio cuerpo con el mismo nombre y no hay que tocar el HTML.
    write_png(os.path.join(OUT, "jhei-portrait.png"), 840, 1050, portrait)
```

**No borrar la generación de `jhei-avatar.png`:** se sigue usando como
`apple-touch-icon` en el `<head>`.

- [ ] **Step 3: Generar los placeholders**

Run: `python3 tools/make-placeholders.py`

Expected: entre las líneas de salida aparece
`img/jhei-portrait.png  840x1050  ...KB`. Verificar que el archivo existe y
pesa menos de 200KB:

```bash
ls -l assets/img/jhei-portrait.png
```

- [ ] **Step 4: Reescribir el marcado del hero en `index.html`**

Sustituir el `<header class="hero shell">` completo (líneas 71–96):

```html
  <header class="hero shell">

    <div class="hero__text">
      <p class="chip hero__chip" data-enter>Viralidad · Contenido · IA aplicada</p>

      <h1 class="hero__name" data-enter>Jhei<br>Trujillo</h1>

      <div class="rule" data-enter aria-hidden="true">
        <span></span><i></i><span></span>
      </div>

      <p class="hero__claim" data-enter>
        Hago que te vean <span class="fire-text">y que te recuerden</span>.
      </p>
    </div>

    <!-- Tarjeta rectangular, NUNCA un círculo: el avatar circular es la firma
         más literal del referente que este rediseño elimina.
         Para cambiar la foto, sobrescribe assets/img/jhei-portrait.png con un
         retrato vertical 4:5 de medio cuerpo. El object-fit absorbe cualquier
         proporción parecida sin romper el layout. -->
    <div class="hero__portrait stroke" data-enter>
      <img src="assets/img/jhei-portrait.png" width="840" height="1050"
           fetchpriority="high" decoding="async" alt="Jhei Trujillo">
      <span class="hero__status">
        <span class="hero__status-dot" aria-hidden="true"></span>Disponible
      </span>
    </div>
  </header>
```

- [ ] **Step 5: Actualizar el `preload` del `<head>` en `index.html`**

Línea 35: cambiar el preload del avatar por el del retrato, que es el nuevo
candidato a LCP.

```html
<link rel="preload" href="assets/img/jhei-portrait.png" as="image" fetchpriority="high">
```

- [ ] **Step 6: Reescribir la sección 5 de `css/styles.css`**

Sustituir todo el bloque `5 · HERO` (líneas ~335–478) salvo `.rule`, que se
conserva tal cual:

```css
/* ════════════════════════════════════════════════════════════════════════════
   5 · HERO
   ---------------------------------------------------------------------------
   Eje asimétrico y alineado a la izquierda EN TODOS LOS TAMAÑOS. Un link in
   bio se consume casi entero en móvil: si la asimetría solo existe en
   escritorio, el rediseño no existe.
   ══════════════════════════════════════════════════════════════════════════ */

.hero {
  display: grid;
  gap: var(--sp-8);
  text-align: start;
  padding-block: clamp(var(--sp-9), 10vh, var(--sp-11)) 0;
}

/* El retrato va PRIMERO en el orden visual de móvil, desplazado a la
   izquierda, y el texto debajo. En escritorio pasa a la derecha. */
.hero__portrait {
  order: -1;
  position: relative;
  width: min(70%, 300px);
  aspect-ratio: 4 / 5;
  border-radius: var(--r-lg);
  overflow: hidden;
  background-color: var(--surface-load);
  box-shadow: var(--sh-3), var(--sh-gold);
}

.hero__portrait img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  /* Con 50% 50% en 4:5 la cara queda demasiado baja y el fundido se la come. */
  object-position: 50% 18%;
}

/* Fundido al fondo por el canto inferior: la tarjeta se disuelve en la página
   en vez de terminar en un corte recto. Va como capa propia y no como máscara
   sobre el <img>, porque una máscara sobre el candidato a LCP obliga al
   navegador a componer la imagen antes de poder pintarla. */
.hero__portrait::after {
  content: "";
  position: absolute;
  inset: auto 0 0 0;
  height: 38%;
  z-index: 1;
  pointer-events: none;
  background-image: var(--grad-portrait-foot);
}

.hero__text {
  display: grid;
  justify-items: start;
}

.hero__chip {
  margin-block-end: var(--sp-6);
}

/* Caja baja y peso 900. La mayúscula sostenida es un rasgo del referente, no
   de AIVI: en aivi.chat no hay un solo titular en versales. La jerarquía la
   carga el peso y el tracking negativo, no la caja. */
.hero__name {
  font-size: var(--fs-display);
  font-weight: var(--fw-black);
  line-height: var(--lh-display);
  letter-spacing: var(--ls-display);
  color: var(--text-primary);
}

.hero__claim {
  margin-block-start: var(--sp-6);
  max-width: var(--w-read);
  font-size: var(--fs-lead);
  font-weight: var(--fw-regular);
  line-height: var(--lh-normal);
  color: var(--text-secondary);
}

/* Anclada a la esquina inferior izquierda de la tarjeta, no centrada bajo un
   círculo. Fondo opaco a propósito: se apoya sobre la foto y el texto tiene
   que leerse sin depender de lo que haya debajo.

   EXCEPCION — mayúscula sostenida. Es el ÚNICO sitio de la página donde se
   permite, porque va por debajo de 11px. Es el mismo criterio que AIVI aplica
   a MÁS POPULAR y SOLO LATAM en su bloque de precios. No replicar en ningún
   otro selector: lo vigila tools/check-rules.py. */
.hero__status {
  position: absolute;
  left: var(--sp-4);
  bottom: var(--sp-4);
  z-index: var(--z-raised);
  display: inline-flex;
  align-items: center;
  gap: var(--sp-2);
  padding: var(--sp-1) var(--sp-3);
  border-radius: var(--r-full);
  background-color: var(--ink-deep);
  border: 1px solid var(--border-gold);
  box-shadow: var(--sh-2);
  font-size: var(--fs-micro);
  font-weight: var(--fw-bold);
  letter-spacing: var(--ls-wide);
  text-transform: uppercase;
  color: var(--text-secondary);
  white-space: nowrap;
}

.hero__status-dot {
  width: 7px;
  height: 7px;
  border-radius: var(--r-full);
  background-color: var(--fire-gold);
  box-shadow: 0 0 8px rgb(var(--rgb-gold) / 70%);
}

/* Filete ornamental: línea · rombo · línea. Alineado a la izquierda con el
   resto del hero, no centrado. */
.rule {
  display: flex;
  align-items: center;
  gap: var(--sp-4);
  margin-block-start: var(--sp-6);
}

.rule span {
  width: clamp(40px, 12vw, 76px);
  height: 1px;
  background-image: var(--grad-hairline);
}

.rule i {
  width: 8px;
  height: 8px;
  rotate: 45deg;
  border-radius: 2px;
  background-image: var(--grad-fire);
}

/* Dos columnas desde 60rem: texto a la izquierda, retrato a la derecha. */
@media (min-width: 60rem) {
  .hero {
    grid-template-columns: 1fr auto;
    align-items: center;
    gap: var(--sp-11);
  }

  .hero__portrait {
    order: 0;
    width: 320px;
  }
}
```

- [ ] **Step 7: Numerar los enlaces en `css/styles.css`**

Sustituir la regla `.links` (líneas ~489–493):

```css
/* Los números viven en su propia columna, FUERA de la píldora: dentro
   competirían con la baldosa del icono por el mismo espacio. */
.links {
  display: grid;
  grid-template-columns: 2.25rem 1fr;
  align-items: center;
  gap: var(--sp-4) 0;
  margin-block-start: var(--sp-9);
}

.links__num {
  font-size: var(--fs-micro);
  font-weight: var(--fw-bold);
  font-variant-numeric: tabular-nums;
  letter-spacing: var(--ls-wide);
  color: var(--text-gold);
}
```

- [ ] **Step 8: Añadir los números al marcado en `index.html`**

Delante de cada `<a class="row ...">` insertar su número. Son decorativos: el
orden ya lo comunica el DOM y un lector de pantalla no debe leer "cero uno"
antes de cada enlace.

```html
    <span class="links__num" aria-hidden="true">01</span>
```

…y `02`, `03` delante de la segunda y la tercera fila respectivamente.

- [ ] **Step 9: Retirar el avatar circular de la capa de movimiento**

En la sección 10 de `css/styles.css`, borrar:
- `html.motion .hero__avatar { opacity: 1; }`
- `html.motion.is-ready .hero__avatar { animation: enter-settle ... }`
- `@keyframes enter-settle`
- `html.motion .hero__avatar::after { animation: halo-breathe ...; will-change: ... }`
- `@keyframes halo-breathe`
- La referencia a `.hero__avatar` en el selector `html.motion.is-entered [data-enter], html.motion.is-entered .hero__avatar`

En el bloque `prefers-reduced-motion` de la sección 11, borrar las dos reglas
que referencian `.hero__avatar`.

Añadir el retardo de entrada del retrato junto a los demás:

```css
.hero__portrait {
  --delay: 60ms;
  --dur: 520ms;
  --from-y: 16px;
}
```

- [ ] **Step 10: Retirar los tokens huérfanos de `css/tokens.css`**

Borrar `--grad-ring` (bloque 5), `--d-breath-a` y `--d-breath-b` (bloque 11).
Ya no los usa nadie.

Verificar que no queda ninguna referencia:

```bash
grep -n "grad-ring\|d-breath\|hero__avatar\|halo-breathe\|enter-settle" css/ js/ index.html -r
```

Expected: sin resultados.

- [ ] **Step 11: Verificar**

Run: `python3 tools/check-rules.py` → PASS
Run: `python3 tools/check-contrast.py` → PASS

En el navegador, a 360px y a 1440px:
1. Todo el hero alineado a la izquierda. Nada centrado.
2. El retrato es una tarjeta rectangular con esquinas redondeadas y trazo en
   degradado. **Ningún círculo en la página.**
3. En móvil el retrato va arriba; desde 60rem pasa a la derecha del texto.
4. Los números 01/02/03 quedan alineados a la izquierda de cada píldora.
5. Sin scroll horizontal a 360px.

- [ ] **Step 12: Commit**

```bash
git add tools/make-placeholders.py assets/img/jhei-portrait.png css/ index.html
git commit -m "Reemplazar el avatar circular por un hero asimétrico con retrato 4:5"
```

---

## Tarea 7: Columnas de luz vertical en el fondo

**Files:**
- Modify: `css/styles.css` — sección 3, reglas `.backdrop__glow` y `.backdrop__glyphs`

**Interfaces:**
- Consumes: `--rgb-gold`, `--rgb-orange` (ya existen).
- Produces: nada que consuman otras tareas.

- [ ] **Step 1: Añadir las columnas a `.backdrop__glow`**

Sustituir la regla completa (líneas ~222–238). Las columnas van como capas
adicionales del **mismo** elemento: cero elementos nuevos y cero capas GPU
nuevas, que es la regla dura de esta sección.

```css
/* ── Resplandor cálido y columnas de luz ────────────────────────────────────
   Las cuatro columnas verticales que suben desde el borde inferior son el
   recurso más reconocible de aivi.chat. Van como capas de background-image de
   ESTE elemento, no como elementos propios: cuatro divs de viewport completo
   serían cuatro texturas de ~14MB cada una en un móvil de 1290x2790.

   Sus posiciones (14%, 37%, 63%, 86%) están elegidas para NO coincidir con el
   centro de la columna de contenido: una columna de luz justo detrás del texto
   le roba contraste.

   La luz se suma en `screen`, que es su comportamiento físico; apilada en
   `normal` daría un lavado sucio y apagado. */
.backdrop__glow {
  z-index: 1;
  opacity: 0.55;
  background-image:
    /* Columnas verticales, de abajo hacia arriba. */
    linear-gradient(to top,
      rgb(var(--rgb-gold) / 22%) 0%,
      rgb(var(--rgb-orange) / 8%) 34%,
      rgb(var(--rgb-orange) / 0%) 72%),
    linear-gradient(to top,
      rgb(var(--rgb-orange) / 26%) 0%,
      rgb(var(--rgb-orange) / 9%) 40%,
      rgb(var(--rgb-orange) / 0%) 78%),
    linear-gradient(to top,
      rgb(var(--rgb-gold) / 18%) 0%,
      rgb(var(--rgb-gold) / 6%) 30%,
      rgb(var(--rgb-gold) / 0%) 66%),
    linear-gradient(to top,
      rgb(var(--rgb-orange) / 20%) 0%,
      rgb(var(--rgb-orange) / 7%) 36%,
      rgb(var(--rgb-orange) / 0%) 74%),
    /* Resplandor de la esquina superior, ya existente. */
    radial-gradient(58% 44% at 92% 0%,
      rgb(var(--rgb-gold) / 16%) 0%,
      rgb(var(--rgb-gold) / 5%) 46%,
      rgb(var(--rgb-gold) / 0%) 76%),
    radial-gradient(88% 62% at 100% -6%,
      rgb(var(--rgb-orange) / 12%) 0%,
      rgb(var(--rgb-orange) / 4%) 40%,
      rgb(var(--rgb-orange) / 0%) 74%);
  background-repeat: no-repeat;
  background-size:
    9% 62%,
    14% 78%,
    7% 48%,
    11% 70%,
    100% 100%,
    100% 100%;
  background-position:
    14% 100%,
    37% 100%,
    63% 100%,
    86% 100%,
    0 0,
    0 0;
  background-blend-mode: screen, screen, screen, screen, screen, screen;
}
```

- [ ] **Step 2: Bajar la intensidad de los hexágonos**

En `.backdrop__glyphs` (línea ~241), cambiar `opacity: 0.5` por `opacity: 0.3`.
La luz vertical tiene que mandar sobre la geometría; con las dos al mismo peso
el fondo se ensucia.

- [ ] **Step 3: Verificar**

Run: `python3 tools/check-rules.py` → PASS, en especial la regla 3
(`Cero capas GPU propias en el fondo`).

En el navegador:
1. Se ven cuatro columnas cálidas subiendo desde el borde inferior, de anchos
   distintos, ninguna justo detrás de la columna de texto.
2. Con DevTools › Layers, el fondo sigue siendo **una sola** capa.
3. Con `prefers-reduced-transparency: reduce` forzado desde DevTools, el
   resplandor baja a 0.3 y las columnas se atenúan con él.

- [ ] **Step 4: Commit**

```bash
git add css/styles.css
git commit -m "Añadir las columnas de luz vertical de AIVI al fondo"
```

---

## Tarea 8: Cintas en bucle y control de pausa

Sustituye el carrusel. Es la tarea que más código elimina.

**Files:**
- Modify: `index.html` — sección de colaboraciones completa, más la banda de texto
- Modify: `css/styles.css` — sección 7 completa; sección 11 (`prefers-reduced-motion`)
- Modify: `js/main.js` — sustituir el bloque 3 (`carousel`, líneas 123–323) por `ribbons`

**Interfaces:**
- Consumes: `.chip` (Tarea 4), `.stroke` (Tarea 5), `--d-ribbon-text`, `--d-ribbon-cards` (Tarea 2).
- Produces: nada que consuman otras tareas.

**Contrato del marcado de una cinta.** El JS lo asume exactamente así:

```html
<div class="ribbon" data-ribbon>
  <div class="ribbon__track">
    <ul class="ribbon__set"> … elementos … </ul>
  </div>
</div>
```

El JS clona `.ribbon__set`, le pone `aria-hidden="true"` y lo añade al
`.ribbon__track`. Con dos sets, el track mide el doble y
`translate3d(-50%, 0, 0)` recorre exactamente un set: el bucle es continuo.
Después añade `is-looped` a `.ribbon`, que es lo que activa la animación en CSS.
Sin JS no hay clon, no hay `is-looped` y no hay animación: la cinta queda
estática y legible, nunca vacía.

- [ ] **Step 1: Escribir el marcado de las dos cintas en `index.html`**

Sustituir la `<section class="collabs section">` completa (líneas 178–225):

```html
  <!-- ══════════════════════════════════════════════════════════════════════
       3 · BANDA DE TEXTO
       El separador en bucle de aivi.chat. El JS duplica el contenido; la copia
       va aria-hidden para que no se lea dos veces.
       ══════════════════════════════════════════════════════════════════════ -->
  <div class="ribbon ribbon--text section" data-ribbon aria-label="Lo que hago">
    <div class="ribbon__track">
      <ul class="ribbon__set">
        <li>Talleres</li>
        <li>Guiones</li>
        <li>Virales</li>
        <li>IA aplicada</li>
        <li>Comunidad</li>
      </ul>
    </div>
  </div>

  <!-- ══════════════════════════════════════════════════════════════════════
       4 · COLABORACIONES
       ══════════════════════════════════════════════════════════════════════ -->
  <section class="collabs section" aria-labelledby="collabs-title">
    <div class="shell shell--wide">
      <p class="chip" data-reveal>Colaboraciones</p>
      <h2 class="collabs__title" id="collabs-title" data-reveal>
        Gente y marcas con las que <span class="fire-text">he construido cosas</span>
      </h2>
    </div>

    <div class="ribbon ribbon--cards" data-ribbon>
      <div class="ribbon__track">
        <ul class="ribbon__set">
          <li class="collab stroke">
            <img class="collab__photo" src="assets/img/collab-1.png" width="420" height="640"
                 loading="lazy" decoding="async" alt="Colaboración con Marca 1">
            <span class="collab__brand">Marca 1</span>
          </li>
          <li class="collab stroke">
            <img class="collab__photo" src="assets/img/collab-2.png" width="420" height="640"
                 loading="lazy" decoding="async" alt="Colaboración con Marca 2">
            <span class="collab__brand">Marca 2</span>
          </li>
          <li class="collab stroke">
            <img class="collab__photo" src="assets/img/collab-3.png" width="420" height="640"
                 loading="lazy" decoding="async" alt="Colaboración con Marca 3">
            <span class="collab__brand">Marca 3</span>
          </li>
          <li class="collab stroke">
            <img class="collab__photo" src="assets/img/collab-4.png" width="420" height="640"
                 loading="lazy" decoding="async" alt="Colaboración con Marca 4">
            <span class="collab__brand">Marca 4</span>
          </li>
          <li class="collab stroke">
            <img class="collab__photo" src="assets/img/collab-5.png" width="420" height="640"
                 loading="lazy" decoding="async" alt="Colaboración con Marca 5">
            <span class="collab__brand">Marca 5</span>
          </li>
          <li class="collab stroke">
            <img class="collab__photo" src="assets/img/collab-6.png" width="420" height="640"
                 loading="lazy" decoding="async" alt="Colaboración con Marca 6">
            <span class="collab__brand">Marca 6</span>
          </li>
        </ul>
      </div>
    </div>

    <!-- WCAG 2.2.2: contenido en movimiento de más de 5 segundos exige un
         mecanismo de pausa. Pausar al pasar el cursor NO cumple: no existe
         para teclado, táctil ni tecnología de apoyo. Este botón sí.
         El JS lo muestra; sin JS no hay movimiento que pausar. -->
    <div class="ribbon-control shell shell--wide">
      <button class="ribbon-toggle" type="button" hidden
              data-ribbon-toggle aria-pressed="false">
        <span class="ribbon-toggle__icon" aria-hidden="true"></span>
        <span data-ribbon-toggle-label>Pausar el movimiento</span>
      </button>
    </div>
  </section>
```

- [ ] **Step 2: Escribir el CSS de las cintas — sustituir la sección 7 de `css/styles.css`**

Borrar todo el bloque `7 · COLABORACIONES Y CARRUSEL` (líneas ~643–893),
incluidos `.carousel`, `.carousel__track`, `.carousel__dots`, `.dot`,
`.dot__track` y sus reglas de estado. Sustituir por:

```css
/* ════════════════════════════════════════════════════════════════════════════
   7 · CINTAS EN BUCLE Y COLABORACIONES
   ---------------------------------------------------------------------------
   Sustituyen al carrusel con dots, que era el bloque más parecido al referente.
   El bucle es continuo: el JS duplica el set y la animación desplaza el track
   un 50% exacto, que con dos sets es justo un set.

   Solo se anima transform. Nunca left ni margin.
   ══════════════════════════════════════════════════════════════════════════ */

.ribbon {
  overflow: hidden;
}

.ribbon__track {
  display: flex;
  width: max-content;
}

.ribbon__set {
  display: flex;
  flex: none;
  align-items: center;
  margin: 0;
}

/* La animación SOLO se activa cuando el JS ha duplicado el set. Sin JS no hay
   clon, y animar un track sin duplicar dejaría un hueco al final del ciclo. */
.ribbon.is-looped .ribbon__track {
  animation: ribbon-slide var(--ribbon-dur) linear infinite;
}

@keyframes ribbon-slide {
  from { transform: translate3d(0, 0, 0); }
  to   { transform: translate3d(-50%, 0, 0); }
}

/* Tres formas de pausar. El botón es la que cumple WCAG 2.2.2; las otras dos
   son comodidad para ratón y teclado. */
html.is-ribbons-paused .ribbon__track,
.ribbon:hover .ribbon__track,
.ribbon:focus-within .ribbon__track {
  animation-play-state: paused;
}

/* ── Banda de texto ──────────────────────────────────────────────────────── */
.ribbon--text {
  --ribbon-dur: var(--d-ribbon-text);
  border-block: 1px solid var(--border-hair);
  padding-block: var(--sp-4);
}

.ribbon--text li {
  font-size: var(--fs-h3);
  font-weight: var(--fw-semi);
  letter-spacing: var(--ls-h3);
  color: var(--text-muted);
  white-space: nowrap;
  padding-inline: var(--sp-6);
}

/* Separador entre palabras, como el "·" del subtítulo antiguo. */
.ribbon--text li::after {
  content: "·";
  padding-inline-start: var(--sp-6);
  color: var(--text-gold);
  opacity: 0.5;
}

/* ── Cinta de tarjetas ───────────────────────────────────────────────────── */
.ribbon--cards {
  --ribbon-dur: var(--d-ribbon-cards);
  margin-block-start: var(--sp-7);
  mask-image: linear-gradient(90deg,
    transparent 0,
    #000 var(--sp-8),
    #000 calc(100% - var(--sp-8)),
    transparent 100%);
}

.ribbon--cards .ribbon__set {
  gap: var(--sp-3);
  padding-inline-end: var(--sp-3);
}

.collab {
  position: relative;
  isolation: isolate;
  flex: 0 0 auto;
  width: min(62vw, 240px);
  aspect-ratio: 5 / 8;
  border-radius: var(--r-lg);
  background-color: var(--surface-load);
  overflow: hidden;
  box-shadow: var(--sh-2);
}

@media (min-width: 37.5rem) {
  .collab {
    width: 232px;
  }
}

@media (min-width: 64rem) {
  .collab {
    width: 256px;
  }
}

/* Monocromo puro: el color de estas fotos era otra fuente de saturación. */
.collab__photo {
  width: 100%;
  height: 100%;
  object-fit: cover;
  /* Obligatorio: con 50% 50% en formato 5:8 el rostro queda demasiado bajo y
     el velo del pie se lo come. */
  object-position: 50% 22%;
  filter: grayscale(1) contrast(1.06) brightness(0.9);
}

/* Velo casi negro que sube desde la base, para que el rótulo blanco mantenga
   su contraste con cualquier foto que ponga el cliente. */
.collab::after {
  content: "";
  position: absolute;
  inset: auto 0 0 0;
  height: 52%;
  z-index: 1;
  background-image: var(--grad-collab-foot);
  pointer-events: none;
}

.collab__brand {
  position: absolute;
  inset: auto 0 8% 0;
  z-index: 2;
  padding-inline: var(--sp-4);
  font-size: var(--fs-small);
  font-weight: var(--fw-bold);
  letter-spacing: var(--ls-none);
  text-align: center;
  color: var(--paper);
}

/* ── Titular ─────────────────────────────────────────────────────────────── */
.collabs__title {
  margin-block-start: var(--sp-4);
  font-size: var(--fs-h2);
  font-weight: var(--fw-bold);
  line-height: var(--lh-snug);
  letter-spacing: var(--ls-h2);
  color: var(--text-primary);
  text-wrap: balance;
  max-width: 22ch;
}

/* ── Control de pausa ────────────────────────────────────────────────────── */
.ribbon-control {
  display: flex;
  margin-block-start: var(--sp-6);
  min-height: var(--tap-min);
}

.ribbon-toggle {
  display: inline-flex;
  align-items: center;
  gap: var(--sp-3);
  min-height: var(--tap-min);
  padding: var(--sp-2) var(--sp-5);
  border-radius: var(--r-full);
  background-color: var(--surface-glass);
  border: 1px solid var(--border-strong);
  color: var(--text-secondary);
  font-size: var(--fs-small);
  font-weight: var(--fw-medium);
  cursor: pointer;
  touch-action: manipulation;
  transition: color var(--d-out) var(--e-fade),
    border-color var(--d-out) var(--e-fade);
}

/* Dos barras (pausa). Al activarse el estado pausado pasa a un triángulo
   (reproducir): el icono cambia de FORMA, no solo de color.

   Las dos barras se hacen con los bordes laterales y el centro hueco, no con
   un clip-path de un solo polígono: un polígono con dos regiones separadas
   tiene que autointersecarse y el resultado depende de la regla de relleno
   del navegador. Con `box-sizing: border-box` (que pone el reset global), los
   dos bordes de 4px caben dentro de los 12px de ancho y dejan 4px de hueco. */
.ribbon-toggle__icon {
  width: 12px;
  height: 12px;
  flex: none;
  border-inline: 4px solid currentColor;
}

.ribbon-toggle[aria-pressed="true"] .ribbon-toggle__icon {
  border-inline: 0;
  background-color: currentColor;
  clip-path: polygon(0 0, 100% 50%, 0 100%);
}

@media (hover: hover) and (pointer: fine) {
  .ribbon-toggle:hover {
    color: var(--text-gold);
    border-color: var(--border-gold-hi);
    transition-duration: var(--d-fast);
  }
}

.ribbon-toggle:focus-visible {
  color: var(--text-gold);
}
```

- [ ] **Step 3: Sustituir el bloque 3 de `js/main.js`**

Borrar el bloque `3 · CARRUSEL` completo (líneas 123–323) y poner en su lugar:

```js
  /* ══ 3 · CINTAS EN BUCLE ═════════════════════════════════════════════════
     El bucle continuo necesita el contenido duplicado: con dos sets el track
     mide el doble y desplazarlo un 50% recorre exactamente un set, así que el
     salto del final del ciclo es invisible.

     La copia va aria-hidden y sin elementos tabulables: es la MISMA
     información, y un lector de pantalla no debe leerla dos veces ni el
     tabulador debe recorrerla.

     WCAG 2.2.2: contenido en movimiento de más de 5 segundos exige un
     mecanismo de pausa. El :hover no cumple — no existe para teclado, táctil
     ni tecnología de apoyo. Por eso hay un botón real.                     */
  (function ribbons() {
    var ribbonEls = document.querySelectorAll("[data-ribbon]");
    if (!ribbonEls.length) return;

    Array.prototype.forEach.call(ribbonEls, function (ribbon) {
      var set = ribbon.querySelector(".ribbon__set");
      if (!set) return;

      var clone = set.cloneNode(true);
      clone.setAttribute("aria-hidden", "true");
      Array.prototype.forEach.call(
        clone.querySelectorAll("a, button, [tabindex]"),
        function (el) {
          el.setAttribute("tabindex", "-1");
        }
      );

      set.parentNode.appendChild(clone);
      /* Solo ahora se activa la animación en CSS: sin clon no hay bucle. */
      ribbon.classList.add("is-looped");
    });

    var toggle = document.querySelector("[data-ribbon-toggle]");
    if (!toggle) return;

    var label = toggle.querySelector("[data-ribbon-toggle-label]");

    function setPaused(paused) {
      root.classList.toggle("is-ribbons-paused", paused);
      toggle.setAttribute("aria-pressed", paused ? "true" : "false");
      if (label) {
        label.textContent = paused
          ? "Reanudar el movimiento"
          : "Pausar el movimiento";
      }
    }

    /* El botón solo existe si hay movimiento que pausar. */
    toggle.hidden = false;

    /* Con movimiento reducido las cintas arrancan DETENIDAS, y el botón
       permite reanudarlas para quien quiera verlas. */
    setPaused(reduce.matches);

    toggle.addEventListener("click", function () {
      setPaused(toggle.getAttribute("aria-pressed") !== "true");
    });
  })();
```

Actualizar también la lista de bloques de la cabecera del archivo (línea 12):

```js
     Bloques:  1 Arranque · 2 Revelado al scroll · 3 Cintas en bucle · 4 Año
```

- [ ] **Step 4: Actualizar `prefers-reduced-motion` en la sección 11 de `css/styles.css`**

Borrar las reglas que referencian `.carousel__track`, `.collab`,
`.collab__photo` y `.dot__track`. Añadir en su lugar:

```css
  /* Las dos cintas quedan detenidas. La de tarjetas vuelve a ser un contenedor
     con scroll horizontal normal: sigue siendo navegable con el dedo y con el
     teclado, solo que no se mueve sola. */
  .ribbon.is-looped .ribbon__track {
    animation: none;
    transform: none;
  }

  .ribbon--cards {
    overflow-x: auto;
    scrollbar-width: none;
  }

  .ribbon--cards::-webkit-scrollbar {
    display: none;
  }
```

Sustituir el selector agrupado de transiciones, que menciona elementos ya
borrados:

```css
  .row,
  .row__arrow,
  .social,
  .ribbon-toggle {
    transition-property: opacity, color, background-color, background-image,
      border-color, box-shadow, filter;
  }
```

- [ ] **Step 5: Actualizar `forced-colors` y `print` en la sección 11**

En `forced-colors: active`, sustituir `.collab` por `.collab` (se mantiene) y
añadir `.ribbon-toggle` al grupo que recibe `border: 1px solid ButtonText`.

En `@media print`, sustituir `.carousel__dots` por `.ribbon-control`.

- [ ] **Step 6: Verificar que no queda nada del carrusel**

```bash
grep -rn "carousel\|dot__track\|is-focus\|data-carousel" css/ js/ index.html
```

Expected: sin resultados.

- [ ] **Step 7: Verificar en el navegador**

1. Las dos cintas se mueven en bucle continuo, sin saltos ni huecos al reiniciar.
2. El botón "Pausar el movimiento" detiene **las dos** a la vez y cambia a
   "Reanudar el movimiento" con el icono en triángulo.
3. Con teclado: `Tab` llega al botón, `Enter` y `Espacio` lo activan, y el
   anillo de foco de dos tonos es visible.
4. Al tabular, el foco **no** entra en las tarjetas duplicadas.
5. En DevTools › Rendering, activar `prefers-reduced-motion: reduce` y recargar:
   las dos cintas arrancan quietas, el botón dice "Reanudar el movimiento" y la
   cinta de tarjetas se puede desplazar con el dedo o con la rueda.
6. Consola sin errores.

- [ ] **Step 8: Commit**

```bash
git add index.html css/styles.css js/main.js
git commit -m "Sustituir el carrusel por cintas en bucle con control de pausa"
```

---

## Tarea 9: Bio, footer, copy y documentación

**Files:**
- Modify: `css/styles.css` — sección 8 (`.bio`, `.socials`), sección 9 (footer)
- Modify: `index.html` — bio, footer
- Modify: `docs/brand/aivi-brand-extract.md`
- Modify: `README.md`

**Interfaces:**
- Consumes: `.chip` (Tarea 4), `.stroke` (Tarea 5).
- Produces: nada.

- [ ] **Step 1: Alinear la bio a la izquierda en `css/styles.css`**

En `.bio` (línea ~899), sustituir `text-align: center` por `text-align: start`.
En `.bio__text`, borrar `margin-inline: auto`. En `.socials`, sustituir
`justify-content: center` por `justify-content: flex-start`.

El eje asimétrico tiene que recorrer la página entera: una bio centrada debajo
de un hero alineado a la izquierda se lee como un error de maquetación.

- [ ] **Step 2: Sustituir el handle por un chip en `index.html`**

Reemplazar la línea 233:

```html
    <p class="chip" data-reveal>Sobre mí</p>
    <p class="bio__handle" data-reveal>@<span class="tbd" data-todo="USUARIO">usuario</span></p>
```

En `css/styles.css`, añadir `margin-block-start: var(--sp-4);` a `.bio__handle`.

- [ ] **Step 3: Aplicar el trazo a los círculos de redes**

En `index.html`, añadir la clase `stroke` a los tres `<a class="social">`:
`class="social stroke"`.

En `css/styles.css`, borrar de `.social` la línea
`border: 1px solid var(--border-soft);` y las dos declaraciones
`border-color: var(--border-gold-hi);` de sus estados `:hover` y
`:focus-visible` — el trazo ya lo gestiona `.stroke`.

No hace falta añadir nada para el encendido del filo: `.stroke:hover::after` y
`.stroke:focus-visible::after` ya lo cubren desde la utilidad. Solo verificar
en el navegador que el filo del círculo se enciende al pasar el cursor y al
enfocar con teclado.

- [ ] **Step 4: Poner el footer en caja baja y a la izquierda**

En `css/styles.css` sección 9: en `.foot`, sustituir `text-align: center` por
`text-align: start`. En `.foot::before`, sustituir `margin: 0 auto var(--sp-7)`
por `margin: 0 0 var(--sp-7)`. En `.foot__claim, .foot__legal`, borrar
`margin-inline: auto`.

Envolver el contenido del footer en un `.shell` en `index.html` para que se
alinee con el resto de la página:

```html
<footer class="foot">
  <div class="shell">
    <p class="foot__claim">Sé visto. Sé recordado.</p>
    <p class="foot__legal">
      © <span data-year>2026</span> Jhei Trujillo · Todos los derechos reservados
    </p>
  </div>
</footer>
```

Y en `css/styles.css`, quitar `padding-inline: var(--sp-gutter);` de `.foot`,
que ahora lo aporta el `.shell`.

- [ ] **Step 5: Corregir `docs/brand/aivi-brand-extract.md`**

Sustituir el último párrafo, que todavía instruye replicar la arquitectura del
referente:

```markdown
Los dos `ref-layout-*` son **material histórico**. Sirvieron para entender qué
bloques necesita un link in bio, no para definir cómo se ven. La arquitectura
de esta página la define
`docs/superpowers/specs/2026-07-28-rediseno-diferenciacion-aivi-design.md`, que
existe precisamente para dejar de parecerse a ellos. No replicar ni su
estructura, ni su ritmo, ni su tipografía en versales.
```

En la lista de referencias, cambiar la descripción de los dos `ref-layout-*`
de "referente de layout que el cliente quiere replicar" a "referente de layout
descartado — ver el spec de diferenciación".

- [ ] **Step 6: Actualizar `README.md`**

Añadir dos apartados:

1. **Retrato del hero:** `assets/img/jhei-portrait.png` es un placeholder 840×1050
   (4:5). Se sustituye por un retrato real de medio cuerpo con el mismo nombre y
   la misma proporción; no hay que tocar el HTML.
2. **Verificación:** cómo y cuándo correr `python3 tools/check-rules.py` y
   `python3 tools/check-contrast.py`, y qué garantiza cada uno.

Revisar además todas las menciones al avatar circular, al carrusel y a los dots,
y actualizarlas.

- [ ] **Step 7: Verificar**

Run: `python3 tools/check-rules.py` → PASS
Run: `python3 tools/check-contrast.py` → PASS

En el navegador: bio, redes y footer alineados a la izquierda, en la misma
vertical que el hero y que los enlaces. Los círculos de redes tienen filo en
degradado que se enciende al pasar el cursor.

- [ ] **Step 8: Commit**

```bash
git add css/styles.css index.html docs/brand/aivi-brand-extract.md README.md
git commit -m "Alinear bio, redes y footer al eje asimétrico y corregir la documentación"
```

---

## Tarea 10: Verificación final

Nada nuevo se implementa aquí. Se comprueba que las ocho garantías del §10 del
spec siguen en pie y que los criterios de éxito del §2 se cumplen.

**Files:**
- Modify: solo si algo falla.

**Interfaces:**
- Consumes: todo lo anterior.
- Produces: el veredicto.

- [ ] **Step 1: Arnés completo**

```bash
python3 tools/check-rules.py && python3 tools/check-contrast.py
```

Expected: los dos en PASS, código de salida 0.

- [ ] **Step 2: Huérfanos**

```bash
grep -rn "hero__avatar\|grad-ring\|halo-breathe\|enter-settle\|carousel\|dot__track\|hero__tagline\|d-breath" css/ js/ index.html
```

Expected: sin resultados.

- [ ] **Step 3: Anchos**

Con el servidor levantado, revisar a **360px**, **390px**, **768px** y **1440px**:

1. Sin scroll horizontal en ninguno.
2. El hero mantiene la asimetría en los cuatro.
3. Las cintas no desbordan el viewport.
4. Ningún texto se corta ni se solapa.

- [ ] **Step 4: Densidad de pantalla**

Verificar el trazo en degradado a **1x** y a **2x**. Si a 1x se lee como un
borde naranja plano, subir `--sw-stroke` a `2px` y volver a verificar.

- [ ] **Step 5: Preferencias del usuario**

Desde DevTools › Rendering, forzar y recargar en cada caso:

| Preferencia | Esperado |
|---|---|
| `prefers-reduced-motion: reduce` | Cintas detenidas, botón en "Reanudar", cero traslaciones, la cinta de tarjetas se desplaza a mano |
| `prefers-contrast: more` | Trazos en filo sólido dorado, glows apagados, grano oculto |
| `prefers-reduced-transparency: reduce` | Resplandor y hexágonos atenuados, grano oculto |
| `forced-colors: active` | Fondo oculto, controles con borde `ButtonText`, cero degradados |

- [ ] **Step 6: Sin JavaScript**

Desactivar JS en DevTools y recargar. Esperado:

1. La página se ve **completa**: nada oculto esperando un observador.
2. Las cintas están quietas y son legibles, no vacías.
3. El botón de pausa **no** aparece (lleva `hidden` en el marcado y solo el JS
   lo muestra).
4. Los tres enlaces funcionan.

- [ ] **Step 7: Rendimiento**

Con DevTools › Performance, grabar un scroll completo de la página en emulación
móvil con CPU a 4x:

1. Sin *long tasks* durante el scroll.
2. Las cintas producen solo *Composite Layers*, nunca *Layout* ni *Paint*.
3. En DevTools › Layers, el fondo sigue siendo **una** capa.

- [ ] **Step 8: Terceros y consola**

En DevTools › Network, recargar con caché desactivada: **ninguna** petición a
un dominio que no sea `localhost`. Consola sin errores ni avisos.

- [ ] **Step 9: Los cinco criterios de éxito del spec**

Comparar la página con `docs/brand/ref-layout-hero.png` y
`ref-layout-bio.png` lado a lado y confirmar uno por uno:

1. Ningún bloque conserva a la vez posición, eje de alineación y tratamiento
   del bloque equivalente en el referente.
2. Cero mayúscula sostenida fuera de `.hero__status`.
3. Los tres enlaces usan trazo o relleno en degradado; ninguno usa borde plano.
4. Están los tres recursos de AIVI: columnas de luz vertical, chips y cinta de
   texto en bucle.
5. Ninguna garantía degradada (pasos 1 y 5 de esta tarea).

- [ ] **Step 10: Commit final**

Solo si algún paso obligó a corregir algo:

```bash
git add -A
git commit -m "Corregir los hallazgos de la verificación final"
```

---

## Autorrevisión del plan

**Cobertura del spec.**

| Sección del spec | Tarea |
|---|---|
| §3.1 Fin de la mayúscula | 3 |
| §3.2 Chips-etiqueta | 4 |
| §3.3 Frase clave en degradado | 6 (hero), 8 (titular de colabs) |
| §4.1 Trazo, construcción y reserva | 5 |
| §4.2 Jerarquía de los tres enlaces | 5 |
| §4.3 Contraste sobre el relleno | 2 (token), 1 y 10 (verificación) |
| §4.4 Alcance del trazo | 5 (filas), 6 (retrato), 8 (cards), 9 (redes) |
| §5 Hero asimétrico, retrato, numeración | 6 |
| §6 Columnas de luz vertical | 7 |
| §7.1–7.2 Cintas | 8 |
| §7.3 Control de pausa | 8 |
| §7.4 Impacto en main.js | 8 |
| §8 Copy | 4, 8, 9 |
| §9 Tokens | 2 (alta), 6 (baja) |
| §10 Garantías | 10 |
| §11 Riesgos | 5 (paso 9: 1x), 10 (pasos 4–7) |
| §13 Documentación | 9 |

Sin huecos.

**Consistencia de nombres.** `.stroke`, `.chip`, `.ribbon`, `.ribbon__track`,
`.ribbon__set`, `.ribbon-toggle`, `is-looped`, `is-ribbons-paused`,
`data-ribbon`, `data-ribbon-toggle`, `data-ribbon-toggle-label`,
`.hero__portrait`, `.hero__claim`, `.hero__chip`, `.links__num`,
`jhei-portrait.png` — cada uno se define en una tarea y se usa con el mismo
nombre en las demás.

**Riesgo conocido, aceptado.** La Tarea 5 introduce `.stroke` sobre `.row`, que
ya tiene `isolation: isolate` por su propia regla. Es una declaración duplicada,
no un conflicto: ambas piden lo mismo. Se deja porque `.stroke` tiene que
funcionar en elementos que no son filas (retrato, cards, redes).
