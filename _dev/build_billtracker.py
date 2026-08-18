#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Two bills, one deadline - the tracker page, and the lock that keeps it true.

TIER 3 EDITORIAL #1. Built 18 August 2026, thirteen days before the
constitutional deadline that decides both bills.

WHY THIS PAGE EXISTS

AB 1598 and SB 903 were both read a second time and ordered to third
reading on 13 August 2026. Under Art. IV, Sec. 10(c) of the California
Constitution, and Joint Rule 61(b)(17), 31 August 2026 is the last day
for each house to pass bills. Within six weeks each of these is law or
it is dead, and both land squarely on this site's readers:

  AB 1598  three of its five changes are about pre-licensed people -
           the six-year window, the fifth renewal, and what an
           unlicensed registrant has to tell a client.
  SB 903   the first California rules on artificial intelligence in
           psychotherapy. This site had no AI coverage at all before
           this page: one incidental mention, on one school page.

WHY THE PAGE IS WRITTEN AS "WHAT IS ON THE TABLE", NOT "THE LAW IS"

A tracker whose facts expire in thirteen days is a liability. Every
claim here is scoped to a dated status line and to a named version of
the bill, so that when a bill passes or dies the page is UPDATED rather
than FALSIFIED. Nothing on the page says either bill is law, and a
guard below fails the build if that language ever appears.

THE FRESHNESS LOCK - READ THIS BEFORE YOU CURSE AT IT

`STATE` below is the whole point of the file. While it reads "pending"
this builder REFUSES TO RUN after 31 August 2026. That is deliberate: it
converts "somebody should remember to update the tracker" into a build
failure that cannot be ignored, which is the only version of that
promise this project has ever kept. The brief that commissioned this
page put it plainly - update it after 31 Aug and again after 30 Sept, or
do not build it.

To clear the lock: re-check both bills at the sources in SOURCES below,
rewrite the two status blocks and STATUS_CHECKED, then move STATE on
("pending" -> "passed" once the houses have voted -> "resolved" once the
Governor has signed or vetoed). The lock re-arms itself at the next
checkpoint each time.

BUILD NOTES

No `%`-formatting anywhere prose is assembled - concatenation only, per
the standing rule, even though this page happens to carry no literal
percent sign. `pagekit.spelling` is unforgiving about British forms and
the legislative sources are full of them: it is "counseling", "license"
and "practice" throughout, including inside quoted bill text, which is
how the bills themselves spell it.
"""
import os, re, sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pagekit as pk

SITE = pk.SITE
PAGE = "california-therapist-bills-2026.html"
DONOR = "bbs-advertising-rules-2026.html"

# ---------------------------------------------------------------- the lock
STATE = "pending"                 # pending -> passed -> resolved
STATUS_CHECKED = "18 August 2026"
PASS_DEADLINE = date(2026, 8, 31)   # Art. IV, Sec. 10(c); J.R. 61(b)(17)
SIGN_DEADLINE = date(2026, 9, 30)   # Art. IV, Sec. 10(b)(2)

# Pages on this site that already carry the CURRENT rule each bill would
# change. The figures are theirs, not this page's - the guard checks they
# are still there.
HOURS = "amft-3000-hours-california.html"
ADRULES = "bbs-advertising-rules-2026.html"
FEES = "bbs-fees-california-2026.html"
ROUTE = "become-an-mft-california.html"
TELE = "telehealth-rules-california-therapist.html"

FIGURES = [("five renewals", HOURS), ("six years", HOURS)]

# Sources, all read 18 August 2026.
LEG_AB = ("https://leginfo.legislature.ca.gov/faces/"
          "billNavClient.xhtml?bill_id=202520260AB1598")
LEG_SB = ("https://leginfo.legislature.ca.gov/faces/"
          "billNavClient.xhtml?bill_id=202520260SB903")
DD_AB = "https://calmatters.digitaldemocracy.org/bills/ca_202520260ab1598"
DD_SB = "https://calmatters.digitaldemocracy.org/bills/ca_202520260sb903"
LS_AB = "https://legiscan.com/CA/bill/AB1598/2025"
LS_SB = "https://legiscan.com/CA/bill/SB903/2025"
LS_AB_T = "https://legiscan.com/CA/text/AB1598/2025"
LS_SB_T = "https://legiscan.com/CA/text/SB903/2025"
BBS_LIST = ("https://www.bbs.ca.gov/pdf/publications/"
            "bills_through_legislature_2026.pdf")
CALENDAR = ("https://clerk.assembly.ca.gov/sites/clerk.assembly.ca.gov/"
            "files/2026-01/2026-calendar.pdf")

JUMPS = [("clock", "The deadline"),
         ("ab1598", "AB 1598"),
         ("sb903", "SB 903"),
         ("rest", "Dead and still moving"),
         ("next", "What happens next"),
         ("sources", "Sources")]


def plain(u, t):
    """An internal link. No rel/target - those are for outbound only."""
    return '<a href="' + u + '">' + t + "</a>"


def link(u, t):
    return ('<a href="' + u + '" rel="nofollow noopener" target="_blank">'
            + t + "</a>")


def sec(anchor, kicker, head):
    return ('<section class="pk-sec" id="' + anchor + '">'
            '<p class="pk-k">' + kicker + "</p>"
            '<h2 class="pk-h">' + head + "</h2>")


def p(html):
    return '<p class="pk-p">' + html + "</p>"


def h3(t):
    return '<h3 class="pk-h3">' + t + "</h3>"


# --------------------------------------------------------------- the body
def body():
    o = ['<article class="pk-wrap">']

    o.append(pk.hero(
        "Two bills &middot; checked " + STATUS_CHECKED
        + " &middot; neither one is law",
        "Two bills that would change your license are on the floor, and "
        "the deadline is 31 August.",
        "Both were ordered to third reading on 13 August 2026. If a bill "
        "does not clear both houses by 31 August it dies where it "
        "stands, and what survives has until 30 September to be signed "
        "or vetoed. Here is what each one would actually change, in the "
        "version currently in print.",
        [("31 Aug", "last day either house can pass a bill"),
         ("13 Aug", "the day both were sent to third reading"),
         ("5", "changes in AB 1598, three of them pre-licensed"),
         ("30 Sept", "last day to sign or veto what passes")],
        JUMPS))

    # ------------------------------------------------------------- clock
    o.append(sec("clock", "The clock, not the politics",
                 "Two dates decide both of these, and one of them is "
                 "this month."))
    o.append(p(
        "A California bill in the second year of a two-year session has "
        "a hard stop. <b>31 August 2026 is the last day for each house "
        "to pass bills</b> &mdash; that is the Constitution, Article IV, "
        "Section 10(c), carried into the Legislature&rsquo;s own "
        "calendar as Joint Rule 61(b)(17). A bill still sitting on the "
        "floor at the end of that day does not carry over. It is "
        "finished."))
    o.append(p(
        "<b>30 September 2026 is the last day for the Governor to sign "
        "or veto</b> a bill passed before 1 September. So the whole "
        "question, for both of these, is settled inside six weeks of "
        "this page being written."))
    o.append(p(
        "&ldquo;Ordered to third reading&rdquo; means a bill has cleared "
        "its committees in the second house and is waiting for a floor "
        "vote there. It is the last step before passage &mdash; and for "
        "these two, not quite the last one. <b>Both bills were amended "
        "in the second house</b>, which means that after the floor vote "
        "each has to go back to the house it started in for a "
        "concurrence vote. Two votes, not one, inside the same "
        "thirteen days."))
    o.append(pk.callout(
        "What this page is, and is not",
        ["Neither bill described below is law. Each is a bill in print, "
         "at the version named in its status block, and any of it can "
         "change on the floor or disappear entirely.",
         "The status blocks carry the date they were checked. This page "
         "is scheduled for rewriting after 31 August and again after "
         "30 September, because a tracker nobody updates is worse than "
         "no tracker at all."]))
    o.append("</section>")

    # ------------------------------------------------------------ AB1598
    o.append(sec("ab1598", "AB 1598 &middot; Behavioral sciences",
                 "Five changes, and three of them are about people who "
                 "are not licensed yet."))
    o.append(pk.callout(
        "Status &middot; AB 1598, checked " + STATUS_CHECKED,
        ["Last recorded action <b>13 August 2026</b>: read a second time "
         "and ordered to third reading, in its second house. It passed "
         "its first house on 21 May 2026 by 74 votes to none, and was "
         "amended in the second house on 10 June 2026 &mdash; so a "
         "concurrence vote is still owed. The description below is of "
         "<b>the version in print as amended 10 June 2026</b>.",
         "The Board of Behavioral Sciences is listed as the bill&rsquo;s "
         "<b>sponsor</b> on its own 2026 tracking list. That is worth "
         "knowing: this is the licensing board asking for these changes, "
         "not a bill being done to it."],
        big="Not law"))

    o.append(h3("The three that land on pre-licensed people"))
    o.append(pk.numbered([
        ("1", "Six years becomes seven",
         "Right now everything has to fall inside a six-year window: "
         "hours older than six years at the date the Board receives "
         "your application are gone, and an associate registration "
         "renews five times before it expires &mdash; the arithmetic is "
         "worked through on "
         + plain(HOURS, "the 3,000-hours page") + ". The bill makes it "
         "<b>six renewals</b>, with the registration running "
         "<b>seven years</b> from the last day of the month it was "
         "issued. It also moves the experience window to seven years, "
         "and requires the California law and ethics exam to have been "
         "passed no more than seven years before the Board receives the "
         "application for a license &mdash; that last one with a "
         "transitional carve-out for applications received before "
         "1 January 2030. In plain terms: one more year, for the people "
         "closest to running out of it."),
        ("2", "You would have to name your employer to clients",
         "An unlicensed registrant already has to tell clients they are "
         "unlicensed and working under supervision &mdash; what has to "
         "be said, and where, is set out on "
         + plain(ADRULES, "the advertising and disclosure page")
         + ". The bill adds one more item to that disclosure: <b>the "
         "name of the employer</b>, or, if the work is unpaid, the name "
         "of the entity being volunteered for. It is a small sentence "
         "with a real effect, because it makes the arrangement behind "
         "the therapy visible to the client."),
        ("3", "The $20 exam rescoring fee is deleted",
         "The fee charged to have a written examination rescored is "
         "struck from all four licensing acts. It is the smallest thing "
         "in the bill and the easiest to check &mdash; either the "
         "twenty dollars is in the fee schedule next year or it is not. "
         "The rest of what an exam costs is on "
         + plain(FEES, "the fee page") + "."),
    ]))

    o.append(h3("The two that do not"))
    o.append(pk.numbered([
        ("4", "The religious exemption grows an imam",
         "California exempts certain religious officials from the "
         "licensing requirement when they counsel within their role. "
         "The bill adds <b>imam</b> to the list alongside priest, rabbi "
         "and minister, for faith-based counseling delivered through a "
         "recognized faith-based entity. The limits stay: the service "
         "has to sit in a religious or spiritual context, and it does "
         "not extend to diagnosing or treating mental illness."),
        ("5", "A hardship extension",
         "The summary published by Digital Democracy also describes a "
         "two-year hardship extension tied to private practice "
         "employment. This is the one item here worth reading in the "
         "bill text yourself before relying on it &mdash; the "
         "conditions are the whole of it, and they are not something to "
         "take second-hand from a web page, including this one."),
    ]))
    o.append(p(
        "Nobody is explaining these five in plain language, which is the "
        "only reason this page exists. Three of them decide how long a "
        "person has to finish. If your registration is in its fourth or "
        "fifth renewal, the first item is the one to watch on "
        "31 August."))
    o.append("</section>")

    # ------------------------------------------------------------- SB903
    o.append(sec("sb903", "SB 903 &middot; Mental health professionals: "
                 "artificial intelligence",
                 "The first California rules for using AI in a therapy "
                 "practice."))
    o.append(pk.callout(
        "Status &middot; SB 903, checked " + STATUS_CHECKED,
        ["Last recorded action <b>13 August 2026</b>: out of the second "
         "house&rsquo;s appropriations committee, read a second time, "
         "ordered to third reading. It passed its first house on 19 May "
         "2026 by 39 votes to none, and was amended twice in the second "
         "house &mdash; 8 June and 2 July 2026 &mdash; so it too owes a "
         "concurrence vote. The description below is of <b>the version "
         "in print as amended 2 July 2026</b>.",
         "The Board of Behavioral Sciences recorded a position of "
         "<b>support if amended</b> on its 2026 tracking list."],
        big="Not law"))

    o.append(p(
        "This one is not about licensure. It is about the software "
        "already sitting in a lot of practices &mdash; the notetaker, "
        "the intake screener, the scheduling assistant &mdash; and it "
        "draws a line through the middle of that market. The shape of "
        "it is three questions: what you may use it for, what you have "
        "to ask the client first, and what nobody may sell at all."))

    o.append(pk.table(
        ["What the bill does with it", "The provision, as printed"],
        [[("Allows", "f"),
          "Artificial intelligence used for <b>administrative "
          "support</b> &mdash; scheduling, billing, logistics &mdash; "
          "and <b>supplementary support</b>, such as record-keeping, "
          "progress tracking and organizing resources."],
         [("Allows, with consent", "f"),
          "Recording a session, transcribing communications, or "
          "screening and triaging clients. Each needs <b>informed "
          "consent</b> first, and the client has to be told that the "
          "tool is being used and the specific purpose it is being used "
          "for. Consent buried inside a general terms-of-service "
          "agreement does not count."],
         [("Restricts", "f"),
          "AI making a therapeutic decision on its own, communicating "
          "clinically with a client, writing a treatment plan without a "
          "licensed professional&rsquo;s review, detecting emotion, or "
          "triaging &mdash; unless the tool is authorized by the FDA "
          "and meets federal privacy requirements."],
         [("Prohibits", "f"),
          "A provider may &ldquo;not advertise or otherwise purport to "
          "offer psychotherapy services when the services are provided "
          "through the use of companion chatbots.&rdquo; That is the "
          "sentence aimed at the chatbot market rather than at "
          "clinicians."],
         [("Prohibits", "f"),
          "A company or entity may not &ldquo;share, sell, store, or "
          "train their models on any data obtained from "
          "psychotherapy&rdquo; in a manner inconsistent with "
          "applicable law &mdash; which in California means the "
          "Confidentiality of Medical Information Act sits on top of "
          "everything above."]],
        caption="Quoted phrases are from the version in print as "
                "amended 2 July 2026. Everything else is a plain-"
                "language reading of it, and the bill text linked below "
                "is the authority."))

    o.append(p(
        "Enforcement runs through <b>the licensing board</b> &mdash; "
        "the same board that handles everything else about your "
        "license, with the remedies it already has. That is the detail "
        "that turns this from technology policy into a practice "
        "question."))

    o.append(pk.checklist(
        "If you already use an AI notetaker, these are the questions "
        "this bill would make answerable",
        ["Does the client know the tool is being used, and were they "
         "told what it is for &mdash; in a conversation, or in a "
         "paragraph they scrolled past?",
         "Is that consent recorded somewhere other than a checkbox on a "
         "vendor&rsquo;s terms of service?",
         "Does the vendor train models on what it hears? The contract "
         "says, and most people have not read that clause.",
         "Is anything in your setup screening or triaging clients "
         "before a person sees them?",
         "Does anything you publish describe a tool as providing "
         "therapy?"]))
    o.append(p(
        "None of those are new obligations today. All five are the "
        "questions a practice would need answered if this passes, and "
        "four of the five are worth answering either way. Adjacent "
        "practice rules that already apply are on "
        + plain(TELE, "the telehealth page") + "."))
    o.append("</section>")

    # -------------------------------------------------------------- rest
    o.append(sec("rest", "The rest of the 2026 list",
                 "Four bills the Board was tracking are already dead."))
    o.append(p(
        "The Board of Behavioral Sciences publishes what it is watching. "
        "On the list dated May 2026, four had already failed: the "
        "Uniform Emergency Volunteer Health Practitioners Act bill, a "
        "prisons and mental health bill, a study of behavioral health "
        "provider comparable worth, and a bill on automated decision "
        "systems in state agencies. Bills die quietly and there is "
        "rarely an announcement, which is why a list like that one is "
        "worth reading rather than assuming."))
    o.append(p(
        "Still moving on that same list, alongside the two above: "
        "another bill on companion chatbots and crisis interruption, "
        "two more on artificial intelligence in health care services, a "
        "bill on notices the Board sends its licensees, one on "
        "conversion-therapy recovery actions, and several on coverage "
        "and Medi-Cal providers. <b>That list carries a May 2026 date "
        "and status has moved since</b> &mdash; it is the right place "
        "to start and the wrong place to stop."))
    o.append("</section>")

    # -------------------------------------------------------------- next
    o.append(sec("next", "What happens next",
                 "Three outcomes, and the one date that separates "
                 "them."))
    o.append(pk.numbered([
        ("1", "It passes both houses by 31 August",
         "Then it goes to the Governor, who has until 30 September to "
         "sign or veto it. A bill signed in this session generally "
         "takes effect on the following 1 January unless it says "
         "otherwise, so the practical question for anything that "
         "survives is what changes in the new year."),
        ("2", "It does not get a floor vote",
         "Then it is finished. Not paused, not carried over &mdash; a "
         "two-year session ends, and a bill that has not passed by the "
         "deadline dies with it. The subject can come back as a new "
         "bill in a new session, with a new number."),
        ("3", "It passes and is vetoed",
         "Then it is also finished for this year, unless the "
         "Legislature overrides, which effectively does not happen in "
         "California."),
    ]))
    o.append(p(
        "<b>This page will be rewritten after 31 August 2026 and again "
        "after 30 September 2026.</b> That is not a good intention: the "
        "program that builds this page refuses to run once the first of "
        "those dates has passed and the status above still says these "
        "bills are pending. The page cannot go stale quietly."))
    o.append(p(
        "To check either bill yourself between now and then, the "
        "Legislature&rsquo;s own page for it is the authority and is "
        "linked below. The history at the bottom of that page is the "
        "part to read: the last dated line tells you where the bill "
        "actually is, whatever anyone else says about it."))
    o.append("</section>")

    # ----------------------------------------------------------- sources
    src, nsrc = pk.sources([
        ("The bills themselves", [
            ("AB 1598, Behavioral sciences &mdash; the Legislature's "
             "page: text of every version, and the complete history",
             LEG_AB),
            ("SB 903, Mental health professionals: artificial "
             "intelligence &mdash; the Legislature's page", LEG_SB),
            ("AB 1598, the versions in print, including the 10 June "
             "2026 amendments described above", LS_AB_T),
            ("SB 903, the versions in print, including the 2 July 2026 "
             "amendments described above", LS_SB_T),
        ]),
        ("Status and history, as checked on " + STATUS_CHECKED, [
            ("AB 1598 &mdash; Digital Democracy, source of the "
             "13 August 2026 action and of the hardship-extension "
             "summary", DD_AB),
            ("SB 903 &mdash; Digital Democracy, source of the "
             "13 August 2026 action", DD_SB),
            ("AB 1598 &mdash; the dated action history, including the "
             "74-0 first-house vote", LS_AB),
            ("SB 903 &mdash; the dated action history, including the "
             "39-0 first-house vote", LS_SB),
        ]),
        ("The deadlines and the Board's own list", [
            ("2026 tentative legislative calendar &mdash; &ldquo;Aug. 31 "
             "Last day for each house to pass bills&rdquo; and "
             "&ldquo;Sept. 30 Last day for Governor to sign or veto "
             "bills&rdquo;", CALENDAR),
            ("2026 legislation considered by the Board of Behavioral "
             "Sciences &mdash; the sponsor and support-if-amended "
             "positions, and which bills are dead. Dated May 2026",
             BBS_LIST),
            ("California Constitution, Article IV, Section 10 &mdash; "
             "the passage and signing deadlines, and Section 8, the "
             "date a statute takes effect", None),
        ]),
        ("The current rules these bills would change", [
            ("The 3,000-hours page &mdash; the six-year window and the "
             "five renewals as they stand today", HOURS),
            ("The advertising and disclosure page &mdash; what an "
             "unlicensed registrant already has to tell clients",
             ADRULES),
            ("The fee page &mdash; what the Board charges now", FEES),
            ("The route to licensure &mdash; where the exams sit in it",
             ROUTE),
        ]),
    ], note="Every status line above was checked on " + STATUS_CHECKED
            + " and both bills were live at that moment. Neither is law. "
            "A bill can be amended on the floor, and a page cannot be; "
            "the Legislature&rsquo;s own page for each bill is the "
            "authority, not this one. This site earns nothing from any "
            "link on this page and has no position on either bill. "
            "Nothing here is legal advice.")
    o.append(src)

    o.append("</article>")
    return "".join(o), nsrc


META = pk.meta_block(
    PAGE,
    "California therapist bills 2026: AB 1598 and SB 903",
    "AB 1598 and SB 903 are both at third reading with a 31 August 2026 "
    "deadline. What each would change for California therapists, and "
    "what happens next.",
    "licensure", "reference",
    "What would AB 1598 and SB 903 change for California therapists?",
    "Both are at third reading and neither is law; each must pass both "
    "houses by 31 August 2026 or die",
    "2 bills, one deadline: 31 August 2026",
    weight=4)


# --------------------------------------------------------------- the lock
def freshness():
    """Refuse to build a tracker whose status blocks have expired.

    This is the page's most important guard and the one most likely to
    stop a build that has nothing to do with legislation. That is the
    trade the brief asked for: the alternative is a page that keeps
    saying "pending" about a bill that died in August.
    """
    today = date.today()
    if STATE == "pending" and today > PASS_DEADLINE:
        print("GUARD: the status blocks say both bills are pending, and "
              "the deadline for each house to pass bills (" +
              PASS_DEADLINE.isoformat() + ") is behind us. Re-check both "
              "bills, rewrite the two status blocks and STATUS_CHECKED, "
              "and set STATE = \"passed\" (or rewrite the page for a "
              "bill that died).")
        return 1
    if STATE in ("pending", "passed") and today > SIGN_DEADLINE:
        print("GUARD: the Governor's deadline (" + SIGN_DEADLINE.isoformat()
              + ") is behind us and STATE is still " + STATE + ". Every "
              "outcome is now known. Rewrite the page around what "
              "happened and set STATE = \"resolved\".")
        return 1
    return 0


def main():
    print("the 2026 bill tracker")

    bad = freshness()
    if bad:
        sys.exit("1 check failure(s) - the tracker has expired")

    html_body, nsrc = body()
    head, header, footer, links, scripts = pk.chrome_parts(DONOR)
    html = pk.assemble(head, META, header, html_body, footer, links,
                       scripts)
    path = os.path.join(SITE, PAGE)
    open(path, "w", encoding="utf-8").write(html)
    print("  wrote " + PAGE + ", " + format(len(html), ",d")
          + " bytes, " + str(nsrc) + " sources")

    # ---- the current-rule figures must still exist where they are credited
    for fig, src_page in FIGURES:
        s = open(os.path.join(SITE, src_page), encoding="utf-8").read()
        if fig not in re.sub(r"\s+", " ", s):
            print("GUARD: \"" + fig + "\" is credited to " + src_page
                  + ", which no longer contains it")
            bad += 1

    n = pk.check_page(path, [
        ("the pk wrapper family_pk adopts", 'class="pk-wrap'),
        ("the Legislature's page for AB 1598", LEG_AB),
        ("the Legislature's page for SB 903", LEG_SB),
        ("the Board's own 2026 bill list", BBS_LIST),
        ("the legislative calendar", CALENDAR),
        ("the 3,000-hours page", HOURS),
        ("the disclosure page", ADRULES),
        ("the fee page", FEES),
        ("the telehealth page", TELE),
        # The five AB 1598 changes. Each is the reason a reader is here.
        ("the seven-year registration", "seven years"),
        ("the sixth renewal", "six renewals"),
        ("the employer disclosure", "name of the employer"),
        ("the rescoring fee", "$20"),
        ("the religious exemption", "imam"),
        # The limit is the fact, not the addition: this exemption has
        # never reached diagnosis or treatment, and a reader who takes
        # only the headline away has been misinformed.
        ("the limit on the religious exemption",
         "religious or spiritual context"),
        ("the registration term", "seven years</b> from the last day"),
        ("the 2030 carve-out", "1 January 2030"),
        # The SB 903 provisions.
        ("the permitted administrative use", "administrative "),
        ("the consent requirement", "informed consent"),
        ("the chatbot advertising ban", "companion chatbots"),
        ("the training-data restriction", "train their models"),
        ("the confidentiality overlay",
         "Confidentiality of Medical Information Act"),
        # The two dates the whole page hangs on.
        ("the passage deadline", "31 August"),
        ("the signing deadline", "30 September"),
        ("the date the status was checked", STATUS_CHECKED),
    ], [h for h, _ in JUMPS])

    s = open(path, encoding="utf-8").read()
    art = pk.article(s)
    flat = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", art)).lower()

    # ---- NOTHING HERE MAY READ AS SETTLED LAW. The single failure mode
    # this page has: a sentence that describes a bill as though it had
    # already passed. Both bills must be labelled not law, by name.
    if flat.count("not law") < 2:
        print("GUARD: each bill needs its own \"not law\" label and only "
              + str(flat.count("not law")) + " survived")
        bad += 1
    for wrong in ("is now law", "became law", "the new law", "as of "
                  "january 1 you must", "now requires", "takes effect "
                  "this year"):
        if wrong in flat:
            print("GUARD: \"" + wrong + "\" states as settled something "
                  "that is still a bill")
            bad += 1
    # ---- and it must say when it will be rewritten, in the body
    for must, why in (("31 august 2026 and again", "the update promise"),
                      ("third reading", "the procedural posture"),
                      ("concurrence", "the second vote nobody explains")):
        if must not in flat:
            print("GUARD: " + why + " (\"" + must + "\") is missing")
            bad += 1

    # ---- the standing site guards
    for track in ("?ref=", "&ref=", "?aff", "&aff", "utm_", "?tap_",
                  "impact.com", "shareasale", "partnerize", "?a_aid",
                  "clickbank", "?pa=", "avantlink"):
        if track in art:
            print("GUARD: links must stay plain - found \"" + track + "\"")
            bad += 1
    if "earns nothing" not in flat:
        print("GUARD: the page no longer states that the site earns "
              "nothing from these links")
        bad += 1
    for wrong in ("we found that", "our testing shows", "the best course",
                  "we recommend buying"):
        if wrong in flat:
            print("GUARD: \"" + wrong + "\" turns a quotation into an "
                  "endorsement")
            bad += 1
    for phrase in ("is hiring", "has openings", "guaranteed",
                   "accepting new"):
        if phrase in flat:
            print("GUARD: banned phrase \"" + phrase + "\" in the article")
            bad += 1
    if "LLC" in art:
        print("GUARD: 'LLC' in the article")
        bad += 1

    # ---- the meta description has a hard ceiling in seo_rules
    desc = re.search(r'<meta name="description" content="([^"]*)"', s)
    dlen = len(desc.group(1)) if desc else 0
    if not 70 <= dlen <= 168:
        print("GUARD: the meta description is " + str(dlen)
              + " characters; seo_rules wants 70 to 168")
        bad += 1

    if n or bad:
        sys.exit(str(n + bad) + " check failure(s)")
    print("  checks passed - 2 bills labelled not law, both deadlines "
          "present, description " + str(dlen) + " chars, "
          + str(nsrc) + " sources")
    print("  freshness lock armed: this builder stops working after "
          + PASS_DEADLINE.isoformat())


if __name__ == "__main__":
    main()
