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

WHAT THIS PASS DOES NOT TOUCH

  Golden Gate University, and the three Golden Gate clinics at CIIS. Proper
  nouns.

  The programme pages' use of "gate" for an academic prerequisite - a course
  you must pass before practicum, a clearance, a candidacy review. That is a
  different and much more natural sense of the word, it is nearly always
  attached to a specific named requirement in the same sentence, and rewriting
  seventy of them mechanically would do more harm than the metaphor does. They
  are left, and the guard below allows them by name.

The rewrite is a fixed list of exact phrases rather than a pattern, because
"gate" in "the gate to practicum" and "gate" in "the four gates" need opposite
treatment and no regular expression can tell them apart.
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
]

# Where the word is allowed to survive: proper nouns, and the programme pages'
# prerequisite sense.
ALLOW = re.compile(r"golden gate|gateway|gatekeep", re.I)
PROGRAM_SENSE = re.compile(
    r"gates? (?:to|on|entry|progression|graduation|practicum|the degree)"
    r"|(?:hard|formal|academic|entry|real|explicit|hidden|first|second|"
    r"zero-unit|zero-credit|fee-bearing|practicum|advancement|writing)\s+gate"
    r"|the gate is|gates? (?:practicum|entry|progression)"
    r"|this is the gate|a gate (?:at|rather|on|in)|gate course|two gates"
    r"|prerequisite gate|eligibility gate|licensure gate|same licensure gate"
    r"|gates template", re.I)


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
            if ALLOW.search(ctx) or PROGRAM_SENSE.search(ctx):
                continue
            print("GUARD %s: %r" % (rel, ctx.strip()[:130]))
            bad += 1

    if bad:
        sys.exit("\n%d unexplained use(s) of \"gate\". Either say "
                 "\"requirement\", or add the phrase to SWAPS." % bad)
    print("  guards clean - no unexplained \"gate\" left in the prose")


if __name__ == "__main__":
    main()
