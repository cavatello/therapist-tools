#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Make the tool cards actual links.

"The tools" block on about, contact, newsletter and tools renders four cards -
icon, title, one-line description - that look exactly like the clickable cards
everywhere else on the site and are `<div class="card">`. A reader clicks
"Practice Simulator" and nothing happens.

This converts the div to an anchor, matched by the card's own <h3> rather than
by position, so re-ordering the block cannot mis-link it. Cards whose title is
not in the map are left as divs and reported, so a new card fails loudly rather
than silently pointing nowhere.
"""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
MARK = "/* _dev/link_cards.py */"

DEST = {
    "Practice Simulator": "practice-simulator.html",
    "Tax & Retirement": "therapist-tax-strategy-california.html",
    "Tax &amp; Retirement": "therapist-tax-strategy-california.html",
    "Grow Your Practice": "grow-your-therapy-practice.html",
    "Associate planner": "associate-mft-job-advisor.html",
    "Associate Planner": "associate-mft-job-advisor.html",
    "Cost of Living": "therapist-cost-of-living-california.html",
    "3,000 Hours": "amft-3000-hours-california.html",
}

CSS = """
/* the cards were already styled as if they were links; they just were not */
a.card{display:block;text-decoration:none;color:inherit;
  transition:transform .12s,box-shadow .12s,border-color .12s}
a.card:hover{transform:translateY(-2px);box-shadow:0 8px 22px rgba(38,36,30,.09)}
a.card:focus-visible{outline:3px solid #2C6350;outline-offset:3px}
a.card h3{text-decoration:none}
"""

CARD = re.compile(r'<div class="card">(.*?)</div>', re.S)
H3 = re.compile(r"<h3>(.*?)</h3>", re.S)


def main():
    total, missed = 0, []
    for f in sorted(os.listdir(SITE)):
        if not f.endswith(".html") or f in ("tycoon.html", "local.html", "concepts.html"):
            continue
        path = os.path.join(SITE, f)
        s = open(path, encoding="utf-8").read()
        s = re.sub(r"\n?<style>" + re.escape(MARK) + r".*?/\* end cards \*/</style>\n?",
                   "", s, flags=re.S)
        # already-converted anchors go back to divs first, so this is idempotent
        s = re.sub(r'<a class="card" href="[^"]*">', '<div class="card">', s)
        s = re.sub(r'</a><!--/card-->', "</div>", s)

        n = [0]

        def conv(m):
            inner = m.group(1)
            h = H3.search(inner)
            if not h:
                return m.group(0)
            title = re.sub(r"<[^>]+>", "", h.group(1)).strip()
            href = DEST.get(title)
            if not href:
                missed.append((f, title))
                return m.group(0)
            n[0] += 1
            return '<a class="card" href="%s">%s</a><!--/card-->' % (href, inner)

        s = CARD.sub(conv, s)
        if n[0]:
            s = s.replace("</body>", "\n<style>" + MARK + CSS + "/* end cards */</style>\n</body>", 1)
            open(path, "w", encoding="utf-8").write(s)
            print("%-44s %d cards linked" % (f, n[0]))
            total += n[0]
        else:
            open(path, "w", encoding="utf-8").write(s)

    for f, t in missed:
        print("  UNMAPPED  %-42s %r" % (f, t))
    print("\n%d cards linked, %d unmapped" % (total, len(missed)))


if __name__ == "__main__":
    main()
