#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Say "requirement", not "gate".

WHAT WAS WRONG, AND IT WAS TWO THINGS

The site had settled into calling the four hour requirements "gates" - four
gates, all four must close, which gate is holding you. One of those phrases was
in the site navigation, so it was on 199 pages.

**Nobody outside the person who wrote it knows what a gate is meant to be.** It
is a metaphor doing the work a plain noun would do better, and this audience is
reading under stress about a licence they cannot afford to get wrong.

**And the metaphor said something false.** "Four gates, all four must close"
puts the 3,000 at the top and frames it as the thing you are working toward.
The 3,000 is almost never what decides anybody's date. A caseload of adult
individuals reaches 3,000 long before it produces 500 relational hours, and
anybody moving quickly is bound by the 104 weeks instead. The site knew this -
`amft-3000-hours-california.html` says it in as many words - and then buried it
under a metaphor pointing the other way.

TWO SENSES, TWO PLAIN WORDS

The word was doing two jobs and both are better done by a plain noun:

  the four hour minimums          -> **requirement**
  an academic step you must pass  -> **checkpoint**
  before practicum

"Checkpoint" is not jargon and needs no explanation, which is the whole test.
The first sense is a fixed list of exact phrases, because those sentences also
needed their meaning corrected. The second is a short list of patterns, because
the programme pages say it seventy different ways and every one of them means
the same thing.

WHAT THIS PASS DOES NOT TOUCH

Golden Gate University, the three Golden Gate clinics at CIIS, and "gateway".
Proper nouns. Everything else is rewritten, and the guard at the end fails the
build on any survivor.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training", "for")

# Exact phrase in, plain phrase out. Longest first so a short rule cannot eat
# the front of a long one.
SWAPS = [
    # the navigation string, on nearly every page
    ("which gate is actually holding you",
     "which requirement is holding you up"),
    ("FOUR GATES &#183; ALL FOUR MUST CLOSE",
     "FOUR REQUIREMENTS &#183; ALL FOUR HAVE TO BE MET"),
    ("FOUR GATES &middot; ALL FOUR MUST CLOSE",
     "FOUR REQUIREMENTS &middot; ALL FOUR HAVE TO BE MET"),

    # the framing that pointed the wrong way
    ("The 3,000 is almost never the gate that decides your date",
     "The 3,000 is almost never the requirement that decides your date"),
    ("The 3,000 is rarely the gate that decides your date",
     "The 3,000 is rarely the requirement that decides your date"),
    ("500 relational hours is the gate people reach 3,000 without",
     "The 3,000 is almost never what decides your date"),
    ("the gate an all-adult caseload never closes",
     "the one an all-adult caseload never produces"),
    ("This is the gate that strands people, because an all-adult caseload "
     "never closes it",
     "This is what strands people, because an all-adult caseload never "
     "produces it"),

    # plain plurals
    ("against all four gates rather than one",
     "against all four requirements rather than one"),
    ("projects a real licensure date against all four gates",
     "projects a real licensure date against all four requirements"),
    ("Your working week projected against all four gates",
     "Your working week projected against all four requirements"),
    ("project all four gates from the week you actually work",
     "project all four requirements from the week you actually work"),
    ("The calculators here project all four gates",
     "The calculators here project all four requirements"),
    ("names the gate you are actually waiting on",
     "names the requirement you are actually waiting on"),
    ("tell you which gate is actually holding you up",
     "tell you which requirement is actually holding you up"),
    ("There are four gates and they close at different speeds",
     "There are four requirements and they fill at different speeds"),
    ("The one holding you is m", "The one holding you up is m"),
    ("02 The four gates", "02 The four requirements"),
    ("The requirements the four gates above are built on",
     "The requirements the four figures above are built on"),
    ("Units of supervision, the four gates, and the one that usually binds",
     "Units of supervision, the four requirements, and the one that usually "
     "binds"),

    # the licensure route
    ("Five gates, each tied to its code section",
     "Five requirements, each tied to its code section"),
    ("The five gates", "The five requirements"),
    ("five gates with no discretion in any of them",
     "five requirements with no discretion in any of them"),
    ("Every gate between a master&rsquo;s degree and an LMFT license",
     "Every requirement between a master&rsquo;s degree and an LMFT license"),
    ("The single most expensive mistake on this page is gate three",
     "The single most expensive mistake on this page is the third"),

    # one-offs
    ("The last gate, taken after the 3,000 hours are already done",
     "The last step, taken after the 3,000 hours are already done"),
    ("The four gates", "The four requirements"),
    ("is gate three", "is the third one"),
    ("What it keeps is the gate:", "What it keeps is the condition:"),
]

# The academic sense. Patterns rather than exact phrases, because seventy
# programme pages say the same thing seventy ways. Verb uses ("CSUDH gates
# entry to fieldwork") need a different rewrite from noun uses, so they are
# listed first and matched first.
PATTERNS = [
    (r"\bgates entry to\b", "controls entry to"),
    (r"\bgates? progression on\b", "makes progression conditional on"),
    (r"\bgates? (?:the )?graduation on\b", "makes graduation conditional on"),
    (r"\bgate entry to\b", "control entry to"),
    (r"\bgates template\b", "restricts template"),
    (r"\bbookend and gate the degree\b", "bookend and control the degree"),
    (r"\bgate to (?:starting )?practicum\b", "checkpoint before practicum"),
    (r"\bgate to entering\b", "checkpoint before entering"),
    (r"\bTwo gates matter\b", "Two checkpoints matter"),
    (r"\bTwo hard gates\b", "Two hard checkpoints"),
    (r"\bgates?\b(?= (?:matter|sit|are|is))", "checkpoint"),
    (r"\bgates\b", "checkpoints"),
    (r"\bgate\b", "checkpoint"),
]

# The only survivors. Proper nouns.
#
# `golden[-\s]gate` rather than `golden gate`: the hyphenated form is how the
# name appears in a slug, and the space-only version is what let this pass
# rewrite a URL. See the note below.
ALLOW = re.compile(r"golden[-\s]gate|gateway|gatekeep", re.I)

# ---------------------------------------------------------------------------
# THE BUG THIS SECTION EXISTS TO CLOSE
#
# Run on its own, this pass used to rewrite
#
#     https://therapistsupport.org/golden-gate-university-mft.html
#  -> https://therapistsupport.org/golden-checkpoint-university-mft.html
#
# inside the JSON-LD on that page - a canonical and a breadcrumb pointing at a
# page that does not exist - and then its own guard reported clean.
#
# Two separate mistakes, and the second is the one worth remembering.
#
# 1. The rewriter split the document on tags, which leaves the CONTENTS of a
#    script element sitting in the "prose" half. JSON-LD is text between tags,
#    not text inside one.
# 2. The guard strips `<script>` and `<style>` before it looks. So the fixer
#    was editing a region the guard was blind to. **A guard and its fixer must
#    measure the same thing** - already written down in this repository after
#    seo_meta.py and seo_rules.py disagreed about the width of an em dash, and
#    true again here.
#
# It was survivable only by luck of ordering: discovery.py runs later in
# ship.py and regenerates that block, so a full build repaired the damage
# before anyone saw it. Running this pass alone, or resuming with `--from`
# past discovery, would have shipped it.
#
# So: script and style contents are protected outright, and inside prose any
# token that looks like a URL, a path or a hyphenated compound is masked out
# before the patterns run and put back afterwards.
PROTECT = re.compile(r"<(script|style)\b[\s\S]*?</\1>", re.I)
# A URL or a filename, and NOTHING ELSE.
#
# The first version of this read "any non-space run containing a slash", which
# also matches `up</i></span></a><a` - a closing tag carries a slash. Run over
# the whole pipeline it reported 239 pages as having their URLs rewritten when
# not one had: the tokens that changed were markup adjacent to the prose being
# corrected. That is the same mistake this file's own note is about, made one
# layer up - a guard measuring something other than the thing it names. Caught
# because a full build went red, which is the point of running one.
#
# So: an explicit scheme, or a token ending in a real file extension, and in
# both cases nothing containing a bracket, a quote or whitespace.
#
# A bare directory link (`/money/`) is deliberately NOT matched. "gate" cannot
# become a different directory without also being part of a hyphenated slug,
# and SLUGGY masks those.
# The filename branch spells its character class out rather than using
# "anything that is not a bracket or a quote". Same 377 matches on the largest
# page here; 0.05s instead of 2.17s. Negated classes backtrack badly against a
# half-megabyte of markup, and this runs twice per page over 242 pages - the
# lazy version took the guard from seconds to a quarter of an hour.
URLISH = re.compile(
    r"""https?://[^\s"'<>]+"""
    r"""|[A-Za-z0-9_~./-]+\.(?:html?|php|css|js|json|xml|pdf|png|jpe?g|svg|webp|ico|txt|md)\b""",
    re.I)
# A hyphenated compound containing the word, e.g. a slug fragment.
SLUGGY = re.compile(r"\b\w*(?:-\w+)*-?gates?(?:-\w+)+\b|\b\w+-gates?\b", re.I)


def mask(seg):
    """Hide anything a rewrite must not reach, and hand back a restorer."""
    store = []

    def keep(m):
        store.append(m.group(0))
        return "\x00%d\x00" % (len(store) - 1)

    seg = URLISH.sub(keep, seg)
    seg = SLUGGY.sub(keep, seg)
    return seg, store


def unmask(seg, store):
    for i, v in enumerate(store):
        seg = seg.replace("\x00%d\x00" % i, v)
    return seg


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return out


def main():
    print("plain words: requirement, not gate")
    changed, hits, urlbad = 0, 0, 0
    for rel in pages():
        p = os.path.join(SITE, rel)
        s = open(p, encoding="utf-8").read()
        before = s

        # Script and style bodies are text between tags, so a plain tag split
        # would treat JSON-LD as prose. Lift them out before ANY rewriting -
        # including the literal swaps - and put them back untouched. These are
        # the same regions this pass's own guard excludes, which is the whole
        # point: a fixer and its guard have to look at the same document.
        held = []

        def hold(m):
            held.append(m.group(0))
            return "\x01%d\x01" % (len(held) - 1)

        s = PROTECT.sub(hold, s)

        for old, new in SWAPS:
            if old in s:
                hits += s.count(old)
                s = s.replace(old, new)

        # Then the academic sense, outside tags and outside proper nouns.
        def one(m):
            t = m.group(0)
            if ALLOW.search(s[max(0, m.start() - 12):m.end() + 8]):
                return t
            for pat, rep in PATTERNS:
                new_t = re.sub(pat, rep, t)
                if new_t != t:
                    return new_t
            return t

        parts = re.split(r"(<[^>]+>)", s)
        for i in range(0, len(parts), 2):
            seg = parts[i]
            if not re.search(r"\bgates?\b", seg, re.I):
                continue
            masked, store = mask(seg)
            if ALLOW.search(masked):
                # rewrite around the proper noun rather than through it
                keep = re.split(r"(Golden Gate|Gateway|gateway|Gatekeep)",
                                masked)
                for j in range(0, len(keep), 2):
                    for pat, rep in PATTERNS:
                        keep[j] = re.sub(pat, rep, keep[j])
                seg2 = "".join(keep)
            else:
                seg2 = masked
                for pat, rep in PATTERNS:
                    seg2 = re.sub(pat, rep, seg2)
            seg2 = unmask(seg2, store)
            if seg2 != seg:
                hits += 1
                parts[i] = seg2
        s = "".join(parts)
        for i, v in enumerate(held):
            s = s.replace("\x01%d\x01" % i, v)

        # The guard for the bug described at the top of this file, stated as
        # the invariant it actually is: THIS PASS MAY NEVER CHANGE A URL. It
        # rewrites prose. Comparing the page's URL-ish tokens before and after
        # catches a rewrite that reached into a link, a canonical, a slug or a
        # JSON-LD block, whichever new spelling of the mistake arrives - and
        # unlike the prose guard below, it looks inside script elements,
        # because that is where the damage happened.
        was, now = sorted(URLISH.findall(before)), sorted(URLISH.findall(s))
        if was != now:
            moved = [x for x in now if x not in was][:4]
            print("GUARD %s: this pass changed %d URL-ish token(s), e.g. %r"
                  % (rel, len(now) - len([x for x in now if x in was]), moved))
            urlbad += 1
            s = before

        if s != before:
            open(p, "w", encoding="utf-8").write(s)
            changed += 1
    print("  %d replacement(s) across %d page(s)" % (hits, changed))
    if urlbad:
        sys.exit("\n%d page(s) had a URL rewritten. Refused, and left "
                 "unchanged. See the note at the top of this file." % urlbad)

    # ----------------------------------------------------------------- guard
    bad = 0
    for rel in pages():
        s = open(os.path.join(SITE, rel), encoding="utf-8").read()
        t = re.sub(r"<(script|style)[\s\S]*?</\1>", " ", s, flags=re.I)
        t = re.sub(r"<[^>]+>", " ", t)
        t = re.sub(r"\s+", " ", t)
        for m in re.finditer(r"\bgates?\b", t, re.I):
            ctx = t[max(0, m.start() - 90):m.start() + 90]
            if ALLOW.search(t[max(0, m.start() - 14):m.end() + 10]):
                continue
            print("GUARD %s: %r" % (rel, ctx.strip()[:130]))
            bad += 1

    if bad:
        sys.exit("\n%d unexplained use(s) of \"gate\". Say "
                 "\"requirement\" for an hour minimum and \"checkpoint\" "
                 "for an academic step, or add the phrase to SWAPS." % bad)
    print("  guards clean - no unexplained \"gate\" left in the prose")


if __name__ == "__main__":
    main()
