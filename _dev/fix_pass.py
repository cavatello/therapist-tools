#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""One pass over the published set for four live defects.

1. DUPLICATE NAV DESTINATION. The Tools menu carried both "Practice Simulator"
   and "Full simulator", and after app.js was deleted BOTH point at
   practice-simulator.html. Two labels, two descriptions, one page. The second
   is a leftover from when the React app was a separate thing.

2. PROTOTYPE FOOTER ON THE LIVE SITE. practice-simulator.html is built by
   splicing the prototype, and the chrome lift replaces the masthead but never
   the footer - so the page shipped saying "Prototype, not the live site."
   Replaced with the global footer every other page carries.

3. WHITE ON WHITE. grow-your-therapy-practice.html carries a hand-written
   <b style="color:#fff"> inside a block that sits on a WHITE card, so the bold
   label of every line in that list is invisible. The dash and the description
   render; the thing being described does not.

4. A DEAD DESTINATION. That same block's CTA points at index.html, which used
   to be the simulator and is now the landing page. "Model the whole practice"
   should land on the simulator.

Idempotent: each fix checks for its own precondition and reports if absent.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
SIM = "practice-simulator.html"

PAGES = [f for f in sorted(os.listdir(SITE))
         if f.endswith(".html") and f not in ("tycoon.html", "local.html")]

log = []


def read(f):
    return open(os.path.join(SITE, f), encoding="utf-8").read()


def write(f, s):
    open(os.path.join(SITE, f), "w", encoding="utf-8").write(s)


# --------------------------------------------------------------- 1. nav ---
# Cut the whole <a>...</a> whose label is "Full simulator". Matched from the
# <a that precedes it rather than by a fixed string, because the icon is an
# inline data-URI that differs per page.
def drop_full_sim(s):
    """The entry appears TWICE per page in two different shapes: the rich panel
    item (icon + <b>label</b> + <i>description</i>) and a plain text link in the
    compact list. Removing only the first left the second on every page."""
    n = 0
    # plain link first - it is unambiguous
    s, k = re.subn(r'<a href="[^"]*"[^>]*>\s*Full simulator\s*</a>', "", s)
    n += k
    while True:
        i = s.find("<b>Full simulator</b>")
        if i < 0:
            break
        start = s.rfind("<a ", 0, i)
        end = s.find("</a>", i)
        if start < 0 or end < 0:
            break
        s = s[:start] + s[end + 4:]
        n += 1
    return s, n > 0


# ------------------------------------------------------------ 2. footer ---
def global_footer(s):
    m = re.search(r"<footer\b.*?</footer>", s, re.S)
    return m.group(0) if m else None


def main():
    # a page that is known good is the donor for the footer
    donor = global_footer(read("tools.html"))
    assert donor and "Prototype" not in donor, "donor footer is wrong"

    for f in PAGES:
        s = orig = read(f)

        s, hit = drop_full_sim(s)
        if hit:
            log.append("%-44s nav: dropped duplicate 'Full simulator' entries" % f)

        if "Prototype, not the live site" in s:
            cur = global_footer(s)
            if cur:
                s = s.replace(cur, donor, 1)
                log.append("%-44s footer: prototype footer -> global footer" % f)
            # the prototype's own footer block may not be a <footer> at all
            s = re.sub(r"<div class=\"proto[^\"]*\">.*?</div>", "", s, flags=re.S)

        if 'style="color:#fff"' in s and f.startswith("grow"):
            n = s.count('<b style="color:#fff">')
            # that block sits on a white card. Use the page's own ink colour.
            s = s.replace('<b style="color:#fff">', '<b style="color:#26241E">')
            log.append("%-44s contrast: %d white-on-white labels -> ink" % (f, n))

        if f.startswith("grow") and '<a class="gcta" href="index.html"' in s:
            s = s.replace('<a class="gcta" href="index.html"',
                          '<a class="gcta" href="%s"' % SIM)
            log.append("%-44s link: 'Model the whole practice' index -> %s" % (f, SIM))

        if s != orig:
            write(f, s)

    # ---- guards -----------------------------------------------------------
    for f in PAGES:
        s = read(f)
        assert "Full simulator" not in s, "nav entry survived in " + f
        assert "Prototype, not the live site" not in s, "prototype footer in " + f
        if f not in ("concepts.html",):
            assert s.count("<footer") == 1, "%s has %d footers" % (f, s.count("<footer"))
    print("\n".join(log) if log else "nothing to do")
    print("\n%d changes" % len(log))


if __name__ == "__main__":
    main()
