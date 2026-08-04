#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Global width pass — stop every page dead-ending at ~1120px on a wide display.

The bug, reported from a 27-inch 5K monitor: content sits in a fixed column and
the rest of the screen is empty. It is every page, not one page, because every
page's outer wrap hard-stops somewhere between 1000px and 1180px and then does
nothing above that.

What this does NOT do: widen prose. A 66ch measure is correct and making lines
1400px long would be worse than the bug. So the rule is:

  - centered containers of 1000px or more   -> grow in two steps
  - anything under 1000px                   -> left alone, it is a measure

The selectors are read out of each page's own CSS rather than typed here, so a
page that renames its wrapper keeps working, and a page whose columns are all
prose is correctly left untouched.

Appended last, so it wins on source order at equal specificity.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)

FILES = [f for f in sorted(os.listdir(SITE))
         if f.endswith(".html") and f not in ("tycoon.html", "concepts.html", "local.html")]

# a centered page container: has margin:0 auto (or margin:X auto) AND a max-width
RULE = re.compile(r"([^{}@]+)\{([^{}]*)\}")
MAXW = re.compile(r"max-width:\s*(\d+)px")
CENTERED = re.compile(r"margin:[^;}]*\bauto\b")

FLOOR = 1000        # below this it is a reading measure, not a page container
STEP1 = (1500, 1320)
STEP2 = (1900, 1560)

MARK = "/* _dev/widen.py */"


def containers(css):
    """Selectors in this page that are centered page-level containers."""
    # Strip comments FIRST. Without this a /* ... */ block preceding a rule is
    # swallowed into the selector text, and this project's CSS is heavily
    # commented - the first run emitted "/* slabs: white cards" as a selector.
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    out = []
    for sel, body in RULE.findall(css):
        sel = sel.strip()
        if not sel or sel.startswith(("@", "%")) or ":" in sel.split()[-1][:1]:
            pass
        m = MAXW.search(body)
        if not m or not CENTERED.search(body):
            continue
        if int(m.group(1)) < FLOOR:
            continue
        # skip anything already inside a media query we wrote
        for part in sel.split(","):
            part = part.strip()
            # a real selector: class/id/tag chains only. Anything with prose
            # punctuation in it is a parsing accident, not a selector.
            if not part or not re.fullmatch(r"[.#]?[\w-]+(?:[\s>+~]+[.#]?[\w-]+)*", part):
                continue
            out.append((part, int(m.group(1))))
    return out


def patch(path):
    s = open(path, encoding="utf-8").read()
    # Idempotent: strip the WHOLE previous <style> element, wrapper included.
    # Stripping only MARK..end-widen left an empty <style></style> behind on
    # every run, so each run changed every file and the drift check stopped
    # meaning anything.
    if MARK in s:
        s = re.sub(r"\n?<style>" + re.escape(MARK) + r".*?/\* end widen \*/</style>\n?",
                   "", s, flags=re.S)
    s = re.sub(r"\n?<style>\s*</style>\n?", "\n", s)   # clean up earlier runs
    styles = re.findall(r"<style>(.*?)</style>", s, re.S)
    found = {}
    for css in styles:
        for sel, w in containers(css):
            found[sel] = max(found.get(sel, 0), w)
    if not found:
        return None
    sels = ",".join(sorted(found))
    block = ("\n<style>" + MARK + "\n"
             "@media (min-width:%dpx){%s{max-width:%dpx}}\n"
             "@media (min-width:%dpx){%s{max-width:%dpx}}\n"
             "/* end widen */</style>\n" % (STEP1[0], sels, STEP1[1],
                                            STEP2[0], sels, STEP2[1]))
    assert "</body>" in s, path
    s = s.replace("</body>", block + "</body>", 1)
    open(path, "w", encoding="utf-8").write(s)
    return sorted(found.items())


def main():
    for f in FILES:
        r = patch(os.path.join(SITE, f))
        if r is None:
            print("%-44s no page-level container found" % f)
        else:
            print("%-44s %s" % (f, ", ".join("%s(%d)" % x for x in r)))


if __name__ == "__main__":
    main()
