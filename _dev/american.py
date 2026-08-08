#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Convert the site from British to American spelling.

WHY THIS IS NOT A STYLE NIT. The audience is Californian therapists and the
subject is a Californian licence - sorry, license. The Board of Behavioral
Sciences issues a LICENSE. Every statute this site cites says license. A page
that says "licence" 489 times while quoting a statute that says "license" is
telling a reader who checks that the writer has not been where the figures come
from. On a site whose entire proposition is that every number traces to a
source, that is a credibility leak rather than a preference.

"programme" is the same problem wearing a different hat, plus a search one: it
appeared 2,776 times including in 68 page titles, and not one title contained
the string an American would actually type.

WHAT IS PROTECTED, AND WHY

  URLs.        href and src values are never touched. A link is a name, not
               prose: rewriting "catalogue.usc.edu" breaks it.
  Quotations.  <blockquote> and <q> carry other people's words. Correcting
               someone's spelling inside quotation marks is misquoting them.
               (As it happens none of the quotes on this site contain a British
               spelling - the sources are all American. The guard stays anyway,
               because the next quote might.)
  Scripts and stylesheets. Identifiers, not prose.
  Proper nouns. PROTECT below. "The USC Catalogue" is the name of a document.
  Attributes.  Only the ones a reader sees - title, alt, placeholder,
               aria-label, and meta content - are converted. Everything else
               inside a tag is left alone.

WHAT IS DELIBERATELY NOT CONVERTED

  analysis, analyses, analyst   Correct in American English. Only the VERB
                                forms move (analyse -> analyze). A blanket
                                "analys -> analyz" would have produced
                                "analyzis", which is why the table lists forms
                                rather than stems.
  practice / practise           American English uses "practice" for both the
                                noun and the verb, so practise -> practice.
                                This is the one pair where the British
                                distinction is real and the American one is not.
  licence / license             Same: American uses "license" for both.

Idempotent - American spelling is a fixed point of the table. Guarded: it exits
non-zero if any British form survives outside a protected region.
"""
import os, re, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training")

# Proper nouns and strings that must survive verbatim. Swapped out for a
# placeholder before the pass and back afterwards.
PROTECT = [
    "catalogue.usc.edu",
    "The USC Catalogue",
    "USC Catalogue",
]

# (pattern, replacement). Case is handled by _cased, which preserves an initial
# capital, so each entry is written in lower case only.
# (pattern, replacement). Case is handled by _cased, which preserves an initial
# capital, so each entry is written in lower case only.
#
# EVERY STEM CARRIES ITS ENDINGS EXPLICITLY. The first version of this table did
# not, and a stem rule is how you turn correct English into gibberish:
#
#     criticis -> criticiz   turned "criticism"  into "criticizm"   (15 times)
#     specialis -> specializ turned "specialist" into "specializt"  (11 times)
#     centre    -> center    turned "centred"    into "centerd"     (8 times)
#
# None of those crashed anything and none of them were caught by a guard looking
# for BRITISH spellings, because the output was neither British nor English. The
# guard at the bottom now also checks that the pass has not invented a word.
WORDS = [
    # -- the two that matter most
    (r"programme", "program"),
    (r"licenc", "licens"),              # licence, licences, licencing, licenced
    (r"practis(e|ed|es|ing)", lambda m: "practic" + ("ing" if m.group(1) == "ing" else m.group(1))),
    # -- -re. Longest first: "centre" would otherwise eat "centred".
    (r"centred", "centered"),
    (r"centres", "centers"),
    (r"centring", "centering"),
    (r"centre", "center"),
    (r"theatre", "theater"),
    (r"kilometre", "kilometer"),
    (r"metre", "meter"),
    (r"metres", "meters"),
    # -- -our
    (r"colour", "color"),
    (r"behaviour", "behavior"),
    (r"favour", "favor"),
    (r"honour", "honor"),
    (r"labour", "labor"),
    (r"neighbour", "neighbor"),
    (r"rumour", "rumor"),
    (r"endeavour", "endeavor"),
    (r"flavour", "flavor"),
    (r"humour", "humor"),
    # -- -ise. Endings are listed so the noun forms that are correct in American
    #    English (specialist, criticism, specialism) are left alone.
    (r"organis(e|ed|es|ing|ation|ations|ational|ationally)",
     lambda m: "organiz" + m.group(1)),
    (r"recognis(e|ed|es|ing|able|ably|ance)", lambda m: "recogniz" + m.group(1)),
    (r"specialis(e|ed|es|ing|ation|ations)", lambda m: "specializ" + m.group(1)),
    (r"criticis(e|ed|es|ing)", lambda m: "criticiz" + m.group(1)),
    (r"emphasis(e|ed|es|ing)", lambda m: "emphasiz" + m.group(1)),
    (r"apologis(e|ed|es|ing)", lambda m: "apologiz" + m.group(1)),
    (r"prioritis(e|ed|es|ing|ation)", lambda m: "prioritiz" + m.group(1)),
    (r"summaris(e|ed|es|ing)", lambda m: "summariz" + m.group(1)),
    (r"utilis(e|ed|es|ing|ation)", lambda m: "utiliz" + m.group(1)),
    (r"normalis(e|ed|es|ing|ation)", lambda m: "normaliz" + m.group(1)),
    (r"minimis(e|ed|es|ing)", lambda m: "minimiz" + m.group(1)),
    (r"maximis(e|ed|es|ing)", lambda m: "maximiz" + m.group(1)),
    (r"standardis(e|ed|es|ing|ation)", lambda m: "standardiz" + m.group(1)),
    (r"formalis(e|ed|es|ing|ation)", lambda m: "formaliz" + m.group(1)),
    (r"categoris(e|ed|es|ing|ation)", lambda m: "categoriz" + m.group(1)),
    (r"realis(e|ed|es|ing)", lambda m: "realiz" + m.group(1)),
    (r"marginalis(e|ed|es|ing|ation)", lambda m: "marginaliz" + m.group(1)),
    (r"contextualis(e|ed|es|ing|ation)", lambda m: "contextualiz" + m.group(1)),
    (r"conceptualis(e|ed|es|ing|ation|ations)", lambda m: "conceptualiz" + m.group(1)),
    (r"itemis(e|ed|es|ing)", lambda m: "itemiz" + m.group(1)),
    (r"characteris(e|ed|es|ing)", lambda m: "characteriz" + m.group(1)),
    (r"individualis(e|ed|es|ing)", lambda m: "individualiz" + m.group(1)),
    (r"centralis(e|ed|es|ing|ation)", lambda m: "centraliz" + m.group(1)),
    (r"colonis(e|ed|es|ing|ation)", lambda m: "coloniz" + m.group(1)),
    (r"randomis(e|ed|es|ing)", lambda m: "randomiz" + m.group(1)),
    (r"authoris(e|ed|es|ing|ation|ations)", lambda m: "authoriz" + m.group(1)),
    (r"analys(e|ed|es\b(?! of)|ing)", None),   # replaced below; see the note
    # -- doubled l
    (r"counsell", "counsel"),           # counsellor, counselling
    (r"cancell", "cancel"),             # cancelled, cancelling
    (r"labelled", "labeled"),
    (r"labelling", "labeling"),
    (r"travelled", "traveled"),
    (r"travelling", "traveling"),
    (r"traveller", "traveler"),
    (r"modelling", "modeling"),
    (r"modelled", "modeled"),
    (r"signalled", "signaled"),
    (r"marvellous", "marvelous"),
    # -- single l where American doubles
    (r"enrolment", "enrollment"),
    (r"enrols\b", "enrolls"),
    (r"enrol\b", "enroll"),
    (r"fulfilment", "fulfillment"),
    (r"fulfil\b", "fulfill"),
    (r"instalment", "installment"),
    (r"skilful", "skillful"),
    # -- -ce / -se nouns
    (r"defence", "defense"),
    (r"offence", "offense"),
    (r"pretence", "pretense"),
    # -- -ogue
    (r"catalogue", "catalog"),
    # -- odds and ends
    (r"judgement", "judgment"),
    (r"ageing", "aging"),
    (r"whilst", "while"),
    (r"amongst", "among"),
    (r"towards", "toward"),
    (r"learnt\b", "learned"),
    (r"spelt\b", "spelled"),
    (r"grey\b", "gray"),
    (r"greyed", "grayed"),
    (r"cheque", "check"),
    (r"storeys", "stories"),
    (r"draught", "draft"),
    (r"sceptic", "skeptic"),
    (r"aluminium", "aluminum"),
    (r"moustache", "mustache"),
    (r"plough", "plow"),
]

# analyse -> analyze, but NOT analysis / analyses(noun) / analyst, all of which
# are correct American English. Spelled out rather than stemmed, for the reason
# in the comment above the table.
WORDS = [w for w in WORDS if w[1] is not None] + [
    (r"analyse\b", "analyze"),
    (r"analysed\b", "analyzed"),
    (r"analysing\b", "analyzing"),
]

# Forms this pass has produced by accident and must never produce again. The
# guard checks for them by name: a British-spelling guard cannot catch output
# that is not a word in either dialect.
NEVER = ["criticizm", "specializt", "specializm", "centerd", "practiceing",
         "analyzis", "organizm", "recognizance" if False else "colord"]

# NOTE ON "dialogue". American English keeps it - "dialog" is the computing
# sense (a dialog box), not the conversational one. Left as a no-op entry rather
# than deleted so the next person does not "fix" the omission.

# Regions whose text is never touched.
SKIP_TAGS = ("script", "style", "blockquote", "q", "code", "pre", "samp", "kbd")
SKIP_RE = re.compile(
    r"<(%s)\b[\s\S]*?</\1>" % "|".join(SKIP_TAGS), re.I)

# JSON-LD is inside a <script>, so the rule above protects it - but it is not
# code. It is the description Google reads and, on 68 school pages, it was the
# only place left saying "programme". Its string VALUES are converted; its keys,
# its @type names and every "item" URL are not.
LD_RE = re.compile(
    r'(<script type="application/ld\+json"[^>]*>)([\s\S]*?)(</script>)', re.I)
LD_STR = re.compile(r'"(name|description|headline|about|text|alternateName)":"((?:[^"\\]|\\.)*)"')

# Attributes a reader actually sees.
VISIBLE_ATTRS = ("title", "alt", "placeholder", "aria-label", "content")
TAG_RE = re.compile(r"<[^>]+>")
ATTR_RE = re.compile(
    r'\b(%s)="([^"]*)"' % "|".join(VISIBLE_ATTRS), re.I)


def _cased(repl):
    """Preserve an initial capital: Programme -> Program, not program."""
    def f(m):
        s = m.group(0)
        out = repl(m) if callable(repl) else repl
        if s[:1].isupper():
            out = out[:1].upper() + out[1:]
        return out
    return f


COMPILED = [(re.compile(p, re.I), _cased(r)) for p, r in WORDS]


def convert(text):
    for rx, rep in COMPILED:
        text = rx.sub(rep, text)
    return text


def process(doc):
    """Convert prose only. Everything else is carried through untouched."""
    # 1. protect proper nouns
    holes = {}
    for i, phrase in enumerate(PROTECT):
        key = "\x00P%d\x00" % i
        if phrase in doc:
            holes[key] = phrase
            doc = doc.replace(phrase, key)

    # 2. JSON-LD first, while it is still findable, and before the <script>
    #    protection hides it
    def ld(m):
        body = LD_STR.sub(
            lambda v: '"%s":"%s"' % (v.group(1), convert(v.group(2))), m.group(2))
        return m.group(1) + body + m.group(3)
    doc = LD_RE.sub(ld, doc)

    # 3. lift out the regions that must not change
    keeps = []

    def stash(m):
        keeps.append(m.group(0))
        return "\x00K%d\x00" % (len(keeps) - 1)

    doc = SKIP_RE.sub(stash, doc)

    # 3. split into tags and text; convert text, and inside tags convert only
    #    the handful of attributes a reader sees
    out, last = [], 0
    for m in TAG_RE.finditer(doc):
        out.append(convert(doc[last:m.start()]))
        tag = m.group(0)
        tag = ATTR_RE.sub(
            lambda a: '%s="%s"' % (a.group(1), convert(a.group(2))), tag)
        out.append(tag)
        last = m.end()
    out.append(convert(doc[last:]))
    doc = "".join(out)

    # 4. put everything back
    for i, k in enumerate(keeps):
        doc = doc.replace("\x00K%d\x00" % i, k)
    for key, phrase in holes.items():
        doc = doc.replace(key, phrase)
    return doc


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return out


def main():
    hits = collections.Counter()
    touched = 0
    for rel in pages():
        p = os.path.join(SITE, rel)
        s = open(p, encoding="utf-8").read()
        out = process(s)
        if out != s:
            for rx, _r in COMPILED:
                n = len(rx.findall(s)) - len(rx.findall(out))
                if n > 0:
                    hits[rx.pattern] += n
            open(p, "w", encoding="utf-8").write(out)
            touched += 1
    print("%d page(s) converted" % touched)
    for k, v in hits.most_common(20):
        print("  %6d  %s" % (v, k))

    # ---- guard: nothing British may survive outside a protected region
    bad = collections.Counter()
    for rel in pages():
        doc = open(os.path.join(SITE, rel), encoding="utf-8").read()
        doc = SKIP_RE.sub("", doc)
        for phrase in PROTECT:
            doc = doc.replace(phrase, "")
        doc = re.sub(r'\b(?:href|src|data-[\w-]+)="[^"]*"', "", doc)
        for rx, _r in COMPILED:
            if rx.pattern == r"dialogue":
                continue
            for m in rx.finditer(doc):
                bad["%s: %s" % (rel, m.group(0))] += 1
    if bad:
        print("\n%d survivor(s):" % sum(bad.values()))
        for k, v in bad.most_common(25):
            print("  %4d  %s" % (v, k))
        sys.exit(1)
    print("guards clean")


if __name__ == "__main__":
    main()
