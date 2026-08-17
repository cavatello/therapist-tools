#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The "you are here" shell - S1 above the article, S3 after it.

WHY. The stage doors are four pages. The sense that the site HAS stages
comes from the other two hundred: a reader who lands on a leaf page from
a search never sees a door unless something on that page says the door
exists. The stage-doors proposal (ops/stage-doors.html, section 08)
mocked three ways to say it and settled on two:

  S1  one line above the article: which stage this page is written for,
      the stage_note saying what it tells you AT that stage, and a link
      to everything else for the stage. Seen by everybody, including
      the four-second bounce. There is no competing breadcrumb line on
      the converted pages, so this is the page's single navigational
      line - the merge the proposal required, satisfied by there being
      nothing to merge with.
  S3  a band after the article: your stage, how many other pages are
      written for it, and the three most people read next. Catches the
      reader at the moment they finish and decide whether to leave.

  S2, the sticky rail, was rejected in the proposal - invisible on
  mobile, where the traffic is - and is not built here.

HONESTY ON MULTI-STAGE PAGES. A page tagged for two stages cannot claim
"you are at counting hours" to a reader who is in a program - the whole
point of stage_note is that the same page says different things to
different readers. So:
  one stage   -> the full S1 line with that stage's note, and the full
                 S3 band with next-reads.
  two or more -> S1 becomes a row of door links ("written for - in a
                 program / counting hours"), no false claim; S3 lists
                 each stage with its own note and count, so the reader
                 self-selects. No next-reads, because "what most people
                 read next" differs by stage.

NEXT-READS ARE THE DOOR'S OWN START QUESTIONS. Each door already names
the four questions that bring its stage to the site; S3 reuses those
files (minus the page itself), so the band cannot recommend anything a
door does not. Labels are short restatements, not registry summaries.

Anchors. S1 goes right after the masthead's </header> - every page has
exactly one before <main>. S3 goes above the FIRST of the signup band /
the up-link / the footer, which is the same anchor scan footer_band.py
uses, so the final order is article, S3, signup, up-link, footer no
matter which pass ran last.

Idempotent: both blocks are bracketed by markers and rewritten in place.
Styles live in css/house-chrome.css (the one sheet every converted page
links); the family passes re-stamp its ?v= hash after this runs.
"""
import html, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
REG = os.path.join(SITE, "mock", "library", "registry.json")

M1, E1 = "<!-- _dev/stage_shell.py s1 -->", "<!-- /ss1 -->"
M3, E3 = "<!-- _dev/stage_shell.py s3 -->", "<!-- /ss3 -->"

# stage -> (door file, S1 label, S3 claim)
STAGE = {
    "deciding": ("for/deciding.html", "thinking about it",
                 "You are still deciding"),
    "student": ("for/students.html", "in a program",
                "You are in the degree"),
    "associate": ("for/associates.html", "counting hours",
                  "You are counting toward 3,000"),
    "licensed": ("for/licensed.html", "licensed",
                 "You are past the license number"),
}

# stage -> the door's four start questions, as (file, short label).
# S3 prints the first three that are not the page itself.
NEXT = {
    "deciding": [
        ("becoming-a-therapist-california-career-change.html",
         "what the whole route actually takes"),
        ("county-therapist-pay-california.html",
         "what the work pays at the end"),
        ("mft-programs-california.html",
         "which of the 78 programs to pick"),
        ("bbs-fees-california-2026.html",
         "what the license itself costs"),
    ],
    "student": [
        ("how-to-find-a-practicum-site-california.html",
         "how to actually find a practicum site"),
        ("practicum-california-mft-trainee.html",
         "what a trainee is allowed to do"),
        ("bbs-90-day-rule-california.html",
         "the paperwork that starts before you graduate"),
        ("amft-3000-hours-california.html",
         "whether practicum hours count later"),
    ],
    "associate": [
        ("amft-3000-hours-california.html",
         "when you actually finish"),
        ("getting-hired-as-a-california-associate.html",
         "why nobody is answering your applications"),
        ("associate-therapist-pay-los-angeles-bay-area.html",
         "what the job should pay"),
        ("associate-unpaid-hours-california.html",
         "whether you have to work unpaid"),
    ],
    "licensed": [
        ("practice-simulator.html",
         "what your practice actually pays you"),
        ("insurance-reimbursement-rates-california-therapist.html",
         "what insurance actually pays per code"),
        ("therapist-tax-strategy-california.html",
         "sole prop against the professional corporation"),
        ("therapy-liability-insurance-california.html",
         "what insurance the practice itself needs"),
    ],
}

CSS_MARK = "/* _dev/stage_shell.py */"
CSS_END = "/* /stage_shell */"
CSS = CSS_MARK + """
.ss1{background:var(--paper);border-bottom:1px solid var(--line)}
.ss1>div{max-width:1120px;margin:0 auto;padding:9px 26px;display:flex;
 flex-wrap:wrap;align-items:baseline;gap:6px 14px;min-width:0}
.ss1 .ssk{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:10px;
 letter-spacing:.09em;text-transform:uppercase;color:var(--pine);
 font-weight:600;white-space:nowrap}
.ss1 .ssn{font-size:12.5px;color:var(--ink);line-height:1.5;min-width:0;
 overflow-wrap:anywhere}
.ss1 .ssn i{font-style:italic}
.ss1 a{font-size:12px;font-weight:700;color:var(--pine);
 text-decoration:none;white-space:nowrap;border-bottom:1px solid
 rgba(44,99,80,.4)}
.ss1 a:hover{border-bottom-color:var(--pine)}
.ssnext{max-width:1120px;margin:34px auto 8px;padding:0 26px}
.ssnext>div{background:#fff;border:1px solid var(--line);border-left:4px
 solid var(--gold);border-radius:14px;padding:20px 24px}
.ssnext .gk{margin:0;font-family:'IBM Plex Mono',ui-monospace,monospace;
 font-size:10px;letter-spacing:.09em;text-transform:uppercase;
 color:#8A6516;font-weight:600}
.ssnext h2{margin:6px 0 0;font-family:Fraunces,serif;font-size:19px;
 line-height:1.3;color:var(--ink);letter-spacing:-.01em}
.ssnext p{margin:9px 0 0;font-size:13.5px;line-height:1.65;
 color:var(--ink);overflow-wrap:anywhere}
.ssnext p a{color:var(--pine);font-weight:600;text-decoration:none;
 border-bottom:1px solid rgba(44,99,80,.4)}
.ssnext p a:hover{border-bottom-color:var(--pine)}
.ssnext .ga{display:inline-block;margin-top:13px;font-size:12.5px;
 font-weight:700;color:var(--pine);text-decoration:none;border-bottom:1px
 solid rgba(44,99,80,.4)}
.ssnext .ga:hover{border-bottom-color:var(--pine)}
.ssnext ul{margin:9px 0 0;padding:0;list-style:none}
.ssnext li{margin:7px 0 0;font-size:13.5px;line-height:1.6;
 color:var(--ink);overflow-wrap:anywhere}
.ssnext li .lk{font-family:'IBM Plex Mono',ui-monospace,monospace;
 font-size:9.5px;letter-spacing:.08em;text-transform:uppercase;
 color:#8A6516;font-weight:600;margin-right:7px}
@media (max-width:640px){.ss1>div{padding:8px 16px}
 .ssnext{padding:0 16px}.ssnext>div{padding:16px 18px}}
""" + CSS_END


def esc(x):
    s = html.escape(str(x))
    return re.sub(r"&amp;(#\d+|[a-zA-Z]+);", r"&\1;", s)


def soften(note):
    """The stage_note, made to follow 'This page tells you ...'."""
    n = note.strip()
    if len(n) > 1 and n[1].islower():
        n = n[0].lower() + n[1:]
    return n


def s1_block(stages, notes, counts):
    o = ['<div class="ss1"><div>']
    if len(stages) == 1:
        st = stages[0]
        door, label, _ = STAGE[st]
        o.append('<span class="ssk">You are at &middot; %s</span>' % label)
        o.append('<span class="ssn">This page tells you <i>%s</i></span>'
                 % esc(soften(notes[st])))
        o.append('<a href="%s">All %d for this stage &rarr;</a>'
                 % (door, counts[st]))
    else:
        o.append('<span class="ssk">Written for</span>')
        o.append('<span class="ssn">')
        parts = []
        for st in stages:
            door, label, _ = STAGE[st]
            parts.append('<a href="%s">%s &rarr;</a>' % (door, label))
        o.append(" &middot; ".join(parts))
        o.append("</span>")
    o.append("</div></div>")
    return M1 + "".join(o) + E1


def s3_block(fname, stages, notes, counts):
    o = ['<section class="ssnext"><div>']
    o.append('<p class="gk">Where you are on the path</p>')
    if len(stages) == 1:
        st = stages[0]
        door, label, claim = STAGE[st]
        o.append("<h2>%s.</h2>" % claim)
        others = counts[st] - 1
        o.append("<p>%s page%s on this site %s written for this stage. "
                 "Next, most people read: " % (
                     ["One other", "%d other" % others][others != 1]
                     if others else "No other",
                     "s" if others != 1 else "",
                     "are" if others != 1 else "is"))
        nxt = [(f, l) for f, l in NEXT[st] if f != fname][:3]
        o.append(" &middot; ".join('<a href="%s">%s</a>' % (f, esc(l))
                                   for f, l in nxt))
        o.append(".</p>")
        o.append('<a class="ga" href="%s">Everything for this stage '
                 "&rarr;</a>" % door)
    else:
        o.append("<h2>This page is written for %s stages of the "
                 "path.</h2>" % ["two", "three", "four"][len(stages) - 2])
        o.append("<ul>")
        for st in stages:
            door, label, _ = STAGE[st]
            o.append('<li><span class="lk">%s</span>%s '
                     '<a href="%s">All %d for this stage &rarr;</a></li>'
                     % (label, esc(notes[st]), door, counts[st]))
        o.append("</ul>")
    o.append("</div></section>")
    return M3 + "".join(o) + E3


def main():
    reg = json.load(open(REG, encoding="utf-8"))
    tagged = [p for p in reg["pages"] if p.get("stages")]
    counts = {}
    for p in tagged:
        for st in p["stages"]:
            counts[st] = counts.get(st, 0) + 1

    bad = 0
    for st in counts:
        if st not in STAGE:
            print("GUARD: stage %r has no door in STAGE" % st)
            bad += 1
            continue
        if not os.path.exists(os.path.join(SITE, STAGE[st][0])):
            print("GUARD: door %s does not exist" % STAGE[st][0])
            bad += 1
    for st, items in NEXT.items():
        for f, _ in items:
            if not os.path.exists(os.path.join(SITE, f)):
                print("GUARD: NEXT names %s, which is not on the site" % f)
                bad += 1
    if bad:
        sys.exit("%d problem(s) before writing anything" % bad)

    done = 0
    for p in tagged:
        fname = p["file"]
        if fname.startswith("for/"):
            continue
        if "/" in fname:
            print("GUARD: %s is tagged but not at the root - the door "
                  "hrefs here are root-relative" % fname)
            bad += 1
            continue
        path = os.path.join(SITE, fname)
        s = open(path, encoding="utf-8").read()
        stages = p["stages"]
        notes = p.get("stage_note") or {}

        s = re.sub(re.escape(M1) + r"[\s\S]*?" + re.escape(E1), "", s)
        s = re.sub(re.escape(M3) + r"[\s\S]*?" + re.escape(E3), "", s)

        i = s.find("</header>")
        if i < 0:
            print("GUARD: %s has no </header> to anchor S1" % fname)
            bad += 1
            continue
        i += len("</header>")
        s = s[:i] + s1_block(stages, notes, counts) + s[i:]

        anchor = None
        for pat in (r"<!-- _dev/footer_band\.py -->",
                    r'<section class="ftnl"',
                    r"<!-- _dev/uplinks\.py -->",
                    r'<section class="uplink"', r"<footer"):
            m = re.search(pat, s)
            if m:
                anchor = m.start()
                break
        if anchor is None:
            print("GUARD: %s has nothing to anchor S3 above" % fname)
            bad += 1
            continue
        s = (s[:anchor] + s3_block(fname, stages, notes, counts)
             + s[anchor:])
        open(path, "w", encoding="utf-8").write(s)
        done += 1

    # ------------------------------------------------------------- css
    cp = os.path.join(SITE, "css", "house-chrome.css")
    cs = open(cp, encoding="utf-8").read()
    new = re.sub(re.escape(CSS_MARK) + r"[\s\S]*?" + re.escape(CSS_END),
                 "", cs).rstrip()
    new += "\n\n" + CSS.strip() + "\n"
    if new != cs:
        open(cp, "w", encoding="utf-8").write(new)

    # ---------------------------------------------------------- guards
    for p in tagged:
        fname = p["file"]
        if fname.startswith("for/") or "/" in fname:
            continue
        s = open(os.path.join(SITE, fname), encoding="utf-8").read()
        for mk, ek, nm in ((M1, E1, "S1"), (M3, E3, "S3")):
            if s.count(mk) != 1 or s.count(ek) != 1:
                print("GUARD: %s has %d/%d %s marker(s)"
                      % (fname, s.count(mk), s.count(ek), nm))
                bad += 1
        i1, i3, ifo = s.find(M1), s.find(M3), s.find("<footer")
        if not (0 <= i1 < i3 < ifo):
            print("GUARD: %s blocks out of order (s1 %d, s3 %d, footer %d)"
                  % (fname, i1, i3, ifo))
            bad += 1
    # And no page OUTSIDE the tagged set carries a stray block.
    stray = set()
    tag_files = {p["file"] for p in tagged}
    for f in sorted(os.listdir(SITE)):
        if not f.endswith(".html") or f in tag_files:
            continue
        s = open(os.path.join(SITE, f), encoding="utf-8").read()
        if M1 in s or M3 in s:
            stray.add(f)
    for f in stray:
        print("GUARD: %s carries a stage shell but is not tagged" % f)
        bad += 1

    if bad:
        sys.exit("%d problem(s)" % bad)
    print("%d page(s) given the stage shell (S1 + S3); by stage: %s"
          % (done, ", ".join("%s %d" % (k, v)
                             for k, v in sorted(counts.items()))))


if __name__ == "__main__":
    main()
