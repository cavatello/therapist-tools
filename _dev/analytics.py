#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Put ONE Google Analytics property on EVERY page, and keep it that way.

WHAT WAS ACTUALLY WRONG. The old property (G-BHXXEN4P0X) was on 16 of 133
pages. Every school page, every psychedelic training page, every topic hub and
the whole content library were uninstrumented - which is worse than having no
analytics at all, because the numbers that did arrive looked like a complete
picture of a site whose traffic was mostly landing somewhere it could not see.
The tag had been pasted by hand into pages as they were written, so coverage
tracked nothing but whoever remembered.

Hence a pass rather than a paste. The tag is now a property of the site, not of
the page, and the guard at the bottom fails if any page is missing it or is
carrying two.

WHERE IT GOES. Immediately before </head>, which is where Google's own snippet
says to put it and, more usefully here, is a position that exists on every page
regardless of template. Anchoring to "after the last <meta>" or "before the
first <link>" would have been a position that some of these 133 pages do not
have.

IDEMPOTENT. It strips any tag it finds - including the old property's - before
inserting, so running it twice does not stack two gtag blocks, and changing ID
below and re-running is the supported way to move properties.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training")

ID = "G-XJCWHH9SFG"

# Every property this site has ever carried. Listed so the stripper removes the
# OLD tag rather than leaving two configs firing at two properties, which is the
# failure mode that makes a migration look like a traffic collapse.
RETIRED_IDS = ["G-BHXXEN4P0X"]

# WHERE THE LIVE PROPERTY ACTUALLY IS, because it took a wrong turn to find it
# and the next person should not repeat it.
#
#   G-XJCWHH9SFG  property "Therapistsupport" (549050855)
#                 account  palo-alto-therapist.com (392417713)
#                 stream   "Therapist Support" (15401186123)
#
# There is a SEPARATE property called "Github Therapy Tools" (547356777) under
# the "Google Ads Account" (372904968) whose stream carries the RETIRED id
# above and still points at https://cavatello.github.io/therapist-tools/. It
# is not this site. Custom dimensions created there are invisible to these
# pages, which is exactly the mistake that was made once.
LIVE_PROPERTY = "a392417713p549050855"

TAG = (
    "<!-- Google tag (gtag.js) -->\n"
    '<script async src="https://www.googletagmanager.com/gtag/js?id=%s"></script>\n'
    "<script>\n"
    "  window.dataLayer = window.dataLayer || [];\n"
    "  function gtag(){dataLayer.push(arguments);}\n"
    "  gtag('js', new Date());\n"
    "  gtag('config', '%s');\n"
    "</script>\n" % (ID, ID)
)

# The comment is optional in the wild, the two <script> tags are not. Matched as
# a unit so a partial strip cannot leave the loader without its config.
BLOCK = re.compile(
    r"(?:<!--\s*Google tag \(gtag\.js\)\s*-->\s*)?"
    r'<script[^>]*src="https://www\.googletagmanager\.com/gtag/js\?id=[^"]*"[^>]*>'
    r"\s*</script>\s*"
    r"<script>\s*window\.dataLayer.*?</script>\s*",
    re.S)

# Pages that are not the site. tycoon.html and concepts.html are internal
# mockups and robots.txt already disallows them; instrumenting them would put
# scratch pageviews in the same property as real ones.
SKIP = {"tycoon.html", "concepts.html"}


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return [f for f in out if os.path.basename(f) not in SKIP]


def main():
    added, moved, kept, nohead = 0, 0, 0, []
    for rel in pages():
        p = os.path.join(SITE, rel)
        s = open(p, encoding="utf-8").read()
        orig = s
        had_old = any(i in s for i in RETIRED_IDS)
        had_any = bool(BLOCK.search(s))

        s = BLOCK.sub("", s)
        # A stray config line left behind by a hand edit, with no loader.
        s = re.sub(r"\s*gtag\('config', '(?:%s)'\);" % "|".join(RETIRED_IDS), "", s)

        i = s.lower().find("</head>")
        if i < 0:
            nohead.append(rel)
            continue
        s = s[:i] + TAG + s[i:]

        if s != orig:
            open(p, "w", encoding="utf-8").write(s)
            if had_old:
                moved += 1
            elif had_any:
                kept += 1
            else:
                added += 1

    # The privacy policy NAMES the measurement ID in prose - correctly, since a
    # policy that describes a property the site does not run is inaccurate in
    # the one document where accuracy is the whole point. It is not a tag, so
    # the block stripper never sees it; it has to be swapped by hand.
    pol = os.path.join(SITE, "privacy.html")
    if os.path.exists(pol):
        s = open(pol, encoding="utf-8").read()
        for old in RETIRED_IDS:
            if "measurement ID %s" % old in s:
                s = s.replace("measurement ID %s" % old, "measurement ID %s" % ID)
                open(pol, "w", encoding="utf-8").write(s)
                print("privacy.html: policy text now names %s" % ID)

    print("%d page(s) newly instrumented" % added)
    print("%d page(s) moved off %s" % (moved, ", ".join(RETIRED_IDS)))
    print("%d page(s) re-emitted" % kept)
    if nohead:
        print("NO </head>: %s" % ", ".join(nohead))

    bad = 0
    for rel in pages():
        s = open(os.path.join(SITE, rel), encoding="utf-8").read()
        n = s.count('gtag/js?id=%s' % ID)
        if n != 1:
            print("GUARD %s: %d loader(s), expected 1" % (rel, n))
            bad += 1
        for old in RETIRED_IDS:
            if old in s:
                print("GUARD %s: still carries %s" % (rel, old))
                bad += 1
        if s.count("gtag('config'") != 1:
            print("GUARD %s: %d config call(s)" % (rel, s.count("gtag('config'")))
            bad += 1
    if bad or nohead:
        sys.exit("\n%d problem(s) - do not let this publish" % (bad + len(nohead)))
    print("guards clean - %d page(s) on %s" % (len(pages()), ID))


if __name__ == "__main__":
    main()
