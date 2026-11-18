/* =========================================================================
   3RD Company — interface behaviour
   - language switch (EN / 中文)
   - text size control (100% – 140%)
   - colour theme switch (light / dark), remembered per browser
   - mobile navigation
   - accessible contact-form validation
   Preferences live in localStorage only; nothing is sent anywhere.
   ========================================================================= */

(function () {
  "use strict";

  var root = document.documentElement;
  var KEY = "3rd-prefs";
  var SIZES = [100, 110, 125, 140];
  var state = {
    lang: "en",
    theme: "light",
    size: 100,
    themeChosen: false
  };

  /* ------------------------------------------------------------ storage */

  function readPrefs() {
    try {
      var raw = localStorage.getItem(KEY);
      return raw ? JSON.parse(raw) || {} : null;
    } catch (e) {
      return null;
    }
  }

  function savePrefs() {
    try {
      localStorage.setItem(
        KEY,
        JSON.stringify({
          lang: state.lang,
          theme: state.theme,
          size: state.size
        })
      );
    } catch (e) {
      /* private mode or storage full: the page still works */
    }
  }

  /* --------------------------------------------------------- announcing */

  function announce(en, zh) {
    var live = document.getElementById("a11y-status");
    if (!live) return;
    live.textContent = "";
    window.setTimeout(function () {
      live.textContent = state.lang === "zh" ? zh : en;
    }, 60);
  }

  /* ------------------------------------------------------------ language */

  function applyLang(lang, notify) {
    state.lang = lang === "zh" ? "zh" : "en";
    root.setAttribute("data-lang", state.lang);
    root.setAttribute("lang", state.lang === "zh" ? "zh-Hant" : "en");

    var stored = root.getAttribute("data-title-" + state.lang);
    if (stored) document.title = stored;

    document.querySelectorAll("[data-lang-set]").forEach(function (btn) {
      btn.setAttribute(
        "aria-pressed",
        btn.getAttribute("data-lang-set") === state.lang ? "true" : "false"
      );
    });

    document.querySelectorAll("[data-aria-en][data-aria-zh]").forEach(function (el) {
      el.setAttribute(
        "aria-label",
        el.getAttribute(state.lang === "zh" ? "data-aria-zh" : "data-aria-en")
      );
    });

    /* <option> cannot hold spans, so its text is swapped instead */
    document.querySelectorAll("option[data-opt-en]").forEach(function (opt) {
      var label = opt.getAttribute(state.lang === "zh" ? "data-opt-zh" : "data-opt-en");
      if (label) opt.textContent = label;
    });

    updateThemeButton();

    if (notify) {
      announce(
        "Language changed to English.",
        "已切換至中文。"
      );
    }
  }

  /* ---------------------------------------------------------- text size */

  function sizeLabel(size) {
    return size + "%";
  }

  function applySize(size, notify) {
    var index = SIZES.indexOf(size);
    if (index === -1) {
      /* snap to the nearest allowed step */
      index = 0;
      var best = Infinity;
      SIZES.forEach(function (s, i) {
        var d = Math.abs(s - size);
        if (d < best) {
          best = d;
          index = i;
        }
      });
    }
    state.size = SIZES[index];
    root.style.fontSize = sizeLabel(state.size);
    root.setAttribute("data-size", String(state.size));

    document.querySelectorAll("[data-size-value]").forEach(function (el) {
      el.textContent = sizeLabel(state.size);
    });

    var dec = document.querySelector('[data-size-step="-1"]');
    var inc = document.querySelector('[data-size-step="1"]');
    if (dec) dec.disabled = index === 0;
    if (inc) inc.disabled = index === SIZES.length - 1;

    if (notify) {
      announce(
        "Text size " + state.size + " percent.",
        "字級 " + state.size + "%。"
      );
    }
  }

  /* --------------------------------------------------------------- theme */

  function updateThemeButton() {
    var btn = document.querySelector("[data-theme-toggle]");
    if (!btn) return;
    var dark = state.theme === "dark";
    btn.setAttribute(
      "aria-label",
      state.lang === "zh"
        ? dark
          ? "切換至淺色主題"
          : "切換至深色主題"
        : dark
          ? "Switch to light theme"
          : "Switch to dark theme"
    );
    btn.setAttribute("aria-pressed", dark ? "true" : "false");
    btn.setAttribute("title", dark ? "Light / 淺色" : "Dark / 深色");
  }

  function applyTheme(theme, notify) {
    state.theme = theme === "dark" ? "dark" : "light";
    root.setAttribute("data-theme", state.theme);
    root.style.colorScheme = state.theme;

    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute("content", state.theme === "dark" ? "#0a1310" : "#ffffff");

    updateThemeButton();

    if (notify) {
      announce(
        state.theme === "dark" ? "Dark theme on." : "Light theme on.",
        state.theme === "dark" ? "已開啟深色主題。" : "已開啟淺色主題。"
      );
    }
  }

  /* ---------------------------------------------------------- navigation */

  function initNav() {
    var toggle = document.querySelector(".nav-toggle");
    var nav = document.getElementById("site-nav");
    if (!toggle || !nav) return;

    function setOpen(open) {
      nav.classList.toggle("is-open", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    }

    toggle.addEventListener("click", function () {
      setOpen(toggle.getAttribute("aria-expanded") !== "true");
    });

    nav.addEventListener("click", function (event) {
      if (event.target.closest("a")) setOpen(false);
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
        setOpen(false);
        toggle.focus();
      }
    });

    document.addEventListener("click", function (event) {
      if (
        toggle.getAttribute("aria-expanded") === "true" &&
        !nav.contains(event.target) &&
        !toggle.contains(event.target)
      ) {
        setOpen(false);
      }
    });

    window.addEventListener("resize", function () {
      if (window.innerWidth >= 900) setOpen(false);
    });
  }

  /* --------------------------------------------------------------- forms */

  function errorFor(field) {
    return document.getElementById(field.id + "-error");
  }

  function validateField(field) {
    var value = (field.value || "").trim();
    var valid = true;
    var message = "";

    if (field.type === "checkbox") {
      valid = field.checked;
      if (!valid) message = "required";
    } else if (field.required && !value) {
      valid = false;
      message = "required";
    } else if (field.type === "email" && value) {
      valid = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(value);
      if (!valid) message = "email";
    }

    var err = errorFor(field);
    if (err) {
      if (valid) {
        err.hidden = true;
      } else {
        var emailIssue = message === "email";
        err.hidden = false;
        err.querySelectorAll(".error-required").forEach(function (n) {
          n.hidden = emailIssue;
        });
        err.querySelectorAll(".error-email").forEach(function (n) {
          n.hidden = !emailIssue;
        });
      }
    }

    field.setAttribute("aria-invalid", valid ? "false" : "true");

    return valid;
  }

  function initContactForm() {
    var form = document.querySelector("[data-contact-form]");
    if (!form) return;

    var fields = Array.prototype.slice.call(form.querySelectorAll("[data-validate]"));
    var status = document.getElementById("form-status");

    fields.forEach(function (field) {
      field.addEventListener("input", function () {
        if (field.getAttribute("aria-invalid") === "true") validateField(field);
      });
      field.addEventListener("change", function () {
        if (field.type === "checkbox") validateField(field);
      });
    });

    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var firstInvalid = null;

      fields.forEach(function (field) {
        var ok = validateField(field);
        if (!ok && !firstInvalid) firstInvalid = field;
      });

      if (firstInvalid) {
        if (status) status.hidden = true;
        firstInvalid.focus();
        announce(
          "The form has errors. Please check the highlighted fields.",
          "表格有錯誤，請檢查標示的欄位。"
        );
        return;
      }

      if (status) {
        status.hidden = false;
        status.focus();
      }
      announce(
        "Your details passed validation.",
        "你的資料已通過檢查。"
      );
    });
  }

  /* ----------------------------------------------------------------- init */

  function init() {
    var saved = readPrefs();
    var boot = window.__3rd || {};
    var systemDark =
      window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;

    state.lang = boot.lang || (saved && saved.lang) || "en";
    state.theme = boot.theme || (saved && saved.theme) || (systemDark ? "dark" : "light");
    state.size = typeof boot.size === "number" ? boot.size : (saved && saved.size) || 100;
    state.themeChosen = Boolean(saved && (saved.theme === "dark" || saved.theme === "light"));

    applyLang(state.lang, false);
    applyTheme(state.theme, false);
    applySize(state.size, false);

    document.querySelectorAll("[data-lang-set]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        applyLang(btn.getAttribute("data-lang-set"), true);
        savePrefs();
      });
    });

    document.querySelectorAll("[data-size-step]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var dir = Number(btn.getAttribute("data-size-step"));
        var index = SIZES.indexOf(state.size) + dir;
        if (index < 0) index = 0;
        if (index > SIZES.length - 1) index = SIZES.length - 1;
        applySize(SIZES[index], true);
        savePrefs();
      });
    });

    var themeBtn = document.querySelector("[data-theme-toggle]");
    if (themeBtn) {
      themeBtn.addEventListener("click", function () {
        applyTheme(state.theme === "dark" ? "light" : "dark", true);
        state.themeChosen = true;
        savePrefs();
      });
    }

    if (window.matchMedia) {
      var mq = window.matchMedia("(prefers-color-scheme: dark)");
      var onChange = function (event) {
        if (state.themeChosen) return;
        applyTheme(event.matches ? "dark" : "light", false);
      };
      if (mq.addEventListener) mq.addEventListener("change", onChange);
      else if (mq.addListener) mq.addListener(onChange);
    }

    initNav();
    initContactForm();

    var year = document.getElementById("year");
    if (year) year.textContent = String(new Date().getFullYear());
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
