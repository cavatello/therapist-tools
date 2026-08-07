#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Put _dev/landing.css into the landing page's inline <style> block.

WHY IT IS INLINE AND WHY IT IS STILL A FILE. The landing stylesheet is used by
exactly one page, so _dev/extract_css.py leaves it alone on purpose - a separate
request for 22 kB used once is worse than the inline copy, and it is the first
paint on the page a stranger arrives at. But a 22 kB stylesheet living inside a
155 kB HTML document is not editable: you cannot diff it, and every edit is a
byte-offset surgery on the file that carries the whole page. So it lives here
and this pass installs it.

The block is located by its opening token, not by position. `.lp{` is the first
thing in it and appears nowhere else on the page; matching on <style> alone
would have caught _dev/widen.py's block, which sits three lines further down and
would have been silently overwritten.

Idempotent - installing the same bytes twice is a no-op.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
PAGE = os.path.join(SITE, "index.html")
SRC = os.path.join(HERE, "landing.css")

# every class the markup actually uses. If a rewrite of landing.css drops one of
# these the element is still on the page - it just renders unstyled, which is
# the failure mode that looks like "content went missing" and is not.
NEEDED = [
    "lheroD", "lhd", "lhdp", "lhdph", "lhdr", "leyebrow", "ldeck", "lacts",
    "lcta", "lghost", "lwho", "lsec", "lpaper", "lwrap", "lnarrow", "llede",
    "lwhy", "lans", "lansc", "lansq", "lansb", "lansg", "lgrid", "lg2", "lg3",
    "lpromise", "lkick", "lkicka", "laud", "lmid", "ltool", "lkind", "ltag",
    "lbody", "lbul", "lname", "lfig", "lpair", "lread", "lkit", "lkitrows",
    "lhead", "lhow", "labout", "lnote", "lnews", "lnewsrow", "lconsent",
]


def main():
    css = open(SRC, encoding="utf-8").read()
    missing = [c for c in NEEDED if ("." + c) not in css]
    if missing:
        sys.exit("landing: landing.css has no rule for " + ", ".join(missing))

    s = open(PAGE, encoding="utf-8").read()
    m = re.search(r"<style>\s*\.lp\{[\s\S]*?</style>", s)
    if not m:
        sys.exit("landing: cannot find the .lp style block in index.html")
    new = "<style>" + css + "</style>"
    if m.group(0) == new:
        print("landing: already current")
        return
    s = s[:m.start()] + new + s[m.end():]
    open(PAGE, "w", encoding="utf-8").write(s)
    print("landing: installed %d bytes" % len(css))

    # guard: exactly one .lp block, and the markup it styles is still there
    s2 = open(PAGE, encoding="utf-8").read()
    if len(re.findall(r"<style>\s*\.lp\{", s2)) != 1:
        sys.exit("landing: %d .lp blocks after install"
                 % len(re.findall(r"<style>\s*\.lp\{", s2)))
    for c in ("lheroD", "ltool", "lkit", "lnews", "lans"):
        if 'class="%s' % c not in s2 and '"%s"' % c not in s2 and c not in s2:
            sys.exit("landing: markup for .%s is gone" % c)
    print("landing: guards clean")


if __name__ == "__main__":
    main()
