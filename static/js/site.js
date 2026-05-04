(function () {
  const root = document.documentElement;
  root.classList.add("js");

  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const mobileViewport = window.matchMedia("(max-width: 991.98px)").matches;
  const isTrabajosRoute = /^\/trabajos(\/|$)/.test(window.location.pathname);
  const revealItems = Array.from(document.querySelectorAll(".reveal"));

  if (prefersReducedMotion || (mobileViewport && isTrabajosRoute) || !("IntersectionObserver" in window)) {
    revealItems.forEach((item) => item.classList.add("is-visible"));
  } else {
    const observer = new IntersectionObserver(
      (entries, obs) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-visible");
          obs.unobserve(entry.target);
        });
      },
      {
        threshold: 0.14,
        rootMargin: "0px 0px -8% 0px",
      }
    );

    revealItems.forEach((item) => observer.observe(item));
  }

  const interactiveSelector = ".btn, .page-link, .project-card a, .navbar a";

  document.addEventListener("pointerdown", (event) => {
    const target = event.target.closest(interactiveSelector);
    if (!target) return;
    target.classList.add("is-pressed");
  });

  const clearPress = (event) => {
    const target = event.target.closest(interactiveSelector);
    if (!target) return;
    target.classList.remove("is-pressed");
  };

  document.addEventListener("pointerup", clearPress);
  document.addEventListener("pointercancel", clearPress);

  const nav = document.querySelector(".site-nav");
  const navCollapse = document.getElementById("navbarSupportedContent");
  const navOverlay = document.getElementById("navOverlay");
  const navToggler = nav ? nav.querySelector(".navbar-toggler") : null;

  if (nav && navCollapse && navOverlay && navToggler && typeof bootstrap !== "undefined") {
    const collapseApi = bootstrap.Collapse.getOrCreateInstance(navCollapse, { toggle: false });
    const mobileMq = window.matchMedia("(max-width: 991.98px)");
    let lockedScrollY = 0;
    const isMobileNavContext = () => mobileMq.matches && window.getComputedStyle(navToggler).display !== "none";

    const updateOverlayTop = () => {
      document.documentElement.style.setProperty("--nav-overlay-top", `${nav.offsetHeight}px`);
    };

    const lockBodyScroll = () => {
      if (document.body.classList.contains("nav-menu-open")) return;
      lockedScrollY = window.scrollY || window.pageYOffset;
      document.body.classList.add("nav-menu-open");
      document.body.style.position = "fixed";
      document.body.style.top = `-${lockedScrollY}px`;
      document.body.style.left = "0";
      document.body.style.right = "0";
      document.body.style.width = "100%";
    };

    const unlockBodyScroll = (restoreScroll = true) => {
      const hadLock =
        document.body.classList.contains("nav-menu-open") || document.body.style.position === "fixed";
      if (!hadLock) return;
      const inlineTop = parseInt(document.body.style.top || "0", 10);
      const restoreY = Number.isFinite(inlineTop) ? Math.abs(inlineTop) : lockedScrollY;
      document.body.classList.remove("nav-menu-open");
      document.body.style.position = "";
      document.body.style.top = "";
      document.body.style.left = "";
      document.body.style.right = "";
      document.body.style.width = "";
      if (restoreScroll) {
        window.scrollTo(0, restoreY || 0);
      }
    };

    const showOverlay = () => {
      if (!isMobileNavContext()) {
        hideOverlay(false);
        return;
      }
      updateOverlayTop();
      navOverlay.classList.add("is-visible");
      navOverlay.setAttribute("aria-hidden", "false");
      lockBodyScroll();
    };

    const hideOverlay = (restoreScroll = true) => {
      navOverlay.classList.remove("is-visible");
      navOverlay.setAttribute("aria-hidden", "true");
      unlockBodyScroll(restoreScroll);
    };

    const resetDesktopNavbar = () => {
      if (isMobileNavContext()) return;
      hideOverlay(false);
      if (navCollapse.classList.contains("show") || navCollapse.classList.contains("collapsing")) {
        collapseApi.hide();
      }
      navCollapse.classList.remove("show", "collapsing");
      navToggler.setAttribute("aria-expanded", "false");
      navCollapse.style.height = "";
      navCollapse.style.overflow = "";
      navCollapse.style.transition = "";
    };

    navCollapse.addEventListener("shown.bs.collapse", showOverlay);
    navCollapse.addEventListener("hidden.bs.collapse", hideOverlay);

    navOverlay.addEventListener("click", () => {
      if (!isMobileNavContext()) return;
      collapseApi.hide();
    });

    navCollapse.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => {
        if (!isMobileNavContext()) return;
        collapseApi.hide();
      });
    });

    window.addEventListener("resize", () => {
      updateOverlayTop();
      if (!isMobileNavContext()) {
        resetDesktopNavbar();
      }
    });

    const handleBreakpointChange = (event) => {
      if (event.matches) return;
      resetDesktopNavbar();
    };

    if (typeof mobileMq.addEventListener === "function") {
      mobileMq.addEventListener("change", handleBreakpointChange);
    } else if (typeof mobileMq.addListener === "function") {
      mobileMq.addListener(handleBreakpointChange);
    }

    updateOverlayTop();
    resetDesktopNavbar();
  }
})();
