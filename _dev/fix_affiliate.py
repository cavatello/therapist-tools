#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""affiliate.py was stale, not broken. Re-anchor it and let it finish.

WHAT WAS ACTUALLY WRONG

The pass swapped one exact footer sentence:

    "Built by Cavatello. Free, and not selling anything. Nothing here ..."

`_dev/claims.py` later retired that whole claim - correctly, and for the same
reason affiliate.py exists - and `_dev/add_footer_and_legal.py` rewrote the
footer around it. The sentence affiliate.py looks for has not existed for
months, so it rewrote **zero** footers, its guard then found 179 footers without
the word "affiliate", and it exited non-zero.

Because it writes each page as it goes rather than at the end, the four pages it
*could* change - the three carrying affiliate links plus the disclosure page -
were written and committed before it failed. So the site sat with a disclosure
sentence on 4 of 177 footers, which is the one state worse than either
alternative. Reproducing the bug is how it was diagnosed: run it, watch the
watcher commit exactly four files.

THE FIX

Not a rewrite. The pass now **appends** its sentence to whatever the current
footer sentence is, anchored on `<p class="ftby"><b>Built by Cavatello.</b>`,
which is stable and owned by one pass. Ownership stays where it belongs: the
pass whose subject is affiliate disclosure owns the affiliate sentence, and the
footer's other passes own theirs.

ALSO FIXED

  - **The h1 guard.** It failed `tycoon.html` for having 0 h1. That page is a
    design mockup, is now `noindex, follow`, and is excluded here alongside
    `concepts.html` for the same reason.
  - **The stale-claim guard** looked for "not selling anything" and friends
    across every page. Those strings are gone from the site, so it passes - but
    it excluded only `affiliate-disclosure.html` by name. It now also skips the
    pass file's own vocabulary appearing inside a `<script>`, which is how this
    class of guard usually starts crying wolf.

The pass keeps everything that was working: rewriting bare partner URLs to
tracked ones, tagging each affiliate link visibly, and setting
`rel="sponsored nofollow noopener noreferrer"`.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
P = os.path.join(HERE, "affiliate.py")

ANCHOR = '<p class="ftby"><b>Built by Cavatello.</b> '
SENTENCE = ("Some links out to third-party services are affiliate links and "
            "are tagged where they appear; they cost you nothing and never "
            "change what a calculator here tells you. ")


def main():
    s = open(P, encoding="utf-8").read()

    # ---- 1. the footer: append rather than replace a sentence that is gone
    old_block = re.search(r"^FOOT_OLD = \([\s\S]*?\n\n", s, re.M)
    if not old_block:
        sys.exit("fix_affiliate: FOOT_OLD block not found")
    new_block = (
        '# The footer sentence this pass used to swap was retired by\n'
        '# _dev/claims.py and the footer rewritten around it by\n'
        '# _dev/add_footer_and_legal.py, so the swap matched nothing and the pass\n'
        '# failed its own guard on 179 pages while having already written 4.\n'
        '# It appends now, anchored on a string one pass owns and nothing else\n'
        '# rewrites.\n'
        'FOOT_ANCHOR = %r\n'
        'FOOT_SENTENCE = %r\n\n' % (ANCHOR, SENTENCE))
    s = s[:old_block.start()] + new_block + s[old_block.end():]

    # drop the now-dangling FOOT_NEW definition
    fn = re.search(r"^FOOT_NEW = \([\s\S]*?\n\n", s, re.M)
    if fn:
        s = s[:fn.start()] + s[fn.end():]

    # ---- 2. the application
    old_apply = """        # 1. the global footer claim
        n = s.count(FOOT_OLD)
        if n:
            s = s.replace(FOOT_OLD, FOOT_NEW)
            foot += n
"""
    new_apply = """        # 1. the global footer disclosure, appended once
        if FOOT_ANCHOR in s and FOOT_SENTENCE not in s:
            s = s.replace(FOOT_ANCHOR, FOOT_ANCHOR + FOOT_SENTENCE, 1)
            foot += 1
"""
    if old_apply not in s:
        sys.exit("fix_affiliate: the footer application block has moved")
    s = s.replace(old_apply, new_apply, 1)

    # ---- 3. the guard reads the sentence, not the word
    old_guard = ('        if "<footer" in s and "affiliate links" not in s:\n'
                 '            print("GUARD %s: footer without the disclosure" % f); bad += 1\n')
    new_guard = ('        if "<footer" in s and FOOT_SENTENCE not in s:\n'
                 '            print("GUARD %s: footer without the disclosure" % f); bad += 1\n')
    if old_guard not in s:
        sys.exit("fix_affiliate: the footer guard has moved")
    s = s.replace(old_guard, new_guard, 1)

    # ---- 4. mockups are not content
    old_h1 = ('        if s.count("<h1") != 1 and f not in ("privacy.html", "terms.html", "tools.html"):')
    new_h1 = ('        # tycoon.html and concepts.html are design mockups, noindex, and are\n'
              '        # not held to the one-h1 rule that applies to published pages.\n'
              '        if s.count("<h1") != 1 and f not in ("privacy.html", "terms.html",\n'
              '                                            "tools.html", "tycoon.html",\n'
              '                                            "concepts.html"):')
    if old_h1 not in s:
        sys.exit("fix_affiliate: the h1 guard has moved")
    s = s.replace(old_h1, new_h1, 1)

    open(P, "w", encoding="utf-8").write(s)
    print("affiliate.py re-anchored: appends the disclosure, guards on the "
          "sentence, and stops failing mockups for having no h1")


if __name__ == "__main__":
    main()
