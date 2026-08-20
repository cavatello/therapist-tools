#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mobile_floor.py's decisions, re-asserted where nothing can drop them.

THE FOURTH TIME

`mobile_last.py`'s docstring names three occasions when a pass did its work,
passed its own guard on the file it had just written, and had the result
removed downstream. It then fixed ONE HALF of the fourth: the form-control
sizes. It says so in as many words - "its `overflow-wrap:anywhere` reaches
240 of 242 pages... This re-asserts the part that does not."

The part it re-asserted was the checkbox. The other two halves of
`mobile_floor.py` - the 12px floor on text that carries a sentence, and the
24px hit area on controls that are not inline prose - went the same way and
were not re-asserted. Measured, not inferred:

    _dev/mobile_floor.py reaches 2 of 242 pages       (reach_baseline.json)
    css/c7da96049445.css holds its rules              (grep)
    8,786 nodes of sub-12px sentence text at 390px    (Playwright, 239 pages)
    1,281 pointer targets under 24px at 390px         (Playwright)

`pass_reach.py --check` is green on this, correctly and uselessly: the
baseline was written after the loss, so 2 IS the recorded reality and the
guard is against further change. A baseline records what is; it does not
know what ought to be.

Two of the five families - `family_rest.py` and `family_tool.py` - ported the
hit-area rule into `house-rest.css` and `house-tool.css`, which is why the
findings cluster on art, pagekit and /for/ pages rather than falling evenly.
That partial port is also why a spot check of one page can say "fine".

WHAT THIS ADDS THAT mobile_floor DID NOT

  the same rules, inline, last          no sheet to hoist, so no sheet to drop
  the hit area at EVERY width           WCAG 2.5.8 is a pointer criterion, not
                                        a phone criterion. mobile_floor gates
                                        the whole block at max-width:640px, so
                                        above 640px the site has no hit-area
                                        floor at all - which is where most of
                                        the findings sit: 221x19, 81x12, 88x13
                                        on [tablet-p,tablet-l,laptop,desktop]
                                        and not on phone.
  prose links addressed structurally    `main a{padding-block:7px}` catches
                                        card links too, and a card link is
                                        block-level: it would grow 14px and
                                        move the grid. Targeting links inside
                                        p/li/td/... instead reaches every link
                                        whose height is set by its own line and
                                        no link whose height is set by a box.

WHY PADDING AND NOT min-height ON THE INLINE ONES

Vertical padding on an inline box does not affect the line box. It grows the
hit rectangle and moves nothing. `min-height` on the same elements would push
every line of every article apart to fix a touch target. mobile_floor says
this too and it is worth keeping in front of the next reader.

The one thing that would have made padding unsafe is an underline drawn as
`border-bottom`, which padding detaches from the text. Checked before writing:
every link measured computes `border-bottom: 0px none` and
`text-decoration: none`. The site draws no underline to detach.

THE LISTS ARE IMPORTED, NOT COPIED

`TINY` and `TAPS` are read from `mobile_floor` at run time. A curated list
copied into a second file is a note-to-self that becomes a fact the moment
the two drift, and this repository has already lost a day to one.

Idempotent: the block carries a marker and is replaced, not appended.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import mobile_floor as mf

SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training", "for")
MARK = "/* _dev/mobile_reassert.py */"
# The mockups. `practice-simulator.html`'s look is protected by decision;
# the other two are visual-direction sketches, not pages a reader is sent to.
SKIP = {"tycoon.html", "concepts.html", "practice-simulator.html"}

# Standalone controls. mobile_floor's TAPS, plus the four the sweep found
# after it was written: the provenance badge (21px), the source-catalogue
# link (12px), the "everything for this stage" link and the /for/ door.
EXTRA_TAPS = ["a.tsbadge", "a.srcl", "a.ga", "a.perma"]

# Two classes that carry a sentence and postdate mobile_floor's list. Its own
# list is left exactly as its author reasoned it - "labels, chips and units are
# absent on purpose" - and these are neither:
#   .vwho  an attribution: "GradReports, Alliant - Marriage and Family..."
#   .hk    a kicker that runs on: "Bay Area organization profile - what it..."
# Everything else still under 12px at 390px IS a label: "In short", "Last
# checked", "5 courses", "On this page". Those are a house device and raising
# them would flatten the page's texture to fix nothing.
EXTRA_TINY = [(".vwho", 10.5), (".hk", 10.5)]

# Elements whose children are text in a line, so a link inside one is inline
# and vertical padding is free. A card link is not in this list, which is the
# whole point of the list.
PROSE = ("p", "li", "dd", "dt", "td", "th", "blockquote", "figcaption",
         "cite", "sup", "small", "i", "b", "em", "strong", "span")

# A NOTE ON THE COMMENTS BELOW
#
# They say DIV rather than writing the tag with its angle brackets, and that
# is not style. `payroll_ops.py` guards its page by counting `<div` against
# `</div>` in the raw HTML, and this pass's CSS ships INSIDE that page - so a
# comment mentioning the tag the ordinary way read as an unclosed element and
# failed the build on the first full run. Sixth entry in this repository's
# list of conventions that turned out to be load-bearing.

CSS = """<style>%(mark)s
/* Global responsive resilience. This block is deliberately last in every
   public document so all page families receive the same floor. */
html{max-width:100%%;overflow-x:hidden;-webkit-text-size-adjust:100%%}
body{min-width:0;max-width:100%%;overflow-x:clip}
img,video,canvas{max-width:100%%;height:auto}
main,section,article,header,footer,nav,
main>*,section>*,article>*,.in,.wrap,.libwrap,.artwrap,.pk-wrap{
  min-width:0}
:where(h1,h2,h3,h4,p,li,dd,dt,blockquote,figcaption){overflow-wrap:anywhere}
:where(input,select,textarea,button){max-width:100%%}
:where(a,button,input,select,textarea,summary):focus-visible{
  outline:3px solid #B0730B!important;outline-offset:3px!important}
.sitenav-top,.sitenav-cta,.sitenav-mark{min-height:44px!important}
.sitenav-top{display:inline-flex!important;align-items:center;justify-content:center}
.navpanel a{min-height:44px}
.tbl,.tw,.pk-tw,.dc-tw,.li-tw,.octw,.srn-w,.tblw{
  max-width:100%%;overflow-x:auto;-webkit-overflow-scrolling:touch}
@media (max-width:900px){
  .sitenav{position:relative}
  .sitenav-links{max-width:100%%!important}
  .ui .strip{grid-template-columns:1fr}
  .ui .strip div{border-left:0;border-top:1px solid var(--hair,#DFE4E0)}
  .ui .strip div:first-child{border-top:0}
}
@media (max-width:640px){
  .band,.sec,.libband,.artband,.pk-hero{max-width:100%%}
  .pull{font-size:clamp(21px,7vw,28px)}
}
@media (prefers-reduced-motion:reduce){
  *,*::before,*::after{scroll-behavior:auto!important;
    animation-duration:.01ms!important;animation-iteration-count:1!important;
    transition-duration:.01ms!important}
}
/* WCAG 2.5.8 asks for 24x24 from any pointer, not from a touch pointer, so
   none of this sits behind a width query. See this pass's docstring. */
%(taps)s{min-height:44px;display:inline-flex;align-items:center;
  padding-block:4px}
summary{min-height:44px;display:flex;align-items:center}
/* `mobile_last.py` gives checkboxes and radios their 24x24 inside
   `@media (max-width:900px)`, because it was written to fix a phone. The
   consent box therefore computes 20x20 on a laptop and a desktop - 228 pages,
   found by the five-viewport sweep, which is the whole argument for measuring
   at more than one width. 2.5.8 does not care what kind of pointer it is. */
input[type="checkbox"],input[type="radio"],
.consent input,.consent input[type="checkbox"]{
  min-width:24px;min-height:24px;width:24px;height:24px}
select,button[type="submit"]{min-height:44px}
.consent{min-height:44px;align-items:center!important}
.toc a{min-height:44px;display:flex;align-items:center}
/* Vertical padding on an inline box grows the hit rectangle and moves
   nothing. Only links inside text elements - a card link is block-level and
   would grow its grid row by 14px. */
%(prose)s{padding-block:6px}
/* The breadcrumb sits outside <main>, which is why `main a` never reached it
   and it measured 115x12 on 23 pages at every one of the five widths. */
.bcr li a{padding-block:6px}
/* Three links that are the only child of a bare, classless DIV and so are
   reached by neither list above: the stage index ("All 28 for this stage"), the in-article
   tool link, and the source-list numerals. Named rather than generalised to
   `div > a`, which would catch every card link and grow its grid row. */
.ss1 a,.arttool > a{padding-block:6px}
/* A source numeral is 8px WIDE - the one target that is short in the other
   direction too, and the reason this is inline-block: min-width does nothing
   to an inline box. Scoped to the sources block so no prose list changes. */
.srcs li > a{display:inline-block;min-width:24px;padding-inline:3px}
/* The last four, each on one page, each found only because the sweep runs at
   five widths: the change-log entries, the comparison cards, the /for/ ask
   block. Named, because a rule general enough to catch `li > div > a` would
   also catch a card link. */
.chglog li > div > a,.alts .alt > a,.ask > a{padding-block:7px}
/* Two targets that are short across, not down: the A-Z index letter (16px)
   and the section permalink (7px). `min-height` alone never touches either.
   `mobile_floor.py` has this rule at 640px and below; 2.5.8 is not a phone
   criterion, so it belongs outside the query. */
.az a,a.perma{min-width:24px;min-height:24px;display:inline-flex;
  align-items:center;justify-content:center}
/* A footnote marker is 18x12: it is the one target that is short in BOTH
   directions, so it needs the inline padding as well. */
sup a{padding-inline:4px}
@media (max-width:640px){
  /* A 12px floor for text that CARRIES A SENTENCE. The 9.5 and 10.5 steps
     stay where they are on labels and eyebrows - those are a house device,
     not an accident. This is mobile_floor's own curated list, imported.
     Quadrupled because `.sec .nlmeta` is (0,2,0) and was winning. */
%(tiny)s
}
</style>
"""

EXISTING = re.compile(r"\n?<style>" + re.escape(MARK) + r"[\s\S]*?</style>\n?")


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return out


def build_css():
    taps = ",\n  ".join(mf.TAPS + EXTRA_TAPS)
    prose = ",\n  ".join("%s > a" % t for t in PROSE)
    tiny = "\n".join("  %s{font-size:12px}" % mf.triple(sel)
                     for sel, _w in mf.TINY + EXTRA_TINY)
    return CSS % {"mark": MARK, "taps": taps, "prose": prose, "tiny": tiny}


def main():
    print("re-asserting %d hit-area selector(s) at every width and %d "
          "sentence class(es) at 640px"
          % (len(mf.TAPS) + len(EXTRA_TAPS), len(mf.TINY) + len(EXTRA_TINY)))
    css = build_css()
    n = 0
    for rel in pages():
        if os.path.basename(rel) in SKIP:
            continue
        p = os.path.join(SITE, rel)
        s = open(p, encoding="utf-8").read()
        orig = s
        s = EXISTING.sub("\n", s)
        i = s.lower().rfind("</body>")
        if i < 0:
            print("  SKIP %s has no </body>" % rel)
            continue
        s = s[:i] + css + s[i:]
        if s != orig:
            open(p, "w", encoding="utf-8").write(s)
            n += 1
    print("%d page(s) written" % n)

    bad = 0
    for rel in pages():
        s = open(os.path.join(SITE, rel), encoding="utf-8").read()
        want = 0 if os.path.basename(rel) in SKIP else 1
        if s.count(MARK) != want:
            print("GUARD %s carries the block %d time(s), wanted %d"
                  % (rel, s.count(MARK), want))
            bad += 1
        if want and 'rel="stylesheet"' in s[s.rfind(MARK):]:
            print("GUARD %s: a stylesheet is linked after the block" % rel)
            bad += 1
    if bad:
        sys.exit("%d problem(s)" % bad)
    print("guard clean - the block is last on every published page")


if __name__ == "__main__":
    main()
