#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The two 2026 bills that reach this site's readers, and the date that decides them.

TIER 3. Queued for three handoffs as "AB 1598 / SB 903 tracker (check
current bill status first)" - a note nobody had acted on. Checked on
18 August 2026, and the check is the reason this page exists now rather
than later: **both bills were at third reading on 13 August 2026, and the
last day for each house to pass bills is 31 August 2026.** Thirteen days.

WHAT MAKES A TRACKER PAGE DANGEROUS

A page whose facts expire is a liability, not an asset. The failure mode
is not being wrong on the day it ships - it is being right on the day it
ships and wrong three weeks later while still reading as current. Two
things are done about that here:

  1. Every status sentence carries the date it was read, and the page
     leads with the two deadlines rather than with the bills. A reader
     who arrives in October is told immediately which dates have passed.
  2. A guard below fails the build if the page ever predicts an outcome.
     Neither bill is law. Both passed their house of origin unopposed and
     cleared appropriations, and that is a fact about the past; "will
     pass" is a forecast, and a forecast on a reference page is the thing
     that makes the page untrustworthy when it is wrong.

THE PAGE MUST BE UPDATED TWICE
     after 31 August 2026   passed, or dead
     after 30 September 2026   signed, or vetoed
That is written into the page in the reader's view, not just here, so
that a stale page accuses itself.

SOURCING

`leginfo.legislature.ca.gov` blocks automated fetching, which this
repository has hit before (see the BBS rules verification note). So bill
TEXT and STATUS come from sources that can be read and checked:

  - the Board of Behavioral Sciences' own bill analyzes. AB 1598 is a
    BOARD-SPONSORED bill, so the Board's April 2026 analysis is as close
    to a primary source on its contents as exists.
  - the Board's 2026 "bills through the Legislature" list, which is what
    gives the dead/pending status of the other thirteen.
  - LegiScan's action histories, for dates and vote counts.
  - the Assembly Clerk's 2026 legislative calendar, for the deadlines.

leginfo is still LINKED, per house rule, as the place to read the bill -
it is just not the place these facts were read from, and the page says so.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pagekit as pk

SITE = pk.SITE
PAGE = "california-therapy-bills-2026.html"
DONOR = "telehealth-rules-california-therapist.html"

READ = "18 August 2026"

# leginfo blocks automated fetches; these are linked, not read from.
LEG1598 = ("https://leginfo.legislature.ca.gov/faces/billStatusClient."
           "xhtml?bill_id=202520260AB1598")
LEG903 = ("https://leginfo.legislature.ca.gov/faces/billStatusClient."
          "xhtml?bill_id=202520260SB903")
BBS1598 = "https://www.bbs.ca.gov/pdf/agen_notice/2026/20260417_pa_item4.pdf"
BBS903 = "https://bbs.ca.gov/pdf/agen_notice/2026/20260507_item28_d.pdf"
BBSLIST = ("https://www.bbs.ca.gov/pdf/publications/"
           "bills_through_legislature_2026.pdf")
CAL = ("https://clerk.assembly.ca.gov/sites/clerk.assembly.ca.gov/files/"
       "2026-01/2026-calendar.pdf")
SCAN1598 = "https://legiscan.com/CA/bill/AB1598/2025"
SCAN903 = "https://legiscan.com/CA/bill/SB903/2025"
TEXT903 = "https://legiscan.com/CA/text/SB903/id/3327547"
CONST = ("https://leginfo.legislature.ca.gov/faces/codes_displaySection."
         "xhtml?sectionNum=SEC.%208.&article=IV&lawCode=CONS")

HOURS = "amft-3000-hours-california.html"
TELE = "telehealth-rules-california-therapist.html"

JUMPS = [("where", "Where they stand"),
         ("ab1598", "AB 1598"),
         ("sb903", "SB 903"),
         ("rest", "The other thirteen"),
         ("next", "What happens next")]


def body():
    o = ['<article class="pk-wrap">']

    o.append(pk.hero(
        "Two bills at third reading &middot; read " + READ
        + " &middot; neither is law",
        "Two bills would change what California associates and therapists "
        "have to do. Both are decided by 31 August.",
        "One is sponsored by the Board itself and would end the annual "
        "Law and Ethics exam for associates. The other would put the "
        "first rules on artificial intelligence in a therapy practice. "
        "Both cleared appropriations on 13 August 2026 and are waiting "
        "for a floor vote. Here is what each one actually says, and the "
        "two dates that settle them.",
        [("31 Aug", "last day for each house to pass a bill"),
         ("30 Sept", "last day for the Governor to sign or veto"),
         ("30", "code sections AB 1598 would amend"),
         ("$10,000", "SB 903&rsquo;s penalty, per violation")],
        JUMPS))

    # ------------------------------------------------------------- where
    o.append('<section class="pk-sec" id="where">')
    o.append('<p class="pk-k">Status, read ' + READ + '</p>')
    o.append('<h2 class="pk-h">Both passed their own house. Neither '
             "bill is law.</h2>")
    o.append('<p class="pk-p">A California bill has to pass both houses '
             "and then be signed. Both of these have cleared one house "
             "and the second house&rsquo;s appropriations committee, and "
             "both were sitting on the second house&rsquo;s floor "
             "calendar when this page was written. Because each was "
             "amended in the second house, each also needs a concurrence "
             "vote back in its house of origin before it can reach the "
             "Governor.</p>")
    o.append(pk.table(
        ["", "AB 1598", "SB 903"],
        [["Author", "Quirk-Silva", "Padilla"],
         ["Sponsor", "The Board of Behavioral Sciences",
          "Author-sponsored"],
         ["Subject", "Behavioral sciences licensing",
          "Artificial intelligence in psychotherapy"],
         ["Passed its own house", ("21 May 2026", "m"),
          ("19 May 2026, 39&ndash;0", "m")],
         ["Off the suspense file", ("13 Aug 2026", "m"),
          ("13 Aug 2026, 13&ndash;0", "m")],
         ["Where it was on " + READ, "Senate third reading",
          "Assembly third reading"],
         ["Still needs", "A Senate floor vote, then Assembly concurrence",
          "An Assembly floor vote, then Senate concurrence"]],
        "Action dates and vote counts from the LegiScan histories; "
        "sponsorship from the Board&rsquo;s own analyzes.", 620))
    o.append("</section>")

    # ------------------------------------------------------------ ab1598
    o.append('<section class="pk-sec" id="ab1598">')
    o.append('<p class="pk-k">AB 1598 &middot; Quirk-Silva</p>')
    o.append('<h2 class="pk-h">The Board is asking to stop making '
             "associates retake the Law and Ethics exam every year.</h2>")
    o.append('<p class="pk-p">This is the Board&rsquo;s own bill, and '
             "almost all of it lands on people who are not licensed yet. "
             "It would amend thirty sections of the Business and "
             "Professions Code and repeal three. These are the changes "
             "the Board&rsquo;s April 2026 analysis describes.</p>")
    o.append(pk.numbered([
        ("1", "The annual Law and Ethics exam for associates would go.",
         "As things stand an associate has to pass the California Law "
         "and Ethics Exam again at every renewal. The bill removes that "
         "yearly retest, and instead requires the exam to have been "
         "passed &ldquo;no more than seven years prior to the "
         "board&rsquo;s receipt of the application&rdquo;."),
        ("2", "Supervised experience would stay valid for seven years, "
         "not six.",
         "The window in which hours you have already earned still count "
         "would grow by a year. For anyone whose hours have been slowed "
         "by a placement falling through, this is the provision that "
         "matters most."),
        ("3", "Up to 750 hours could be counted before the degree is "
         "finished.",
         "The bill permits counseling and supervision hours gained "
         "before degree completion, capped at 750."),
        ("4", "Associate registrations could be renewed six times "
         "instead of five.",
         "Seven years of registration in total rather than six, with the "
         "renewal deadline extended to match."),
        ("5", "A one-time, two-year hardship extension.",
         "For an associate on a subsequent registration number, working "
         "in a single private practice setting."),
        ("6", "The clinical exam would stay valid for seven years.",
         "Matching the Law and Ethics change above."),
        ("7", "The $20 exam rescoring fee would be removed.",
         "Small, and the only fee change in the bill."),
        ("8", "The exemption for counseling in a religious context "
         "would be clarified.",
         "The bill restates who is exempt when counseling is provided "
         "&ldquo;in a religious or spiritual context&rdquo;, and keeps "
         "the condition that an exempt person must not claim to be "
         "licensed or use a restricted title."),
    ]))
    o.append(pk.callout(
        "If you are counting hours",
        ["Nothing here is in force. The rules that govern your hours "
         "today are the ones on our page for the 3,000 hours, and they "
         "are unchanged until a bill is signed and takes effect. What "
         "this bill would change is how long those hours stay good and "
         "how many times you can renew while you earn them.",
         '<a href="' + HOURS + '">The 3,000 hours, as the rules stand '
         "&rarr;</a>"]))
    o.append("</section>")

    # ------------------------------------------------------------- sb903
    o.append('<section class="pk-sec" id="sb903">')
    o.append('<p class="pk-k">SB 903 &middot; Padilla</p>')
    o.append('<h2 class="pk-h">The first rules on using AI in a therapy '
             "practice, and a $10,000 penalty behind them.</h2>")
    o.append('<p class="pk-p">SB 903 would create the Wellness and '
             "Oversight for Psychological Resources Act as a new chapter "
             "of the Business and Professions Code, beginning at section "
             "4989.80. It does two separable things: it says who may "
             "offer psychotherapy at all, and it draws a line through "
             "what a licensed practitioner may hand to a machine.</p>")
    o.append(pk.quote(
        "The advertising provision, in the bill&rsquo;s own words",
        ["&ldquo;An individual, corporation, or entity shall not "
         "provide, advertise, or otherwise offer therapy or "
         "psychotherapy services &hellip; unless the therapy or "
         "psychotherapy services are conducted by an individual who is a "
         "licensed professional.&rdquo;"]))
    o.append(pk.table(
        ["A licensed professional could not let AI&hellip;",
         "&hellip;but could use it to"],
        [["Make independent therapeutic decisions",
          "Manage appointment scheduling and reminders"],
         ["Interact directly with a client in any form of therapeutic "
          "communication, unless the product is FDA-approved and "
          "HIPAA-compliant",
          "Process billing and insurance claims"],
         ["Generate therapeutic recommendations or treatment plans "
          "without review and approval",
          "Draft general communications about therapy logistics that "
          "carry no therapeutic advice"],
         ["Detect emotions or mental states",
          "Prepare and maintain client records, including therapy "
          "notes"],
         ["", "Analyze anonymized data to track progress or identify "
          "trends, subject to review"],
         ["", "Identify and organize external resources or referrals"]],
        "The prohibitions are in the proposed section 4989.84(b); the "
        "permitted administrative and supplementary uses in 4989.82.",
        620))
    o.append(pk.numbered([
        ("1", "Consent would have to be taken before AI touches a "
         "recorded session.",
         "Written notice and consent, disclosing that AI is being used "
         "and &ldquo;the specific purpose of the artificial intelligence "
         "tool or system&rdquo;. If you use an AI scribe, this is the "
         "provision to read."),
        ("2", "The penalty is civil, and it is per violation.",
         "Up to $10,000 for each violation, assessed on the severity of "
         "the harm and the circumstances."),
        ("3", "The Board asked for changes before supporting it.",
         "The Board&rsquo;s recommended position was SUPPORT IF AMENDED. "
         "Its analysis asked for consent to be written rather than "
         "verbal, for a clearer line between permitted and prohibited "
         "uses, for the religious-counseling definitions to be made "
         "consistent, and for the jurisdiction question to be settled "
         "where a violator is not a named license type."),
    ]))
    o.append(pk.callout(
        "The practical read",
        ["An AI note-taker or scribe sits on the permitted side, and "
         "acquires a consent duty. A chatbot that talks to your clients "
         "sits on the prohibited side unless it is an FDA-approved, "
         "HIPAA-compliant product. Between those two poles is where the "
         "Board asked for clarification, and where the bill as written "
         "is hardest to apply to a real product.",
         '<a href="' + TELE + '">What the telehealth rule already '
         "requires of a recorded session &rarr;</a>"]))
    o.append("</section>")

    # -------------------------------------------------------------- rest
    o.append('<section class="pk-sec" id="rest">')
    o.append('<p class="pk-k">The rest of the Board&rsquo;s 2026 list</p>')
    o.append('<h2 class="pk-h">Thirteen other bills, four of them '
             "already dead.</h2>")
    o.append('<p class="pk-p">The Board publishes what it is tracking. '
             "Subjects and statuses below are that list as it read on "
             + READ + "; we have not read these bills, and the subject "
             "line is the Board&rsquo;s wording, not ours.</p>")
    o.append(pk.table(
        ["Bill", "Subject", "Status"],
        [[("AB 1988", "m"), "Companion chatbots: crisis interruption "
          "pauses", "Pending"],
         [("AB 1979", "m"), "Health care services: artificial "
          "intelligence", "Pending"],
         [("AB 2011", "m"), "Nonquantitative treatment limitations",
          "Pending"],
         [("AB 2352", "m"), "Medi-Cal providers: nonprofit public "
          "benefit corporations", "Pending"],
         [("AB 2551", "m"), "Health care coverage", "Pending"],
         [("AB 2575", "m"), "Health care services: artificial "
          "intelligence", "Pending"],
         [("SB 934", "m"), "Sexual orientation or gender identity change "
          "efforts: actions for recovery", "Pending"],
         [("SB 993", "m"), "Board of Behavioral Sciences: licensees: "
          "notices", "Pending"],
         [("SB 1445", "m"), "Healing arts", "Pending"],
         [("AB 1558", "m"), "Uniform Emergency Volunteer Health "
          "Practitioners Act", "Dead"],
         [("AB 2259", "m"), "Prisons: mental health", "Dead"],
         [("AB 2511", "m"), "Behavioral health provider comparable worth "
          "study", "Dead"],
         [("SB 1248", "m"), "State agencies: automated decision systems",
          "Dead"]],
        "From the Board&rsquo;s 2026 bills-through-the-Legislature list.",
        620))
    o.append("</section>")

    # -------------------------------------------------------------- next
    o.append('<section class="pk-sec" id="next">')
    o.append('<p class="pk-k">The two dates</p>')
    o.append('<h2 class="pk-h">31 August, then 30 September.</h2>')
    o.append(pk.numbered([
        ("31 Aug 2026", "The last day for each house to pass bills.",
         "A bill still on the floor calendar at the end of that day does "
         "not go to the Governor this year. Final recess begins on "
         "adjournment."),
        ("30 Sept 2026", "The last day for the Governor to sign or veto "
         "anything passed before 1 September.",
         "Signed, vetoed, or allowed to become law without a signature - "
         "the decision is made by this date."),
        ("1 Jan 2027", "When a signed bill would ordinarily take effect.",
         "A statute passed in the regular session takes effect on the "
         "1 January following its enactment, unless it carries an "
         "urgency clause. Neither of these does."),
    ]))
    o.append(pk.checklist("This page has two update dates built into it", [
        "After 31 August 2026 &mdash; passed, or dead. Every status "
        "sentence above is stamped &ldquo;read " + READ + "&rdquo; "
        "precisely so that a reader arriving later can see it has not "
        "been revisited.",
        "After 30 September 2026 &mdash; signed, or vetoed.",
        "If you are reading this after those dates and the page still "
        "says third reading, it is out of date and you should check the "
        "bill on the Legislature&rsquo;s own site before relying on it.",
    ]))
    o.append("</section>")

    # ----------------------------------------------------------- sources
    src, nsrc = pk.sources([
        ("The bills themselves", [
            ("AB 1598 on the Legislature&rsquo;s own site - the place to "
             "read the bill and check its current status", LEG1598),
            ("SB 903 on the Legislature&rsquo;s own site", LEG903),
            ("The text of SB 903, including the proposed sections "
             "4989.80 to 4989.87 quoted above", TEXT903),
        ]),
        ("What the bills do - the Board of Behavioral Sciences&rsquo; "
         "own analyzes, read " + READ, [
            ("The Board&rsquo;s April 2026 analysis of AB 1598, which "
             "it sponsors - the source for every provision listed on "
             "this page", BBS1598),
            ("The Board&rsquo;s May 2026 analysis of SB 903, its "
             "SUPPORT IF AMENDED position, and the amendments it asked "
             "for", BBS903),
            ("The Board&rsquo;s 2026 list of bills through the "
             "Legislature - the source for the thirteen other bills and "
             "which four are dead", BBSLIST),
        ]),
        ("Dates and vote counts", [
            ("The 2026 legislative calendar - 31 August to pass bills, "
             "30 September for the Governor", CAL),
            ("AB 1598 action history", SCAN1598),
            ("SB 903 action history", SCAN903),
            ("California Constitution, article IV, section 8 - when a "
             "statute takes effect", CONST),
        ]),
    ], note="The Legislature&rsquo;s own site blocks automated reading, "
            "so the provisions on this page were read from the "
            "Board&rsquo;s published analyzes and the action histories "
            "rather than from the bill text on leginfo. Leginfo is "
            "linked above because it is where you should check the "
            "current status yourself. This page is a reference, not "
            "legal advice, and neither bill is law.")
    o.append(src)

    o.append("</article>")
    return "".join(o), nsrc


META = pk.meta_block(
    PAGE,
    "California therapy bills 2026: AB 1598, SB 903, and the 31 August "
    "deadline",
    "AB 1598 would end the annual Law and Ethics exam for associates. "
    "SB 903 would set the first rules on AI in therapy. Both were at "
    "third reading on 13 August 2026.",
    "licensure", "reference",
    "What California therapy bills are moving in 2026?",
    "What AB 1598 and SB 903 would change, where each one stood on "
    "18 August 2026, and the two dates that decide them",
    "2 bills at third reading; 31 August to pass",
    weight=4)


def main():
    print("the 2026 bill tracker")
    html_body, nsrc = body()
    head, header, footer, links, scripts = pk.chrome_parts(DONOR)
    html = pk.assemble(head, META, header, html_body, footer, links,
                       scripts)
    p = os.path.join(SITE, PAGE)
    open(p, "w", encoding="utf-8").write(html)
    print("  wrote " + PAGE + ", " + format(len(html), ",d")
          + " bytes, " + str(nsrc) + " sources")

    n = pk.check_page(p, [
        ("the pk wrapper family_pk adopts", 'class="pk-wrap'),
        ("the AB 1598 leginfo link", "202520260AB1598"),
        ("the SB 903 leginfo link", "202520260SB903"),
        ("the Board's AB 1598 analysis", "20260417_pa_item4.pdf"),
        ("the Board's SB 903 analysis", "20260507_item28_d.pdf"),
        ("the Board's 2026 bill list", "bills_through_legislature_2026"),
        ("the legislative calendar", "2026-calendar.pdf"),
        ("the pass-bills deadline", "31 August 2026"),
        ("the Governor's deadline", "30 September 2026"),
        ("the date this page was read", READ),
        ("the proposed AI chapter", "4989.8"),
        ("the link to the hours page", HOURS),
        ("the link to the telehealth page", TELE),
    ], [h for h, _ in JUMPS])

    s = open(p, encoding="utf-8").read()
    art = re.search(r'<article class="pk-wrap[\s\S]*?</article>', s).group(0)
    flat = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", art)).lower()

    # THE GUARD THIS PAGE EXISTS FOR. A tracker that forecasts is a
    # tracker that will be wrong in public. Neither bill is law, and the
    # page has to keep saying so.
    if "neither bill is law" not in flat:
        print("GUARD: the page no longer states that neither bill is law")
        n += 1
    for forecast in ("will become law", "will pass", "is expected to pass",
                     "once it passes", "when it takes effect",
                     "is likely to pass", "will take effect on 1 january",
                     "the new rules require", "you must now",
                     "as of january, therapists must"):
        if forecast in flat:
            print("GUARD: %r forecasts an outcome or states the bill as "
                  "law" % forecast)
            n += 1
    # Every status claim has to be dated, or a reader in October cannot
    # tell that it is stale.
    if flat.count(READ.lower()) < 3:
        print("GUARD: the read date appears %d time(s); status claims "
              "must be dated" % flat.count(READ.lower()))
        n += 1
    if "third reading" not in flat:
        print("GUARD: the page no longer says where the bills actually "
              "stood")
        n += 1

    # House content rules.
    if "LLC" in art:
        print("GUARD: 'LLC' in the article")
        n += 1
    for banned in ("guaranteed", "is hiring", "has openings",
                   "accepting new", "we recommend", "we found that"):
        if banned in flat:
            print("GUARD: banned phrase %r in the article" % banned)
            n += 1

    if n:
        sys.exit(str(n) + " check failure(s)")
    print("  checks passed - 2 bills dated and sourced, no forecast, "
          "13 others listed from the Board's own tracker")


if __name__ == "__main__":
    main()
