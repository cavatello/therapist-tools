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
ALLOW = re.compile(r"golden gate|gateway|gatekeep", re.I)


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
    changed, hits = 0, 0
    for rel in pages():
        p = os.path.join(SITE, rel)
        s = open(p, encoding="utf-8").read()
        before = s
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
            if re.search(r"golden gate|gateway|gatekeep", seg, re.I):
                # rewrite around the proper noun rather than through it
                keep = re.split(r"(Golden Gate|Gateway|gateway|Gatekeep)", seg)
                for j in range(0, len(keep), 2):
                    for pat, rep in PATTERNS:
                        keep[j] = re.sub(pat, rep, keep[j])
                seg2 = "".join(keep)
            else:
                seg2 = seg
                for pat, rep in PATTERNS:
                    seg2 = re.sub(pat, rep, seg2)
            if seg2 != seg:
                hits += 1
                parts[i] = seg2
        s = "".join(parts)
        if s != before:
            open(p, "w", encoding="utf-8").write(s)
            changed += 1
    print("  %d replacement(s) across %d page(s)" % (hits, changed))

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
