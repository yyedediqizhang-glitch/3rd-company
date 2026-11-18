# -*- coding: utf-8 -*-
"""Sanity checks for the generated pages."""
import pathlib
import re
import sys
from collections import Counter

from lxml import html as LH

ROOT = pathlib.Path(__file__).resolve().parent.parent
FILES = sorted(ROOT.glob("*.html"))
problems = []

CJK = re.compile(r"[\u4e00-\u9fff]")
LATIN_WORD = re.compile(r"[A-Za-z]{3,}")

for f in FILES:
    src = f.read_text(encoding="utf-8")
    doc = LH.fromstring(src)

    # 1. basics
    if doc.find(".//main[@id='main']") is None:
        problems.append(f"{f.name}: no main#main")
    h1s = doc.xpath("//main//h1")
    if len(h1s) != 1:
        problems.append(f"{f.name}: {len(h1s)} h1 inside main")

    # 2. duplicate ids
    ids = [e.get("id") for e in doc.xpath("//*[@id]")]
    for i, n in Counter(ids).items():
        if n > 1:
            problems.append(f"{f.name}: duplicate id #{i} x{n}")

    # 3. internal links
    for a in doc.xpath("//a[@href]"):
        href = a.get("href")
        if href.startswith(("http", "mailto:", "#")):
            if href.startswith("#") and href != "#":
                if href[1:] not in ids:
                    problems.append(f"{f.name}: dangling anchor {href}")
            continue
        target = href.split("#")[0]
        if target and not (ROOT / target).exists():
            problems.append(f"{f.name}: missing link target {target}")
        elif "#" in href:
            frag = href.split("#")[1]
            if frag:
                other = LH.fromstring((ROOT / target).read_text(encoding="utf-8"))
                if not other.xpath(f"//*[@id='{frag}']"):
                    problems.append(f"{f.name}: link to missing anchor {href}")

    # 4. nav state (the accessibility page is reachable from the footer only)
    cur = doc.xpath("//nav[@id='site-nav']//a[@aria-current='page']")
    expected = 0 if f.name == "accessibility.html" else 1
    if len(cur) != expected:
        problems.append(f"{f.name}: aria-current count {len(cur)}, expected {expected}")

    # 5. describedby targets
    for el in doc.xpath("//*[@aria-describedby]"):
        for ref in el.get("aria-describedby").split():
            if not doc.xpath(f"//*[@id='{ref}']"):
                problems.append(f"{f.name}: aria-describedby -> missing #{ref}")

    # 6. Chinese leaking into .lang-en, and Latin prose leaking into .lang-zh
    for span in doc.xpath("//span[contains(@class,'lang-en')]"):
        text = " ".join(span.itertext())
        if CJK.search(text):
            problems.append(f"{f.name}: CJK inside .lang-en -> {text.strip()[:60]!r}")
    for span in doc.xpath("//span[contains(@class,'lang-zh')]"):
        text = " ".join(span.itertext())
        text = re.sub(r"[\w.+-]+@[\w-]+\.[\w.]+", " ", text)  # email addresses
        words = LATIN_WORD.findall(text)
        # a handful of proper nouns / interface keys are kept on purpose
        allowed = {
            "BBC", "STEAM", "STEM", "PET", "PP", "HDPE", "SDG", "WCAG",
            "Narrator", "NVDA", "Hong", "Kong", "Company", "GEL", "StartmeupHK",
            "EN", "Tech", "Good", "People", "First", "Tab", "Enter", "Escape",
            "Windows", "Coral", "Reef", "A", "E", "B", "H",
        }
        bad = [w for w in words if w not in allowed]
        if bad:
            problems.append(f"{f.name}: Latin inside .lang-zh -> {text.strip()[:70]!r}")

    # 7. every fieldset-ish label points at a real control
    for lab in doc.xpath("//label[@for]"):
        if not doc.xpath(f"//*[@id='{lab.get('for')}']"):
            problems.append(f"{f.name}: label for missing #{lab.get('for')}")

    # 8. html lang / data-lang defaults
    if not doc.xpath("//html[@data-lang='en']"):
        problems.append(f"{f.name}: html missing data-lang")

print(f"checked {len(FILES)} pages")
if problems:
    print(f"\n{len(problems)} problem(s):")
    for p in problems:
        print(" -", p)
    sys.exit(1)
print("all checks passed")
