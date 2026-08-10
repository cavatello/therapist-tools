#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Two pages everything links to, that link to nothing.

WHAT THE AUDIT FOUND

Measuring in-body prose links only - stripping the masthead, the footer and the
up-link block, because those are furniture and a crawler weights them
accordingly - two of the most-linked pages on the site pass nothing on:

    associate-mft-job-advisor.html .... 0 outbound prose links
    become-an-mft-california.html ..... 0 outbound prose links

Four other pages in the same cluster link *to* them. They are link sinks: they
absorb authority and pass none, and a reader who finishes one has nowhere to go
except a block at the foot of the page that every regular reader has learned to
skip.

The newest page on the site, `associate-therapist-pay-los-angeles-bay-area.html`,
is the clearest casualty. It links out to both calculators; neither links back,
so in prose terms it is reachable only from navigation.

WHY NOT JUST ADD A RELATED-LINKS MODULE

Because `_dev/uplinks.py` already put one at the foot of every page, and its
header says plainly that it will not add a second: *no "you might also like",
no tag list, no recirculation module with eight thumbnails*. That decision was
right and this pass does not reverse it.

WHAT IT DOES INSTEAD

Inserts **one sentence, in the body, at the point where a reader actually has
the question** - after the section that raises it. Three insertions, each
anchored to a heading that exists:

  - the job advisor, after *Side by side* -> the published pay bands to check an
    offer against
  - the job advisor, after *Your hours plan* -> the hours calculator
  - the route guide, after *The 3,000 hours* -> the same calculator

Each is a real editorial link, not furniture: it names what the reader gets, not
just where it goes.

Anchored on the `<h2>` text rather than on markup structure, because both pages
are frozen HTML whose builders no longer run, and the headings are the only
stable thing in them.

Idempotent, guarded.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
MARK = "<!-- _dev/link_sinks.py -->"
END = "<!-- /link_sinks -->"

# page, heading to sit after, sentence
INSERTS = [
    ("associate-mft-job-advisor.html", "Side by side",
     'An offer only means something next to the ones around it. '
     '<a href="associate-therapist-pay-los-angeles-bay-area.html">Published '
     'pay scales for Los Angeles and the Bay Area</a> &mdash; named employers, '
     'county salary schedules, and the wage floors an offer has to clear.'),
    ("associate-mft-job-advisor.html", "Your hours plan",
     'To project a licensure date against all four gates rather than one, '
     '<a href="amft-3000-hours-california.html">the 3,000-hours '
     'calculator</a> takes your weekly numbers and names the gate you are '
     'actually waiting on.'),
    ("become-an-mft-california.html", "The 3,000 hours",
     'The 3,000 is rarely the gate that decides your date. '
     '<a href="amft-3000-hours-california.html">The hours calculator</a> '
     'projects all four from the week you actually work, and '
     '<a href="associate-therapist-pay-los-angeles-bay-area.html">what '
     'associate jobs pay</a> shows what the caseload behind those hours is '
     'worth.'),
]

CSS = """<style>%s
/* One sentence, not a module. Marked as an aside so it reads as the author
   pointing somewhere rather than as an advertisement, and sized below body
   copy so it never competes with the section it follows. */
.tsnext{margin:14px 0 22px;padding:11px 15px;border-left:3px solid #2C6350;
  background:#FBF9F3;font-size:14.6px;line-height:1.65;color:#3A3529;
  max-width:70ch;border-radius:0 8px 8px 0}
.tsnext a{color:#2C6350;font-weight:600}
</style>""" % MARK


def find_section_end(s, heading):
    """The end of the paragraph run that follows a given <h2>.

    Returns the offset just after the first `</p>` that follows the heading, so
    the sentence lands under the section's opening prose rather than between
    the heading and its first line."""
    m = re.search(r"<h2[^>]*>\s*(?:<[^>]+>\s*)*" + re.escape(heading),
                  s, re.I)
    if not m:
        return None
    p = s.find("</p>", m.end())
    return p + 4 if p > 0 else None


def main():
    changed = 0
    for rel in sorted({i[0] for i in INSERTS}):
        p = os.path.join(SITE, rel)
        if not os.path.exists(p):
            sys.exit("link_sinks: %s is missing" % rel)
        s = open(p, encoding="utf-8").read()
        orig = s
        s = re.sub(re.escape(MARK) + r"[\s\S]*?" + re.escape(END) + r"\n?", "", s)
        s = re.sub(r"<style>" + re.escape(MARK) + r"[\s\S]*?</style>\n?", "", s)

        # Insert from the bottom of the document upward, so an earlier
        # insertion cannot move the offset of a later one.
        mine = [i for i in INSERTS if i[0] == rel]
        spots = []
        for _rel, heading, text in mine:
            at = find_section_end(s, heading)
            if at is None:
                print("  MISSING  %s has no <h2> reading %r" % (rel, heading))
                continue
            spots.append((at, text))
        for at, text in sorted(spots, reverse=True):
            s = s[:at] + MARK + '<p class="tsnext">' + text + "</p>" + END + s[at:]

        e = s.lower().rfind("</body>")
        if e > 0 and spots:
            s = s[:e] + CSS + "\n" + s[e:]

        if s != orig:
            open(p, "w", encoding="utf-8").write(s)
        print("  ok       %-46s %d link sentence(s)" % (rel[:44], len(spots)))
        changed += len(spots)

    print("\n%d contextual link(s) inserted" % changed)

    # --------------------------------------------------------------- guards
    bad = 0
    for rel in sorted({i[0] for i in INSERTS}):
        s = open(os.path.join(SITE, rel), encoding="utf-8").read()
        want = len([i for i in INSERTS if i[0] == rel])
        got = s.count(MARK) - s.count("<style>" + MARK)
        if got != want:
            print("GUARD %s: %d insertion(s), expected %d" % (rel, got, want))
            bad += 1
        # every target must exist, or this pass has added dead links to the
        # two pages the whole site points at
        for href in re.findall(r'<p class="tsnext">[\s\S]*?</p>', s):
            for t in re.findall(r'href="([a-z0-9\-]+\.html)"', href):
                if not os.path.exists(os.path.join(SITE, t)):
                    print("GUARD %s: links to %s, which is not on the site"
                          % (rel, t))
                    bad += 1
        # and the sentence must sit inside the article, not after it
        m = re.search(r"<main[^>]*>([\s\S]*?)</main>", s)
        if m and m.group(1).count('class="tsnext"') != want:
            print("GUARD %s: %d of %d sentence(s) landed outside <main>"
                  % (rel, want - m.group(1).count('class="tsnext"'), want))
            bad += 1
        if s.count("<style>" + MARK) != 1:
            print("GUARD %s: %d stylesheet(s)" % (rel, s.count("<style>" + MARK)))
            bad += 1

    # The point of the pass: these two must no longer be sinks.
    for rel in ("associate-mft-job-advisor.html", "become-an-mft-california.html"):
        s = open(os.path.join(SITE, rel), encoding="utf-8").read()
        m = re.search(r"<main[^>]*>([\s\S]*?)</main>", s)
        body = re.sub(r"<!-- _dev/uplinks\.py -->[\s\S]*?<!-- /uplinks -->", " ",
                      m.group(1) if m else s)
        out = {t for t in re.findall(r'href="([a-z0-9\-]+\.html)"', body)
               if t != rel}
        if not out:
            print("GUARD %s: still has no outbound prose link" % rel)
            bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean - both former sinks now pass authority on, every "
          "target exists, and every sentence is inside the article")


if __name__ == "__main__":
    main()
