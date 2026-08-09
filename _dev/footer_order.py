#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The signup band belongs against the footer. Put it there, on every page.

WHAT IT LOOKED LIKE

    ... end of the article
    [ dark band ]   You should not have to work this part out on your own.
    [ cream card ]  Last checked - Figures current as of - Figures checked...
    [ dark footer ] Tools / Topics / Browse / About / The small print

Two dark blocks with a cream card wedged between them. On a phone that reads as
a mistake: the page appears to end, then restarts, then ends again. It was
reported three times.

The cause is ordinary. `_dev/footer_band.py` inserts the signup immediately
before `<footer>`, and `_dev/pixel_concepts.py` later inserts its provenance
card in the same place - so whichever ran last ends up nearest the footer, and
pixel_concepts runs last. Neither pass is wrong; nobody owned the ORDER.

WHAT IT SHOULD BE, AND WHY THIS ORDER

    ... end of the article
    [ cream card ]  the provenance: when this was checked, against what
    [ dark band ]   the ask: leave your email
    [ dark footer ] the map

Provenance belongs with the content it vouches for - it is the last thing you
say about the page. The ask comes after you have finished making the case, not
in the middle of it. And putting the band directly against the footer merges
two dark blocks into one, so the page ends once.

HOW IT IS DONE

This pass owns the order and nothing else. It moves the existing `.ftnl`
section verbatim - no markup is rewritten, no copy changes - to sit immediately
before `<footer>`, after whatever provenance the other passes left there. Run it
last and it is the final word; run it twice and the second run finds the band
already in place and does nothing.

The guard is the useful part: it asserts that on every page carrying both, the
signup band is the LAST element before the footer. That is a property no other
pass checks, which is why this drifted three times.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training")

BAND_OPEN = re.compile(r'<section class="ftnl"')
BAND_MARK = "<!-- _dev/footer_band.py -->"
MARK = "/* _dev/footer_order.py */"

# The band and the footer are both dark. Sitting them together should read as
# one block, not two - so the seam between them is closed.
CSS = """<style>%s
/* The signup band now sits directly on the footer. They are the same colour
   family, so the join has to disappear or it reads as two page endings. */
.ftnl{margin-bottom:0 !important;border-bottom:0}
.ftnl + .sitefoot,
.ftnl + footer{margin-top:0;border-top:0}
.sitefoot{margin-top:0}
</style>""" % MARK


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return out


def band_span(s):
    """(start, end) of the whole signup band, including its own marker."""
    m = BAND_OPEN.search(s)
    if not m:
        return None
    start = m.start()
    if s[:start].rstrip().endswith(BAND_MARK):
        start = s.rindex(BAND_MARK, 0, start)
    end = s.find("</section>", m.end())
    if end < 0:
        return None
    return (start, end + len("</section>"))


def main():
    moved = already = 0
    skipped = []
    for rel in pages():
        p = os.path.join(SITE, rel)
        s = open(p, encoding="utf-8").read()
        orig = s

        span = band_span(s)
        foot = s.rfind("<footer")
        if not span or foot < 0:
            skipped.append(rel)
            continue

        block = s[span[0]:span[1]]
        rest = s[:span[0]] + s[span[1]:]
        foot = rest.rfind("<footer")
        if foot < 0:
            skipped.append(rel)
            continue

        # Is everything between the band and the footer already nothing but
        # whitespace? Then it is where it belongs and the file is left alone.
        between = s[span[1]:s.rfind("<footer")]
        if span[1] < s.rfind("<footer") and not between.strip():
            already += 1
        else:
            s = rest[:foot] + block + "\n" + rest[foot:]
            moved += 1

        s = re.sub(r"\n?<style>" + re.escape(MARK) + r"[\s\S]*?</style>\n?", "", s)
        e = s.lower().rfind("</body>")
        if e > 0:
            s = s[:e] + CSS + "\n" + s[e:]

        if s != orig:
            open(p, "w", encoding="utf-8").write(s)

    print("%d page(s) reordered, %d already correct, %d without both blocks"
          % (moved, already, len(skipped)))

    # ------------------------------------------------------------- guards
    bad = 0
    checked = 0
    for rel in pages():
        s = open(os.path.join(SITE, rel), encoding="utf-8").read()
        span = band_span(s)
        foot = s.rfind("<footer")
        if not span or foot < 0:
            continue
        checked += 1
        if span[1] > foot:
            print("GUARD %s: the band is AFTER the footer" % rel)
            bad += 1
            continue
        between = s[span[1]:foot]
        if between.strip():
            snip = re.sub(r"\s+", " ", between.strip())[:70]
            print("GUARD %s: %d chars between the band and the footer: %s"
                  % (rel, len(between.strip()), snip))
            bad += 1
        if s.count(MARK) != 1:
            print("GUARD %s: %d order stylesheets" % (rel, s.count(MARK)))
            bad += 1
    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean - on all %d page(s) with both, the signup band is the "
          "last thing before the footer" % checked)


if __name__ == "__main__":
    main()
