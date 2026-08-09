#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Put the footer on every page, and the legal links in every footer.

Three published pages - the Job Advisor, the tax page and the grow page - had no
<footer> at all. The chrome lift took the masthead and the nav panel; the footer
markup was never taken, so those pages simply stop. The CSS was already there,
which is why nobody noticed: nothing looked broken, there was just nothing at
the bottom.

This does two jobs:
  1. inserts the lifted footer before </body> on any page missing one
  2. rewrites the small-print column on every page to carry Terms and Privacy

Idempotent. Run it after any rebuild that regenerates a page from the chrome.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FTR = os.path.normpath(os.path.join(ROOT, "..", "mock", "amft", "_chrome_ftr.txt"))
assert os.path.exists(FTR), "run mock/legal/build_legal.py first - it writes the snapshot"
FOOTER = open(FTR, encoding="utf-8").read()

# Pages that get a footer. tycoon.html belongs to another session and is never
# touched; concepts.html is a scratch page with no chrome.
SKIP = {"tycoon.html", "concepts.html", "local.html"}
PAGES = [f for f in sorted(os.listdir(ROOT))
         if f.endswith(".html") and f not in SKIP]

OLD_SMALL = re.compile(
    r"<div><h5>The small print</h5>.*?</div>", re.S)
NEW_SMALL = ("<div><h5>The small print</h5>"
             '<a href="terms.html">Terms of Use</a>'
             '<a href="privacy.html">Privacy</a>'
             '<a href="contact.html">Report a wrong figure</a>'
             # The byline directly below this column already says "nothing here is
             # legal, tax, financial or clinical advice". Saying it again three
             # inches higher read as a mistake, and it was one. What is left here
             # is the part the byline does NOT say: which year the figures are.
             "<p>Figures are 2026 federal and California rates, each carrying "
             "the date it was last checked.</p></div>")

OLD_BY = re.compile(r'<p class="ftby">.*?</p>', re.S)
NEW_BY = ('<p class="ftby"><b>Built by Cavatello.</b> Free, and not selling anything. '
          'Nothing here is legal, tax, financial or clinical advice, and using this site '
          'does not create a professional relationship &mdash; see the '
          '<a href="terms.html">Terms of Use</a>.</p>')

added, updated, replaced = [], [], []

for name in PAGES:
    path = os.path.join(ROOT, name)
    s = open(path, encoding="utf-8").read()
    before = s

    # index.html still carries the PROTOTYPE's own footer - a different element
    # (.foot, not .sitefoot) whose first line reads "Prototype, not the live
    # site." on the live site. It is replaced wholesale rather than patched:
    # the words are wrong, and the structure has no small-print column to fix.
    if "<footer" in s and 'class="sitefoot"' not in s:
        s = re.sub(r"<footer.*?</footer>", lambda m: FOOTER, s, count=1, flags=re.S)
        replaced.append(name)
        open(path, "w", encoding="utf-8").write(s)
        continue

    if "<footer" not in s:
        # Before </body>, after everything else. A footer inside <main> would
        # inherit the page's own scoped styles and land on the wrong ground.
        i = s.rfind("</body>")
        assert i > 0, name + ": no </body>"
        s = s[:i] + "\n" + FOOTER + "\n" + s[i:]
        added.append(name)
    else:
        if OLD_SMALL.search(s):
            s = OLD_SMALL.sub(lambda m: NEW_SMALL, s, count=1)
        if OLD_BY.search(s):
            s = OLD_BY.sub(lambda m: NEW_BY, s, count=1)
        if s != before:
            updated.append(name)

    if s != before:
        open(path, "w", encoding="utf-8").write(s)

print("footer added to  :", ", ".join(added) or "(none)")
print("footer updated on:", ", ".join(updated) or "(none)")
print("footer replaced on:", ", ".join(replaced) or "(none)")

# --- assertions. Every page must now have exactly one footer, carrying both
#     legal links, and both legal pages must exist.
bad = []
for name in PAGES:
    s = open(os.path.join(ROOT, name), encoding="utf-8").read()
    n = s.count("<footer")
    if n != 1:
        bad.append("%s: %d footers" % (name, n))
    elif 'href="terms.html"' not in s or 'href="privacy.html"' not in s:
        bad.append("%s: footer missing a legal link" % name)
for f in ("terms.html", "privacy.html"):
    if not os.path.exists(os.path.join(ROOT, f)):
        bad.append("%s does not exist" % f)
if bad:
    sys.exit("FAILED\n  " + "\n  ".join(bad))
print("\nAll %d pages carry one footer with Terms and Privacy." % len(PAGES))
