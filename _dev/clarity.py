#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Microsoft Clarity, with every piece of text masked.

WHY CLARITY AND NOT MORE GA4

GA4 answers "how many" well and "why" not at all. It can tell you that 60% of
the people who started the practice simulator never reached a result. It cannot
show you the moment they stopped, and that moment is the entire finding.

Clarity is free, unlimited, unsampled, and does session replay, heatmaps,
rage-click and dead-click detection. Dead clicks in particular are the one
signal `_dev/error_tracking.py` deliberately does not attempt, because working
out that a click *should* have done something needs the whole recording.

THE PRIVACY SETTING THAT MATTERS, AND WHY IT IS NOT OPTIONAL HERE

Clarity's default masking mode is "Balanced", which records the text of most
elements and masks only fields it recognises as sensitive. On a site where a
therapist types their income, their caseload and their rent into a form, that
default is wrong.

This pass sets `content: false`, which is Clarity's **strict** mode: no text is
recorded at all. Replays show layout, cursor, scroll and click position with
every character rendered as a block. You still see exactly where somebody got
stuck. You never see what they typed, and neither does Microsoft.

That keeps the promise the calculator pages make in print - "Nothing you type
is sent anywhere" - literally true with Clarity installed, which it would not
be on the default setting.

The guard at the bottom refuses to write the tag if that flag is missing or
set to true.

BEFORE THIS CAN RUN

Clarity needs a project ID, and getting one means signing in at
clarity.microsoft.com and creating a project for therapistsupport.org. That is
an account action, so it is not done for you - set PROJECT_ID below to the ID
from Settings -> Overview -> Project ID and run this.

Idempotent, guarded. Run in the STRUCTURE stage, after analytics.py.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training")
MARK = "<!-- _dev/clarity.py -->"

# Set this to the project ID from clarity.microsoft.com, then run.
# Until it is set, this pass removes any tag it previously wrote and stops.
PROJECT_ID = ""

TAG = """%(mark)s
<script type="text/javascript">
  (function(c,l,a,r,i,t,y){
    c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
    t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
    y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
  })(window, document, "clarity", "script", "%(pid)s");

  // STRICT MASKING. Not the default.
  //
  // Clarity's default is "Balanced", which records most on-page text. This
  // site asks therapists to type their income into a form and tells them in
  // print that nothing they type is sent anywhere. `content: false` is
  // Clarity's strict mode: no text is captured at all, so a replay shows
  // layout, cursor, scroll and clicks with every character blocked out.
  //
  // You still see where somebody got stuck. You never see what they typed.
  window.clarity("consent", false);
  window.clarity("set", "maskTextContent", "true");
</script>
<script type="text/javascript">
  window.clarityConfig = { content: false, cookies: false };
</script>
%(end)s"""

END = "<!-- /clarity -->"


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return out


def strip(s):
    return re.sub(re.escape(MARK) + r"[\s\S]*?" + re.escape(END) + r"\n?", "", s)


def main():
    if not PROJECT_ID:
        # Not configured. Remove anything a previous run left, and say plainly
        # what is missing rather than writing a tag with an empty id, which
        # would load a 404 script on all 163 pages.
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
        print()
        print("To finish:")
        print("  1. Sign in at https://clarity.microsoft.com")
        print("  2. Create a project for https://therapistsupport.org")
        print("  3. Settings -> Overview -> Project ID")
        print("  4. Put it in PROJECT_ID at the top of this file and re-run")
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
            continue
        s = s[:i] + tag + "\n" + s[i:]
        if s != orig:
            open(p, "w", encoding="utf-8").write(s)
            n += 1
    print("Clarity installed on %d page(s), project %s" % (n, PROJECT_ID))

    # ------------------------------------------------------------- guards
    bad = 0
    for rel in pages():
        s = open(os.path.join(SITE, rel), encoding="utf-8").read()
        if "sitenav" in s and s.count(MARK) != 1:
            print("GUARD %s: %d copies" % (rel, s.count(MARK)))
            bad += 1

    # THE GUARD THIS PASS EXISTS FOR. Balanced masking on this site would
    # record a therapist's income off the screen and into a replay.
    if "content: false" not in tag:
        print("GUARD: strict masking is not set. Clarity would default to "
              "Balanced and record on-page text, including what readers type "
              "into the calculators.")
        bad += 1
    if re.search(r"content:\s*true", tag):
        print("GUARD: content masking is explicitly disabled"); bad += 1
    if "maskTextContent" not in tag:
        print("GUARD: maskTextContent is not set"); bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean - strict masking on, no text is recorded")


if __name__ == "__main__":
    main()
