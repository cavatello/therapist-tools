#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Text coloured for one surface, sitting on the opposite one. Measured.

WHAT THE SWEEP FOUND

`_dev/contrast_pass.py` fixed one defect - the muted label family, all of
it on light surfaces. A second headless sweep over EVERY page, measuring
every text node against its computed background, found a different and
worse one: **31 signatures across 16 pages where the text colour belongs
to the opposite surface from the one it sits on.**

Not "a bit light". Ratios of 1.05, 1.17, 1.21, 1.26, 1.35 and 1.37 -
text very nearly invisible on live pages, including the practice
simulator's own intro paragraph and the whole of the job advisor's
guidance cards. Reported by the site's owner, then reproduced and
enumerated headlessly rather than fixed page by page from screenshots.

THE MECHANISM, WHICH IS THE SAME EVERY TIME

A dark-band rule written as a DESCENDANT selector reaches into a light
card nested inside that band, or the reverse. The clearest case:

    .bc2 .slab p{color:#C6DBD1}      <- correct ON the dark slab

reaches `section.slab.indigo > div.flags > div.flag > p`, and `.flag` has
a LIGHT background. The page's own `.flag p{color:var(--muted)}` loses,
because `.bc2 .slab p` is (0,2,1) and `.flag p` is (0,1,1). Specificity
is decided before order, so load order cannot rescue it.

WHY THIS SHIPS AS AN INLINE BLOCK BEFORE </body>, LIKE contrast_pass

The first version of this pass appended to `css/house-chrome.css` and
fixed only half the findings. The reason is worth writing down, because
it will catch the next person too:

  * `house-chrome.css` is the SECOND stylesheet on every page. Ten to
    sixteen more load after it, so anything written there loses every
    specificity tie.
  * The retired "house skin" is still live. Every page carries `house`
    in its body class and `body.house{...}` redefines the palette -
    `--gold:#FFE7A3`, `--muted:#5F6A64`, `--pine:#2C6350`. Several of
    the findings ARE that palette: #FFE7A3 is a light gold, and used as
    a text colour on white it measures 1.36:1.
  * `house-rest.css` and `house-skin.css` carry
    `body.house .slab.pine :where(p,span,label,...){color:inherit
    !important}`. `:where()` adds no specificity, so that rule is
    (0,2,1) - but the `!important` beats any normal declaration at any
    specificity. That is why `.acta strong` could be fixed and
    `.acta span` could not.

So the rules below are (a) prefixed `body.house` to reach (0,2,x),
(b) marked `!important` to survive the `:where(... ) !important` sweeps,
and (c) injected as the last <style> in the document, after every linked
sheet, so an equal-specificity tie resolves in their favour. All three
are needed; two out of three was measured and did not work.

`!important` is used here for the same reason `_dev/token_floor.py` and
`_dev/chrome_armor.py` use it: this is a measured accessibility floor,
not a style preference, and each selector is narrow and named.

EVERY VALUE HERE IS VERIFIED IN THIS FILE

`main()` computes the WCAG ratio for every (colour, surface) pair below
and exits non-zero if any lands under its floor. Nothing is eyeballed.
Re-run `_dev/_paths.mjs` after any change: the sweep that found these is
the test that proves they are gone.

THE UNDERLYING PROBLEM THIS DOES NOT FIX

The house skin was recorded as retired and is not. Until it is actually
removed, two palettes are live at once and this pass is a floor under
the collision, not a cure for it. See the project doc.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
MARK = "/* _dev/surface_fix.py */"
LEGACY_END = "/* /surface_fix */"
SHEET = os.path.join(SITE, "css", "house-chrome.css")
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training",
           "for")

# Values already in the design system - this pass introduces no new
# colours, it only puts existing ones on the right surfaces.
MINT = "#C6DBD1"     # the established on-dark body colour
WHITE = "#FFFFFF"
INK = "#1B2420"
MUTED = "#635D4E"    # contrast_pass's verified muted, light surfaces only
GOLDINK = "#8A6516"  # the established gold-on-light (stage_shell .gk)
PINE = "#2C6350"
DEEPINK = "#14372C"  # dark enough for the gold button
MUTEDMINT = "#84AC99"  # the muted on-dark kicker, lifted just over 4.5

# (selector, colour, the surface it lands on, floor, why)
FIXES = [
    # --- the root cause: .bc2 .slab p reaching into light cards ---------
    (".bc2 .slab .rule p,.bc2 .slab .flag p,.bc2 .slab .how p,"
     ".bc2 .slab .how .howb p,.bc2 .slab .how .howb li",
     INK, "#F6F8F6", 4.5,
     "light cards nested inside the dark slab - the 1.35:1 case"),
    # ...and its mirror: .howb as a DIRECT child of the slab is on dark
    # and needs the opposite colour. Disambiguated by combinator.
    (".bc2 .slab>.howb li,.bc2 .slab>.howb p",
     MINT, "#123C30", 4.5,
     "the same class sitting directly on the dark slab"),
    (".bc2 .slab .ig-cap",
     MINT, "#123C30", 4.5, "figure caption on the dark slab, was pine"),

    # --- the kicker on the affiliate/product band -----------------------
    # `p.sub{color:#4E4940}` is the page-body sub-heading colour, correct
    # on every light surface it was written for. `.afband` is a DARK band
    # (#123C30) whose `.sub` is a mono kicker and never sets a colour of
    # its own, so the global rule paints it dark-on-dark: **1.37:1, the
    # worst pair on the site.** One class, two surfaces, for the fourth
    # time in this repository.
    #
    # It had been invisible to this sweep for a reason worth recording:
    # the audit walks up the DOM for a `background-color` and a gradient
    # ancestor returns none, so the pair could not be measured until
    # `flat_bands.py` replaced those gradients with flat fills. Flattening
    # did not cause this; it made it MEASURABLE.
    (".afband .sub,.afband p.sub",
     MINT, "#123C30", 4.5,
     "the mono kicker on the affiliate band, was the light-surface grey"),

    # --- "Stay updated", the masthead CTA, on 238 pages ------------------
    # The worst finding of the whole design audit, and the one every sweep
    # had been structurally unable to see. The button itself is correct:
    #
    #   body.house .sitenav-cta{background:var(--pine)!important;
    #                           color:#fff!important}
    #
    # But a second rule paints its CHILDREN:
    #
    #   nav.sitenav.sitenav .sitenav-cta *{color:#1B2420}
    #
    # and the label lives in a `<span class="long">`. `!important` on the
    # anchor does not reach a span - inheritance is not specificity - so
    # the text of the primary call to action on every page of this site
    # rendered as **--ink on --pine, 2.28:1**, near-black on dark green.
    #
    # It survived every previous pass because `_dev/_contrast_audit.mjs`
    # excludes `header, footer, nav` - a scope decision made when the sweep
    # was about article text, never revisited. It took a sweep that walks
    # the chrome too (`_dev/_viewports.mjs`) to find it, at which point it
    # was on 238 pages at every width.
    # The element carrying `.sitenav` is a <div>, not a <nav> - the first
    # version of this fix said `nav.sitenav...` and matched nothing at all,
    # which the browser confirmed by not listing it among the rules that
    # apply. The competing rule triples the class to reach (0,4,0), so this
    # triples it too and `_scope()` adds `body.house` on top.
    (".sitenav.sitenav.sitenav .sitenav-cta *",
     "#FFFFFF", "#2C6350", 4.5,
     "the label inside the masthead CTA, painted by a child rule the "
     "button's own !important could not reach"),

    # --- gold CTA buttons: pine text measured 4.35, just under ----------
    # :not([style*='color']) matters. One .rwcta carries inline
    # `background:#2C6350;color:#fff` - a per-instance pine variant - and
    # an !important rule here overrides an inline NON-important colour,
    # which turned a correct 6.98:1 button into 1.87:1. Measured, not
    # predicted. Any per-instance override on this site is inline, so
    # excluding an inline COLOUR is the general form of the exception -
    # a plain :not([style]) also skipped a .tcta whose inline style is
    # only `margin-top:16px`, leaving it at 4.35:1.
    (".acta:not([style*='color']),.acta:not([style*='color']) strong,"
     ".acta:not([style*='color']) span,.gcta:not([style*='color']),"
     ".gcta:not([style*='color']) strong,.gcta:not([style*='color']) span,"
     ".tcta:not([style*='color']),.tcta:not([style*='color']) strong,"
     ".tcta:not([style*='color']) span,.clgo:not([style*='color']),.rwcta:not([style*='color']),.pr-cta:not([style*='color']),.pr-cta:not([style*='color']) strong,.pr-cta:not([style*='color']) span",
     DEEPINK, "#F6C560", 4.5, "gold call-to-action buttons"),

    # --- ink on a dark band --------------------------------------------
    (".band .bcr a,.band .bcr li,.band .bcr .sep",
     MINT, "#123C30", 4.5, "breadcrumbs on the dark band"),

    # --- on-dark mint on a white card ----------------------------------
    # SCOPED, and the scope is the whole point. .tsshort is on a WHITE
    # card inside section.band on about/contact/newsletter, and on the
    # DARK #123C30 hero (section.scband) on all 66 school pages. An
    # unscoped rule here fixed 3 pages and broke 89 - caught by
    # re-running the sweep, which is why the sweep is the test.
    (".band .pw .tsshort .tsk", MUTED, WHITE, 4.5,
     "the 'In short' label on the white card, light pages only"),
    (".band .pw .tsshort .tsa,.band .pw .tsshort .tsfig", INK, WHITE, 4.5,
     "the 'In short' answer and figure, light pages only"),

    # --- the skin's light gold, used as text on light -------------------
    (".grouplab span", GOLDINK, "#F6F8F6", 4.5,
     "section group labels, gold on white"),
    (".reffold summary span,.reffold>span", GOLDINK, WHITE, 4.5,
     "the reference-fold label"),
    (".lgwrap .bcr li span", GOLDINK, "#F6F8F6", 4.5,
     "the terms/privacy breadcrumb"),
    (".lghero span", GOLDINK, "#F6F8F6", 4.5, "the terms hero label"),
    (".slider .out.empty", GOLDINK, "#F6F8F6", 4.5,
     "the tax slider's empty-state line"),
    (".promise .chg li time", MUTED, "#F6F8F6", 4.5,
     "the change-log dates"),

    # --- pine on pine, and the skin's grey on dark ----------------------
    (".li-card .li-go", WHITE, PINE, 4.5,
     "an outbound link that was pine on pine at 1.05:1"),
    (".ap-hero .hk", MINT, PINE, 4.5, "the associate-pay hero kicker"),
    (".hero .in .lede", MINT, "#123C30", 4.5,
     "the practice simulator's own intro paragraph"),
    (".cc-meta .tag", PINE, "#E6F1EB", 4.5, "the concept-page tags"),

]


def _lin(c):
    c /= 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def lum(h):
    h = h.lstrip("#")
    return (0.2126 * _lin(int(h[0:2], 16)) + 0.7152 * _lin(int(h[2:4], 16))
            + 0.0722 * _lin(int(h[4:6], 16)))


def ratio(fg, bg):
    a, b = lum(fg), lum(bg)
    return (max(a, b) + 0.05) / (min(a, b) + 0.05)


def _scope(sel):
    """Prefix one selector so it outranks the still-live house skin.

    `.bc2` is a class on BODY, not on a wrapper inside it. So the obvious
    "body.house " + sel produces `body.house .bc2 .slab p`, which asks
    for a .bc2 element INSIDE body.house and matches nothing at all. The
    first version of this pass shipped exactly that and silently fixed
    none of the .slab findings. Compound onto the body instead.
    """
    if sel.startswith(".bc2"):
        return "body.house" + sel
    return "body.house " + sel


def block():
    o = ["<style>" + MARK]
    o.append("/* Text coloured for the opposite surface from the one it sits")
    o.append("   on. Each rule names its surface; every pair is verified over")
    o.append("   4.5:1 by _dev/surface_fix.py before it is emitted. Prefixed")
    o.append("   body.house and marked !important to outrank the retired-but-")
    o.append("   still-live house skin, which sweeps spans with")
    o.append("   :where(...){color:inherit!important}. */")
    for sel, col, surface, floor, why in FIXES:
        full = ",".join(_scope(s.strip()) for s in sel.split(","))
        o.append("/* %s - %.2f:1 on %s */" % (why, ratio(col, surface),
                                              surface))
        o.append("%s{color:%s !important}" % (full, col))
    o.append("</style>")
    return "\n".join(o)


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return out


def main():
    bad = 0
    worst = 99.0
    for sel, col, surface, floor, why in FIXES:
        r = ratio(col, surface)
        worst = min(worst, r)
        if r < floor:
            print("GUARD: %s on %s is %.2f:1, under the %.1f floor (%s)"
                  % (col, surface, r, floor, why))
            bad += 1
    if bad:
        sys.exit("%d colour(s) under the floor - nothing written. Darken "
                 "the colour; do not lower the floor." % bad)

    # The first version of this pass wrote into house-chrome.css. That
    # block is inert now (the sheet loads too early to win) - remove it
    # so two copies of these rules cannot drift apart.
    if os.path.exists(SHEET):
        s = open(SHEET, encoding="utf-8").read()
        if MARK in s and LEGACY_END in s:
            s = re.sub(re.escape(MARK) + r"[\s\S]*?"
                       + re.escape(LEGACY_END) + r"\n?", "", s, count=1)
            open(SHEET, "w", encoding="utf-8").write(s)
            print("  removed the inert house-chrome.css copy")

    blk = block()
    n = 0
    for rel in pages():
        p = os.path.join(SITE, rel)
        s = open(p, encoding="utf-8").read()
        orig = s
        s = re.sub(r"\n?<style>" + re.escape(MARK) + r"[\s\S]*?</style>\n?",
                   "", s)
        i = s.lower().rfind("</body>")
        if i < 0:
            continue
        s = s[:i] + blk + "\n" + s[i:]
        if s != orig:
            open(p, "w", encoding="utf-8").write(s)
            n += 1

    # ---------------------------------------------------------- guards
    for rel in pages():
        s = open(os.path.join(SITE, rel), encoding="utf-8").read()
        if s.count(MARK) != 1:
            print("GUARD %s: %d copies of the block" % (rel, s.count(MARK)))
            bad += 1
        # It has to be the LAST style in the document, or the whole
        # mechanism is pointless.
        if s.count(MARK) == 1:
            after = s[s.find(MARK):]
            if "<link rel=\"stylesheet\"" in after:
                print("GUARD %s: a stylesheet link follows the block" % rel)
                bad += 1
    if os.path.exists(SHEET):
        s = open(SHEET, encoding="utf-8").read()
        if MARK in s:
            print("GUARD: the inert house-chrome.css copy is still there")
            bad += 1
    if bad:
        sys.exit("%d guard failure(s)" % bad)
    print("%d rule(s) on %d page(s), every pair over 4.5:1 (worst %.2f)"
          % (len(FIXES), n, worst))


if __name__ == "__main__":
    main()
