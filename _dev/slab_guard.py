#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The build guard P8 says it has, and the reason it never existed.

WHAT P8 SAYS

    | HEY | One slab per page. **One.** | Deep pine, scalloped edges, aimed
    | at the one claim that page makes. A second slab halves the value of
    | the first - **enforced by a build guard.**

There is no such guard. There never was. And the rule could not have been
enforced even if someone had written one, because `.slab` names TWO
components on this site:

    class="slab"                the P8 slab - deep pine, scalloped, one
                                claim. On index.html, and on the three
                                `ops/` documents that exist to demonstrate
                                it.
    class="slab pine"           a coloured SECTION BAND, four to eight per
    class="slab carbon"         page, on five tool and long-form pages:
    class="slab brick"          amft-3000-hours, associate-mft-job-advisor,
    class="slab indigo"         grow-your-therapy-practice,
    class="slab gold"           practice-simulator, therapist-tax-strategy.

Counting `.slab` therefore reports "five pages carry eight slabs each",
which reads as a flagrant violation and is nothing of the kind. That is the
sixth name collision found in this repository, after `.sn`, `.tsshort`,
`.sub`, `.lg` and `.gapbar-seg` - and it is the one that silently disabled
a rule the design document claims is machine-enforced.

HOW THEY ARE TOLD APART WITHOUT TOUCHING ANY MARKUP

The separation is already there and it is total: **a P8 slab carries the
class and nothing else; a section band always carries a colour modifier.**
Measured across every page - 17 bare, 28 modified, and no page mixes them.

So the guard reads the modifier rather than renaming a component. That
matters here specifically: two of the five band pages are
`practice-simulator.html`, whose look is protected by decision, and
`therapist-tax-strategy-california.html`. Renaming a class on those to make
a guard easier would be the tail wagging the dog.

WHAT IT ENFORCES, AND WHAT IT DELIBERATELY DOES NOT

  ENFORCED   no published page may carry more than ONE bare `.slab`. That
             is P8's rule, and it is now true and checked.
  ENFORCED   the two components stay distinguishable - a bare slab must not
             acquire a colour modifier, or the rule silently switches off
             again.
  ENFORCED   the P8 slab keeps its scalloped edge. The scallop is a
             `mask-image:radial-gradient(...)`, and `flat_bands.py` removes
             decorative gradients - so a future version of that pass which
             stopped distinguishing masks from decoration would quietly
             square off the one component P8 borrows from HEY. This guard
             is the tripwire.

  NOT ENFORCED   "one per page" as a floor. **236 of 242 pages have no slab
             at all.** P8 describes a rollout that never happened, and each
             slab is "aimed at the one claim that page makes" - so adding
             236 of them is writing 236 claims. That is a content project,
             not a conformance pass, and a guard that failed the build over
             it would be a guard nobody could ever make green.

The number is printed on every run so the gap stays visible instead of
living in a document nobody opens.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
CSSDIR = os.path.join(SITE, "css")
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training", "for")

BARE = re.compile(r'class="slab"')
MODIFIED = re.compile(r'class="slab\s+([a-z-]+)"')
# The scalloped edge, however a pass chooses to spell the property.
SCALLOP = re.compile(r"(?:-webkit-)?mask(?:-image)?\s*:[^;}]*radial-gradient")


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return out


def main():
    sheets = {f: open(os.path.join(CSSDIR, f), encoding="utf-8").read()
              for f in os.listdir(CSSDIR) if f.endswith(".css")}
    bad, one, none, bands = 0, [], 0, {}
    scalloped = 0
    for rel in pages():
        html = open(os.path.join(SITE, rel), encoding="utf-8").read()
        n = len(BARE.findall(html))
        mods = MODIFIED.findall(html)
        if mods:
            bands[rel] = len(mods)
        if n > 1:
            print("GUARD %s carries %d slabs. P8: \"One slab per page. "
                  "One.\"" % (rel, n))
            bad += 1
        elif n == 1:
            one.append(rel)
            blob = html + "\n" + "\n".join(
                sheets[s] for s in re.findall(
                    r'href="(?:\.\./)?css/([^"?]+\.css)', html) if s in sheets)
            if SCALLOP.search(blob):
                scalloped += 1
            else:
                print("GUARD %s has a slab with no scalloped edge - the mask "
                      "gradient is gone. See flat_bands.py: a mask is not "
                      "decoration." % rel)
                bad += 1
        else:
            none += 1
        # the two components must stay tellable apart
        if n and mods:
            print("GUARD %s mixes a bare slab with %d colour-modified "
                  "band(s); the rule cannot be checked on a page that does "
                  "both" % (rel, len(mods)))
            bad += 1

    print("%d page(s) carry exactly one P8 slab, %d carry none."
          % (len(one), none))
    print("%d of them keep the scalloped edge." % scalloped)
    if bands:
        print("%d page(s) use the SECTION BAND component (`slab <colour>`), "
              "%d band(s) in total - a different thing, not counted above:"
              % (len(bands), sum(bands.values())))
        for rel, k in sorted(bands.items()):
            print("      %-46s %d" % (rel, k))
    print("P8's rollout gap: the slab is on %d of %d published page(s). "
          "That is a content decision, not a build failure - see this "
          "file's docstring." % (len(one), len(pages())))

    if bad:
        sys.exit("%d slab problem(s)" % bad)
    print("guard clean - no page carries two slabs, and every slab it "
          "does carry still has its scallop")


if __name__ == "__main__":
    main()
