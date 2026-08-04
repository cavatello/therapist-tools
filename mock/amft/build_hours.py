#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""amft-3000-hours-california.html

The hours half of the Job Advisor, given its own page.

Why split: the two halves have completely different rhythms. You compare offers
once, while job-hunting. You track hours every week for two years. And they are
different searches — "how long to get 3000 hours amft" is not "what does an amft
job pay". One page trying to rank for both ranked well for neither.

This imports the SAME engine.py the advisor uses, so hoursCalc() and drawHours()
exist once. Nothing here is a second copy of the arithmetic; the two pages simply
render different parts of it.
"""
import os, re, json

HERE = os.path.dirname(os.path.abspath(__file__))
import content as C
from css import CSS
from engine import JS as ENGINE_JS
from art import HERO_ART

SITE = "https://cavatello.github.io/therapist-tools"
SLUG = "amft-3000-hours-california.html"
ADVISOR = "associate-mft-job-advisor.html"
TITLE = ("How long to 3,000 hours? An AMFT hours calculator for California")
DESC = ("Work out your real licensure date as a California associate. The 3,000 is "
        "almost never the gate that decides it — this projects all four, including the "
        "500 relational hours and the 104 weeks, and tells you which one you are "
        "actually waiting on.")

chrome_css = open(os.path.join(HERE, "_chrome_css.txt")).read()
chrome_hdr = open(os.path.join(HERE, "_chrome_hdr.txt")).read()
chrome_head = open(os.path.join(HERE, "_chrome_head.txt")).read()
chrome_js = open(os.path.join(HERE, "_chrome_js.txt")).read().split("\n/*---*/\n")[0]
chrome_ftr = open(os.path.join(HERE, "_chrome_ftr.txt")).read()
chrome_hdr = re.sub(r'(<a href="[^"]*") class="on"', r"\1", chrome_hdr)

# NOTE: importing this module RUNS it, so the advisor is rebuilt as a side
# effect. That is harmless (same inputs, same output) and it guarantees the two
# pages are always generated from the same field() and the same chrome.
import build_advisor as BA


def build_body():
    B = []
    A = B.append

    A('<section class="ahero"><div class="in"><div>')
    A('<p class="akick">California &middot; registered associates</p>')
    A('<h1>How long to <em>3,000 hours</em>?</h1>')
    A('<p class="atag">The 3,000 is almost never the gate that decides your date.</p>')
    A('<p class="alede">There are four requirements and they close at different speeds. '
      'A caseload of adult individuals will finish the 3,000 and still not qualify you, '
      'because 500 of your direct hours have to be couples, families or children. This '
      'projects all four from the week you actually work, and names the one you are '
      'waiting on.</p>')
    A('<div class="aherocta"><a href="#week">Work out my date</a>'
      '<a class="ghost" href="%s">What the job pays &rarr;</a></div>' % ADVISOR)
    A('</div><div class="aart">' + HERO_ART + '</div></div></section>')

    # --- the week
    A('<section class="slab pine" id="week"><div class="ch-h"><span class="ch-n">01</span>'
      '<h2>Your week, and what you have banked</h2></div>')
    A('<p class="dek">Six numbers for the week you work now, and four for what is already '
      'signed off. Nothing is saved &mdash; your setup lives in the address bar, so a '
      'bookmark keeps it.</p>')
    A('<div class="job" style="border-style:solid"><div class="fsub" style="margin-top:0">'
      'Your week, by who is in the room</div><div class="fgrid">')
    A(BA.field("h_ind", "Individual adults", "hrs", mn=0, mx=45, step=.5, ph="12"))
    A(BA.field("h_rel", "Couples, families and children", "hrs", mn=0, mx=45, step=.5, ph="12"))
    A(BA.field("h_grp", "Groups", "hrs", mn=0, mx=45, step=.5, ph="0"))
    A(BA.field("h_non", "Notes, meetings, trainings", "hrs", mn=0, mx=45, step=.5, ph="10"))
    A(BA.field("h_sup", "Supervision", "hrs", mn=0, mx=12, step=.5, ph="1"))
    A(BA.field("h_weeks", "Weeks you work a year", "wks", mn=1, mx=52, step=1, ph="48"))
    A('</div>')
    A('<p class="waitnote" id="planwait"></p>')
    A('<p class="jobfoot">Couples, families and children go in one box because the BBS '
      'counts them together against the same 500 &mdash; it does not care which of the '
      'three a given hour was. Groups are counted as direct clinical but not as relational '
      'here, because whether a particular group qualifies depends on who is in it; ask '
      'your supervisor, and move the hours across if it does.</p>')
    A('<div class="fsub">What you have already banked</div><div class="fgrid">')
    A(BA.field("h_have", "Total hours so far", "hrs", mn=0, mx=3000, step=1, ph="0"))
    A(BA.field("h_have_d", "Of those, direct clinical", "hrs", mn=0, mx=3000, step=1, ph="0"))
    A(BA.field("h_have_r", "Of those, couples/families/children", "hrs", mn=0, mx=3000,
               step=1, ph="0"))
    A(BA.field("h_have_w", "Weeks of supervision completed", "wks", mn=0, mx=400, step=1,
               ph="0"))
    A('</div>')
    A('<p class="jobfoot">Practicum hours count if you were enrolled and had the '
      'coursework, within the pre-degree caps: 1,300 in total as a trainee, of which at '
      'most 750 may be counselling plus supervisor contact.</p>')
    A('</div>')
    A('</section>')

    # --- the gates
    A('<section class="slab carbon" id="gates"><div class="ch-h"><span class="ch-n">02</span>'
      '<h2>The four gates</h2></div>')
    A('<p class="dek">Each one projected from the week above. The one holding you is '
      'marked &mdash; it is the only one worth changing your caseload for.</p>')
    A('<div id="plan"></div>')
    A('</section>')

    # --- the rules, lifted from the advisor's own reference block
    A('<section class="slab indigo" id="rules"><div class="ch-h"><span class="ch-n">03</span>'
      '<h2>What the Board requires</h2></div>')
    A('<p class="dek">The requirements the four gates above are built on, in the '
      'Board&rsquo;s own terms.</p>')
    for title, sub in C.CHECKLIST if hasattr(C, "CHECKLIST") else []:
        A('<div class="jobfoot"><b>%s</b> &mdash; %s</div>' % (title, sub))
    A('<div class="howb"><ul>')
    A('<li><b>3,000 hours over at least 104 weeks.</b> The weeks requirement is a floor no '
      'caseload can beat: 3,000 hours in a year is not 3,000 hours of experience as far as '
      'the Board is concerned.</li>')
    A('<li><b>1,750 direct clinical minimum</b>, and <b>500 of them with couples, families '
      'or children.</b> This is the gate that strands people, because an all-adult '
      'caseload never closes it.</li>')
    A('<li><b>1,250 non-clinical maximum.</b> Notes, meetings and training count, but only '
      'to a ceiling &mdash; past it they stop adding to your total.</li>')
    A('<li><b>40 hours credited in any week</b>, and <b>six hours of supervision.</b> '
      'Working eighty does not bank eighty.</li>')
    A('<li><b>One unit of supervision a week</b>, and <b>a second in any week you provide '
      'more than ten hours of direct clinical counselling.</b> One unit is one hour of '
      'individual or triadic supervision, or two hours of group.<sup>[1][9]</sup></li>')
    A('</ul></div>')
    A('</section>')

    # --- the other half
    A('<section class="slab pine" id="next"><div class="ch-h"><span class="ch-n">04</span>'
      '<h2>The other half of the question</h2></div>')
    A('<p class="dek">Hours are one currency. The other is money, and a placement can be '
      'good at one and bad at the other. The Job Advisor prices what an offer actually '
      'pays &mdash; flat rate, share of the fee or salary &mdash; once unpaid admin and '
      'supervision are counted.</p>')
    A('<a class="acta" href="%s"><strong>What an AMFT job actually pays &rarr;</strong>'
      '<span>take-home, real hourly rate, and what each hour towards your licence is '
      'worth</span></a>' % ADVISOR)
    A('</section>')

    # --- sources
    A('<div class="adv"><div class="cites"><h3>Sources</h3>')
    for n, cite, url, note in C.CITES:
        A('<div class="cite"><span class="n">[' + str(n) + ']</span><span>'
          + ('<a href="' + url + '" target="_blank" rel="noopener noreferrer">' + cite
             + '</a>' if url else "<b>" + cite + "</b>")
          + ' &mdash; ' + note + '</span></div>')
    A('<p class="pay-note" style="margin-top:14px"><b>Estimates, not advice.</b> This '
      'projects the Board&rsquo;s published requirements onto the week you described. It '
      'cannot know what your supervisor will sign, how a particular group is classified, '
      'or what your Experience Verification forms already say. Keep your own weekly log '
      'and confirm anything that matters with your supervisor.</p>')
    A('</div></div>')
    return "\n".join(B)


LD = [
 {"@context": "https://schema.org", "@type": "WebApplication", "name": TITLE,
  "url": SITE + "/" + SLUG, "applicationCategory": "FinanceApplication",
  "operatingSystem": "Any web browser", "description": DESC,
  "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}},
 {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{
   "@type": "Question",
   "name": "How long does it take to get 3,000 hours as an AMFT in California?",
   "acceptedAnswer": {"@type": "Answer", "text":
     "It depends on which of four requirements closes last. Registered associates need "
     "3,000 hours over at least 104 weeks, of which at least 1,750 must be direct "
     "clinical counselling and at least 500 of those with couples, families or children. "
     "No more than 1,250 may be non-clinical, and no more than 40 hours count in any "
     "week. A caseload of adult individuals can complete the 3,000 without ever closing "
     "the 500."}}]},
]

SHELL = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s</title>
<meta name="description" content="%(desc)s" />
<link rel="canonical" href="%(site)s/%(slug)s" />
<meta property="og:title" content="%(title)s" />
<meta property="og:description" content="%(desc)s" />
<meta property="og:type" content="website" />
<meta property="og:url" content="%(site)s/%(slug)s" />
%(head)s
<style>%(chrome_css)s</style>
<style>%(css)s</style>
<script type="application/ld+json">%(ld)s</script>
</head><body>
%(hdr)s
<main class="adv">
%(body)s
</main>
%(ftr)s
<script>%(navjs)s</script>
<script>
%(js)s
</script>
</body></html>
"""


def main():
    body = build_body()
    html = SHELL % dict(title=TITLE, desc=DESC, site=SITE, slug=SLUG,
                        head=chrome_head, chrome_css=chrome_css, css=CSS,
                        ld=json.dumps(LD, separators=(",", ":")), hdr=chrome_hdr,
                        body=body, ftr=chrome_ftr, navjs=chrome_js, js=ENGINE_JS)
    assert html.count("<h1") == 1, "exactly one h1"
    assert html.count("<footer") == 1
    assert 'href="terms.html"' in html and 'href="privacy.html"' in html
    assert "</script>" not in ENGINE_JS
    # the ids drawHours() and the wait-prompt write into must exist
    for need in ('id="plan"', 'id="planwait"', 'id="i-h_ind"', 'id="i-h_have"'):
        assert need in html, "missing " + need
    # drawHours() writes into #plan. Two elements carrying that id means the
    # gates land in whichever comes first, which was the input form.
    import collections
    ids = re.findall(r'id="([\w-]+)"', html)
    dup = [k for k, v in collections.Counter(ids).items() if v > 1]
    assert not dup, "duplicate ids: %s" % dup
    open(os.path.join(HERE, SLUG), "w", encoding="utf-8").write(html)
    print("wrote %s  %d kB" % (SLUG, len(html) // 1024))


if __name__ == "__main__":
    main()
