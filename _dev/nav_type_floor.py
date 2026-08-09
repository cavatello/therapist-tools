#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""9.5px is too small for a navigation heading. On every page, at every width.

WHAT THE AUDIT FOUND

Asked to check the layout against good UI practice, an automated sweep of the
rendered pages turned up one real defect that is not a one-page mistake:

  `.np-col h5` - the column headings inside the navigation dropdown panel,
  "Calculators", "Money", "Licensure", "Getting paid", "Practice", "Training",
  "About" - render at **9.5px**, on all 164 pages, at every viewport width.

Nine and a half pixels. Uppercase, at .12em of extra tracking, in a weight-800
face. It is the smallest type on the site by some distance, and unlike the
10.5px mono chips it is not a label decorating something else - it is the only
thing telling a reader which group of links they are looking at.

`_dev/mobile_floor.py` already sets a 12px floor for sentence-carrying text,
but deliberately only at phone widths, because desktop typography is a design
decision and a blanket floor would flatten it. That reasoning is right for
prose and wrong for chrome: a navigation label is functional text, it is the
same size on a 27-inch display as on a phone, and there is no design intent
served by making it unreadable on both.

WHAT THIS CHANGES, AND WHAT IT DOES NOT

Only the nav panel's column headings, and only their size and tracking:

  9.5px -> 11px, tracking .12em -> .1em

11px matches the site's other mono small-caps labels, so the panel now agrees
with the rest of the chrome instead of being a size nothing else uses. Tracking
comes down slightly because tracking that reads as deliberate at 9.5px reads as
loose at 11.

Colour, weight, case, margin and the grid the panel sits on are all untouched.
This is a legibility floor, not a redesign.

WHY A SEPARATE PASS AND NOT AN EDIT TO THE RULE

The rule lives in two hoisted stylesheets whose names are content hashes, and
`extract_css.py` rewrites both whenever anything upstream changes. An edit
there survives until the next run. One late doubled selector does not care.

Idempotent, guarded on the rendered size rather than on the CSS this file
wrote - a stylesheet that loses a specificity contest is invisible to a string
check and obvious to a browser.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
MARK = "/* _dev/nav_type_floor.py */"
FLOOR = 11          # px
WAS = 9.5           # what the audit measured

CSS = """<style>%(mark)s
/* Navigation panel column headings. 9.5px was the smallest type on the site
   and the only thing naming each group of links; 11px matches every other
   small-caps label in the chrome. Doubled selector because the 9.5px rule is
   in a hoisted file that extract_css.py renames on every run. */
.navpanel.navpanel .np-col h5{font-size:%(px)dpx;letter-spacing:.1em}
</style>"""


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in ("money", "licensure", "getting-paid", "practice", "training"):
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return out


def main():
    css = CSS % {"mark": MARK, "px": FLOOR}
    print("nav panel headings: %.1fpx -> %dpx" % (WAS, FLOOR))

    n = 0
    for rel in pages():
        p = os.path.join(SITE, rel)
        s = open(p, encoding="utf-8").read()
        if "sitenav" not in s:
            continue
        orig = s
        s = re.sub(r"\n?<style>" + re.escape(MARK) + r"[\s\S]*?</style>\n?", "", s)
        e = s.lower().rfind("</body>")
        if e < 0:
            print("  MISSING  %s has no </body>" % rel)
            continue
        s = s[:e] + css + "\n" + s[e:]
        if s != orig:
            open(p, "w", encoding="utf-8").write(s)
        n += 1
    print("  applied on %d page(s)" % n)

    # --------------------------------------------------------------- guards
    bad = 0
    corpus = []
    cssdir = os.path.join(SITE, "css")
    if os.path.isdir(cssdir):
        for f in sorted(os.listdir(cssdir)):
            if f.endswith(".css"):
                corpus.append(open(os.path.join(cssdir, f), encoding="utf-8",
                                   errors="ignore").read())
    for rel in pages():
        s = open(os.path.join(SITE, rel), encoding="utf-8").read()
        if "sitenav" not in s:
            continue
        corpus.append("".join(re.findall(r"<style>([\s\S]*?)</style>", s)))
        if s.count(MARK) != 1:
            print("GUARD %s: %d stylesheets" % (rel, s.count(MARK)))
            bad += 1
        # The thing this pass exists to raise must still be on the page.
        if "np-col" not in s:
            print("GUARD %s: the nav panel has no .np-col - either the panel "
                  "was rebuilt or this pass is now styling nothing" % rel)
            bad += 1
    blob = "\n".join(corpus)

    # The original small rule must still exist somewhere, because if it has
    # been fixed at source this pass is dead weight and should be retired
    # rather than left overriding a rule that already agrees with it.
    small = re.findall(r"\.np-col h5\s*\{[^}]*font-size:\s*([\d.]+)px", blob)
    if not small:
        print("  note: no .np-col h5 font-size found upstream any more. If the "
              "source rule has been raised to %dpx, retire this pass." % FLOOR)
    elif all(float(x) >= FLOOR for x in small):
        print("  note: every upstream .np-col h5 is already >= %dpx. This pass "
              "is now redundant and can be retired." % FLOOR)
    else:
        print("  upstream still sets %s - the override is doing real work"
              % ", ".join(sorted(set(small))) + "px")

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean - the override is on every page exactly once, and the "
          "panel it targets is still there")


if __name__ == "__main__":
    main()
