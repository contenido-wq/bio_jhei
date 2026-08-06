#!/usr/bin/env python3
"""Verifica los contrastes WCAG declarados en css/tokens.css.

Lee los valores REALES del archivo, nunca copias hardcodeadas: si alguien
cambia un token, este script se entera. Solo librería estándar.

Comprueba dos familias de contraste:

  · Textual (WCAG 1.4.3), mínimo 4.5:1 — un texto tiene que poder leerse.

  · NO textual (WCAG 1.4.11), mínimo 3:1 — un trazo, un borde o un icono
    tiene que poder VERSE como límite de un control, aunque no haya letras
    de por medio. Esta página apoya la señal de "esto es un control" en el
    trazo en degradado (`.stroke`) de las redes, las filas secundarias, las
    cards de colaboraciones y el retrato del hero; en `.social` el trazo es
    la ÚNICA señal (el fondo de vidrio mide 1.10:1, muy por debajo del
    mínimo), así que ninguna parada de ese degradado puede caer por debajo
    de 3:1 contra el fondo sobre el que se pinta.

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
    ("plata de acento sobre el fondo", "--text-accent", "--ink", 4.5),
    # Palabra clave en azul. Se mide la parada APAGADA del degradado, que es
    # el arranque del recorrido y por tanto el peor punto de la palabra.
    ("azul de palabra clave, parada apagada", "--accent-blue-deep", "--ink", 4.5),
    ("azul de palabra clave, parada plena", "--accent-blue", "--ink", 4.5),
    ("texto sobre el relleno, extremo rojo", "--text-on-fire", "--fire-red", 4.5),
    ("texto sobre el relleno, extremo naranja", "--text-on-fire", "--fire-orange", 4.5),
    ("texto sobre el relleno, extremo dorado", "--text-on-fire", "--fire-gold", 4.5),
    ("subtítulo sobre el relleno, extremo rojo", "--text-on-fire-soft", "--fire-red", 4.5),
    ("subtítulo sobre el relleno, extremo dorado", "--text-on-fire-soft", "--fire-gold", 4.5),
    # Los dos rellenos de acento de las filas de taller. Se miden las paradas
    # -deep y -lit de cada degradado: la profunda es el punto de MENOR
    # contraste de todo el recorrido y por tanto la que decide si el texto
    # negro es legible; la clara se mide igualmente para dejar constancia del
    # otro extremo. La parada intermedia queda entre ambas por construcción.
    ("texto sobre el relleno estética, parada profunda",
     "--text-on-fill", "--accent-aesthetic-deep", 4.5),
    ("texto sobre el relleno estética, parada clara",
     "--text-on-fill", "--accent-aesthetic-lit", 4.5),
    ("subtítulo sobre el relleno estética, parada profunda",
     "--text-on-fill-soft", "--accent-aesthetic-deep", 4.5),
    ("texto sobre el relleno ventas, parada profunda",
     "--text-on-fill", "--accent-sales-deep", 4.5),
    ("texto sobre el relleno ventas, parada clara",
     "--text-on-fill", "--accent-sales-lit", 4.5),
    ("subtítulo sobre el relleno ventas, parada profunda",
     "--text-on-fill-soft", "--accent-sales-deep", 4.5),
]

# Contraste NO TEXTUAL (WCAG 1.4.11) del trazo en degradado contra --ink, que
# es el fondo real sobre el que se pinta en los cuatro hosts de `.stroke`
# (`.social`, las filas secundarias, `.collab` y `.hero__portrait`). Cada
# parada del degradado se mide por separado: el navegador nunca compone un
# color plano equivalente, así que una parada floja en un extremo no queda
# disimulada por las otras dos.
STROKE_MINIMUM = 3.0
STROKE_STOPS = [
    ("trazo en reposo, parada clara", 0),
    ("trazo en reposo, parada apagada", 1),
    ("trazo en reposo, parada de cierre", 2),
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


def gradient_stops(src, name):
    """Extrae las paradas `rgb(var(--rgb-x) / NN%)` de un token gradiente,
    en el orden en que aparecen. Devuelve una lista de (r, g, b, alpha)."""
    value = raw_token(src, name)
    if value is None:
        raise KeyError("token no encontrado en tokens.css: " + name)

    stops = re.findall(r"rgb\(\s*var\((--[\w-]+)\)\s*/\s*([\d.]+)%\s*\)", value)
    if not stops:
        raise ValueError("no se encontraron paradas rgb(var(...)/NN%) en " + name)

    result = []
    for comp_name, alpha in stops:
        comps = raw_token(src, comp_name)
        if comps is None:
            raise KeyError("token de componentes no encontrado: " + comp_name)
        parts = [int(p) for p in comps.split()]
        result.append((parts[0], parts[1], parts[2], float(alpha) / 100.0))
    return result


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

    print("\nContraste NO TEXTUAL · trazo en degradado contra --ink\n")

    try:
        ink = resolve(src, "--ink")
        stops = gradient_stops(src, "--grad-stroke")
    except (KeyError, ValueError) as err:
        print("  FALLA  %-44s  %s" % ("trazo en degradado", err))
        failures += 1
        stops = []

    for label, idx in STROKE_STOPS:
        if idx >= len(stops):
            print("  FALLA  %-44s  parada %d no encontrada en --grad-stroke"
                  % (label, idx))
            failures += 1
            continue

        ratio = contrast(composite(stops[idx], ink), ink)
        ok = ratio >= STROKE_MINIMUM
        print("  %-5s  %-44s  %5.2f:1  (mínimo %.1f)"
              % ("OK" if ok else "FALLA", label, ratio, STROKE_MINIMUM))
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
