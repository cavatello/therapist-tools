#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The mark was never removed. It was hidden, and nobody wrote down why.

WHAT WAS ASKED

"I thought we selected new logo and was being applied on site? Does not look
like it's working."

It is not working, and the reason is one line of CSS.

WHAT IS ACTUALLY TRUE

The mark is in the markup of every page, as
`<img class="sitenav-fig" src="data:image/svg+xml,...">` inside the masthead
link. It loads - 150x150 natural. `house-chrome.css` sizes it at 28px, and
26px below 860px. Then two later rules turn it off:

    house-chrome.css   body.house .sitenav-fig { display:none }
    house-rest.css     body.bcz  .sitenav-fig { display:none }

Every page carries `body.house`, so the mark has been hidden on all 239 of
them while shipping in the HTML the whole time - and it is still the favicon,
which is why it shows in a browser tab and nowhere else.

WHY THIS PASS RESTORES IT RATHER THAN LEAVING IT

Because the decision on record is the opposite of what is live.
`claude/brand-art-assets.md` records, as a user decision:

    Header treatment: A - the figure in the header, wordmark beside it
    Lead mark: approach 01 ... the 32px sibling is what actually ships in the
    nav (rendered at 28px)

The masthead was then rebuilt in August as a light bar on the principle "type
is the graphic" (`claude/handoff-2026-08-07.md`), and the figure was hidden as
part of that. **That principle was a design position taken during the rebuild.
The decision to have a figure in the header was the site owner's.** A recorded
owner decision outranks an unrecorded one made while refactoring, so this puts
it back.

If the light-bar-without-a-mark is later preferred, delete this pass - it adds
nothing else, and the two `display:none` rules it overrides are still there.

WHAT IT COSTS

Nothing in layout. The mark sits inside `.sitenav-mark`, beside the wordmark,
in the grid area that already exists for it. Measured across widths, the
masthead height does not change and no page gains overflow.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training", "for")

CSS_MARK = "/* _dev/masthead_mark.py */"
CSS_END = "/* /_dev/masthead_mark.py */"
STYLE_OPEN = "<style>" + CSS_MARK
STYLE_SHUT = CSS_END + "</style>"

# Two rules hide it, on two different body classes, so this has to outrank
# both. `body.house.house` beats `body.house`; `body.bcz.bcz` beats `body.bcz`.
CSS = """
body.house.house .sitenav-fig,body.bcz.bcz .sitenav-fig,
body.house.house.bcz .sitenav-fig{display:block !important;
width:28px !important;height:28px !important;flex:0 0 auto !important}
@media (max-width:860px){body.house.house .sitenav-fig,
body.bcz.bcz .sitenav-fig,body.house.house.bcz .sitenav-fig{
width:26px !important;height:26px !important}}
"""


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f)
                    for f in sorted(os.listdir(p)) if f.endswith(".html")]
    return out


def strip(s):
    return re.sub(re.escape(STYLE_OPEN) + r"[\s\S]*?" + re.escape(STYLE_SHUT),
                  "", s)


def main(check_only=False):
    bad, done, none = [], 0, 0
    for page in pages():
        p = os.path.join(SITE, page)
        s = open(p, encoding="utf-8").read()
        out = strip(s)
        if "sitenav-fig" not in out:
            none += 1
            if out != s and not check_only:
                open(p, "w", encoding="utf-8").write(out)
            continue
        h = out.rfind("</head>")
        if h < 0:
            bad.append("%s has no head to put the mark rule in" % page)
            continue
        if not check_only:
            out = out[:h] + STYLE_OPEN + CSS + STYLE_SHUT + out[h:]
            if out != s:
                open(p, "w", encoding="utf-8").write(out)
        done += 1

    if not check_only:
        for page in pages():
            s = open(os.path.join(SITE, page), encoding="utf-8").read()
            if "sitenav-fig" not in s:
                continue
            if s.count(CSS_MARK) != 1 or s.count(CSS_END) != 1:
                bad.append("%s has %d/%d mark marker(s)"
                           % (page, s.count(CSS_MARK), s.count(CSS_END)))

    if bad:
        for b in bad:
            print("GUARD: %s" % b)
        sys.exit("%d problem(s)" % len(bad))
    print("the masthead mark is visible again on %d page(s); %d page(s) carry "
          "no mark in the markup." % (done, none))


if __name__ == "__main__":
    main("--check" in sys.argv)
