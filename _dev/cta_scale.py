#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bring the big page-foot CTAs back to a button's proportions.

`_dev/audit.mjs` reported these at 38px of Fraunces, 167px tall and 69% of the
viewport wide, on four pages. They read as a second hero rather than as a
control: a full-width gold slab with a headline inside it.

The shape they inherited is `display:flex; flex-direction:column;
align-items:center; width:100%` with `strong` at `clamp(22px,3vw,38px)`. That is
hero typography on a button.

What changes: the fill stops being full-bleed, the type comes down to a scale a
button can carry, and the block left-aligns so it reads as an action rather than
as a banner. The colour, the shadow and the press animation are untouched -
those are the parts that make it feel like a control, and they were never the
problem.

Selectors are discovered per page (`.gcta`, `.tcta`, `.acta`, …) rather than
typed, so a page that names its CTA something else is still caught.
"""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
MARK = "/* _dev/cta_scale.py */"

PAGES = [f for f in sorted(os.listdir(SITE))
         if f.endswith(".html") and f not in ("tycoon.html", "local.html", "concepts.html")]

# a slab CTA: a class whose rule is a full-width column flex with a big padding
SLAB = re.compile(r"\.([a-z][\w-]*)\{([^}]*)\}")


def slab_ctas(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    out = set()
    for name, body in SLAB.findall(css):
        if "width:100%" not in body.replace(" ", ""):
            continue
        if "flex-direction:column" not in body.replace(" ", ""):
            continue
        if "display:flex" not in body.replace(" ", ""):
            continue
        # and it must carry a headline-scale <strong> somewhere in this sheet
        if re.search(r"\." + re.escape(name) + r"\s+strong\{[^}]*font-size:clamp\(\s*\d\d", css):
            out.add(name)
    return out


def block(names):
    sels = ",".join("." + n for n in sorted(names))
    strongs = ",".join(".%s strong" % n for n in sorted(names))
    spans = ",".join(".%s span" % n for n in sorted(names))
    return ("\n<style>" + MARK + "\n"
            # not full-bleed, and left-aligned: an action, not a banner
            + sels + "{width:auto;max-width:min(100%,640px);align-items:flex-start;"
                     "text-align:left;gap:4px;padding:15px 26px;min-height:64px}\n"
            # a button's type scale, not a hero's
            + strongs + "{font-size:clamp(17px,1.5vw,21px);max-width:none;line-height:1.2}\n"
            + spans + "{font-size:13px;font-weight:600;opacity:.72}\n"
            "/* end cta_scale */</style>\n")


def main():
    total = 0
    for f in PAGES:
        path = os.path.join(SITE, f)
        s = open(path, encoding="utf-8").read()
        if MARK in s:
            s = re.sub(r"\n?<style>" + re.escape(MARK) + r".*?/\* end cta_scale \*/</style>\n?",
                       "", s, flags=re.S)
        names = set()
        for css in re.findall(r"<style>(.*?)</style>", s, re.S):
            names |= slab_ctas(css)
        if not names:
            open(path, "w", encoding="utf-8").write(s)
            continue
        assert "</body>" in s, f
        s = s.replace("</body>", block(names) + "</body>", 1)
        open(path, "w", encoding="utf-8").write(s)
        print("%-44s %s" % (f, ", ".join("." + n for n in sorted(names))))
        total += 1
    print("\n%d page(s) rescaled" % total)


if __name__ == "__main__":
    main()
