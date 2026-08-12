#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Retire the "no account, no sign-up, no server" claim across the site.

WHY. It is the third promise this site has had to narrow, and the pattern is
always the same: a claim that was true when it was written, repeated into the
footer of every page, and then quietly falsified by something the site went on
to do. "Not selling anything" went when the first affiliate link shipped. This
one goes now, on the same principle and before rather than after.

The site's whole proposition is that every figure is computed or cited. A stale
promise in the chrome of 121 pages is worth less than the promise costs.

WHAT REPLACES IT. Not silence, and not a weaker version of the same promise -
those age the same way. The replacement describes what a reader can verify from
the page in front of them: the calculators run in the browser and the numbers
travel in the link. That is a statement about how the tool works, not an
undertaking about how the site will always be operated.

TWO CATEGORIES, HANDLED DIFFERENTLY.

  Marketing copy - footers, heroes, meta descriptions, promise blocks - loses
  the claim entirely.

  privacy.html and terms.html are different. A privacy policy that simply
  deletes its description of data handling is worse than one that overstates
  it. Those keep a factual, present-tense description scoped to the calculators,
  with no forward-looking undertaking.

Idempotent, and guarded: the pass fails if any retired phrasing survives
anywhere, and it will not run twice into a double replacement.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training", "for")

# (old, new). Ordered longest-first so a short phrase cannot eat a long one it
# happens to be contained in.
SWAPS = [
    # ---- the global footer, on every page
    ("<b>Built by Cavatello.</b> Free to use, no account, nothing stored. Some links out",
     "<b>Built by Cavatello.</b> Some links out"),

    # ---- privacy and terms: keep a factual description, drop the undertaking
    ("No account, and nothing you type into a calculator is sent anywhere. Your setup "
     "lives in the address bar of your",
     "What you type into a calculator is held in the page and written into the "
     "address bar of your"),
    ("The calculators on this Site have no account, no login and no database.",
     "The calculators on this Site run in your browser."),
    ("there is no account and no server, and what you type stays in your browser and "
     "in the address bar",
     "what you type is held in your browser and in the address bar"),
    ("This site is free, stores nothing you type, and is not advice.",
     "This site is free and is not advice."),

    # ---- home page promise block
    ("<h3>Nothing saved, no account</h3>", "<h3>How the calculators work</h3>"),
    ("No account, no email required, nothing stored on a server. Your numbers live in "
     "the page and in a link you can copy.",
     "The calculators run in your browser, and your numbers travel in a link you "
     "can copy."),
    ("<b>Nothing is saved</b>", "<b>Your numbers stay in the link</b>"),
    ("No account, no sign-up, no server. What you type stays in the page. Close the "
     "tab and it is gone.",
     "What you type is written into the address bar, so a bookmark keeps your "
     "setup and a link carries it to someone else."),
    ("Shareable by link, nothing saved", "Shareable by link"),

    # ---- tool heroes
    # Two pages use a literal em-dash where the others use the entity, and one
    # ends the sentence rather than continuing it. Both variants have to be
    # listed: a swap table matches bytes, not meaning.
    ("Nothing is saved and there is no account \u2014 your setup lives in the address "
     "bar, so bookmarking this page keeps it.",
     "Your setup lives in the address bar, so bookmarking this page keeps it."),
    ("Nothing is saved and there is no account \u2014 your setup lives in the address "
     "bar.",
     "Your setup lives in the address bar."),
    ("Nothing is saved and there is no account &mdash; your setup lives in the address "
     "bar, so bookmarking this page keeps it.",
     "Your setup lives in the address bar, so bookmarking this page keeps it."),
    ("Nothing is saved and there is no account. Your setup lives in the ",
     "Your setup lives in the "),
    ("Nothing is saved and nothing is sent &mdash; your setup lives in the link,",
     "Your setup lives in the link,"),
    ("Free, nothing saved", "Free to use"),

    # ---- calculators index
    ("All of them run entirely in your browser: nothing you type is stored, nothing is "
     "sent anywhere, and there is no account.",
     "All of them run in your browser, and your figures travel in the address bar "
     "rather than anywhere else."),
    ("Nothing stored, nothing sent.", "Every figure traces to a published rate."),

    # ---- meta descriptions and structured data
    ("Nothing saved, no account.", "Every figure traces to a published rate."),
    ("Free, nothing saved.", "Free to use."),

    # ---- the second sweep, 7 August
    # The first pass listed the phrasings it could see. These four were on live
    # pages and in one generated string inside a script, and survived because a
    # swap table matches bytes and nobody had written down the bare form of the
    # claim. The RETIRED guard now carries "Nothing is saved" on its own, which
    # is what surfaced them - so the lesson is that the guard should describe
    # the CLAIM and the table should describe the phrasings, and the first pass
    # had both describing phrasings.
    ("&middot; five minutes &middot; nothing is saved",
     "&middot; five minutes"),
    ("&middot; free &middot; nothing is saved", "&middot; free"),
    # The backslash is literal: this sits inside a JavaScript string in the page,
    # written as an escape sequence rather than as the character itself, so the
    # swap must match the six bytes and not the middot they stand for. Using a
    # plain literal here silently matched nothing.
    (r"takes about five minutes \u00B7 nothing is saved",
     "takes about five minutes"),
    ("Everything below is computed from them &mdash; nothing is saved, and your "
     "setup lives in the address bar.",
     "Everything below is computed from them, and your setup lives in the "
     "address bar."),
    ("Nothing is saved &mdash; your setup lives in the address bar, so a",
     "Your setup lives in the address bar, so a"),
    ("Nothing is saved anywhere.", "Your setup lives in the address bar."),
]

# Anything matching these must not survive the pass anywhere on the site.
RETIRED = [
    r"no account, no sign-?up",
    r"nothing stored on a server",
    r"there is no account",
    r"no account, no login and no database",
    r"Nothing saved, no account",
    r"nothing you type is stored",
    r"stores nothing you type",
    r"Free to use, no account, nothing stored",
    # Caught on the cost-of-living rebuild: this page is generated by a builder
    # that lives outside the site tree, so it never saw the original swap and
    # shipped the retired claim back in. A guard that only knows the phrasings
    # present when it was written cannot catch that; this one is the bare claim.
    r"\bNothing is saved\b",
]


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return out


def main():
    hits = {}
    changed = 0
    for f in pages():
        path = os.path.join(SITE, f)
        s = open(path, encoding="utf-8").read()
        before = s
        for old, new in SWAPS:
            n = s.count(old)
            if n:
                s = s.replace(old, new)
                hits[old[:44]] = hits.get(old[:44], 0) + n
        if s != before:
            open(path, "w", encoding="utf-8").write(s)
            changed += 1

    for k in sorted(hits, key=lambda x: -hits[x]):
        print("%5d  %s" % (hits[k], k))
    print("%d page(s) rewritten" % changed)

    bad = 0
    for f in pages():
        s = open(os.path.join(SITE, f), encoding="utf-8").read()
        for pat in RETIRED:
            m = re.search(pat, s, re.I)
            if m:
                print("GUARD %s: retired claim survives - %r"
                      % (f, s[max(0, m.start() - 40):m.end() + 40]
                         .replace("\n", " ")))
                bad += 1
        # A replacement applied twice would read as a stutter and is the usual
        # failure mode of a string-swap pass run without a marker.
        if "Your setup lives in the address bar, so bookmarking this page keeps " \
           "it. Your setup lives" in s:
            print("GUARD %s: replacement applied twice" % f)
            bad += 1
    if bad:
        sys.exit("claims: %d guard failure(s)" % bad)
    print("guards clean")


if __name__ == "__main__":
    main()
