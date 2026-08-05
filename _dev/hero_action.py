#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Every tool hero gets one thing to press.

`_dev/hero-budget.mjs` reports `hero offers no action` for
therapist-cost-of-living-california.html, and reading the markup confirms it
rather than blaming the detector: the only <a> elements in that hero are the two
breadcrumb links. A reader arrives, is told what the page is for, is shown three
computed figures - and is given nothing to do. The first control is 1,013px down
at desktop width, past the fold, with no signpost that it exists.

This is rule 4 in claude/hero-design-rules.md: one primary action, at most one
ghost beside it. Here it is one, pointing at section 01, which is where the
reader has to go anyway.

Two details that are easy to get wrong:

* The anchor has to EXIST. The page's sections carry no ids at all, so the pass
  adds `id="where"` to the first `.clsec` as well as the link that targets it.
  A CTA pointing at a missing anchor is worse than no CTA - it looks broken and
  it does nothing.
* The masthead is `position:sticky`, so an in-page jump lands the heading
  underneath it. `scroll-margin-top` on the target fixes that - but it has to be
  MEASURED at both widths, not guessed once. The first attempt used 84px, which
  cleared the desktop masthead (bottom edge 133px) by luck and left the heading
  hidden on a phone, where the capsule wraps to two rows and its bottom edge is
  171px. Values below are measured with the masthead's own bounding box.

* The insertion point has to be the HERO's end, found by balancing <section>
  tags. The first attempt searched for the literal `</div></div></section>`
  after the h1; the hero closes with only one </div>, so that matched a section
  thousands of pixels down the page and the button rendered at y=5039 - present,
  clickable, and nowhere near the hero. Same lesson as hero_notes.py: do not
  anchor on a string that happens to appear near the thing you want.

The class name and styling are `.clgo`, matching the undeployed Option 3 build
exactly, so that when Option 3 finally ships this pass becomes a no-op instead
of a conflict.

Idempotent. Run after breadcrumbs.py, before linkcheck.py.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
MARK = "/* _dev/hero_action.py */"
TAG = "<!-- hero action -->"

CSS = """
/* Matches the Option 3 build's .clgo so the two cannot disagree. Gold on the
   deep indigo band - the site's pine green would be a low-contrast button on
   that background, and this is the one thing in the hero meant to be pressed. */
.clgo{display:inline-flex;align-items:center;min-height:46px;padding:0 20px;
  margin:18px 0 0;border-radius:999px;background:var(--pop);color:#2A2010;
  font-weight:700;font-size:15px;text-decoration:none}
.clgo:hover{background:#FFD57A}
.clgo:focus-visible{outline:2px solid #fff;outline-offset:2px}
/* measured: masthead bottom edge is 133px at 1440 and 171px at 390 */
#where{scroll-margin-top:146px}
@media (max-width:640px){#where{scroll-margin-top:186px}}
"""

# page -> (anchor id, the element to give it to, the CTA html, what to put it after)
ACTIONS = {
    "therapist-cost-of-living-california.html": {
        "anchor": "where",
        "anchor_on": '<section class="clsec">',
        "cta": '<a class="clgo" href="#where">Start with where I live &darr;</a>',
    },
}


def hero_end(s):
    """Offset of `</section>` closing the section that holds the first <h1>."""
    h1 = s.find("<h1")
    if h1 < 0:
        return None
    start = s.rfind("<section", 0, h1)
    if start < 0:
        return None
    depth = 0
    for m in re.finditer(r"<section\b|</section>", s[start:]):
        depth += 1 if m.group(0).startswith("<section") else -1
        if depth == 0:
            return start + m.start()
    return None


def main():
    n = 0
    for slug, spec in sorted(ACTIONS.items()):
        path = os.path.join(SITE, slug)
        if not os.path.exists(path):
            print("%-44s MISSING" % slug)
            continue
        s = open(path, encoding="utf-8").read()

        if TAG in s:
            s = re.sub(r"\n?<style>" + re.escape(MARK) + r".*?/\* end ha \*/</style>\n?",
                       "", s, flags=re.S)
            s = s.replace("</body>", "\n<style>" + MARK + CSS + "/* end ha */</style>\n</body>", 1)
            open(path, "w", encoding="utf-8").write(s)
            print("%-44s already has its action" % slug)
            continue

        # 1. give the target an id
        want = spec["anchor_on"]
        if want not in s:
            print("%-44s anchor host %r not found - skipped" % (slug, want))
            continue
        s = s.replace(want, want[:-1] + ' id="%s">' % spec["anchor"], 1)

        # 2. insert the CTA at the end of the hero, found by balancing sections
        end = hero_end(s)
        if end is None:
            print("%-44s hero not found - skipped" % slug)
            continue
        at = s.rfind("</div>", 0, end)      # inside the hero's own wrapper
        if at < 0:
            print("%-44s no wrapper to close inside - skipped" % slug)
            continue
        s = s[:at] + TAG + spec["cta"] + s[at:]

        s = s.replace("</body>", "\n<style>" + MARK + CSS + "/* end ha */</style>\n</body>", 1)
        open(path, "w", encoding="utf-8").write(s)
        n += 1
        print("%-44s action added, targeting #%s" % (slug, spec["anchor"]))

    bad = 0
    for slug, spec in ACTIONS.items():
        path = os.path.join(SITE, slug)
        if not os.path.exists(path):
            continue
        s = open(path, encoding="utf-8").read()
        if s.count(TAG) != 1:
            print("GUARD %s: %d actions" % (slug, s.count(TAG))); bad += 1
        if s.count(MARK) != 1:
            print("GUARD %s: %d stylesheets" % (slug, s.count(MARK))); bad += 1
        if s.count('id="%s"' % spec["anchor"]) != 1:
            print("GUARD %s: %d #%s anchors" % (
                slug, s.count('id="%s"' % spec["anchor"]), spec["anchor"])); bad += 1
        # the link must resolve to something on this page
        if ('href="#%s"' % spec["anchor"]) not in s:
            print("GUARD %s: CTA href missing" % slug); bad += 1
    if bad:
        sys.exit("hero_action: %d guard failure(s)" % bad)
    print("%d action(s) added" % n)


if __name__ == "__main__":
    main()
