#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""8,126 elements render at a weight the page never downloaded.

WHAT WAS REPORTED

"Tyopgrapohy and text still wrong."

WHAT IS TRUE

`font_links.py` established the rule that a page asking for a typeface must
load it. This is the same rule one level down: a page asking for a WEIGHT
must load that weight, and the site was not.

Every element that renders text, measured across all 247 pages, by the face
and weight its CSS asks for - against what the font link actually requests:

    face             link requests        CSS asks for
    Fraunces         400, 600, 700        400, 600, 700, 800, 900
    IBM Plex Mono    400, 500, 600        400, 500, 600, 700, 800
    Inter            400,500,600,700,800  400,500,600,700,800, 900

The gaps, counted:

    Fraunces 800       5,251 elements   -> rendered at 700
    Fraunces 900          83 elements   -> rendered at 700
    IBM Plex Mono 800  1,489 elements   -> rendered at 600
    IBM Plex Mono 700  1,303 elements   -> rendered at 600
    Inter 900              5 elements   -> rendered at 800

8,126 in total, every one of them lighter than the design asks for, on a
site whose display face had just become a serif - where the weight is most
of what makes a heading read as a heading.

Nothing failed. The browser picks the nearest weight it has and renders
without complaint, which is why this survived a type census, a contrast
audit and a design audit.

WHAT EACH FACE CAN ACTUALLY SERVE - CHECKED, NOT ASSUMED

Fetched from the font service with a browser User-Agent and the @font-face
weights counted:

  * `Fraunces:opsz,wght@9..144,...,800;9..144,900` returns 400,600,700,800,900.
    It is variable, so the wider range is the same file, not more files.
  * `Inter:wght@...;900` returns up to 900. Also variable.
  * `IBM+Plex+Mono:wght@...;800` returns 400,500,600,700 - **the request for
    800 is silently dropped, because Plex Mono has no 800.** So the 1,489
    elements asking for it can only ever render at 700, and the fix for them
    is to make 700 available rather than to keep asking for a weight that
    does not exist. Plex Mono is static, so 700 is one additional file - the
    only download this pass adds.

WHAT IT DOES NOT DO

It does not touch the CSS. Nothing is clamped and no declaration is
rewritten: an element asking for Plex Mono 800 still asks for it, and now
resolves to a 700 that is present instead of a 600 that was three steps
away. Changing what the CSS asks for is a design decision; making the page
load what it already asks for is not.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training", "for")

# The mockups choose their own faces and weights on purpose.
SKIP = {"tycoon.html", "concepts.html"}

# face key -> the `family=` fragment it must request. One entry per house
# face; anything else on a link is left exactly as written.
WANT = {
    "Fraunces": "Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700;"
                "9..144,800;9..144,900",
    "Inter": "Inter:wght@400;500;600;700;800;900",
    "IBM+Plex+Mono": "IBM+Plex+Mono:wght@400;500;600;700",
}

LINK = re.compile(r'(<link[^>]+href=")([^"]*fonts\.googleapis\.com[^"]*)(")')


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return out


def fix(href):
    """Rewrite only the fragments for house faces. Order is preserved, so a
    link that already reads correctly is returned byte-identical."""
    changed = False
    parts = href.split("&")
    for i, part in enumerate(parts):
        # The FIRST family rides on the query string itself -
        # `...css2?family=Fraunces:...` - so it does not start with
        # `family=` and an earlier draft skipped it, silently fixing the
        # other two faces and leaving the display face short of 800 on all
        # 244 pages. Split on the `?` too.
        head, sep, tail = part.partition("?family=")
        if sep:
            prefix, frag = head + "?family=", tail
        elif part.startswith("family="):
            prefix, frag = "family=", part[len("family="):]
        else:
            continue
        name = frag.split(":", 1)[0]
        if name in WANT and frag != WANT[name]:
            parts[i] = prefix + WANT[name]
            changed = True
    return "&".join(parts), changed


def main():
    check = "--check" in sys.argv
    hit, bad = 0, []
    for rel in pages():
        if os.path.basename(rel) in SKIP:
            continue
        p = os.path.join(SITE, rel)
        with open(p, encoding="utf-8") as fh:
            t = fh.read()
        out = t
        page_changed = False
        for m in LINK.finditer(t):
            new_href, changed = fix(m.group(2))
            if changed:
                page_changed = True
                if not check:
                    out = out.replace(m.group(0),
                                      m.group(1) + new_href + m.group(3))
        if page_changed:
            if check:
                bad.append(rel)
            else:
                hit += 1
                with open(p, "w", encoding="utf-8") as fh:
                    fh.write(out)

    if check:
        if bad:
            print("  font_weights.py: %d page(s) request a face without the "
                  "weights the site renders it at" % len(bad))
            for b in bad[:6]:
                print("    " + b)
            return 1
        print("  guards clean - every page loads the weights its own CSS asks "
              "each house face to render")
        return 0
    print("  %d page(s): font links widened to the weights the CSS actually "
          "asks for" % hit)
    return 0


if __name__ == "__main__":
    sys.exit(main())
