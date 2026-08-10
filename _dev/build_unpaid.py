#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""You were not paid for the notes: the wage claim an associate can actually file.

THE QUESTION THIS ANSWERS

The most-discussed thread in a California AMFT/ASW/APCC support group in the
period this page was researched - 77 reactions and 86 comments - was somebody
describing unpaid non-clinical hours at a private practice: notes written after
hours, no-shows, required supervision, staff meetings, none of it paid. They
went to the Board of Behavioral Sciences. The Board declined and suggested a
wage claim against their own supervisor.

Eighty-six comments followed, almost all of them guesses.

WHY THE BOARD DECLINED, AND WHY THAT IS NOT A BRUSH-OFF

The Board is not a wage regulator, and nothing it publishes claims to be. Its
complaint form, its enforcement flyer and the seventeen separate attestations
on the MFT Supervisor Responsibility Statement are all silent on paying the
supervisee. The statute the Board enforces says an associate must be an
employee or a volunteer and not a contractor; it does not say what an employee
must be paid, because that is the Labor Code's job and the Labor
Commissioner's.

That is a finding established by absence, which this page states as such. It
does not say "the Board has no jurisdiction"; it says which documents were
read and what was not in them.

THE FOUR THINGS NOBODY IN THE THREAD KNEW

1. **The claim is free to file.** Nothing in DLSE Form 1 or the online filing
   system mentions a fee, and the word does not appear on the form.
2. **Liquidated damages are available at the Labor Commissioner**, not only in
   court. Labor Code 1194.2 doubles the minimum-wage portion, and Form 1 has a
   tick box for it.
3. **Per-session pay is piece rate.** Labor Code 226.2 requires non-productive
   time to be paid separately, and forbids averaging the session rate across
   the hours between sessions. The DIR's own definition page offers "nurses
   compensated by number of procedures performed" as an example.
4. **A licensing board's permission to work unpaid is not a wage-and-hour
   exemption.** BPC 4980.43.3(a) allows volunteer hours. The US Department of
   Labor states that employees may not volunteer services to for-profit
   private sector employers. Both are true, and the page ends on that.

WHAT IS DELIBERATELY NOT ON THE PAGE

Advice about whether to file. The page is about what the mechanism is and what
it is worth, because the thread's actual failure was that nobody knew either.
And no prediction of outcome: the estimator computes what a claim is *worth on
its face*, labelled as such, and says plainly that it is not a forecast.

Idempotent - rewrites its page from scratch every run. Guarded.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import pagekit as pk

PAGE = "associate-unpaid-hours-california.html"
DONOR = "hiring-first-associate-california-therapist.html"

HIRING = "hiring-first-associate-california-therapist.html"
ASSOCPAY = "associate-therapist-pay-los-angeles-bay-area.html"
HOURS = "amft-3000-hours-california.html"
ADVISOR = "associate-mft-job-advisor.html"

# Labor Code numbers used in more than one place, so a correction lands once.
SOL_YEARS = 3
DETERMINATION_DAYS = 30
HEARING_DAYS = 90
DECISION_DAYS = 15
WAITING_CAP_DAYS = 30
INTEREST = 10.0
STUB_FIRST = 50
STUB_LATER = 100
STUB_CAP = 4000
NONCLIN_CAP = 1250
TOTAL_HOURS = 3000

JUMPS = [
    ("board", "Why the Board declined"),
    ("claim", "How the claim works"),
    ("worth", "What it is worth"),
    ("piece", "Per-session is piece rate"),
    ("volunteer", "The volunteer problem"),
    ("hours", "Do the hours still count?"),
]


def body():
    o = ['<article class="pk-wrap">']

    o.append(pk.hero(
        "Unpaid hours &middot; the Labor Commissioner &middot; checked %s"
        % pk.CHECKED,
        "You were not paid for the notes.",
        "The Board of Behavioral Sciences does not regulate what your "
        "supervisor pays you. <b>Somebody else does</b>, the claim costs "
        "nothing to file, and the law may double part of what you are owed.",
        [("$0", "published filing fee"),
         ("%d years" % SOL_YEARS, "to file an unpaid-wages claim"),
         ("%d days" % DETERMINATION_DAYS, "to a decision on how it proceeds"),
         ("2&times;", "the minimum-wage portion, if awarded")],
        JUMPS))

    # ------------------------------------------------------------ the question
    o.append('<section class="pk-sec">')
    o.append(pk.quote(
        "The post, and eighty-six comments of guesses",
        ["I&rsquo;m an associate at a private practice. I get paid per "
         "session. I don&rsquo;t get paid for notes, for no-shows, for the "
         "staff meeting, or for the supervision <b>the Board requires me to "
         "attend</b>. I asked the BBS. They told me they couldn&rsquo;t help "
         "and that I should file a wage claim &mdash; against my own "
         "supervisor."]))

    o.append('<p class="pk-k">The short version</p>')
    o.append('<h2 class="pk-h">The Board was right, and it was not brushing '
             "you off.</h2>")
    o.append('<p class="pk-d">Two different systems govern your associateship '
             "and they do not overlap. One decides whether your hours count "
             "toward licensure. The other decides whether you have to be paid "
             "for them. The Board runs the first and has no part in the "
             "second, which is why its answer sounded like a shrug and was "
             "not one.</p>")

    o.append(pk.numbered([
        ("1", "The Board regulates the hours, not the wage",
         "Business and Professions Code &sect;4980.43.3(a) requires an "
         "associate to be an <b>employee or a volunteer, never an "
         "independent contractor</b>. That is as far as the Board&rsquo;s "
         "statute goes into your pay. It does not set a rate, it does not "
         "require that any particular hour be paid, and the Board publishes "
         "nothing that says otherwise."),
        ("2", "The Labor Commissioner regulates the wage",
         "California&rsquo;s Division of Labor Standards Enforcement takes "
         "unpaid-wage claims from any employee against any employer, with "
         "<b>no fee, no lawyer required, and no minimum amount</b>. A "
         "therapy practice is an employer like any other. Being supervised "
         "by the person you are claiming against changes nothing about your "
         "standing."),
        ("3", "Per-session pay is piece-rate pay",
         "This is the part that decides most of these cases. Under Labor "
         "Code &sect;226.2 an employer paying by the piece must pay "
         "<b>separately</b> for time that is not spent on the piece &mdash; "
         "and may not average the session rate across it. Notes, no-shows, "
         "meetings and the supervision your registration requires are that "
         "time."),
        ("4", "&ldquo;You agreed to it&rdquo; is not a defense",
         "Minimum wage cannot be waived by agreement, and an agreement to "
         "work unpaid does not become lawful because a licensing board "
         "permits volunteers. Those are two different bodies of law giving "
         "two different answers, and the section at the foot of this page is "
         "about what happens where they collide."),
    ]))
    o.append("</section>")

    # -------------------------------------------------------------- the Board
    o.append('<section class="pk-sec" id="board">')
    o.append('<p class="pk-k">Established by absence</p>')
    o.append('<h2 class="pk-h">What the Board publishes about your pay: '
             "nothing.</h2>")
    o.append('<p class="pk-d">This is a claim about what is <i>not</i> in a '
             "set of documents, so here are the documents. Each was read in "
             "full, and none of them mentions the supervisee&rsquo;s wage, "
             "the rate, or whether any hour must be paid at all.</p>")
    o.append(pk.table(
        ["What was read", "What it covers", "On paying the supervisee"],
        [["Consumer Complaint form (comp-2a)",
          "The form the Board gives the public and licensees for reporting a "
          "licensee. Lists the conduct it wants reported.",
          ("Silent", "m")],
         ["Complaints and the courts flyer",
          "The Board&rsquo;s own explanation of what its enforcement "
          "program can and cannot do for a complainant.",
          ("Silent", "m")],
         ["MFT Supervisor Responsibility Statement (mfrespon)",
          "Seventeen numbered attestations a supervisor signs, covering "
          "everything the Board holds them to.",
          ("Silent", "m")],
         ["Supervision Agreement, 37M-300",
          "Signed by both parties within 60 days. Item 16 requires the "
          "supervisor to confirm W-2 employment or volunteer status.",
          ("Employment status only", "m")]],
        "The Board&rsquo;s statute reaches your <b>classification</b> and "
        "stops. That is not a gap in enforcement; it is the division of "
        "labor between a licensing board and a labor agency, and it is the "
        "reason the Board sent you somewhere else instead of nowhere."))
    o.append("</section>")

    # ------------------------------------------------------------ the claim
    o.append('<section class="pk-sec" id="claim">')
    o.append('<p class="pk-k">The mechanism</p>')
    o.append('<h2 class="pk-h">What actually happens after you file.</h2>')
    o.append('<p class="pk-d">The instrument is the Initial Report or Claim, '
             "<b>DLSE Form 1</b>, revised July 2025. You can file it online, "
             "by post, or in person at a district office. Nothing on the "
             "form and nothing in the filing system mentions a fee &mdash; "
             "the word does not appear on it. You do not need a lawyer, and "
             "the hearings are designed on the assumption that most people "
             "will not have one.</p>")

    o.append(pk.table(
        ["Stage", "The statutory clock", "What it is"],
        [[("File", "m"), "Within %d years for unpaid minimum wages and "
          "unpaid hours" % SOL_YEARS,
          "Form 1, with your own record of the hours. There is no threshold "
          "amount; small claims are routine."],
         [("Determination", "m"),
          "%d days from filing" % DETERMINATION_DAYS,
          "Labor Code &sect;98(a). The Commissioner decides whether to hold "
          "a hearing, refer the claim to court, or take no further action."],
         [("Conference", "m"), "Usually first",
          "An informal settlement conference. <b>Not under oath, and not a "
          "hearing</b> &mdash; but failing to appear at it can dismiss your "
          "claim, which is the single most common way these are lost."],
         [("Hearing", "m"), "Within %d days of the determination"
          % HEARING_DAYS,
          "Sworn testimony before a hearing officer, on the record. Both "
          "sides may bring witnesses and documents."],
         [("Decision", "m"), "%d days after the hearing" % DECISION_DAYS,
          "An Order, Decision or Award. Either side may appeal it to the "
          "superior court, which then hears the matter afresh."]],
        "On appeal &sect;98.2(c) assesses the other side&rsquo;s costs and "
        "fees against whoever brought the appeal and did not do better, and "
        "the statute says an employee <b>&ldquo;is successful if the court "
        "awards an amount greater than zero&rdquo;</b>. In practice that "
        "makes appealing a small award expensive for an employer, which is "
        "worth knowing before you decide the amount is too small to bother "
        "with."))

    o.append(pk.checklist(
        "What to have before you fill in the form",
        ["<b>Your own hours record.</b> The employer is required to keep "
         "one; if theirs is missing or wrong, yours is what the hearing "
         "works from. Reconstruct it from your calendar and your notes if "
         "you have to, and say that you reconstructed it.",
         "<b>Every pay stub you were given.</b> Itemised-statement penalties "
         "are separate money and depend on what the stubs did or did not "
         "say.",
         "<b>The written offer, contract or handbook</b>, and anything that "
         "states the per-session rate or the admin rate.",
         "<b>Which hours you are claiming for.</b> Notes, no-shows, "
         "cancellations inside the notice window, staff meetings, required "
         "training, and the supervision hour itself &mdash; listed "
         "separately, because they are separately arguable.",
         "<b>Your registration number and dates.</b> Not because the Labor "
         "Commissioner needs them, but because the answer to &ldquo;why "
         "were you attending supervision?&rdquo; is that your registration "
         "required it."]))
    o.append("</section>")

    # ------------------------------------------------------------- what it is
    o.append('<section class="pk-sec" id="worth">')
    o.append('<p class="pk-k">The money</p>')
    o.append('<h2 class="pk-h">Five separate things you can be owed.</h2>')
    o.append('<p class="pk-d">The unpaid wage is the smallest of them. Each '
             "line below is its own statute with its own conditions, and "
             "they stack.</p>")
    o.append(pk.table(
        ["Statute", "What it gives", "The condition"],
        [[("&sect;1194", "m"), "The unpaid wages themselves, plus interest, "
          "reasonable attorney&rsquo;s fees and costs.",
          "Any unpaid minimum wage or overtime. Cannot be waived by "
          "agreement."],
         [("&sect;1194.2", "m"), "<b>Liquidated damages equal to the unpaid "
          "minimum wages</b> &mdash; in effect doubling that portion.",
          "Expressly available in a &sect;98 claim before the Labor "
          "Commissioner, not only in court. Form 1 has a tick box for it."],
         [("&sect;218.6", "m"), "Interest at %s%% on all unpaid wages from "
          "the date each was due." % format(INTEREST, ".0f"),
          "Automatic on an award of unpaid wages."],
         [("&sect;203", "m"), "Your daily rate for every day the final "
          "wages were late, up to %d days." % WAITING_CAP_DAYS,
          "Only if the employment has ended, and only if the failure to pay "
          "was wilful."],
         [("&sect;226(e)", "m"), "$%d for the first pay period and $%d for "
          "each one after, capped at $%s."
          % (STUB_FIRST, STUB_LATER, format(STUB_CAP, ",d")),
          "A knowing and intentional failure to give an accurate itemised "
          "wage statement, causing injury."]],
        "Form 1 item 37 has boxes for &sect;203 and &sect;1194.2 "
        "specifically. If you do not tick them, you have not claimed them."))

    o.append(CALC_HTML)

    o.append('<p class="pk-fine">This estimator is arithmetic on the '
             "statutes above, not a prediction. It assumes every hour you "
             "enter is compensable and that the failure was wilful, and a "
             "hearing may find neither. It is here because the thread that "
             "prompted this page was full of people who thought the amount "
             "was too small to be worth a form, and it usually is not.</p>")
    o.append("</section>")

    # -------------------------------------------------------------- piece rate
    o.append('<section class="pk-sec" id="piece">')
    o.append('<p class="pk-k">The argument that wins these</p>')
    o.append('<h2 class="pk-h">Per-session pay is piece rate, and piece rate '
             "has its own statute.</h2>")
    o.append('<p class="pk-d">Most of the argument in a per-session case is '
             "not about whether you worked the hours. It is about whether the "
             "session rate was <i>meant</i> to cover them. Labor Code "
             "&sect;226.2 answers that, and the answer is no.</p>")
    o.append(pk.callout(
        "Labor Code &sect;226.2",
        ["Employees paid on a piece-rate basis must be <b>compensated for "
         "rest and recovery periods and other non-productive time separately "
         "from any piece-rate compensation</b>.",
         "&ldquo;Other non-productive time&rdquo; is defined as time under "
         "the employer&rsquo;s control, exclusive of rest and recovery "
         "periods, that is not directed at the activity being compensated on "
         "a piece-rate basis. Writing the note is not the session. Sitting in "
         "supervision is not the session. Waiting for a client who does not "
         "arrive is not the session."]))
    o.append('<p class="pk-d">The Department of Industrial Relations&rsquo; '
             "own page defining piece rate gives, as one of its worked "
             "examples, <b>nurses compensated by the number of procedures "
             "performed</b>. A therapist paid by the session is the same "
             "structure with a different license on the wall. Form 1 asks "
             "about it directly: <b>item 34</b> is a straight question about "
             "whether you were paid on a piece-rate basis.</p>")
    o.append(pk.checklist(
        "What &ldquo;separately&rdquo; means in practice",
        ["Non-productive time must be paid at <b>no less than the applicable "
         "minimum wage</b> &mdash; the local one where you work, which in "
         "several California cities is well above the state figure.",
         "The employer may not take a high per-session rate and argue it "
         "already covers the notes. That is exactly the averaging "
         "&sect;226.2 forbids.",
         "The wage statement has to show the total non-productive hours and "
         "the rate paid for them, as separate line items. If yours never "
         "did, that is the &sect;226(e) claim in the table above.",
         "None of this depends on you being right about the total. Bring the "
         "hours you can evidence; the hearing decides the rest."]))
    o.append("</section>")

    # -------------------------------------------------------------- volunteer
    o.append('<section class="pk-sec" id="volunteer">')
    o.append('<p class="pk-k">Where the two systems collide</p>')
    o.append('<h2 class="pk-h">A licensing board&rsquo;s permission is not a '
             "wage-and-hour exemption.</h2>")
    o.append('<p class="pk-d">This is the part of the thread that nobody '
             "resolved, and it is genuinely unresolved &mdash; not a thing "
             "somebody had failed to look up. Two agencies say two things "
             "and neither has reconciled them in writing.</p>")
    o.append(pk.table(
        ["Who says it", "What they say", "What it means for you"],
        [(["California Board of Behavioral Sciences",
           "BPC &sect;4980.43.3(a) permits experience to be gained as a "
           "<b>volunteer</b>, and adds that employers are &ldquo;encouraged "
           "to provide fair remuneration&rdquo; to associates.",
           "Unpaid hours are creditable toward the %s. The Board will not "
           "reject them for being unpaid." % format(TOTAL_HOURS, ",d")],
          "hi"),
         (["United States Department of Labor",
           "On its own compliance advisor for the Fair Labor Standards Act: "
           "<b>&ldquo;employees may not volunteer services to for-profit "
           "private sector employers.&rdquo;</b>",
           "A private practice is a for-profit private sector employer. The "
           "federal position is that the arrangement is not a volunteer "
           "arrangement at all."],
          "bad")],
        "Both statements are current and both are published by the body that "
        "made them. &ldquo;Encouraged to provide fair remuneration&rdquo; is "
        "a licensing board declining to set a wage, not a federal agency "
        "granting an exemption &mdash; and only one of those two bodies "
        "enforces the minimum wage. A non-profit or public agency is a "
        "different question, with its own answer; this row is about the "
        "private practice the thread was describing."))
    o.append("</section>")

    # ------------------------------------------------------------- the hours
    o.append('<section class="pk-sec" id="hours">')
    o.append('<p class="pk-k">The fear underneath the thread</p>')
    o.append('<h2 class="pk-h">Filing does not cost you the hours.</h2>')
    o.append('<p class="pk-d">The reason most people in that thread said they '
             "would not file was not the money. It was that the person they "
             "would be claiming against signs their Verification of "
             "Experience. That is a real problem and this page will not "
             "pretend otherwise &mdash; but two things are worth being "
             "precise about.</p>")
    o.append(pk.numbered([
        ("1", "Unpaid hours still count",
         "Nothing in the Board&rsquo;s statute conditions creditable "
         "experience on being paid. Hours already worked and already "
         "supervised do not become uncreditable because you later asked to "
         "be paid for them."),
        ("2", "The hours you are arguing about are mostly the "
         "non-clinical ones",
         "And &sect;4980.43(c) counts up to <b>%s non-clinical hours</b> "
         "toward the %s &mdash; the category that covers writing records, "
         "attending meetings and workshops, and the administrative work of "
         "the caseload. The unpaid hours in these threads are almost always "
         "hours the Board already credits."
         % (format(NONCLIN_CAP, ",d"), format(TOTAL_HOURS, ",d"))),
        ("3", "Retaliation is its own claim",
         "An employer may not discharge or discriminate against an employee "
         "for filing a wage claim. That does not make retaliation "
         "impossible; it makes it a second claim rather than an unanswerable "
         "one. If the practical risk to your signature is what is stopping "
         "you, that is a legitimate reason to wait until the hours are "
         "verified &mdash; and the %d-year limit is long enough that waiting "
         "is often possible." % SOL_YEARS),
    ]))
    o.append('<p class="pk-fine">Nothing here is legal advice, and this page '
             "is not a substitute for talking to an employment lawyer. Many "
             "take wage cases on contingency and consultations are commonly "
             "free, which is worth knowing before you decide the case is too "
             "small for one. If it is the hours rather than the money you are "
             "worried about, the "
             '<a href="%s">licensure hours calculator</a> and the '
             '<a href="%s">job advisor</a> both work from your own numbers '
             "and send nothing anywhere.</p>" % (HOURS, ADVISOR))
    o.append("</section>")

    # ---------------------------------------------------------------- sources
    src, n = pk.sources([
        ("The Board, and what it does not cover", [
            ("BPC &sect;4980.43.3 &mdash; employee or volunteer, never an "
             "independent contractor",
             "https://leginfo.legislature.ca.gov/faces/codes_displaySection"
             ".xhtml?sectionNum=4980.43.3.&lawCode=BPC"),
            ("BPC &sect;4980.43 &mdash; the hour categories and the "
             "%s non-clinical cap" % format(NONCLIN_CAP, ",d"),
             "https://leginfo.legislature.ca.gov/faces/codes_displaySection"
             ".xhtml?sectionNum=4980.43.&lawCode=BPC"),
            ("BBS Consumer Complaint form &mdash; read for what it does not "
             "list", "https://www.bbs.ca.gov/pdf/forms/comp-2a.pdf"),
            ("BBS complaints and the courts flyer",
             "https://www.bbs.ca.gov/pdf/publications/"
             "complaints_court_flyer.pdf"),
            ("MFT Supervisor Responsibility Statement &mdash; the seventeen "
             "attestations", "https://www.bbs.ca.gov/pdf/forms/mft/"
             "mfrespon.pdf"),
            ("Supervision Agreement 37M-300",
             "https://www.bbs.ca.gov/pdf/forms/supervision_agreement.pdf"),
        ]),
        ("Filing the claim", [
            ("DLSE Form 1, Initial Report or Claim (rev. 07/2025)",
             "https://www.dir.ca.gov/dlse/Forms/Wage/English.pdf"),
            ("File a wage claim online with the Labor Commissioner",
             "https://cadir.my.site.com/oc"),
            ("Labor Code &sect;98 &mdash; the %d-day determination and the "
             "%d-day hearing" % (DETERMINATION_DAYS, HEARING_DAYS),
             "https://leginfo.legislature.ca.gov/faces/codes_displaySection"
             ".xhtml?lawCode=LAB&sectionNum=98"),
            ("Labor Code &sect;98.2 &mdash; appeal, and costs against the "
             "unsuccessful appellant",
             "https://leginfo.legislature.ca.gov/faces/codes_displaySection"
             ".xhtml?lawCode=LAB&sectionNum=98.2"),
        ]),
        ("What can be recovered", [
            ("Labor Code &sect;1194 &mdash; unpaid minimum wage, interest, "
             "fees and costs",
             "https://leginfo.legislature.ca.gov/faces/codes_displaySection"
             ".xhtml?lawCode=LAB&sectionNum=1194"),
            ("Labor Code &sect;1194.2 &mdash; liquidated damages",
             "https://leginfo.legislature.ca.gov/faces/codes_displaySection"
             ".xhtml?lawCode=LAB&sectionNum=1194.2"),
            ("Labor Code &sect;218.6 &mdash; interest on unpaid wages",
             "https://leginfo.legislature.ca.gov/faces/codes_displaySection"
             ".xhtml?lawCode=LAB&sectionNum=218.6"),
            ("Labor Code &sect;203 &mdash; waiting-time penalties",
             "https://leginfo.legislature.ca.gov/faces/codes_displaySection"
             ".xhtml?lawCode=LAB&sectionNum=203"),
            ("Labor Code &sect;226 &mdash; itemised wage statements and "
             "&sect;226(e) penalties",
             "https://leginfo.legislature.ca.gov/faces/codes_displaySection"
             ".xhtml?lawCode=LAB&sectionNum=226"),
        ]),
        ("Piece rate", [
            ("Labor Code &sect;226.2 &mdash; non-productive time paid "
             "separately",
             "https://leginfo.legislature.ca.gov/faces/codes_displaySection"
             ".xhtml?lawCode=LAB&sectionNum=226.2"),
            ("DIR &mdash; what piece-rate compensation is, with the nursing "
             "example",
             "https://www.dir.ca.gov/pieceratebackpayelection/piecerate.html"),
        ]),
        ("Volunteering", [
            ("US Department of Labor elaws advisor &mdash; employees may not "
             "volunteer for for-profit private sector employers",
             "https://webapps.dol.gov/elaws/whd/flsa/scope/er16.asp"),
        ]),
    ], note="Every statute above is linked to the text of the law rather than "
            "to a summary of it, because summaries of &sect;226.2 in "
            "particular disagree with each other. Where this page describes "
            "what a document does <i>not</i> say, the document is listed so "
            "you can check the absence yourself.")
    o.append(src)

    o.append("</article>")
    return "".join(o), n


# ------------------------------------------------------------- the estimator
# Nothing typed here leaves the page: no URL state, no storage, no analytics
# call, no network. The site's printed promise is that nothing a reader types
# is sent anywhere, and a page about a wage claim against a named employer is
# the last place on the site where that promise could be allowed to bend.
CALC_HTML = """<div class="pk-calc" id="uh-calc">
<h3 class="pk-h3" style="margin-top:0">What the claim is worth on its face</h3>
<div class="pk-cg">
<div class="pk-cc">
<label class="pk-fl" for="uh-hrs">Unpaid hours in a typical week</label>
<input type="number" id="uh-hrs" min="0" max="60" step="0.5" placeholder="0">
<label class="pk-fl" for="uh-wks">Weeks it went on</label>
<input type="number" id="uh-wks" min="0" max="156" step="1" placeholder="0">
</div>
<div class="pk-cc">
<label class="pk-fl" for="uh-min">Minimum wage where you work ($/hr)</label>
<input type="number" id="uh-min" min="0" max="40" step="0.01" placeholder="0">
<label class="pk-fl" for="uh-day">Your daily pay, if the job has ended ($)</label>
<input type="number" id="uh-day" min="0" max="5000" step="1" placeholder="0">
</div>
</div>
<div class="pk-out">
<div class="r hd"><span>Line</span><span>Amount</span></div>
<div class="r"><span class="lbl">Unpaid hours claimed</span><span class="va" id="uh-o-hrs">&mdash;</span></div>
<div class="r"><span class="lbl">Wages at the minimum wage &mdash; &sect;1194</span><span class="va" id="uh-o-wage">&mdash;</span></div>
<div class="r"><span class="lbl">Liquidated damages &mdash; &sect;1194.2</span><span class="va" id="uh-o-liq">&mdash;</span></div>
<div class="r"><span class="lbl">Interest at 10% &mdash; &sect;218.6</span><span class="va" id="uh-o-int">&mdash;</span></div>
<div class="r"><span class="lbl">Waiting-time penalty, up to 30 days &mdash; &sect;203</span><span class="va" id="uh-o-wait">&mdash;</span></div>
<div class="r tot"><span class="lbl"><b>On its face</b></span><span class="va" id="uh-o-tot">&mdash;</span></div>
</div>
<p class="pk-note" id="uh-warn">Enter the hours and the weeks. Everything is
computed in your browser and nothing is sent anywhere.</p>
</div>"""

CALC_JS = """<script>
(function(){
  var ids = ['uh-hrs','uh-wks','uh-min','uh-day'];
  function num(id){
    var el = document.getElementById(id);
    if(!el) return 0;
    var v = parseFloat(el.value);
    return (isFinite(v) && v > 0) ? v : 0;
  }
  function money(n){
    return '$' + Math.round(n).toLocaleString('en-US');
  }
  function set(id, txt){
    var el = document.getElementById(id);
    if(el) el.textContent = txt;
  }
  function run(){
    var hrs = num('uh-hrs'), wks = num('uh-wks');
    var min = num('uh-min'), day = num('uh-day');
    var warn = document.getElementById('uh-warn');
    if(!hrs || !wks || !min){
      ['uh-o-hrs','uh-o-wage','uh-o-liq','uh-o-int','uh-o-wait','uh-o-tot']
        .forEach(function(id){ set(id, '\\u2014'); });
      if(warn) warn.innerHTML = 'Enter the hours, the weeks and the minimum ' +
        'wage where you work. Everything is computed in your browser and ' +
        'nothing is sent anywhere.';
      return;
    }
    var total = hrs * wks;
    var wage = total * min;
    var liq = wage;
    /* Simple interest over the average age of the claim, which is half the
       period if the hours were spread evenly across it. This understates a
       claim whose unpaid hours were concentrated early and overstates one
       concentrated late; it is an estimate and the page says so. */
    var yrs = (wks / 52) / 2;
    var interest = wage * 0.10 * yrs;
    var wait = day * 30;
    set('uh-o-hrs', total.toFixed(1).replace(/\\.0$/, '') + ' hrs');
    set('uh-o-wage', money(wage));
    set('uh-o-liq', money(liq));
    set('uh-o-int', money(interest));
    set('uh-o-wait', day ? money(wait) : '\\u2014');
    set('uh-o-tot', money(wage + liq + interest + wait));
    if(warn){
      warn.innerHTML = 'The minimum-wage figure is the floor, not your rate: ' +
        'if you were promised more per hour than the minimum, the ' +
        '<b>&sect;1194</b> line rises and the <b>&sect;1194.2</b> line does ' +
        'not, because liquidated damages double the minimum-wage portion ' +
        'only. Interest is simple, at 10%, over half the period. Nothing ' +
        'here is sent anywhere.';
    }
  }
  ids.forEach(function(id){
    var el = document.getElementById(id);
    if(el){ el.addEventListener('input', run); }
  });
  run();
})();
</script>"""


META = pk.meta_block(
    PAGE,
    "Unpaid hours as a California associate: the wage claim, step by step",
    "Your supervisor did not pay you for notes, no-shows or supervision. The "
    "BBS does not regulate that. Here is what the Labor Commissioner does, "
    "what it costs, and what the claim is worth.",
    "licensure", "guide",
    "My supervisor doesn&rsquo;t pay me for notes or supervision &mdash; is "
    "there anything I can actually do?",
    "The wage claim the Board cannot help with: how to file it, what it "
    "costs, and the five statutes that decide what it is worth",
    "$0 to file, %d years to do it" % SOL_YEARS,
    weight=5)


def main():
    print("unpaid hours and the wage claim")

    head, header, footer, links, scripts = pk.chrome_parts(DONOR)
    html_body, nsrc = body()
    html = pk.assemble(head, META, header, html_body, footer, links, scripts,
                       extra=CALC_JS)

    p = os.path.join(SITE, PAGE)
    open(p, "w", encoding="utf-8").write(html)
    print("  wrote %s, %s bytes, %d sources"
          % (PAGE, format(len(html), ",d"), nsrc))

    bad = pk.check_page(p, [
        ("the estimator", 'id="uh-calc"'),
        ("the estimator's script", "uh-o-tot"),
        ("the liquidated-damages line", "1194.2"),
        ("the piece-rate statute", "226.2"),
        ("the DOL volunteer finding", "for-profit private sector"),
    ], [j[0] for j in JUMPS] + ["sources"])

    s = open(p, encoding="utf-8").read()

    # The page's whole premise is that the Board is not a wage regulator. If
    # the word LLC or any advice-shaped verb has crept in from a copied
    # pattern, that is the failure mode this site has had before.
    if "LLC" in pk.article(s):
        print("GUARD: the page says LLC. California-licensed MFTs cannot form "
              "one, and this page has no reason to mention it at all")
        bad += 1

    # Every source must be a real link or deliberately unlinked. A source list
    # with a bare href="#" is worse than no source list.
    if 'href="#"' in s:
        print("GUARD: a placeholder link survived into the page")
        bad += 1

    if nsrc < 15:
        print("GUARD: %d sources. A page making this many statutory claims "
              "with fewer than 15 has lost some." % nsrc)
        bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("  guards clean - %d sources, every jump anchor present, the "
          "estimator wired" % nsrc)


if __name__ == "__main__":
    main()
