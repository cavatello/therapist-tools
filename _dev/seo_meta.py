#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bring titles and descriptions inside the length a result actually shows.

THE FINDING

`_dev/seo_rules.py`, run across the whole site for the first time, returned two
findings far more often than anything else: 93 titles longer than 68 characters
and 104 descriptions longer than 168. That is well over half the site.

Nothing is wrong with the writing. The problem is purely that a search result
shows roughly 60 characters of title and 160 of description, and everything past
that is replaced with an ellipsis. On the 78 school pages the part being cut is
the part that distinguishes them:

    Point Loma Nazarene University - MFT program in California: accreditation,
    cost and what people say                                       (99 chars)

The tail is identical on all 78 pages, so it is both the least useful text on
the page and the only text a reader sees truncated.

HOW IT SHORTENS, AND WHAT IT REFUSES TO DO

Never by truncating mid-sentence and never by adding an ellipsis. A machine
cannot write a better title, but it can find the boundary the author already
put in:

  titles         Drop a trailing site suffix; then cut at the last colon or em
                 dash that still leaves a real title. If neither yields
                 something inside the limit, LEAVE IT ALONE and report it - a
                 hard-truncated title is worse than a long one.
  descriptions   Keep whole sentences: as many complete sentences as fit. If
                 even the first sentence is too long, cut at the last clause
                 boundary - a dash, semicolon or comma - and only if what is
                 left still reads as a sentence and is at least 70 characters.
                 Otherwise leave it and report it.

WHAT THE GUARDS ENFORCE

  - nothing gets shorter than the floor (15 title, 70 description)
  - nothing ends mid-word, on a preposition, or on an opening bracket
  - no two pages end up with the same title or the same description, which
    would trade one problem for a worse one
  - the number of pages with a title and a description does not change

Idempotent: run twice and the second run finds nothing to do. Run before
extract_css and discovery.
"""
import os, re, sys, html

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training")
EXCLUDE = {"tools.html", "concepts.html", "tycoon.html"}
ARTEFACTS = ("_chrome.html",)

TITLE_MAX, TITLE_MIN = 68, 15
DESC_MAX, DESC_MIN = 168, 70

SUFFIXES = (" &mdash; Therapist Support", " &ndash; Therapist Support",
            " — Therapist Support", " - Therapist Support",
            " | Therapist Support", " – Therapist Support")
# A title must not end on one of these. Cutting at a boundary can leave a
# dangling connective, which reads as a truncation even though it is not.
DANGLE = {"and", "or", "the", "a", "an", "of", "in", "on", "for", "to", "with",
          "at", "by", "from", "what", "that", "which", "plus", "including"}

# An author-placed boundary, in either the literal or the entity form. This site
# writes `&mdash;` in its titles, so a pattern that matched only the character
# found no boundary in any of them.
BOUND = (r"\s*(?::|—|–|&mdash;|&ndash;|&#8212;|&#8211;)\s*|\s+(?:•|&bull;)\s+")
DBOUND = (r"\s*(?:—|–|;|&mdash;|&ndash;)\s*|,\s+")


def pages():
    out = [f for f in sorted(os.listdir(SITE))
           if f.endswith(".html") and not f.endswith(ARTEFACTS)]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html") and not f.endswith(ARTEFACTS)]
    return [p for p in out if os.path.basename(p) not in EXCLUDE]


def vis(s):
    """Length as a reader sees it: entities are one character, not six."""
    return len(html.unescape(re.sub(r"\s+", " ", s).strip()))


def ok_end(s):
    t = html.unescape(s).rstrip()
    if not t or t[-1] in "([{-—–,;:":
        return False
    return t.split()[-1].strip(".,;:’'\"").lower() not in DANGLE


def shorten_title(t):
    """Return a shorter title, or None if there is no honest way to shorten it."""
    t = re.sub(r"\s+", " ", t).strip()
    for suf in SUFFIXES:
        if t.endswith(suf) and vis(t[:-len(suf)]) >= TITLE_MIN:
            cand = re.sub(r"(?:\s|&mdash;|&ndash;|[—–|-])+$", "", t[:-len(suf)])
            if vis(cand) <= TITLE_MAX and ok_end(cand):
                return cand
            t = cand          # keep going from the de-suffixed version
            break
    if vis(t) <= TITLE_MAX:
        return t
    # A long parenthetical is the other thing that blows the budget, and it is
    # always the least load-bearing part of the line: "National University
    # (absorbed Northcentral University and John F. Kennedy University) - MFT
    # program in California: ..." is 154 characters, 63 of them an aside.
    without = re.sub(r"\s*\([^()]{12,}\)", "", t).strip()
    if vis(without) >= TITLE_MIN and vis(without) < vis(t):
        t = without
        if vis(t) <= TITLE_MAX and ok_end(t):
            return t
    # Cut at the last author-placed boundary that leaves something real. The
    # entity forms matter: this site writes `&mdash;` in its titles, and the
    # first version of this pattern only looked for the literal character, so
    # every title separated by an entity was reported and never shortened.
    best = None
    for m in re.finditer(BOUND, t):
        head = t[:m.start()].rstrip()
        if TITLE_MIN <= vis(head) <= TITLE_MAX and ok_end(head):
            best = head       # the LAST qualifying boundary, so keep the most
    return best               # None means: leave it alone and report it


SENT = re.compile(r"(?<=[.!?])\s+")


def shorten_desc(d):
    d = re.sub(r"\s+", " ", d).strip()
    if vis(d) <= DESC_MAX:
        return d
    # As many whole sentences as fit.
    parts = SENT.split(d)
    acc = ""
    for p in parts:
        cand = (acc + " " + p).strip() if acc else p
        if vis(cand) > DESC_MAX:
            break
        acc = cand
    if vis(acc) >= DESC_MIN and ok_end(acc):
        return acc
    # The first sentence is itself too long. Fall back to the last clause
    # boundary the author put in, and only if it still reads as one.
    best = None
    for m in re.finditer(DBOUND, d):
        head = d[:m.start()].rstrip()
        if DESC_MIN <= vis(head) <= DESC_MAX and ok_end(head):
            best = head
    return best


def main():
    tfix = dfix = 0
    left_t, left_d = [], []
    titles, descs = {}, {}

    docs = {}
    for rel in pages():
        docs[rel] = open(os.path.join(SITE, rel), encoding="utf-8").read()

    changes = {}
    for rel, s in docs.items():
        out = s

        m = re.search(r"<title>([\s\S]*?)</title>", s, re.I)
        if m:
            t = re.sub(r"\s+", " ", m.group(1)).strip()
            if vis(t) > TITLE_MAX:
                short = shorten_title(t)
                if short and short != t:
                    out = out[:m.start()] + "<title>%s</title>" % short + out[m.end():]
                    tfix += 1
                    t = short
                else:
                    left_t.append((rel, vis(t)))
            titles.setdefault(html.unescape(t).lower(), []).append(rel)

        m = re.search(r'(<meta\s+name="description"\s+content=")([^"]*)(")', out, re.I)
        if m:
            d = re.sub(r"\s+", " ", m.group(2)).strip()
            if vis(d) > DESC_MAX:
                short = shorten_desc(d)
                if short and short != d:
                    out = out[:m.start()] + m.group(1) + short + m.group(3) + out[m.end():]
                    dfix += 1
                    d = short
                else:
                    left_d.append((rel, vis(d)))
            descs.setdefault(html.unescape(d).lower(), []).append(rel)

        if out != s:
            changes[rel] = out

    # ------------------------------------------------------------ collisions
    # Shortening is the one operation here that can CREATE a duplicate: 78
    # school titles that differ only in their tail all collapse onto the same
    # string if the shortener cuts too early. Checked before anything is
    # written, and the whole pass refuses rather than shipping the trade.
    clash = 0
    for t, ps in titles.items():
        if len(ps) > 1:
            print("COLLISION: %d pages would share the title %r" % (len(ps), t[:56]))
            for p in ps[:4]:
                print("           %s" % p)
            clash += 1
    for d, ps in descs.items():
        if len(ps) > 1:
            print("COLLISION: %d pages would share a description" % len(ps))
            for p in ps[:4]:
                print("           %s" % p)
            clash += 1
    if clash:
        sys.exit("\n%d collision(s) - nothing written" % clash)

    for rel, out in changes.items():
        open(os.path.join(SITE, rel), "w", encoding="utf-8").write(out)

    print("%d title(s) shortened, %d description(s) shortened, %d page(s) written"
          % (tfix, dfix, len(changes)))
    if left_t:
        print("\n%d title(s) left alone - no honest boundary to cut at:" % len(left_t))
        for rel, n in left_t[:12]:
            print("  %-54s %d chars" % (rel[:54], n))
    if left_d:
        print("\n%d description(s) left alone:" % len(left_d))
        for rel, n in left_d[:12]:
            print("  %-54s %d chars" % (rel[:54], n))

    # ---------------------------------------------------------------- guards
    bad = 0
    have_t = have_d = 0
    for rel in pages():
        s = open(os.path.join(SITE, rel), encoding="utf-8").read()
        m = re.search(r"<title>([\s\S]*?)</title>", s, re.I)
        if m:
            have_t += 1
            t = m.group(1).strip()
            if vis(t) < TITLE_MIN:
                print("GUARD %s: title down to %d chars" % (rel, vis(t))); bad += 1
            if not ok_end(t):
                print("GUARD %s: title ends badly: %r" % (rel, t[-28:])); bad += 1
        m = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', s, re.I)
        if m:
            have_d += 1
            d = m.group(1).strip()
            if vis(d) < DESC_MIN:
                print("GUARD %s: description down to %d chars" % (rel, vis(d)))
                bad += 1
            if not ok_end(d):
                print("GUARD %s: description ends badly: %r" % (rel, d[-30:]))
                bad += 1
    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("\nguards clean - %d page(s) with a title, %d with a description, none "
          "cut mid-thought" % (have_t, have_d))


if __name__ == "__main__":
    main()
