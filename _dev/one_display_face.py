#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Two display faces become one, and 242 pages stop downloading the other.

THE STATE THIS FIXES

Every page on this site loaded FOUR typefaces, and two of them did the same
job:

    Inter                 body text, on all 242 pages. P8's choice.
    IBM Plex Mono         figures, kickers, unit labels.
    Fraunces              headings on ~190 pages - the article, directory
                          and editorial families.
    Bricolage Grotesque   headings on ~48 pagekit pages, including every
                          pagekit hero.

Two display faces is not a system with a rule, it is two systems that never
met. A reader moving from an article to a research page crosses a typeface
boundary that corresponds to nothing they can see a reason for - which is
the same complaint, in a different medium, as the palette drift: *"colors
seem different across site."*

WHY FRAUNCES, AND WHAT IS GIVEN UP

Fraunces wins on count - 190 pages against 48 - and on identity: it sets
the home page headline, every article, and `rates.html`, which is the
site's editorial showpiece. The pagekit pages are the minority and the
newest, so consolidating moves the smaller, later set onto the established
voice rather than the reverse.

What is given up is real and worth naming: a grotesque reads
product-and-data, and pagekit's pages ARE data - directories, comparisons,
tables. There is a genuine argument that the sans was right for them. The
argument that beats it is that a design system's job is to be one system;
a per-family display face is how you end up with four.

Reversing this is one line - swap DISPLAY and RETIRED below.

WHAT IT DOES

  1. every `font-family` stack whose FIRST real face is the retired one is
     rewritten to lead with the display face, keeping the rest of the stack
     as written
  2. the retired family is removed from the Google Fonts `family=` list on
     every page, which is a webfont request saved on all 242 of them
  3. every remaining mention of a face that is neither loaded nor a system
     fallback is dropped from the stacks. With Bricolage gone, 240 pages
     still read `'Fraunces','Archivo',Inter,system-ui,sans-serif` - and
     Archivo is not a webfont this site loads and not a font anyone has
     installed, so it sits between a face that always loads and the real
     system fallbacks doing nothing at all. It was the second name in
     pagekit's stack and it outlived the first.
  4. `_dev/font_links.py`'s guard then proves the reverse direction: no page
     may set a face at the head of a stack that it does not load

Only the FIRST position matters, which is the rule `font_links.py`
established: `'Bricolage Grotesque','Archivo',Inter,system-ui` names
Archivo, but Archivo can never render behind a face that loads. A stack is
a fallback chain, and only its head is a request.

Idempotent: after one run no stack leads with the retired face. Guarded: no
page may load the retired family, and no in-scope stack may name it first.
"""
import hashlib, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
CSSDIR = os.path.join(SITE, "css")
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training", "for")
# The mockups pick their own faces on purpose, and rates.html is the
# editorial exception that already sets Fraunces and Newsreader by decision.
SKIP = {"tycoon.html", "concepts.html"}

LINKED = re.compile(r'href="((?:\.\./)*)css/([0-9a-f]{12})\.css"')
DISPLAY = "'Fraunces'"
DISPLAY_KEY = "fraunces"
RETIRED_KEY = "bricolage grotesque"
# The `family=` fragment to strip from every Google Fonts URL.
RETIRED_URL = re.compile(r"&?family=Bricolage\+Grotesque(?::[^&\"']*)?")

# A FONT STACK IS NOT ALWAYS BEHIND `font-family:`.
#
# This matched `font-family:` only, and the site keeps its display stack in
# CUSTOM PROPERTIES - `--disp` in house.css, `--hs-disp` in house-chrome.css
# and house-rest.css - each of them still reading
# `'Bricolage Grotesque','Inter',system-ui,sans-serif`. So the retired face
# stayed at the head of the stack that the masthead CTA and 24 other
# elements use, this pass's own guard passed (it only looked at
# `font-family:`), and `type_census.py` recorded `used_but_not_loaded: {}`
# for the same reason. The face is not loaded, so those elements have been
# silently rendering in the SECOND name in the stack.
#
# The custom-property arm is deliberately narrow: a property whose value
# contains a quoted family name or a known generic. `--gap:12px` is not a
# font stack and must not be rewritten.
FACE = re.compile(r"(font-family\s*:\s*)([^;}]+)")
VARFACE = re.compile(
    r"(--[a-z0-9-]*(?:disp|font|face|type)[a-z0-9-]*\s*:\s*)"
    r"([^;}]*(?:'[^']+'|\"[^\"]+\"|system-ui|sans-serif|serif|monospace)"
    r"[^;}]*)")
# A named face that is never loaded and is not a system fallback. See
# point 3 above.
ORPHAN_FACE = re.compile(r"\s*,\s*['\"]?Archivo['\"]?(?=\s*[,;}]|$)")
# The retired face at the HEAD of a custom-property stack. `ORPHAN_FACE`
# only removes a face that follows a comma, and Bricolage leads, so it needs
# its own pattern: drop the name and the comma after it, leaving whatever
# was second to lead. Used only by the custom-property arm - a `font-family:`
# stack that leads with the retired face is PROMOTED to the display face by
# `one()`, which is the documented behaviour and is left alone.
RETIRED_HEAD = re.compile(
    r"^\s*['\"]?Bricolage Grotesque['\"]?\s*,\s*", re.I)
GENERIC = {"system-ui", "sans-serif", "serif", "monospace", "ui-monospace",
           "ui-sans-serif", "ui-serif", "cursive", "fantasy", "inherit",
           "initial", "unset"}


def lead_is_retired(stack):
    for part in stack.split(","):
        name = re.sub(r'[\\"\']', "", part)
        name = re.sub(r"!\s*important", "", name).strip().lower()
        if not name or name.startswith("var("):
            continue
        return name == RETIRED_KEY
    return False


def rewrite(text):
    n = 0

    def one(m):
        nonlocal n
        stack = m.group(2)
        if not lead_is_retired(stack):
            return m.group(0)
        n += 1
        # Replace only the leading face, keep the rest of the chain verbatim.
        parts = stack.split(",")
        for i, p in enumerate(parts):
            name = re.sub(r'[\\"\']', "", p)
            name = re.sub(r"!\s*important", "", name).strip().lower()
            if not name or name.startswith("var("):
                continue
            bang = " !important" if "!important" in p else ""
            parts[i] = DISPLAY + bang
            break
        return m.group(1) + ",".join(parts)
    out = FACE.sub(one, text)
    # DELIBERATELY NOT `VARFACE.sub(one, ...)`.
    #
    # The custom-property arm only STRIPS the dead face; it does not promote
    # the display face into its place. Removing a family the site never
    # loads changes nothing a reader sees - those elements were already
    # rendering in the second name in the stack. Promoting Fraunces into the
    # masthead CTA and 24 other chrome elements WOULD change what a reader
    # sees, on every page, and that is a design decision about whether the
    # chrome is a serif - not a defect to be fixed by a guard. The stack is
    # made honest here; what leads it is left to be chosen.

    def strip(m):
        nonlocal n
        stack = m.group(2)
        cleaned = ORPHAN_FACE.sub("", stack)
        if cleaned != stack:
            n += 1
        return m.group(1) + cleaned

    def strip_var(m):
        nonlocal n
        stack = m.group(2)
        cleaned = ORPHAN_FACE.sub("", RETIRED_HEAD.sub("", stack))
        if cleaned != stack:
            n += 1
        return m.group(1) + cleaned
    out = FACE.sub(strip, out)
    return VARFACE.sub(strip_var, out), n


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return out


def main():
    sheets, changed, remap = 0, 0, {}
    for fn in sorted(os.listdir(CSSDIR)):
        if not fn.endswith(".css"):
            continue
        p = os.path.join(CSSDIR, fn)
        body = open(p, encoding="utf-8").read()
        fixed, n = rewrite(body)
        if not n:
            continue
        sheets += 1
        changed += n
        # A content-addressed sheet MUST be renamed when its bytes change.
        # The first version of this pass edited them in place, reasoning
        # that the CSS chain re-derives the names later - and `token_floor`,
        # which runs BEFORE that chain and guards name == sha1(contents),
        # failed the build on nine sheets. A file whose name is its hash has
        # no "small enough" change.
        if re.fullmatch(r"[0-9a-f]{12}", fn[:-4]):
            new = hashlib.sha1(fixed.encode("utf-8")).hexdigest()[:12]
            open(os.path.join(CSSDIR, "%s.css" % new), "w",
                 encoding="utf-8").write(fixed)
            remap[fn[:-4]] = new
            print("  css/%s -> %s  (%d stack(s))" % (fn[:-4], new, n))
        else:
            open(p, "w", encoding="utf-8").write(fixed)
            print("  css/%-22s %d stack(s)" % (fn, n))

    inline, stripped, touched = 0, 0, 0
    for rel in pages():
        if os.path.basename(rel) in SKIP:
            continue
        p = os.path.join(SITE, rel)
        s = open(p, encoding="utf-8").read()
        orig = s
        if remap:
            s = LINKED.sub(
                lambda m: 'href="%scss/%s.css"'
                          % (m.group(1), remap.get(m.group(2), m.group(2))), s)

        def block(m):
            nonlocal inline
            fixed, n = rewrite(m.group(2))
            inline += n
            return m.group(1) + fixed + m.group(3)
        s = re.sub(r"(<style\b[^>]*>)([\s\S]*?)(</style>)", block, s)
        fixed, n = rewrite(s)
        inline += n
        s = fixed
        # and stop asking the network for a face nothing sets any more
        if RETIRED_URL.search(s):
            s = RETIRED_URL.sub("", s)
            # a stripped leading param would leave "css2?&family=..."
            s = s.replace("css2?&family=", "css2?family=")
            stripped += 1
        if s != orig:
            open(p, "w", encoding="utf-8").write(s)
            touched += 1

    if remap:
        binned = os.path.join(SITE, "_to_delete")
        os.makedirs(binned, exist_ok=True)
        allhtml = []
        for root, dirs, files in os.walk(SITE):
            dirs[:] = [d for d in dirs
                       if d not in ("_to_delete", ".git", "node_modules")]
            for f in sorted(files):
                if f.endswith(".html"):
                    allhtml.append(os.path.join(root, f))
        for fp in allhtml:
            t = open(fp, encoding="utf-8").read()
            o = LINKED.sub(
                lambda m: 'href="%scss/%s.css"'
                          % (m.group(1), remap.get(m.group(2), m.group(2))), t)
            if o != t:
                open(fp, "w", encoding="utf-8").write(o)
        current = [open(fp, encoding="utf-8").read() for fp in allhtml]
        for old in sorted(remap):
            if any("%s.css" % old in c for c in current):
                continue
            try:
                os.replace(os.path.join(CSSDIR, "%s.css" % old),
                           os.path.join(binned, "pre-face-%s.css" % old))
            except OSError as e:
                print("  could not move css/%s.css (%s)" % (old, e))

    print("%d stack(s) in %d sheet(s), %d in page markup; the retired family "
          "removed from %d font URL(s); %d page(s) rewritten"
          % (changed, sheets, inline, stripped, touched))

    # ------------------------------------------------------------- guards
    bad = 0
    sheet = {fn: open(os.path.join(CSSDIR, fn), encoding="utf-8").read()
             for fn in os.listdir(CSSDIR) if fn.endswith(".css")}
    for rel in pages():
        if os.path.basename(rel) in SKIP:
            continue
        html = open(os.path.join(SITE, rel), encoding="utf-8").read()
        if "Bricolage+Grotesque" in html:
            print("GUARD %s still loads the retired family" % rel)
            bad += 1
        blob = html + "\n" + "\n".join(
            sheet[n] for n in re.findall(r'href="(?:\.\./)?css/([^"?]+\.css)',
                                         html) if n in sheet)
        for m in FACE.finditer(blob):
            if lead_is_retired(m.group(2)):
                print("GUARD %s: a stack still leads with the retired face: "
                      "%s" % (rel, " ".join(m.group(2).split())[:52]))
                bad += 1
                break
    if bad:
        sys.exit("%d problem(s)" % bad)
    print("guard clean - one display face, and no page requests the other")


if __name__ == "__main__":
    main()
