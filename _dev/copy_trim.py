#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Retire two pieces of chrome copy that were repeated on every page.

WHAT GOES, AND WHY

1. THE AFFILIATE SENTENCE. "Some links out to third-party services are
   affiliate links and are tagged where they appear; they cost you nothing and
   never change what a calculator here tells you." It was in the footer of 135
   pages. Asked for three times; removed here.

   The DEDICATED PAGE STAYS. affiliate-disclosure.html keeps its own body copy
   and keeps its footer link, because the disclosure is a real obligation and a
   site that removes the sentence AND the page has removed the disclosure, not
   the repetition. What was asked for was the repetition.

2. THE "YOUR NUMBERS TRAVEL IN THE LINK" FRAMING. Same problem as the claim it
   replaced in claims.py: it describes a mechanism rather than a benefit, it is
   the third thing said in a hero before the reader has seen a number, and it
   invites the follow-up question ("so is it saved or not?") that the sentence
   exists to avoid. It comes out of the heroes, the promise blocks and the "How
   it works" list. Nothing replaces it in the heroes - a hero note that says
   less is shorter, which is the point.

   privacy.html and terms.html are UNTOUCHED. They describe data handling as a
   matter of record; removing that description to tidy the marketing copy would
   make the policy less accurate, which is the opposite trade to the one being
   made here.

Idempotent. Run it twice and the second run reports nothing to do, and it
guards: it exits non-zero if a retired phrase survives on any page it owns.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training")

AFF_LONG = ("Some links out to third-party services are affiliate links and are "
            "tagged where they appear; they cost you nothing and never change "
            "what a calculator here tells you. ")
AFF_SHORT = (" A few links out to third-party services are affiliate links, "
             "tagged where they appear &mdash; they never change what a "
             "calculator here tells you.")

# (old, new). Plain byte swaps. Ordered longest-first so a short phrase cannot
# eat a longer one that contains it.
SWAPS = [
    (AFF_LONG, ""),
    (AFF_SHORT, ""),

    # ---- hero notes: the sentence goes, the sentence around it survives
    ("Six numbers for the week you work now, and four for what is already "
     "signed off. Your setup lives in the address bar, so a bookmark keeps it.",
     "Six numbers for the week you work now, and four for what is already "
     "signed off."),
    (" <b>Your setup lives in the address bar.</b>", ""),
    ("A projection, not a forecast. Your setup lives in the address bar, so "
     "bookmarking this page keeps it.",
     "A projection, not a forecast."),
    ("Arrived from the simulator? Your rate, caseload and costs came with you. "
     "Your setup lives in the address bar.",
     "Arrived from the simulator? Your rate, caseload and costs came with you."),
    ("Four numbers. Everything below is computed from them, and your setup "
     "lives in the address bar.",
     "Four numbers. Everything below is computed from them."),
    ("Housing, transport, food and medical <b>by county</b>; <b>RAP, IBR and "
     "PSLF</b> for the loan. Your figures travel in the link.",
     "Housing, transport, food and medical <b>by county</b>; <b>RAP, IBR and "
     "PSLF</b> for the loan."),

    # ---- promise and index copy
    ("All free, and every figure traceable to the rule or schedule it came "
     "from. Your setup lives in the link, so you can save it, share it or send "
     "it to your accountant without an account existing anywhere.",
     "All free, and every figure traceable to the rule or schedule it came "
     "from."),
    ("No account, no database. Your setup lives in the link, which is also how "
     "you share it.",
     "No account and no database. Nothing you type is sent anywhere."),
    ("All of them run in your browser, and your figures travel in the address "
     "bar rather than anywhere else. Every figure they produce traces back to "
     "a published rate, limit or statute that is linked from the tool itself.",
     "Every figure they produce traces back to a published rate, limit or "
     "statute that is linked from the tool itself."),
    ("<li>Shareable by link</li>",
     "<li>Break-even, and what one more client adds</li>"),

    # ---- the home page promise card that was ABOUT the mechanism
    ("<h3>How the calculators work</h3><p>The calculators run in your browser, "
     "and your numbers travel in a link you can copy.",
     "<h3>Updated when the rules move</h3><p>2026 federal and California rates, "
     "each one carrying the date it was last checked against its source. When "
     "a threshold moves, the change is listed on the "
     "<a href=\"changes.html\">What changed</a> page rather than quietly "
     "swapped in."),

    # ---- hero deck
    ("Your own numbers, nothing saved.", "Your own numbers, worked properly."),

    # ---- practice-simulator.html. The <p> wraps across a newline in the
    # source, so the swap has to carry the newline and the indentation with it;
    # a single-line literal matches nothing here and fails silently.
    ('    <p class="anote">Your setup lives in the link,\n'
     '    which is also how you share it.</p>\n', ""),
    # The same claim in the meta description and in the JSON-LD, where it is
    # the sentence Google shows under the result.
    ("No account, nothing saved.", "Every figure traces to a published rate."),
]

# The two "How it works" bullets on the home page. Both said the same thing,
# which is its own argument for removing them.
LI_KILL = [
    "<b>Your numbers stay in the link</b>",
    "<b>Your numbers travel in a link</b>",
]
LI_NEW = (
    "<li><div><b>Nothing on the page is illustrative</b>"
    "<span>There are no worked examples standing in for your practice. Every "
    "dollar shown is computed from a figure you entered.</span></div></li>"
    "<li><div><b>California, not a state dropdown</b>"
    "<span>Its own income tax schedule, its own franchise tax, and its own rule "
    "that a licensed therapist may not form an LLC.</span></div></li>"
)

RETIRED = [
    "affiliate links and are tagged where they appear",
    "affiliate links, tagged where they appear",
    "lives in the address bar",
    "travel in a link",
    "travel in the link",
    "stay in the link",
    "lives in the link",
    "Shareable by link",
    "nothing saved",
]

# Pages that are ALLOWED to keep the retired phrasings, and why.
EXEMPT = {
    "affiliate-disclosure.html": "the disclosure itself",
    "privacy.html": "a factual description of data handling",
    "terms.html": "a factual description of data handling",
    "tycoon.html": "belongs to another workstream",
}


def pages():
    out = []
    for f in sorted(os.listdir(SITE)):
        if f.endswith(".html"):
            out.append(f)
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return out


def kill_li(s):
    """Remove each <li> whose <b> is one of LI_KILL, and add the replacements
    once. Located by the <b>, then widened to the enclosing <li>...</li>, so it
    survives whitespace changes inside the item."""
    n = 0
    for mark in LI_KILL:
        while True:
            i = s.find(mark)
            if i < 0:
                break
            a = s.rfind("<li>", 0, i)
            b = s.find("</li>", i)
            if a < 0 or b < 0:
                break
            s = s[:a] + s[b + len("</li>"):]
            n += 1
    if n and "Nothing on the page is illustrative" not in s:
        j = s.find('<ul class="lhow">')
        if j >= 0:
            j += len('<ul class="lhow">')
            s = s[:j] + LI_NEW + s[j:]
    return s, n


def kill_lwhy(s):
    """Remove the 'Four questions nobody covered in grad school' section.

    Located by its inner div, then widened to the enclosing <section>. There is
    no nested <section> inside it, so the first closing tag after it is the
    right one - checked, not assumed."""
    i = s.find('<div class="lwrap lwhy">')
    if i < 0:
        return s, 0
    a = s.rfind("<section", 0, i)
    b = s.find("</section>", i)
    if a < 0 or b < 0:
        return s, 0
    inner = s[a:b]
    if inner.count("<section") != 1:
        sys.exit("kill_lwhy: nested <section> - refusing to guess the boundary")
    return s[:a] + s[b + len("</section>"):], 1


def main():
    touched, swaps = 0, 0
    for rel in pages():
        p = os.path.join(SITE, rel)
        try:
            s = open(p, encoding="utf-8").read()
        except (IOError, UnicodeDecodeError):
            continue
        orig = s
        if os.path.basename(rel) not in EXEMPT:
            for old, new in SWAPS:
                if old in s:
                    swaps += s.count(old)
                    s = s.replace(old, new)
        if rel == "index.html":
            s, n = kill_li(s)
            swaps += n
            s, n = kill_lwhy(s)
            swaps += n
        # A footer sentence that now begins with a space, or a <p> that starts
        # with one, is what a blind byte-swap leaves behind.
        s = s.replace("</b>  ", "</b> ").replace("<p> ", "<p>")
        s = re.sub(r"\s+</p>", "</p>", s)
        if s != orig:
            open(p, "w", encoding="utf-8").write(s)
            touched += 1
            print("  %s" % rel)

    print("\n%d swap(s) across %d page(s)" % (swaps, touched))

    bad = 0
    for rel in pages():
        base = os.path.basename(rel)
        if base in EXEMPT:
            continue
        s = open(os.path.join(SITE, rel), encoding="utf-8").read()
        for phrase in RETIRED:
            if phrase in s:
                print("GUARD %s: %r survives" % (rel, phrase))
                bad += 1
    if bad:
        sys.exit("\n%d survivor(s) - fix the swap table, do not let this ship"
                 % bad)
    print("guards clean")


if __name__ == "__main__":
    main()
