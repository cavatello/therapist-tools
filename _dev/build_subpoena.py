#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A subpoena arrived. It is not a court order, and you must claim the privilege.

TIER 3 EDITORIAL #1c. The brief's description of the gap was exact: high
anxiety, high search, and the free material is bad. Two distinctions decide
almost everything and almost nothing states them plainly.

ONE. A SUBPOENA IS NOT A COURT ORDER

Code of Civil Procedure section 2020.210(b): "An attorney of record for any
party may sign and issue a deposition subpoena." No judge has read it. The
clerk's own version issues "signed and sealed, but otherwise in blank" -
the paper arrives looking judicial because it IS court paper, filled in by
the other side's lawyer. Everything that reads as an instruction on it is
a demand by a party to a lawsuit you are not in.

TWO. CLAIMING THE PRIVILEGE IS NOT OPTIONAL

Evidence Code section 1015 is one sentence and it says SHALL:

    "The psychotherapist who received or made a communication subject to
    the privilege under this article shall claim the privilege whenever he
    is present when the communication is sought to be disclosed and is
    authorized to claim the privilege under subdivision (c) of Section
    1014."

The privilege belongs to the patient (section 1014). The therapist is its
custodian when the patient is not there to hold it. So the frightened
question - "am I allowed to refuse?" - is the wrong way round. The default
is that you assert it and let the court decide, and handing the file over
because the paper looked official is the failure mode.

WHAT THE PAGE DELIBERATELY DOES NOT DO

It does not tell anyone what to do in their own matter, and a guard fails
the build if the not-legal-advice line and the call-your-insurer line both
disappear. This site is not a lawyer and the whole shape of the page is
"here is what the paper is, here is the clock you are on, here is who to
phone today" - not "here is your answer".

The insurer point is not filler. This site's own liability-insurance page
already establishes, from the public record, that a records subpoena is
the MOST COMMONLY REPORTED USE of a therapist's policy, and that the
policies carry subpoena-assistance sublimits and an attorney helpline. The
reader almost certainly already owns the help they need and does not know
it. That is the most useful sentence on the page and it is carried, not
invented.

SOURCING. leginfo blocks automated fetching, so statute text was read from
Justia, FindLaw and the Sacramento County Public Law Library's own guide,
and leginfo is linked as the place to read the section. Every day count
below is from the statute or that guide, and every one of them is the kind
of number that gets misremembered - which is why they are guarded.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pagekit as pk

SITE = pk.SITE
PAGE = "subpoena-california-therapist.html"
DONOR = "bbs-advertising-rules-2026.html"

READ = "18 August 2026"

INS = "therapy-liability-insurance-california.html"
CASE = "discipline-case-billed-for-sessions-that-never-happened.html"
EHR = "therapynotes-vs-simplepractice-california.html"
TELE = "telehealth-rules-california-therapist.html"
ADRULES = "bbs-advertising-rules-2026.html"

# Carried from this site, not computed here.
FIGURES = [("most commonly reported use", INS), ("$10,000", INS),
           ("Subpoena assistance", INS), ("shredded", CASE),
           ("seven years", EHR)]

# Statutes. leginfo is linked in the site's established pattern; the text
# was read at the mirrors below, and the page says so.
def leg(code, section):
    return ("https://leginfo.legislature.ca.gov/faces/"
            "codes_displaySection.xhtml?lawCode=" + code
            + "&sectionNum=" + section + ".")


EVID1014 = leg("EVID", "1014")
EVID1015 = leg("EVID", "1015")
CCP1985_3 = leg("CCP", "1985.3")
CCP1987_1 = leg("CCP", "1987.1")
CCP2020_210 = leg("CCP", "2020.210")
J1015 = ("https://law.justia.com/codes/california/code-evid/division-8/"
         "chapter-4/article-7/section-1015/")
F2020 = ("https://codes.findlaw.com/ca/code-of-civil-procedure/"
         "ccp-sect-2020-210/")
F1987 = ("https://codes.findlaw.com/ca/code-of-civil-procedure/"
         "ccp-sect-1987-1/")
SACLAW = ("https://saclaw.org/resource_library/"
          "discovery-business-records-subpoena-for-consumer-employee-records/")
HIPAA = ("https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/"
         "part-164/subpart-E/section-164.512")

JUMPS = [("today", "What to do today"),
         ("what", "What the paper is"),
         ("privilege", "You must claim it"),
         ("clock", "The clock"),
         ("kinds", "Records or testimony"),
         ("never", "What never helps"),
         ("sources", "Sources")]


def plain(u, t):
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


def body():
    o = ['<article class="pk-wrap">']

    o.append(pk.hero(
        "Read this first &middot; checked " + READ + " &middot; not legal "
        "advice",
        "A subpoena is not a court order, and claiming the privilege is "
        "not optional.",
        "Two sentences of California law decide most of what happens "
        "next, and almost nothing written for therapists says them "
        "plainly. An attorney of record can sign and issue a subpoena "
        "with no judge involved. And the Evidence Code does not say you "
        "<i>may</i> claim your client&rsquo;s privilege &mdash; it says "
        "you <b>shall</b>. Here is what the paper actually is, what "
        "clock you are on, and who to phone today.",
        [("0", "judges who read it before it was sent"),
         ("shall", "the word the Evidence Code uses"),
         ("5", "days before production a client can object"),
         ("1", "phone call you almost certainly already own")],
        JUMPS))

    # ------------------------------------------------------------- today
    o.append(sec("today", "Before anything else",
                 "Three things to do today, in this order."))
    o.append(pk.numbered([
        ("1", "Do not send the records. Do not confirm the client "
         "exists.",
         "Acknowledging that somebody is or was your client is itself a "
         "disclosure. Nothing on the paper requires you to answer it "
         "today, and the deadline on it is later than it looks &mdash; "
         "see the clock below."),
        ("2", "Phone your liability insurer&rsquo;s attorney helpline.",
         "This is the sentence most worth reading on this page. On this "
         "site&rsquo;s own reading of the public record, a subpoena for "
         "records is the <b>most commonly reported use</b> of a "
         "California therapist&rsquo;s liability policy &mdash; not "
         "being sued. The policies carry subpoena assistance and "
         "deposition sublimits, some at $10,000, and an attorney line "
         "you have already paid for. "
         + plain(INS, "Which policies carry what &rarr;")),
        ("3", "Diary the dates on the paper, and keep the envelope.",
         "The production date, the date you were served, and how you "
         "were served all matter, because the notice periods below run "
         "from them. Write down when it arrived while you still "
         "remember."),
    ]))
    o.append(pk.callout(
        "What this page is",
        ["An explanation of the document and the procedure around it, "
         "with every rule linked to the statute it comes from. It is "
         "<b>not legal advice</b>, it cannot be, and no page can be: "
         "what you should do turns on the case, the client, the court "
         "and what is actually being asked for. The point of it is to "
         "make the first hour calmer and better informed, and to make "
         "the call to a lawyer a shorter one."]))
    o.append("</section>")

    # -------------------------------------------------------------- what
    o.append(sec("what", "The distinction everything else rests on",
                 "It is court paper. That is not the same as a judge "
                 "having ordered anything."))
    o.append(p(
        "California&rsquo;s Code of Civil Procedure says that "
        "&ldquo;the clerk of the court in which the action is pending "
        "shall issue a deposition subpoena signed and sealed, but "
        "otherwise in blank&rdquo; &mdash; and then, in the very next "
        "subdivision, that <b>&ldquo;an attorney of record for any party "
        "may sign and issue a deposition subpoena.&rdquo;</b> That is "
        "section 2020.210. A subpoena is a demand made by one side of "
        "somebody else&rsquo;s lawsuit. It carries real consequences and "
        "it cannot be ignored, and it has also never been read by a "
        "judge."))
    o.append(p(
        "A <b>court order</b> is the other thing. A judge has considered "
        "the question and decided it, and the difference is not "
        "academic: under the federal privacy rule, with a court order a "
        "covered entity may disclose only &ldquo;the protected health "
        "information expressly authorized by such order&rdquo;, while a "
        "bare subpoena requires satisfactory assurance that the person "
        "was notified and given a chance to object, or that a qualified "
        "protective order is in place. Same file, two entirely different "
        "duties."))
    o.append(pk.table(
        ["", "Subpoena", "Court order"],
        [["Who signed it", "An attorney for one of the parties, or the "
          "clerk in blank", "A judge"],
         ["Has anyone weighed your client&rsquo;s privacy",
          ("No", "f"), ("Yes, that is what the order is", "f")],
         ["What you disclose", "Nothing yet &mdash; the privilege "
          "question comes first",
          "Only what the order expressly authorizes"],
         ["Can it be challenged", "Yes &mdash; objection, or a motion to "
          "quash under section 1987.1",
          "It has already been decided; compliance is the question"]],
        caption="Federal duties from 45 CFR 164.512(e); issuance from "
                "Code of Civil Procedure section 2020.210. Both linked "
                "below.", minw=620))
    o.append("</section>")

    # --------------------------------------------------------- privilege
    o.append(sec("privilege", "The sentence nobody quotes",
                 "You are not deciding whether to protect the record. "
                 "You are required to."))
    o.append(pk.quote(
        "California Evidence Code section 1015, in full",
        ["&ldquo;The psychotherapist who received or made a "
         "communication subject to the privilege under this article "
         "<b>shall claim the privilege</b> whenever he is present when "
         "the communication is sought to be disclosed and is authorized "
         "to claim the privilege under subdivision (c) of Section "
         "1014.&rdquo;"]))
    o.append(p(
        "The privilege belongs to the patient, not to you &mdash; "
        "section 1014 makes the patient the holder, and lets the "
        "psychotherapist claim it on their behalf when the holder is not "
        "there to do it. Section 1015 then turns that permission into a "
        "duty. So the question people arrive with, <i>am I allowed to "
        "refuse</i>, has the wrong shape. Asserting the privilege and "
        "letting a court resolve it is the ordinary course. Producing "
        "the file because the paper looked official is the thing that "
        "goes wrong."))
    o.append(p(
        "None of that means the privilege always wins. There are "
        "exceptions, a client can waive it, a client who has put their "
        "own mental condition in issue may have already narrowed it, and "
        "a judge can order production after hearing the argument. It "
        "means the decision is not yours to make quietly, on your own, "
        "on the day the envelope arrives."))
    o.append("</section>")

    # ------------------------------------------------------------- clock
    o.append(sec("clock", "The clock you are actually on",
                 "The procedure assumes your client gets a chance to "
                 "object, and builds in the days for it."))
    o.append(p(
        "Where the records sought are a person&rsquo;s own &mdash; which "
        "is what a therapy file is &mdash; Code of Civil Procedure "
        "section 1985.3 puts a notice procedure in front of production. "
        "The person whose records they are gets told, and gets time. The "
        "day counts below are from the statute and the Sacramento County "
        "Public Law Library&rsquo;s guide to it, read " + READ + "."))
    o.append(pk.table(
        ["Step", "When"],
        [["The subpoena and a Notice to Consumer are served on the "
          "client whose records are sought",
          ("at least 25 days before the production date", "f")],
         ["Or, where the client is served personally",
          ("at least 20 days before", "f")],
         ["The subpoena is served on you, the record holder",
          ("at least 15 days before the production date", "f")],
         ["The client can serve a written objection",
          ("up to 5 days before the production date", "f")],
         ["Once an objection has been served, production",
          ("does not happen unless the court orders it", "f")]],
        caption="Code of Civil Procedure section 1985.3. A client who is "
                "already a party to the case objects by moving to quash "
                "rather than on the form.", minw=620))
    o.append(p(
        "Two things follow that are worth saying out loud. First, the "
        "date on the paper is a <b>production date</b>, not a deadline "
        "to reply by return of post &mdash; there is room to take "
        "advice. Second, if the notice procedure was not followed "
        "properly, that is itself something to raise rather than "
        "something to quietly absorb."))
    o.append(pk.callout(
        "Objection, or a motion to quash",
        ["Section 1987.1 lets a party, a witness, or the client whose "
         "records are sought ask the court to quash the subpoena "
         "entirely, modify it, or impose conditions &mdash; and it says "
         "the court may make any other order appropriate to protect a "
         "person from &ldquo;unreasonable or oppressive demands, "
         "including unreasonable violations of the right of privacy of "
         "the person&rdquo;.",
         "You are the witness in that sentence. So is the file."]))
    o.append("</section>")

    # ------------------------------------------------------------- kinds
    o.append(sec("kinds", "Two different documents, two different "
                 "problems",
                 "What you do about a records subpoena is not what you "
                 "do about a testimony subpoena."))
    o.append(pk.numbered([
        ("1", "A subpoena for records",
         "It wants the file, or part of it. The questions are what is "
         "actually being asked for, whether the notice procedure was "
         "followed, whether the privilege is asserted, and &mdash; if "
         "production is eventually ordered &mdash; how narrow it can be "
         "made. You may never appear anywhere. This is the common one, "
         "and it is the one your policy is most often used for."),
        ("2", "A subpoena to testify",
         "It wants you, in person, under oath. Everything above about "
         "privilege still applies, and now there is a second set of "
         "problems: what you can be asked, what you must decline to "
         "answer, and whether you are being treated as a fact witness "
         "or drifted into giving an expert opinion about someone you "
         "treated. Preparation for this is exactly what an insurer&rsquo;s "
         "appointed attorney does."),
        ("3", "And one document can be both",
         "California has a subpoena that commands production of records "
         "<i>and</i> the attendance and testimony of the person holding "
         "them. Read which one you have before deciding anything; people "
         "answer the wrong one."),
    ]))
    o.append("</section>")

    # ------------------------------------------------------------- never
    o.append(sec("never", "The three that make it worse",
                 "Each of these is common, and each turns a manageable "
                 "problem into a different one."))
    o.append(pk.numbered([
        ("1", "Sending the whole file to be helpful",
         "Over-production cannot be undone. The privilege question "
         "applies to what is asked for, and what is asked for is "
         "frequently broader than what the case could possibly need "
         "&mdash; which is precisely what a motion to quash or a "
         "protective order is for."),
        ("2", "Ignoring it",
         "A subpoena not being a court order does not make it optional. "
         "It has a procedure attached, and the procedure includes the "
         "other side going to a judge. The distinction on this page buys "
         "you standing and time, not the ability to file it in a "
         "drawer."),
        ("3", "Tidying the record first",
         "This is the one that ends careers rather than cases. This "
         "site&rsquo;s discipline library carries a case where a "
         "therapist told a state investigator the subpoenaed records had "
         "been <b>shredded</b>, in a matter where a client&rsquo;s own "
         "signed form was later shown to have been altered. Whatever the "
         "file says, it says it. California expects records to be kept "
         "for seven years in any event &mdash; that arithmetic is on "
         + plain(EHR, "the records-storage comparison")
         + ". " + plain(CASE, "The case &rarr;")),
    ]))
    o.append(p(
        "If the request has arrived because of something you did rather "
        "than something a client is litigating, that is a different "
        "page: what the Board can do and what a policy covers is on "
        + plain(INS, "the liability insurance page") + ", and what you "
        "are required to tell clients about your own status is on "
        + plain(ADRULES, "the advertising and disclosure page") + "."))
    o.append("</section>")

    # ----------------------------------------------------------- sources
    src, nsrc = pk.sources([
        ("The two sentences the page turns on", [
            ("Evidence Code section 1015 - the psychotherapist "
             "&ldquo;shall claim the privilege&rdquo;", EVID1015),
            ("The same section, as read for this page", J1015),
            ("Evidence Code section 1014 - the patient is the holder, "
             "and when the psychotherapist may claim it", EVID1014),
            ("Code of Civil Procedure section 2020.210 - the clerk "
             "issues in blank, and an attorney of record may sign and "
             "issue", CCP2020_210),
            ("The same section, as read for this page", F2020),
        ]),
        ("The procedure and the days", [
            ("Code of Civil Procedure section 1985.3 - notice to the "
             "person whose records are sought", CCP1985_3),
            ("Sacramento County Public Law Library, business records "
             "subpoena for consumer records - the source of the 25, 20, "
             "15 and 5 day counts above", SACLAW),
            ("Code of Civil Procedure section 1987.1 - who may move to "
             "quash, and the protective orders a court may make",
             CCP1987_1),
            ("The same section, as read for this page", F1987),
            ("45 CFR 164.512(e) - what may be disclosed for a judicial "
             "proceeding with a court order, and what a bare subpoena "
             "requires instead", HIPAA),
        ]),
        ("Carried from pages on this site", [
            ("Liability insurance compared - that a records subpoena is "
             "the most commonly reported use of a policy, the subpoena "
             "and deposition sublimits, and the attorney helplines",
             INS),
            ("The discipline case in which subpoenaed records had been "
             "shredded", CASE),
            ("Where the seven-year retention arithmetic is worked, and "
             "what each option costs", EHR),
            ("The telehealth standard of practice, for what a recorded "
             "session already asks of you", TELE),
        ]),
    ], note="leginfo blocks automated reading, so each statute above was "
            "read at the mirror linked beside it and leginfo is linked "
            "as the place to read the section itself. The day counts "
            "come from section 1985.3 and the law library guide and were "
            "checked on " + READ + ". <b>Nothing on this page is legal "
            "advice</b> and no page can be: what to do about a "
            "particular subpoena depends on the case, the client and "
            "what is being asked for. Call the attorney line on your "
            "liability policy first &mdash; you have already paid for "
            "it. This site earns nothing from any link here and has no "
            "relationship with any insurer, law firm or vendor named on "
            "it.")
    o.append(src)

    o.append("</article>")
    return "".join(o), nsrc


META = pk.meta_block(
    PAGE,
    "Subpoenaed as a California therapist: what to do first",
    "A subpoena is not a court order, and Evidence Code 1015 says you "
    "shall claim your client's privilege. What the paper is, the notice "
    "clock, and who to call.",
    "practice", "guide",
    "A subpoena arrived for my client's records. What do I do?",
    "Do not produce, call the attorney line on your policy, and assert "
    "the privilege the Evidence Code requires you to assert",
    "0 judges have read it before it reaches you",
    weight=5)


def main():
    print("the subpoena page")
    html_body, nsrc = body()
    head, header, footer, links, scripts = pk.chrome_parts(DONOR)
    html = pk.assemble(head, META, header, html_body, footer, links,
                       scripts)
    path = os.path.join(SITE, PAGE)
    open(path, "w", encoding="utf-8").write(html)
    print("  wrote " + PAGE + ", " + format(len(html), ",d")
          + " bytes, " + str(nsrc) + " sources")

    bad = 0
    for fig, src_page in FIGURES:
        s = re.sub(r"\s+", " ",
                   open(os.path.join(SITE, src_page),
                        encoding="utf-8").read())
        if fig not in s:
            print("GUARD: \"" + fig + "\" is credited to " + src_page
                  + ", which no longer contains it")
            bad += 1

    n = pk.check_page(path, [
        ("the pk wrapper family_pk adopts", 'class="pk-wrap'),
        # Every statute the page rests on, by number.
        ("Evidence Code 1015", "sectionNum=1015."),
        ("Evidence Code 1014", "sectionNum=1014."),
        ("CCP 1985.3", "sectionNum=1985.3."),
        ("CCP 1987.1", "sectionNum=1987.1."),
        ("CCP 2020.210", "sectionNum=2020.210."),
        ("the federal rule", "164.512"),
        # The two distinctions the page exists for.
        ("the issuance quote", "may sign and issue a deposition subpoena"),
        # Keyed on the LONG phrase, not "shall claim the privilege" -
        # that shorter string also appears in the source description
        # below, so the guard passed with the quotation block gutted.
        # Third time this trap has been hit across these builders: key a
        # content guard on words that appear ONCE, in the sentence that
        # carries the claim.
        ("the mandatory-claim quote",
         "whenever he is present when "),
        ("the records-or-testimony split", "subpoena to testify"),
        # The notice clock, every count.
        ("the 25-day count", "25 days"),
        ("the 20-day count", "20 days"),
        ("the 15-day count", "15 days"),
        ("the 5-day count", "5 days"),
        # The carried material.
        ("the insurance page", INS),
        ("the discipline case", CASE),
        ("the storage page", EHR),
    ], [h for h, _ in JUMPS])

    s = open(path, encoding="utf-8").read()
    art = pk.article(s)
    flat = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", art)).lower()

    # ---- THE TWO SENTENCES THIS PAGE MAY NOT SHIP WITHOUT. It is a page
    # about a legal emergency, written by people who are not lawyers. If
    # either the disclaimer or the call-your-insurer instruction is ever
    # edited away, the page stops being safe to publish.
    if "not legal advice" not in flat:
        print("GUARD: the not-legal-advice line has gone from a page "
              "about what to do when you are served")
        bad += 1
    if "attorney" not in flat or "helpline" not in flat:
        print("GUARD: the instruction to call the attorney line on your "
              "own policy has gone - it is the most useful sentence on "
              "the page and the only concrete action a reader can take "
              "today")
        bad += 1
    # ---- and it may not tell anyone what the answer is
    for wrong in ("you should refuse", "you must refuse", "simply refuse",
                  "you do not have to comply", "just ignore",
                  "you are not required to respond"):
        if wrong in flat:
            print("GUARD: \"" + wrong + "\" states an outcome this page "
                  "is not entitled to state. The page explains the "
                  "procedure; it does not decide anybody's matter.")
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
            print("GUARD: \"" + wrong + "\" reads as an endorsement")
            bad += 1
    for phrase in ("is hiring", "has openings", "guaranteed",
                   "accepting new"):
        if phrase in flat:
            print("GUARD: banned phrase \"" + phrase + "\" in the article")
            bad += 1
    if "LLC" in art:
        print("GUARD: 'LLC' in the article")
        bad += 1

    desc = re.search(r'<meta name="description" content="([^"]*)"', s)
    dlen = len(desc.group(1)) if desc else 0
    if not 70 <= dlen <= 168:
        print("GUARD: the meta description is " + str(dlen)
              + " characters; seo_rules wants 70 to 168")
        bad += 1

    if n or bad:
        sys.exit(str(n + bad) + " check failure(s)")
    print("  checks passed - 5 statutes cited, both distinctions intact, "
          "4 notice counts, disclaimer and helpline present, "
          "description " + str(dlen) + " chars, " + str(nsrc) + " sources")


if __name__ == "__main__":
    main()
