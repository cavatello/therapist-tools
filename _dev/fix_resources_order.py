#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The toolkit page opens with a changelog. Move it, and say who it is for.

REPORTED

  "Shouldn't the toolkit toolbox have hero h1 content as landing page
   explaining what kind of toolkit and for whom? seems above the fold or right
   after should jump right into categories"

Correct on both counts. `resources.html` is the site's "everything" page and the
destination of the masthead's Resources link, the footer's Everything link and
every topic hub's "the other four areas" block. Its first section under the hero
was **What moved, and when** - a changelog.

A changelog is the right thing to publish and the wrong thing to lead with. A
reader arriving at "everything on this site" is asking *what is here and is any
of it for me*. Answering with "here are four figures that changed recently"
assumes they already know.

WHAT CHANGES

Two things, both small:

1. **A "who this is for" line under the hero**, before anything else. The hero
   already says what the site contains - seven calculators, two directories, the
   reference pages, each stamped with the month it was checked. It does not say
   who it is for, and that is the sentence that lets somebody decide in three
   seconds whether to keep reading.
2. **The changelog moves to the end**, after the calculators, the questions, the
   topics and the directories. It keeps its `#what-moved` id, so every existing
   link to it still lands.

Nothing is deleted and no copy is rewritten. The page now goes: what this is and
who it is for, then straight into the categories, then what changed.

Run before `mock/library/build_library.py`; it edits the builder, not the page.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
B = os.path.join(SITE, "mock", "library", "build_library.py")

WHO = '''<section class="sec"><h2 id="who">Who this is for</h2>
<p>California therapists, at every stage &mdash; somebody choosing between an MFT
and a doctorate, an associate counting toward 3,000 hours, a newly licensed
clinician working out what a practice actually pays, and a practice with room to
grow. <b>Everything here is free, and nothing asks you to make an account.</b>
Every figure is either computed from your own numbers or cited to the rule it
came from, and every page carries the month it was last checked.</p>
<p>If you do not know where to start, the three routes below are the same
material sorted three ways: by the number you need, by the question you arrived
with, or by the area you are dealing with.</p></section>

'''


def main():
    s = open(B, encoding="utf-8").read()

    start = s.index('<section class="promise"><h2 id="what-moved">')
    end = s.index('<section class="sec"><h2 id="calculators">')
    block = s[start:end]
    if "%s" not in block:
        sys.exit("fix_resources_order: the changes block lost its placeholder")

    if 'id="who"' in s:
        print("already reordered")
        return

    # The block carries a %s, and the body is built with positional %-formatting,
    # so moving the text without moving its argument silently shifts every later
    # argument by one - which surfaces as "%d format: a real number is required,
    # not str", nowhere near the actual mistake.
    #
    # Rather than reorder a nine-item tuple by hand, the placeholder is swapped
    # for a sentinel that %-formatting ignores, and the changelog is substituted
    # after the format completes. The tuple is then left exactly as it was.
    moved = block.replace("%s", "@@CHANGES@@").rstrip()

    s = s[:start] + WHO + s[end:]

    tail = s.index('</div>""" % (changes_block(4),')
    s = s[:tail] + moved + "\n" + s[tail:]
    s = s.replace('</div>""" % (changes_block(4),\n', '</div>""" % (', 1)

    # substitute after the format, wherever the body is finished
    anchor = "\n    return "
    i = s.index(anchor, s.index("@@CHANGES@@"))
    s = (s[:i] + '\n    body = body.replace("@@CHANGES@@", changes_block(4))\n'
         + s[i:])

    open(B, "w", encoding="utf-8").write(s)
    print("build_library.py: orientation first, changelog last")

    # ---- guards
    s = open(B, encoding="utf-8").read()
    if s.count('id="what-moved"') != 1:
        sys.exit("guard: %d what-moved anchors" % s.count('id="what-moved"'))
    if s.index('id="who"') > s.index('id="calculators"'):
        sys.exit("guard: the orientation block did not land above the categories")
    if s.index('id="calculators"') > s.index('id="what-moved"'):
        sys.exit("guard: the changelog is still above the categories")
    print("guards clean - who, then the three routes, then what changed")


if __name__ == "__main__":
    main()
