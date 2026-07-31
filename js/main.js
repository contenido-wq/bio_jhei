/* ============================================================================
   main.js — Link in bio · Jhei Trujillo
   ---------------------------------------------------------------------------
   Sin dependencias, sin build, sin módulos ES (así el archivo también funciona
   abriendo index.html directamente desde el disco).

   Cada bloque es independiente y se degrada solo: si uno falla, los demás
   siguen. Y si el JS entero no carga, la página se ve completa y todos los
   enlaces funcionan — la clase `motion` que oculta cosas la pone un script
   inline en el <head>, no este archivo.

   Bloques:  1 Arranque · 2 Revelado al scroll · 3 Cintas en bucle · 4 Año
   ========================================================================= */

(function () {
  "use strict";

  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)");
  var root = document.documentElement;

  /* ══ 1 · ARRANQUE ════════════════════════════════════════════════════════
     Se espera a que las fuentes estén listas para que el texto no salte de
     métrica a mitad de la animación, pero con un techo de 350ms: la
     impaciencia del visitante manda sobre la pulcritud tipográfica.

     `is-entered` apaga las animaciones de entrada cuando acaban. No es
     cosmético: `animation-fill-mode: both` deja fijado el transform del último
     keyframe y, en la cascada, una animación gana siempre a una declaración
     — sin ese apagado los :hover de las filas no volverían a mover nada.     */
  function boot() {
    if (reduce.matches) {
      root.classList.add("is-ready", "is-entered");
      return;
    }
    /* Doble rAF: garantiza que los estilos iniciales ya se aplicaron antes del
       cambio de clase, para que la animación se vea desde el frame 0. */
    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        root.classList.add("is-ready");
        /* La última entrada (la tercera fila) cierra a los 880ms. */
        setTimeout(function () {
          root.classList.add("is-entered");
        }, 1100);
      });
    });
  }

  var fontsReady = document.fonts ? document.fonts.ready : Promise.resolve();
  Promise.race([
    fontsReady,
    new Promise(function (resolve) {
      setTimeout(resolve, 350);
    })
  ]).then(boot, boot);

  /* ══ 2 · REVELADO AL SCROLL ══════════════════════════════════════════════ */
  (function reveal() {
    var targets = document.querySelectorAll("[data-reveal], [data-reveal-stagger]");
    if (!targets.length) return;

    function showAll() {
      Array.prototype.forEach.call(targets, function (el) {
        el.classList.add("is-revealed");
      });
    }

    /* Sin IntersectionObserver o con reduced-motion: todo visible, sin
       excepciones. Nunca se deja contenido oculto esperando un observador. */
    if (reduce.matches || !("IntersectionObserver" in window)) {
      showAll();
      return;
    }

    /* Índice de cascada para los hijos de un grupo, sin tocar el layout. */
    Array.prototype.forEach.call(
      document.querySelectorAll("[data-reveal-stagger]"),
      function (group) {
        Array.prototype.forEach.call(group.children, function (child, i) {
          child.style.setProperty("--i", String(Math.min(i, 6)));
        });
      }
    );

    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-revealed");
          io.unobserve(entry.target); /* un solo disparo: nunca se re-oculta */
        });
      },
      {
        /* threshold 0 a propósito: con un bloque más alto que el viewport (la
           bio en móvil) un ratio de 0.15 puede no dispararse nunca. El retardo
           lo aporta el rootMargin negativo, no el ratio. */
        threshold: 0,
        rootMargin: "0px 0px -12% 0px"
      }
    );

    Array.prototype.forEach.call(targets, function (el) {
      io.observe(el);
    });

    /* Red de seguridad: si el navegador restaura la posición de scroll antes de
       que el observador se registre, forzamos una comprobación. */
    window.addEventListener(
      "load",
      function () {
        requestAnimationFrame(function () {
          Array.prototype.forEach.call(targets, function (el) {
            var r = el.getBoundingClientRect();
            if (r.top < window.innerHeight && r.bottom > 0) {
              el.classList.add("is-revealed");
            }
          });
        });
      },
      { once: true }
    );
  })();

  /* ══ 3 · CINTA DE COLABORACIONES ════════════════════════════════════════
     El bucle continuo necesita el set duplicado: con dos copias el track mide
     el doble y desplazarlo un 50% recorre exactamente una copia, así que el
     salto del final del ciclo es invisible. La copia va aria-hidden porque es
     la MISMA información y un lector de pantalla no debe leerla dos veces.

     AVISO: sin control visible de pausa, por decisión de diseño del cliente.
     WCAG 2.2.2 exige poder detener el movimiento automático de más de 5
     segundos y el :hover no cumple para táctil. Queda cubierto el ratón, el
     teclado y quien pide movimiento reducido en su sistema.

     Sin JS no se clona nada, no se añade `is-looped` y la cinta se queda
     quieta y recorrible a mano.                                            */
  (function ribbon() {
    var cinta = document.querySelector("[data-ribbon-cards]");
    if (!cinta) return;

    var set = cinta.querySelector(".ribbon__set");
    if (!set) return;

    var copia = set.cloneNode(true);
    copia.setAttribute("aria-hidden", "true");
    set.parentNode.appendChild(copia);
    cinta.classList.add("is-looped");
  })();

  /* ══ 4 · AÑO DEL FOOTER ══════════════════════════════════════════════════ */
  (function year() {
    var slot = document.querySelector("[data-year]");
    if (slot) slot.textContent = String(new Date().getFullYear());
  })();
})();
