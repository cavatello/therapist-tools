#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Remove the blocks that were asked for by name, and nothing else.

WHAT WAS ASKED

  "we can get rid of these blocks!"   - the "How it works" and "Who makes this"
                                        sections on the home page
  "can remove these"                  - the What-it-costs / What-it-stores
                                        cards on the about page

WHY THEY EARN REMOVING, BEYOND HAVING BEEN ASKED

All three are the site talking about itself, placed where a reader is trying to
get to a tool. "How it works" appears on BOTH the home page and the about page
with different wording and the same content, which is the clearest possible
sign that neither is load-bearing.

The three fact cards are also redundant twice over. "Nothing you type is sent
anywhere" is on every calculator page, where it is actually relevant. "These
are models and references. Take the shape of a decision to a CPA or an
attorney" is a shorter, weaker version of the disclaimer already in the footer
byline on all 164 pages - the same duplication that was removed from the
footer's small-print column earlier in this session.

REMOVING MARKUP IS THE MOST DANGEROUS KIND OF PASS

Everything else in `_dev/` adds or rewrites. This deletes, and a regex that
matches one character too far takes the rest of the page with it. So:

  - every block is identified by an anchor string AND a required section class,
    and the pass refuses to cut if either is missing
  - the cut is bounded by balanced <section> tags, counted, not by a lazy
    `[\\s\\S]*?</section>` which stops at the first nested close
  - the length removed is checked against an expected range, so a match that
    ran away takes out the build instead of the page
  - what remains is checked for the page's own furniture - nav, footer, h1 -
    because "the page still parses" is not the same as "the page is intact"

Not idempotent in the usual sense: once a block is gone it is gone, so a second
run reports "already removed" and changes nothing.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)

# page, anchor text inside the block, required class on the <section>,
# (min, max) plausible length of the block, why
BLOCKS = [
    ("index.html", "<h2>How it works</h2>", "lsec", (400, 3000),
     "The same content as the about page's version, in the reader's way"),
    ("index.html", "<h2>Who makes this</h2>", "lsec", (300, 2500),
     "The site talking about itself, above the fold of a tool"),
    ("about.html", "<h2>How it works</h2>", "sec", (500, 3500),
     "Heading plus the three fact cards. Two of the three are said better "
     "elsewhere and the third is in the footer on every page"),
]


def section_span(s, anchor, cls):
    """The <section ...class=cls...> ... </section> that contains `anchor`.

    Balanced, because a lazy match to the first </section> would stop inside a
    nested one and leave a stray closing tag behind - which renders as the rest
    of the page moving inside a block that was supposed to be deleted."""
    a = s.find(anchor)
    if a < 0:
        return None
    # walk backwards to the opening <section that carries the class
    start = -1
    for m in re.finditer(r"<section\b[^>]*>", s[:a]):
        if cls in m.group(0):
            start = m.start()
    if start < 0:
        return None
    depth = 0
    for m in re.finditer(r"<section\b[^>]*>|</section\s*>", s[start:]):
        depth += 1 if m.group(0).startswith("<section") else -1
        if depth == 0:
            return (start, start + m.end())
    return None


def main():
    print("removing blocks that were asked for by name:")
    bad = 0
    touched = {}

    for page, anchor, cls, (lo, hi), why in BLOCKS:
        p = os.path.join(SITE, page)
        if not os.path.exists(p):
            print("  MISSING  %s" % page)
            bad += 1
            continue
        s = touched.get(page) or open(p, encoding="utf-8").read()

        span = section_span(s, anchor, cls)
        if not span:
            if anchor not in s:
                print("  already  %-12s %s" % (page, anchor))
                touched[page] = s
                continue
            print("  GUARD    %-12s found %r but no enclosing <section class=%r>"
                  % (page, anchor, cls))
            bad += 1
            continue

        n = span[1] - span[0]
        if not (lo <= n <= hi):
            # The runaway case. Refusing here is the whole point of the pass.
            print("  GUARD    %-12s %s would remove %d chars, expected %d-%d. "
                  "Refusing - a match that ran away takes the page with it."
                  % (page, anchor, n, lo, hi))
            bad += 1
            continue

        s = s[:span[0]] + s[span[1]:]
        touched[page] = s
        print("  ok       %-12s %-26s %5d chars  %s"
              % (page, anchor.replace("<h2>", "").replace("</h2>", ""), n, why[:40]))

    if bad:
        sys.exit("\n%d problem(s) - nothing was written" % bad)

    for page, s in touched.items():
        open(os.path.join(SITE, page), "w", encoding="utf-8").write(s)

    # ------------------------------------------------------------- guards
    # "It still parses" is not "it is intact". Check the furniture.
    for page in sorted(touched):
        s = open(os.path.join(SITE, page), encoding="utf-8").read()
        for what, test in (
            ("no h1", s.count("<h1") != 1),
            ("no nav", "sitenav" not in s),
            ("no footer", "<footer" not in s),
            ("no closing body", "</body>" not in s.lower()),
            ("stray </section>",
             len(re.findall(r"<section\b", s)) != len(re.findall(r"</section", s))),
        ):
            if test:
                print("GUARD %s: %s" % (page, what))
                bad += 1
        for anchor_page, anchor, _c, _r, _w in BLOCKS:
            if anchor_page == page and anchor in s:
                print("GUARD %s: %r survived" % (page, anchor))
                bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("\n%d page(s) written. guards clean - section tags balanced, nav, "
          "footer and h1 all intact" % len(touched))


if __name__ == "__main__":
    main()
