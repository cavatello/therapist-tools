#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The contrast nobody could see, because it does not exist until you use it.

WHAT WAS WRONG

Reported from a phone, not from an audit: the calculator pages are hard to
read. Measured at 390px with the tools actually driven, the worst text on the
site sits at **1.29:1** against a required 4.5, and there are eighteen
failures across three of the seven calculators.

  1.29:1   .verdict p                 the light card's own text
  1.30:1   #plan .finish b            the licence date, 27px
  1.75:1   #plan .finish em           the label above it
  2.18:1   .slab.indigo .rw i         six ledger rows on the tax page
  3.49:1   .pr-num u                  the simulator's hint text
  4.32:1   .apanel .anote  /  .tpanel .pr em

WHY NO GUARD SAW IT. TWO BLIND SPOTS, AND THE SECOND IS THE INTERESTING ONE.

  1. `_dev/_contrast_audit.mjs` runs at 1440 and only at 1440. Eight of these
     are present on load, at 390, and it has never looked at that width.
  2. The other ten DO NOT EXIST until the calculator runs. The ledger is
     written by JavaScript on input; in the delivered HTML it is a hidden
     template with zero height, so the audit measures nothing and moves on.

Every guard in this repository measures the document. Seven of these pages are
applications, and on an application the document is the least of what a reader
sees. That is a new category of blind spot, not a missed case - and it applies
to overflow, tap targets and type scale exactly as much as to contrast.

FOUR SEPARATE CAUSES, NOT ONE

  A. A house pass's `!important` beat the page's own dark-mode colour.
     `associate-mft-job-advisor.html` authors a proper dark plaque -
     `#plan .finish em{color:#84AC99}`, `#plan .finish p{color:#C6DBD1}`,
     both correct - and `house-tool.css` carries
     `body.bct .finish em{color:#2C6350 !important}`, written for the light
     state, which wins. The page was right and the sitewide fix broke it.

  B. A dark-surface colour authored wrongly in the first place.
     `#plan .finish b{color:#8A6516}` is a light-surface amber sitting on deep
     pine. Even without (A) it fails. Gold is this system's dark-surface
     emphasis - it is what `.slab .eb` already uses.

  C. A band's text colour leaking into a light card nested inside it.
     `.bc2 .slab p{color:#C6DBD1}` is correct for a dark band and catastrophic
     for `.verdict.bad`, a pale pink card that happens to live inside one.
     1.29:1 - very nearly invisible, and it is the sentence telling somebody
     the structure is not worth it.

  D. Alpha whites set slightly too faint. `rgba(255,255,255,.5)` on deep pine
     is 4.32, and `.42` is 3.49. Raising to `.62` gives 5.74 and keeps the
     quieter-than-white intent the author wanted.

This is the eleventh, twelfth and thirteenth time on this site that one class
has turned out to name two surfaces. What is new is that (A) is the house
fix causing it rather than missing it.

HOW IT IS FIXED

Re-asserted, not rewritten. Every value below is either the page's OWN intent
restored (A and C) or the system's dark-surface token (B and D), set with
enough specificity to beat both the page's inline CSS and the house sheets'
`!important`. `#plan` is an id, so `#plan .finish em` outranks
`body.bct .finish em` on specificity rather than on order.

Ships inline, in LAST, after the hoisting chain - same reasoning as
`mobile_reassert.py`. A colour fix that a later pass can unlink is not a fix.

Every replacement is stated with its measured ratio, and the driven audit
re-measures all of them.

TWO OVER-REACHES THE FIRST VERSION MADE, BOTH CAUGHT BY RE-MEASURING

  * `#plan .finish` is DARK on `associate-mft-job-advisor.html` and CREAM
    (`#FDF4DF`) on `amft-3000-hours-california.html`. Same id, same class, two
    surfaces - the fourteenth instance, and this pass walked straight into it,
    turning a page that had ZERO failures into one with three, the worst at
    1.11:1. The plaque rules are now emitted only where the page's own CSS
    declares `#plan .finish{...background:#123C30}`, which is the fact that
    makes them correct. Detected, not assumed.

  * `.slab.indigo i` matched an `<i>` inside a white table cell nested in the
    indigo band, taking `.paytab td i` from readable to 1.45:1. Narrowed to
    `.slab.indigo .rw i`, the ledger row it was written for.

Both are the same lesson in different clothes, and it is the lesson this whole
file is about: **a selector is not a surface.** You cannot tell from a
selector what a thing will be painted on. Either scope to a fact you have
checked, or measure the result - and this pass now does both.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)

MARK = "<!-- _dev/tool_surface.py -->"
END = "<!-- /_dev/tool_surface.py -->"
CSS_MARK = "/* _dev/tool_surface.py */"
CSS_END = "/* /_dev/tool_surface.py */"

# The seven calculator pages. The rules are inert where the structure is
# absent, and byte-identical everywhere, so this stays one block.
PAGES = (
    "amft-3000-hours-california.html",
    "associate-mft-job-advisor.html",
    "grow-your-therapy-practice.html",
    "practice-simulator.html",
    "therapist-cost-of-living-california.html",
    "therapist-tax-strategy-california.html",
    "therapist-working-remotely-california.html",
)

# value, and the ratio it measures against the surface it lands on
BASE = """
/* D - quieter than white, and above the floor. .50 was 4.32, .42 was 3.49 */
.apanel .anote,.tpanel .pr em,.thero .pr em,.pr-num u,
.tpanel .pn,.tpanel .pn b,.apanel .pn,.apanel .pn b{
color:rgba(255,255,255,.62) !important}
/* C - a light card nested in a dark band keeps its own text colour.
   .verdict is light in all three of its variants - good, bad and flat. */
.verdict p,.verdict li{color:#4E4940 !important}     /* 7.94 on #FBEFEC */
/* the indigo band is the one band modifier that is actually dark. Scoped to
   the ledger row, NOT to the band: a bare `.slab.indigo i` also matched an
   italic inside a white table cell sitting in the same band. */
.slab.indigo .rw i{color:#C6DBD1 !important}         /* 8.43 on #123C30 */
"""

# Only for a page that declares the dark plaque itself. See the docstring:
# the same selector is cream on another page, and assuming otherwise made
# that page worse than it started.
PLAQUE = """
/* A - the page's own dark-plaque colours, restored over a house !important */
#plan .finish em{color:#84AC99 !important}           /* 4.86 on #123C30 */
#plan .finish p,#plan .finish i,#plan .finish span{
color:#C6DBD1 !important}                            /* 8.43 on #123C30 */
/* B - the author's dark-mode amber was a light-surface amber */
#plan .finish b,#plan .finish p b{color:#FFE7A3 !important}   /* 10.04 */
"""

# The fact that makes PLAQUE correct, checked rather than assumed.
DARKPLAQUE = re.compile(r"#plan\s+\.finish\s*\{[^}]*background\s*:\s*#123C30",
                        re.I)

STYLE_OPEN = "<style>" + CSS_MARK
STYLE_SHUT = CSS_END + "</style>"


def strip(s):
    s = re.sub(re.escape(MARK) + r"[\s\S]*?" + re.escape(END), "", s)
    s = re.sub(re.escape(STYLE_OPEN) + r"[\s\S]*?" + re.escape(STYLE_SHUT),
               "", s)
    return s


def main(check_only=False):
    bad, done, plaques = [], 0, []
    for page in PAGES:
        p = os.path.join(SITE, page)
        if not os.path.exists(p):
            bad.append("%s does not exist" % page)
            continue
        s = open(p, encoding="utf-8").read()
        out = strip(s)
        h = out.rfind("</head>")
        if h < 0:
            bad.append("%s has no head to put the tool colours in" % page)
            continue
        own = "\n".join(re.findall(r"<style[^>]*>([\s\S]*?)</style>", out))
        css = BASE + (PLAQUE if DARKPLAQUE.search(own) else "")
        if DARKPLAQUE.search(own):
            plaques.append(page)
        if not check_only:
            out = out[:h] + STYLE_OPEN + css + STYLE_SHUT + out[h:]
            if out != s:
                open(p, "w", encoding="utf-8").write(out)
        done += 1

    if not check_only:
        for page in PAGES:
            p = os.path.join(SITE, page)
            if not os.path.exists(p):
                continue
            s = open(p, encoding="utf-8").read()
            if s.count(CSS_MARK) != 1 or s.count(CSS_END) != 1:
                bad.append("%s has %d/%d tool-colour marker(s)"
                           % (page, s.count(CSS_MARK), s.count(CSS_END)))

    if bad:
        for b in bad:
            print("GUARD: %s" % b)
        sys.exit("%d problem(s)" % len(bad))
    print("tool-output colours re-asserted on %d calculator page(s); the "
          "dark-plaque rules on %d of them (%s)."
          % (done, len(plaques), ", ".join(plaques) or "none"))


if __name__ == "__main__":
    main("--check" in sys.argv)
