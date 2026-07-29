#!/usr/bin/env python3
"""Genera los PNG placeholder en línea gráfica AIVI.

Cada placeholder vive en la ruta final que usará el archivo real, así que el
cliente solo tiene que sobrescribir el archivo: no hay que tocar el HTML.

Uso:  python3 tools/make-placeholders.py
Requisitos: ninguno, solo la librería estándar.
"""

import math
import os
import struct
import zlib

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "img")

INK = (16, 16, 16)
FIRE_RED = (255, 65, 59)
FIRE_ORANGE = (254, 128, 63)
FIRE_GOLD = (255, 194, 82)
PAPER = (250, 250, 250)


def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def fire_ramp(t):
    """Rampa rojo -> naranja -> dorado, igual que --gradient-fire."""
    t = max(0.0, min(1.0, t))
    if t < 0.5:
        return lerp(FIRE_RED, FIRE_ORANGE, t * 2)
    return lerp(FIRE_ORANGE, FIRE_GOLD, (t - 0.5) * 2)


def grain(x, y, amount):
    """Ruido determinista y barato: mismo resultado en cada ejecución.

    El grano se aplica en bloques de 2x2 px y cuantizado a pocos niveles. El grano
    por píxel se ve mejor, pero destruye la compresión PNG: la misma imagen pasaba
    de 60KB a casi 1MB. Como estos archivos se sirven en la página real hasta que el
    cliente los sustituya, el peso manda.
    """
    bx, by = x >> 1, y >> 1
    n = (bx * 374761393 + by * 668265263) & 0xFFFFFFFF
    n = (n ^ (n >> 13)) * 1274126177 & 0xFFFFFFFF
    step = max(1, round(amount / 2))
    return (((n >> 16) & 0xFF) // 64) * step - step * 1.5


def posterize(rgb, step=6):
    """Cuantiza el color para que el PNG comprima de verdad.

    A step=6 la banda es invisible sobre un fondo con grano, pero reduce
    drásticamente el número de colores únicos.
    """
    return tuple(min(255, (round(c / step) * step)) for c in rgb)


def write_png(path, width, height, pixel_fn):
    rows = []
    for y in range(height):
        row = bytearray()
        for x in range(width):
            r, g, b = posterize(pixel_fn(x, y, width, height))
            row += bytes((max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b))))
        rows.append(bytes(row))
    raw = b"".join(b"\x00" + r for r in rows)

    def chunk(tag, data):
        return (
            struct.pack(">I", len(data))
            + tag
            + data
            + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        )

    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    png = (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", header)
        + chunk(b"IDAT", zlib.compress(raw, 9))
        + chunk(b"IEND", b"")
    )
    with open(path, "wb") as fh:
        fh.write(png)
    print(f"  {os.path.relpath(path, os.path.dirname(OUT))}  {width}x{height}  {len(png) // 1024}KB")


def chevron_field(x, y, w, h, scale=0.42, weight=0.30):
    """Bandas en chevron inclinadas, la geometría del isotipo de AIVI."""
    nx, ny = x / w, y / h
    band = (nx * 1.0 + abs(ny - 0.5) * 1.6) / scale
    edge = abs((band % 1.0) - 0.5) * 2
    return 1.0 if edge > (1.0 - weight) else 0.0


def light_beam(x, y, w, h, angle=-24.0, center=0.5, width_=0.30):
    """Haz de luz diagonal con núcleo brillante."""
    rad = math.radians(angle)
    nx, ny = x / w - 0.5, y / h - 0.5
    d = nx * math.sin(rad) + ny * math.cos(rad) + (center - 0.5)
    falloff = max(0.0, 1.0 - abs(d) / width_)
    return falloff ** 2.4


# --- Placeholders -----------------------------------------------------------


def avatar(x, y, w, h):
    """Avatar circular: silueta de busto sobre un resplandor c\u00e1lido tenue.

    Se recorta a c\u00edrculo con las esquinas en negro, para que tambi\u00e9n se vea
    bien si alguna vez se usa sin el `border-radius` del CSS.
    """
    nx, ny = x / w, y / h
    if math.hypot(nx - 0.5, ny - 0.5) > 0.5:
        return INK
    beam = light_beam(x, y, w, h, angle=-30, center=0.58, width_=0.55)
    base = lerp(INK, fire_ramp(0.28 + beam * 0.5), beam * 0.5)
    head_dx, head_dy = (nx - 0.5) / 0.19, (ny - 0.36) / 0.22
    body_dx, body_dy = (nx - 0.5) / 0.42, (ny - 1.02) / 0.52
    if head_dx ** 2 + head_dy ** 2 < 1.0 or (body_dx ** 2 + body_dy ** 2 < 1.0 and ny > 0.5):
        base = (13, 13, 13)
    n = grain(x, y, 10)
    return tuple(round(c + n) for c in base)


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


def make_collab(seed):
    """Card de colaboración: retrato monocromo.

    Sin pie de fuego: ese degradado lo pinta el CSS. Si el placeholder lo
    trajera horneado, en la página se verían dos superpuestos.
    """

    def fn(x, y, w, h):
        nx, ny = x / w, y / h
        v = 26 + light_beam(x, y, w, h, angle=-14, center=0.35 + seed * 0.12, width_=0.6) * 96
        head_dx, head_dy = (nx - 0.5) / 0.22, (ny - 0.30) / 0.17
        body_dx, body_dy = (nx - 0.5) / 0.46, (ny - 0.98) / 0.55
        if head_dx ** 2 + head_dy ** 2 < 1.0 or (body_dx ** 2 + body_dy ** 2 < 1.0 and ny > 0.42):
            v = 116 + (0.5 - abs(nx - 0.5)) * 74
        base = (round(v), round(v), round(v))
        n = grain(x, y, 10)
        return tuple(round(c + n) for c in base)

    return fn


def og_image(x, y, w, h):
    beam = light_beam(x, y, w, h, angle=-24, center=0.70, width_=0.40)
    chev = chevron_field(x, y, w, h, scale=0.30, weight=0.26) * 0.06
    base = lerp(INK, fire_ramp(0.25 + beam * 0.6), beam * 0.9 + chev)
    n = grain(x, y, 12)
    return tuple(round(c + n) for c in base)


def main():
    os.makedirs(OUT, exist_ok=True)
    print("Generando placeholders en línea AIVI:")

    # El avatar es ahora la imagen principal de la página: se sirve a 196px de
    # ancho como máximo, así que 480px cubre pantallas de 2x con margen.
    write_png(os.path.join(OUT, "jhei-avatar.png"), 480, 480, avatar)

    # Retrato del hero. 4:5, se sirve a 420px de ancho como máximo, así que
    # 840px cubre pantallas de 2x. El cliente lo sustituye por una foto real
    # de medio cuerpo con el mismo nombre y no hay que tocar el HTML.
    write_png(os.path.join(OUT, "jhei-portrait.png"), 840, 1050, portrait)

    for i in range(1, 7):
        write_png(os.path.join(OUT, f"collab-{i}.png"), 420, 640, make_collab((i - 1) / 5))

    write_png(os.path.join(OUT, "og-image.png"), 1200, 630, og_image)
    print("Listo. Sobrescribe cualquier archivo con el real y la página lo toma.")


if __name__ == "__main__":
    main()
