# 3RD Company — website

A seven-page, bilingual (English / 繁體中文) website for **3RD Company**, the social enterprise
designed in the GEL3027 group report: 3D printing combined with reduce, reuse and recycle.

## Live site

**https://yyedediqizhang-glitch.github.io/3rd-company/**

Public, free and permanent. Hosted on GitHub Pages from the repository
[`yyedediqizhang-glitch/3rd-company`](https://github.com/yyedediqizhang-glitch/3rd-company).
Anyone with the link can open it on a phone or a laptop — no account, no app.

To update the live site after editing, double-click **`publish.cmd`** (it commits and pushes; the
site refreshes in about a minute).

No server, no framework, no internet connection needed to preview it locally.
Open `index.html` in any modern browser.

---

## How to open it

1. Open the folder `3RD-Website`.
2. Double-click **`index.html`**.

Everything else (CSS, JavaScript, icon) is loaded from the `assets` folder, so keep the folder
structure intact if you copy the site to a USB stick or upload it.

---

## Pages

| File | English | 中文 |
| --- | --- | --- |
| `index.html` | Home | 首頁 |
| `about.html` | About us — story, problem, goal, gaps, roadmap | 關於我們 |
| `programmes.html` | Education, community and medical programmes + the six-question framework | 計劃項目 |
| `technology.html` | What 3D printing is, the six-step loop, linear vs circular table, the three Rs | 技術與 3R |
| `impact.html` | Who benefits, coral-reef case, trade shows, roadmap, SDGs | 成效與願景 |
| `contact.html` | Enquiry form, contact details, FAQ | 聯絡我們 |
| `accessibility.html` | Accessibility statement, features, known limitations | 無障礙 |

The top menu appears on every page and marks the current page for screen readers
(`aria-current="page"`).

---

## What it does

**Bilingual.** The EN / 中文 buttons switch every page instantly. Both languages are stored in the
HTML itself (not loaded afterwards), so the text is there even with JavaScript turned off. The
`<html lang>` attribute changes to `zh-Hant`, which tells a screen reader to switch pronunciation.
The choice is remembered on the next page and on the next visit.

**Text size.** A− / A+ scale the whole page between **100% and 140%**. Everything is sized in `rem`,
so headings, cards and buttons grow together and the layout reflows instead of overlapping.

**Light and dark themes.** The sun / moon button switches theme. On a first visit the page follows
the operating system setting. Both themes keep body text at a contrast ratio of at least 4.5:1.

**Accessibility.** Built for screen-reader and keyboard users:

- skip link as the first focusable item;
- landmarks (`header`, `nav`, `main`, `footer`) and one `h1` per page;
- visible 3px focus outline on every control, 44px+ touch targets;
- decorative SVG hidden from assistive technology, icons paired with text;
- form fields with real `<label>`, hints and error messages linked by `aria-describedby`,
  `aria-invalid` on error, focus moved to the first invalid field;
- status announcements through an `aria-live` region when language, text size or theme changes;
- `prefers-reduced-motion` respected; no autoplay, no keyboard traps, no hover-only content.

**Responsive.** One column on phones, two on tablets, full editorial layout on desktop. The menu
collapses to a Menu button that closes with `Escape`.

---

## Editing the content

Two options.

**A. Edit the HTML directly.** Every page is plain, well-commented HTML. Search for the English text
you want to change; the Chinese translation sits in the `<span class="lang-zh">` right next to it.

**B. Edit the generator (recommended for big changes).** All pages are produced from
`_build/build.py`, which holds the shared header, footer and accessibility controls in one place,
so a change there reaches all seven pages.

```powershell
# from the 3RD-Website folder
python _build\build.py     # rebuild all pages
python _build\check.py     # link / id / language sanity checks
```

The pages are generated files — if you edit them by hand and then run `build.py`, the hand edits are
overwritten.

---

## Notes and honest limitations

- **The contact form is a prototype.** It validates input in the browser and then shows a message;
  it does not send or store anything. There is no back end. The email addresses
  (`hello@3rdcompany.hk` etc.) are placeholders.
- **No real photographs.** The illustrations are inline SVG, so the site works offline and every
  graphic is either decorative (`aria-hidden`) or backed by real text.
- **Figures are qualitative.** The report did not include measured impact numbers, so the site talks
  about what each programme does rather than inventing statistics.
- **Not independently audited.** The accessibility page says so, and lists what has and has not been
  tested.
- `_build/` is development-only. You can delete it and the site still works.

## Sources used for the copy

The content is taken from the group outline, including:

- Elena Novak (2022), *3D Printing in Education* — STEAM, critical making.
- BBC News — brothers making free mobility aids with 3D printers.
- Ellen Macarthur Foundation — the linear economy.
- Mansour, N. K. (2025) — circular economy and 3D printing in healthcare.
- StartmeupHK (2023) — 3D-printed artificial coral reefs near Lantau Airport.
- CUHK Information Services Office — printing in green and 3D.
