#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Which stage of the path each page is written for, and what it says there.

WHY THE TAGGING IS INCREMENTAL RATHER THAN BULK

The proposal that led to this recommends two fields per registry entry,
`stages` and `stage_note`, and says plainly that **stage_note must be
mandatory wherever stages has an entry**. It is the only thing standing
between a stage hub and a re-listing of a topic hub, and an optional field
gets skipped on exactly the pages where writing it is hardest.

Holding to that rule has a consequence the proposal did not spell out: it
makes bulk tagging impossible. Two hundred pages cannot be given two hundred
honest one-line annotations in one pass, and generating them mechanically
would produce exactly the thin duplicate the field exists to prevent.

So a page is tagged when a hub that lists it is built, and not before. Nothing
is tagged speculatively. The guard is therefore trivially satisfiable and
still real: every entry here has a note somebody wrote.

WHAT A GOOD stage_note IS

Not the page's summary - the registry already holds `outcome` for that. It
answers "what does this page tell ME, at MY stage", which is different for a
reader counting hours than for a reader deciding whether to enrol. The county
pay page tells a career-changer what the job pays at the end; it tells an
associate which employer to apply to first. Same page, two notes.

STAGES

    deciding   thinking about it, or choosing between programs
    student    enrolled, practicum approaching or underway
    associate  registered, counting toward 3,000
    licensed   licensed, first years
    owner      running a practice with other people in it

The gap between degree and registration number is deliberately folded into
`student`, per the proposal: it is a real status with its own law, and it is
too small to hold a hub of its own.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
REG = os.path.join(SITE, "mock", "library", "registry.json")

STAGES = ("deciding", "student", "associate", "licensed", "owner")

# file -> {stage: the one line saying what this page tells THAT reader}
TAGS = {
    "amft-3000-hours-california.html": {
        "student": "Up to 1,300 pre-degree hours can bank toward the 3,000 "
                   "- what your practicum pace is worth after you graduate.",
        "associate": "What date you finish, at the hours you are actually "
                     "logging - and which of the four sub-totals is behind."},
    "getting-hired-as-a-california-associate.html": {
        "student": "Read before your final term: which settings can legally "
                   "bill for a pre-licensed clinician decides where "
                   "applications land.",
        "associate": "Why half your applications get no reply: it is a "
                     "billing rule, not your hour count."},
    "associate-therapist-pay-los-angeles-bay-area.html": {
        "associate": "What the offer should be, salary against per-session, "
                     "before you accept one."},
    "associate-unpaid-hours-california.html": {
        "associate": "The wage claim for unpaid non-clinical time, step by "
                     "step - and why the Board is not where you file it."},
    "associate-hours-telehealth-out-of-state.html": {
        "associate": "Whether hours you gain from another state count. The "
                     "Board has answered five times and nobody links it."},
    "associate-hours-trackers-compared.html": {
        "student": "Log like the Board reads logs from week one - five "
                   "trackers compared, and what counts as a signature.",
        "associate": "Five hour-tracking products compared, and what the "
                     "Board actually accepts as a supervisor signature."},
    "prelicensed-job-sites-california.html": {
        "associate": "61 employers statewide whose own sites say they "
                     "take pre-licensed clinicians - each row links the "
                     "page that says so."},
    "county-job-portals-california.html": {
        "associate": "Where the application form is, in all 58 counties - "
                     "including the seven whose obvious URL is somebody else."},
    "county-therapist-pay-california.html": {
        "deciding": "What the job pays at the end, county by county, from "
                    "employers' own returns - a 2.8x spread inside one "
                    "state.",
        "associate": "Which county to apply to first, from what each one "
                     "actually paid rather than what it advertised."},
    "loan-forgiveness-employers-california.html": {
        "associate": "You may already be accruing qualifying payments. PSLF "
                     "asks about your employer and not about your license."},
    "mbh-slrp-california.html": {
        "associate": "The one loan-repayment program that names registered "
                     "associates - and the 32-hour obligation attached."},
    "medi-cal-safety-net-employers-california.html": {
        "associate": "The employers that can legally bill for you, by name: "
                     "57 county plans and 218 health center organizations."},
    "bbs-exam-pass-rates-california.html": {
        "deciding": "The exams at the end of the road, and what they "
                    "actually pass at, first-time, from the Board's own "
                    "packets.",
        "associate": "What the law and ethics exam actually passes at, "
                     "first-time, across seven quarters."},
    "bbs-processing-times-california.html": {
        "student": "How long the Board takes on a new associate application "
                   "- worth knowing before your final term, not after.",
        "associate": "How long the Board is taking right now, so a renewal or "
                     "an application is filed with room to spare."},
    "bbs-90-day-rule-california.html": {
        "student": "The one deadline that starts before you graduate: get "
                   "the employer Live Scan stamped before your award date.",
        "associate": "If you worked between your degree and your number, "
                     "whether those hours exist &mdash; and the documents "
                     "that decide it."},
    "bbs-fees-california-2026.html": {
        "deciding": "What the license itself costs the state - the "
                    "Board's whole fee schedule, halved through 2030.",
        "student": "What registering will cost when you file - the "
                   "application fees halved in July 2026, and revert in 2030.",
        "associate": "What your renewal costs since July 2026, and what it "
                     "goes back to in 2030."},
    "out-of-state-to-california-licensure.html": {
        "associate": "If you are moving here mid-registration: which hours "
                     "travel, and which do not."},
    "associate-mft-job-advisor.html": {
        "associate": "Which setting fits the hours you still need, rather "
                     "than the hours you already have."},
    "therapists-by-county-california.html": {
        "associate": "How many associates are competing for a supervisor in "
                     "your county, from the state register."},
    "associate-employers-bay-area.html": {
        "associate": "The Bay Area employers that can bank your 3,000 "
                     "&mdash; complete where public files reach, and honest "
                     "about the private-practice hole where they do not."},
    "practicum-sites-bay-area.html": {
        "student": "The Bay Area settings the code lets you be placed in "
                   "&mdash; and the site-agreement question to ask your "
                   "program before contacting any of them."},
    "training-programs-bay-area.html": {
        "student": "Ten agencies with a training program in writing - "
                   "supervision hours and stipends where stated, and the "
                   "page each fact came from.",
        "associate": "Three of these programs name registered associates "
                     "as well as trainees - worth reading before a cold "
                     "application round."},
    "east-bay-practicum-site-directory.html": {
        "student": "The 21 sites in EB CAMFT's own 2026-27 directory "
                   "&mdash; who was accepting at the dated read, hours, "
                   "supervision, and the named contact to write to.",
        "associate": "Three of the chapter's practicum sites say they "
                     "also hire registered associates &mdash; one of "
                     "them is associates-only."},
    "how-to-find-a-practicum-site-california.html": {
        "deciding": "Whose job the placement search is at each kind of "
                    "program &mdash; worth knowing before you pick one, not "
                    "after.",
        "student": "The search in order: your program's model first, the "
                   "five statutory strikes, then six-plus applications "
                   "across the four shelves of seats."},
    "practicum-california-mft-trainee.html": {
        "deciding": "The highest-variance year of the degree - read the "
                    "78-program placement table before you pick a school.",
        "associate": "What of your pre-degree hours the Board still counts, "
                     "and the 90-day rule if you are newly graduated.",
        "student": "Who finds your practicum site at each of the 78 programs, "
                   "and the seven rules that decide if a placement counts."},
    "continuing-education-california-lmft.html": {
        "associate": "Not yet - but the law and ethics course inside your "
                     "first renewal period is, and it is easy to miss."},
    "become-an-mft-california.html": {
        "deciding": "Every requirement, cost and year between deciding and "
                    "the license, each with its code section.",
        "student": "Every requirement between today and the license, each "
                   "with its code section - the map your program does not "
                   "hand you."},
    "mft-programs-california.html": {
        "deciding": "All 78 California programs compared on the thing "
                    "that varies most - who finds your practicum site."},
    "psyd-programs-california.html": {
        "deciding": "If the doctorate is on your list: every California "
                    "PsyD, and what accreditation actually decides."},
    "therapist-cost-of-living-california.html": {
        "deciding": "What a month costs in the places you might "
                    "practice, against what the work actually pays."},
    "therapists-by-state-compared.html": {
        "deciding": "How crowded California is against every other "
                    "state, from the licensing registers themselves."},
    "becoming-a-therapist-california-career-change.html": {
        "deciding": "The whole route from another career, ordered by "
                    "what you can start this month - written for the "
                    "person still deciding."},
    "bbs-advertising-rules-2026.html": {
        "associate": "Your profile needs five elements including your "
                     "employer and a supervision statement - the "
                     "April 2026 rule as a checklist.",
        "licensed": "Three things every ad must carry since April 2026 "
                    "- and the seven ways the Board's own examples "
                    "show profiles failing."},
    "telehealth-rules-california-therapist.html": {
        "associate": "The telehealth rule as it actually reads - "
                     "including the per-session duty that started in "
                     "2016, not January.",
        "licensed": "What the 1 January 2026 amendment changed (two "
                    "subdivisions) and what it did not - plus what "
                    "naming the Security Rule asks of a solo "
                    "practice."},
    "is-therapy-financially-viable-california.html": {
        "deciding": "The is-there-money question answered in arithmetic "
                    "- what entering costs, what the lean years pay, "
                    "and what a full practice nets."},
    "therapist-tax-strategy-california.html": {
        "licensed": "The whole tax decision worked on your numbers - "
                    "sole prop against the corporation, with the payroll "
                    "gap most comparisons leave out."},
    "practice-simulator.html": {
        "licensed": "What your practice actually pays you at your rate "
                    "and caseload, after expenses and tax - live, in the "
                    "browser."},
    "grow-your-therapy-practice.html": {
        "licensed": "What a client is worth at your rate, and which of "
                    "three channels actually fills a caseload."},
    "insurance-reimbursement-rates-california-therapist.html": {
        "licensed": "What each payer actually reimburses, computed per "
                    "code - before you decide which panels are worth it."},
    "headway-for-california-therapists.html": {
        "licensed": "What Headway pays and what it keeps, priced at real "
                    "caseloads - read before signing."},
    "therapy-liability-insurance-california.html": {
        "licensed": "Eight malpractice programs compared on what they "
                    "publish and what people actually pay."},
    "therapist-working-remotely-california.html": {
        "licensed": "The same practice run from eight places - what "
                    "moving does to your license, your taxes and your "
                    "clients."},
    "simplepractice-california-therapists.html": {
        "licensed": "What the software actually costs all-in at your "
                    "caseload, including the fees the pricing page "
                    "skips."},
    "continuing-education-california-lmft.html": {
        "licensed": "36 hours per renewal, and the audit 62% fail - "
                    "what counts, what does not, and the paper to keep."},
    "therapist-cost-of-living-california.html": {
        "licensed": "What a month costs where you practice, against "
                    "what your caseload brings in - the relocation "
                    "arithmetic."},
    "therapist-discipline-cases-california.html": {
        "licensed": "48 real Board decisions and what each one cost - "
                    "most begin with paperwork, not with clients.",
        "associate": "What the Board actually acts on. Several of these begin "
                     "with an hours form or a supervisor signature."},
}


def main():
    print("stage tagging")
    reg = json.load(open(REG, encoding="utf-8"))
    by = {p["file"]: p for p in reg["pages"]}

    missing = [f for f in TAGS if f not in by]
    if missing:
        sys.exit("%d tagged file(s) are not in the registry - renamed or "
                 "deleted:\n  %s" % (len(missing), "\n  ".join(sorted(missing))))

    n_pages = 0
    n_notes = 0
    for f, notes in TAGS.items():
        for st in notes:
            if st not in STAGES:
                sys.exit("%s has unknown stage %r" % (f, st))
            if not notes[st].strip():
                sys.exit("%s has an empty note for %r" % (f, st))
        p = by[f]
        p["stages"] = sorted(notes, key=lambda s: STAGES.index(s))
        p["stage_note"] = notes
        n_pages += 1
        n_notes += len(notes)

    # THE RULE. A page carrying `stages` without a note for each one would be
    # a page that appears on a hub with nothing to say there, which is the
    # thin duplicate this whole field exists to prevent.
    for p in reg["pages"]:
        for st in p.get("stages", []):
            if not (p.get("stage_note") or {}).get(st, "").strip():
                sys.exit("%s is tagged %r with no stage_note - that is the one "
                         "thing this field may not do" % (p["file"], st))

    json.dump(reg, open(REG, "w", encoding="utf-8"), indent=1,
              ensure_ascii=False)
    counts = {}
    for p in reg["pages"]:
        for st in p.get("stages", []):
            counts[st] = counts.get(st, 0) + 1
    print("  %d page(s) tagged, %d note(s) written" % (n_pages, n_notes))
    print("  by stage: %s" % ", ".join("%s %d" % (s, counts[s])
                                       for s in STAGES if s in counts))
    print("  %d of %d pages carry no stage yet, which is expected - a page is "
          "tagged when a hub that lists it is built"
          % (len(reg["pages"]) - sum(1 for p in reg["pages"] if p.get("stages")),
             len(reg["pages"])))


if __name__ == "__main__":
    main()
