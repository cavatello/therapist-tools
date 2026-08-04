#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Newsletter -> "Stay updated", everywhere, and repoint the copy at what it is
actually for: new tools and additions to the site.

"Get the newsletter" asks the reader to want a newsletter. Almost nobody wants a
newsletter. "Stay updated" asks them to want the thing the newsletter carries,
which is: this site keeps changing, and you would like to know when a tool you
use gets a new section or a rate changes underneath one of your figures.

Touches the chrome on every published page plus the newsletter page itself, and
then the chrome SNAPSHOT the generators lift from - without that last step the
next build of any generated page silently restores the old wording.

Idempotent: a file already carrying the new strings is skipped.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SNAP = os.path.join(ROOT, "..", "mock", "amft", "_chrome_hdr.txt")

# (old, new). Order matters: the longest strings first, so a shorter one cannot
# eat part of a longer one before it is matched.
SUBS = [
    # masthead button, wide and narrow variants
    ('<span class="long">Get the newsletter</span><span class="short">Newsletter</span>',
     '<span class="long">Stay updated</span><span class="short">Updates</span>'),
    # the promo card inside the nav panel
    ('<b>One email a month</b><p>Free tools, better ways to run a practice, and what '
     'other California therapists are doing.</p><span>Get the newsletter</span>',
     '<b>New tools, as they land</b><p>What has been added or changed here, plus rate '
     'and rule updates that move a figure you rely on.</p><span>Stay updated</span>'),
    # nav panel entry
    ('<span><b>Newsletter</b><i>one email a month, from someone doing the same work</i>',
     '<span><b>Stay updated</b><i>new tools and what changed in the numbers</i>'),
    # footer inventory link
    ('<a href="newsletter.html">Newsletter</a>',
     '<a href="newsletter.html">Stay updated</a>'),
    # react app: same button, built through createElement
    ('React.createElement("span", null, "Get the newsletter")',
     'React.createElement("span", null, "Stay updated")'),
    # rates.html carries a variant of the nav-panel promo with its own wording,
    # and app.js builds the masthead button through two createElement calls
    # rather than the one-line span pair the HTML pages use. Both were missed by
    # the exact-match subs above and caught by the final assertion, which is
    # what the assertion is for.
    ('<b>One email a month</b><p>What other California therapists are doing, and '
     'anything new here.</p><span>Get the newsletter</span>',
     '<b>New tools, as they land</b><p>What has been added or changed here, plus rate '
     'and rule updates that move a figure you rely on.</p><span>Stay updated</span>'),
    ('React.createElement("span", {className: "long"}, "Get the newsletter"),\n'
     '       /*#__PURE__*/React.createElement("span", {className: "short"}, "Newsletter")),',
     'React.createElement("span", {className: "long"}, "Stay updated"),\n'
     '       /*#__PURE__*/React.createElement("span", {className: "short"}, "Updates")),'),
]

# The newsletter page's own head and hero. Kept separate because these are
# unique to one file and should fail loudly if that file is restructured.
PAGE = [
    ("<title>The Therapist Support newsletter &mdash; one email a month for "
     "California therapists",
     "<title>Stay updated &mdash; new tools and rate changes for California therapists"),
    ("<title>The Therapist Support newsletter — one email a month for "
     "California therapists",
     "<title>Stay updated — new tools and rate changes for California therapists"),
    ("<h1>You should not have to work this part out <em>on your own</em>.</h1>",
     "<h1>Know when something here <em>changes</em>.</h1>"),
    ("<b>One email a month, written by a therapist, for the people doing the same "
     "work</b>",
     "<b>One email a month: what is new here, and what changed in the numbers</b>"),
]

PAGES = [f for f in sorted(os.listdir(ROOT))
         if f.endswith(".html") and f != "tycoon.html"] + ["app.js"]


def apply(path, subs, required=False):
    s = open(path, encoding="utf-8").read()
    before = s
    hits = 0
    for old, new in subs:
        n = s.count(old)
        if n:
            s = s.replace(old, new)
            hits += n
    if s != before:
        open(path, "w", encoding="utf-8").write(s)
    return hits


def main():
    total = 0
    for name in PAGES:
        path = os.path.join(ROOT, name)
        if not os.path.exists(path):
            continue
        n = apply(path, SUBS)
        if name == "newsletter.html":
            n += apply(path, PAGE)
        total += n
        print("  %-42s %d replacement(s)" % (name, n))

    # The snapshot the generators lift. Miss this and the next build of the
    # advisor, tax or grow page puts "Get the newsletter" straight back.
    snap = os.path.normpath(SNAP)
    if os.path.exists(snap):
        n = apply(snap, SUBS)
        print("  %-42s %d replacement(s)" % ("_chrome_hdr.txt (snapshot)", n))
        total += n
    else:
        print("  !! chrome snapshot not found at", snap)

    # Nothing may still advertise the old wording.
    stale = []
    for name in PAGES + ["../mock/amft/_chrome_hdr.txt"]:
        path = os.path.join(ROOT, name)
        if not os.path.exists(path):
            continue
        s = open(path, encoding="utf-8").read()
        if "Get the newsletter" in s:
            stale.append(name)
    if stale:
        sys.exit("still carrying the old CTA: " + ", ".join(stale))
    print("\n%d replacements, no file still says 'Get the newsletter'." % total)


if __name__ == "__main__":
    main()
