#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""associate-mft-job-advisor.html

Its own file, its own <title>, its own structured data. The site chrome — the
masthead, the nav panel, their CSS and the toggle script — is lifted verbatim
from a published page at build time rather than retyped, so this page cannot
drift away from the rest of the site the way a hand-copied header always does.
"""
import os, re, json

HERE = os.path.dirname(os.path.abspath(__file__))
import content as C
from css import CSS
from engine import JS
from art import HERO_ART

SITE = "https://therapistsupport.org"
SLUG = "associate-mft-job-advisor.html"
TITLE = ("Associate MFT Job Advisor — compare California AMFT jobs, pay and "
         "3,000 hours")
DESC = ("Compare California AMFT job offers side by side: W-2 take-home after federal, "
        "state, FICA and SDI; what an hour is really worth once unpaid notes are counted; "
        "and when your 3,000 BBS hours actually close.")

# ---------------------------------------------------------------- chrome ---
chrome_css = open(os.path.join(HERE, "_chrome_css.txt")).read()
chrome_hdr = open(os.path.join(HERE, "_chrome_hdr.txt")).read()
chrome_head = open(os.path.join(HERE, "_chrome_head.txt")).read()
chrome_js = open(os.path.join(HERE, "_chrome_js.txt")).read().split("\n/*---*/\n")[0]
# The footer was never lifted, which is why this page used to just
# stop. Its CSS was inside _chrome_css.txt all along.
chrome_ftr = open(os.path.join(HERE, "_chrome_ftr.txt")).read()

# This page joins the Tools column. The entry is inserted into the lifted markup
# rather than written out, so it inherits the icon, the classes and the hover
# behaviour of every other entry automatically.
# Once the entry is live on the source page it arrives with the lifted chrome and
# must not be added a second time. Idempotent either way, so this build works
# before and after the nav migration ships.
if SLUG not in chrome_hdr:
    _tools_first = re.search(
        r'(<div class="np-col"><h5>Tools</h5>)(<a href="tools\.html"[^>]*>)(.*?)(</a>)',
        chrome_hdr, re.S)
    assert _tools_first, "could not find the Tools column in the lifted masthead"
    _icon = re.search(r'<img src="(data:image/svg\+xml[^"]*)"',
                      _tools_first.group(3)).group(1)
    NEW_ENTRY = ('<a href="' + SLUG + '"><img src="' + _icon + '" alt="" aria-hidden="true">'
                 '<span><b>Associate Job Advisor</b><i>compare AMFT jobs, pay and your 3,000 '
                 'hours</i></span></a>')
    chrome_hdr = chrome_hdr.replace(
        _tools_first.group(0), _tools_first.group(0) + NEW_ENTRY, 1)
SELF = SLUG
# The chrome is lifted from tools.html, where "All free tools" legitimately
# carries class="on". Lifted onto another page that marker is a lie: every page
# was telling the reader they were on the tools page. Strip every marker first,
# then set the one that belongs to THIS page.
chrome_hdr = re.sub(r'(<a href="[^"]*") class="on"', r'\1', chrome_hdr)
_self = re.search(r'<a href="' + re.escape(SELF) + r'"', chrome_hdr)
assert _self, "this page has no entry of its own in the lifted nav: " + SELF
chrome_hdr = (chrome_hdr[:_self.end() - 1] + '" class="on"'
              + chrome_hdr[_self.end():])
assert chrome_hdr.count('class="on"') == 1

# ------------------------------------------------------------ structured ---
LD = [
 {"@context":"https://schema.org","@type":"WebApplication",
  "name":"Associate MFT Job Advisor","url":SITE + "/" + SLUG,
  "applicationCategory":"FinanceApplication","operatingSystem":"Any web browser",
  "browserRequirements":"Requires JavaScript",
  "offers":{"@type":"Offer","price":"0","priceCurrency":"USD"},
  "description":DESC,
  "audience":{"@type":"Audience",
              "audienceType":"Associate and trainee marriage and family therapists in California"},
  "featureList":["W-2 take-home for California associates",
                 "Side-by-side job offer comparison",
                 "Effective hourly rate including unpaid documentation time",
                 "Dollars per BBS supervised hour",
                 "3,000-hour projection against all four BBS requirements"]},
 {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
   {"@type":"ListItem","position":1,"name":"Therapist Support","item":SITE + "/"},
   {"@type":"ListItem","position":2,"name":"Free tools","item":SITE + "/tools.html"},
   {"@type":"ListItem","position":3,"name":"Associate MFT Job Advisor",
    "item":SITE + "/" + SLUG}]},
 {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
   {"@type":"Question","name":"How many hours does a California AMFT need?",
    "acceptedAnswer":{"@type":"Answer","text":
      "3,000 hours of supervised experience over at least 104 weeks. At least 1,750 must be "
      "direct clinical counseling, at least 500 of those 1,750 must involve couples, families "
      "or children, and no more than 1,250 may be non-clinical. No more than 40 hours are "
      "credited in any one week and no more than 6 of those may be supervision."}},
   {"@type":"Question","name":"Can an AMFT be paid as a 1099 contractor in California?",
    "acceptedAnswer":{"@type":"Answer","text":
      "No. Associates and trainees must work as W-2 employees or as volunteers. The narrow "
      "1099 exceptions cover expense reimbursement and recruitment stipends, not clinical "
      "work. Business and Professions Code section 4980.43.3."}},
   {"@type":"Question","name":"How long do the 500 couples, families and children hours take?",
    "acceptedAnswer":{"@type":"Answer","text":
      "500 of the 1,750 direct clinical hours must be relational work, which is 29% of the "
      "direct caseload. A caseload made up of adult individuals reaches 3,000 total hours and "
      "still does not qualify, which is why this is the requirement most associates finish "
      "last."}},
   {"@type":"Question","name":"What does an associate therapist earn in California?",
    "acceptedAnswer":{"@type":"Answer","text":
      "Roughly $58,000 to $62,000 in community mental health and federally qualified health "
      "centers where supervision is included, and about $40,600 to $46,000 in group private "
      "practice where supervision is often billed back to the associate at around $450 a "
      "month. 2025 figures."}}]}]


# ------------------------------------------------------------------ fields --
def field(fid, label, unit="", kind="number", opts=None, mn=None, mx=None,
          step=None, ph="", cls="", wrap=None):
    """The one field pattern. Everything on this page is one of these, so a fix
    to focus, contrast or tap target lands everywhere at once."""
    inner = ""
    if kind == "select":
        inner = ('<select id="i-' + fid + '">'
                 + "".join('<option value="%s">%s</option>' % (v, t) for v, t in opts)
                 + "</select>")
        val = '<span class="fv">' + inner + "</span>"
    else:
        attrs = 'id="i-%s" type="%s"' % (fid, kind)
        if mn is not None: attrs += ' min="%s"' % mn
        if mx is not None: attrs += ' max="%s"' % mx
        if step is not None: attrs += ' step="%s"' % step
        if ph: attrs += ' placeholder="%s"' % ph
        pre = '<span class="unit">$</span>' if unit == "$" else ""
        post = ('<span class="unit">' + unit + "</span>") if unit and unit != "$" else ""
        val = '<span class="fv">' + pre + "<input " + attrs + ">" + post + "</span>"
    s = ('<label class="f ' + cls + '"' + (' id="%s"' % wrap if wrap else "")
         + '><em>' + label + "</em>" + val + "</label>")
    return s


# Two models, because associate posts are advertised two ways. A fee per session
# is the same shape as a rate per clinical hour and does not need its own option.
PAY_OPTS = [("salary", "Annual salary"),
            ("hourly", "Rate per clinical hour"),
            ("split", "Share of the fee")]
SUP_OPTS = [("onclock", "Provided, on the clock"),
            ("owntime", "Provided, but on your own time"),
            ("youpay", "You arrange it and pay for it")]
FILING_OPTS = [("single", "Single"), ("mfj", "Married filing jointly"),
               ("hoh", "Head of household")]


def job_col(p, letter, dashed=False):
    g = lambda *a, **k: field(p + "_" + a[0], *a[1:], **k)
    s = ['<div class="job' + (" b" if dashed else "") + '"'
         + (' id="jobB" hidden' if dashed else "") + ">"]
    s.append('<div class="jobhead"><span class="jobtag">' + letter + "</span>"
             '<span class="jn"><input id="i-' + p + '_name" type="text" maxlength="34" '
             'aria-label="Name for offer ' + letter + '" value="'
             + ("The other one" if dashed else "This placement")
             + '"></span></div>')

    s.append('<div class="fsub">What they pay</div><div class="fgrid">')
    s.append(g("pay", "How you are paid", kind="select", opts=PAY_OPTS, cls="sm wide"))
    # Three boxes, two of them hidden at any moment. Each keeps its own value, so
    # a salary can never appear under a label that says "per hour".
    s.append(field(p + "_amt", "Annual salary", "$", mn=0, mx=400000, step=500,
                   ph="60000", cls="wide", wrap=p + "_amtwrap"))
    s.append(field(p + "_hr", "Per clinical hour", "$", mn=0, mx=300, step=1,
                   ph="45", wrap=p + "_hrwrap"))
    s.append(field(p + "_adminhr", "Per admin hour", "$", mn=0,
                   mx=300, step=1, ph="22", wrap=p + "_adminhrwrap"))
    s.append(field(p + "_fee", "What the practice bills", "$", mn=0, mx=1000, step=5,
                   ph="150", wrap=p + "_feewrap"))
    s.append(field(p + "_split", "Your share of it", "%", mn=0, mx=100, step=1,
                   ph="60", wrap=p + "_splitwrap"))
    s.append('</div>')
    # one note, rewritten by render() to match the model on screen
    s.append('<p class="jobfoot" id="' + p + '_paynote"></p>')

    s.append('<div class="fsub">Your week</div><div class="fgrid">')
    s.append(g("client", "Client hours booked a week", "hrs", mn=0, mx=60, step=.5, ph="25"))
    # "Show rate" is industry shorthand and the reader asked what it meant. The
    # label now says the thing itself; the shorthand is taught in the note below,
    # so the word is still learnable rather than just gone.
    s.append(g("show", "Of those, actually happen", "%", mn=0, mx=100, step=1, ph="85"))
    # One admin field, not two. "Paid admin" plus "unpaid hours" asked the reader
    # to split a number the pay model already splits for them: under a fee split
    # every admin hour is unpaid by construction, under salary they are all paid,
    # and under an hourly post they are paid at the admin rate. Asking for the
    # split invited a guess and then quietly double-counted it in worked hours.
    s.append(g("admin", "Admin and notes, hours a week", "hrs", mn=0, mx=60,
               step=.5, ph="10"))
    s.append(g("weeks", "Weeks you work a year", "wks", mn=1, mx=52, step=1, ph="48"))
    s.append('</div>')
    s.append('<p class="jobfoot"><b>&ldquo;Of those, actually happen&rdquo; is the show '
             'rate</b> &mdash; the share of booked sessions that are not cancelled or '
             'no-showed. Around 85% is normal; below 75% is worth asking about. It counts '
             'twice: a session that does not happen is an hour you do not get towards your '
             '3,000, and on an hourly or fee-split job it is money you do not get '
             'either.</p>')

    s.append('<div class="fsub">Supervision</div><div class="fgrid">')
    s.append(g("sup", "How it is arranged", kind="select", opts=SUP_OPTS, cls="sm wide"))
    s.append(g("indiv", "Individual or triadic", "hrs", mn=0, mx=10, step=.5, ph="1"))
    s.append(g("group", "Group", "hrs", mn=0, mx=12, step=.5, ph="0"))
    s.append(field(p + "_supcost", "What you pay for it", "$/mo", mn=0, mx=3000, step=25,
                   ph="450", cls="wide", wrap=p + "_supcostwrap"))
    s.append('</div>')
    # The Board's requirement, computed from the direct hours entered above and
    # rendered by render(). It is a check, not an autofill: the reader is
    # describing an offer that exists, and silently rewriting their entry would
    # hide exactly the shortfall this is here to surface.
    s.append('<p class="supreq" id="' + p + '_supreq"></p>')

    s.append('<div class="fsub">Everything that is not pay</div><div class="fgrid">')
    s.append(g("health", "Employer health contribution", "$/mo", mn=0, mx=3000, step=25,
               ph="450"))
    s.append(g("extra", "Match, stipends, reimbursements", "$/yr", mn=0, mx=40000, step=100,
               ph="1200"))
    s.append('</div>')
    s.append('</div>')
    return "".join(s)


# --------------------------------------------------------------------- body --
BODY = []
A = BODY.append

A('<div class="adv">')

# ---- hero
A('<section class="ahero"><div class="in"><div>')
A('<p class="akick">For practicum students and new associates &middot; California</p>')
A('<h1>Evaluating AMFT jobs and earnings in <em>California</em>.</h1>')
A('<p class="atag">Put one job in. Add a second only if you are choosing between '
  'them.</p>')
A('<p class="alede">A placement is two decisions wearing one coat: <b>what it pays you '
  'now</b>, and <b>how fast it closes your 3,000 hours</b>. The offer letter only tells you '
  'about the first, and it rounds that up.</p>')
A('<div class="aherocta"><a href="#offers">Start with one job</a>'
  '<a class="ghost" href="#hours">Just the hours plan</a></div>')
A('</div><div class="apanel">' + HERO_ART + '<div id="apanel"></div></div>')
A('</div></section>')

# ---- 01 the offers
A('<section class="slab pine" id="offers"><div class="ch-h"><span class="ch-n">01</span>'
  '<h2>The placement</h2></div>')
A('<p class="dek">Fill in one and everything below wakes up &mdash; take-home, the real '
  'hourly rate, and your licence date. The fields people skip &mdash; how many sessions '
  'actually happen, how much of the week is notes, who pays for supervision &mdash; are '
  'the ones that change '
  'the answer most, so they are not buried in an advanced panel. '
  '<b>Nothing is saved anywhere.</b></p>')
A('<div class="fgrid" style="max-width:420px;margin-bottom:18px">'
  + field("filing", "Your tax filing status", kind="select", opts=FILING_OPTS,
          cls="sm wide") + '</div>')
A('<div class="jobs">' + job_col("a", "A") + job_col("b", "B", dashed=True) + '</div>')
A('<button class="addb" id="addB" type="button">+&nbsp; Compare a second offer</button>')
A('<p class="jobfoot">Optional &mdash; everything below works on one job.</p>')
A('<details class="how"><summary><b>What these fields mean, and why these ones</b>'
  '<span>show rate, admin time, and what the Board requires</span></summary>'
  '<div class="howb"><ul>'
  '<li><b>Supervision, in units.</b> The Board counts units, not hours: one unit is one hour of individual or triadic supervision, or two hours of group. You need at least one unit in any week you gain experience in a setting &mdash; and a <b>second unit</b> in any week you provide more than ten hours of direct clinical counselling there. The line under the supervision boxes checks the offer against that rule.<sup>[1][9]</sup></li>'
  '<li><b>Show rate.</b> The share of booked sessions that actually happen. A no-show costs '
  'you the hour towards your licence whatever the pay model is. On fee-for-service it costs '
  'you the fee as well, which is why that model can pay far less than it advertises.</li>'
  '<li><b>Paid admin hours.</b> Notes, case conferences, team meetings, trainings &mdash; the '
  'hours you are on the clock and not with a client. These count towards your 3,000 as '
  'non-clinical experience, up to the 1,250 ceiling.</li>'
  '<li><b>Unpaid hours.</b> Work you do that nobody is paying for. Writing notes at home is '
  'the usual one. It is the single biggest difference between the hourly rate on the offer '
  'and the hourly rate you live on.</li>'
  '<li><b>Who arranges supervision.</b> Agency posts almost always provide it on the clock. '
  'Group private practice often bills it back to you at roughly $450 a month, which is '
  'about $5,400 a year out of your take-home. Both are legal; only one is in the salary '
  'figure.</li>'
  '<li><b>Employer health contribution.</b> Not pay, but money you do not spend. Two offers '
  '$4,000 apart on salary can be level once one of them covers a premium.</li>'
  '</ul></div></details>')
A('</section>')

# ---- 02 take-home
A('<section class="slab carbon" id="takehome"><div class="ch-h"><span class="ch-n">02</span>'
  '<h2>What you actually take home</h2></div>')
A('<p class="dek">A W-2 associate pays five separate things out of one salary, and California '
  'adds one nobody expects. Here they are one at a time, so you can see which line is taking '
  'what rather than looking at a single number labelled &ldquo;taxes&rdquo;.</p>')
A('<div id="take"></div>')
A('<details class="how"><summary><b>Where these figures come from</b>'
  '<span>2026 federal and California, and the one California surprise</span></summary>'
  '<div class="howb"><ul>'
  '<li><b>Federal income tax</b> uses the 2026 rate schedules and the $16,100 single standard '
  'deduction from IRS Rev. Proc. 2025-32.</li>'
  '<li><b>California income tax</b> uses the 2025 schedules, because the FTB’s own 2026 '
  'Form 540-ES tells filers to use them &mdash; the 2026 tables are not published yet.</li>'
  '<li><b>Social Security</b> is 6.2% of wages up to $184,500. <b>Medicare</b> is 1.45% of '
  'everything with no ceiling. Your employer pays the same again; you do not see it, and it '
  'is not counted here because it is not your money.</li>'
  '<li><b>California SDI</b> is the surprise: 1.3% of every dollar you earn, with no wage cap '
  'at all since 2024. On $60,000 that is $780 a year, more than most people expect from a '
  'line they have never heard of.</li>'
  '<li>Pre-tax retirement deferrals are deliberately not modelled. On an associate salary they '
  'flatter every offer by about the same amount and change which one wins by nothing.</li>'
  '</ul></div></details>')
A('</section>')

# ---- 03 the hour
A('<section class="slab brick" id="hourly"><div class="ch-h"><span class="ch-n">03</span>'
  '<h2>The hour that counts</h2></div>')
A('<p class="dek">Two numbers decide between associate jobs, and neither is on the offer '
  'letter. <b>What an hour of your life is worth</b> once you count the hours nobody pays '
  'for, and <b>what each BBS hour pays</b> &mdash; because for the next two years you are '
  'buying hours as much as earning money.</p>')
A('<div id="hour"></div>')
A('</section>')

# ---- 04 verdict
A('<section class="slab gold" id="compare"><div class="ch-h"><span class="ch-n">04</span>'
  '<h2>Side by side</h2></div>')
A('<p class="dek">Only fills in once you have added a second job. The row that wins is '
  'marked. Read the bottom three before the top one: gross pay is the number that misleads, '
  'and hours towards licensure are the currency you are actually short of.</p>')
A('<div id="cmp"></div>')
A('</section>')

# ---- 05 hours plan
A('<section class="slab pine" id="hours"><div class="ch-h"><span class="ch-n">05</span>'
  '<h2>Your hours plan</h2></div>')
A('<p class="dek">Everyone quotes the 3,000. It is almost never the requirement that decides '
  'your date. There are four gates and they close at different speeds &mdash; this works out '
  'all four and tells you which one you are actually waiting on.</p>')
A('<div class="job" style="border-style:solid"><div class="fsub" style="margin-top:0">'
  'Your week, by who is in the room</div><div class="fgrid">')
A(field("h_ind", "Individual adults", "hrs", mn=0, mx=45, step=.5, ph="12"))
A(field("h_rel", "Couples, families and children", "hrs", mn=0, mx=45, step=.5, ph="12"))
A(field("h_grp", "Groups", "hrs", mn=0, mx=45, step=.5, ph="0"))
A(field("h_non", "Notes, meetings, trainings", "hrs", mn=0, mx=45, step=.5, ph="10"))
A(field("h_sup", "Supervision", "hrs", mn=0, mx=12, step=.5, ph="1"))
A(field("h_weeks", "Weeks you work a year", "wks", mn=1, mx=52, step=1, ph="48"))
A('</div>')
# Named right under the boxes it is about, not in the output area below the
# card - a prompt the reader has to scroll past the fields to find is a prompt
# about the wrong thing.
A('<p class="waitnote" id="planwait"></p>')
A('<p class="jobfoot">Couples, families and children go in one box because the BBS counts '
  'them together against the same 500 &mdash; it does not care which of the three a given '
  'hour was. Groups are counted as direct clinical but not as relational here, because '
  'whether a particular group qualifies depends on who is in it; ask your supervisor, and '
  'move the hours across if it does.</p>')
A('<div class="fsub">What you have already banked</div><div class="fgrid">')
A(field("h_have", "Total hours so far", "hrs", mn=0, mx=3000, step=1, ph="0"))
A(field("h_have_d", "Of those, direct clinical", "hrs", mn=0, mx=3000, step=1, ph="0"))
A(field("h_have_r", "Of those, couples/families/children", "hrs", mn=0, mx=3000, step=1,
        ph="0"))
A(field("h_have_w", "Weeks of supervision completed", "wks", mn=0, mx=400, step=1, ph="0"))
A('</div>')
A('<p class="jobfoot">Practicum hours count if you were enrolled and had the coursework, '
  'within the pre-degree caps: 1,300 in total as a trainee, of which at most 750 may be '
  'counselling plus supervisor contact.</p>')
A('<button class="addb" id="prefill" type="button" style="margin-top:14px">'
  '&#8681;&nbsp; Copy the caseload from offer A</button>')
A('</div>')
A('<div id="plan"></div>')
A('</section>')

# ---- 06 rules
A('<section class="slab indigo" id="rules"><div class="ribbon">Before you sign</div>')
A('<div class="ch-h"><span class="ch-n">06</span><h2>What the Board requires, '
  'and what it will not fix</h2></div>')
A('<p class="dek">These are the rules that make an offer workable or void, taken from the '
  'BBS’s own handbook and FAQ. An employer getting one of them wrong is not a detail you '
  'can sort out later &mdash; it is hours you do not get back.</p>')
A('<div class="rules">' + "".join(
    '<div class="rule"><b>' + t + '</b><p>' + p + '</p>'
    '<span class="src">' + s + '</span></div>' for t, p, s in C.RULES) + '</div>')

A('<div class="ch-h" style="margin-top:30px"><h2 style="font-size:clamp(19px,2.2vw,24px)">'
  'What associates actually report going wrong</h2></div>')
A('<p class="dek">None of this is exotic. It is the ordinary texture of pre-licensure work in '
  'California, and every item is something you can ask about in an interview without sounding '
  'difficult.</p>')
A('<div class="flags">' + "".join(
    '<div class="flag"><b>' + t + '</b><p>' + p + '</p></div>' for t, p in C.FLAGS) + '</div>')

A('<details class="how"><summary><b>What the whole thing costs in fees</b>'
  '<span>registration through licence, at the current schedule</span></summary>'
  '<div class="howb"><table class="paytab"><tbody>'
  + "".join('<tr><td>%s</td><td>$%s</td></tr>' % (n, v) for n, v in C.FEES)
  + '<tr><td><b>Registration, five renewals, both exams and licensure</b></td>'
    '<td><b>$'
  + str(75 + 75 * 5 + 75 + 125 + 125 + 100) + '</b></td></tr>'
  '</tbody></table><p style="margin-top:12px">Fees are the BBS temporary reduction in '
  'force from 1 July 2026 to 30 June 2030; they revert after that. The law and '
  'ethics exam has to be taken during each renewal cycle until you pass it, so the $75 can '
  'recur. A separate $20 Mental Health Practitioner Education Fund fee applies to licence '
  'renewal-related applications and is not reduced, so it is not in the total above. '
  'Not included: your own supervision if you pay for it, professional liability '
  'insurance, and continuing education.</p></div></details>')

A('<details class="how"><summary><b>What associates are paid, by setting</b>'
  '<span>2025 figures, and why the gap is bigger than it looks</span></summary>'
  '<div class="howb"><table class="paytab"><thead><tr><th>Setting</th>'
  '<th>Annual</th></tr></thead><tbody>'
  + "".join('<tr><td>%s<i>%s</i></td><td>%s</td></tr>'
            % (n, note, ("$%s" % f"{lo:,}") if lo == hi else "$%s–$%s" % (f"{lo:,}", f"{hi:,}"))
            for n, lo, hi, note in C.PAY)
  + '</tbody></table><p style="margin-top:12px">The setting decides this far more than the '
  'credential does. A community mental health post at $60,000 with supervision and a health '
  'plan included is worth substantially more than a group practice at $60,000 where you pay '
  '$5,400 for supervision and buy your own cover &mdash; and the second one is the offer that '
  'sounds better on the phone.</p></div></details>')
A('</section>')

# ---- what comes next
# NOT a tax-strategy pitch. On $58,000 with no business to run, deferral is close
# to worthless and the sole-prop-versus-corporation question does not exist yet -
# an associate cannot be in private practice at all. Selling that page here would
# be selling the wrong thing to the one audience it does not serve.
A('<section class="slab carbon" id="next"><div class="ch-h"><span class="ch-n">07</span>'
  '<h2>What actually helps between now and the licence</h2></div>')
A('<p class="dek">Not tax planning. At an associate salary the retirement-account '
  'arithmetic that matters to a licensed therapist in private practice barely moves '
  'the needle, and you cannot be in private practice anyway. What moves the needle now '
  'is the rate you are paid, the hours you are credited, and knowing what the work is '
  'worth before you agree to it.</p>')
A('<div class="alist" style="border-top:0;padding-top:0;margin-top:4px">' + "".join(
    '<div><i>&rarr;</i><span><b>' + a + '</b> &mdash; ' + b + '</span></div>' for a, b in [
      ("Ask what share of the caseload is relational",
       "before you accept, not at hour 2,800"),
      ("Get your hours signed as you go",
       "a supervisor who has moved on is hard to chase"),
      ("Keep your own weekly log",
       "the Board audits, and your employer's records are not yours"),
      ("Get the admin time in writing",
       "documentation is work, and whether it is paid is the biggest gap between the advertised rate and the real one"),
      ("Check the offer is W-2, not 1099",
       "an associate cannot be a contractor for clinical work in California"),
      ("Know what the setting pays before you negotiate",
       "the gap between community mental health and a group practice is bigger than the gap between offers"),
    ]) + '</div>')
A('<a class="acta" href="rates.html"><strong>What California therapy actually pays '
  '&rarr;</strong><span>insurance panels against private pay, measured &middot; the '
  'ceiling your rate is negotiated under</span></a>')
A('<p class="jobfoot" style="margin-top:14px;text-align:center">When the licence does '
  'arrive, the '
  '<a href="practice-simulator.html" style="color:#F6C560;font-weight:600">practice simulator</a> '
  'models the whole thing &mdash; rate, caseload, expenses and the tax questions that '
  'only exist once you are running a business.</p>')
A('</section>')

A('</div>')  # /.adv

# ---- citations
A('<div class="adv"><div class="cites"><h3>Sources</h3>')
for n, cite, url, note in C.CITES:
    A('<div class="cite"><span class="n">[' + str(n) + ']</span><span>'
      + ('<a href="' + url + '" target="_blank" rel="noopener noreferrer">' + cite + '</a>'
         if url else "<b>" + cite + "</b>")
      + ' &mdash; ' + note + '</span></div>')
A('</div>')
A('<p class="disc"><b>Estimates, not advice.</b> This models a single W-2 job for a California '
  'resident with no other household income, no pre-tax deferrals and no itemised deductions. '
  'Your actual withholding depends on your W-4, other income, and credits this does not model. '
  'The hour projection assumes the caseload you enter holds steady, which no caseload does. '
  'The BBS decides what counts, not this page and not your employer &mdash; keep your own '
  'weekly log, get it signed as you go, and check anything load-bearing against the handbook '
  'linked above. Nothing here is legal, tax or career advice.</p>')
A('</div>')

BODY = "\n".join(BODY)

# --------------------------------------------------------------------- head --
HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
{chrome_head}
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<meta name="robots" content="index, follow, max-image-preview:large" />
<meta name="google-adsense-account" content="ca-pub-6079968999170000" />
<title>{title}</title>
<meta name="description" content="{desc}" />
<link rel="canonical" href="{site}/{slug}" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="Therapist Support" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{desc}" />
<meta property="og:url" content="{site}/{slug}" />
<meta property="og:image" content="{site}/og-image.png" />
<meta name="twitter:card" content="summary_large_image" />
<script type="application/ld+json">{ld}</script>
<style>
{chrome_css}
</style>
<style>
{css}
</style>
</head>
<body>
{hdr}
<main>
{body}
</main>
<script>
{navjs}
</script>
<script>
{js}
</script>
{ftr}
</body>
</html>
"""

html = HEAD.format(chrome_head=chrome_head, title=TITLE, desc=DESC, site=SITE, slug=SLUG,
                   ld=json.dumps(LD, separators=(",", ":")),
                   chrome_css=chrome_css, css=CSS, hdr=chrome_hdr, body=BODY,
                   navjs=chrome_js, js=JS, ftr=chrome_ftr)

# --- build-time guards. Every one of these has been a real bug on this site. ---
assert "</script>" not in JS, "a literal </script> inside the engine would close the tag"
assert html.count("<style>") == 2 and html.count("</style>") == 2
assert html.count("<body>") == 1 and html.count("</body>") == 1
# Three pages shipped with no footer at all because the lift never took it.
assert html.count("<footer") == 1, "exactly one footer, please"
assert 'href="terms.html"' in html and 'href="privacy.html"' in html, \
    "the footer must carry the legal links"
for need in ["id=\"apanel\"", "id=\"take\"", "id=\"hour\"", "id=\"cmp\"", "id=\"plan\"",
             "id=\"addB\"", "id=\"prefill\"", "id=\"jobB\""]:
    assert html.count(need) == 1, "expected exactly one " + need
# every key the engine binds must have a field on the page
import re as _re
keys = _re.search(r"var S = \{(.*?)\n\};", JS, _re.S).group(1)
for k in _re.findall(r"(\w+):", keys):
    if k in ("showB",):
        continue
    assert 'id="i-%s"' % k in html, "state key %s has no input" % k
# ...and every field must be a key the engine knows, or it silently does nothing
for k in set(_re.findall(r'id="i-([\w]+)"', html)):
    assert _re.search(r"\b%s:" % _re.escape(k), keys), "input i-%s is not in state" % k

out = os.path.join(HERE, SLUG)
open(out, "w").write(html)
print("wrote", SLUG, len(html) // 1024, "kB;",
      len(_re.findall(r'id="i-', html)), "inputs")
