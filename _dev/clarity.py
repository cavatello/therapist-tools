#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Microsoft Clarity, with the whole document masked from the page itself.

WHY CLARITY AND NOT MORE GA4

GA4 answers "how many" well and "why" not at all. It can tell you that 60% of
the people who started the practice simulator never reached a result. It cannot
show you the moment they stopped, and that moment is the entire finding.

Clarity is free, unlimited, unsampled, and does session replay, heatmaps,
rage-click and dead-click detection. Dead clicks in particular are the one
signal `_dev/error_tracking.py` deliberately does not attempt, because working
out that a click *should* have done something needs the whole recording.

THE PRIVACY SETTING THAT MATTERS - AND THE FIRST VERSION OF THIS FILE HAD IT
WRONG

Clarity's default masking mode is **Balanced**: it records the text of most
elements and masks only what it classifies as sensitive. On a site where a
therapist types their income, their caseload and their rent into a form, that
default is wrong.

The first version of this pass tried to force strict mode from the tag with
`window.clarityConfig = {content:false}` and
`clarity("set","maskTextContent","true")`. **Neither is a real API for the
JavaScript tag.** They would have loaded silently, done nothing, and left the
project on Balanced while this file's guard cheerfully reported "strict masking
on, no text is recorded". A guard that checks a string it wrote itself proves
nothing; that is why this one now checks the page.

What Microsoft actually documents:

  - masking mode is a **dashboard** setting, Settings -> Masking -> Strict
  - `data-clarity-mask="True"` on an element masks that element **and all its
    children**, and overrides the dashboard setting
  - input boxes and dropdowns are always masked in every mode, and cannot be
    unmasked

So this pass puts `data-clarity-mask="True"` on the `<body>` of every page. The
whole document is masked from the page's own markup, whatever the dashboard
says and whoever changes it later. Replays show layout, cursor, scroll and
click position with every character rendered as a block. You still see exactly
where somebody got stuck. You never see what they typed.

That keeps the promise the calculator pages make in print - "Nothing you type
is sent anywhere" - literally true with Clarity installed.

**Also set Settings -> Masking -> Strict in the dashboard.** The attribute is
the belt; the dashboard setting is the braces, and it is the one that covers
any page that ever ships without this pass having run.

Idempotent, guarded on the rendered page rather than on its own tag text.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training", "for")
MARK = "<!-- _dev/clarity.py -->"
END = "<!-- /clarity -->"
MASK = 'data-clarity-mask="True"'

# From clarity.microsoft.com, Settings -> Overview -> Project ID.
# Until it is set, this pass removes any tag it previously wrote and stops.
PROJECT_ID = "xzv1qvmwpe"

TAG = """%(mark)s
<script type="text/javascript">
  /* Microsoft Clarity. The whole document is masked by the
     data-clarity-mask attribute on the body element, written by
     _dev/clarity.py - masking cannot be forced from this tag, only from the
     markup or from the dashboard. */
  (function(c,l,a,r,i,t,y){
    c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
    t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
    y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
  })(window, document, "clarity", "script", "%(pid)s");
</script>
%(end)s"""


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return out


def body_tag(s):
    """The real body element, not a `<body>` written inside a head script."""
    h = s.lower().find("</head>")
    if h < 0:
        return None
    return re.search(r"<body([^>]*)>", s[h:], re.I) and \
        re.compile(r"<body([^>]*)>", re.I).search(s, h)


# An inline Clarity script that carries no MARK. `pagekit.chrome_parts`
# copies a donor page's inline scripts into a page being built, and it
# collects `<script>...</script>` only - so it takes the tag BODY and leaves
# the MARK comment behind, because the mark sits outside the element. The
# copy is therefore invisible to a strip that keys on the mark, and invisible
# to a guard that COUNTS the mark. 106 published pages were loading the
# tracker twice, and `clarity.py` reported one tag on every one of them.
#
# The eleventh instance of this repository's signature bug: a marker-based
# guard, and a copy that lost the marker.
UNMARKED = re.compile(
    r'[ \t]*<script(?![^>]*\bsrc=)[^>]*>(?:(?!</script>)[\s\S])*?'
    r'clarity\.ms(?:(?!</script>)[\s\S])*?</script>\n?')


def strip(s):
    s = re.sub(re.escape(MARK) + r"[\s\S]*?" + re.escape(END) + r"\n?", "", s)
    # Any surviving tag is one of the unmarked copies described above.
    s = UNMARKED.sub("", s)
    # ...and the copy left its CLOSING comment behind. `chrome_parts` took
    # the `<script>` element and the `<!-- /clarity -->` that followed it in
    # the donor's tail, but not the `<!-- _dev/clarity.py -->` that opened
    # it - the mark sits before the element, the end sits after. Removing
    # the script alone therefore leaves a dangling end marker, which
    # `analytics_once.py` counts and fails on: 1 opening against 2 closing.
    # Anything left is orphaned by construction, because the marked block
    # was removed whole in the first substitution above.
    s = re.sub(r"[ \t]*" + re.escape(END) + r"\n?", "", s)
    return re.sub(r"\s*" + re.escape(MASK), "", s)


def main():
    if not PROJECT_ID:
        removed = 0
        for rel in pages():
            p = os.path.join(SITE, rel)
            s = open(p, encoding="utf-8").read()
            t = strip(s)
            if t != s:
                open(p, "w", encoding="utf-8").write(t)
                removed += 1
        print("PROJECT_ID is not set, so nothing was installed.")
        if removed:
            print("%d page(s) had an old tag removed." % removed)
        print("\nTo finish: clarity.microsoft.com -> Settings -> Overview -> "
              "Project ID, put it in PROJECT_ID and re-run.")
        return

    tag = TAG % {"mark": MARK, "pid": PROJECT_ID, "end": END}

    n = 0
    for rel in pages():
        p = os.path.join(SITE, rel)
        s = open(p, encoding="utf-8").read()
        if "sitenav" not in s:
            continue
        orig = s
        s = strip(s)

        i = s.lower().find("</head>")
        if i < 0:
            print("  MISSING  %s has no </head>" % rel)
            continue
        s = s[:i] + tag + "\n" + s[i:]

        # The mask attribute, on the body element, on every page. This is the
        # part that actually does the work; the tag above is just the loader.
        #
        # Searched AFTER </head>, and the first version of this pass did not.
        # The literal text `<body>` appeared inside this file's own script
        # comment, which sits in the head - so `re.search("<body[^>]*>")`
        # matched the COMMENT on all 163 pages, wrote the attribute into a
        # string of JavaScript, and left every real body element unmasked. The
        # guard then read the same first match back and reported success.
        # Anchoring past </head> is the fix; the guard below does the same.
        m = body_tag(s)
        if not m:
            print("  MISSING  %s has no <body> after </head>" % rel)
            continue
        s = s[:m.start()] + "<body%s %s>" % (m.group(1).rstrip(), MASK) \
            + s[m.end():]

        if s != orig:
            open(p, "w", encoding="utf-8").write(s)
        n += 1

    print("Clarity on %d page(s), project %s, whole document masked from the "
          "markup" % (n, PROJECT_ID))

    # --------------------------------------------------------------- guards
    # These read the written page, not the tag string this file composed.
    # Checking your own template proves only that you can spell.
    bad = 0
    checked = 0
    for rel in pages():
        s = open(os.path.join(SITE, rel), encoding="utf-8").read()
        if "sitenav" not in s:
            continue
        checked += 1
        if s.count(MARK) != 1:
            print("GUARD %s: %d Clarity tags" % (rel, s.count(MARK)))
            bad += 1
        # Count the TAG, not the comment above it. A marker can be lost in a
        # copy; the thing that actually loads the tracker cannot. This is the
        # check that would have caught the duplication on 106 pages.
        if s.count("clarity.ms") != 1:
            print("GUARD %s: the Clarity endpoint appears %d time(s); the "
                  "page would load the tracker more than once"
                  % (rel, s.count("clarity.ms")))
            bad += 1
        body = body_tag(s)
        if not body or MASK not in body.group(0):
            print("GUARD %s: <body> does not carry %s. Clarity would fall back "
                  "to the dashboard setting, which defaults to Balanced and "
                  "records on-page text." % (rel, MASK))
            bad += 1
        if body and body.group(0).count(MASK) > 1:
            print("GUARD %s: the mask attribute is on <body> twice" % rel)
            bad += 1
        # Exactly one body element. More than one means something - very
        # possibly this pass - has written `<body` into the page as text.
        if len(re.findall(r"<body[\s>]", s, re.I)) != 1:
            print("GUARD %s: %d `<body` in the document. The mask has to land "
                  "on the element, not on a copy of the word."
                  % (rel, len(re.findall(r"<body[\s>]", s, re.I))))
            bad += 1
        # An unmask anywhere would punch a hole in the whole thing.
        if "data-clarity-unmask" in s:
            print("GUARD %s: something carries data-clarity-unmask, which "
                  "overrides the document-level mask" % rel)
            bad += 1

    # Nothing in the tag may claim to configure masking, because nothing in a
    # tag can. A fake call here is worse than none: it reads as a guarantee.
    for fake in ("clarityConfig", "maskTextContent", 'clarity("set"'):
        if fake in tag:
            print("GUARD: the tag contains %r, which is not a real Clarity "
                  "JavaScript API. Masking comes from data-clarity-mask and "
                  "the dashboard, and a call that does nothing reads as a "
                  "promise that is being kept." % fake)
            bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean - %d page(s), every <body> masked, no unmask anywhere, "
          "and no fake masking API in the tag" % checked)
    print()
    print("STILL TO DO BY HAND, and it is the belt to this pass's braces:")
    print("  clarity.microsoft.com -> Settings -> Masking -> Strict")
    print("  It covers any page that ships without this pass having run.")


if __name__ == "__main__":
    main()
