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

# La mayúscula sostenida está prohibida SIN excepción. Hubo una lista blanca
# para la micro-insignia "Disponible" del hero, pero esa insignia se retiró y
# la excepción sobrevivió apuntando a un selector inexistente: un permiso que
# ya no protegía nada y que dejó pasar una regresión real. Cero es cero.

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
    """1 · Cero mayúscula sostenida, sin excepciones."""
    lines = src.splitlines()
    offenders = []
    for i, line in enumerate(lines):
        if "text-transform" not in line or "uppercase" not in line:
            continue
        offenders.append(
            "línea %d, selector %s" % (i + 1, enclosing_selector(lines, i))
        )
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
    ("Cero mayúscula sostenida, sin excepciones", rule_uppercase),
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
