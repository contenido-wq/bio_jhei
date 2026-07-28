/* ============================================================================
   main.js — Link in bio · Jhei Trujillo
   ---------------------------------------------------------------------------
   Sin dependencias, sin build, sin módulos ES (así el archivo también funciona
   abriendo index.html directamente desde el disco).

   Cada bloque es independiente y se degrada solo: si uno falla, los demás
   siguen. Y si el JS entero no carga, la página se ve completa y todos los
   enlaces funcionan — la clase `motion` que oculta cosas la pone un script
   inline en el <head>, no este archivo.

   Bloques:  1 Arranque · 2 Revelado al scroll · 3 Carrusel · 4 Año
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

  /* ══ 3 · CARRUSEL ════════════════════════════════════════════════════════
     La física la pone el navegador: scroll-snap nativo y el momentum del
     sistema, en el hilo de composición. Este bloque solo añade los dots, el
     arrastre con ratón, la navegación por teclado y el estado.

     Sin autoplay a propósito: contenido en movimiento de más de 5 segundos
     exige un control de pausa (WCAG 2.2.2), y aquí no aporta nada — deslizar,
     los dots y las flechas ya son la vía completa de navegación.            */
  (function carousel() {
    var track = document.querySelector("[data-carousel]");
    if (!track) return;

    var cards = Array.prototype.slice.call(track.children);
    var dotsHost = document.querySelector("[data-carousel-dots]");
    if (!cards.length) return;

    /* ── Dots ─────────────────────────────────────────────────────────── */
    var dots = [];
    if (dotsHost) {
      cards.forEach(function (card, i) {
        var dot = document.createElement("button");
        dot.type = "button";
        dot.className = "dot";
        dot.setAttribute("role", "tab");
        dot.setAttribute("aria-selected", "false");
        dot.setAttribute(
          "aria-label",
          "Colaboración " + (i + 1) + " de " + cards.length
        );
        dot.tabIndex = -1;
        dot.innerHTML =
          '<span class="dot__track" aria-hidden="true"><span></span><span></span></span>';
        dot.addEventListener("click", function () {
          goTo(i);
        });
        dotsHost.appendChild(dot);
        dots.push(dot);
      });
    }

    /* ── Geometría cacheada: nunca se lee layout dentro de un handler de
          scroll. Se recalcula solo cuando el tamaño cambia de verdad. ───── */
    var centers = [];
    function measure() {
      centers = cards.map(function (c) {
        return c.offsetLeft + c.offsetWidth / 2;
      });
    }
    measure();

    if ("ResizeObserver" in window) {
      new ResizeObserver(measure).observe(track);
    } else {
      window.addEventListener("resize", measure, { passive: true });
    }

    /* ── Estado, limitado a un rAF por frame ──────────────────────────── */
    var rafId = 0;
    var active = -1;

    function nearestIndex(scrollLeft) {
      var focus = scrollLeft + track.clientWidth / 2;
      var best = 0;
      var bestD = Infinity;
      for (var i = 0; i < centers.length; i++) {
        var d = Math.abs(centers[i] - focus);
        if (d < bestD) {
          bestD = d;
          best = i;
        }
      }
      return best;
    }

    function sync() {
      rafId = 0;
      var i = nearestIndex(track.scrollLeft);
      if (i === active) return;
      active = i;
      cards.forEach(function (card, k) {
        card.classList.toggle("is-focus", k === i);
      });
      dots.forEach(function (dot, k) {
        var on = k === i;
        dot.classList.toggle("is-active", on);
        dot.setAttribute("aria-selected", on ? "true" : "false");
        /* Roving tabindex: un solo tab stop en todo el grupo de dots. */
        dot.tabIndex = on ? 0 : -1;
      });
    }

    function queueSync() {
      if (!rafId) rafId = requestAnimationFrame(sync);
    }

    track.addEventListener("scroll", queueSync, { passive: true });
    if ("onscrollend" in window) track.addEventListener("scrollend", sync);
    sync();

    function goTo(i) {
      var idx = Math.max(0, Math.min(i, centers.length - 1));
      track.scrollTo({
        left: centers[idx] - track.clientWidth / 2,
        behavior: reduce.matches ? "auto" : "smooth"
      });
    }

    /* ── Teclado ──────────────────────────────────────────────────────── */
    track.addEventListener("keydown", function (e) {
      var handled = true;
      if (e.key === "ArrowRight") goTo(active + 1);
      else if (e.key === "ArrowLeft") goTo(active - 1);
      else if (e.key === "Home") goTo(0);
      else if (e.key === "End") goTo(centers.length - 1);
      else handled = false;
      if (handled) e.preventDefault();
    });

    if (dotsHost) {
      dotsHost.addEventListener("keydown", function (e) {
        var next = -1;
        if (e.key === "ArrowRight") next = Math.min(active + 1, dots.length - 1);
        else if (e.key === "ArrowLeft") next = Math.max(active - 1, 0);
        else if (e.key === "Home") next = 0;
        else if (e.key === "End") next = dots.length - 1;
        if (next < 0) return;
        e.preventDefault();
        goTo(next);
        /* El foco sigue al dot activo, que es el único tabulable. */
        requestAnimationFrame(function () {
          if (dots[next]) dots[next].focus();
        });
      });
    }

    /* ── Arrastre con ratón. En táctil manda el scroll nativo. ─────────── */
    var dragging = false;
    var startX = 0;
    var startScroll = 0;
    var lastX = 0;
    var lastT = 0;
    var velocity = 0;
    var travelled = 0;
    var suppressClick = false;

    var FLICK_MS = 130; /* el punto en que un flick corto avanza 1 card */
    var CLICK_SLOP = 6; /* por debajo es temblor de mano, no un gesto */

    track.addEventListener("pointerdown", function (e) {
      if (e.pointerType === "touch" || e.button !== 0) return;
      dragging = true;
      travelled = 0;
      velocity = 0;
      startX = lastX = e.clientX;
      startScroll = track.scrollLeft;
      lastT = e.timeStamp;
      track.setPointerCapture(e.pointerId);
      track.classList.add("is-dragging");
    });

    track.addEventListener("pointermove", function (e) {
      if (!dragging) return;
      var dx = e.clientX - lastX;
      var dt = Math.max(1, e.timeStamp - lastT);
      velocity = dx / dt; /* px/ms */
      lastX = e.clientX;
      lastT = e.timeStamp;
      travelled += Math.abs(dx);
      /* Ratio 1:1. Cualquier multiplicador mayor se siente resbaladizo y
         desconecta el cursor del contenido. */
      track.scrollLeft = startScroll - (e.clientX - startX);
      queueSync();
    });

    function endDrag(e) {
      if (!dragging) return;
      dragging = false;
      track.classList.remove("is-dragging");
      if (e && e.pointerId !== undefined && track.hasPointerCapture(e.pointerId)) {
        track.releasePointerCapture(e.pointerId);
      }
      suppressClick = travelled > CLICK_SLOP;
      /* El destino no es donde soltaste, es donde habrías llegado. */
      goTo(nearestIndex(track.scrollLeft - velocity * FLICK_MS));
    }

    track.addEventListener("pointerup", endDrag);
    track.addEventListener("pointercancel", endDrag);

    /* Arrastrar no debe activar nada dentro de una card. Fase de captura. */
    track.addEventListener(
      "click",
      function (e) {
        if (!suppressClick) return;
        e.preventDefault();
        e.stopPropagation();
        suppressClick = false;
      },
      true
    );
  })();

  /* ══ 4 · AÑO DEL FOOTER ══════════════════════════════════════════════════ */
  (function year() {
    var slot = document.querySelector("[data-year]");
    if (slot) slot.textContent = String(new Date().getFullYear());
  })();
})();
