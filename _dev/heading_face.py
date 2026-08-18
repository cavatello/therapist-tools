#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""1,209 headings on 91 pages render in the body face.

WHAT WAS REPORTED

"Tyopgrapohy and text still wrong, not using the 37signals basecamp design."

WHAT IS TRUE

Measured in a browser across all 247 pages, every `h1`/`h2`/`h3` that
actually renders:

    Fraunces        2744
    Inter           1209      <- the BODY face, on 91 pages
    IBM Plex Mono    186      (labels, correct)
    Rubik              3      (tycoon.html, a mockup, by design)

Roughly a third of the headings on the site are set in the face the body
text uses. That is not a typeface anyone chose; it is a fall-through.

HOW IT HAPPENED, PRECISELY

`one_display_face.py` retired Bricolage Grotesque onto Fraunces. It has two
arms, and they disagree:

  * the `font-family:` arm PROMOTES - a stack that led with Bricolage is
    rewritten to lead with `'Fraunces'`
  * the custom-property arm STRIPS - `RETIRED_HEAD` removes the dead name
    and, in its own words, leaves "whatever was second to lead"

The display tokens read

    --disp:'Bricolage Grotesque','Inter',system-ui,sans-serif
    --hs-disp:'Bricolage Grotesque','Inter',system-ui,sans-serif

and the second name is **Inter**. So stripping the head promoted the body
face into the display token. Both tokens now read `'Inter',system-ui,
sans-serif`, and `body.bcz h1,h2,h3,h4{font-family:var(--hs-disp)}` hands
that to every heading on those pages.

WHY THIS DOES NOT JUST CHANGE THE TOKEN

Because the pass author's reasoning for leaving it alone is right, and was
written down: `--hs-disp` is also what the masthead CTA and two dozen other
chrome elements use, and "promoting Fraunces into the masthead CTA WOULD
change what a reader sees, on every page, and that is a design decision
about whether the chrome is a serif - not a defect to be fixed by a guard."

That is correct about chrome. What it could not have known is that page
HEADINGS ride the same token, so "leave it to be chosen" quietly chose the
body face for a third of the site's headings.

So this pass names the display face for headings only, and does not touch
`--hs-disp`. Chrome keeps whatever the token says; the decision about the
masthead stays open, exactly where it was left.

WHAT IT DOES NOT TOUCH

Nothing more specific than `body <class> h1..h4`. The 186 IBM Plex Mono
headings are labels set by component rules carrying at least two classes -
`body.bcp .pk-src h3` and its kin - which outrank this and continue to win.
That is verified by re-measuring after the pass: the mono count must not
move.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training", "for")

# The mockups choose their own faces on purpose, and rates.html is the
# editorial exception that sets Fraunces and Newsreader by decision.
SKIP = {"tycoon.html", "concepts.html", "rates.html"}

MARK = "/* _dev/heading_face.py */"
END = "/* /_dev/heading_face.py */"
OPEN = "<style>" + MARK
SHUT = END + "</style>"

DISPLAY = "'Fraunces',Inter,system-ui,sans-serif"
# A page that does not LOAD the face must not name it at the head of a
# stack - that is `font_links.py`'s standing rule, and naming a face a page
# cannot fetch just moves the fall-through one step later. `tools.html` is a
# meta-refresh redirect stub with no webfont link at all.
LOADS = re.compile(r"family=Fraunces")

# One selector per body class the house uses, so the rule sits at the same
# specificity as the `body.bcz h1,h2,h3,h4` rule it is correcting and wins
# on order, while every component rule with a second class still outranks it.
CSS = "\n".join(
    "body.%s h1,body.%s h2,body.%s h3,body.%s h4{font-family:%s}"
    % (b, b, b, b, DISPLAY)
    for b in ("bcz", "bc2", "bct", "bcp", "bca", "house")) + "\n"


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return out


def strip(t):
    return re.sub(re.escape(OPEN) + r"[\s\S]*?" + re.escape(SHUT), "", t)


def main():
    check = "--check" in sys.argv
    block = OPEN + CSS + SHUT
    done, bad, skipped = 0, [], []
    for rel in pages():
        if os.path.basename(rel) in SKIP:
            continue
        p = os.path.join(SITE, rel)
        with open(p, encoding="utf-8") as fh:
            t = fh.read()
        if not LOADS.search(t):
            skipped.append(rel)
            if not check:
                new = strip(t)
                if new != t:
                    with open(p, "w", encoding="utf-8") as fh:
                        fh.write(new)
            continue
        if check:
            if OPEN not in t:
                bad.append("%s does not name a display face for its headings" % rel)
            else:
                done += 1
            continue
        new = strip(t)
        i = new.rfind("</head>")
        if i < 0:
            bad.append("%s has no </head>" % rel)
            continue
        new = new[:i] + block + new[i:]
        done += 1
        if new != t:
            with open(p, "w", encoding="utf-8") as fh:
                fh.write(new)

    if check:
        if bad:
            print("  heading_face.py: %d page(s) with no display face named "
                  "for headings" % len(bad))
            for b in bad[:6]:
                print("    " + b)
            return 1
        print("  guards clean - headings name the display face on %d page(s)"
              "%s" % (done, ", and %d that do not load it were left alone"
                      % len(skipped) if skipped else ""))
        return 0
    print("  %d page(s): headings name the display face rather than "
          "inheriting the body one%s" % (done,
          ", %d skipped for not loading it" % len(skipped) if skipped else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
