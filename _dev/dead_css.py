#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A stylesheet no page links is retired, and cannot come back quietly.

WHY A NAIVE CHECK FOUND NOTHING

Asked "which sheets in `css/` are dead?", the obvious grep - is this
filename mentioned anywhere in the repository? - answered **none of 49**,
and the answer was worthless. Three retired sheets were being kept alive by
files that are not the site:

    css/house-skin.css      the bc2 skin, ported into the five family
                            sheets and linked by no page - but still loaded
                            by `tools.html`, which put it back on every
                            reader's first paint of that URL
    css/ff2cf0c766d9.css    the dark-header nav, referenced only by
                            `_dev/chrome_donor.html`

`tools.html` is the instructive one. It is a **meta-refresh redirect stub**
that a reader sees for zero milliseconds. It is `ts:skip`, it is not in
`sitemap.xml`, and `build_redirect.py` writes it as a 44-line document with
no stylesheets at all. But that pass was never wired into `ship.py`, so for
every build since, one pass after another appended its chrome, its nav, its
analytics and its `<link>`s to a file whose entire content is "go
somewhere else" - seventeen stylesheets, one of which was the only thing
keeping the retired skin on the live site.

Which is the shape of the whole problem the palette work is about: the old
styles were not lying around unreferenced. They were referenced by
something nobody thought of as a page.

WHAT IT DOES

Walks every `.html` in the repository except `_dev/` and `_to_delete/`,
collects every `css/*.css` a page actually links, and moves anything in
`css/` that nothing links into `_to_delete/`. Moved, not deleted: this
repository is edited through a bridge that cannot delete, so an `unlink`
here would fail on the device.

`_dev/chrome_donor.html` IS counted, and calling it scratch was a mistake
that cost a pipeline run. Eight builders copy its <head> into the pages they
write on every build, so a sheet it names is a sheet the site will link
again in twenty minutes. Everything else under `_dev/` - the mockups, the
structure sketches - is excluded: a sketch must not be able to pin a retired
stylesheet to the site.

THE ONE SHEET THAT IS UNLINKED AND MUST STAY

`css/house-skin.css` is linked by nothing, and retiring it breaks the build.
It is not residue, it is a build INTERMEDIATE, and the pipeline reads it
twice on every run:

  `house_swap.py --all` appends it to every published page and hashes its
  bytes for the `?v=` cache key, and

  the five `family_*.py` passes then take those skinned pages, port the
  rules the page's family needs into `house-<family>.css`, and remove the
  link again - which is why ship.py's own comment reads "After this pass
  NOTHING links house-skin.css."

So the skin is how a page that no family has claimed yet gets found: skin
it, then let `family_rest.py` convert whatever is still skinned. Delete the
file and `house_swap.py` cannot compute its hash and the whole tail of the
build stops. It stays, with this paragraph as the reason, and it costs a
reader nothing because no page links it.

Then it guards the reverse direction too, which is the failure this pass
would otherwise cause: every sheet a page links must exist.

Idempotent: a second run finds nothing to move.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
CSSDIR = os.path.join(SITE, "css")
BINNED = os.path.join(SITE, "_to_delete")
LINKED = re.compile(r'href="(?:\.\./)*css/([^"?]+\.css)')
# Unlinked on purpose. See "THE ONE SHEET THAT IS UNLINKED AND MUST STAY".
KEEP = {"house-skin.css"}


# Read by eight builders every run, so its links are live links.
TEMPLATES = ("_dev/chrome_donor.html",)


def html_files():
    out = []
    for root, dirs, files in os.walk(SITE):
        dirs[:] = [d for d in dirs
                   if d not in ("_dev", "_to_delete", ".git", "node_modules")]
        for f in sorted(files):
            if f.endswith(".html"):
                out.append(os.path.relpath(os.path.join(root, f), SITE))
    out += [t for t in TEMPLATES if os.path.exists(os.path.join(SITE, t))]
    return sorted(out)


def main():
    pages = {rel: open(os.path.join(SITE, rel), encoding="utf-8").read()
             for rel in html_files()}
    live = set()
    for html in pages.values():
        live |= set(LINKED.findall(html))
    disk = {f for f in os.listdir(CSSDIR) if f.endswith(".css")}

    dead = sorted(disk - live - KEEP)
    if dead:
        os.makedirs(BINNED, exist_ok=True)
    moved = 0
    for fn in dead:
        dst = os.path.join(BINNED, "unlinked-" + fn)
        try:
            os.replace(os.path.join(CSSDIR, fn), dst)
            print("  retired  css/%-24s nothing links it" % fn)
            moved += 1
        except OSError as e:
            print("  could not move css/%s (%s)" % (fn, e))
    print("%d stylesheet(s) on disk, %d linked, %d retired"
          % (len(disk), len(live), moved))

    # ------------------------------------------------------------- guards
    bad = 0
    disk = {f for f in os.listdir(CSSDIR) if f.endswith(".css")}
    for rel, html in pages.items():
        for fn in sorted(set(LINKED.findall(html))):
            if fn not in disk:
                print("GUARD %s: links css/%s, which is not on disk"
                      % (rel, fn))
                bad += 1
    for fn in sorted(disk - live - KEEP):
        print("GUARD css/%s: still unlinked after the sweep" % fn)
        bad += 1
    for fn in sorted(KEEP):
        if not os.path.exists(os.path.join(CSSDIR, fn)):
            print("GUARD css/%s is a build intermediate and is missing - "
                  "house_swap.py cannot hash it" % fn)
            bad += 1
    # And the specific way this went wrong once. `build_redirect.py` writes
    # tools.html with no stylesheets and asserts it - correctly, on the file
    # it has just written. Then `house_swap.py --all` ran at the end of the
    # build and put css/house-skin.css back, and because no family pass
    # claims a ts:skip page, nothing ever took it off again. So a redirect
    # stub shipped the retired skin to the live site through a green build
    # and a passing assertion. This pass runs AFTER house_swap and the five
    # families, which is the only place the check means anything.
    for rel, html in pages.items():
        if not re.search(r'<meta http-equiv="refresh"', html, re.I):
            continue
        links = re.findall(r'<link rel="stylesheet"[^>]*>', html)
        if links:
            print("GUARD %s is a redirect stub and carries %d stylesheet(s): "
                  "%s" % (rel, len(links), links[0][:70]))
            bad += 1
    if bad:
        sys.exit("%d problem(s)" % bad)
    print("guard clean - every sheet on disk is linked, every link resolves")


if __name__ == "__main__":
    main()
