#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ninety-two font sizes become a scale of thirteen.

WHY THIS ONE NEEDED A DECISION FIRST

The radius work had a spec to conform to - P8 names 6px and gives its
reason - so it was cleanup. Type had no such thing. P8 says *"Tokens and
the two type sizes"* and names one number, the 16.5px body metric, and the
rendered audit confirms that metric landing correctly on **240 of 242
pages**. So the body is right. What was never written down is everything
else, and in the absence of a scale the site grew **92 distinct font
sizes** across 2,307 declarations, 42 of them not on a whole or half pixel:
8.6px, 9.2px, 9.4px, 9.6px, 9.8px, 10.2px, 10.4px, 10.6px, 10.8px, 11.2px,
11.4px, 11.6px, 11.7px, 11.8px, and on up.

Nobody chose those. They are what happens when each pass picks a size that
looks right in the block it is writing, and there is no list to pick from.
So this pass is two things: **the list**, and the conformance to it.

THE SCALE, AND WHERE IT COMES FROM

Thirteen steps, anchored on the body metric P8 already fixed and spaced
roughly 1.15x-1.25x apart, which is close enough to a modular scale to feel
even and loose enough to keep the moves small:

     9.5   mono kickers, eyebrows, unit labels
    10.5   small caps labels, table heads
    12     captions, credits, chips
    13.5   dense table text
    15     secondary prose
    16.5   BODY - P8's metric, the anchor
    19     leads and deks
    23     h3
    28     h2
    34     h1 on an article
    42     h1 in a hero
    52     the display figure
    66     the largest stat

The step count is not an aesthetic preference, it is measured. Every
candidate scale was tested against the real distribution:

    12 steps, no 9.5   219 declarations move more than 8%, worst 40%
    13 steps, with 9.5  76 declarations move more than 8%, worst 27%
    12 steps, respaced   76 over 8%, but 513 over 5% instead of 241

The thirteen-step version wins on both counts, and it wins because of one
step: the small end is where the site is densest (688 declarations under
11px), so a scale that is coarse down there moves a lot of text a long way.
A scale is only as good as the distribution it has to absorb.

WHAT MOVES, AND THE ONLY MOVES WORTH ARGUING ABOUT

1,705 declarations change; 602 were already on a step. Of the changes, all
but 76 are under 8%, and most are a fraction of a pixel - 12.4px, 12.5px
and 12.6px all landing on 12px, which no reader can see and which removes
three decisions.

The genuinely visible ones are at the bottom of the range and they are
improvements:

    7.5px -> 9.5px    3 uses.  Seven-and-a-half pixel text is not small,
    8px   -> 9.5px    1 use.   it is unreadable, and `mobile_floor.py`
    8.5px -> 9.5px   46 uses.  already had to override a list of these to
                               12px on phones because they were carrying
                               sentences.

And four at the top, each moving under 11%: 38px and 37px to 34px, 31px to
28px, 21px to 19px.

INTERACTION WITH THE MOBILE FLOOR

`mobile_floor.py` writes `{font-size:12px}` overrides for a named list of
selectors whose text was under 12px AND carrying a sentence rather than a
label. Those are per-selector overrides at 390px, not base declarations, so
this pass and that one do not fight: the base size may be 9.5px on a laptop
and the phone still gets 12px. The two steps below 12px exist for labels,
which is what they were always for.

NOT IN SCOPE

`practice-simulator.html`, `tycoon.html`, `concepts.html` - the protected
tool and the two mockups, same as `flat_bands.py` and `radius_floor.py`.
`clamp()` and `vw` sizes are left alone: a fluid size is a range, not a
step, and forcing a step on it would break the fluidity it exists for.

Idempotent: every target is a step, and a step maps to itself. Guarded: no
in-scope declaration may carry a size off the scale.
"""
import hashlib, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
CSSDIR = os.path.join(SITE, "css")
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training", "for")
SKIP = {"practice-simulator.html", "tycoon.html", "concepts.html"}

SCALE = (9.5, 10.5, 12, 13.5, 15, 16.5, 19, 23, 28, 34, 42, 52, 66)

# A plain px font-size. `clamp(...)`, `calc(...)` and `vw` values do not
# match, on purpose - see NOT IN SCOPE.
SIZE = re.compile(r"(font-size\s*:\s*)(\d+(?:\.\d+)?)px(?![^;}]*[)v])")
LINKED = re.compile(r'href="((?:\.\./)*)css/([0-9a-f]{12})\.css"')


def step(px):
    return min(SCALE, key=lambda s: abs(s - px))


def fmt(px):
    return ("%g" % px) + "px"


def conform(text):
    n = 0

    def one(m):
        nonlocal n
        px = float(m.group(2))
        t = step(px)
        if fmt(t) == m.group(2) + "px":
            return m.group(0)
        n += 1
        return m.group(1) + fmt(t)
    return SIZE.sub(one, text), n


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return out


def main():
    # ------------------------------------------------ the scale is loop-free
    for s in SCALE:
        if step(s) != s:
            sys.exit("%g is not its own nearest step - the scale is not "
                     "idempotent" % s)

    remap, changed, sheets = {}, 0, 0
    for fn in sorted(os.listdir(CSSDIR)):
        if not fn.endswith(".css"):
            continue
        path = os.path.join(CSSDIR, fn)
        body = open(path, encoding="utf-8").read()
        fixed, n = conform(body)
        if not n:
            continue
        sheets += 1
        changed += n
        if re.fullmatch(r"[0-9a-f]{12}", fn[:-4]):
            new = hashlib.sha1(fixed.encode("utf-8")).hexdigest()[:12]
            open(os.path.join(CSSDIR, "%s.css" % new), "w",
                 encoding="utf-8").write(fixed)
            remap[fn[:-4]] = new
            print("  css/%s -> %s  (%d size(s))" % (fn[:-4], new, n))
        else:
            open(path, "w", encoding="utf-8").write(fixed)
            print("  css/%-22s in place    (%d size(s))" % (fn, n))

    allhtml = []
    for root, dirs, files in os.walk(SITE):
        dirs[:] = [d for d in dirs
                   if d not in ("_to_delete", ".git", "node_modules")]
        for f in sorted(files):
            if f.endswith(".html"):
                allhtml.append(os.path.relpath(os.path.join(root, f), SITE))
    inline, touched = 0, 0
    for rel in sorted(allhtml):
        p = os.path.join(SITE, rel)
        s = open(p, encoding="utf-8").read()
        orig = s
        if remap:
            s = LINKED.sub(
                lambda m: 'href="%scss/%s.css"'
                          % (m.group(1), remap.get(m.group(2), m.group(2))), s)
        if os.path.basename(rel) not in SKIP and not rel.startswith("_dev/"):
            def block(m):
                nonlocal inline
                fixed, n = conform(m.group(2))
                inline += n
                return m.group(1) + fixed + m.group(3)
            s = re.sub(r"(<style\b[^>]*>)([\s\S]*?)(</style>)", block, s)

            def attr(m):
                nonlocal inline
                fixed, n = conform(m.group(1))
                inline += n
                return 'style="%s"' % fixed
            s = re.sub(r'style="([^"]*)"', attr, s)
        if s != orig:
            open(p, "w", encoding="utf-8").write(s)
            touched += 1

    print("%d size(s) conformed in %d stylesheet(s), %d in page markup, "
          "%d page(s) rewritten" % (changed, sheets, inline, touched))

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
                           os.path.join(binned, "pre-scale-%s.css" % old))
            except OSError as e:
                print("  could not move css/%s.css (%s)" % (old, e))

    # ------------------------------------------------------------- guards
    bad = 0
    for fn in sorted(os.listdir(CSSDIR)):
        if not fn.endswith(".css"):
            continue
        b = open(os.path.join(CSSDIR, fn), encoding="utf-8").read()
        _f, n = conform(b)
        if n:
            print("GUARD css/%s: %d size(s) still off the scale" % (fn, n))
            bad += 1
        if re.fullmatch(r"[0-9a-f]{12}", fn[:-4]):
            h = hashlib.sha1(b.encode("utf-8")).hexdigest()[:12]
            if h != fn[:-4]:
                print("GUARD css/%s: not named for its own contents (%s)"
                      % (fn, h))
                bad += 1
    # Published pages only, for the same reason as the other conformance
    # passes: a stale name under mock/ is not a reader's problem.
    for rel in pages():
        s = open(os.path.join(SITE, rel), encoding="utf-8").read()
        for _u, h in LINKED.findall(s):
            if not os.path.exists(os.path.join(CSSDIR, "%s.css" % h)):
                print("GUARD %s: links css/%s.css, which is not there"
                      % (rel, h))
                bad += 1
        if os.path.basename(rel) in SKIP:
            continue
        for m in re.finditer(r"<style\b[^>]*>([\s\S]*?)</style>", s):
            _f, n = conform(m.group(1))
            if n:
                print("GUARD %s: %d inline size(s) off the scale" % (rel, n))
                bad += 1
                break
    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean - every in-scope font-size is one of the %d steps"
          % len(SCALE))


if __name__ == "__main__":
    main()
