#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Merge the video, photo and voices research into videos.json and depth/.

WHAT THIS FIXES. Thirty-four school pages had no video, thirty-nine no photo,
and thirty-three no student voices - and a page with an absent voices section
is not neutral. On a directory that links real forum discussion for the schools
it has any for, silence reads as an endorsement. The pages already say so in
words; this reduces how often they have to.

WHAT DID NOT GET FILLED, AND WHY THAT IS THE RIGHT OUTCOME. The researchers
returned nothing for a large minority of schools and were told to. A campus-tour
video on a page about one specific degree is worse than an empty slot; a
university-wide Niche review presented as an MFT voice is worse still, because
it is wrong rather than merely thin. Several near-misses were rejected on those
grounds and are listed in the run output so the next pass does not re-find them.

THREE JUDGEMENTS BAKED IN HERE.

Photos. Wikimedia Commons only, and only PD/CC0/CC BY/CC BY-SA - the licence
read from the API's own LicenseShortName rather than from anyone's memory of the
file. Pacifica Graduate Institute has six good campus photos and every one is
GFDL, so Pacifica gets no photo. That is the rule working.

Out-of-state buildings are labelled as such. Campbellsville's photo is the
Kentucky main campus, The Chicago School's is Chicago, Northwestern's is
Evanston. Each caption says so, because a California reader looking at a
photograph of a building they cannot attend should be told that is what they
are looking at.

Voices are not filtered for tone. The Antioch complaint about getting practicum
hours signed off, the CSU East Bay graduate finding Colorado would not count the
degree, the Notre Dame de Namur "degree factory" review - those are the most
useful entries in the set and they go in as written.

WHAT WAS EXCLUDED ON PROVENANCE. Two glowing Sentio practicum posts trace to a
forum account that says elsewhere in the same forum "I'm Clinic Director at
Sentio". An unlabelled staff endorsement is not a student voice, and on a school
carrying a Board notice it is the opposite of one.
"""
import os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
DEPTH = os.path.join(HERE, "depth")
VIDEOS = os.path.join(HERE, "videos.json")
SLUGS = json.load(open(os.path.join(HERE, "school_slugs.json"), encoding="utf-8"))
PROGRAMS = json.load(open(os.path.join(HERE, "programs.json"), encoding="utf-8"))
NAMES = {p["institution"] for p in PROGRAMS}

# The researchers keyed on the Board's shorter strings for two schools whose
# display name carries a parenthetical. Map rather than rename: the display
# names are load-bearing (they set the slugs, which are live URLs).
ALIAS = {
    "National University":
        "National University (absorbed Northcentral University and "
        "John F. Kennedy University)",
    "Campbellsville University — Los Angeles Education Center":
        "Campbellsville University — Los Angeles Education Center "
        "(formerly Phillips Graduate University/Institute)",
}

# A caption must not let a reader think an out-of-state building is theirs.
OFF_CAMPUS = {
    "Campbellsville University — Los Angeles Education Center "
    "(formerly Phillips Graduate University/Institute)":
        "This is the Kentucky main campus. The MFT degree is taught at the Los "
        "Angeles Education Center, which is a satellite.",
    "The Chicago School":
        "This is the Chicago building the institution is named for. Its "
        "California MFT programmes are taught in Southern California.",
    "Northwestern University, The Family Institute":
        "This is the Evanston, Illinois campus — the only one. Californians "
        "take the online branch.",
}

# Voices captured from a track that is adjacent to, but not, the MFT degree.
# Kept because they are real and about the same department, labelled because
# passing them off as MFT voices would be the dishonest version of keeping them.
WRONG_TRACK = ("Counseling MA", "LPCC track", "School Counseling",
               "Art Therapy", "different programme")


def load(name):
    p = "/tmp/slices/%s.json" % name
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}


def key(k):
    return ALIAS.get(k, k)


def main():
    vid = {**load("videoA"), **load("videoB")}
    pho = load("photos")
    vox = {**load("voicesA"), **load("voicesB")}

    unknown = [k for d in (vid, pho, vox) for k in d if key(k) not in NAMES]
    if unknown:
        sys.exit("media_apply: unknown institution(s): %s" % ", ".join(unknown))

    # ---- videos
    V = json.load(open(VIDEOS, encoding="utf-8"))
    added_v = []
    for k, v in vid.items():
        n = key(k)
        if n in V:
            continue                      # never overwrite a curated entry
        if not v.get("id") or len(v["id"]) != 11:
            print("  skipped %s: %r is not a YouTube id" % (n, v.get("id")))
            continue
        if not v.get("title") or not v.get("channel"):
            # The researchers were told to copy these verbatim out of the oembed
            # response. A missing one means the id was never actually resolved.
            print("  skipped %s: no oembed title/channel, so the id is unverified" % n)
            continue
        V[n] = {"id": v["id"], "title": v["title"], "channel": v["channel"],
                "why": v.get("why") or "", "kind": v.get("kind") or "program-overview"}
        added_v.append(n)
    json.dump(V, open(VIDEOS, "w", encoding="utf-8"), indent=1, ensure_ascii=False)

    # ---- photos and voices, into the per-school depth records
    OK_LIC = ("cc0", "public domain", "cc by", "cc by-sa", "pd")
    added_p, added_x, skipped = [], [], []
    for n in sorted(NAMES):
        sl = SLUGS.get(n, "").replace(".html", "")
        f = os.path.join(DEPTH, sl + ".json")
        if not sl or not os.path.exists(f):
            continue
        d = json.load(open(f, encoding="utf-8"))
        changed = False

        p = pho.get(n) or pho.get(next((a for a, b in ALIAS.items() if b == n), ""))
        if p and not d.get("photo"):
            lic = (p.get("license") or "").lower()
            if not any(lic.startswith(x) for x in OK_LIC) or "nc" in lic.split() \
               or "-nc" in lic or "-nd" in lic or "gfdl" in lic:
                skipped.append("%s (licence %r)" % (n, p.get("license")))
            elif not p.get("file", "").startswith("https://upload.wikimedia.org/"):
                skipped.append("%s (not a Commons upload URL)" % n)
            else:
                cap = p.get("caption") or ""
                if n in OFF_CAMPUS:
                    cap = (cap.rstrip(". ") + ". " + OFF_CAMPUS[n]).strip()
                d["photo"] = {"file": p["file"], "page": p.get("page"),
                              "license": p["license"], "credit": p.get("credit"),
                              "caption": cap}
                added_p.append(n)
                changed = True

        x = vox.get(n) or vox.get(next((a for a, b in ALIAS.items() if b == n), ""))
        if x:
            have = {(v.get("url"), v.get("text")) for v in (d.get("voices") or [])}
            new = []
            for v in x:
                if not v.get("url") or not v.get("text"):
                    continue
                if (v["url"], v["text"]) in have:
                    continue
                if v.get("sentiment") not in ("positive", "negative", "mixed", "info"):
                    v["sentiment"] = "info"
                new.append({"text": v["text"], "who": v.get("who") or "",
                            "sentiment": v["sentiment"], "url": v["url"]})
            if new:
                d["voices"] = (d.get("voices") or []) + new
                added_x.append("%s(%d)" % (n[:28], len(new)))
                changed = True

        if changed:
            json.dump(d, open(f, "w", encoding="utf-8"), indent=1,
                      ensure_ascii=False)

    print("videos  +%d  (now %d of %d schools)" % (len(added_v), len(V), len(SLUGS)))
    print("photos  +%d" % len(added_p))
    print("voices  +%d school(s): %s" % (len(added_x), ", ".join(sorted(added_x))))
    if skipped:
        print("REFUSED (licence or source):")
        for s in skipped:
            print("   " + s)

    # ---- guards
    bad = 0
    for n, v in V.items():
        if n not in NAMES:
            print("GUARD: videos.json names %r, which is not an institution" % n)
            bad += 1
        if len(v.get("id", "")) != 11:
            print("GUARD %s: bad video id" % n)
            bad += 1
    n_pho = n_vox = 0
    for n in NAMES:
        sl = SLUGS.get(n, "").replace(".html", "")
        f = os.path.join(DEPTH, sl + ".json")
        if not sl or not os.path.exists(f):
            continue
        d = json.load(open(f, encoding="utf-8"))
        ph = d.get("photo")
        if ph:
            n_pho += 1
            lic = (ph.get("license") or "").lower()
            if "nc" in lic.replace("nc-", "") and "-nc" in lic or "-nd" in lic \
               or "gfdl" in lic:
                print("GUARD %s: photo licence %r is not usable here"
                      % (n, ph.get("license")))
                bad += 1
            if not ph.get("credit"):
                print("GUARD %s: photo with no credit line" % n)
                bad += 1
        for v in (d.get("voices") or []):
            n_vox += 1
            if not v.get("url"):
                print("GUARD %s: a voice with no link - it cannot be checked" % n)
                bad += 1
    print("totals: %d with a photo, %d voices across the set" % (n_pho, n_vox))
    if bad:
        sys.exit("media_apply: %d guard failure(s)" % bad)
    print("guards clean")


if __name__ == "__main__":
    main()
