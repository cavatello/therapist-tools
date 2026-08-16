#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rollout step 5, family 5: every remaining skinned page goes bc2.

Family 4 (16 Aug): the interactive tools -> body.bct + css/house-tool.css

The three earlier families converted by REPLACING their CSS wholesale,
because a family sheet could restyle their whole vocabulary. The tools
cannot convert that way: each carries a real application (the simulator,
the advisor, the hours calculator...) whose extracted app sheets and
inline style blocks hold hundreds of layout rules nobody should re-type.
So this family converts by SUBTRACTION AND RE-GROUNDING instead:

  1. drop exactly the legacy sheets that css/house-chrome.css replicates
     (derived at runtime from its own "from css/XXXX.css" markers - the
     list maintains itself), plus the house-skin link and any stray house
     links. THE APP'S OWN HASH SHEETS AND INLINE <style> BLOCKS STAY.
  2. add, right after the fonts link and before the app sheets:
         css/house.css?v=<hash>          tokens + element rules (.bc2)
         css/house-chrome.css?v=<hash>   the shared chrome
         css/house-tool.css?v=<hash>     this family's re-grounding
     house-tool.css is the set of house-skin rules that touched tool-app
     vocabulary, ported verbatim with body.house -> body.bct (and the
     token block restated, since the skin carried it) - so a converted
     page looks exactly as it did skinned, minus the flash of unstyled
     old design, because the replicated chrome no longer loads at all.
  3. <body class="..."> gains bc2 + bct + house.

MEMBERSHIP IS A LIST, not a marker: the tools share no wrapper class.
finding-a-clinical-supervisor-california.html sits here rather than in
family 2 because it embeds the advisor app (family_pk.py's own note).

GUARDS: no replicated-chrome sheet remains; no skin link; exactly three
house links; the fonts request survives; at least one app sheet remains
on pages that had one (dropping a tool's own CSS is the catastrophic
failure mode here); body carries bc2/bct/house exactly once each.

USAGE
    python3 _dev/family_rest.py           convert/refresh
    python3 _dev/family_rest.py --check   verify only

Idempotent. ship.py runs it in LAST after house_swap (which re-skins
these pages every run - this pass undoes that), family_art and family_pk
(both of whose sweeps must skip body.bct, via FAMILY_CLASSES).
"""
import hashlib, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)

CLS = "bcz"
SHEET = "house-rest.css"
PAGES = [
    "about.html",
    "affiliate-disclosure.html",
    "associate-therapist-pay-los-angeles-bay-area.html",
    "become-an-mft-california.html",
    "changes.html",
    "concepts.html",
    "contact.html",
    "discipline-case-a-battery-conviction-and-a-default.html",
    "discipline-case-a-decade-of-employer-warnings.html",
    "discipline-case-a-felony-assault-and-a-default.html",
    "discipline-case-a-forty-year-license-surrendered.html",
    "discipline-case-a-mandated-report-never-filed.html",
    "discipline-case-almost-forty-years-of-rehabilitation.html",
    "discipline-case-asking-a-client-where-to-buy-drugs.html",
    "discipline-case-billed-for-sessions-that-never-happened.html",
    "discipline-case-cannabis-with-a-client.html",
    "discipline-case-charged-without-a-conviction.html",
    "discipline-case-denied-it-then-admitted-it.html",
    "discipline-case-discipline-follows-your-other-license.html",
    "discipline-case-disciplined-for-emails.html",
    "discipline-case-drinking-at-lunch.html",
    "discipline-case-eight-weeks-without-a-therapist.html",
    "discipline-case-eight-years-of-escalation.html",
    "discipline-case-embezzlement-outside-the-practice.html",
    "discipline-case-failing-to-report-your-own-conviction.html",
    "discipline-case-falsified-course-certificates-end-a-probation.html",
    "discipline-case-felony-child-endangerment-never-reported.html",
    "discipline-case-forged-supervisor-signature.html",
    "discipline-case-four-ways-to-violate-probation.html",
    "discipline-case-from-dui-to-surrender.html",
    "discipline-case-ignoring-an-order-to-be-examined.html",
    "discipline-case-letting-a-registration-lapse-on-probation.html",
    "discipline-case-out-of-state-discipline.html",
    "discipline-case-probation-traded-for-surrender.html",
    "discipline-case-pseudonyms-and-sleepovers.html",
    "discipline-case-psychology-probation-reaches-a-second-license.html",
    "discipline-case-road-rage-and-a-default-revocation.html",
    "discipline-case-serious-felonies-ignore-the-seven-year-rule.html",
    "discipline-case-seven-business-practice-failures.html",
    "discipline-case-seven-years-under-supervision.html",
    "discipline-case-sex-with-a-residential-client.html",
    "discipline-case-signed-her-supervisors-name.html",
    "discipline-case-the-address-of-record.html",
    "discipline-case-the-custody-letter.html",
    "discipline-case-the-only-public-reproval.html",
    "discipline-case-the-slow-boil.html",
    "discipline-case-the-two-year-rule-is-not-a-loophole.html",
    "discipline-case-thirty-days-to-report-discipline.html",
    "discipline-case-thirty-four-year-sentence-then-registration.html",
    "discipline-case-three-days-after-the-last-session.html",
    "discipline-case-twenty-three-sessions-in-one-day.html",
    "discipline-case-two-duis-five-years-probation.html",
    "discipline-case-two-nursing-actions-before-registration.html",
    "discipline-case-underground-psychedelics-and-two-clients.html",
    "discipline-case-when-the-judge-cuts-the-bill.html",
    "getting-paid/index.html",
    "headway-for-california-therapists.html",
    "index.html",
    "licensure/index.html",
    "mft-programs-california.html",
    "mock/library/out/calculators.html",
    "mock/library/out/changes.html",
    "mock/library/out/getting-paid/index.html",
    "mock/library/out/licensure/index.html",
    "mock/library/out/money/index.html",
    "mock/library/out/practice/index.html",
    "mock/library/out/questions.html",
    "mock/library/out/resources.html",
    "mock/library/out/training/index.html",
    "money/index.html",
    "newsletter.html",
    "practice/index.html",
    "privacy.html",
    "psychedelic-therapy-training-california.html",
    "psychedelic-training-ciis-psychedelic-assisted-therapies.html",
    "psychedelic-training-ciis-psychedelic-studies-bs.html",
    "psychedelic-training-embody-lab-somatic-psychedelic.html",
    "psychedelic-training-fluence-training.html",
    "psychedelic-training-innertrek.html",
    "psychedelic-training-integrative-psychiatry-institute.html",
    "psychedelic-training-mind-foundation-apt.html",
    "psychedelic-training-naropa-psilocybin-facilitator.html",
    "psychedelic-training-pacifica-psychedelic.html",
    "psychedelic-training-polaris-insight-kap.html",
    "psychedelic-training-prati.html",
    "psychedelic-training-psychedelic-coalition-for-health.html",
    "psychedelic-training-soundmind-institute.html",
    "psychedelic-training-spiral-process-training.html",
    "psychedelic-training-uc-berkeley-bcsp.html",
    "psychedelic-training-vital-psychedelics-today.html",
    "psyd-programs-california.html",
    "questions.html",
    "resources.html",
    "simplepractice-california-therapists.html",
    "terms.html",
    "therapist-discipline-cases-california.html",
    "therapist-working-remotely-california.html",
    "therapy-liability-insurance-california.html",
    "training/index.html",
]
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training",
           "for")

SKIN_LINK = re.compile(
    r'[ \t]*<link rel="stylesheet" href="(?:\.\./)*css/house-skin\.css'
    r'(?:\?v=[0-9a-f]+)?">\n?')
HOUSE_LINKS = re.compile(
    r'[ \t]*<link rel="stylesheet" href="(?:\.\./)*css/house'
    r'(?:-art|-sc|-pk|-tool|-rest|-chrome)?\.css(?:\?v=[0-9a-f]+)?">\n?')
TOOL_SHEET = re.compile(
    r'[ \t]*<link rel="stylesheet" href="(?:\.\./)*css/house-rest\.css'
    r'(?:\?v=[0-9a-f]+)?">\n?')
HASH_LINK_ANY = re.compile(
    r'<link rel="stylesheet" href="(?:\.\./)*css/([0-9a-f]{12})\.css">')
BODY = re.compile(r"<body([^>]*)>")


def replicated_chrome():
    """The sheets house-chrome.css was extracted from, by its own markers."""
    s = open(os.path.join(SITE, "css", "house-chrome.css"),
             encoding="utf-8").read()
    names = set(re.findall(r'from css/([0-9a-f]{12})\.css', s))
    if len(names) < 5:
        sys.exit("family_rest: house-chrome.css markers name only %d "
                 "sheet(s) - the derivation is broken" % len(names))
    return names


def v(name):
    p = os.path.join(SITE, "css", name)
    return hashlib.sha1(open(p, "rb").read()).hexdigest()[:8]


def body_classes(s):
    m = BODY.search(s)
    cm = re.search(r'class="([^"]*)"', m.group(1)) if m else None
    return (cm.group(1).split() if cm else []), m


def check_page(rel, s, chrome, had_app):
    bad = []
    for name in HASH_LINK_ANY.findall(s):
        if name in chrome:
            bad.append("replicated chrome sheet %s.css still linked" % name)
    if SKIN_LINK.search(s):
        bad.append("house-skin still linked")
    n = len(HOUSE_LINKS.findall(s))
    if n != 3:
        bad.append("expected exactly 3 house sheets, found %d" % n)
    if "fonts.googleapis.com/css2" not in s:
        bad.append("fonts request missing")
    if had_app and not HASH_LINK_ANY.search(s):
        bad.append("ALL hash sheets gone - the app's own CSS was dropped")
    classes, _ = body_classes(s)
    for c in ("bc2", CLS, "house"):
        if classes.count(c) != 1:
            bad.append("body class %r count %d" % (c, classes.count(c)))
    return bad


def convert(rel, chrome):
    p = os.path.join(SITE, rel)
    s = open(p, encoding="utf-8").read()
    orig = s

    # drop only the replicated chrome sheets, keep the app's own
    def drop(m):
        return "" if m.group(1) in chrome else m.group(0)
    s = re.sub(r'[ \t]*<link rel="stylesheet" href="(?:\.\./)*css/'
               r'([0-9a-f]{12})\.css">\n?',
               lambda m: "" if m.group(1) in chrome else m.group(0), s)
    s = SKIN_LINK.sub("", s)
    s = HOUSE_LINKS.sub("", s)

    fonts = re.search(r'<link href="https://fonts\.googleapis\.com[^>]*>', s)
    if not fonts:
        return "NO FONTS LINK", s
    up = "../" * rel.count("/")
    links = "".join('\n<link rel="stylesheet" href="%scss/%s?v=%s">'
                    % (up, n, v(n))
                    for n in ("house.css", "house-chrome.css", SHEET))
    s = s[:fonts.end()] + links + s[fonts.end():]

    classes, m = body_classes(s)
    if m is None:
        return "NO BODY", s
    lead = ["bc2", CLS, "house"]
    for c in lead:
        if c not in classes:
            classes.append(c)
    order = lead + [c for c in classes if c not in lead]
    attrs = m.group(1)
    cm = re.search(r'class="([^"]*)"', attrs)
    new = 'class="%s"' % " ".join(order)
    attrs = attrs.replace(cm.group(0), new) if cm else attrs + " " + new
    s = s[:m.start()] + "<body%s>" % attrs + s[m.end():]

    changed = s != orig
    open(p, "w", encoding="utf-8").write(s)
    return ("converted" if changed else "already"), s


def sweep_borrowed(check_only):
    """Strip a borrowed house-tool link off any page that is not body.bct."""
    fixed, bad = 0, 0
    rels = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            rels += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                     if f.endswith(".html")]
    for rel in rels:
        p = os.path.join(SITE, rel)
        s = open(p, encoding="utf-8").read()
        classes, _ = body_classes(s)
        if CLS in classes:
            continue
        new = TOOL_SHEET.sub("", s)
        if new != s:
            if check_only:
                print("SWEEP %s: borrowed house-tool link present" % rel)
                bad += 1
            else:
                open(p, "w", encoding="utf-8").write(new)
                fixed += 1
    if fixed:
        print("  swept borrowed house-tool link off %d non-family page(s)"
              % fixed)
    return bad


def main():
    check_only = "--check" in sys.argv
    if not os.path.exists(os.path.join(SITE, "css", SHEET)):
        sys.exit("family_rest: css/%s is missing" % SHEET)
    chrome = replicated_chrome()
    failures = 0
    for rel in PAGES:
        p = os.path.join(SITE, rel)
        if not os.path.exists(p):
            print("MISSING %s" % rel); failures += 1; continue
        before = open(p, encoding="utf-8").read()
        had_app = any(n not in chrome
                      for n in HASH_LINK_ANY.findall(before))
        if check_only:
            s = before
            classes, _ = body_classes(s)
            if CLS not in classes:
                print("UNCONVERTED %s" % rel); failures += 1; continue
        else:
            status, s = convert(rel, chrome)
            if status.startswith("NO "):
                print("FAIL %s: %s" % (rel, status)); failures += 1
                continue
        bad = check_page(rel, s, chrome, had_app)
        for b in bad:
            print("GUARD %s: %s" % (rel, b))
        failures += len(bad)
    failures += sweep_borrowed(check_only)
    if failures:
        print("family_rest: %d FAILURE(S)" % failures)
        sys.exit(1)
    print("family_rest: %d page(s) %s, all guards clean"
          % (len(PAGES), "checked" if check_only else "converted"))


if __name__ == "__main__":
    main()
