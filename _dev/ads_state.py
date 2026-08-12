#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The advertising sentence, derived from whether the site actually serves ads.

THE PROBLEM WITH THE SENTENCE THAT IS THERE

`affiliate-disclosure.html` currently says, in the list of things this site does
not do:

    This site carries advertising, and advertising never buys a mention, a
    ranking or a number.

It does not carry advertising. Not one slot, not one network script. The
sentence was written to retire the old **"no advertising, ever"** promise ahead
of ads arriving, which was the right instinct - a promise you intend to break is
worse than no promise - but the replacement over-corrected into a claim that is
false today.

On a site whose entire proposition is that every figure traces to something
real, an inaccurate sentence on the *disclosure* page is the worst possible
place to keep one. It is also the sentence a reader is most likely to test.

WHY A CONSTANT RATHER THAN A REWRITE

Rewriting it to "does not currently carry advertising" just moves the problem:
the day ads ship, the disclosure page quietly becomes wrong again, and nobody
will remember this file. Whoever adds the ad tag will be thinking about the ad
tag.

So the sentence is *derived*. One boolean at the top of this file decides which
of two paragraphs renders, and the guard at the bottom **checks the boolean
against the site itself**: it greps every page for the known ad-network
signatures, and exits non-zero if the site is serving ads while the flag says it
is not, or the other way round. The claim cannot drift from the fact without the
build failing.

This is the same shape as the affiliate list on that page, which is generated
from a single file precisely so a link cannot exist on the site without
appearing in the disclosure. The advertising sentence now works the same way.

WHEN ADS SHIP

Flip `CARRIES_ADS` to True and re-run. Nothing else. Both paragraphs are written
already, and both say the part that actually matters - that nothing an
advertiser pays for gets inside a calculator, a comparison or a recommendation -
because that promise is true in either state and is the one worth making.

Idempotent, guarded.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
PAGE = os.path.join(SITE, "affiliate-disclosure.html")
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training", "for")

# The single fact this page's advertising sentence is derived from.
CARRIES_ADS = False

# What "serving ads" looks like in the wild. Checked against every page.
AD_SIGNATURES = [
    "googlesyndication.com", "adsbygoogle", "doubleclick.net",
    "amazon-adsystem.com", "media.net", "carbonads", "ethicalads",
    "buysellads", "adthrive", "mediavine", "ezoic", "data-ad-client",
]

WITHOUT = ("<b>No sponsored content, and no paid placement.</b> This site does "
           "not carry advertising today. If that changes it will be said here "
           "first, and the rule will not: advertising never buys a mention, a "
           "ranking or a number. Ad slots are ad slots; nothing an advertiser "
           "pays for appears inside a calculator, a comparison or a "
           "recommendation.")

WITH = ("<b>No sponsored content, and no paid placement.</b> This site carries "
        "advertising, and advertising never buys a mention, a ranking or a "
        "number. Ad slots are ad slots; nothing an advertiser pays for appears "
        "inside a calculator, a comparison or a recommendation.")

# Everything this pass will recognise as its own sentence, so it can replace
# whichever one is there without depending on which run wrote it.
KNOWN = [
    WITHOUT, WITH,
    ("<b>No sponsored content, and no paid placement.</b> This site carries "
     "advertising, and advertising never buys a mention, a ranking or a "
     "number. Ad slots are ad slots; nothing an advertiser pays for appears "
     "inside a calculator, a comparison or a recommendation."),
]

LI = re.compile(r"<li><b>No sponsored content, and no paid placement\.</b>"
                r"[\s\S]*?</li>")


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return out


def serving_ads():
    """Does the site, in fact, serve advertising? Ask the files, not the flag."""
    found = []
    for rel in pages():
        s = open(os.path.join(SITE, rel), encoding="utf-8").read().lower()
        for sig in AD_SIGNATURES:
            if sig in s:
                found.append((rel, sig))
    return found


def main():
    if not os.path.exists(PAGE):
        sys.exit("ads_state: affiliate-disclosure.html is not there")

    observed = serving_ads()
    print("ad-network signatures found on the site: %d" % len(observed))
    for rel, sig in observed[:8]:
        print("  %s  %s" % (rel, sig))

    # The whole point: the flag has to agree with the site.
    if bool(observed) != CARRIES_ADS:
        sys.exit(
            "\nCARRIES_ADS is %s but the site %s ad-network code.\n"
            "  Either flip the constant at the top of _dev/ads_state.py, or "
            "work out why that code is (or is not) there.\n"
            "  The disclosure page is not allowed to disagree with the site."
            % (CARRIES_ADS, "does serve" if observed else "serves no"))

    s = open(PAGE, encoding="utf-8").read()
    orig = s
    want = WITH if CARRIES_ADS else WITHOUT

    m = LI.search(s)
    if not m:
        sys.exit("ads_state: the 'No sponsored content' bullet is not where it "
                 "was - re-read the page rather than letting this half-apply")
    current = m.group(0)[len("<li>"):-len("</li>")]
    if current.strip() == want:
        print("\nthe sentence already matches the fact")
    else:
        if current.strip() not in [k.strip() for k in KNOWN]:
            print("\n  note: replacing a sentence this pass did not write:")
            print("  %s" % current.strip()[:160])
        s = s[:m.start()] + "<li>" + want + "</li>" + s[m.end():]
        open(PAGE, "w", encoding="utf-8").write(s)
        print("\nrewritten for CARRIES_ADS = %s" % CARRIES_ADS)

    # ------------------------------------------------------------- guards
    s = open(PAGE, encoding="utf-8").read()
    bad = 0
    if want not in s:
        print("GUARD: the sentence did not land")
        bad += 1
    other = WITH if not CARRIES_ADS else WITHOUT
    if other in s:
        print("GUARD: both versions of the sentence are on the page")
        bad += 1
    # The retired promise must not come back.
    for gone in ("no advertising, ever", "This site will never carry",
                 "never carry advertising", "and never will"):
        if gone.lower() in s.lower():
            print("GUARD: the retired promise %r has reappeared" % gone)
            bad += 1
    # And the claim must still match the site after the write.
    if bool(serving_ads()) != CARRIES_ADS:
        print("GUARD: the site and the flag disagree")
        bad += 1
    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean - the disclosure page and the site agree")


if __name__ == "__main__":
    main()
