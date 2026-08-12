#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild registry.json from the pages, so a new page needs no central edit.

This is the second half of the handover started by registry_meta.py. That pass
writes each page's library metadata into the page. This one reads it back and
regenerates the registry's `pages` array from what the pages actually say.

AFTER THIS, THE PAGE IS THE SOURCE OF TRUTH. Write an article, give it a
ts:meta block, run the pipeline, and it appears on its topic hub, in the
question index, and in the up-link rotation of its siblings. Nobody edits a
central file, so nobody forgets to.

WHAT THIS PASS DOES *NOT* TOUCH, AND WHY.

`topics` stays hand-written - the name, the tagline, the two paragraphs of
orientation, and the cluster structure. Those are editorial judgements, not
metadata. Deciding that "Sole proprietor, or a corporation" is one idea and
"Tax you can defer, and tax you must send" is another is the work; a machine
grouping by weight would produce five buckets called "Money 1" through
"Money 5" and the topic hubs would stop being worth reading. The hub study was
explicit that a category page which is only an auto-generated list is a thin
page, and the fix is that it carries writing of its own.

`changes` stays hand-written for the same reason: it is a log of numbers that
moved, and a machine cannot know that a fee schedule changed.

CLUSTER PLACEMENT IS AUTOMATIC WHEN IT HAS TO BE. A page whose file appears in
no cluster is appended to a per-topic "More in {Topic}" cluster rather than
dropped. That is the safety net which lets the loop actually close: an author
who writes a page and does not think about clusters still gets a page that is
reachable, and the editor can move it into a real cluster later. Without it,
"no central edit required" would be false the moment somebody wrote something.

Directory leaves are excluded from that net - eighty-one programme and training
pages appended to a topic hub would be a directory wearing a hub's clothes,
which is the thing the whole structure exists to avoid. They stay reachable
through their directory.

ORDER IN THE PIPELINE: after the page builders, after registry_meta.py, and
BEFORE build_library.py - which reads the registry this writes.
"""
import os, re, sys, json, html

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
REGISTRY = os.path.join(SITE, "mock", "library", "registry.json")
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training", "for")
CATCHALL = "More in %s"


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return out


def read_meta(doc):
    out = {}
    for m in re.finditer(r'<meta name="ts:([a-z]+)" content="([^"]*)">', doc):
        k, v = m.group(1), html.unescape(m.group(2))
        if k in ("leaf", "stale", "skip"):
            out[k] = (v == "true")
        elif k == "weight":
            try:
                out[k] = int(v)
            except ValueError:
                out[k] = 1
        else:
            out[k] = v
    return out


def title_of(doc):
    m = re.search(r"<title>(.*?)</title>", doc, re.S)
    return html.unescape(re.sub(r"\s+", " ", m.group(1)).strip()) if m else ""


def main():
    if not os.path.exists(REGISTRY):
        sys.exit("registry_sync: %s missing" % REGISTRY)
    REG = json.load(open(REGISTRY, encoding="utf-8"))
    old = {p["file"]: p for p in REG["pages"]}

    found, added, changed, dropped = {}, [], [], []
    for f in pages():
        s = open(os.path.join(SITE, f), encoding="utf-8").read()
        meta = read_meta(s)
        if not meta.get("topic") or not meta.get("question"):
            continue                      # not a library page
        rec = {
            "file": f,
            "title": title_of(s) or old.get(f, {}).get("title", f),
            "topic": meta["topic"],
            "format": meta.get("format", "answer"),
            "question": meta["question"],
            "outcome": meta.get("outcome", ""),
            "number": meta.get("number") or None,
            "stale": bool(meta.get("stale")),
            "weight": meta.get("weight", 1),
            "skip": bool(meta.get("skip")),
            "leaf": bool(meta.get("leaf")),
        }
        # KEYS THIS PASS DOES NOT OWN SURVIVE. `rec` is rebuilt from the
        # page's own meta tags every run, so anything held only in the
        # registry - the stage tagging written by _dev/stage_tags.py, for one -
        # would be silently deleted on the next build. It was, once. The page
        # meta is the source of truth for the fields above and the registry is
        # the source of truth for everything else, so carry the rest across.
        for k, v in old.get(f, {}).items():
            if k not in rec:
                rec[k] = v

        found[f] = rec
        if f not in old:
            added.append(f)
        else:
            diff = [k for k in rec
                    if k != "title" and rec[k] != old[f].get(k)]
            if diff:
                changed.append((f, diff))
    dropped = [f for f in old if f not in found]

    REG["pages"] = [found[f] for f in sorted(found)]

    # ---- sweep files that no longer exist, FIRST
    # Placement below decides whether a catch-all cluster is empty and can
    # be removed. If a deleted page is still sitting in that cluster when
    # the check runs, the cluster reads as non-empty and survives as an
    # empty heading on the topic hub. Sweep, then place.
    # a cluster may still name a file that no longer exists
    for t, T in REG["topics"].items():
        for c in T["clusters"]:
            gone = [x for x in c["files"] if x not in found]
            if gone:
                c["files"] = [x for x in c["files"] if x in found]
                dropped += [g for g in gone if g not in dropped]

    # ---- cluster placement, for anything an author did not file by hand
    placed = 0
    for t, T in REG["topics"].items():
        filed = {x for c in T["clusters"] for x in c["files"]}
        loose = [f for f, r in found.items()
                 if r["topic"] == t and not r["skip"] and not r["leaf"]
                 and f not in filed]
        if not loose:
            # tidy up: an empty catch-all left behind by a later hand edit
            T["clusters"] = [c for c in T["clusters"]
                             if c["files"] or c["name"] != CATCHALL % T["name"]]
            continue
        name = CATCHALL % T["name"]
        cat = next((c for c in T["clusters"] if c["name"] == name), None)
        if not cat:
            cat = {"name": name, "files": []}
            T["clusters"].append(cat)
        for f in sorted(loose):
            cat["files"].append(f)
            placed += 1

    json.dump(REG, open(REGISTRY, "w", encoding="utf-8"),
              indent=1, ensure_ascii=False)

    print("registry: %d pages from page meta" % len(found))
    if added:
        print("  added   %d: %s" % (len(added), ", ".join(added[:5])))
    if changed:
        print("  updated %d: %s" % (len(changed),
                                    ", ".join("%s(%s)" % (f, ",".join(d))
                                              for f, d in changed[:4])))
    if dropped:
        print("  removed %d: %s" % (len(dropped), ", ".join(dropped[:5])))
    if placed:
        print("  auto-filed %d page(s) into a 'More in ...' cluster" % placed)

    # ---- guards
    bad = 0
    live = set(pages())
    for p in REG["pages"]:
        if p["file"] not in live:
            print("GUARD: registry names a missing file %s" % p["file"])
            bad += 1
        if p["topic"] not in REG["topics"]:
            print("GUARD %s: unknown topic %r" % (p["file"], p["topic"]))
            bad += 1
        if not p["outcome"] and not p["skip"]:
            print("GUARD %s: no outcome line - every card needs one" % p["file"])
            bad += 1
    # Every non-leaf, non-skipped page must end up in exactly one cluster, or
    # it is unreachable from its own topic hub.
    for t, T in REG["topics"].items():
        filed = [x for c in T["clusters"] for x in c["files"]]
        if len(filed) != len(set(filed)):
            dupes = sorted({x for x in filed if filed.count(x) > 1})
            print("GUARD %s: file in two clusters: %s" % (t, ", ".join(dupes)))
            bad += 1
        want = {p["file"] for p in REG["pages"]
                if p["topic"] == t and not p["skip"] and not p["leaf"]}
        missing = want - set(filed)
        if missing:
            print("GUARD %s: unreachable from its hub: %s"
                  % (t, ", ".join(sorted(missing))))
            bad += 1
    # This pass must never silently empty the registry - a bad regex would.
    # Nothing that was in the registry may leave it without the page leaving
    # the site. A key vanishing from every record at once is what a rewrite
    # that forgot to carry fields across looks like.
    before = set()
    for r in old.values():
        before |= set(r)
    after = set()
    for r in REG["pages"]:
        after |= set(r)
    lost = before - after
    if lost and old:
        print("GUARD: %s disappeared from every record - this pass rebuilt "
              "them and dropped a field it does not own"
              % ", ".join(sorted(lost)))
        bad += 1

    if len(REG["pages"]) < 0.8 * len(old):
        print("GUARD: registry shrank from %d to %d - refusing"
              % (len(old), len(REG["pages"])))
        bad += 1
    if bad:
        sys.exit("registry_sync: %d guard failure(s)" % bad)
    print("guards clean")


if __name__ == "__main__":
    main()
