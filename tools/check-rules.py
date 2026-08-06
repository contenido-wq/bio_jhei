#!/usr/bin/env python3
"""Guardas estáticas del sistema de diseño.

Cinco reglas que el rediseño no puede romper. Solo librería estándar.

Uso:  python3 tools/check-rules.py
Sale con 1 si alguna regla se incumple.
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STYLES = os.path.join(ROOT, "css", "styles.css")
TOKENS = os.path.join(ROOT, "css", "tokens.css")

# La mayúscula sostenida ya no está prohibida del todo: está ACOTADA.
#
# Lo estuvo, y con motivo. Hubo una lista blanca para la micro-insignia
# "Disponible" del hero; la insignia se retiró, la excepción sobrevivió
# apuntando a un selector que ya no existía, y ese permiso muerto dejó pasar
# una regresión real. La lección de aquello no fue "las versales son malas",
# fue "un permiso que nombra un selector deja de proteger en cuanto el
# selector cambia de nombre".
#
# Así que este permiso no nombra selectores. Describe la única forma tipográfica
# en la que las versales hacen un trabajo real —la etiqueta micro: pequeña,
# monoespaciada y muy espaciada— y exige las tres condiciones a la vez. Un
# titular en versales no puede colarse porque no puede cumplirlas: en cuanto
# alguien sube el cuerpo o quita el tracking, el bloque falla.
#
# Las tres condiciones se buscan DENTRO del mismo bloque de declaración, no en
# la hoja entera.
UPPERCASE_MAX_FONT_SIZE = "--fs-micro"     # el escalón más pequeño de la escala
UPPERCASE_REQUIRED_FAMILY = "--font-mono"
UPPERCASE_MIN_TRACKING = ("--ls-wider", "--ls-widest")  # 0.12em y 0.16em

# Los cinco colores de marca. styles.css los consume por token, nunca por hex.
# `--ink` dejó de ser #101010 al pasar el fondo a negro azulado; el token nuevo
# entra en la lista para que siga sin poder escribirse a mano.
BRAND_HEXES = ["#080b12", "#fafafa", "#ff413b", "#fe803f", "#ffc252"]


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


def declaration_block(lines, index):
    """Las líneas del bloque `{ ... }` que contiene la línea `index`."""
    start = index
    while start > 0 and not lines[start].strip().endswith("{"):
        start -= 1
    end = index
    while end < len(lines) - 1 and "}" not in lines[end]:
        end += 1
    return lines[start:end + 1]


def rule_uppercase(src):
    """1 · Versales SOLO en la forma de etiqueta micro.

    Se exigen las tres condiciones a la vez y en el mismo bloque. Que sean
    tres no es celo: cada una sola se rompe sin querer. Cuerpo pequeño sin
    tracking da un amasijo ilegible; tracking sin monoespaciada no cambia de
    registro; monoespaciada a cuerpo grande es un titular en versales, que es
    justo lo que esta regla existe para impedir.
    """
    lines = src.splitlines()
    offenders = []
    for i, line in enumerate(lines):
        if "text-transform" not in line or "uppercase" not in line:
            continue

        selector = enclosing_selector(lines, i)
        block = "\n".join(declaration_block(lines, i))
        faltan = []

        if UPPERCASE_MAX_FONT_SIZE not in block:
            faltan.append("no usa %s" % UPPERCASE_MAX_FONT_SIZE)
        if UPPERCASE_REQUIRED_FAMILY not in block:
            faltan.append("no usa %s" % UPPERCASE_REQUIRED_FAMILY)
        if not any(t in block for t in UPPERCASE_MIN_TRACKING):
            faltan.append("no usa %s" % " ni ".join(UPPERCASE_MIN_TRACKING))

        if faltan:
            offenders.append(
                "línea %d, selector %s → %s" % (i + 1, selector, "; ".join(faltan))
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


def rule_comments_balanced(src, path):
    """5 · Ningún comentario CSS mal cerrado.

    Existe porque este fallo ya se coló DOS veces en el mismo archivo, y las
    dos de la misma forma: al reescribir el comentario de un token se dejó el
    `*/` viejo, y la prosa que venía detrás quedó suelta en mitad de la hoja.

    Lo peligroso no es el error, es su síntoma. CSS no avisa: descarta en
    silencio desde la basura hasta el siguiente punto y coma, así que el token
    que venía justo después se queda VACÍO. La primera vez se llevó por delante
    el relleno de una fila entera; la segunda, la palabra clave del hero, que
    quedó invisible porque su color es `transparent` y el degradado que la
    pintaba había desaparecido.

    Ninguna de las otras comprobaciones lo detecta —el contraste lee el
    archivo como texto, no como CSS— y en pantalla se ve como "algo no se
    pinta", que manda a buscar a cualquier otro sitio.
    """
    offenders = []
    i = 0
    dentro = False
    while i < len(src):
        if src.startswith("/*", i):
            if dentro:
                linea = src[:i].count("\n") + 1
                offenders.append("línea %d: se abre un comentario dentro de otro" % linea)
            dentro = True
            i += 2
            continue
        if src.startswith("*/", i):
            if not dentro:
                linea = src[:i].count("\n") + 1
                offenders.append("línea %d: `*/` sin comentario abierto" % linea)
            dentro = False
            i += 2
            continue
        i += 1
    if dentro:
        offenders.append("el archivo termina con un comentario sin cerrar")
    return ["%s · %s" % (os.path.basename(path), o) for o in offenders]


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
    ("Versales solo en la forma de etiqueta micro", rule_uppercase),
    ("Cero hex de marca literal en styles.css", rule_no_brand_hex),
    ("Cero capas GPU propias en el fondo", rule_backdrop_no_gpu),
    ("Reserva @supports para mask-composite", rule_mask_fallback),
]


def main():
    src = read(STYLES)
    failures = 0
    print("Reglas del sistema de diseño · css/styles.css + css/tokens.css\n")

    for label, check in RULES:
        offenders = check(src)
        if offenders:
            failures += 1
            print("  FALLA  %s" % label)
            for offender in offenders:
                print("           · %s" % offender)
        else:
            print("  OK     %s" % label)

    # Esta va sobre LOS DOS archivos: las dos veces que se rompió un comentario
    # fue en tokens.css, que las demás reglas ni miran.
    balance = []
    for path in (STYLES, TOKENS):
        balance += rule_comments_balanced(read(path), path)
    if balance:
        failures += 1
        print("  FALLA  Comentarios CSS bien cerrados")
        for offender in balance:
            print("           · %s" % offender)
    else:
        print("  OK     Comentarios CSS bien cerrados")

    print("")
    if failures:
        print("%d regla(s) incumplida(s)." % failures)
        return 1
    print("Todas las reglas se cumplen.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
