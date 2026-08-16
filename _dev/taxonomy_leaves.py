#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The 48 case pages become leaves, and three reference pages get real homes.

WHAT WAS WRONG

`mock/library/registry.json` groups every page into a named cluster under one of
five topic hubs. Anything an author does not file by hand gets swept into a
catch-all called "More in {Topic}". That safety net is correct - it stops new
pages becoming orphans - but it is a holding pen, not a category, and the
holding pen had **fifty pages in it**:

    More in Practice ......... 50   (48 discipline cases + 2 reference pages)
    More in Training .......... 1

So the Practice hub read as five small curated sections followed by a wall of
fifty undifferentiated links, and the case library - the site's most
distinctive asset - was presented as leftovers.

THE PATTERN ALREADY EXISTED

This site has solved this once. Sixty-six MFT school pages carry `ts:leaf` and
are represented on the Licensure hub by one directory entry,
`mft-programs-california.html`. Sixteen psychedelic-training pages do the same
under `psychedelic-therapy-training-california.html`. Leaves are reachable,
indexed and linked from their directory; they are simply not listed
individually on a topic hub, because fifty links to fifty case studies is not a
category, it is a table of contents in the wrong place.

The 48 case pages are exactly that shape and were the only large set on the
site not flagged. They now are, and `therapist-discipline-cases-california.html`
represents them - which is what it is for.

THE THREE THAT WERE NOT LEAVES

Three real pages had been swept in with them because nobody had written a
cluster they fit:

  - `therapist-discipline-cases-california.html` and
    `therapy-liability-insurance-california.html` - the two halves of one
    subject. What gets you disciplined, and what answers for it. They become
    **"When something goes wrong"** under Practice.
  - `psyd-programs-california.html` - a directory of doctorates with no cluster
    at all under Training. It becomes **"Where the doctorate comes from"**,
    deliberately parallel to Licensure's "Where the degree comes from".

After this there is no catch-all cluster on the site.

Idempotent. Run before `registry_sync.py`.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
REG = os.path.join(SITE, "mock", "library", "registry.json")

NEW_CLUSTERS = [
    ("practice", "When something goes wrong",
     ["therapist-discipline-cases-california.html",
      "therapy-liability-insurance-california.html"]),
    ("training", "Where the doctorate comes from",
     ["psyd-programs-california.html"]),
    # The practicum page arrived with no cluster to belong to and was swept
    # into the Licensure catch-all, which is exactly the failure this pass
    # exists to stop. It is not part of "Counting the hours" - those pages
    # are all about the post-degree associate - so it gets its own.
    # The stage doors are entry points rather than reference pages, so they
    # get a cluster of their own rather than sitting among the pages they
    # point at.
    ("licensure", "Doors by stage",
     ["for/associates.html",
      "for/students.html",
      "for/deciding.html",
      "for/licensed.html"]),
    ("licensure", "The practicum, and the year before you register",
     ["practicum-california-mft-trainee.html",
      "how-to-find-a-practicum-site-california.html",
      "practicum-sites-bay-area.html",
      "training-programs-bay-area.html",
      "east-bay-practicum-site-directory.html"]),
    # The career-change page is the front door to the whole licensure topic,
    # so it belongs with the route rather than in a cluster of its own. Named
    # here in full because this list replaces a cluster's files rather than
    # appending to them.
    # The portal directory belongs with the pages about getting the job, not
    # with the pages about getting the license.
    # The supervisor page belongs here rather than in "The route": nobody
    # looks for a supervisor before they are registered, and the whole
    # question is which weeks bank and which quietly do not.
    ("licensure", "Counting the hours, and the job that banks them",
     ["finding-a-clinical-supervisor-california.html",
      "county-job-portals-california.html",
      "prelicensed-job-sites-california.html",
      "amft-3000-hours-california.html",
      "bbs-90-day-rule-california.html",
      "associate-employers-bay-area.html",
      "getting-hired-as-a-california-associate.html",
      "loan-forgiveness-employers-california.html",
      "mbh-slrp-california.html",
      "medi-cal-safety-net-employers-california.html",
      "associate-mft-job-advisor.html",
      "associate-therapist-pay-los-angeles-bay-area.html",
      "associate-unpaid-hours-california.html",
      "associate-hours-telehealth-out-of-state.html",
      "associate-hours-trackers-compared.html",
      "out-of-state-to-california-licensure.html",
      "therapists-by-county-california.html",
      "therapists-by-state-compared.html"]),
    ("licensure", "The route, and what it costs",
     ["becoming-a-therapist-california-career-change.html",
      "become-an-mft-california.html",
      "bbs-fees-california-2026.html"]),
]


def main():
    # ------------------------------------------------- 1. ts:leaf on the cases
    n = 0
    for f in sorted(os.listdir(SITE)):
        if not f.startswith("discipline-case-") or not f.endswith(".html"):
            continue
        p = os.path.join(SITE, f)
        s = open(p, encoding="utf-8").read()
        if re.search(r'<meta name="ts:leaf" content="true">', s):
            continue
        if re.search(r'<meta name="ts:leaf"', s):
            s = re.sub(r'<meta name="ts:leaf"[^>]*>',
                       '<meta name="ts:leaf" content="true">', s)
        else:
            # after ts:format, so the block keeps the order registry_meta writes
            m = re.search(r'<meta name="ts:format"[^>]*>', s)
            if not m:
                print("  SKIP %s has no ts:format to anchor to" % f)
                continue
            s = (s[:m.end()] + '\n<meta name="ts:leaf" content="true">'
                 + s[m.end():])
        open(p, "w", encoding="utf-8").write(s)
        n += 1
    print("ts:leaf written on %d case page(s)" % n)

    # ------------------------------------------- 2. real clusters, no catch-all
    reg = json.load(open(REG, encoding="utf-8"))
    moved = 0
    for topic, name, files in NEW_CLUSTERS:
        T = reg["topics"][topic]
        for c in T["clusters"]:
            c["files"] = [f for f in c["files"] if f not in files]
        existing = [c for c in T["clusters"] if c["name"] == name]
        if existing:
            existing[0]["files"] = files
        else:
            # before any catch-all, so a curated cluster never sorts below one
            at = len(T["clusters"])
            for i, c in enumerate(T["clusters"]):
                if c["name"].lower().startswith("more in"):
                    at = i
                    break
            T["clusters"].insert(at, {"name": name, "files": list(files)})
        moved += len(files)
        print("  ok  %-10s %-32s %d page(s)" % (topic, name, len(files)))

    # Drop the case pages out of every cluster - they are leaves now, and a
    # leaf listed in a cluster would still be printed by build_library.
    cases = {f for f in os.listdir(SITE)
             if f.startswith("discipline-case-") and f.endswith(".html")}
    dropped = 0
    for T in reg["topics"].values():
        for c in T["clusters"]:
            before = len(c["files"])
            c["files"] = [f for f in c["files"] if f not in cases]
            dropped += before - len(c["files"])

    # And remove any catch-all left empty.
    for key, T in reg["topics"].items():
        keep = []
        for c in T["clusters"]:
            if c["name"].lower().startswith("more in") and not c["files"]:
                print("  ok  removed the empty catch-all in %s" % key)
                continue
            keep.append(c)
        T["clusters"] = keep

    json.dump(reg, open(REG, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("  ok  %d case listing(s) dropped from clusters" % dropped)

    # ----------------------------------------------------------------- guards
    bad = 0
    reg = json.load(open(REG, encoding="utf-8"))
    for key, T in reg["topics"].items():
        for c in T["clusters"]:
            if c["name"].lower().startswith("more in"):
                print("GUARD: %s still has a catch-all with %d page(s)"
                      % (key, len(c["files"])))
                bad += 1
            if not c["files"]:
                print("GUARD: %s / %r is empty" % (key, c["name"]))
                bad += 1
            for f in c["files"]:
                if f in cases:
                    print("GUARD: %s is a leaf and still listed in %r"
                          % (f, c["name"]))
                    bad += 1
                if not os.path.exists(os.path.join(SITE, f)):
                    print("GUARD: %r names %s, which is not on the site"
                          % (c["name"], f))
                    bad += 1

    # A leaf must still be reachable, or this pass has created 48 orphans.
    hub = open(os.path.join(SITE, "therapist-discipline-cases-california.html"),
               encoding="utf-8").read()
    missing = [f for f in sorted(cases)
               if 'href="%s"' % f not in hub]
    if missing:
        print("GUARD: %d case page(s) are leaves but the hub does not link "
              "them: %s" % (len(missing), ", ".join(missing[:4])))
        bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean - no catch-all clusters, no empty clusters, and every "
          "leaf still linked from its hub")


if __name__ == "__main__":
    main()
