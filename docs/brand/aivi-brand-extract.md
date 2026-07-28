# Línea gráfica AIVI — extracto de la guía de uso

Extraído de `AV-GuiaDeUso.pdf`. Esta es la fuente de verdad del sistema visual.
**El logo y el isotipo de AIVI NO se usan en este proyecto.** Solo se hereda paleta,
tipografía y lenguaje visual.

## Paleta oficial

| Nombre | HEX | RGB | CMYK | Rol declarado en la guía |
|---|---|---|---|---|
| Negro | `#101010` | 16 16 16 | 80/70/62/89 | "representa inteligencia y control" |
| Blanco | `#FAFAFA` | 250 250 250 | 2/2/1/0 | "simplicidad y entendimiento" |
| Naranja | `#FE803F` | 254 128 63 | 0/61/76/0 | tono de acción |
| Dorado | `#FFC252` | 255 194 82 | 0/28/74/0 | tono de acción |
| Rojo | `#FF413B` | 255 65 59 | 0/84/71/0 | tono de acción |

Cita textual de la guía: *"La paleta de AIVI combina tecnología, claridad y acción.
El negro representa inteligencia y control. El blanco, simplicidad y entendimiento."*

## Tipografía

**Hanken Grotesk** — pesos declarados en la guía: Thin, Light, Bold, Black.
Disponible en Google Fonts (variable 100–900). Sin tipografía secundaria.

## Lenguaje visual observado en las piezas

- Fondo casi negro, nunca negro puro (`#101010`), con caída a negro en los bordes.
- Geometría derivada del isotipo: **chevrones y hexágonos con esquinas redondeadas**,
  inclinados aprox. 20–25°, usados a gran escala y recortados por el lienzo.
- **Haces de luz cálida** naranja→rojo→dorado que cruzan la composición en diagonal,
  con un núcleo casi blanco donde la luz es más intensa.
- **Paneles tipo vidrio**: superficies apenas más claras que el fondo, con borde
  translúcido de 1px y desenfoque. Nunca cajas opacas grises.
- **Grano fino** sobre todo el fondo: le quita el aspecto plano y digital al degradado.
- Jerarquía de texto: titular en blanco, y la última línea o palabra clave en el
  degradado de fuego (ej. "Únete a **AIVI**" con "Únete a" en rojo y "AIVI" en dorado).
- Tono general: cálido, tecnológico, con contraste alto. Nada pastel, nada frío.

## Referencias visuales en esta carpeta

- `ref-aivi-social.png` — pieza social: fondo, haces de luz, chevrones, jerarquía de texto.
- `ref-aivi-web.png` — mockup del sitio de AIVI: botón degradado, hero, nav.
- `ref-aivi-isotipo.png` — isotipo, solo para entender la geometría. **No usar.**
- `ref-layout-hero.png` — referente de layout que el cliente quiere replicar (arriba).
- `ref-layout-bio.png` — referente de layout (abajo: carrusel, bio, redes, footer).

Los dos `ref-layout-*` están en morado porque son de otro autor (Jhonny Lubo). Se
replica su **arquitectura y ritmo**, no su color: el morado se sustituye por el fuego
de AIVI.
