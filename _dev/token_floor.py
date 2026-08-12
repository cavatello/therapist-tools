#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Every text colour on the site, measured by photograph, raised to 4.5:1.

HOW THESE WERE FOUND

A full 131-page sweep with `px_audit.mjs`, which does not guess at backgrounds.
The old detector walked up the DOM for a `background-color` and gave up the
moment it met a `background-image` - so a gradient hero returned "unknown" and
was skipped, which is precisely where light-on-light hides. This one collects
candidates cheaply, then for each one sets its text to `transparent`,
screenshots the element's own box, and takes the **modal pixel** as the
background. Not the mean: a mean averages a two-tone band into a colour that
appears nowhere on screen. The mode is a colour a reader actually receives.

337 findings. They collapse to **eleven hex values**, which is the whole point of
writing this as a token pass rather than fifty patches:

    #7C8878   3.24-3.72   67 pages of "On this page", 46 "Orientation" chips,
                          40 candidate counts, 37 "Commons" links, table heads
    #9A8F76   2.96        46 pages of "Why it is worth noticing"
    #8A8477   3.35-3.72   article source discs, table heads
    #7C766A   3.96-4.28   .sitenav-sub and the small italics
    #9A9384   2.83        unit labels ("wks", "hrs")
    #9A9280   2.93        struck-through prices
    #A29A88   2.79        "optional" tags
    #8A8069   ~3.5        the "not approved" badges
    #C98B4B   2.51-2.89   the amber, used as TEXT
    #B08430   2.95-3.39   citation markers and statute references
    #3F9577   3.16-3.64   the green, used as TEXT

The last three are the interesting ones and they are the same case: a colour
that is completely fine as a **rule, a bar, a border or a chip** and fails only
when it is asked to carry letterforms. `rates_contrast.py` established the fix
for `#3F9577` on one page - swap it only where the declaration is a text colour,
and leave every `background`, `border`, `fill`, `stroke` and `box-shadow`
untouched. The same guard runs here, sitewide, for all three.

THE ONES THAT CANNOT BE SWAPPED BLINDLY

`#F6C560` is correct as text on the dark pine bands and catastrophic on white
(1.61:1 on `associate-mft-job-advisor.html`). `#635D4E` is correct on every
light surface and catastrophic on the dark `.pxband` - **1.03:1**, the worst
ratio on the site, and it is there because `_dev/contrast_pass.py` put `.sb` in
its list of 26 tripled classes without noticing that `.sb` appears on both a
white card and a dark green band. A previous fix of mine is the cause. Those
cases get named, context-scoped overrides at the end of this file instead of a
find-and-replace.

WHY IT REHASHES THE STYLESHEETS

Same reason `css_cdo_fix.py` does: a file in `css/` is named for the sha1 of its
contents, and that name is the cache key. Editing the bytes in place leaves a
file whose name no longer describes it. So each repaired sheet is written under
its new hash, every `<link>` is repointed, and the stale file is moved to
`_to_delete/` only once nothing references it - moved, not unlinked, because
this repository is edited through a bridge that cannot delete.

NOT FIXED HERE, ON PURPOSE

`practice-simulator.html`'s gold chapter slab: `.ch-n`, `.dek` and `.small` read
3.38-4.17 as near-black on a gold gradient, made worse by an `opacity:.6` the
detector cannot see. Every available fix is visible - a lighter band, a darker
band with light text, or dropping the fade - and the simulator's look is
explicitly protected. It is reported rather than changed.

Idempotent: the replacements already clear the floor, so a second run finds
nothing. Guarded: it re-measures every replacement against every surface the
sweep actually observed, and refuses to write if one would ship under 4.5.
"""
import os, re, sys, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
CSSDIR = os.path.join(SITE, "css")
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training", "for")
MARK = "/* _dev/token_floor.py */"
FLOOR = 4.5

LINKED = re.compile(r'<link rel="stylesheet" href="((?:\.\./)*)css/([0-9a-f]{12})\.css">')

# Every surface the sweep actually observed one of these colours sitting on.
SURFACES = {
    "white":  "#FFFFFF",
    "cream":  "#FBF9F3",
    "paper":  "#F4F0E6",
    "mint":   "#F2F6EE",
    "sand":   "#FBF6E9",
    "ivory":  "#FFFDF6",
    "oat":    "#F7F3E9",
    "chip":   "#F3EFE4",
}

# old -> new. Text only; see TEXT_ONLY below.
SWAPS = [
    # the green-grey family keeps its hue
    ("#7C8878", "#4A5A46"),
    ("#8A8069", "#635E53"),
    # the warm greys go to the muted the rest of the site already uses
    ("#8A8477", "#635E53"),
    ("#9A8F76", "#635E53"),
    ("#7C766A", "#635E53"),
    ("#9A9384", "#635E53"),
    ("#9A9280", "#635E53"),
    ("#A29A88", "#635E53"),
    # a colour is not a typeface: these three stay on every bar and border
    ("#C98B4B", "#8A6023"),
    ("#B08430", "#8A6023"),
    ("#3F9577", "#2C6350"),
]

# Swapped only where the declaration paints letters. A bar, a rule, a chip or a
# border keeps the colour it was designed with.
# The two greys are NOT in here, deliberately. They are bound to `--mut` and
# friends, and protecting variables (see KEEP) would leave `--mut` at 3.24:1 on
# 67 pages of "On this page". A grey is never load-bearing as a bar the way the
# amber and the green are; where one edges a hairline border, darkening it by
# this much is invisible. The amber and the green stay protected, and the
# handful of classes that consume THEM as text are named in OVERRIDES instead.
TEXT_ONLY = {"#C98B4B", "#B08430", "#3F9577"}
#
# A custom property counts as a surface here, which is the subtle part. `--pop`
# is consumed by `.acta{background:var(--pop)}` AND by four `color:var(--pop)`
# rules on the same page; swapping the declaration repainted the gold CTA band
# dark amber and produced three new failures where there had been one. For a
# colour we only dare swap where we can SEE it painting letters, a variable is
# by definition not such a place.
KEEP = re.compile(
    r"(--[a-z0-9-]+|"
    r"background|background-color|background-image|border|border-color|"
    r"border-top-color|border-left-color|border-right-color|border-bottom-color|"
    r"fill|stroke|box-shadow|outline|outline-color|caret-color|"
    r"text-decoration-color|column-rule)[^;:{}]*:[^;{}]*$", re.I)

# The context-dependent cases, written as scoped rules rather than replacements.
OVERRIDES = """<style>%s
/* .sb is a badge that appears on a white card in the directory and on a dark
   green band on the leaf pages. contrast_pass.py darkened it for the first and
   so destroyed the second: 1.03:1, the worst on the site. The band wins here
   because it is more specific, and the card keeps the darkened grey. */
.pxband .sb.sb.sb{color:rgba(255,255,255,.92)}
.pxband .sb.sb.sb.ok{color:#FFE3B8}
/* Gold on a dark band is right; gold on white is 1.61:1. */
.hint.hint.hint{color:#FFD37A}
/* Pine reads 4.35:1 on the gold chip - just under. The chip already has an ink
   that reads 10.31:1, and every other gold CTA on the site uses it. */
.hwcta.hwcta.hwcta,
.hwcta.hwcta.hwcta *{color:#16211B}
/* The amber and the green stay protected in the token table because they are
   real bar, border and chip colours. These are the classes that consume them
   as TEXT, named one by one so the bars keep the colour they were drawn with:
     .yes    "Varies by payer" verdicts        3.45:1
     .src/.n citation markers and references   3.22:1  */
.yes.yes.yes{color:#2C6350}
.src.src.src,
.n.n.n{color:#8A6023}
/* `.grouplab span` is `color:var(--gold)` - the section standfirsts, 2.74:1 on
   cream. Same reason as above: the variable itself is a background elsewhere,
   so the consumer is named rather than the token swapped. */
.grouplab.grouplab span{color:#8A6023}
/* 4.40:1, ten pixels, on a pale amber pill. Under by a tenth. */
.soon.soon.soon{color:#7A5418}
</style>""" % MARK

# Named rules whose colour must be repaired in the page rather than the token
# table, because the token is correct elsewhere. (page, old, new, why)
NAMED = [
    ("associate-mft-job-advisor.html", "#F6C560", "#8A6023",
     "an inline link reading 1.61:1 - gold text on a white card"),
]
# Gold is a background on that page as well as a text colour, and the first
# version of this pass replaced both - turning the signup band into dark amber
# with dark text on it, three fresh failures where there had been one. A named
# repair goes through the same surface guard as everything else.
NAMED_TEXT_ONLY = True


def _lin(c):
    c /= 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def lum(h):
    h = h.lstrip("#")
    r, g, b = (_lin(int(h[i:i + 2], 16)) for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(a, b):
    x, y = lum(a), lum(b)
    return (max(x, y) + 0.05) / (min(x, y) + 0.05)


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return out


def swap_in(text, table=None, text_only=None):
    """Replace tokens, skipping any occurrence that paints a surface."""
    out, n = text, 0
    if text_only is None:
        text_only = TEXT_ONLY
    for old, new in (table if table is not None else SWAPS):
        pieces, last, hits = [], 0, 0
        for m in re.finditer(re.escape(old), out, re.I):
            a = max(out.rfind(";", 0, m.start()),
                    out.rfind("{", 0, m.start()),
                    out.rfind("}", 0, m.start())) + 1
            decl = out[a:m.start()]
            pieces.append(out[last:m.start()])
            if old.upper() in text_only and KEEP.search(decl):
                pieces.append(m.group(0))
            else:
                pieces.append(new)
                hits += 1
            last = m.end()
        pieces.append(out[last:])
        out = "".join(pieces)
        n += hits
    return out, n


def main():
    # ------------------------------------------------- measure before writing
    print("replacements, against every surface the sweep observed:")
    worst, bad = 99.0, 0
    for old, new in SWAPS:
        lo = min(ratio(new, s) for s in SURFACES.values())
        worst = min(worst, lo)
        print("  %s -> %s   worst %5.2f:1  %s"
              % (old, new, lo, "ok" if lo >= FLOOR else "FAILS"))
        if lo < FLOOR:
            bad += 1
    for label, fg, bg, floor in [
            ("badge on dark band", "#EAEAE8", "#465D3D", FLOOR),
            ("approved badge on band", "#FFE3B8", "#465D3D", FLOOR),
            ("hint on pine", "#FFD37A", "#3B6248", FLOOR),
            ("hwcta ink on gold", "#16211B", "#F6C560", FLOOR),
            ("job-advisor link on white", "#8A6023", "#FFFFFF", FLOOR),
            ("group standfirst on cream", "#8A6023", "#FBF9F3", FLOOR),
            ("'In progress' on its pill", "#7A5418", "#FBEFD5", FLOOR)]:
        r = ratio(fg, bg)
        print("  %-26s %5.2f:1  %s" % (label, r, "ok" if r >= floor else "FAILS"))
        if r < floor:
            bad += 1
    if bad:
        sys.exit("%d replacement(s) would ship under %.1f:1" % (bad, FLOOR))

    # ------------------------------------------------------ the stylesheets
    remap, swapped = {}, 0
    for fn in sorted(os.listdir(CSSDIR)):
        if not fn.endswith(".css"):
            continue
        path = os.path.join(CSSDIR, fn)
        body = open(path, encoding="utf-8").read()
        fixed, n = swap_in(body)
        if not n or fixed == body:
            continue
        new = hashlib.sha1(fixed.encode("utf-8")).hexdigest()[:12]
        open(os.path.join(CSSDIR, "%s.css" % new), "w", encoding="utf-8").write(fixed)
        remap[fn[:-4]] = new
        swapped += n
        print("  css/%s -> %s  (%d colour(s))" % (fn[:-4], new, n))

    # ------------------------------------- the pages: inline styles and links
    touched = 0
    for rel in pages():
        p = os.path.join(SITE, rel)
        s = open(p, encoding="utf-8").read()
        orig = s

        # repoint any stylesheet we rehashed
        if remap:
            s = LINKED.sub(
                lambda m: '<link rel="stylesheet" href="%scss/%s.css">'
                          % (m.group(1), remap.get(m.group(2), m.group(2))), s)

        # inline <style> blocks that were never hoisted
        def one(m):
            fixed, _n = swap_in(m.group(2))
            return m.group(1) + fixed + m.group(3)
        s = re.sub(r"(<style\b[^>]*>)([\s\S]*?)(</style>)", one, s)

        # style="..." attributes. 26 occurrences sitewide, and they are invisible
        # to a pass that only looks at stylesheets - which is how the Headway
        # affiliate note kept its 3.53:1 grey through the first run of this.
        def attr(m):
            fixed, _n = swap_in(m.group(1))
            return 'style="%s"' % fixed
        s = re.sub(r'style="([^"]*)"', attr, s)

        for page, old, new, _why in NAMED:
            if rel == page:
                s, _n = swap_in(s, table=[(old, new)], text_only={old.upper()})

        # the scoped overrides, last
        s = re.sub(r"\n?<style>" + re.escape(MARK) + r"[\s\S]*?</style>\n?", "", s)
        if "sitenav" in s:
            i = s.lower().rfind("</body>")
            if i > 0:
                s = s[:i] + OVERRIDES + "\n" + s[i:]

        if s != orig:
            open(p, "w", encoding="utf-8").write(s)
            touched += 1
    print("\n%d colour(s) swapped in css/, %d page(s) rewritten" % (swapped, touched))

    # ------------------------------------------------- retire stale sheets
    if remap:
        live = set()
        for rel in pages():
            live |= set(h for _u, h in LINKED.findall(
                open(os.path.join(SITE, rel), encoding="utf-8").read()))
        binned = os.path.join(SITE, "_to_delete")
        for old in remap:
            if old in live:
                continue
            os.makedirs(binned, exist_ok=True)
            try:
                os.replace(os.path.join(CSSDIR, "%s.css" % old),
                           os.path.join(binned, "pre-floor-%s.css" % old))
            except OSError as e:
                print("  could not move css/%s.css (%s) - unreferenced, so it is "
                      "dead weight rather than a fault" % (old, e))

    # ------------------------------------------------------------- guards
    bad = 0
    for fn in sorted(os.listdir(CSSDIR)):
        if not fn.endswith(".css"):
            continue
        b = open(os.path.join(CSSDIR, fn), encoding="utf-8").read()
        h = hashlib.sha1(b.encode("utf-8")).hexdigest()[:12]
        if h != fn[:-4]:
            print("GUARD css/%s: name does not match its contents (%s)" % (fn, h))
            bad += 1
        again, n = swap_in(b)
        if n:
            print("GUARD css/%s: %d colour(s) still swappable" % (fn, n))
            bad += 1
    for rel in pages():
        s = open(os.path.join(SITE, rel), encoding="utf-8").read()
        for m in re.finditer(r'style="([^"]*)"', s):
            _f, n = swap_in(m.group(1))
            if n:
                print("GUARD %s: inline style still carries %r"
                      % (rel, m.group(1)[:60]))
                bad += 1
        for page, old, _new, _why in NAMED:
            if rel == page:
                _f, n = swap_in(s, table=[(old, "#000000")],
                                text_only={old.upper()})
                if n:
                    print("GUARD %s: %s still paints text" % (rel, old))
                    bad += 1
        for _u, h in LINKED.findall(s):
            if not os.path.exists(os.path.join(CSSDIR, "%s.css" % h)):
                print("GUARD %s: links css/%s.css which is not there" % (rel, h))
                bad += 1
        if "sitenav" in s and s.count(MARK) != 1:
            print("GUARD %s: %d override block(s)" % (rel, s.count(MARK)))
            bad += 1
    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean")
    print("\nreported, not changed: practice-simulator.html's gold chapter slab "
          "(.ch-n/.dek/.small, 3.38-4.17:1). Every fix is a visible change to a "
          "page whose design is protected.")


if __name__ == "__main__":
    main()
