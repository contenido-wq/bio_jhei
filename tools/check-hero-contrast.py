#!/usr/bin/env python3
"""Contraste del texto del hero sobre la FOTO, no sobre un color plano.

Es el único punto de la página cuyo contraste no depende solo de los tokens:
el texto del hero se apoya en una fotografía, y una foto distinta cambia el
resultado sin que se toque una sola línea de CSS. `tools/check-contrast.py`
no puede verlo — lee tokens.css como texto y ahí no hay ningún píxel.

Lo que hace este script es lo que antes se hacía a ojo:

  1 · recorta la foto como lo haría `object-fit: cover` con el
      `object-position` que declara css/styles.css, en once tamaños de
      pantalla que cubren de un móvil de 320 a un escritorio de 1920;
  2 · compone encima las capas de `.hero__scrim`, leídas TAMBIÉN de
      css/styles.css y no copiadas aquí;
  3 · busca el píxel MÁS CLARO de la banda donde cae el texto, que es el peor
      caso y el único que decide;
  4 · mide contra él los tres colores que el hero pone sobre la foto.

Los valores no se escriben a mano en ningún sitio: si alguien cambia una
parada del velo, el encuadre o la propia foto, este script se entera.

Necesita Pillow (`pip3 install Pillow`). Es la única herramienta del proyecto
que no va con la librería estándar, y es porque no hay forma razonable de
decodificar un JPEG sin ella. Si no está instalada, el script lo dice y se
salta la comprobación en vez de fallar.

Uso:  python3 tools/check-hero-contrast.py
Sale con 1 si alguna pareja incumple su mínimo.
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STYLES = os.path.join(ROOT, "css", "styles.css")
TOKENS = os.path.join(ROOT, "css", "tokens.css")
PHOTO = os.path.join(ROOT, "assets", "img", "jhei-hero.jpg")

MINIMUM = 4.5          # WCAG 1.4.3, texto
BREAKPOINT = 960       # 60rem · donde el texto se va a la izquierda

# Alto del bloque de texto contando su hueco inferior. En móvil vive pegado
# abajo, así que su banda se deriva de la ALTURA DEL HERO y no de una fracción
# fija: en un teléfono corto el bloque ocupa mucha más parte del hero y empieza
# mucho más arriba.
#
# 258 no es una estimación: se midió en el navegador a 320, 360, 390 y 430, y
# en los cuatro dio entre 248 y 250px. Apenas cambia de alto entre teléfonos
# porque la frase cabe en una línea en todos. Los ~8px de más son el margen.
#
# Se mueve con CUALQUIER cambio del bloque de texto del hero, y con él la
# calibración entera del fundido inferior. Ha valido 210 (antes de subir las
# cifras de la bio), 290 (con las cifras y 56px de hueco inferior) y 258 (con
# el hueco bajado a 24 para que el bloque no quedara tan alto en móvil).
# Cambiar contenido O separación del hero obliga a volver a medirlo.
#
# Estuvo en 240 "por si acaso", y ese por si acaso salía caro: cuarenta píxeles
# de banda inventada empujaban al velo a ser mucho más oscuro de lo necesario
# para protegerla. Un margen de seguridad en el sitio equivocado no es
# prudencia, es una foto apagada.
TEXT_BLOCK_PX = 258

# En escritorio el texto se centra en vertical y arranca en el EJE DEL HERO,
# que no es el de la página: `.hero__text` sube su tope a `--w-wide` (1120px)
# para que el titular entre por el 14,5% del ancho, como en la referencia. El
# borde derecho lo pone el tope de 28rem que llevan sus hijos.
HERO_AXIS_PX = 1120
TEXT_CAP_PX = 448          # 28rem
SAFE_RIGHT = 0.62          # límite del velo lateral: nada de texto lo cruza

VIEWPORTS = [
    (1920, 1080), (1440, 900), (1280, 800), (1024, 700), (960, 600),
    (834, 1112), (768, 1024), (430, 932), (390, 844), (360, 640), (320, 568),
]


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


# ── Lectura de css ──────────────────────────────────────────────────────────

def token_rgb(src, name):
    """Resuelve un token de color de tokens.css a (r, g, b, alpha)."""
    m = re.search(r"^\s*" + re.escape(name) + r"\s*:\s*([^;]+);", src, re.M)
    if not m:
        raise KeyError("token no encontrado: " + name)
    value = m.group(1).strip()

    m2 = re.fullmatch(r"#([0-9a-fA-F]{6})", value)
    if m2:
        h = m2.group(1)
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 1.0)

    m2 = re.fullmatch(r"var\((--[\w-]+)\)", value)
    if m2:
        return token_rgb(src, m2.group(1))

    m2 = re.fullmatch(r"rgb\(\s*var\((--[\w-]+)\)\s*/\s*([\d.]+)%\s*\)", value)
    if m2:
        comps = re.search(r"^\s*" + re.escape(m2.group(1)) + r"\s*:\s*([^;]+);",
                          src, re.M).group(1)
        r, g, b = [int(p) for p in comps.split()]
        return (r, g, b, float(m2.group(2)) / 100.0)

    raise ValueError("formato no soportado en %s: %s" % (name, value))


def rule_body(src, selector, inside_media=None):
    """Cuerpo del bloque `selector { ... }`. Si `inside_media` viene dado, solo
    busca dentro de esa `@media`."""
    scope = src
    if inside_media:
        i = src.find(inside_media)
        if i < 0:
            raise KeyError("no existe la media query " + inside_media)
        # Cierre de la @media: se cuentan llaves desde su apertura.
        j = src.index("{", i)
        depth, k = 1, j + 1
        while depth and k < len(src):
            if src[k] == "{":
                depth += 1
            elif src[k] == "}":
                depth -= 1
            k += 1
        scope = src[j:k]

    m = re.search(r"(?m)^\s*" + re.escape(selector) + r"\s*\{([^}]*)\}", scope)
    if not m:
        raise KeyError("no existe la regla " + selector)
    return m.group(1)


def gradients(body):
    """Todas las funciones `linear-gradient(...)` de una declaración
    `background-image`, en el orden en que se declaran (la primera va encima)."""
    m = re.search(r"background-image\s*:\s*(.+?);", body, re.S)
    if not m:
        raise KeyError("la regla no declara background-image")
    out, src = [], m.group(1)
    for start in [g.start() for g in re.finditer(r"linear-gradient\(", src)]:
        depth, i = 0, src.index("(", start)
        j = i
        while j < len(src):
            if src[j] == "(":
                depth += 1
            elif src[j] == ")":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        out.append(src[start:j + 1])
    return out


def parse_gradient(text, tokens_src):
    """(ángulo, unidad, [(posición, alpha)]) de un linear-gradient de ink.

    La unidad puede ser "pct" —posiciones 0..1 sobre el eje— o "px", y no es
    un detalle: el fundido inferior de móvil va en píxeles medidos desde el
    borde de abajo justamente para NO depender del alto del hero. Un lector
    que convirtiera los px a porcentaje se cargaría lo único que hace que ese
    degradado funcione en pantallas de alturas distintas.
    """
    angle = int(re.search(r"\((\d+)deg", text).group(1))
    found = re.findall(
        r"(var\(--ink\)|rgb\(var\(--rgb-ink\)\s*/\s*[\d.]+%\))\s+([\d.]+)(px|%)",
        text)
    if not found:
        raise ValueError("degradado sin paradas reconocibles: " + text[:60])

    unidades = {u for _, _, u in found}
    if len(unidades) > 1:
        raise ValueError("degradado con px y % mezclados: " + text[:60])
    unit = "px" if found[0][2] == "px" else "pct"

    stops = []
    for value, pos, _ in found:
        if value == "var(--ink)":
            alpha = 1.0
        else:
            alpha = float(re.search(r"/\s*([\d.]+)%", value).group(1)) / 100.0
        stops.append((float(pos) if unit == "px" else float(pos) / 100.0, alpha))
    return angle, unit, stops


def object_position(styles):
    """(x, y) de `object-position`, en fracción."""
    body = rule_body(styles, ".hero__media img")
    m = re.search(r"object-position\s*:\s*([\d.]+)%\s+([\d.]+)%", body)
    return float(m.group(1)) / 100.0, float(m.group(2)) / 100.0


def hero_height_fraction(tokens_src):
    """`--h-hero` en fracción de la altura de la ventana.

    El hero NO llena la pantalla: mide `--h-hero`. Da igual para el texto,
    pero no para la FOTO — cuanto más baja la caja, más recorte vertical hace
    `cover` y más cambian los píxeles que quedan detrás del texto. Medir
    contra la ventana entera daría un recorte que no existe."""
    m = re.search(r"^\s*--h-hero\s*:\s*([\d.]+)svh\s*;", tokens_src, re.M)
    if not m:
        raise KeyError("--h-hero no encontrado o no está en svh")
    return float(m.group(1)) / 100.0


# ── Color ───────────────────────────────────────────────────────────────────

def luminance(c):
    def channel(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * channel(c[0]) + 0.7152 * channel(c[1]) + 0.0722 * channel(c[2])


def contrast(fg, bg):
    a, b = luminance(fg), luminance(bg)
    if a < b:
        a, b = b, a
    return (a + 0.05) / (b + 0.05)


def flatten(rgba, backdrop):
    r, g, b, alpha = rgba
    return tuple(round((r, g, b)[i] * alpha + backdrop[i] * (1 - alpha))
                 for i in range(3))


def ramp(stops, t):
    if t <= stops[0][0]:
        return stops[0][1]
    if t >= stops[-1][0]:
        return stops[-1][1]
    for i in range(len(stops) - 1):
        p0, a0 = stops[i]
        p1, a1 = stops[i + 1]
        if p0 <= t <= p1:
            k = 0.0 if p1 == p0 else (t - p0) / (p1 - p0)
            return a0 + (a1 - a0) * k
    return stops[-1][1]


# ── Medición ────────────────────────────────────────────────────────────────

def cover(photo, cw, ch, pos):
    pos_x, pos_y = pos
    iw, ih = photo.size
    if cw / ch < iw / ih:
        w, h = round(ih * cw / ch), ih
    else:
        w, h = iw, round(iw * ch / cw)
    ox, oy = round(pos_x * (iw - w)), round(pos_y * (ih - h))
    from PIL import Image
    return photo.crop((ox, oy, ox + w, oy + h)).resize((cw, ch), Image.LANCZOS)


def brightest(frame, box, layers, ink):
    """Píxel más claro de `box` una vez compuestas las capas del velo."""
    cw, ch = frame.size
    px = frame.load()
    x0, y0, x1, y1 = box
    best, best_lum = None, -1.0
    for y in range(int(y0 * ch), min(int(y1 * ch), ch), 2):
        for x in range(int(x0 * cw), min(int(x1 * cw), cw), 2):
            alpha = 0.0
            for angle, unit, stops in layers:
                # 90deg → hacia la derecha, se lee sobre X.
                # 180deg → hacia abajo, sobre Y desde arriba.
                # 0deg → hacia arriba, sobre Y desde ABAJO.
                if angle == 90:
                    pos = x if unit == "px" else x / cw
                elif angle == 0:
                    pos = (ch - y) if unit == "px" else (ch - y) / ch
                else:
                    pos = y if unit == "px" else y / ch
                a = ramp(stops, pos)
                alpha = alpha + a - alpha * a          # apilado de capas
            c = flatten(ink + (alpha,), px[x, y][:3])
            lum = luminance(c)
            if lum > best_lum:
                best_lum, best = lum, c
    return best


def main():
    try:
        from PIL import Image
    except ImportError:
        print("Pillow no está instalado: se salta la comprobación de la foto.")
        print("Para activarla:  pip3 install Pillow")
        return 0

    styles, tokens = read(STYLES), read(TOKENS)
    ink = token_rgb(tokens, "--ink")[:3]
    pos = object_position(styles)
    hero_frac = hero_height_fraction(tokens)

    desktop_media = "@media (min-width: 60rem)"
    layers_mobile = [parse_gradient(g, tokens)
                     for g in gradients(rule_body(styles, ".hero__scrim"))]
    layers_desktop = [parse_gradient(g, tokens)
                      for g in gradients(rule_body(styles, ".hero__scrim",
                                                   desktop_media))]

    # Los tres colores que el hero pone encima de la foto. El azul es la parada
    # APAGADA del degradado de la palabra clave: el arranque del recorrido y
    # por tanto el peor punto de la palabra.
    probes = [
        ("nombre",  flatten(token_rgb(tokens, "--text-primary"), ink)),
        ("frase",   flatten(token_rgb(tokens, "--text-secondary"), ink)),
        ("palabra", flatten(token_rgb(tokens, "--accent-blue-deep"), ink)),
    ]

    photo = Image.open(PHOTO).convert("RGB")
    print("Contraste del texto del hero sobre %s\n" % os.path.relpath(PHOTO, ROOT))
    print("  encuadre: object-position %.0f%% %.0f%%   ·   alto del hero: %.0f%% "
          "de la ventana   ·   mínimo: %.1f:1\n"
          % (pos[0] * 100, pos[1] * 100, hero_frac * 100, MINIMUM))

    failures = 0
    for cw, cv in VIEWPORTS:
        # `ch` es la caja del HERO, no la ventana.
        ch = round(cv * hero_frac)
        if cw >= BREAKPOINT:
            layers = layers_desktop
            left_px = max(0.0, (cw - HERO_AXIS_PX) / 2) + gutter(cw)
            right_px = left_px + TEXT_CAP_PX
            if right_px / cw > SAFE_RIGHT:
                print("  AVISO  a %dpx el tope de la columna (%.0fpx) cruza el "
                      "límite del velo lateral (%.0fpx)."
                      % (cw, right_px, SAFE_RIGHT * cw))
            # El bloque ya no se centra: `margin-block-end: 17svh` lo sube
            # hasta el 41,5% de la altura. Medido en el navegador, el chip
            # arranca en el 28,8% y la frase termina en el 54,1%; la banda va
            # con holgura por los dos lados.
            box = (left_px / cw, 0.26, min(right_px / cw, 1.0), 0.58)
        else:
            layers = layers_mobile
            box = (0.04, max(0.0, 1 - TEXT_BLOCK_PX / ch), 0.96, 1.0)

        bg = brightest(cover(photo, cw, ch, pos), box, layers, ink)
        ratios = [(label, contrast(color, bg)) for label, color in probes]
        worst = min(r for _, r in ratios)
        ok = worst >= MINIMUM
        failures += 0 if ok else 1
        print("  %-4s %-9s %s  peor fondo rgb%-15s %s"
              % ("OK" if ok else "FALLA", "%dx%d" % (cw, cv),
                 "escritorio" if cw >= BREAKPOINT else "móvil     ",
                 str(bg),
                 "   ".join("%s %5.2f:1" % (l, r) for l, r in ratios)))

    print("")
    if failures:
        print("%d tamaño(s) por debajo del mínimo. Refuerza .hero__scrim en "
              "css/styles.css." % failures)
        return 1
    print("Todos los tamaños cumplen.")
    return 0


def gutter(cw):
    """`--sp-gutter`, resuelto: clamp(20px, 0.8333rem + 1.8519vw, 40px)."""
    return max(20.0, min(40.0, 13.333 + 0.018519 * cw))


if __name__ == "__main__":
    sys.exit(main())
