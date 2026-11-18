# -*- coding: utf-8 -*-
"""
Build script for the 3RD Company site.

The pages are generated from this file so that the shared header, footer and
accessibility controls stay identical on every page. Run:

    python build.py

The output is plain, static HTML — no server, no build step needed afterwards.
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent


def L(en, zh):
    """Inline bilingual span pair (only one is visible at a time)."""
    return (
        f'<span class="lang-en">{en}</span>'
        f'<span class="lang-zh" lang="zh-Hant">{zh}</span>'
    )


NAV = [
    ("index.html", "home", "Home", "首頁"),
    ("about.html", "about", "About us", "關於我們"),
    ("programmes.html", "programmes", "Programmes", "計劃項目"),
    ("technology.html", "technology", "Technology &amp; 3R", "技術與 3R"),
    ("impact.html", "impact", "Impact", "成效與願景"),
    ("contact.html", "contact", "Contact", "聯絡我們"),
]

# --------------------------------------------------------------------- icons

ICONS = {
    "education": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M2.5 8.5 12 4l9.5 4.5L12 13z"/><path d="M6 10.6V15c0 1.6 2.7 3 6 3s6-1.4 6-3v-4.4"/><path d="M21.5 8.5V14"/></svg>',
    "community": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><circle cx="9" cy="8" r="3"/><circle cx="17.5" cy="9.5" r="2.4"/><path d="M3.5 19.5c0-3.1 2.4-5.3 5.5-5.3s5.5 2.2 5.5 5.3"/><path d="M16.2 14.6c2.4.3 4 2.1 4 4.9"/></svg>',
    "medical": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M20.3 6.2a4.6 4.6 0 0 0-6.5 0L12 8l-1.8-1.8a4.6 4.6 0 1 0-6.5 6.5L12 21l8.3-8.3a4.6 4.6 0 0 0 0-6.5Z"/><path d="M5.8 12h2.7l1.4-2.3 2 4.6 1.4-2.3h2.9"/></svg>',
    "recycle": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M20 12a8 8 0 0 1-13.4 5.8"/><path d="M4 12a8 8 0 0 1 13.4-5.8"/><path d="M17.7 2.8v3.9h-3.9"/><path d="M6.3 21.2v-3.9h3.9"/></svg>',
    "printer": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M7 9V3.5h10V9"/><rect x="3" y="9" width="18" height="8" rx="2"/><path d="M7 14.5h10v6H7z"/><path d="M17.5 12h.01"/></svg>',
    "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M12 3 5 6v6c0 4.6 3 7.6 7 9 4-1.4 7-4.4 7-9V6z"/><path d="m9 12 2 2 4-4"/></svg>',
}

# -------------------------------------------------------------------- head

HEAD = """<!DOCTYPE html>
<html lang="en" data-lang="en" data-theme="light" data-size="100"
      data-title-en="{title_en}" data-title-zh="{title_zh}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title_en}</title>
  <meta name="description" content="{desc}">
  <meta name="color-scheme" content="light dark">
  <meta name="theme-color" content="#ffffff">
  <link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
  <link rel="stylesheet" href="assets/css/styles.css">
  <script>
    /* Apply saved preferences before the first paint to avoid a flash. */
    (function () {
      var d = document.documentElement, p = {};
      try { p = JSON.parse(localStorage.getItem("3rd-prefs") || "{}") || {}; } catch (e) { p = {}; }
      var lang = p.lang === "zh" ? "zh" : "en";
      var theme = (p.theme === "dark" || p.theme === "light") ? p.theme
        : (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
      var sizes = [100, 110, 125, 140];
      var size = sizes.indexOf(p.size) !== -1 ? p.size : 100;
      d.setAttribute("data-lang", lang);
      d.setAttribute("lang", lang === "zh" ? "zh-Hant" : "en");
      d.setAttribute("data-theme", theme);
      d.setAttribute("data-size", String(size));
      d.style.fontSize = size + "%";
      d.className += " js";
      window.__3rd = { lang: lang, theme: theme, size: size };
    })();
  </script>
</head>
<body class="site">
"""

SKIP = """
  <a class="skip-link" href="#main">
    <span class="lang-en">Skip to main content</span>
    <span class="lang-zh" lang="zh-Hant">跳至主要內容</span>
  </a>
"""


def header(active):
    items = []
    for href, key, en, zh in NAV:
        current = ' aria-current="page"' if key == active else ""
        items.append(
            f'<li><a href="{href}"{current}>{L(en, zh)}</a></li>'
        )
    nav_items = "\n            ".join(items)

    return f"""
  <header class="site-header">
    <div class="container">
      <div class="header-bar">
        <a class="brand" href="index.html">
          <svg class="brand-mark" viewBox="0 0 48 48" aria-hidden="true" focusable="false">
            <rect x="1.5" y="1.5" width="45" height="45" rx="12" fill="currentColor" opacity="0.13"/>
            <path d="M24 9.5 38 17v14L24 38.5 10 31V17z" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linejoin="round"/>
            <path d="M10 17l14 7.5L38 17M24 24.5v14" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linejoin="round"/>
          </svg>
          <span>
            <span class="brand-name">3RD Company</span>
            <span class="brand-tag">{L("Tech for Good, People First", "科技向善，以人為本")}</span>
          </span>
        </a>

        <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">
          <span class="nav-toggle-bars" aria-hidden="true"></span>
          {L("Menu", "選單")}
        </button>

        <nav class="site-nav" id="site-nav" data-aria-en="Main menu" data-aria-zh="主選單" aria-label="Main menu">
          <ul>
            {nav_items}
          </ul>
        </nav>
      </div>

      <div class="toolbar">
        <div class="control-group" role="group" data-aria-en="Language" data-aria-zh="語言" aria-label="Language">
          <span class="control-label" aria-hidden="true">{L("Language", "語言")}</span>
          <button class="seg" type="button" data-lang-set="en" lang="en" aria-pressed="true">EN</button>
          <button class="seg" type="button" data-lang-set="zh" lang="zh-Hant" aria-pressed="false">中文</button>
        </div>

        <div class="control-group" role="group" data-aria-en="Text size" data-aria-zh="字級" aria-label="Text size">
          <span class="control-label" aria-hidden="true">{L("Text size", "字級")}</span>
          <button class="icon-btn" type="button" data-size-step="-1"
                  data-aria-en="Smaller text" data-aria-zh="縮小字級" aria-label="Smaller text">A−</button>
          <span class="size-value" data-size-value aria-hidden="true">100%</span>
          <button class="icon-btn" type="button" data-size-step="1"
                  data-aria-en="Larger text" data-aria-zh="放大字級" aria-label="Larger text">A+</button>
        </div>

        <div class="control-group">
          <span class="control-label" aria-hidden="true">{L("Display", "顯示")}</span>
          <button class="icon-btn" type="button" data-theme-toggle aria-label="Switch to dark theme" aria-pressed="false">
            <svg class="icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true" focusable="false">
              <circle cx="12" cy="12" r="4.2"/>
              <path d="M12 2.6v2.3M12 19.1v2.3M2.6 12h2.3M19.1 12h2.3M5.2 5.2l1.7 1.7M17.1 17.1l1.7 1.7M18.8 5.2l-1.7 1.7M6.9 17.1l-1.7 1.7"/>
            </svg>
            <svg class="icon-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" aria-hidden="true" focusable="false">
              <path d="M20.5 14.4A8.6 8.6 0 0 1 9.6 3.5a8.7 8.7 0 1 0 10.9 10.9Z"/>
            </svg>
          </button>
        </div>
      </div>
    </div>
  </header>
"""

FOOTER = f"""
  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div>
          <p class="footer-brand">3RD Company</p>
          <p class="footer-tagline">{L("Tech for Good, People First", "科技向善，以人為本")}</p>
          <p class="footer-note">{L(
              "A student project for GEL3027 — Entrepreneurship, innovation and national security education in the context of humanities.",
              "GEL3027「人文脈絡下的創業、創新與國家安全教育」學生專題習作。")}</p>
        </div>

        <nav data-aria-en="Footer" data-aria-zh="頁尾" aria-label="Footer">
          <h2>{L("Explore", "瀏覽")}</h2>
          <ul>
            <li><a href="about.html">{L("About us", "關於我們")}</a></li>
            <li><a href="programmes.html">{L("Programmes", "計劃項目")}</a></li>
            <li><a href="technology.html">{L("Technology &amp; 3R", "技術與 3R")}</a></li>
            <li><a href="impact.html">{L("Impact &amp; vision", "成效與願景")}</a></li>
            <li><a href="accessibility.html">{L("Accessibility", "無障礙")}</a></li>
          </ul>
        </nav>

        <div>
          <h2>{L("Contact", "聯絡")}</h2>
          <ul>
            <li><a href="mailto:hello@3rdcompany.hk">hello@3rdcompany.hk</a></li>
            <li>{L("Kowloon, Hong Kong", "香港九龍")}</li>
            <li>{L("Mon–Fri, 10:00–18:00 HKT", "星期一至五 10:00–18:00（香港時間）")}</li>
          </ul>
        </div>
      </div>

      <div class="footer-bottom">
        <p>© <span id="year">2026</span> 3RD Company. {L("All rights reserved.", "版權所有。")}</p>
        <p>{L(
            "Your language, theme and text-size choices are saved in this browser only.",
            "你的語言、主題與字級選擇只會儲存在這個瀏覽器。")}</p>
      </div>
    </div>
  </footer>

  <p class="sr-only" role="status" aria-live="polite" id="a11y-status"></p>
"""

TAIL = """
  <script src="assets/js/main.js"></script>
</body>
</html>
"""


def page_head(h1_en, h1_zh, lead_en, lead_zh, crumb_en, crumb_zh, eyebrow_en="", eyebrow_zh=""):
    eye = ""
    if eyebrow_en:
        eye = f'<p class="eyebrow">{L(eyebrow_en, eyebrow_zh)}</p>\n        '
    return f"""
    <section class="page-head">
      <div class="container">
        <nav class="breadcrumb" data-aria-en="Breadcrumb" data-aria-zh="導覽路徑" aria-label="Breadcrumb">
          <ol>
            <li><a href="index.html">{L("Home", "首頁")}</a></li>
            <li><span aria-current="page">{L(crumb_en, crumb_zh)}</span></li>
          </ol>
        </nav>
        {eye}<h1>{L(h1_en, h1_zh)}</h1>
        <p class="lead">{L(lead_en, lead_zh)}</p>
      </div>
    </section>
"""


def section(inner, alt=False, labelledby=None):
    cls = "section section--alt" if alt else "section"
    attr = f' aria-labelledby="{labelledby}"' if labelledby else ""
    return f"""
    <section class="{cls}"{attr}>
      <div class="container">
{inner}
      </div>
    </section>
"""


def card(icon, h_en, h_zh, p_en, p_zh, href=None, link_en=None, link_zh=None):
    link = ""
    if href:
        link = f'\n        <a class="card-link" href="{href}">{L(link_en, link_zh)} →</a>'
    return f"""
        <article class="card">
          <span class="card-icon">{ICONS[icon]}</span>
          <h3>{L(h_en, h_zh)}</h3>
          <p>{L(p_en, p_zh)}</p>{link}
        </article>"""


def card_grid(cards):
    return f'\n      <div class="card-grid">{"".join(cards)}\n      </div>'


def flow(steps):
    items = "".join(
        f"""
          <li>
            <span class="flow-num" aria-hidden="true">{i:02d}</span>
            <h3>{L(h_en, h_zh)}</h3>
            <p>{L(p_en, p_zh)}</p>
          </li>"""
        for i, (h_en, h_zh, p_en, p_zh) in enumerate(steps, start=1)
    )
    return f'\n      <ol class="flow">{items}\n      </ol>'


# =====================================================================
#  PAGES
# =====================================================================

PAGES = []


def add(filename, key, title_en, title_zh, desc, body):
    PAGES.append(
        dict(
            filename=filename,
            key=key,
            title_en=title_en,
            title_zh=title_zh,
            desc=desc,
            body=body,
        )
    )


# ------------------------------------------------------------------- index

INDEX_BODY = f"""
  <section class="hero">
    <div class="container hero-grid">
      <div>
        <p class="eyebrow">{L("Hong Kong · Social enterprise", "香港 · 社會企業")}</p>
        <h1>{L("3D printing for a more inclusive society",
                "打印一個更共融的社會")}</h1>
        <p class="lead">{L(
            "We collect the plastic Hong Kong throws away and turn it into something useful: classroom learning, neighbourhood workshops, and low-cost aids for patients and carers.",
            "我們收集香港被丟棄的塑膠，把它變成有用的東西：課堂學習、社區工作坊，以及病人與照顧者都負擔得起的輔助器具。")}</p>
        <div class="hero-actions">
          <a class="btn btn-primary" href="programmes.html">{L("Explore our programmes", "探索我們的計劃")}</a>
          <a class="btn btn-ghost" href="about.html">{L("Read our story", "了解我們的故事")}</a>
        </div>
        <div class="pill-row">
          <span class="pill">{L("3R — reduce · reuse · recycle", "3R：減用 · 重用 · 回收")}</span>
          <span class="pill">{L("3D — additive manufacturing", "3D：增材製造")}</span>
          <span class="pill">{L("Made in Hong Kong", "香港製造")}</span>
        </div>
      </div>

      <div class="hero-visual">
        <svg class="hero-svg" viewBox="0 0 460 380" aria-hidden="true" focusable="false">
          <defs>
            <linearGradient id="layerGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0" stop-color="var(--brand)" stop-opacity="0.95"/>
              <stop offset="1" stop-color="var(--brand-strong)" stop-opacity="0.8"/>
            </linearGradient>
          </defs>
          <circle cx="230" cy="190" r="152" fill="none" stroke="var(--border)" stroke-width="1.6" stroke-dasharray="7 9"/>
          <rect x="96" y="60" width="268" height="258" rx="22" fill="var(--surface-2)" stroke="var(--border)" stroke-width="1.6"/>
          <path d="M116 104v158M344 104v158" stroke="var(--brand)" stroke-width="3" stroke-linecap="round" opacity="0.22"/>
          <rect x="112" y="92" width="236" height="9" rx="4.5" fill="var(--brand)" opacity="0.7"/>
          <rect x="208" y="104" width="44" height="30" rx="7" fill="var(--brand)"/>
          <path d="M222 134h16l-4 14h-8z" fill="var(--brand-strong)"/>
          <path d="M230 152v10" stroke="var(--brand-strong)" stroke-width="2.5" stroke-dasharray="3 4" stroke-linecap="round"/>
          <circle cx="230" cy="167" r="3.4" fill="var(--accent)"/>
          <rect x="128" y="268" width="204" height="10" rx="5" fill="var(--brand)" opacity="0.45"/>
          <rect x="184" y="253" width="92" height="13" rx="3" fill="url(#layerGrad)" opacity="0.45"/>
          <rect x="190" y="238" width="80" height="13" rx="3" fill="url(#layerGrad)" opacity="0.58"/>
          <rect x="195" y="223" width="70" height="13" rx="3" fill="url(#layerGrad)" opacity="0.72"/>
          <rect x="201" y="208" width="58" height="13" rx="3" fill="url(#layerGrad)" opacity="0.85"/>
          <rect x="208" y="193" width="44" height="13" rx="3" fill="url(#layerGrad)"/>
          <rect x="216" y="178" width="28" height="13" rx="3" fill="url(#layerGrad)"/>
        </svg>
      </div>
    </div>
  </section>

{section(f'''
      <div class="section-head">
        <h2 id="pillars">{L("Three places we work", "我們工作的三個場景")}</h2>
        <p>{L(
          "The same idea runs through each programme: plastic that would be thrown away becomes something a person can use.",
          "同一個想法貫穿三個計劃：原本會被丟棄的塑膠，變成真正有人用得著的東西。")}</p>
      </div>
      {card_grid([
          card("education", "Educate", "教育",
               "Students learn by making — anatomy models printed in class, then volunteering to teach the next group how to sort plastic and run a printer.",
               "學生從動手做中學習：在課堂打印人體解剖模型，然後成為義工，教下一班同學分類塑膠和操作打印機。",
               "programmes.html#education", "Education programme", "教育計劃"),
          card("community", "Community", "社區",
               "We place collection points for clean PET, PP and HDPE bottles in housing estates, and reward residents with supermarket vouchers.",
               "我們在屋苑設置收集點，回收潔淨的 PET、PP 及 HDPE 膠樽，並以超市禮券回饋居民。",
               "programmes.html#community", "Community programme", "社區計劃"),
          card("medical", "Medical", "醫療",
               "Hospitals can turn their own clean plastic waste into customised prosthetics, dental models and surgical practice models.",
               "醫院可以把自身的潔淨塑膠廢料，製成度身訂造的義肢、牙科模型及手術練習模型。",
               "programmes.html#medical", "Medical programme", "醫療計劃"),
      ])}''', labelledby="pillars")}

{section(f'''
      <div class="section-head">
        <h2 id="how">{L("From a bottle to a helping hand", "從一個膠樽，到一雙援手")}</h2>
        <p>{L(
          "Six steps, all of them visible to the people taking part — nothing is shipped overseas to disappear.",
          "六個步驟，全部讓參與者親眼看見——沒有把廢料運到海外，眼不見為淨。")}</p>
      </div>
      {flow([
          ("Collect", "收集",
           "Clean PET, PP and HDPE bottles arrive at our community points and hospital collection bins.",
           "潔淨的 PET、PP、HDPE 膠樽送到社區收集點及醫院回收箱。"),
          ("Sort and clean", "分類清洗",
           "Volunteers check the plastic code, remove caps and labels, then wash and dry the material.",
           "義工核對塑膠編號、去除瓶蓋與標籤，再清洗及烘乾材料。"),
          ("Process", "加工",
           "The plastic is shredded and processed into filament that our printers can use.",
           "塑膠被粉碎並加工成打印機可用的線材。"),
          ("Print", "打印",
           "Workshop participants design and print something useful: a teaching model, a phone stand, a new grip for a walking stick.",
           "工作坊參加者設計並打印實用物件：教具、手機座、拐杖的新握把。"),
          ("Give back", "回饋",
           "The finished object goes to a student, a resident or a patient — and the skills stay in the community.",
           "完成品送到學生、居民或病人手上，而技術就留在社區。"),
          ("Return", "回用",
           "Failed prints and supports go back to the shredder, so the loop closes instead of ending in a bin.",
           "打印失敗的成品與支撐材料會送回粉碎步驟，讓循環閉合，而不是丟進垃圾桶。"),
      ])}''', alt=True, labelledby="how")}

  <section class="section">
    <div class="container container--narrow">
      <blockquote class="big-quote">
        <p>{L("Technology should not be a privilege for the few. It should belong to the whole society.",
              "科技不應是少數人的特權，而應屬於整個社會。")}</p>
        <cite>{L("3RD Company — our core value", "3RD 公司——我們的核心價值")}</cite>
      </blockquote>
    </div>
  </section>

  <section class="section section--alt">
    <div class="container split">
      <div>
        <h2>{L("Bring a workshop to your school, estate or hospital",
                "把工作坊帶到你的學校、屋邨或醫院")}</h2>
        <p>{L(
          "We plan every session with the host. Tell us the size of the group, the age range and the dates you have in mind, and we will propose a format.",
          "每個工作坊都與主辦單位一起規劃。告訴我們人數、年齡組別和希望舉行的日期，我們會提出合適的形式。")}</p>
      </div>
      <div>
        <p><a class="btn btn-primary" href="contact.html">{L("Start a conversation", "與我們聯絡")}</a></p>
        <p>{L("Or read how the recycling loop works on the",
              "你也可以先了解回收循環的運作：")}
          <a href="technology.html">{L("technology page", "技術頁面")}</a>.</p>
      </div>
    </div>
  </section>
"""

add(
    "index.html",
    "home",
    "3RD Company — 3D printing for a more inclusive society",
    "3RD 公司 — 打印一個更共融的社會",
    "3RD Company is a Hong Kong social enterprise that turns collected plastic waste into 3D-printed learning, community workshops and low-cost medical aids.",
    INDEX_BODY,
)

# ------------------------------------------------------------------- about

ABOUT_BODY = f"""
{page_head(
    "About 3RD Company", "關於 3RD 公司",
    "Our name carries the idea: 3R for reduce, reuse and recycle; 3D for printing. Put them together and a linear habit becomes a loop.",
    "我們的名字就是我們的想法：3R 代表減用、重用、回收；3D 代表三維打印。兩者結合，把「用完即棄」的習慣變成一個循環。",
    "About us", "關於我們",
    "Our story", "我們的故事")}

{section(f'''
      <div class="split split--wide-right">
        <div>
          <h2 id="story">{L("A technology that arrived at the right time", "一項來得正合時宜的技術")}</h2>
        </div>
        <div class="prose">
          <p>{L(
            "3D printing lays down successive layers of material under computer control to build a three-dimensional object. A designer can turn a drawing into a prototype in hours instead of weeks. It is no longer a laboratory curiosity: the BBC has reported on two brothers who used 3D printers to make free mobility aids for toddlers.",
            "三維打印是在電腦控制下，逐層鋪上材料，建構出立體物件。設計師可以在數小時內把圖紙變成原型，而不必等上數星期。它已不再是實驗室裡的稀奇玩意：BBC 曾報道一對兄弟用三維打印機，免費為幼童製作行動輔助器具。")}</p>
          <p>{L(
            "For many people the technology is still unfamiliar. For us, the attraction is specific: eco-friendly plastic materials, and a market that is still largely untapped in Hong Kong.",
            "對很多人來說，這項技術仍然陌生。對我們而言，吸引之處很具體：環保塑膠材料，以及香港仍然大致未被開發的市場。")}</p>
        </div>
      </div>''', labelledby="story")}

{section(f'''
      <div class="split split--wide-right">
        <div>
          <h2 id="problem">{L("The problem we are working on", "我們正在處理的問題")}</h2>
          <p class="pill">{L("Linear → circular", "線性 → 循環")}</p>
        </div>
        <div class="prose">
          <p>{L(
            "Since the Industrial Revolution, the linear economy — take, make, waste — has shaped how things are produced. Material is extracted, used once, and discarded. The damage to land, water and air is often irreversible.",
            "自工業革命以來，線性經濟——開採、製造、丟棄——主導了產品的生產方式。材料被開採、使用一次，然後被丟棄。對土地、水源與空氣造成的破壞，往往不可逆轉。")}</p>
          <p>{L(
            "We started 3RD Company because 3D printing suits a circular economy unusually well. It builds objects layer by layer, so it uses close to the material it needs. It can run on recycled plastic. And it works at a small scale, which means a school, an estate or a hospital can do it — not only a factory far away.",
            "我們創立 3RD 公司，是因為三維打印與循環經濟特別契合。它逐層建構物件，因此用料接近所需，浪費較少；它可以採用回收塑膠；而且它適合小規模運作，學校、屋邨或醫院都可以做，不必依賴遠方的工廠。")}</p>
        </div>
      </div>''', alt=True, labelledby="problem")}

  <section class="section">
    <div class="container container--narrow">
      <blockquote class="big-quote">
        <p>{L(
          "Our goal is to use 3D printing so that everyone can enjoy the benefits of technology at low cost — and to make that technology part of a circular economy rather than a linear one.",
          "我們的目標，是運用三維打印，讓每個人都能以低廉的成本享受科技的好處；並且讓這項技術成為循環經濟的一部分，而不是線性經濟的延伸。")}</p>
        <cite>{L("Our goal", "我們的目標")}</cite>
      </blockquote>
    </div>
  </section>

{section(f'''
      <div class="section-head">
        <h2 id="gaps">{L("Three gaps we found in Hong Kong", "我們在香港發現的三個缺口")}</h2>
        <p>{L(
          "These gaps are the reason the company exists. They are also, honestly, the hardest part of the work.",
          "這三個缺口，就是這家公司存在的原因；也是工作上最困難的部分。")}</p>
      </div>
      {card_grid([
          card("community", "Awareness", "認知",
               "3D printing is still unfamiliar to most people here. There are few local success stories to point to, and little public promotion of what the technology can do.",
               "三維打印對這裡大多數人仍然陌生。本地可供參考的成功案例不多，社會也少有推廣這項技術能做到什麼。"),
          card("recycle", "A missing platform", "缺少平台",
               "Research, material supply, social need and environmental requirements rarely meet. Hong Kong has no shared platform connecting them, so good work stays isolated.",
               "研究技術、材料供應、社會需求與環保要求，彼此很少交匯。香港沒有一個共同的平台把它們連起來，好的工作因此各自為政。"),
          card("shield", "Safety and trust", "安全與信任",
               "Medical 3D printing raises questions about regulatory oversight and material safety. Users need to know what is safe to print — and what is not.",
               "醫療三維打印涉及法規監管與材料安全問題。使用者需要知道什麼可以安全打印，什麼不可以。"),
      ])}''', labelledby="gaps")}

{section(f'''
      <div class="section-head">
        <h2 id="position">{L("Where we stand", "我們的定位")}</h2>
        <p>{L(
          "A short, honest look at what we are good at, what is in our favour, and what we still have to solve.",
          "誠實地看看我們擅長什麼、有什麼有利條件，以及還有什麼要解決。")}</p>
      </div>
      {card_grid([
          card("printer", "Our strength", "我們的優勢",
               "3D printing and the 3R principles reinforce each other: recycled plastic becomes printing material, and printing extends the life of products that would otherwise be replaced.",
               "三維打印與 3R 原則互相強化：回收塑膠成為打印材料，而打印則延長了原本要被替換的產品壽命。"),
          card("education", "Our opportunity", "我們的機遇",
               "The audience is broad — from young children to older adults — because environmental protection benefits everyone. The technology is also maturing: in 2021, 3D-printed artificial reefs were installed near Lantau Airport and shown to support marine life.",
               "受眾很廣，由幼童到長者，因為環境保護本身就對整體社會有益。技術亦日趨成熟：2021 年，東涌機場附近以三維打印製成的人工珊瑚礁，已被證實能支持海洋生態。"),
          card("shield", "Our challenge", "我們的挑戰",
               "Hong Kong lacks a cooperation and promotion platform. We are building one instead of waiting for one — connecting research, material supply, social need and environmental requirements.",
               "香港缺乏合作與推廣平台。我們選擇自己建立一個，而不是等待它出現——把研究、材料供應、社會需求與環保要求連在一起。"),
      ])}''', alt=True, labelledby="position")}

{section(f'''
      <div class="split">
        <div>
          <h2 id="serve">{L("Who we serve", "我們服務的對象")}</h2>
          <p>{L(
            "Our customers are the people who are under-served by existing technology and existing recycling schemes.",
            "我們的顧客，是現有科技與現有回收計劃都照顧不足的人。")}</p>
          <p>{L(
            "That includes students in STEAM education, residents of public housing estates, hospitals and clinics, older people and disabled people who need affordable custom aids, and the university volunteers who run our workshops.",
            "包括 STEAM 教育中的學生、公共屋邨的居民、醫院與診所，以及需要可負擔度身訂造輔助器具的長者與殘疾人士；還有負責帶領工作坊的大學義工。")}</p>
        </div>
        <div>
          <h2 id="outlook">{L("What comes next", "下一步")}</h2>
          {flow([
              ("Now — Hong Kong", "現在——香港",
               "Build a solid base in the local market: understand 3D printing, analyse demand and test the business model.",
               "在本土市場建立穩固基礎：深入了解三維打印，分析市場需求，測試商業模式。"),
              ("Next — repeatable", "下一步——可複製",
               "Turn the model into a repeatable system, then reproduce it in cities where it can work, extending our reach beyond Hong Kong.",
               "把模式變成可複製的系統，然後在合適的城市重現，把影響力延伸到香港以外。"),
              ("Later — a platform", "其後——平台",
               "Build a business ecosystem and run it as a platform, so more people can buy the things they need at lower prices.",
               "建立商業生態並以平台形式運作，讓更多人可以用更低的價錢買到他們需要的東西。"),
          ])}
        </div>
      </div>''', labelledby="serve")}
"""

add(
    "about.html",
    "about",
    "About us — 3RD Company",
    "關於我們 — 3RD 公司",
    "The story, the problem and the people behind 3RD Company: 3D printing combined with reduce, reuse and recycle in Hong Kong.",
    ABOUT_BODY,
)

# -------------------------------------------------------------- programmes

PROGRAMMES_BODY = f"""
{page_head(
    "Our programmes", "我們的計劃",
    "Three programmes, one idea: plastic that would be wasted becomes something a person can use. Each one is run with a partner who knows the people in the room.",
    "三個計劃，一個想法：原本會被浪費的塑膠，變成真正有人用得著的東西。每個計劃都與熟悉參加者的夥伴合辦。",
    "Programmes", "計劃項目",
    "What we do", "我們做什麼")}

{section(f'''
      <div class="split">
        <div>
          <p class="pill">{L("Programme 01", "計劃 01")}</p>
          <h2 id="education">{L("Education: learning by making", "教育：從動手做中學習")}</h2>
          <p class="lead">{L(
            "3D printing is an emerging educational technology. Connected to STEAM teaching, it changes the way students meet a difficult idea: they hold it.",
            "三維打印是新興的教育技術。與 STEAM 教學結合，它改變了學生面對困難概念的方式：他們可以把概念拿在手上。")}</p>
          <div class="prose">
            <h3>{L("What a school session includes", "學校工作坊內容")}</h3>
            <ul>
              <li>{L("A short introduction to additive manufacturing and the circular economy",
                    "三維打印與循環經濟簡介")}</li>
              <li>{L("Hands-on plastic sorting, and a demonstration of how filament is made",
                    "親手分類塑膠，並示範線材的製作過程")}</li>
              <li>{L("A design task the class can keep and improve", "可以帶走、繼續改良的設計任務")}</li>
              <li>{L("A printed teaching model for the school", "送給學校的打印教具")}</li>
              <li>{L("Optional: training for students who want to volunteer at later workshops",
                    "可選：培訓有意在日後工作坊擔任義工的學生")}</li>
            </ul>
          </div>
        </div>
        <div class="prose">
          <p>{L(
            "It improves the learning experience and encourages self-directed learning and innovation. Teachers use it in three ways: teaching 3D printing itself, supporting other subjects, and making learning aids. A printed organ model makes human anatomy easier to grasp than a diagram on a page.",
            "它提升學習體驗，鼓勵自主學習與創新。教師的用法有三種：直接教授三維打印、作為其他科目的支援技術，以及製作教具。一個打印出來的人體器官模型，比書頁上的圖解更容易理解。")}</p>
          <p>{L(
            "It also changes how students learn. Instead of memorising, they explore, make and test — critical making rather than rote learning. When they are ready, they step out of the textbook and volunteer at our workshops, teaching participants to operate a printer and to sort plastic properly. Students stop being only receivers of knowledge and become people who pass it on.",
            "它也改變了學生的學習方式。他們不再只是背誦，而是探索、製作與測試——是批判性的動手做，而不是死記硬背。準備好之後，他們會走出課本，在我們的工作坊擔任義工，教參加者操作打印機、正確分類塑膠。學生成為知識的傳遞者，而不只是接收者。")}</p>
        </div>
      </div>''', labelledby="education")}

{section(f'''
      <div class="split">
        <div>
          <p class="pill">{L("Programme 02", "計劃 02")}</p>
          <h2 id="community">{L("Community: recycling that pays back", "社區：回收有回報")}</h2>
          <p class="lead">{L(
            "A recycling point only works if people use it. Ours gives something back — vouchers for the plastic, and skills for the people who bring it.",
            "回收點要有人用才有意義。我們的回收點會回饋：膠樽換禮券，而帶來膠樽的人也可以學到技術。")}</p>
          <div class="notice">
            <p><strong>{L("Bring your bottles", "帶膠樽來")}</strong>
            {L("Clean, empty bottles with caps and labels removed. We accept recycling codes 1 (PET), 5 (PP) and 2 (HDPE) only.",
               "潔淨、空的膠樽，請先移除瓶蓋與標籤。我們只接受回收編號 1（PET）、5（PP）及 2（HDPE）。")}</p>
          </div>
        </div>
        <div class="prose">
          <p>{L(
            "We set up recycling stations in the community to collect clean PET, PP and HDPE plastic bottles. The plastic is then repurposed for 3D printing. To encourage residents to take part and to build a sustainable daily habit, we offer supermarket and shopping mall vouchers.",
            "我們在社區設置回收站，收集潔淨的 PET、PP 及 HDPE 膠樽，再將其改用作三維打印材料。為了鼓勵居民參與、逐步建立可持續的日常習慣，我們提供超市及商場禮券作為回饋。")}</p>
          <p>{L(
            "University student volunteers run the on-site workshops. Participants learn 3D thinking, sketching and design, then operate a printer and watch waste plastic become a new object. That is how STEM knowledge reaches a local community, and how ordinary citizens get access to an emerging technology.",
            "由大學義工主持現場工作坊。參加者學習三維思維、草圖與設計，然後親自操作打印機，看著廢塑膠變成一件新物件。STEM 知識就是這樣走進社區，一般市民就是這樣接觸到新興技術。")}</p>
          <h3>{L("Copyright, taught properly", "版權，要教得清楚")}</h3>
          <p>{L(
            "Many people have little legal awareness of what can be printed. Our workshops cover permitted use, adaptation and plagiarism, remind participants to avoid infringement, and encourage original design. The aim is a higher level of digital legal awareness — and a more cohesive community.",
            "很多人對「可以打印什麼」缺乏法律意識。工作坊會講解使用限制、改作與抄襲，提醒參加者避免侵權，同時鼓勵原創設計。目標是提升公眾的數碼法律意識，也讓社區更凝聚。")}</p>
        </div>
      </div>''', alt=True, labelledby="community")}

{section(f'''
      <div class="split">
        <div>
          <p class="pill">{L("Programme 03", "計劃 03")}</p>
          <h2 id="medical">{L("Medical: made close to the patient", "醫療：在病人身邊製造")}</h2>
          <p class="lead">{L(
            "3D printing has shown real potential in medicine. Applying circular economy principles to it can deliver environmental benefits and improve the quality of care at the same time.",
            "三維打印在醫療領域展現出實質潛力。把循環經濟原則應用其中，可以同時帶來環境效益與更好的護理質素。")}</p>
          <div class="notice notice--warn">
            <p><strong>{L("Where we stop", "我們的分界")}</strong>
            {L("We do not print anything that touches a patient’s body without the hospital’s clinical and infection-control teams. Medical work follows the partner hospital’s material, sterilisation and regulatory requirements — not our own judgement.",
               "任何會接觸病人身體的物件，都必須在醫院臨床及感染控制團隊參與下才會製作。醫療項目一律依從合作醫院的材料、消毒及法規要求，而不是我們自己的判斷。")}</p>
          </div>
        </div>
        <div class="prose">
          <h3>{L("Clinical use", "臨床應用")}</h3>
          <p>{L(
            "Personalised prosthetics and dental devices, made to a patient’s own measurements rather than adapted from a standard size.",
            "個人化的義肢與牙科裝置，按病人本身的尺寸製作，而不是把標準尺寸改裝。")}</p>
          <h3>{L("Non-clinical use", "非臨床應用")}</h3>
          <p>{L(
            "Surgical models for simulation and practice, so a team can rehearse a difficult procedure before it happens to a patient.",
            "用於模擬與練習的手術模型，讓團隊可以在真正動手術之前先演練一次。")}</p>
          <h3>{L("Recycling inside the hospital", "醫院內的循環")}</h3>
          <p>{L(
            "Hospitals can also recycle their own clean plastic waste into products through in-house printing, moving from a linear model to a sustainable circulation system. Using recycled material for assistive devices lowers the cost of medical supplies and reduces the financial burden on patients.",
            "醫院也可以把自身的潔淨塑膠廢料，透過院內打印製成產品，由線性模式走向可持續的循環系統。以回收材料製作輔助器具，可以降低醫療用品的成本，減輕病人的經濟負擔。")}</p>
        </div>
      </div>''', labelledby="medical")}

{section(f'''
      <div class="section-head">
        <h2 id="framework">{L("How we designed these programmes", "我們如何設計這些計劃")}</h2>
        <p>{L(
          "Before writing a single workshop plan, we worked through six questions. They still shape every programme we run.",
          "在寫第一份工作坊計劃之前，我們先回答了六條問題。它們至今仍然影響每一個計劃。")}</p>
      </div>
      {card_grid([
          card("education", "Interest", "興趣",
               "For many people 3D printing is a new technology. For us the attraction is specific: eco-friendly plastic materials, and a market that is still largely untapped.",
               "對很多人來說，三維打印是新技術。對我們而言，吸引之處很具體：環保塑膠材料，以及仍然大致未被開發的市場。"),
          card("shield", "Frustrations", "挫折",
               "There are few successful local precedents to learn from. Hong Kong differs from other cities in its lack of promotion and public awareness of 3D printing.",
               "本地可供參考的成功先例不多。香港與其他城市不同之處，在於對三維打印的推廣與公眾認知都不足。"),
          card("recycle", "Problems", "問題",
               "Research, material supply, social need and environmental requirements are disconnected. Medical 3D printing also faces questions of regulatory oversight and material safety.",
               "研究技術、材料供應、社會需求與環保要求彼此脫節。醫療三維打印亦面對法規監管與材料安全的問題。"),
          card("printer", "Solutions", "方案",
               "Combine 3D printing with the 3R principles: plastic collection points, community education workshops, and recycling inside hospitals to make medical assistive products.",
               "把三維打印與 3R 原則結合：設立塑膠收集點、舉辦社區教育工作坊，並在醫院內回收塑膠以製作醫療輔助產品。"),
          card("community", "Customers", "顧客",
               "People who are under-served: students in education, community residents, and hospitals, older people and disabled people who need low-cost custom aids.",
               "被忽略的一群：教育界的學生、社區居民，以及需要低成本度身訂造輔助器具的醫院、長者與殘疾人士。"),
          card("medical", "Appeal", "吸引力",
               "Lower the barriers with low-cost, eco-friendly technology, reward recycling with vouchers, and empower communities through university volunteers. Tech for Good, People First.",
               "以低成本、環保的技術降低門檻，用禮券回饋回收，並透過大學義工賦能社區。科技向善，以人為本。"),
      ])}''', alt=True, labelledby="framework")}

  <section class="section">
    <div class="container container--narrow">
      <h2>{L("Which programme fits you?", "哪個計劃適合你？")}</h2>
      <p>{L(
        "If you are a school, start with education. If you manage a housing estate or a community centre, start with a collection point. If you work in a hospital or a clinic, start with a conversation about materials and oversight.",
        "如果你是學校，可以由教育計劃開始。如果你管理屋苑或社區中心，可以由設置收集點開始。如果你在醫院或診所工作，可以先和我們談材料與監管要求。")}</p>
      <p><a class="btn btn-primary" href="contact.html">{L("Talk to us", "與我們聯絡")}</a></p>
    </div>
  </section>
"""

add(
    "programmes.html",
    "programmes",
    "Programmes — 3RD Company",
    "計劃項目 — 3RD 公司",
    "Education workshops, community recycling points and low-cost medical aids, all built on 3D printing and the 3R principles.",
    PROGRAMMES_BODY,
)

# -------------------------------------------------------------- technology

TECH_BODY = f"""
{page_head(
    "Technology and the 3R loop", "技術與 3R 循環",
    "Recycled plastic is not a lesser material. Sorted, cleaned and processed properly it prints well — and it keeps waste out of landfill.",
    "回收塑膠不是次一等的材料。只要分類、清洗、加工得宜，它一樣打印得好——同時讓廢物不必送去堆填區。",
    "Technology &amp; 3R", "技術與 3R",
    "How it works", "運作方式")}

{section(f'''
      <div class="split split--wide-right">
        <div>
          <h2 id="what">{L("What 3D printing actually is", "三維打印到底是什麼")}</h2>
          <p class="pill">{L("Additive manufacturing", "增材製造")}</p>
        </div>
        <div class="prose">
          <p>{L(
            "It is a process in which successive layers of material are laid down under computer control to make a three-dimensional object. Nothing is cut away, so there is very little offcut waste — the object is built only where it is needed.",
            "這是一個在電腦控制下，逐層鋪上材料以製成立體物件的過程。整個過程沒有切削，因此幾乎沒有邊角廢料——物件只在需要的位置生成。")}</p>
          <p>{L(
            "That makes it good for one-off parts, small batches and repairs. A grip for a walking stick, a replacement clip for a hospital trolley, a model of a heart for a biology lesson: these are cheap to print and expensive to tool up for.",
            "這使它適合單件製作、小批量生產和維修。拐杖握把、醫院手推車的替換扣件、生物課用的心臟模型——這些東西打印起來便宜，但要開模生產就很貴。")}</p>
          <p>{L(
            "There are limits, and we would rather name them. Prints are slow compared with injection moulding, the choice of materials is narrower, and the strength of a part depends on how it is oriented on the bed. We design around those limits instead of pretending they do not exist.",
            "它也有局限，我們寧願說清楚：打印速度比注塑慢，可選材料較少，而零件的強度取決於它在打印床上的放置方向。我們按這些局限來設計，而不是假裝它們不存在。")}</p>
        </div>
      </div>''', labelledby="what")}

{section(f'''
      <div class="section-head">
        <h2 id="loop">{L("The loop, step by step", "循環，一步一步")}</h2>
        <p>{L(
          "Six steps from a used bottle to a finished object. Every one of them happens in Hong Kong.",
          "由一個用過的膠樽到一件完成品，共六個步驟，全部在香港發生。")}</p>
      </div>
      {flow([
          ("Collect", "收集",
           "Community points, housing estates and hospital collection bins take in clean PET, PP and HDPE bottles.",
           "社區收集點、屋苑及醫院回收箱，接收潔淨的 PET、PP、HDPE 膠樽。"),
          ("Sort", "分類",
           "Volunteers read the recycling code and reject anything mixed, dirty or unknown. Sorting is the step that decides quality.",
           "義工查看回收編號，剔除混合、污穢或來歷不明的塑膠。分類是決定質素的關鍵一步。"),
          ("Shred", "粉碎",
           "Bottles are stripped of caps and labels, washed, dried and shredded into flakes.",
           "膠樽去除瓶蓋與標籤，清洗、烘乾，再粉碎成薄片。"),
          ("Extrude", "製線",
           "Flakes are heated and drawn into filament of a consistent diameter, then spooled for the printer.",
           "薄片經加熱拉製成直徑一致的線材，再捲上線軸供打印機使用。"),
          ("Print", "打印",
           "The printer lays the filament down layer by layer, following a design made in a workshop or a classroom.",
           "打印機依工作坊或課堂完成的設計，逐層鋪上線材。"),
          ("Return", "回用",
           "Finished objects go to a student, a resident or a patient. Failed prints and supports go back into the shredder.",
           "完成品送到學生、居民或病人手上；打印失敗的成品與支撐材料，會送回粉碎步驟。"),
      ])}''', alt=True, labelledby="loop")}

{section(f'''
      <div class="section-head">
        <h2 id="compare">{L("Linear and circular, side by side", "線性與循環，並列比較")}</h2>
      </div>
      <div class="table-wrap" role="region" data-aria-en="Comparison of linear and circular economy" data-aria-zh="線性經濟與循環經濟比較" aria-label="Comparison table" tabindex="0">
        <table>
          <caption>{L("How the two models differ in our work", "兩種模式在我們工作中的分別")}</caption>
          <thead>
            <tr>
              <th scope="col">{L("Question", "問題")}</th>
              <th scope="col">{L("Linear economy", "線性經濟")}</th>
              <th scope="col">{L("Circular economy (our model)", "循環經濟（我們的模式）")}</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <th scope="row">{L("Where material comes from", "材料從哪裡來")}</th>
              <td>{L("Newly extracted raw material", "新開採的原料")}</td>
              <td>{L("Collected plastic waste, sorted by type", "回收塑膠廢料，按種類分類")}</td>
            </tr>
            <tr>
              <th scope="row">{L("How long a product lasts", "產品用多久")}</th>
              <td>{L("Until it breaks or goes out of fashion", "直到損壞或退流行")}</td>
              <td>{L("Repaired and re-printed to extend its life", "維修與重新打印，延長使用壽命")}</td>
            </tr>
            <tr>
              <th scope="row">{L("What happens at the end", "最終如何處理")}</th>
              <td>{L("Discarded; often to landfill", "丟棄，多數送往堆填區")}</td>
              <td>{L("Returned as feedstock for the next print", "回收成為下一次打印的原料")}</td>
            </tr>
            <tr>
              <th scope="row">{L("Who can make things", "誰可以生產")}</th>
              <td>{L("Factories, at large scale", "工廠，大規模生產")}</td>
              <td>{L("Schools, communities and hospitals, at small scale", "學校、社區與醫院，小規模生產")}</td>
            </tr>
            <tr>
              <th scope="row">{L("Where the cost lands", "成本落在哪裡")}</th>
              <td>{L("On the environment, and later on the public", "落在環境，日後落在社會")}</td>
              <td>{L("On the collection and sorting system we run", "落在我們營運的收集與分類系統")}</td>
            </tr>
          </tbody>
        </table>
      </div>''', labelledby="compare")}

{section(f'''
      <div class="section-head">
        <h2 id="three-r">{L("The three Rs, in practice", "三個 R，實際怎樣做")}</h2>
        <p>{L(
          "Reduce, reuse and recycle are not slogans here. Each one describes a decision we make at a different point in a product’s life.",
          "在這裡，減用、重用、回收不是口號。每一個都代表我們在產品生命週期不同階段所作的決定。")}</p>
      </div>
      {card_grid([
          card("printer", "Reduce", "減用",
               "We reduce the consumption of natural resources from the very beginning — at the design and material-selection stage. Printing only where material is needed means less waste than cutting a part out of a block.",
               "我們從一開始就減少天然資源的消耗——在設計與選材階段。只在需要的位置打印，比從一整塊材料切削出零件浪費更少。"),
          card("recycle", "Reuse", "重用",
               "3D printing extends the life of products. A worn grip or a broken bracket can be printed again, so a device is repaired instead of being thrown away and replaced.",
               "三維打印延長產品壽命。磨損的握把或斷裂的支架可以重新打印，器具因此得以維修，而不是丟棄再買。"),
          card("shield", "Recycle", "回收",
               "Printing material can be made from waste plastic, or combined with it. Our PET, PP and HDPE collections feed directly into the filament we print with.",
               "打印材料可以由廢塑膠製成，或與廢塑膠混合。我們收集的 PET、PP、HDPE，直接成為打印線材的原料。"),
      ])}''', labelledby="three-r")}

{section(f'''
      <div class="split">
        <div>
          <h2 id="safety">{L("Safety and honest limits", "安全與誠實的局限")}</h2>
          <p>{L(
            "Recycled material is not the same as virgin material every time. We test each batch and we tell partners what they are getting.",
            "回收材料每次都不等於全新材料。我們會測試每一批材料，並如實告訴夥伴他們拿到的是什麼。")}</p>
        </div>
        <div class="prose">
          <ul>
            <li>{L("Material traceability: every spool is labelled with the plastic type, the batch and the date it was processed.",
                  "材料可追溯：每一軸線材都標明塑膠種類、批次與加工日期。")}</li>
            <li>{L("No food contact and no body contact unless the partner’s own safety process approves it.",
                  "不用於接觸食物或用於身體接觸，除非合作夥伴本身的安全程序批准。")}</li>
            <li>{L("Ventilation and filtration when printing, because heating plastic releases fumes.",
                  "打印時保持通風並使用過濾，因為加熱塑膠會釋放氣體。")}</li>
            <li>{L("Medical devices follow the hospital’s regulatory and sterilisation requirements, not our preferences.",
                  "醫療器材依從醫院的法規與消毒要求，而不是我們的偏好。")}</li>
          </ul>
        </div>
      </div>''', alt=True, labelledby="safety")}
"""

add(
    "technology.html",
    "technology",
    "Technology & 3R — 3RD Company",
    "技術與 3R — 3RD 公司",
    "How 3D printing, plastic collection and the three Rs fit together: the six-step recycling loop, linear versus circular, and the limits of the technology.",
    TECH_BODY,
)

# ------------------------------------------------------------------ impact

IMPACT_BODY = f"""
{page_head(
    "Impact and what comes next", "成效與下一步",
    "We count success in three ways: what people learn, what stays out of landfill, and what becomes cheaper and easier to get.",
    "我們用三種方式衡量成效：人們學到什麼、有多少東西不必送往堆填區，以及有什麼變得更便宜、更容易得到。",
    "Impact", "成效與願景",
    "Why it matters", "為什麼重要")}

{section(f'''
      <div class="section-head">
        <h2 id="benefit">{L("Who benefits", "誰受惠")}</h2>
        <p>{L(
          "A social enterprise has to be useful to more than one group at once. These are the five we design for.",
          "社會企業要同時對多個群體有用。以下是我們設計時考慮的五個群體。")}</p>
      </div>
      {card_grid([
          card("education", "Students", "學生",
               "A way into STEM that is hands-on and creative. Older students also gain teaching experience as volunteers, which is useful on its own terms.",
               "一條動手、有創意的 STEM 入門路徑。較年長的學生更可以在義工服務中獲得教學經驗，這本身就有價值。"),
          card("community", "Residents", "社區居民",
               "A reason to recycle — vouchers — and free workshops that give access to a technology they would otherwise only read about.",
               "一個回收的理由——禮券——以及免費工作坊，讓他們接觸到本來只會在報道中看見的技術。"),
          card("medical", "Hospitals and patients", "醫院與病人",
               "Customised aids and models at lower cost, and a route for the hospital’s own clean plastic waste to become something useful.",
               "更低成本的度身訂造輔助器具與模型，也為醫院自身的潔淨塑膠廢料找到有用出路。"),
          card("shield", "Older people and disabled people", "長者與殘疾人士",
               "Affordable, repairable aids. When a part wears out, a replacement can be printed instead of a whole new device being bought.",
               "負擔得起、可以維修的輔助器具。零件磨損時，可以打印替換件，而不必整件重新購買。"),
          card("recycle", "University volunteers", "大學義工",
               "Real practice in teaching, facilitation and design — and a reason to understand the material cycle rather than just the printer.",
               "在教學、帶領活動與設計上的實際鍛鍊，也讓他們理解整個材料循環，而不只是操作打印機。"),
      ])}''', labelledby="benefit")}

{section(f'''
      <div class="split">
        <div>
          <h2 id="case">{L("What 3D printing can already do", "三維打印已經做到的事")}</h2>
          <p>{L(
            "The technology is not a promise about the future. It is already being used at a scale that matters.",
            "這項技術不是對未來的許諾，它已經在實際規模上被使用。")}</p>
        </div>
        <div>
          <blockquote class="big-quote">
            <p>{L(
              "In 2021, artificial coral reefs near Lantau Airport were created using 3D printing technology, and have been shown to protect the marine ecosystem.",
              "2021 年，機場附近水域以三維打印技術製成人工珊瑚礁，並已證實有助保護海洋生態。")}</p>
            <cite>{L("StartmeupHK, 2023 — “3D-printed coral reefs: reviving marine ecosystems”", "StartmeupHK，2023——《3D打印環保珊瑚礁 以創科活化海洋生態圈》")}</cite>
          </blockquote>
          <p>{L(
            "It is a useful reminder that the same layer-by-layer method can rebuild a habitat as easily as it can make a part. After several years of development the technology has matured, which is why we think now is the right time to link 3D printing with environmental conservation.",
            "這提醒我們：同一種逐層建構的方法，可以用來重建一個棲息地，也可以只用來做一個零件。經過多年發展，技術已經成熟，所以我們認為現在正是把三維打印與環境保育連起來的時候。")}</p>
        </div>
      </div>''', alt=True, labelledby="case")}

{section(f'''
      <div class="split">
        <div>
          <h2 id="trade">{L("Trade shows and partnerships", "展覽與合作")}</h2>
          <p>{L(
            "We are a small organisation, so being visible in the right room matters more than advertising.",
            "我們規模小，所以在對的場合露面，比賣廣告更重要。")}</p>
        </div>
        <div class="prose">
          <p>{L(
            "Exhibiting at a trade show builds trust and a professional image: samples and certifications can be shown, and clients can meet the team face to face. It is also where partnerships begin — with local distributors, or with university research teams.",
            "參展可以建立信任與專業形象：展示樣本與認證，讓客戶親身認識團隊。合作也往往由這裡開始——與本地分銷商，或與大學研究團隊。")}</p>
          <ul>
            <li>{L("Samples, certifications and printed parts that people can hold", "可以親手拿起的樣本、認證與打印成品")}</li>
            <li>{L("Partnerships with distributors and university research teams", "與分銷商及大學研究團隊建立合作")}</li>
            <li>{L("Media coverage, especially for environmental and healthcare topics", "媒體報道，尤其是環保與醫療相關題材")}</li>
            <li>{L("Access to corporate marketing funds, which support the next programme", "申請企業市場推廣基金，支持下一個計劃")}</li>
          </ul>
        </div>
      </div>''', labelledby="trade")}

{section(f'''
      <div class="section-head">
        <h2 id="roadmap">{L("The road ahead", "前路")}</h2>
        <p>{L(
          "Three steps, in order. We do not skip the first one.",
          "三步，依次而行。我們不會跳過第一步。")}</p>
      </div>
      {flow([
          ("Establish in Hong Kong", "立足香港",
           "Build a solid base in the local market: understand 3D printing deeply, analyse market demand and test business models.",
           "在本土市場建立穩固基礎：深入理解三維打印，分析市場需求，測試商業模式。"),
          ("Make it repeatable", "變成可複製",
           "Turn the model into a repeatable system, then reproduce it in cities where the conditions allow, extending our influence beyond Hong Kong.",
           "把模式變成可複製的系統，然後在條件合適的城市重現，把影響力延伸到香港以外。"),
          ("Become a platform", "成為平台",
           "Build a business ecosystem and run it as a platform, so more people who need 3D printing can buy what they need at lower prices.",
           "建立商業生態並以平台形式運作，讓更多需要三維打印的人可以用更低價錢買到所需。"),
      ])}''', alt=True, labelledby="roadmap")}

  <section class="section">
    <div class="container container--narrow">
      <h2>{L("Where this fits the Sustainable Development Goals", "與可持續發展目標的呼應")}</h2>
      <p>{L(
        "Our work touches several of the UN Sustainable Development Goals. We describe this as alignment, not certification — we are a student project, not an accredited programme.",
        "我們的工作與聯合國多項可持續發展目標相關。我們稱之為「呼應」，而不是「認證」——我們是學生專案，不是受認可的計劃。")}</p>
      <div class="pill-row">
        <span class="pill">{L("SDG 4 — Quality education", "SDG 4——優質教育")}</span>
        <span class="pill">{L("SDG 3 — Good health", "SDG 3——良好健康與福祉")}</span>
        <span class="pill">{L("SDG 11 — Sustainable cities", "SDG 11——可持續城市")}</span>
        <span class="pill">{L("SDG 12 — Responsible consumption and production", "SDG 12——負責任消費與生產")}</span>
      </div>
    </div>
  </section>

  <section class="section section--alt">
    <div class="container container--narrow">
      <blockquote class="big-quote">
        <p>{L(
          "3D printing can print more than an object. It can print a more inclusive and compassionate society.",
          "三維打印打印的不只是一件物件，更是一個更共融、更有人情味的社會。")}</p>
        <cite>{L("3RD Company — conclusion", "3RD 公司——結語")}</cite>
      </blockquote>
    </div>
  </section>
"""

add(
    "impact.html",
    "impact",
    "Impact and vision — 3RD Company",
    "成效與願景 — 3RD 公司",
    "Who benefits from 3RD Company, the 3D-printed coral reef case, trade-show partnerships and the three-step plan beyond Hong Kong.",
    IMPACT_BODY,
)

# ----------------------------------------------------------------- contact

CONTACT_BODY = f"""
{page_head(
    "Talk to us", "與我們聯絡",
    "Schools, housing estates, hospitals, universities and companies each work with us in a different way. Tell us what you have in mind.",
    "學校、屋苑、醫院、大學與企業，各自以不同方式與我們合作。告訴我們你在想什麼。",
    "Contact", "聯絡我們",
    "Get in touch", "聯絡我們")}

{section(f'''
      <div class="split split--wide-right">
        <div>
          <h2 id="form-heading">{L("Send an enquiry", "送出查詢")}</h2>
          <p>{L(
            "Fields marked with an asterisk are required. This is a prototype: the form checks your input in the browser but does not send anything.",
            "有星號的欄位為必填。這是原型版本：表格只在瀏覽器內檢查你的輸入，不會送出任何資料。")}</p>

          <div class="notice">
            <p><strong>{L("Prototype notice", "原型版本說明")}</strong>
            {L("Nothing you type here leaves your computer and nothing is stored. To reach the team for real, write to hello@3rdcompany.hk.",
               "你在這裡輸入的內容不會離開你的電腦，也不會被儲存。如要真正聯絡團隊，請電郵 hello@3rdcompany.hk。")}</p>
          </div>

          <ul class="prose" style="padding-left:1.2rem">
            <li>{L("Workshops for schools and community centres", "學校及社區中心工作坊")}</li>
            <li>{L("Setting up a plastic collection point", "設置塑膠收集點")}</li>
            <li>{L("Hospital and clinic projects", "醫院及診所項目")}</li>
            <li>{L("Volunteering, partnerships and media", "義工、合作與媒體")}</li>
          </ul>
        </div>

        <form class="form" data-contact-form novalidate>
          <div class="field">
            <label for="name">{L('Your name <span class="req" aria-hidden="true">*</span>', '你的姓名 <span class="req" aria-hidden="true">*</span>')}</label>
            <input id="name" name="name" type="text" autocomplete="name" required data-validate
                   aria-describedby="name-error">
            <p class="error" id="name-error" hidden>
              <span class="lang-en error-required">Please enter your name.</span>
              <span class="lang-zh error-required" lang="zh-Hant">請輸入你的姓名。</span>
            </p>
          </div>

          <div class="field">
            <label for="email">{L('Email address <span class="req" aria-hidden="true">*</span>', '電郵地址 <span class="req" aria-hidden="true">*</span>')}</label>
            <input id="email" name="email" type="email" autocomplete="email" required data-validate
                   aria-describedby="email-hint email-error">
            <p class="field-hint" id="email-hint">{L("We only use this to reply to you.", "我們只會用來回覆你。")}</p>
            <p class="error" id="email-error" hidden>
              <span class="lang-en error-required">Please enter your email address.</span>
              <span class="lang-zh error-required" lang="zh-Hant">請輸入你的電郵地址。</span>
              <span class="lang-en error-email" hidden>That does not look like a complete email address.</span>
              <span class="lang-zh error-email" lang="zh-Hant" hidden>這個電郵地址似乎並不完整。</span>
            </p>
          </div>

          <div class="field">
            <label for="org">{L("Organisation", "機構")}</label>
            <input id="org" name="org" type="text" autocomplete="organization"
                   aria-describedby="org-hint">
            <p class="field-hint" id="org-hint">{L("School, estate, hospital, university or company — optional.",
                                                   "學校、屋苑、醫院、大學或企業——可選填。")}</p>
          </div>

          <div class="field">
            <label for="interest">{L("I am interested in", "我有興趣的是")}</label>
            <select id="interest" name="interest" data-opt-lang>
              <option value="" data-opt-en="Please choose" data-opt-zh="請選擇">Please choose</option>
              <option value="school" data-opt-en="A workshop for a school" data-opt-zh="學校工作坊">A workshop for a school</option>
              <option value="community" data-opt-en="A recycling point in my community" data-opt-zh="在社區設置收集點">A recycling point in my community</option>
              <option value="medical" data-opt-en="A hospital or clinic project" data-opt-zh="醫院或診所項目">A hospital or clinic project</option>
              <option value="volunteer" data-opt-en="Volunteering" data-opt-zh="成為義工">Volunteering</option>
              <option value="partner" data-opt-en="Partnership or media enquiry" data-opt-zh="合作或媒體查詢">Partnership or media enquiry</option>
              <option value="other" data-opt-en="Something else" data-opt-zh="其他">Something else</option>
            </select>
          </div>

          <div class="field">
            <label for="message">{L('Your message <span class="req" aria-hidden="true">*</span>', '你的訊息 <span class="req" aria-hidden="true">*</span>')}</label>
            <textarea id="message" name="message" required data-validate
                      aria-describedby="message-hint message-error"></textarea>
            <p class="field-hint" id="message-hint">{L(
              "Helpful details: the size of the group, the age range, and any dates you have in mind.",
              "有助我們回覆的資料：人數、年齡組別，以及你希望舉行的日期。")}</p>
            <p class="error" id="message-error" hidden>
              <span class="lang-en error-required">Please write a short message.</span>
              <span class="lang-zh error-required" lang="zh-Hant">請寫下一段簡短訊息。</span>
            </p>
          </div>

          <div class="field">
            <div class="checkbox-row">
              <input id="consent" name="consent" type="checkbox" required data-validate
                     aria-describedby="consent-error">
              <label for="consent">{L(
                "I agree that 3RD Company may contact me about this enquiry.",
                "我同意 3RD 公司就此查詢與我聯絡。")}</label>
            </div>
            <p class="error" id="consent-error" hidden>
              <span class="lang-en error-required">Please tick this box so we can reply.</span>
              <span class="lang-zh error-required" lang="zh-Hant">請勾選此欄，我們才能回覆你。</span>
            </p>
          </div>

          <div>
            <button class="btn btn-primary" type="submit">{L("Check and send", "檢查並送出")}</button>
          </div>

          <div class="form-status" id="form-status" role="status" tabindex="-1" hidden>
            <p><strong>{L("Your message passed validation.", "你的訊息已通過檢查。")}</strong></p>
            <p>{L(
              "This prototype does not send email or store anything. To reach the team, please write to hello@3rdcompany.hk.",
              "這個原型版本不會寄出電郵，也不會儲存任何資料。如要聯絡團隊，請電郵 hello@3rdcompany.hk。")}</p>
          </div>
        </form>
      </div>''', labelledby="form-heading")}

{section(f'''
      <div class="split">
        <div>
          <h2 id="details">{L("Where to find us", "在哪裡找到我們")}</h2>
          <p>{L(
            "We are a student team at a Hong Kong university. Replies may take a few days during term time.",
            "我們是香港一所大學的學生團隊。學期期間，回覆可能需要數天。")}</p>
        </div>
        <div class="prose">
          <ul>
            <li><strong>{L("Email", "電郵")}:</strong> <a href="mailto:hello@3rdcompany.hk">hello@3rdcompany.hk</a></li>
            <li><strong>{L("Workshops", "工作坊")}:</strong> <a href="mailto:workshops@3rdcompany.hk">workshops@3rdcompany.hk</a></li>
            <li><strong>{L("Accessibility", "無障礙")}:</strong> <a href="mailto:accessibility@3rdcompany.hk">accessibility@3rdcompany.hk</a></li>
            <li><strong>{L("Hours", "辦公時間")}:</strong> {L("Monday to Friday, 10:00–18:00 HKT", "星期一至五，10:00–18:00（香港時間）")}</li>
            <li><strong>{L("Address", "地址")}:</strong> {L("Kowloon, Hong Kong (venue confirmed per workshop)", "香港九龍（工作坊地點另行確認）")}</li>
          </ul>
        </div>
      </div>''', alt=True, labelledby="details")}

{section(f'''
      <div class="section-head">
        <h2 id="faq">{L("Frequently asked questions", "常見問題")}</h2>
      </div>
      <div class="accordion">
        <details>
          <summary>{L("Is the recycled plastic safe to print?", "回收塑膠可以安全打印嗎？")}</summary>
          <div class="details-body">
            <p>{L(
              "We accept only clean PET, PP and HDPE (recycling codes 1, 5 and 2). Mixed, dirty or unidentified plastic is rejected at sorting. Prints are not used for food contact, and anything used in a clinical setting is approved by the partner hospital’s own safety process.",
              "我們只接受潔淨的 PET、PP 及 HDPE（回收編號 1、5、2）。混合、污穢或無法辨識的塑膠會在分類階段被剔除。打印成品不會用於接觸食物；任何臨床用途的物件，都須經合作醫院本身的安全程序批准。")}</p>
          </div>
        </details>
        <details>
          <summary>{L("Do participants need any experience?", "參加者需要有經驗嗎？")}</summary>
          <div class="details-body">
            <p>{L(
              "No. Workshops start with sketching on paper and a short explanation of how a printer works. Most participants print their first object within the session.",
              "不需要。工作坊由紙上草圖開始，並簡單講解打印機的運作。大部分參加者都能在同一節工作坊內打印出自己的第一件作品。")}</p>
          </div>
        </details>
        <details>
          <summary>{L("What does a workshop cost?", "工作坊收費如何？")}</summary>
          <div class="details-body">
            <p>{L(
              "Community and school workshops are free or charged at cost, because the material comes from plastic we have collected. A custom programme with a venue, materials and staff time is quoted individually.",
              "社區及學校工作坊免費或只收回成本，因為材料來自我們收集的塑膠。如屬度身訂造的計劃，涉及場地、材料與人手，則會另行報價。")}</p>
          </div>
        </details>
        <details>
          <summary>{L("Can we donate plastic?", "可以捐贈塑膠嗎？")}</summary>
          <div class="details-body">
            <p>{L(
              "Yes, if it is clean and sorted: empty bottles with caps and labels removed, codes 1, 5 and 2 only. Businesses with larger volumes should email us first so we can arrange collection.",
              "可以，只要是潔淨並已分類：空的膠樽，已移除瓶蓋與標籤，只限編號 1、5、2。如屬較大量的商業捐贈，請先電郵聯絡，以便安排收集。")}</p>
          </div>
        </details>
        <details>
          <summary>{L("Do you make medical devices?", "你們會製作醫療器材嗎？")}</summary>
          <div class="details-body">
            <p>{L(
              "Not on our own. Medical work is done with the partner hospital’s clinical team, in line with its regulatory, material and sterilisation requirements. Student prototypes are never used in patient care.",
              "我們不會自行製作。醫療項目由合作醫院的臨床團隊參與，並依從其法規、材料及消毒要求。學生原型不會用於病人護理。")}</p>
          </div>
        </details>
      </div>''', labelledby="faq")}
"""

add(
    "contact.html",
    "contact",
    "Contact — 3RD Company",
    "聯絡我們 — 3RD 公司",
    "Contact 3RD Company about a school workshop, a community recycling point, a hospital project, volunteering or a partnership.",
    CONTACT_BODY,
)

# ------------------------------------------------------------ accessibility

ACCESS_BODY = f"""
{page_head(
    "Accessibility", "無障礙",
    "This site is built so that people using screen readers, keyboard navigation or magnification can use it — not as an afterthought, but as part of the design.",
    "這個網站是為了讓使用螢幕閱讀器、鍵盤操作或放大工具的人也能使用而建——不是事後補救，而是設計的一部分。",
    "Accessibility", "無障礙",
    "Everyone should be able to read this", "每個人都應該讀得到")}

{section(f'''
      <div class="split split--wide-right">
        <div>
          <h2 id="statement">{L("Our commitment", "我們的承諾")}</h2>
        </div>
        <div class="prose">
          <p>{L(
            "We aim to meet the Web Content Accessibility Guidelines (WCAG) 2.1 at level AA. This site is a student prototype for a university course, so it has not been independently audited — where we know of a limitation, it is listed below rather than hidden.",
            "我們以《無障礙網頁內容指引》（WCAG）2.1 AA 級為目標。這個網站是大學課程的學生原型，因此未經獨立審核——我們已知的限制會列在下方，而不是隱藏起來。")}</p>
          <p>{L(
            "Accessibility matters to this project for a practical reason. If our aim is to make technology available to people who are usually left out, the way we present our own work should not exclude anyone either.",
            "無障礙對這個專案有實際的理由。如果我們的目標是讓平常被忽略的人也能使用科技，那麼我們呈現自己工作的方式，也不應該排擠任何人。")}</p>
        </div>
      </div>''', labelledby="statement")}

{section(f'''
      <div class="section-head">
        <h2 id="features">{L("What is built in", "已加入的功能")}</h2>
      </div>
      <div class="card-grid">
        <article class="card">
          <h3>{L("Text size", "字級調整")}</h3>
          <p>{L(
            "The A− and A+ buttons in the header change the whole page between 100% and 140%. The layout is built in relative units, so it reflows instead of clipping. Your choice is remembered on this device.",
            "標題列的 A− 與 A+ 按鈕，可以把整個頁面在 100% 至 140% 之間調整。版面以相對單位建立，因此會重新排版，而不是被裁切。你的選擇會在此裝置上保留。")}</p>
        </article>
        <article class="card">
          <h3>{L("Light and dark themes", "深色與淺色主題")}</h3>
          <p>{L(
            "The sun and moon button switches theme, and the page follows your operating system setting until you choose. Both themes keep text contrast at 4.5:1 or better.",
            "太陽與月亮按鈕可切換主題；在你自行選擇之前，頁面會跟隨作業系統設定。兩個主題的文字對比度都維持在 4.5:1 或以上。")}</p>
        </article>
        <article class="card">
          <h3>{L("Two languages", "雙語")}</h3>
          <p>{L(
            "Every page is available in English and Traditional Chinese. The page language attribute changes with the content, so a screen reader uses the right pronunciation rules.",
            "每一頁都提供英文及繁體中文版本。頁面的語言標記會隨內容改變，螢幕閱讀器因此會使用正確的發音規則。")}</p>
        </article>
        <article class="card">
          <h3>{L("Screen readers", "螢幕閱讀器")}</h3>
          <p>{L(
            "Pages use landmarks, one main heading, a logical heading order, and a skip link as the first focusable item. Decorative graphics are hidden from assistive technology; nothing important is described only by an image.",
            "頁面使用地標區域、單一主標題、合乎層級的標題順序，並以「跳至主要內容」作為第一個可聚焦項目。裝飾性圖形不會被輔助技術讀出；重要資訊不會只以圖像表達。")}</p>
        </article>
        <article class="card">
          <h3>{L("Keyboard only", "純鍵盤操作")}</h3>
          <p>{L(
            "Every control works with Tab, Enter and Space, focus is always visible, and the mobile menu closes with Escape. There are no keyboard traps and nothing is triggered automatically by hovering.",
            "所有控制項都可以用 Tab、Enter 及空格鍵操作，焦點永遠可見，手機版選單可按 Escape 關閉。沒有鍵盤陷阱，也沒有隻靠滑鼠停留才觸發的內容。")}</p>
        </article>
        <article class="card">
          <h3>{L("Motion and forms", "動態效果與表格")}</h3>
          <p>{L(
            "Animation is minimal and respects the reduced-motion setting. Form fields have visible labels, hints, and error messages tied to the field, and errors are announced and focused.",
            "動態效果極少，並尊重系統的「減少動態」設定。表格欄位有可見標籤、提示，以及與欄位連結的錯誤訊息；錯誤會被讀出並把焦點移到出錯的欄位。")}</p>
        </article>
      </div>''', alt=True, labelledby="features")}

{section(f'''
      <div class="split">
        <div>
          <h2 id="how-to">{L("Using the controls", "如何使用這些控制")}</h2>
          <p>{L(
            "The three controls sit under the main menu on every page.",
            "三個控制項位於每一頁的主選單下方。")}</p>
        </div>
        <div class="prose">
          <ul>
            <li>{L("Language — the EN and Chinese buttons. The current language is marked as pressed.",
                  "語言——EN 與「中文」按鈕。目前語言會標示為已按下。")}</li>
            <li>{L("Text size — A− makes text smaller, A+ makes it larger. The current percentage is shown between them.",
                  "字級——A− 縮小文字，A+ 放大文字，中間會顯示目前的百分比。")}</li>
            <li>{L("Theme — the sun or moon button switches between light and dark.",
                  "主題——太陽或月亮按鈕，在淺色與深色之間切換。")}</li>
            <li>{L("All three choices are saved in this browser only. Clearing site data resets them.",
                  "三個選擇只會儲存在這個瀏覽器。清除網站資料即會重設。")}</li>
          </ul>
        </div>
      </div>''', labelledby="how-to")}

{section(f'''
      <div class="split">
        <div>
          <h2 id="limits">{L("Known limitations", "已知限制")}</h2>
        </div>
        <div class="prose">
          <ul>
            <li>{L("The site has not been tested with every screen reader and browser combination. We have tested with Windows Narrator, NVDA and keyboard-only navigation.",
                  "網站未經所有螢幕閱讀器與瀏覽器組合測試。我們以 Windows 朗讀程式、NVDA 及純鍵盤操作測試過。")}</li>
            <li>{L("The contact form is a prototype: it validates input but does not send or store it.",
                  "聯絡表格是原型：會檢查輸入，但不會送出或儲存。")}</li>
            <li>{L("There is no audio or video content, so no captions are needed yet.",
                  "目前沒有音訊或影片內容，因此暫無字幕需要。")}</li>
            <li>{L("A few technical terms (filament, additive manufacturing) appear in English inside the Chinese text, because there is no settled Hong Kong translation.",
                  "少數技術詞彙（線材、增材製造）在中文版中會保留英文，因為香港尚未有統一譯法。")}</li>
          </ul>
        </div>
      </div>''', alt=True, labelledby="limits")}

  <section class="section">
    <div class="container container--narrow">
      <h2>{L("Tell us what does not work", "告訴我們哪裡不能用")}</h2>
      <p>{L(
        "If something on this site blocks you — a control you cannot reach, text you cannot read, a page that does not make sense with a screen reader — please write to",
        "如果這個網站有任何地方阻礙你——無法到達的控制項、讀不到的文字、用螢幕閱讀器讀起來不合理的頁面——請電郵")}
        <a href="mailto:accessibility@3rdcompany.hk">accessibility@3rdcompany.hk</a>.
        {L("We will fix it and say what we changed.", "我們會修正，並說明改了什麼。")}</p>
      <p><a class="btn btn-ghost" href="contact.html">{L("Other ways to contact us", "其他聯絡方式")}</a></p>
    </div>
  </section>
"""

add(
    "accessibility.html",
    "accessibility",
    "Accessibility — 3RD Company",
    "無障礙 — 3RD 公司",
    "How this site supports screen readers, keyboard navigation, larger text, dark mode and bilingual reading.",
    ACCESS_BODY,
)

# __MORE_CONTENT__

# =====================================================================
#  WRITE
# =====================================================================

def render(p):
    head = (
        HEAD.replace("{title_en}", p["title_en"])
        .replace("{title_zh}", p["title_zh"])
        .replace("{desc}", p["desc"])
    )
    return (
        head
        + SKIP
        + header(p["key"])
        + '\n  <main id="main">'
        + p["body"]
        + "\n  </main>\n"
        + FOOTER
        + TAIL
    )


if __name__ == "__main__":
    for p in PAGES:
        out = ROOT / p["filename"]
        out.write_text(render(p), encoding="utf-8")
        print("wrote", out.name)



