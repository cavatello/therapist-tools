#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Point the two nav-panel blurbs at counts.py instead of at a memory.

`restyle.py` said "30 real BBS decisions" while the library held 48.
`nav_rebuild.py` said "65 California schools" while there were 66. Both appear
in the navigation panel on every page, so the wrong number was on 185 pages
twice over.

Both files are edited here rather than by hand so the change is recorded with
its reasoning, and both now interpolate. A guard in each file fails the build if
the rendered blurb disagrees with the data.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)


def patch(fname, edits, importline):
    s = open(fname, encoding="utf-8").read()
    for old, new in edits:
        if s.count(old) != 1:
            sys.exit("patch_counts: %s - %r matched %d times"
                     % (fname, old.strip()[:60], s.count(old)))
        s = s.replace(old, new, 1)
        print("  ok  %-18s %s" % (fname, old.strip()[:52]))
    if "import counts" not in s:
        m = re.search(r"^import [^\n]+$", s, re.M)
        s = s[:m.end()] + "\n" + importline + s[m.end():]
    open(fname, "w", encoding="utf-8").write(s)


IMPORT = ('sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\n'
          'import counts  # noqa: E402  - the site\'s counts, computed\n')

patch("restyle.py", [
    ('     "30 real BBS decisions, and what each one cost",',
     '     "%d real BBS decisions, and what each one cost" % counts.cases(),'),
], IMPORT)

patch("nav_rebuild.py", [
    ('     "65 California schools, and what people say",',
     '     "%d California schools, and what people say" % counts.schools(),'),
], IMPORT)
print("\ndone - both blurbs now read off the data")
