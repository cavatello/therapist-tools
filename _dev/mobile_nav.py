#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The mobile nav is scrollable and does not look it. Give it an edge.

WHAT IS ACTUALLY WRONG

On a 390px phone the masthead's link row is 338px wide and holds 630px of
buttons. It is already `overflow-x:auto`, so Practice, Training and About are
reachable — you just have to guess they are there. iOS does not paint a
scrollbar until you are mid-drag, so what a reader sees is "Practic" sliced
down the middle and nothing to suggest a swipe would help. Reported, reasonably,
as "seems broke iPhone".

This is the failure mode of every horizontal scroller that ships without an
affordance, and it is invisible to a desktop audit: at 1440px the row fits, so
nothing overflows and nothing is flagged. It only exists at phone widths.

WHY NOT JUST WRAP TO TWO ROWS

That was the first instinct and it is worse here. The masthead is sticky, it
already spends two rows on a phone — wordmark and Updates, then the links — and
a third row of chrome would follow the reader down every page of a long article
to solve a problem that a 12px shadow solves.

THE FIX: SCROLL SHADOWS THAT KNOW WHERE THEY ARE

Four background layers, no JavaScript:

  two `local` layers   scroll WITH the content, painted in the bar's own colour
  two `scroll` layers  stay put, and are soft shadows at the left and right edges

At rest, the local layer sits on top of the shadow and hides it. Scroll right
and the local layer moves away, revealing the left shadow — and the right one
covers itself when you reach the end. So the cue appears exactly when there is
more to see in that direction and disappears when there is not, without a line
of script or a resize listener.

Applied only under 900px, because above that the row fits and a shadow would be
decoration.

Also: `scroll-snap` on the buttons so a swipe lands on a label rather than
halfway through one, and `-webkit-overflow-scrolling:touch` for momentum on
older iOS.

Idempotent, guarded.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training")
MARK = "/* _dev/mobile_nav.py */"

NAVBG = "#FBF9F3"      # .sitenav background, from restyle.css

CSS = """<style>%(mark)s
@media (max-width:900px){
  /* The row scrolls. These four layers make it look like it scrolls, and stop
     looking like it at each end. The two `local` layers travel with the
     content and mask the shadow underneath; the two `scroll` layers stay put.
     No script, no resize listener. */
  .sitenav .sitenav-links{
    overflow-x:auto;
    -webkit-overflow-scrolling:touch;
    scroll-snap-type:x proximity;
    scrollbar-width:none;
    background-image:
      linear-gradient(to right, %(bg)s 42%%, rgba(251,249,243,0)),
      linear-gradient(to left,  %(bg)s 42%%, rgba(251,249,243,0)),
      radial-gradient(farthest-side at 0%% 50%%, rgba(22,33,27,.22), rgba(22,33,27,0)),
      radial-gradient(farthest-side at 100%% 50%%, rgba(22,33,27,.22), rgba(22,33,27,0));
    background-position:left center, right center, left center, right center;
    background-size:34px 100%%, 34px 100%%, 13px 100%%, 13px 100%%;
    background-repeat:no-repeat;
    background-attachment:local, local, scroll, scroll;
  }
  .sitenav .sitenav-links::-webkit-scrollbar{display:none}
  .sitenav .sitenav-links>*{scroll-snap-align:start}
  /* Room for the shadow to sit in without clipping the first and last label. */
  .sitenav .sitenav-links{padding-right:14px}
}
</style>""" % {"mark": MARK, "bg": NAVBG}


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return out


def main():
    n = 0
    for rel in pages():
        p = os.path.join(SITE, rel)
        s = open(p, encoding="utf-8").read()
        if "sitenav-links" not in s:
            continue
        orig = s
        s = re.sub(r"\n?<style>" + re.escape(MARK) + r"[\s\S]*?</style>\n?", "", s)
        i = s.lower().rfind("</body>")
        if i < 0:
            continue
        s = s[:i] + CSS + "\n" + s[i:]
        if s != orig:
            open(p, "w", encoding="utf-8").write(s)
            n += 1
    print("%d page(s) given the mobile nav affordance" % n)

    bad = 0
    for rel in pages():
        s = open(os.path.join(SITE, rel), encoding="utf-8").read()
        if "sitenav-links" in s and s.count(MARK) != 1:
            print("GUARD %s: %d copies" % (rel, s.count(MARK)))
            bad += 1
    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean")


if __name__ == "__main__":
    main()
