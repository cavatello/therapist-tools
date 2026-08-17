#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Twenty corner radii become two, and the pills become buttons.

WHY

P8 names one radius rule and one prohibition:

    "No pill buttons; Basecamp's 6px is right for something clicked twenty
     times a session."

The rendered audit found **twenty distinct border-radius values** in use -
2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 20, 22, 30 and
999px - which is not a system, it is twenty separate decisions. Nine of
them differ from a neighbour by a single pixel, which no reader can see and
every future author has to guess at.

So: two values, named, and everything lands on one of them.

    --r   10px   panels, cards, slabs, images, tables - anything with
                 content inside it
    --rs   6px   buttons, links, chips, badges, inputs - anything you click
                 or read as a label

WHICH WAY EACH VALUE GOES

By size, not by guesswork about the element: a small radius is on a small
thing, and a small thing is a chip or a button.

    <= 7px    -> 6px     already a button radius, or near enough
    8 - 30px  -> 10px    the card radius
    999px     -> see below

WHAT DOES **NOT** CHANGE, AND WHY THAT MATTERS MORE THAN WHAT DOES

`999px` is the interesting case, because "no pill buttons" is a rule about
BUTTONS, and a browser probe over all 242 pages found that most of the
site's pill radii are not on buttons at all:

    .ig-bars .track, .ig-bars .fill   progress bars. A bar with square ends
                                      reads as a broken bar. The rounded end
                                      IS the affordance, and P8's rule has
                                      nothing to say about it.
    circles                           a dot, an avatar, a numbered marker -
                                      anything whose box is square. Forcing
                                      6px on those turns a circle into a
                                      rounded square.
    .tsbadge, .who span, .soon,       badges and eyebrows. Nobody clicks a
    .np-col h5, .sitefoot h5,         badge; P8's reasoning ("something
    .dc-row .rm span, .bcrq           clicked twenty times a session") does
                                      not reach them, and a lozenge label
                                      is a different component from a
                                      lozenge button.

What IS a button gets 6px, and the list is short because the probe made it
short - 351 of the site's pill instances turned out to be ONE rule,
`.pk-hero .hj a`, the jump-links in the pagekit hero, on about fifty pages.

This is the same discipline as `palette_conform.py`'s roled group and for
the same reason: **the property is not the design, the job the element does
is the design.** A 999px radius means "pill" on a button, "capsule" on a
badge and "round end" on a progress bar, and one rule cannot serve all
three.

Idempotent: every target is one of the two values, and neither is a key.
Guarded: no value outside the allowed set may survive on an in-scope rule,
and the pill allowlist must still resolve to rules that exist.
"""
import hashlib, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
CSSDIR = os.path.join(SITE, "css")
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training", "for")
# The simulator's look is explicitly protected and the two mockups are
# deliberately other. Same exclusions as flat_bands.py.
SKIP = {"practice-simulator.html", "tycoon.html", "concepts.html"}

R, RS = "10px", "6px"

# The rules whose 999px IS a pill button. Everything else keeps its 999px -
# see WHAT DOES NOT CHANGE.
PILLS = (
    ".pk-hero .hj a",      # pagekit hero jump-links: 351 instances, ~50 pages
    ".dc-hero .hj a",      # the same component on the discipline hub
    ".dc-toc a",           # its table of contents
    ".dc-fb",              # the hub's filter buttons
    ".hmost a",
    ".hgo",
    ".clcta",
    ".rwcta",
    ".hh-chip",            # the topic-hub hero chips - the same component
                           # as .hj a, one level up
    ".np-hub",             # the hub link that closes each footer column
    ".sitenav-cta",        # "Stay updated" in the masthead
    ".sitenav-top",
    ".pill",
)
# A rule whose selector ends with one of these keeps its radius.
KEEPERS = (".ig-bars .track", ".ig-bars .fill", ".tsbadge", ".who span",
           ".soon", ".np-col h5", ".sitefoot h5", ".dc-row .rm span",
           ".bcrq", ".sitenav-links")

RULE = re.compile(r"([^{}]*)\{([^{}]*)\}")
RAD = re.compile(r"(border(?:-[a-z]+)?-radius\s*:\s*)([^;}]+)")
NUM = re.compile(r"(\d+(?:\.\d+)?)px")


def target(px):
    return RS if px <= 7 else R


def selector_is(sel, names):
    flat = " ".join(sel.split())
    return any(flat.endswith(n) or (n + ",") in flat + "," or
               re.search(re.escape(n) + r"(?:[\s,:]|$)", flat) for n in names)


def fix_value(value, sel):
    """Rewrite one border-radius value. Returns (value, changed)."""
    pills = selector_is(sel, PILLS)
    keeper = selector_is(sel, KEEPERS)

    def one(m):
        px = float(m.group(1))
        if px >= 100:
            # a pill radius. Only a button loses it.
            return (RS if (pills and not keeper) else m.group(0))
        # Below 100 the keeper list does NOT apply. It exists to stop a
        # progress bar or a badge losing its CAPSULE, not to exempt them
        # from the two-value system - a badge at 3px on one family and 5px
        # on another is the same twenty-decisions problem in miniature, and
        # the first run of this pass left exactly that behind on
        # `.tsbadge` in four sheets.
        return target(px)
    out = NUM.sub(one, value)
    return out, out != value


def sheet_pass(text):
    n = 0
    out, last = [], 0
    for m in RULE.finditer(text):
        sel, body = m.group(1), m.group(2)
        if "radius" not in body:
            continue

        def rad(rm):
            nonlocal n
            v, ch = fix_value(rm.group(2), sel)
            if ch:
                n += 1
            return rm.group(1) + v
        newbody = RAD.sub(rad, body)
        if newbody != body:
            out.append(text[last:m.start(2)])
            out.append(newbody)
            last = m.end(2)
    out.append(text[last:])
    return "".join(out), n


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return out


def main():
    remap, changed, sheets = {}, 0, 0
    for fn in sorted(os.listdir(CSSDIR)):
        if not fn.endswith(".css"):
            continue
        path = os.path.join(CSSDIR, fn)
        body = open(path, encoding="utf-8").read()
        fixed, n = sheet_pass(body)
        if not n:
            continue
        sheets += 1
        changed += n
        if re.fullmatch(r"[0-9a-f]{12}", fn[:-4]):
            new = hashlib.sha1(fixed.encode("utf-8")).hexdigest()[:12]
            open(os.path.join(CSSDIR, "%s.css" % new), "w",
                 encoding="utf-8").write(fixed)
            remap[fn[:-4]] = new
            print("  css/%s -> %s  (%d radius rule(s))" % (fn[:-4], new, n))
        else:
            open(path, "w", encoding="utf-8").write(fixed)
            print("  css/%-22s in place    (%d radius rule(s))" % (fn, n))

    LINKED = re.compile(r'href="((?:\.\./)*)css/([0-9a-f]{12})\.css"')
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
                fixed, n = sheet_pass(m.group(2))
                inline += n
                return m.group(1) + fixed + m.group(3)
            s = re.sub(r"(<style\b[^>]*>)([\s\S]*?)(</style>)", block, s)
        if s != orig:
            open(p, "w", encoding="utf-8").write(s)
            touched += 1

    print("%d radius rule(s) conformed in %d stylesheet(s), %d in page "
          "markup, %d page(s) rewritten" % (changed, sheets, inline, touched))

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
                           os.path.join(binned, "pre-radius-%s.css" % old))
            except OSError as e:
                print("  could not move css/%s.css (%s)" % (old, e))

    # ------------------------------------------------------------- guards
    bad = 0
    seen = {}
    for fn in sorted(os.listdir(CSSDIR)):
        if not fn.endswith(".css"):
            continue
        b = open(os.path.join(CSSDIR, fn), encoding="utf-8").read()
        _f, n = sheet_pass(b)
        if n:
            print("GUARD css/%s: %d radius rule(s) still conformable"
                  % (fn, n))
            bad += 1
        if re.fullmatch(r"[0-9a-f]{12}", fn[:-4]):
            h = hashlib.sha1(b.encode("utf-8")).hexdigest()[:12]
            if h != fn[:-4]:
                print("GUARD css/%s: not named for its own contents (%s)"
                      % (fn, h))
                bad += 1
        for m in RULE.finditer(b):
            for rm in RAD.finditer(m.group(2)):
                for px in NUM.findall(rm.group(2)):
                    seen.setdefault(float(px), set()).add("css/" + fn)
    # The link-exists guard runs over PUBLISHED pages only, and the
    # distinction is not laziness. `css_dedupe.py` retires a superseded
    # sheet as `_to_delete/orphan-<hash>.css` and repoints the pages that
    # matter; `_dev/chrome_donor.html` and the regenerated scratch under
    # `mock/library/out/` are left naming the retired file, and the CSS
    # chain corrects the built pages downstream anyway. Failing a release
    # over a stale name in a scratch directory helps nobody. A stale name
    # on a real page is a different thing, and that is what this checks.
    for rel in pages():
        s = open(os.path.join(SITE, rel), encoding="utf-8").read()
        for _u, h in LINKED.findall(s):
            if not os.path.exists(os.path.join(CSSDIR, "%s.css" % h)):
                print("GUARD %s: links css/%s.css, which is not there"
                      % (rel, h))
                bad += 1

    allowed = {6.0, 10.0, 999.0, 50.0, 100.0}
    stray = {px: v for px, v in seen.items() if px not in allowed}
    if stray:
        print("  radius values still in stylesheets outside {6,10,999}:")
        for px in sorted(stray):
            print("      %-7s %s" % ("%gpx" % px,
                                     ", ".join(sorted(stray[px]))[:76]))
    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean - %d value(s) in the stylesheets, pills only on the "
          "%d button rule(s), progress bars and badges untouched"
          % (len(seen), len(PILLS)))


if __name__ == "__main__":
    main()
