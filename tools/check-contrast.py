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
