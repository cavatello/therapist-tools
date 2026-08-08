#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hide the calculator output containers until they have something in them.

Every tool page carries a set of divs that JavaScript fills once you have
entered a rate and a caseload — #recap, #planout, #blocks, #corpout, #remoteout,
#funnel, #cmp and so on. Before that they are empty, and several of them carry a
border and a background, so a reader arriving at a tool sees empty bordered
boxes with nothing in them. On a phone, where one box fills most of the screen,
that reads as a page that failed to load rather than a page waiting for input.

This is a real consequence of the deliberate decision that every numeric input
on this site starts blank rather than pre-filled with an example. That decision
is right — an illustrative number a reader mistakes for their own is worse than
no number — but it means the empty state is the FIRST state, and it was never
designed.

:empty DOES THE WORK, AND UNDOES IT

`:empty` matches an element with no children, and browsers now treat
whitespace-only content as empty too. The moment the script writes into a
container the selector stops matching and the box appears, with no script, no
class toggling and nothing to keep in sync. The rule cannot get out of step with
the behaviour because it IS the behaviour.

Scoped to the known ids rather than `div:empty`, because a blanket rule would
also collapse spacers and grid cells that are empty on purpose.

Idempotent, guarded.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
MARK = "/* _dev/empty_outputs.py */"

# The JS-filled containers, per page. Read off the tool pages, not guessed.
IDS = ["recap", "sell", "planout", "blocks", "corpout", "remoteout",
       "promo", "growpromo", "panel-rows", "worthout", "funnel", "needout",
       "capout", "apanel", "take", "hour", "cmp", "plan", "rows"]

CSS = ("<style>%s\n"
       "/* Empty until the script fills them. :empty stops matching the moment\n"
       "   it does, so the box appears on its own - no class toggling to keep in\n"
       "   sync with the behaviour. */\n"
       "%s{display:none}\n"
       "</style>" % (MARK, ",".join("#%s:empty" % i for i in IDS)))


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    return out


def main():
    n = 0
    for rel in pages():
        p = os.path.join(SITE, rel)
        s = open(p, encoding="utf-8").read()
        if not any(('id="%s"' % i) in s for i in IDS):
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
    print("%d tool page(s) given the empty-state rule" % n)

    bad = 0
    for rel in pages():
        s = open(os.path.join(SITE, rel), encoding="utf-8").read()
        if any(('id="%s"' % i) in s for i in IDS) and s.count(MARK) != 1:
            print("GUARD %s: %d copies" % (rel, s.count(MARK)))
            bad += 1
    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean")


if __name__ == "__main__":
    main()
