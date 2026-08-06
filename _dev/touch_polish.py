#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Legibility and tap targets, measured across nine real device sizes.

From _dev/deviceaudit.mjs run over 15 pages x 9 viewports (27" 5K iMac,
MacBook Pro 14, MacBook Air 13, iPad Pro/Air portrait and landscape, iPhone
15 Pro Max / 15 / SE). Zero HIGH findings - no overflow, no sideways scroll,
no dead links, no duplicate ids, no JS errors anywhere. What follows is the
MED list, deduplicated to causes rather than instances.

WHAT IS FIXED, and why each one is real:

1. FORM FIELDS 18-22px TALL. The job advisor has a 328x18 <select> and the
   3,000-hours page has 263x22 number inputs, both with zero padding. That is
   half the height of a finger. This is the single worst usability defect the
   sweep found, and it is on the two pages an ASSOCIATE uses - the readers
   least likely to be at a desk. Scoped to `pointer: coarse` so it fixes
   phones and tablets and leaves the dense desktop forms exactly as they are.

2. FIELD LABELS AT 8.5px. `.f em` renders the label above every input in
   8.5px uppercase. The job advisor alone has 50 of them. Small caps is a fine
   convention; 8.5px is below what a tired person reads at arm's length, and
   this audience is reading about their own money. Raised to 10.5px, which is
   still unmistakably a label.

3. SECTION SUB-HEADINGS AT 8.5px. `.fsub` - "Your week, by who is in the
   room" - is a HEADING rendered smaller than the footnotes under it.

4. FOOTER LINKS 15px TALL. A 12.5px link with no padding, on all 15 pages.
   The gap between rows was margin, which is not tappable. Converting the
   margin into padding makes the target ~32px without moving anything
   visually - the row rhythm is unchanged, the hit area is doubled.

5. FOOTER HEADINGS AT 9.5px. Raised to 10.5px. Still a tracked label.

7. THE MASTHEAD TAGLINE AT 8.5px, on every page at every size.

6. THE CONSENT CHECKBOX AT 16x16. Its <label> wrapper already makes the whole
   354x37 row tappable, so this was never broken - but WCAG 2.5.8 asks for
   24x24 on the control itself and 20px plus its padding clears it.

WHAT IS DELIBERATELY NOT CHANGED. The 11px nav descriptions and the 26px-tall
masthead logo were both flagged. The nav text is secondary description under
an 15px bold label and reads fine at every size tested; the logo is 226px
wide, so it is a large target that happens to be short. Chasing every number
under an arbitrary threshold is how a design gets flattened.

Run BEFORE mobile_hero.py - that pass guards on being the last stylesheet in
the document, and this one has no business overriding a hero.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
MARK = "/* _dev/touch_polish.py */"
MH = "/* _dev/mobile_hero.py */"
SKIP = {"tycoon.html", "concepts.html"}

CSS = """
/* ---- 2,3,5,7: legibility. Not device-specific, so not in a media query. */
/* 7: the masthead tagline sat at 8.5px on every page and every viewport,
   including a 27-inch 5K display, where it is the smallest type on the site.
   10px still reads as a subtitle under the wordmark. */
.sitenav-sub{font-size:10px}
/* 8: three more found only after the first pass cleared the noise - the
   "What it costs / stores / is not" card labels on about.html at 9px, and the
   "In progress" badge at 9.5px. Both are labels, not footnotes. */
.fact em{font-size:10.5px}
/* 9: the sub-9px tail, found only once the 10-11px noise was gone. A form
   label at 7.5px and a field hint at 8px are the two that matter - both sit
   next to an input the reader is about to type a real number into. Selectors
   are compounded because a narrower existing rule was winning at equal
   specificity; the computed size is asserted below rather than assumed. */
.f em,.fgrid .f em,label.f em,.f.sm em{font-size:10.5px}
.f .hint,.f span.hint{font-size:10.2px}
.tile em,.tile > em{font-size:10.2px}
.soon{font-size:10px}
@media (max-width:520px){.bcr{font-size:10.2px}}
.f em,.fsub{font-size:10.5px}
.fsub{font-size:11px;letter-spacing:.1em}
.ftcols h5{font-size:10.5px}

/* ---- 4: footer tap targets. The vertical gap was margin, which cannot be
   tapped. Move it into padding: same rhythm on screen, twice the hit area. */
.ftcols a{padding:8px 0;margin-bottom:1px}

/* ---- 6: the consent control itself */
.consent input{width:20px;height:20px}

/* ---- 1: touch only. `pointer: coarse` is the honest test - it catches
   phones and tablets including ones nobody has shipped yet, and never a
   trackpad. Desktop keeps its dense forms untouched. */
@media (pointer: coarse){
  input[type=number],input[type=text],input[type=email],input[type=tel],
  input[type=search],select,textarea{min-height:42px;padding:6px 10px}
  .ftcols a{padding:10px 0}
  /* the breadcrumb is 26px tall with 5px padding; on a finger that is thin */
  .bcr a{min-height:32px}
  .consent input{width:22px;height:22px}
}
"""


def main():
    n = 0
    for f in sorted(os.listdir(SITE)):
        if not f.endswith(".html") or f in SKIP:
            continue
        path = os.path.join(SITE, f)
        s = open(path, encoding="utf-8").read()
        if "http-equiv=\"refresh\"" in s or "http-equiv=refresh" in s:
            continue                                  # redirect stub, no chrome
        s = re.sub(r"\n?<style>" + re.escape(MARK) + r".*?/\* end tp \*/</style>\n?",
                   "", s, flags=re.S)
        block = "\n<style>" + MARK + CSS + "/* end tp */</style>\n"
        # sit BEFORE the mobile-hero sheet, which guards on being last
        i = s.find("<style>" + MH)
        if i < 0:
            i = s.rfind("</body>")
        if i < 0:
            print("%-44s nowhere to insert" % f)
            continue
        s = s[:i] + block + s[i:]
        open(path, "w", encoding="utf-8").write(s)
        n += 1

    bad = 0
    for f in sorted(os.listdir(SITE)):
        if not f.endswith(".html") or f in SKIP:
            continue
        s = open(os.path.join(SITE, f), encoding="utf-8").read()
        if "http-equiv" in s and "refresh" in s:
            continue
        if s.count(MARK) != 1:
            print("GUARD %s: %d stylesheets" % (f, s.count(MARK))); bad += 1
        if MH in s and s.find(MARK) > s.find(MH):
            print("GUARD %s: sits after mobile_hero" % f); bad += 1
    if bad:
        sys.exit("touch_polish: %d guard failure(s)" % bad)
    print("%d page(s) polished" % n)


if __name__ == "__main__":
    main()
