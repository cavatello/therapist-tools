#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Put the signup band at the top of the footer, on every page.

It was on four pages out of 134. The site's one conversion surface existed on
about, contact, newsletter and rates — three of which are pages a reader
reaches only if they already care. The pages that actually receive search
traffic, the 78 school pages and the articles, had no signup at all.

WHERE IT GOES, AND WHY THAT ORDER

    …page content
    signup band          ← here
    "More on this"       (the up-link)
    site footer

The band is the last thing that asks for something, and the up-link is the last
thing that offers something. A reader who does not want the newsletter scrolls
straight past into three more things to read; a reader who does never has to
find it. Putting the ask after the offer would mean the last thing on every
page is a form.

The pixel-concept foot block (last checked, review badge) sits above all three.
Provenance, then ask, then offer, then chrome.

ONE COPY PER PAGE. The band carries a form with `id="ft-email"`, and duplicate
ids inside one document break the label association for screen readers and make
the second field unlabelled. The pass removes any existing copy before it
inserts, and the guard fails on two.

The markup is lifted from about.html rather than retyped, so the 13KB inline
pixel-art SVG, the field names, the consent wording and the Formspree endpoint
all stay byte-identical to the version that already works.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training")
SOURCE = os.path.join(SITE, "about.html")

MARK = "<!-- _dev/footer_band.py -->"
END = "<!-- /footer_band -->"

# Pages that must not get it, and why.
SKIP = {
    "newsletter.html": "the whole page is the signup",
    "contact.html": "already ends in a form; two forms in a column is a maze",
    "about.html": "carries the original copy this pass clones",
    "rates.html": "carries its own, tuned to the article",
    "tycoon.html": "a mockup",
    "concepts.html": "a mockup",
    "privacy.html": "policy pages should not sell",
    "terms.html": "policy pages should not sell",
    "affiliate-disclosure.html": "policy pages should not sell",
}


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return out


def band(depth):
    s = open(SOURCE, encoding="utf-8").read()
    i = s.find('<section class="ftnl">')
    if i < 0:
        sys.exit("footer_band: about.html no longer carries the band")
    j = s.index("</section>", i) + len("</section>")
    blk = s[i:j]
    # Nothing in the band is a relative link today, but if one is ever added it
    # has to survive being dropped into a page one directory down.
    if depth:
        up = "../" * depth
        blk = re.sub(r'href="(?!https?:|mailto:|#|\.\./)([^"]+)"',
                     lambda m: 'href="%s%s"' % (up, m.group(1)), blk)
    # The id is unique per page, not per site, but a page that somehow ends up
    # with two bands would otherwise carry two #ft-email.
    return MARK + blk + END


def main():
    added, cleaned, skipped = 0, 0, 0
    for rel in pages():
        base = os.path.basename(rel)
        p = os.path.join(SITE, rel)
        s = open(p, encoding="utf-8").read()
        orig = s

        # Always strip our own previous copy first.
        #
        # This used to be one non-greedy MARK...END match, which assumes the two
        # markers are still adjacent and still in that order. `_dev/footer_order.py`
        # later moves the band - and, as written, ONLY the band - down to sit
        # against the footer, leaving END behind above the relocated MARK. The
        # regex then matched nothing, the strip silently did nothing, and this
        # pass inserted a SECOND signup band on 125 pages. The guard below
        # caught it. The stripper should not have needed the guard.
        #
        # So strip what is actually on the page rather than what this pass
        # believes it wrote: the bracketed block if the markers still bracket
        # it, then any surviving band, then any orphaned marker.
        s = re.sub(re.escape(MARK) + r"[\s\S]*?" + re.escape(END), "", s)
        if base not in SKIP:
            # Only on the pages this pass owns. about.html is the SOURCE the
            # band is cloned from and rates.html carries its own copy tuned to
            # that article; a blanket `<section class="ftnl">` strip deletes
            # those originals, which is what the first version of this fix did.
            s = re.sub(r'<section class="ftnl">[\s\S]*?</section>', "", s)
            s = s.replace(MARK, "").replace(END, "")

        if base in SKIP or "sitefoot" not in s:
            if s != orig:
                open(p, "w", encoding="utf-8").write(s)
                cleaned += 1
            skipped += 1
            continue

        blk = band(rel.count("/"))

        # above the up-link if there is one, else directly above the footer
        anchor = None
        for pat in (r"<!-- _dev/uplinks\.py -->", r'<section class="uplink"',
                    r"<footer"):
            m = re.search(pat, s)
            if m:
                anchor = m.start()
                break
        if anchor is None:
            skipped += 1
            continue
        s = s[:anchor] + blk + s[anchor:]

        if s != orig:
            open(p, "w", encoding="utf-8").write(s)
            added += 1

    print("%d page(s) given the band, %d skipped, %d cleaned" %
          (added, skipped, cleaned))

    bad = 0
    for rel in pages():
        s = open(os.path.join(SITE, rel), encoding="utf-8").read()
        n = s.count('<section class="ftnl">')
        if n > 1:
            print("GUARD %s: %d bands - duplicate id=ft-email" % (rel, n))
            bad += 1
        if s.count(MARK) != s.count(END):
            print("GUARD %s: unbalanced markers" % rel)
            bad += 1
        # it must sit ABOVE the footer, not inside it
        i, f = s.find(MARK), s.find("<footer")
        if i >= 0 and f >= 0 and i > f:
            print("GUARD %s: band is inside the footer" % rel)
            bad += 1
    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean")


if __name__ == "__main__":
    main()
