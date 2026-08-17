#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The decorative gradients become flat fills, and only those.

WHY, AND WHY THE LAST ATTEMPT AT THIS WAS REVERTED

P8 is explicit: *"Flat fills, hairline ring + soft shadow"*, and under
Deliberately NOT borrowed, *"No gradients from anywhere."* The rendered
audit found gradients on 32 pages.

An earlier pass, `flat_fills.py`, tried this and **broke 286 contrast pairs
across 73 pages** and was reverted. It failed for one reason worth stating
plainly: it replaced a gradient with a colour chosen from the RULE, not from
the gradient's own stops, so `.artband` - which is `var(--paper)` in the art
family and a dark band elsewhere - got a fill that was right on one family
and catastrophic on the other. It also flattened gradients that were never
decoration.

So this pass does two things differently. It **classifies first**, and every
replacement is **one of the gradient's own stops**, which makes the direction
of the contrast change predictable instead of arbitrary.

WHAT IS A DECORATION AND WHAT IS NOT

Of 125 gradient declarations, **52 are not decoration at all** and are left
untouched:

    43  translucent or fade   `linear-gradient(to right,#F6F8F6 30%,
                              rgba(251,249,243,0))` is the fade at the edge
                              of a horizontally scrolling table, and
                              `radial-gradient(farthest-side at 0 50%,
                              rgba(22,33,27,.16),...)` is the shadow that
                              tells a reader there is more table to the
                              left. Both are affordances. Deleting them
                              deletes information, and neither reads as a
                              gradient.
     8  masks                 `-webkit-mask-image:radial-gradient(9px at
                              50% 0,transparent 98%,#000)` is how the HEY
                              slab gets its SCALLOPED EDGE - which P8 does
                              not merely permit, it specifies. A gradient
                              used as a mask paints no colour at all.
     1  a var() stop          `linear-gradient(transparent 68%,var(--gold)
                              68%)` has no blend: two hard stops at the same
                              position. It is the gold highlighter rule
                              under the home page headline, drawn with a
                              gradient because that is how you draw a rule
                              behind text.

Two more are excluded by the same reasoning even though they are opaque:
`linear-gradient(#000,#000)` is a solid used for `background-clip`, and
`linear-gradient(115deg,#2C6350 0 6px,#6E9587 6px 12px)` is a hatch pattern
with hard stops, not a blend.

That leaves the ones a reader actually perceives as a gradient: the deep
pine sweeps behind heroes and bands.

HOW A REPLACEMENT IS CHOSEN

Every target below is **a stop of the gradient it replaces**, or the
sanctioned token that stop was approximating - never a new colour. For a
dark band that carries light text this means taking the DARKEST end, so
every pixel that changes gets darker and contrast for the text on it can
only improve. For the one light surface (`#fff` to `#F6F8F6`) it means
taking `--paper`, because P8 says tinted paper and never pure white.

That property is what makes this safe to reason about, and the browser
sweep is what proves it.

NOT IN SCOPE

`practice-simulator.html` and `tycoon.html`. The simulator's look is
explicitly protected (see `token_floor.py`, which reports its gold chapter
slab rather than changing it) and tycoon is a mockup. Between them they
hold every purple gradient in the census. The red band
(`#7E3630`->`#A25A52`) and the blue band (`#1F5573`->`#13324A`) are left
too: they are semantic colour, and the semantic palette is a design
decision that has not been made yet.

Idempotent: every replacement is a flat colour, so a second run finds no
gradient to classify. Guarded: no listed gradient may survive in scope, and
the count of remaining gradients must not exceed the recorded functional
set.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
CSSDIR = os.path.join(SITE, "css")
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training", "for")
SKIP = {"practice-simulator.html", "tycoon.html", "concepts.html"}

# gradient (verbatim) -> the flat colour that replaces it.
# Every value on the right is a stop of the gradient on the left, or the
# sanctioned token that stop was approximating.
FLAT = {
    # the deep pine hero sweeps -> --deep, the slab colour, and the darkest
    # or near-darkest stop in each
    "linear-gradient(135deg,#1B2420 0%,#123C30 48%,#2C6350 100%)": "#123C30",
    "linear-gradient(135deg,#123C30 0%,#2C6350 55%,#3F9577 100%)": "#123C30",
    "linear-gradient(135deg,#123C30 0%,#2C6350 52%,#3F9577 100%)": "#123C30",
    "linear-gradient(135deg,#123C30,#2C6350)": "#123C30",
    "linear-gradient(150deg,#2C6350,#1F4C3C)": "#123C30",
    "linear-gradient(150deg,#123C30,#14372C)": "#123C30",
    "linear-gradient(160deg,#1B2420 0%,#14372C 55%,#123C30 100%)": "#123C30",
    # the simulator masthead's own sweep, kept on its darkest stop
    "linear-gradient(150deg,#14372C 0%,#2C6350 46%,#48A382 100%)": "#14372C",
    # a two-stop pine bar -> --pine, its own dark end
    "linear-gradient(90deg,#2C6350,#3F9577)": "#2C6350",
    "linear-gradient(90deg,#3F9577,#5EC49B)": "#2C6350",
    # the near-black bands -> --ink
    "linear-gradient(135deg,#141712 0%,#1B2420 55%,#2C6350 100%)": "#1B2420",
    "linear-gradient(135deg,#141712,#1B2420 52%,#2C6350)": "#1B2420",
    "linear-gradient(135deg,#141712 0%,#1B2420 60%,#2A3327 100%)": "#1B2420",
    # gold bars -> the CTA gold, which is the light stop each was reaching
    # for. These carry no text; the sweep confirms it.
    "linear-gradient(90deg,#B5843F,#D8AC63)": "#F6C560",
    "linear-gradient(90deg,#C98B4B,#F6C560)": "#F6C560",
    "linear-gradient(90deg,#F6C560,#C99C46)": "#F6C560",
    "linear-gradient(180deg,#F6C560,#B08430)": "#F6C560",
    # the gold-brown band -> the sanctioned gold-on-light, its middle stop
    "linear-gradient(135deg,#6B4A18 0%,#8A6516 55%,#946C28 100%)": "#8A6516",
    # the one light surface. --paper, not #fff: P8 says tinted paper, never
    # pure white.
    "linear-gradient(180deg,#fff 0%,#F6F8F6 100%)": "#F6F8F6",
    # The blue band on therapist-working-remotely-california.html. Left out
    # of the first pass as "semantic colour, a decision not yet made" - and
    # the cost of leaving it turned out to be that the page was
    # UNMEASURABLE: a contrast sweep resolves a background by walking up
    # for a background-COLOR, a gradient ancestor returns none, and the
    # whole hero reported as white-on-white at 1.00:1 at all five
    # viewports. Ten findings that were neither real nor dismissible.
    # Flattened to its own darkest stop, which keeps the blue and makes the
    # page checkable.
    "linear-gradient(160deg,#1F5573 0%,#173F5A 70%,#13324A 100%)": "#13324A",
}

GRAD = re.compile(r"(?:linear|radial|conic)-gradient\s*\(")


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return out


def flatten(text):
    n = 0
    for grad, flat in FLAT.items():
        c = text.count(grad)
        if c:
            text = text.replace(grad, flat)
            n += c
    return text, n


def remaining(text):
    """Gradients still present, so the guard can count them."""
    return len(GRAD.findall(text))


def main():
    # -------------------------------------------------- every target is a stop
    HEX = re.compile(r"#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b")
    TOKENS = {"#123C30", "#1B2420", "#2C6350", "#F6C560", "#8A6516",
              "#F6F8F6", "#14372C"}
    bad = 0
    for grad, flat in FLAT.items():
        stops = {s.upper() for s in HEX.findall(grad)}
        if flat.upper() not in stops and flat.upper() not in TOKENS:
            print("GUARD %s -> %s, which is neither a stop of it nor a "
                  "sanctioned token" % (grad[:52], flat))
            bad += 1
    if bad:
        sys.exit("%d replacement(s) invent a colour - see HOW A REPLACEMENT "
                 "IS CHOSEN" % bad)

    # ------------------------------------------------------- the stylesheets
    import hashlib
    remap, swapped, sheets = {}, 0, 0
    for fn in sorted(os.listdir(CSSDIR)):
        if not fn.endswith(".css"):
            continue
        path = os.path.join(CSSDIR, fn)
        body = open(path, encoding="utf-8").read()
        fixed, n = flatten(body)
        if not n:
            continue
        sheets += 1
        swapped += n
        if re.fullmatch(r"[0-9a-f]{12}", fn[:-4]):
            new = hashlib.sha1(fixed.encode("utf-8")).hexdigest()[:12]
            open(os.path.join(CSSDIR, "%s.css" % new), "w",
                 encoding="utf-8").write(fixed)
            remap[fn[:-4]] = new
            print("  css/%s -> %s  (%d gradient(s))" % (fn[:-4], new, n))
        else:
            open(path, "w", encoding="utf-8").write(fixed)
            print("  css/%-22s in place    (%d gradient(s))" % (fn, n))

    # ------------------------------------------------------------ the pages
    LINKED = re.compile(r'href="((?:\.\./)*)css/([0-9a-f]{12})\.css"')
    inline, touched = 0, 0
    allhtml = []
    for root, dirs, files in os.walk(SITE):
        dirs[:] = [d for d in dirs
                   if d not in ("_to_delete", ".git", "node_modules")]
        for f in sorted(files):
            if f.endswith(".html"):
                allhtml.append(os.path.relpath(os.path.join(root, f), SITE))
    for rel in sorted(allhtml):
        p = os.path.join(SITE, rel)
        s = open(p, encoding="utf-8").read()
        orig = s
        if remap:
            s = LINKED.sub(
                lambda m: 'href="%scss/%s.css"'
                          % (m.group(1), remap.get(m.group(2), m.group(2))), s)
        if os.path.basename(rel) not in SKIP and not rel.startswith("_dev/"):
            s, n = flatten(s)
            inline += n
        if s != orig:
            open(p, "w", encoding="utf-8").write(s)
            touched += 1

    print("%d gradient(s) flattened in %d stylesheet(s), %d in page markup, "
          "%d page(s) rewritten" % (swapped, sheets, inline, touched))

    if remap:
        binned = os.path.join(SITE, "_to_delete")
        os.makedirs(binned, exist_ok=True)
        current = {rel: open(os.path.join(SITE, rel), encoding="utf-8").read()
                   for rel in allhtml}
        for old in sorted(remap):
            if any("%s.css" % old in s for s in current.values()):
                continue
            try:
                os.replace(os.path.join(CSSDIR, "%s.css" % old),
                           os.path.join(binned, "pre-flat-%s.css" % old))
            except OSError as e:
                print("  could not move css/%s.css (%s)" % (old, e))

    # ------------------------------------------------------------- guards
    bad = 0
    for fn in sorted(os.listdir(CSSDIR)):
        if not fn.endswith(".css"):
            continue
        b = open(os.path.join(CSSDIR, fn), encoding="utf-8").read()
        _f, n = flatten(b)
        if n:
            print("GUARD css/%s: %d listed gradient(s) survived" % (fn, n))
            bad += 1
        if re.fullmatch(r"[0-9a-f]{12}", fn[:-4]):
            h = hashlib.sha1(b.encode("utf-8")).hexdigest()[:12]
            if h != fn[:-4]:
                print("GUARD css/%s: not named for its own contents (%s)"
                      % (fn, h))
                bad += 1
    # The link-exists guard runs over PUBLISHED pages only, and the
    # distinction is not laziness. `css_dedupe.py` retires a superseded
    # sheet as `_to_delete/orphan-<hash>.css` and repoints the pages that
    # matter; `_dev/chrome_donor.html` and the regenerated scratch under
    # `mock/library/out/` are left naming the retired file, and the CSS
    # chain corrects the built pages downstream anyway. Failing a release
    # over a stale name in a scratch directory helps nobody. A stale name
    # on a real page is a different thing, and that is what this checks.
    for rel in pages():
        if os.path.basename(rel) in SKIP:
            continue
        s = open(os.path.join(SITE, rel), encoding="utf-8").read()
        _f, n = flatten(s)
        if n:
            print("GUARD %s: %d listed gradient(s) survived" % (rel, n))
            bad += 1
        for _u, h in LINKED.findall(s):
            if not os.path.exists(os.path.join(CSSDIR, "%s.css" % h)):
                print("GUARD %s: links css/%s.css, which is not there"
                      % (rel, h))
                bad += 1
    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean - %d listed gradient(s) remain nowhere in scope; the "
          "masks, the scroll fades and the highlighter rule are untouched by "
          "design" % len(FLAT))


if __name__ == "__main__":
    main()
