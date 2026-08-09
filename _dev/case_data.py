# -*- coding: utf-8 -*-
"""Thirty California MFT discipline cases, de-identified, 2024-2026.

WHERE THIS COMES FROM

The Board of Behavioral Sciences does not publish a browsable list of its
disciplinary decisions. It publishes a quarterly newsletter, and in the
"Formal Disciplinary Actions" section of each issue every licensee's name is a
live hyperlink to the signed Decision and Order, Stipulated Settlement or
Accusation, hosted by the Department of Consumer Affairs. Eight issues cover
July 2023 through March 2026 with no gap.

Reading all eight yields 286 disciplinary entries across every BBS licence
type. 152 are LMFT or AMFT. 104 of those took effect in 2024, 2025 or 2026.
103 of the 104 source documents were retrieved and read in full; one entry had
no hyperlink in the newsletter.

The thirty cases below are drawn from those documents.

WHY THERE ARE NO NAMES HERE

Every name is public record - the Board publishes them itself, and so does DCA.
This site does not republish them. The reason is editorial, not legal: a page
that names people becomes a page people arrive at by searching a name, and then
its purpose is no longer teaching. Nothing here is anonymised in a way that
changes the lesson. The case number and effective date are given for every
case, so any decision below can be pulled from the public record by anyone who
wants to check it, and the route to do that is documented on the hub page.

Identifying detail has been removed or generalised: no names, no cities, no
employer or facility names, and client initials replaced. Conduct, statute,
outcome and dollar figure are exactly as the decision states them.

WHAT A STIPULATED SETTLEMENT MEANS, SINCE MOST OF THESE ARE ONE

In a stipulated settlement the licensee does not admit the allegations. They
agree that the Board could establish a prima facie case, and they accept the
discipline. Where a case went to a full hearing instead, it says so.
"""

# ---------------------------------------------------------------- provenance
CHECKED = "August 2026"

NEWSLETTERS = "https://www.bbs.ca.gov/resources/general.html"
LAWSREGS = "https://www.bbs.ca.gov/pdf/publications/lawsregs.pdf"
DISPGUID = "https://www.bbs.ca.gov/pdf/publications/dispguid.pdf"
SUNSET = "https://www.bbs.ca.gov/pdf/publications/bbs_2025_sunset_report.pdf"
BROCHURE = "https://www.dca.ca.gov/publications/proftherapy.pdf"


def leg(section, code="bpc"):
    """A real link to the California code section, not a bracketed number."""
    return ("https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml"
            "?sectionNum=%s&lawCode=%s" % (section, code.upper()))


# ------------------------------------------------------------------- groups
GROUPS = [
    {
        "key": "sexual",
        "n": "Sexual boundaries",
        "lede": "Six cases. One went to a full hearing; the rest settled. The "
                "penalty floor here is the highest in the guidelines, and for "
                "sexual contact as defined in &sect;729 the revocation cannot be "
                "stayed by anyone &mdash; not the administrative law judge, not "
                "the Board.",
    },
    {
        "key": "dual",
        "n": "Boundary drift with no sexual contact",
        "lede": "Five cases where nobody touched anybody. Texting, emails, "
                "dinners, a sleepover, a shared joint. These are the cases most "
                "worth reading, because in every one of them the therapist could "
                "have described what they were doing out loud and it would still "
                "have sounded reasonable to them.",
    },
    {
        "key": "records",
        "n": "Records, confidentiality and the file",
        "lede": "Three cases about paper. A letter written for the wrong person, "
                "a records request ignored for six months, an address never "
                "updated. Confidentiality is the second most common ground for a "
                "citation in California, ahead of everything clinical.",
    },
    {
        "key": "money",
        "n": "Money, billing and honesty",
        "lede": "Three cases. One involves no clients at all &mdash; the "
                "conviction came from a bookkeeping job &mdash; and it still cost "
                "the registration.",
    },
    {
        "key": "another",
        "n": "Discipline that arrives from somewhere else",
        "lede": "Four cases under &sect;4982.25. If any other board, in any "
                "state, disciplines any healing-arts licence you hold, that fact "
                "alone is unprofessional conduct in California. A certified copy "
                "of the other board's decision is conclusive evidence &mdash; "
                "there is nothing to relitigate.",
    },
    {
        "key": "fitness",
        "n": "Fitness-to-practice examinations",
        "lede": "One page, three cases, one lesson: an order to be examined is "
                "not a request, and ignoring it is its own independent ground for "
                "revocation with no &sect;4982 charge attached.",
    },
    {
        "key": "conviction",
        "n": "Convictions, and the duty to report one",
        # Trimmed from five write-ups to three, deliberately. Sixty-two of the
        # 103 decisions are convictions and most are a DUI, so the category is
        # by far the largest in the data - but past the first case they stop
        # teaching anything new. What is kept is the modal case, the reporting
        # duty, and the fact that no conviction is needed at all. The base rate
        # stays in the lede, because it is the finding; the repetition does not.
        "lede": "The largest category in the data by a wide margin &mdash; "
                "sixty-two of the 103 decisions cite &sect;4982(a), and most of "
                "those are a DUI arriving through the Department of Justice "
                "notification feed rather than through a client. Three are "
                "written up here rather than all of them, because past the first "
                "one they repeat. What is kept is the case that shows what the "
                "typical one looks like, the case about reporting it, and the "
                "case that shows the Board does not need a conviction at all.",
    },
    {
        "key": "probation",
        "n": "What happens after discipline",
        "lede": "Three cases about the part nobody plans for. Probation runs "
                "three to seven years, you pay for the monitoring, you tell your "
                "clients and your employer, and the coursework you are ordered to "
                "take does not count toward your continuing education.",
    },
]

# --------------------------------------------------------------------- cases
# Each: slug, group, t, dek, role, eff, case, facts[], charges[(cite,url,plain)],
#       outcome, cost, rule, ins, prevent[]
CASES = [

    # ===================================================== sexual boundaries
    {
        "slug": "discipline-case-sex-with-a-residential-client",
        "group": "sexual",
        "t": "The clinical director who slept with an inpatient, then asked him for $5 million",
        "dek": "Seven years of probation and $15,883 &mdash; the largest cost "
               "recovery in three years of California MFT discipline.",
        "role": "LMFT",
        "eff": "December 19, 2024",
        "case": "2002022002057",
        "hear": "OAH No. 2024040833",
        "facts": [
            "The therapist was clinical director of a residential treatment "
            "facility and the primary therapist for a client admitted for a "
            "30-day inpatient stay. Mid-session, she told him she could only "
            "think about a sexual act.",
            "She took him out of the facility to a shopping mall, describing the "
            "outing as exposure therapy, then to her own residence, where they "
            "had intercourse.",
            "After his discharge she continued what was billed as tele-therapy. "
            "It consisted of near-nightly video calls in which she exposed "
            "herself. He travelled back to California twice; they had sex at a "
            "hotel and again over New Year's, using drugs and alcohol.",
            "She told him she could lose her license over it, and then asked him "
            "for <b>$5 million</b> to protect her against that risk. He sent her "
            "at least $14,500 that had nothing to do with therapy. Among the "
            "text messages in the record is one from the client reading "
            "&ldquo;Wait this is illegal.&rdquo;",
        ],
        "charges": [
            ("B&amp;P &sect;4982(d)", leg("4982"),
             "Gross negligence in the performance of marriage and family therapy."),
            ("B&amp;P &sect;4982(i)", leg("4982"),
             "Intentionally or recklessly causing physical or emotional harm to a client."),
            ("B&amp;P &sect;4982(j)", leg("4982"),
             "A dishonest, corrupt or fraudulent act substantially related to the "
             "duties of a licensee &mdash; here, the demand for money."),
            ("B&amp;P &sect;4982(k), with &sect;&sect;726 and 729", leg("4982"),
             "Sexual relations with a client. &sect;729 is the criminal statute: "
             "sexual exploitation by a psychotherapist."),
        ],
        "outcome": "Revocation stayed. Seven years of probation &mdash; the "
                   "maximum probation term the disciplinary guidelines set for "
                   "sexual misconduct.",
        "cost": "$15,883",
        "rule": "&sect;4982(k) covers sexual relations with a client and with a "
                "former client for two years after termination. It also covers "
                "solicitation &mdash; asking is the violation, whether or not "
                "anything follows. Separately, &sect;4982.26 says that if a "
                "decision contains <b>any finding of fact</b> that the licensee "
                "engaged in sexual contact as defined in &sect;729, the Board "
                "shall revoke, and &ldquo;the revocation shall not be stayed by "
                "the administrative law judge or the board.&rdquo; A settlement "
                "that avoids that finding is the only reason a stay is available "
                "at all in a case like this one.",
        "ins": "Almost nowhere. Professional liability policies sold to "
               "therapists treat sexual misconduct as <b>defense coverage "
               "only</b> &mdash; the insurer may pay a lawyer, and will pay "
               "nothing on the claim itself. Several policies condition even that "
               "on the allegation turning out to be unfounded and the insured "
               "never admitting it. The board-defense sublimit that would fund "
               "the administrative case runs $5,000 to $35,000 depending on the "
               "program; seven years of probation monitoring, ordered separately, "
               "is not an insured cost at all.",
        "prevent": [
            "There is no version of this that a policy, a consultation or a "
            "supervisor rescues. It is on the list because it is the ceiling, and "
            "because the cost recovery number is the one therapists most "
            "underestimate.",
            "The detail worth carrying away is the $14,500. Money moving between "
            "a therapist and a client in either direction, for any reason, is its "
            "own separate cause of action under &sect;4982(j).",
        ],
    },
    {
        "slug": "discipline-case-the-two-year-rule-is-not-a-loophole",
        "group": "sexual",
        "t": "&ldquo;We could date if we ended therapy&rdquo;",
        "dek": "Said out loud in session, to a client the accusation described as "
               "vulnerable to exploitation. License surrendered, $12,515.",
        "role": "LMFT",
        "eff": "December 19, 2024",
        "case": "2002022002121",
        "hear": "OAH No. 2024040620",
        "facts": [
            "The client was seen weekly. His chart documented mood lability, "
            "feelings of emptiness and elevated suicide risk. The accusation "
            "expressly characterises those as &ldquo;symptoms of a patient "
            "vulnerable to exploitation&rdquo; &mdash; the chart the therapist "
            "wrote was used to establish that she knew.",
            "He disclosed romantic feelings. She said she felt the same, and told "
            "him they <i>could</i> pursue a relationship if they ended therapy. "
            "He cancelled his next appointment. The relationship began "
            "immediately.",
            "They used cocaine together. She also told friends and acquaintances "
            "that he had been her patient.",
            "His anxiety worsened over the course of the relationship and he "
            "began having panic attacks.",
        ],
        "charges": [
            ("B&amp;P &sect;4982(k)", leg("4982"),
             "Sexual relations with a former client inside the two-year window."),
            ("B&amp;P &sect;4982(d)", leg("4982"), "Gross negligence."),
            ("B&amp;P &sect;4982(m)", leg("4982"),
             "Failure to maintain confidentiality &mdash; telling friends he had "
             "been a client."),
            ("B&amp;P &sect;4982(c)", leg("4982"),
             "Use of a controlled substance in a manner dangerous to others."),
            ("B&amp;P &sect;4982(i)", leg("4982"),
             "Recklessly causing emotional harm."),
        ],
        "outcome": "License surrendered.",
        "cost": "$12,515, payable in full before any new license could ever issue.",
        "rule": "Two things in this case are misread constantly. First, the "
                "two-year rule in &sect;4982(k) is a prohibition, not a waiting "
                "period with a procedure attached &mdash; and ending therapy in "
                "order to start a relationship is the fact pattern &sect;729 "
                "singles out by name. Second, &sect;4982(k) prohibits "
                "<b>soliciting</b> sexual relations with a client. The sentence "
                "in the session was itself chargeable before anything else "
                "happened.",
        "ins": "Defense only, on every program a California therapist can buy. "
               "The confidentiality count &mdash; telling friends he had been a "
               "patient &mdash; is the one piece here that a HIPAA or "
               "privacy-defense sublimit might otherwise have touched, and those "
               "run $25,000 to $50,000; it does not survive being bundled into a "
               "sexual misconduct case.",
        "prevent": [
            "A client's disclosure of romantic feelings is clinical material. It "
            "is the one moment in this case where the alternative path was "
            "obvious and cheap: name it, keep it in the room, take it to "
            "consultation, document it.",
            "Note what the chart did here. Careful documentation of vulnerability "
            "is good practice and it is also the evidence that establishes what "
            "you knew. That is not an argument for thinner notes. It is an "
            "argument for behaving consistently with them.",
        ],
    },
    {
        "slug": "discipline-case-three-days-after-the-last-session",
        "group": "sexual",
        "t": "Coffee three days after the final session",
        "dek": "An intern who never told his supervisor, &ldquo;for fear of being "
               "fired.&rdquo; Four years of probation.",
        "role": "LMFT",
        "eff": "April 4, 2024",
        "case": "2002021002677",
        "hear": "OAH No. 2023060971",
        "facts": [
            "He treated the client for five months while still an intern. In what "
            "became the final session he told the client he had feelings for him. "
            "They agreed to end therapy and to meet for coffee three days later.",
            "A romantic and sexual relationship followed and ran for about two "
            "years and three months.",
            "He did not consult his clinical supervisor about any of it &mdash; "
            "the decision records his reason as fear of being fired.",
            "The client later called a crisis line and described feeling "
            "&ldquo;confused, anxious, distracted, worried, and was trying not to "
            "cave into pressure or guilt.&rdquo;",
        ],
        "charges": [
            ("B&amp;P &sect;4982(d) and (e)", leg("4982"),
             "Gross negligence, and violating the chapter and the Board's regulations."),
            ("B&amp;P &sect;4982(i)", leg("4982"), "Recklessly causing emotional harm."),
            ("B&amp;P &sect;4982(k)", leg("4982"),
             "Sexual relations with a former client within two years of termination."),
        ],
        "outcome": "Revocation stayed. Four years of probation.",
        "cost": "$4,254",
        "rule": "Pre-licensure conduct follows the license. He was an intern when "
                "this began and an LMFT when it was charged, and the discipline "
                "attached to the license he eventually held. The supervision point "
                "is statutory too: &sect;4982(u) makes violating the rules "
                "governing the gaining and supervision of experience its own "
                "ground for discipline.",
        "ins": "An associate covered under an employer's policy is usually not a "
               "named insured on it, and the employer has no reason to carry "
               "board-defense cover for someone else's registration. This is the "
               "single most common coverage gap for California associates, and it "
               "is the reason the individual policies start at roughly $35 to $65 "
               "a year for a registrant.",
        "prevent": [
            "The sentence &ldquo;for fear of being fired&rdquo; is the whole case. "
            "Every supervision relationship should be able to survive the "
            "disclosure that a supervisee is having a reaction to a client. If "
            "yours cannot, that is a fact about the placement worth acting on "
            "before it becomes a fact about your license.",
            "Consultation is not just protective clinically. A documented "
            "consultation is the single most useful piece of evidence a "
            "respondent can bring to a boundary case, and it did not exist here.",
        ],
    },
    {
        "slug": "discipline-case-eight-years-of-escalation",
        "group": "sexual",
        "t": "Eight years, one client, and four sessions on MDMA",
        "dek": "Trainee to intern to licensed private practice, with the same "
               "client throughout. License surrendered.",
        "role": "LMFT",
        "eff": "October 24, 2024",
        "case": "2002023000085",
        "hear": None,
        "facts": [
            "He treated the same client continuously from 2011, when he was a "
            "trainee, through his internship, to licensure and private practice "
            "in 2019.",
            "Physical contact escalated over years: from hugs, to lying together "
            "on the couch with him holding her from behind in what the record "
            "calls a bear hug. On several of those occasions she was aware he had "
            "an erection.",
            "Four sessions between 2014 and 2016 involved <b>MDMA taken by both "
            "the therapist and the client</b>, along with alcohol. During one, he "
            "removed her shirt, touched her breasts and kissed her.",
            "Outside sessions he socialised with her, sought emotional support "
            "from her about his own life, and sent emails and text messages "
            "signed &ldquo;Love, T.&rdquo;",
        ],
        "charges": [
            ("B&amp;P &sect;4982(k), with &sect;&sect;726 and 729", leg("4982"),
             "Two separate counts &mdash; sexual contact with an intimate part, "
             "and improper physical contact."),
            ("B&amp;P &sect;4982(d)", leg("4982"), "Gross negligence."),
            ("B&amp;P &sect;4982(i)", leg("4982"), "Recklessly causing emotional harm."),
            ("B&amp;P &sect;4982(c)", leg("4982"),
             "Administering a controlled substance in a manner dangerous to "
             "another person. &sect;4982(c) requires denial or revocation for "
             "anyone who uses or offers drugs in the course of performing MFT "
             "services."),
        ],
        "outcome": "License surrendered.",
        "cost": "$7,826",
        "rule": "&sect;4982(c) is the subdivision therapists working in "
                "psychedelic-adjacent settings should read most carefully. Its "
                "second sentence is mandatory: the Board <b>shall</b> deny or "
                "revoke for a licensee who uses or offers a controlled substance "
                "in the course of performing marriage and family therapy "
                "services. There is no clinical-context exception in the text.",
        "ins": "Nothing reaches this. Beyond the sexual misconduct exclusion, "
               "every therapist policy excludes criminal acts, and the "
               "administration of a Schedule I substance in session is one. A "
               "therapist practising legally in a ketamine-assisted or "
               "state-licensed psilocybin context needs to confirm in writing "
               "that the policy names that modality &mdash; several exclude "
               "practice outside the profession named on the declarations page.",
        "prevent": [
            "Eight years with one client through three levels of licensure is a "
            "structural risk, not a clinical one. Nobody with authority over the "
            "work ever saw it, because the supervisor changed each time the "
            "license did.",
            "Escalation cases almost never have a first bad act. Look for the "
            "first <b>unusual</b> act instead &mdash; the first hug, the first "
            "message signed with love &mdash; and treat that as the point where "
            "consultation was owed.",
        ],
    },
    {
        "slug": "discipline-case-denied-it-then-admitted-it",
        "group": "sexual",
        "t": "Denied it to her employer, admitted it two days later",
        "dek": "One of the few cases in this dataset proved at a full hearing by "
               "clear and convincing evidence. Registration revoked.",
        "role": "AMFT",
        "eff": "September 25, 2025",
        "case": "2002024000792",
        "hear": "OAH No. 2024120108",
        "facts": [
            "A coworker reported that the associate had said she was in a sexual "
            "relationship with a former client, and had brought him to a wedding "
            "as her date.",
            "She denied it to her employer, and denied it again to a private "
            "investigator the employer retained. She was terminated. Two days "
            "later she admitted it.",
            "She told the Board investigator the romantic and sexual relationship "
            "ran from late July to late August 2023. The last therapy session had "
            "been February 28, 2023 &mdash; five months earlier, and well inside "
            "the two-year window.",
            "Asked why she had denied it, she said she feared losing her job and "
            "her registration.",
        ],
        "charges": [
            ("B&amp;P &sect;4982(d)", leg("4982"), "Gross negligence."),
            ("B&amp;P &sect;4982(i)", leg("4982"), "Recklessly causing emotional harm."),
            ("B&amp;P &sect;4982(k), with &sect;&sect;726 and 729", leg("4982"),
             "Sexual relations with a former client within two years."),
        ],
        "outcome": "Registration revoked. This one was not settled &mdash; it was "
                   "proved at hearing by clear and convincing evidence.",
        "cost": None,
        "rule": "Five months is not two years. The clock in &sect;4982(k) runs "
                "from termination of therapy, and there is no procedure &mdash; "
                "no consent form, no consultation, no waiting list &mdash; that "
                "shortens it.",
        "ins": "The denial is the part with insurance consequences beyond the "
               "misconduct itself. Every policy contains a cooperation clause and "
               "most contain a provision voiding coverage for misrepresentation "
               "in connection with a claim. A false statement to an employer's "
               "investigator, made before any claim exists, is also the statement "
               "an insurer will read when deciding whether to defend.",
        "prevent": [
            "The two days between the denial and the admission cost more than the "
            "relationship did procedurally &mdash; they are why this went to "
            "hearing rather than settling, and a hearing means findings of fact "
            "on the record.",
            "If you are ever asked about conduct like this, the answer is not "
            "yours to improvise. That is the moment to call your own attorney, "
            "which is what a board-defense sublimit is for.",
        ],
    },
    {
        "slug": "discipline-case-the-slow-boil",
        "group": "sexual",
        "t": "Three years of small steps, no single event",
        "dek": "The most carefully documented escalation in the whole dataset. "
               "License surrendered, $8,039.",
        "role": "LMFT",
        "eff": "December 4, 2025",
        "case": "2002024001059",
        "hear": None,
        "facts": [
            "The client presented with anxiety and a history of sexual abuse and "
            "exploitation. The decision reconstructs the escalation month by "
            "month.",
            "Texting between sessions began around five months in and became "
            "daily. Gifts of stuffed animals. Hugging at the end of sessions. The "
            "therapist called the client &ldquo;little sister&rdquo; and told her "
            "she loved her. Sessions ran for hours, at night.",
            "She disclosed her own extramarital affair and her BDSM activities, "
            "and suggested the client might explore BDSM. She gave the client "
            "stiletto heels and shared photographs of herself in lingerie.",
            "She asked to share a photograph of the client in the stilettos with "
            "her boyfriend, who had a foot fetish. The two of them photographed "
            "themselves together in lingerie and sent the images to him. He then "
            "posted photographs and videos of the client on social media.",
            "There was a trip to a theme park and a hotel stay; the client slept "
            "in the therapist's bed. The therapist took calls from other clients "
            "in her presence and used their names. She told the client there "
            "would never be a final therapy session between them.",
        ],
        "charges": [
            ("B&amp;P &sect;4982(k)", leg("4982"), "Sexual misconduct with a client."),
            ("B&amp;P &sect;4982(c)", leg("4982"), "Substance use."),
            ("B&amp;P &sect;4982(m)", leg("4982"),
             "Failure to maintain confidentiality &mdash; the other clients named "
             "on speakerphone."),
            ("B&amp;P &sect;4982(i)", leg("4982"), "Recklessly causing emotional harm."),
        ],
        "outcome": "License surrendered.",
        "cost": "$8,039",
        "rule": "Read the confidentiality count. Taking a call from another "
                "client in the room, and saying that client's name, is a separate "
                "&sect;4982(m) violation with its own penalty range &mdash; "
                "stayed revocation, 60 to 90 days suspension, three to five years "
                "of probation. It would have been chargeable on its own, in an "
                "otherwise unremarkable practice.",
        "ins": "The sexual misconduct count makes the rest academic. Standing "
               "alone, the confidentiality breach is exactly what a privacy or "
               "HIPAA defense sublimit exists for, and those are the sublimits "
               "that vary most between programs &mdash; $25,000 on some, $50,000 "
               "on the highest.",
        "prevent": [
            "No step here is the step. That is the point of including it: an "
            "escalation case is a sequence of decisions each of which looked "
            "defensible against the one before it, and indefensible against the "
            "first one.",
            "The tell available at any point was structural, not moral. Sessions "
            "that run for hours, at night, with daily texting between them, are "
            "measurable. A practice that reviewed its own session lengths would "
            "have found this in month six.",
        ],
    },

    # ================================================================== dual
    {
        "slug": "discipline-case-pseudonyms-and-sleepovers",
        "group": "dual",
        "t": "&ldquo;Hope&rdquo; and &ldquo;Faith&rdquo;",
        "dek": "Two clients from a residential eating-disorder program, code "
               "names in the text messages, and two overnight stays. Five years "
               "of probation.",
        "role": "AMFT",
        "eff": "March 6, 2025",
        "case": "2002022002868",
        "hear": None,
        "facts": [
            "The associate ran roughly fifty sessions with a client at a "
            "residential recovery centre, then began informal texting during "
            "treatment.",
            "After discharge the contact became near-daily phone calls, weekly "
            "meetings, dinners, a trip to the coast, and two overnight stays at "
            "the therapist's home.",
            "They used pseudonyms &mdash; &ldquo;Hope&rdquo; and "
            "&ldquo;Faith&rdquo; &mdash; in their text messages so that nobody "
            "would know they were still in contact.",
            "She discussed her other clients with this client, by name.",
            "The facility terminated her for continuing to communicate with the "
            "client. The same pattern was alleged with a second client.",
        ],
        "charges": [
            ("B&amp;P &sect;4982(d)", leg("4982"),
             "Charged twice, and separately per client: gross negligence, and "
             "incompetence."),
            ("B&amp;P &sect;4982(i)", leg("4982"), "Recklessly causing emotional harm."),
            ("B&amp;P &sect;4982(m)", leg("4982"),
             "Failure to maintain confidentiality as to the other clients."),
        ],
        "outcome": "Revocation stayed. Five years of probation. Eight causes for "
                   "discipline in total.",
        "cost": None,
        "rule": "The findings in this decision are the cleanest statement of the "
                "California standard anywhere in the dataset. The therapist "
                "&ldquo;engaged in an avoidable dual relationship &hellip; "
                "simultaneously with the therapeutic relationship, which "
                "continued following the termination&rdquo; and &ldquo;fostered "
                "dependency &hellip; by engaging in frequent, non-urgent, and "
                "casual telephone, text message, and in-person "
                "communications.&rdquo; Two elements, both of which you can audit "
                "in your own practice this afternoon: is the second relationship "
                "<b>avoidable</b>, and is the contact <b>non-urgent</b>.",
        "ins": "This is squarely inside what board-defense cover is for, and it "
               "is the shape of case where the sublimit actually gets tested. A "
               "contested administrative hearing with an expert and a defense "
               "lawyer at $250 to $500 an hour will run past a $5,000 sublimit "
               "before the prehearing conference. The programs sold to California "
               "therapists carry $5,000, $25,000 or $35,000 of it.",
        "prevent": [
            "The pseudonyms are the part to notice. Choosing code names is an act "
            "of concealment, and concealment is the reliable signal that the "
            "person already knows. There is no clinical decision that improves "
            "when it becomes unspeakable to a supervisor.",
            "&ldquo;Non-urgent&rdquo; is the operative word in the finding. "
            "Between-session contact is not prohibited. Between-session contact "
            "with no clinical purpose, at volume, is what got charged.",
        ],
    },
    {
        "slug": "discipline-case-disciplined-for-emails",
        "group": "dual",
        "t": "Three years of probation for an email correspondence",
        "dek": "No touching. No meetings. No sex. &ldquo;Dear One,&rdquo; "
               "&ldquo;My Candle Light,&rdquo; &ldquo;Have faith in my "
               "guidance.&rdquo; $7,644.",
        "role": "LMFT",
        "eff": "July 24, 2025",
        "case": "2002022001270",
        "hear": "OAH No. 2024120237",
        "facts": [
            "This is the most useful case on this site for an ordinary therapist, "
            "because nothing obviously wrong happened. The entire factual record "
            "is an email correspondence.",
            "The emails were frequent, non-urgent, outside session, sometimes "
            "several in a day.",
            "They used terms of endearment: &ldquo;Dear One,&rdquo; "
            "&ldquo;Gorgeous,&rdquo; &ldquo;My Candle Light,&rdquo; &ldquo;Super "
            "Spirit.&rdquo;",
            "They contained statements of personal fondness &mdash; &ldquo;I will "
            "always be your Hero,&rdquo; &ldquo;you are treasured,&rdquo; and, on "
            "receiving gifts from the client, &ldquo;crying tears of "
            "gratitude.&rdquo;",
            "They contained prescriptive daily directives: &ldquo;Light a candle. "
            "Take a hot shower. Put on nice jammies.&rdquo;",
            "They positioned the therapist as the authority over the client's own "
            "judgement: &ldquo;If you were the professional practitioner then you "
            "could make that decision,&rdquo; and &ldquo;Have faith in my "
            "guidance.&rdquo;",
            "And they asserted merger, repeatedly: &ldquo;I am with you,&rdquo; "
            "&ldquo;Always beside you,&rdquo; &ldquo;You're still all around "
            "me.&rdquo;",
        ],
        "charges": [
            ("B&amp;P &sect;4982(d)", leg("4982"),
             "Gross negligence <i>and</i> incompetence, charged as separate "
             "causes: an avoidable dual relationship, and fostering dependency."),
            ("B&amp;P &sect;4982(i)", leg("4982"), "Recklessly causing emotional harm."),
        ],
        "outcome": "Revocation stayed. Three years of probation.",
        "cost": "$7,644",
        "rule": "Nothing in &sect;4982 requires physical contact, a meeting, or a "
                "financial relationship. Gross negligence and incompetence are "
                "measured against the standard of care, and the standard of care "
                "in California includes not fostering dependency. Warmth is not "
                "the violation. Volume, merger language, and positioning yourself "
                "as the client's decision-maker are.",
        "ins": "The clearest board-defense case in the set, and a good argument "
               "for reading your sublimit before you need it. $7,644 of the "
               "Board's costs were assessed on top of whatever the respondent paid "
               "her own lawyer; a $5,000 per-proceeding sublimit does not cover "
               "the first number, let alone both.",
        "prevent": [
            "Reread your own between-session messages from the last month as if "
            "an investigator were reading them. That is the entire exercise this "
            "case supports.",
            "Two specific habits are chargeable on this record: terms of "
            "endearment, and directive instructions about how the client should "
            "spend an evening. Both feel like care. Both appear in the findings.",
            "If a client's emails are escalating and yours are matching them, the "
            "answer is a conversation about the frame in session, documented, not "
            "a warmer reply.",
        ],
    },
    {
        "slug": "discipline-case-cannabis-with-a-client",
        "group": "dual",
        "t": "Smoked with a client, drove her home impaired, offered her Xanax",
        "dek": "&ldquo;I did put us in danger driving.&rdquo; Registration "
               "surrendered, $5,000.",
        "role": "AMFT",
        "eff": "July 24, 2025",
        "case": "2002024000596",
        "hear": "OAH No. 2025010815",
        "facts": [
            "Eight months of therapy, then two weeks of contact after "
            "termination. Frequent texting throughout.",
            "Three outings the associate himself characterised as social and "
            "&ldquo;not therapy.&rdquo; At the third, he used cannabis with the "
            "client and then drove her while impaired. His own words in the "
            "record: &ldquo;I did put us in danger driving&hellip; my judgment "
            "gets impaired when I'm using.&rdquo;",
            "He offered her Xanax. She declined. He admitted to abusing his own "
            "stimulant prescription.",
            "When she said she felt unsafe and wanted to go back to telehealth, "
            "he responded with statements the accusation characterises as "
            "coercive &mdash; &ldquo;I don't want to lose you.&rdquo; He told her "
            "&ldquo;I truly love and care about you,&rdquo; and offered to end "
            "therapy so they could be friends.",
            "He never raised any of it with his clinical supervisor.",
        ],
        "charges": [
            ("B&amp;P &sect;4982(d)", leg("4982"), "Gross negligence."),
            ("B&amp;P &sect;4982(i)", leg("4982"), "Recklessly causing emotional harm."),
            ("B&amp;P &sect;4982(e)", leg("4982"),
             "Attempting to violate &sect;4982(c) by <b>offering</b> to provide "
             "Xanax. The offer was refused; the attempt is still the violation."),
        ],
        "outcome": "Registration surrendered.",
        "cost": "$5,000",
        "rule": "&sect;4982(e) reaches violating, <b>attempting</b> to violate, "
                "or conspiring to violate any provision of the chapter or any "
                "Board regulation. That is how a refused offer becomes a cause "
                "for discipline, and it is also the hook that pulls the whole of "
                "title 16 of the California Code of Regulations into &sect;4982.",
        "ins": "Nothing here is insurable. Furnishing a controlled substance is a "
               "criminal act and every policy excludes those. The surrender means "
               "there was never a hearing to defend, which is the pattern across "
               "this dataset: the board-defense sublimit gets spent on advice and "
               "negotiation, not on trials.",
        "prevent": [
            "&ldquo;Not therapy&rdquo; is not a category that exists. The "
            "associate used that phrase himself to describe the outings, "
            "apparently believing it moved them outside the therapeutic "
            "relationship. It appears in the accusation as an admission.",
            "Every one of these cases involving an associate contains the same "
            "sentence: the supervisor was never told. Supervision is the cheapest "
            "risk control in the profession and it is free to the supervisee.",
        ],
    },
    {
        "slug": "discipline-case-asking-a-client-where-to-buy-drugs",
        "group": "dual",
        "t": "&ldquo;Do you know where a gal could get some E?&rdquo;",
        "dek": "Texted to a client after 54 documented sessions. Registration "
               "surrendered, $8,107.",
        "role": "AMFT",
        "eff": "October 24, 2024",
        "case": "2002023000019",
        "hear": None,
        "facts": [
            "After 54 documented sessions, the associate texted her client: "
            "&ldquo;Do you know where a gal could get some E or Molly or some "
            "shit like that? Asking for a friend.&rdquo; The conversation went on "
            "to drug types and quantities.",
            "Asked whether she was drunk, she replied &ldquo;Not drunk &ndash; "
            "high yes.&rdquo; She proposed taking mushrooms with the client.",
            "She disclosed being bisexual and &ldquo;interested in swinging,&rdquo; "
            "and said &ldquo;When I'm high, I'll do anything, I would try to "
            "sleep with you.&rdquo;",
            "She insisted the friendship be kept secret.",
            "The client complained to her employer and she was fired. She then "
            "asked the client not to report her to the Board.",
        ],
        "charges": [
            ("B&amp;P &sect;4982(d)", leg("4982"), "Gross negligence."),
            ("B&amp;P &sect;4982(i)", leg("4982"), "Recklessly causing emotional harm."),
            ("B&amp;P &sect;4982(e)", leg("4982"),
             "Violating or attempting to violate the chapter and the Board's "
             "regulations."),
        ],
        "outcome": "Registration surrendered.",
        "cost": "$8,107",
        "rule": "Asking a client not to report you to the Board is not a "
                "mitigating step taken in panic; it is an aggravating fact that "
                "goes in the accusation. The Board treats obstruction of its own "
                "process as its own category &mdash; 16 CCR &sect;1845 makes "
                "failure to cooperate with an investigation unprofessional "
                "conduct in its own right.",
        "ins": "$8,107 in cost recovery on a case that ended in surrender is a "
               "useful number to hold next to a sublimit. A therapist with a "
               "$5,000 per-proceeding board-defense benefit is out of pocket "
               "before the Board's own costs are even counted &mdash; and cost "
               "recovery is not a defense cost, so no sublimit pays it at all.",
        "prevent": [
            "Fifty-four sessions of ordinary work do not create a store of "
            "credit. The record is one text message thread.",
            "The moment after you realise you have sent something like this is "
            "the moment to call a lawyer and your supervisor, in that order, and "
            "not to call the client.",
        ],
    },
    {
        "slug": "discipline-case-drinking-at-lunch",
        "group": "dual",
        "t": "One afternoon: drank at lunch, came back, saw clients",
        "dek": "That is the entire factual record. Four years of probation, "
               "$5,190.",
        "role": "LMFT",
        "eff": "July 24, 2025",
        "case": None,
        "hear": None,
        "facts": [
            "Staff reported that the clinical director appeared drunk at work and "
            "smelled of alcohol.",
            "He admitted making what he called the unprofessional decision to "
            "drink at lunch and then return to provide individual psychotherapy "
            "to a client and to co-facilitate a men's group.",
            "There is nothing else in the record. One afternoon, no complaint "
            "from any client, no clinical harm alleged.",
        ],
        "charges": [
            ("B&amp;P &sect;4982(d)", leg("4982"), "Gross negligence."),
            ("B&amp;P &sect;4982(c)", leg("4982"),
             "Use of alcohol to an extent or in a manner dangerous or injurious "
             "to others, or that impairs the ability to practise safely."),
            ("B&amp;P &sect;4982(i)", leg("4982"), "Recklessly causing emotional harm."),
        ],
        "outcome": "Revocation stayed. Four years of probation.",
        "cost": "$5,190",
        "rule": "&sect;4982(c) does not require a diagnosis, a pattern, or a "
                "consequence. It requires use in a manner that impairs the "
                "ability to practise safely. A single session is enough, and the "
                "disciplinary guidelines put the floor for impaired ability at "
                "stayed revocation with 60 to 90 days of suspension and five "
                "years of probation.",
        "ins": "Impairment sits in the gap between what the policies cover and "
               "what actually happens. There is no malpractice claim here at all "
               "&mdash; no client sued, no damages &mdash; so the $1 million "
               "limit is irrelevant. The four-year probation, the monitoring "
               "costs of roughly $1,200 a year, and the ordered treatment are all "
               "uninsured.",
        "prevent": [
            "The report came from colleagues, not clients. Most therapists model "
            "their risk as arriving from the people they treat; in this dataset "
            "it arrives from coworkers, employers, other agencies and the "
            "Department of Justice far more often.",
            "California's diversion-style options for impaired licensees are "
            "worth knowing about before you need them, because they are a very "
            "different conversation to have with the Board than an accusation is.",
        ],
    },

    # ============================================================== records
    {
        "slug": "discipline-case-the-custody-letter",
        "group": "records",
        "t": "The letter written for the ex-spouse",
        "dek": "Confidentiality, altered records and a missed child abuse report, "
               "in one case. License surrendered, $12,242.",
        "role": "LMFT",
        "eff": "September 25, 2025",
        "case": "2002021001271 and 2002026000262",
        "hear": "OAH No. 2023020686",
        "facts": [
            "The therapist treated a client twice weekly for anxiety, depression "
            "and suicidality. The client's spouse later joined for couples work.",
            "After termination, the <b>ex-spouse</b> contacted the therapist and "
            "asked her to diagnose the client for her own files. She said he was "
            "drinking heavily, had a gun, might attempt suicide again, and that "
            "she was afraid he might kill the children first.",
            "The therapist wrote a &ldquo;To Whom It May Concern&rdquo; letter "
            "setting out the client's diagnosis, suicide attempts and treatment, "
            "and gave it to the ex-spouse. She had no consent from the client, "
            "was not appointed by any court, and had not been asked for it by the "
            "family court. It was presented at the custody hearing along with his "
            "records.",
            "When the Board investigated, the copies of the intake form, Notice "
            "of Privacy Practices, depression checklist and EMDR worksheet that "
            "the therapist produced <b>differed from the client's copies</b>: "
            "different handwriting, marks on different pages, different checklist "
            "entries bearing the same date.",
            "And on being told that the ex-spouse feared he would kill the "
            "children, no child abuse report was made.",
        ],
        "charges": [
            ("B&amp;P &sect;4982(d)", leg("4982"), "Gross negligence."),
            ("B&amp;P &sect;4982(m)", leg("4982"),
             "Failure to maintain confidentiality of information received in "
             "confidence during treatment."),
            ("B&amp;P &sect;4982(j)", leg("4982"),
             "A dishonest, corrupt or fraudulent act &mdash; the record "
             "discrepancies."),
            ("B&amp;P &sect;4982(w), with Penal Code &sect;11166", leg("4982"),
             "Failure to comply with the child abuse reporting requirements."),
        ],
        "outcome": "Stayed revocation with probation in September 2023, then "
                   "<b>license surrendered</b> in September 2025 under a condition "
                   "of that order. Cannot reapply for three years; all charges "
                   "deemed true and admitted for any future application; the "
                   "surrender forecloses any petition for reinstatement.",
        "cost": "$12,242",
        "rule": "Three separate rules collide here and each is worth stating on "
                "its own. A former client's confidentiality survives termination "
                "and survives the other spouse asking nicely. A record is a "
                "contemporaneous document; a later version that differs from the "
                "client's copy is evidence of a dishonest act under "
                "&sect;4982(j), not a correction. And a mandated report is "
                "triggered by a reasonable suspicion arising from information "
                "received in a professional capacity &mdash; including from a "
                "third party, and including about a former client's household.",
        "ins": "This is the case that best justifies the privacy sublimit on a "
               "policy. An unauthorised disclosure to a third party who then uses "
               "it in litigation is the paradigm HIPAA-defense claim, and those "
               "sublimits run $25,000 to $50,000. The record discrepancies are "
               "not insurable at all &mdash; the moment the allegation is "
               "alteration rather than error, the intentional-acts exclusion is "
               "in play.",
        "prevent": [
            "Never write a letter about a client for anyone who is not the "
            "client, without the client's written authorisation, and preferably "
            "not at all in a custody matter unless a court has appointed you.",
            "If you amend a record, amend it visibly: date the amendment, mark it "
            "as an amendment, and keep the original. A clean second version is "
            "the worst possible artifact to hand an investigator.",
            "Write the mandated report even when the source is a hostile ex-"
            "spouse and you doubt her. The reporting duty is a low bar by design "
            "and the assessment is not yours to make.",
        ],
    },
    {
        "slug": "discipline-case-seven-business-practice-failures",
        "group": "records",
        "t": "Revoked outright for how the practice was run",
        "dek": "Seven causes for discipline. No sexual misconduct, no substance "
               "use, no clinical error alleged at all.",
        "role": "LMFT",
        "eff": "July 24, 2025",
        "case": "2002022002849",
        "hear": "OAH No. 2024090623",
        "facts": [
            "A college student was told her sessions would be covered by "
            "insurance, based on the practice's website and a verbal assurance. "
            "She was then issued a superbill for $1,365 of out-of-network care "
            "her plan did not cover, and had to obtain an emergency grant from "
            "her college.",
            "Six of those sessions were provided during a period when the "
            "therapist's <b>license was not valid</b>.",
            "The practice advertised under a corporate name and a variant "
            "personal name rather than the name on the license.",
            "A second client's attorney requested records. The request was "
            "ignored for six months, and part of the record was never produced at "
            "all. Duplicate charges and charges for sessions that never happened "
            "were never explained or refunded. That client was then terminated "
            "abruptly, with no explanation and no referral.",
            "A third family received superbills carrying invalid diagnostic "
            "codes. Corrections were promised and then not made, and the parent "
            "had to pause the child's treatment.",
            "The Board investigator's calls, letters and emails went unanswered "
            "for over a year.",
        ],
        "charges": [
            ("16 CCR &sect;1845, via B&amp;P &sect;4982(e)", None,
             "Failure to cooperate with and participate in a Board investigation."),
            ("B&amp;P &sect;4982(y), with Health &amp; Safety Code &sect;123110",
             leg("4982"),
             "Willful failure to provide the client access to their own records."),
            ("B&amp;P &sect;4980(b), with &sect;4982(d) and (e)", leg("4980"),
             "Practising without a valid license."),
            ("B&amp;P &sect;4982(p), with &sect;651", leg("4982"),
             "Advertising in a false, fraudulent, misleading or deceptive manner."),
            ("B&amp;P &sect;4982(d), (j) and (n)", leg("4982"),
             "Gross negligence, a dishonest act, and failure to disclose the fee "
             "or the basis on which it would be computed before treatment began."),
            ("B&amp;P &sect;4982(d)", leg("4982"),
             "Gross negligence &mdash; abandonment, for the termination with no "
             "referral."),
            ("B&amp;P &sect;4982(i)", leg("4982"), "Recklessly causing emotional harm."),
        ],
        "outcome": "<b>License revoked outright.</b> No stay, no probation "
                   "&mdash; one of only a handful of unstayed revocations in "
                   "three years.",
        "cost": None,
        "rule": "Every count here is administrative and every one of them is "
                "avoidable with a calendar reminder or a template. &sect;4982(n) "
                "requires the fee, or the basis on which it will be computed, to "
                "be disclosed <b>before treatment commences</b>. Health &amp; "
                "Safety Code &sect;123110 gives a client the right to inspect "
                "their records within five working days and to receive copies "
                "within fifteen. &sect;4982(p) requires you to advertise under "
                "the name on your license. And 16 CCR &sect;1845 makes ignoring "
                "the Board its own violation, regardless of the merits of "
                "whatever it was investigating.",
        "ins": "The single most instructive case in the set for coverage, "
               "because almost none of it is insurable. Fee disputes and failure "
               "to collect or pay money are explicitly excluded on therapist "
               "policies. Practising on an expired license is outside the "
               "coverage grant entirely &mdash; the policy insures professional "
               "services you were licensed to render. Board defense would answer "
               "for the administrative case; nothing answers for the underlying "
               "conduct.",
        "prevent": [
            "Diary your renewal, and check it. Six sessions on a lapsed license "
            "converted an ordinary billing dispute into a revocation.",
            "Answer the Board. Every single time. The failure-to-cooperate count "
            "is available in every case and it carries the same penalty range as "
            "serious clinical misconduct.",
            "Put the fee, the basis of the fee, and your out-of-network status in "
            "writing before the first session, and have the client sign it. "
            "&sect;4982(n) is one of the easiest subdivisions in the statute to "
            "comply with and one of the easiest to forget.",
            "Respond to a records request in writing within the statutory window "
            "even if you are disputing it.",
        ],
    },
    {
        "slug": "discipline-case-the-address-of-record",
        "group": "records",
        "t": "The address of record",
        "dek": "A separate, chargeable violation for not telling the Board where "
               "you are.",
        "role": "LMFT",
        "eff": "April 4, 2024",
        "case": None,
        "hear": None,
        "facts": [
            "The accusation charged gross negligence and failure to cooperate "
            "with the Board's investigation &mdash; and, as its own separate "
            "count, failure to maintain a current address of record with the "
            "Board.",
            "The license was surrendered.",
        ],
        "charges": [
            ("16 CCR &sect;1804", None,
             "Failure to maintain a current address of record with the Board."),
            ("B&amp;P &sect;4982(d)", leg("4982"), "Gross negligence."),
            ("16 CCR &sect;1845, via &sect;4982(e)", None,
             "Failure to cooperate with the investigation."),
        ],
        "outcome": "License surrendered.",
        "cost": None,
        "rule": "16 CCR &sect;1804 requires every licensee and registrant to keep "
                "a current address of record on file with the Board, and it is "
                "the address the Board uses to serve you. This is the shortest "
                "case in the library and it is here for a structural reason: an "
                "accusation served on a stale address is still served. The "
                "failure-to-cooperate count in most of these files begins with "
                "letters that went to an address the licensee had moved out of.",
        "ins": "Nothing to insure and nothing to defend. Worth noting that "
               "several therapist policies also require notice to the insurer at "
               "your current address, and a missed renewal notice is how "
               "claims-made coverage lapses.",
        "prevent": [
            "Update your address of record within 30 days of moving, in the "
            "BreEZe system, and separately from your public practice address.",
            "Do the same with your malpractice carrier and, if you are an "
            "associate, with your supervisor of record.",
        ],
    },

    # ================================================================ money
    {
        "slug": "discipline-case-forged-supervisor-signature",
        "group": "money",
        "t": "The supervisor had died, and the hours still needed signing",
        "dek": "The &sect;4982(u) case &mdash; experience hours, a forged "
               "signature, and an email chain that documented all of it.",
        "role": "AMFT",
        "eff": "December 4, 2025",
        "case": "2002024001984 and 2002025002324",
        "hear": None,
        "facts": [
            "The associate's supervisor of record had died. To complete her hours "
            "she sought signatures from other people at the agency.",
            "Per the accusation, she forged her supervisor's signature on an "
            "In-State Experience Verification form and a Weekly Summary of "
            "Experience Hours, submitted as part of her exam eligibility "
            "application.",
            "The decision reproduces the whole email chain, including her "
            "requests to agency staff to sign on the deceased supervisor's "
            "behalf, and the clinical director's replies of &ldquo;Here you "
            "go.&rdquo;",
            "The Board denied her LMFT application. She appealed. The accusation "
            "against her associate registration and the statement of issues on "
            "the license application were consolidated.",
        ],
        "charges": [
            ("B&amp;P &sect;4982(b)", leg("4982"),
             "Securing a license or registration by fraud, deceit or "
             "misrepresentation."),
            ("B&amp;P &sect;4982(j)", leg("4982"), "A dishonest or fraudulent act."),
            ("B&amp;P &sect;4982(u)", leg("4982"),
             "Violation of the statutes and regulations governing the gaining and "
             "supervision of experience."),
            ("B&amp;P &sect;4982(e), with 16 CCR &sect;1815.8 and B&amp;P "
             "&sect;&sect;4980.43 and 4980.50", leg("4982"),
             "&sect;1815.8 is the regulation that sets out how to prove hours "
             "when a supervisor is deceased or incapacitated. There was a "
             "procedure. It was not used."),
        ],
        "outcome": "Revocation stayed. Three years of probation.",
        "cost": None,
        "rule": "The disciplinary guidelines set the <b>minimum</b> penalty for "
                "fraud in securing a license at outright revocation. This "
                "settlement landed below the published minimum, which is worth "
                "knowing: the guidelines are the Board's starting point in "
                "settlement negotiation, not a ceiling on what can be negotiated.",
        "ins": "Outside every policy. Professional liability insurance covers "
               "professional services rendered to clients; an application for "
               "licensure is not one. This is a case for a licensing attorney, "
               "paid out of pocket, and it is exactly the situation where the "
               "board-defense sublimit some associates assume they have through "
               "an employer turns out not to exist.",
        "prevent": [
            "16 CCR &sect;1815.8 exists precisely for this. If your supervisor "
            "dies, becomes incapacitated, leaves without signing, or refuses to "
            "sign, there is a documented alternative route to proving your hours "
            "&mdash; use it, and start the paperwork the week it happens.",
            "Get your Weekly Summary signed weekly. Every case in the data "
            "involving hours begins with a backlog.",
            "Nobody at an agency has authority to sign for another supervisor, "
            "however senior and however willing. In this record the clinical "
            "director's cheerful cooperation is part of the evidence.",
        ],
    },
    {
        "slug": "discipline-case-twenty-three-sessions-in-one-day",
        "group": "money",
        "t": "23 sessions billed in a single day",
        "dek": "17.25 hours of psychotherapy. More than 24 sessions a day on 75 "
               "different dates. Seven felony counts.",
        "role": "LMFT",
        "eff": "September 25, 2025",
        "case": "2002024002764",
        "hear": None,
        "facts": [
            "A Department of Justice Medi-Cal Fraud and Elder Abuse investigation "
            "found that she had billed a managed care organisation for as many as "
            "<b>23 individual 45-minute psychotherapy sessions in a single "
            "day</b> &mdash; 17.25 hours of therapy &mdash; on at least two "
            "occasions.",
            "She billed one patient for 51 sessions. That patient had been seen "
            "once.",
            "Her Medi-Cal billings showed more than ten hours of therapy on 22 "
            "different days, including two days of 20.5 hours. Across all plans, "
            "she billed more than 24 sessions per day on 75 different dates.",
            "She was charged with seven felony counts of presenting false "
            "Medi-Cal claims and seven felony counts of insurance fraud, with "
            "aggravating-factor allegations for planning and sophistication, "
            "great monetary value, and taking advantage of a position of trust. "
            "She pleaded nolo contendere to one felony count and received two "
            "years of probation and restitution.",
            "She then ignored the Board's request for an explanation and "
            "attempted to withdraw her renewal application.",
        ],
        "charges": [
            ("B&amp;P &sect;490 and &sect;4982(a)", leg("490"),
             "Conviction of a crime substantially related to the qualifications, "
             "functions or duties of a licensee."),
            ("B&amp;P &sect;4982(j)", leg("4982"),
             "A dishonest, corrupt or fraudulent act &mdash; the false claims."),
            ("16 CCR &sect;1845, via &sect;4982(e)", None,
             "Failure to participate in the Board's investigation, <b>and</b> "
             "failure to report the conviction within 30 days."),
        ],
        "outcome": "License revoked.",
        "cost": None,
        "rule": "Note the separate count for failing to report the conviction. 16 "
                "CCR &sect;1845 requires a licensee to report any felony or "
                "misdemeanor conviction to the Board within 30 days &mdash; "
                "independently of the Department of Justice, which will report it "
                "anyway. Not reporting adds a cause for discipline with a "
                "penalty range of its own and removes any argument about candour.",
        "ins": "Billing fraud is uninsurable everywhere. What is worth knowing is "
               "that a billing <b>audit</b> is not: several therapist policies "
               "carry a small sublimit for the cost of responding to a payer's "
               "records request or audit, which is the stage before this. That is "
               "the coverage to check if you take Medi-Cal or Medicare.",
        "prevent": [
            "Reconcile what your billing service submits against your own "
            "calendar quarterly. In a group practice or under a billing company, "
            "the claim goes out under your NPI whoever pressed the button.",
            "Report a conviction to the Board yourself, within 30 days, before "
            "the Department of Justice feed does it for you.",
        ],
    },
    {
        "slug": "discipline-case-embezzlement-outside-the-practice",
        "group": "money",
        "t": "62 checks written at a bookkeeping job, and a revoked registration",
        "dek": "Nothing to do with therapy, no client involved, and the "
               "registration went anyway.",
        "role": "AMFT",
        "eff": "February 12, 2026",
        "case": "2002025001092",
        "hear": None,
        "facts": [
            "She was employed as an accounts payable clerk at a plumbing company "
            "&mdash; a job with no connection to her registration or to any "
            "client.",
            "She wrote 62 checks to herself, totalling $183,200.",
            "She was convicted on 33 felony counts of grand theft by embezzlement "
            "and one count of money laundering, with an aggravated white-collar "
            "crime enhancement. The sentence was 365 days in county jail stayed, "
            "two years of supervised probation, and $195,600 in restitution.",
        ],
        "charges": [
            ("B&amp;P &sect;490 and &sect;4982(a)", leg("490"),
             "Conviction of a substantially related crime."),
            ("B&amp;P &sect;490 and &sect;4982(j)", leg("490"),
             "A dishonest, corrupt or fraudulent act substantially related to the "
             "duties of a licensee."),
        ],
        "outcome": "Registration revoked.",
        "cost": None,
        "rule": "&ldquo;Substantially related&rdquo; is defined by 16 CCR "
                "&sect;1812 as conduct that to a substantial degree evidences "
                "present or potential unfitness, judged on three factors: the "
                "nature and gravity of the offence, the number of years since it "
                "happened, and the nature and duties of a marriage and family "
                "therapist. Dishonesty involving money and a position of trust "
                "clears that bar without ever touching a client.",
        "ins": "Entirely outside professional liability coverage &mdash; it is "
               "not a professional service, there is no claimant, and criminal "
               "acts are excluded. The board proceeding that follows is a "
               "board-defense claim, and it is the reason to check whether your "
               "sublimit is per proceeding or per year.",
        "prevent": [
            "The teaching point is simply that &sect;4982(a) and (j) reach your "
            "whole life. Bookkeeping, a second job, a shoplifting charge, a bar "
            "fight &mdash; the test is the &sect;1812 relationship test, not "
            "whether it happened at work.",
            "The Board learns about it automatically. Convictions and arrests "
            "arrive at BBS through the Department of Justice notification feed "
            "under Penal Code &sect;11105.2, which is the single largest source "
            "of BBS discipline. There is no version of this where nobody finds "
            "out.",
        ],
    },

    # ============================================================== another
    {
        "slug": "discipline-case-discipline-follows-your-other-license",
        "group": "another",
        "t": "The psychology board acted, and the MFT license followed",
        "dek": "&sect;4982.25(a): another board's discipline is itself "
               "unprofessional conduct here.",
        "role": "LMFT",
        "eff": "September 25, 2025",
        "case": "2002024001648",
        "hear": None,
        "facts": [
            "The California Board of Psychology disciplined the licensee's "
            "psychologist license in January 2024.",
            "BBS then filed its own accusation against the MFT license, on the "
            "basis of that discipline &mdash; plus a separate count for the "
            "underlying violations.",
        ],
        "charges": [
            ("B&amp;P &sect;4982.25(a)", leg("4982.25"),
             "Discipline by another state, territory or governmental agency on a "
             "healing-arts license is unprofessional conduct. A certified copy of "
             "the other decision is conclusive evidence."),
            ("B&amp;P &sect;4982(e)", leg("4982"),
             "The underlying conduct, charged again independently."),
        ],
        "outcome": "Revocation stayed. Two years of probation.",
        "cost": "$3,000",
        "rule": "&sect;4982.25 is the subdivision dual-licensed clinicians "
                "underestimate. It is not a re-hearing. The certified copy of the "
                "other board's decision is conclusive evidence of the facts "
                "found, so the only issue left in the California case is the "
                "penalty. Subdivision (b) does the same thing for discipline by "
                "BBS on another BBS license you hold.",
        "ins": "Board-defense sublimits are generally written per proceeding or "
               "per policy year. Two boards means two proceedings, and one of "
               "them may sit in a different policy year, which is either a "
               "second sublimit or a second retention depending on how the policy "
               "is worded. Read that clause if you hold more than one license.",
        "prevent": [
            "If any board anywhere opens a matter against you, tell your "
            "California licensing attorney immediately &mdash; the facts you "
            "settle in the first proceeding become conclusive in the second.",
            "The same applies to a settlement you might otherwise accept because "
            "it looks cheap. A stipulation in another state is not a private "
            "arrangement; it is evidence here.",
        ],
    },
    {
        "slug": "discipline-case-thirty-days-to-report-discipline",
        "group": "another",
        "t": "The 30 days that made it worse",
        "dek": "Another board's discipline, plus a separate count for not "
               "reporting it. License surrendered.",
        "role": "LMFT",
        "eff": "September 25, 2025",
        "case": "2002025000504",
        "hear": None,
        "facts": [
            "The Board of Psychology disciplined the licensee's psychologist "
            "license in August 2024.",
            "He did not report that discipline to BBS within 30 days. That "
            "failure was charged as a separate cause.",
        ],
        "charges": [
            ("B&amp;P &sect;4982.25(a)", leg("4982.25"),
             "Discipline by another licensing entity."),
            ("16 CCR &sect;1845(c)(2), via &sect;4982(e)", None,
             "Failure to report discipline by another licensing entity to the "
             "Board within 30 days."),
        ],
        "outcome": "License surrendered.",
        "cost": "$1,859",
        "rule": "16 CCR &sect;1845 sets out five separate reporting and "
                "cooperation duties, and this is the one most often missed. "
                "Within 30 days you must report (1) any felony or misdemeanor "
                "conviction and (2) discipline by another licensing entity. You "
                "must also give the Board records within 15 days of a request, "
                "provide arrest documentation within 30 days of a request, and "
                "cooperate with any investigation. Accusations filed between "
                "2023 and 2025 cite the older lettering &mdash; &sect;1845(g)(1) "
                "and &sect;1845(h) &mdash; for the conviction-reporting and "
                "arrest-document duties; the current published text puts them at "
                "(c)(1) and (d).",
        "ins": "Nothing here is a claim. It is an obligation with a calendar "
               "date on it, and missing it converts one proceeding into two.",
        "prevent": [
            "Put a 30-day reminder in your calendar the day anything reportable "
            "happens, and report in writing so you have proof of the date.",
            "Report even when you think BBS already knows. The duty is on you and "
            "it is not discharged by someone else's notification.",
        ],
    },
    {
        "slug": "discipline-case-out-of-state-discipline",
        "group": "another",
        "t": "Disciplined in Arizona, surrendered in California",
        "dek": "A licence you keep current in another state is a live exposure "
               "here.",
        "role": "LMFT",
        "eff": "March 6, 2025",
        "case": "2002025000734",
        "hear": None,
        "facts": [
            "The Arizona Board of Behavioral Health Examiners disciplined the "
            "licensee's Arizona marriage and family therapy license.",
            "BBS charged that discipline under &sect;4982.25(a). The California "
            "license was surrendered.",
        ],
        "charges": [
            ("B&amp;P &sect;4982.25(a)", leg("4982.25"),
             "Discipline by another state on a healing-arts license."),
        ],
        "outcome": "California license surrendered.",
        "cost": "$2,345",
        "rule": "The statute says &ldquo;another state, territory, or any other "
                "governmental agency.&rdquo; It does not require that you were "
                "practising in California, that any California client was "
                "affected, or that the other state's rule has a California "
                "equivalent. Where the conduct is not a violation here, that "
                "affects the penalty, not the cause of action.",
        "ins": "Multi-state telehealth practice makes this common and most "
               "therapist policies are written for the states listed on the "
               "declarations page. If you hold licences in more than one state, "
               "confirm in writing that board defense applies to proceedings "
               "before <b>each</b> of those boards, not just the one where you "
               "live.",
        "prevent": [
            "Keep track of licences you are not using. An inactive out-of-state "
            "licence still generates discipline you must report here, and a "
            "renewal you forget is a lapse that can itself be charged.",
            "If you practise across state lines, know each board's reporting "
            "clock. They are not all 30 days.",
        ],
    },
    {
        "slug": "discipline-case-the-only-public-reproval",
        "group": "another",
        "t": "The floor of the sanction ladder",
        "dek": "A public reproval &mdash; the mildest formal outcome available, "
               "and the only one in three years.",
        "role": "LMFT",
        "eff": "March 6, 2025",
        "case": "2002024002761",
        "hear": None,
        "facts": [
            "The Medical Board of California publicly reprimanded the licensee's "
            "physician's certificate for unprofessional conduct and repeated "
            "negligent acts with a patient, requiring 40 hours of continuing "
            "medical education and cost recovery.",
            "BBS charged that discipline under &sect;4982.25(a) against the MFT "
            "license.",
        ],
        "charges": [
            ("B&amp;P &sect;4982.25(a)", leg("4982.25"),
             "Discipline by another California healing-arts board."),
        ],
        "outcome": "<b>Public Reproval</b> &mdash; the only public reprimand of "
                   "an MFT in the 2024&ndash;2026 data, and the mildest formal "
                   "discipline in the entire set. Cost recovery payable in full "
                   "within 90 days.",
        "cost": "Ordered, payable within 90 days.",
        "rule": "It is worth knowing the whole ladder, because most therapists "
                "only ever hear about the top of it. In ascending order: a "
                "citation and fine, which is not formal discipline; a public "
                "reproval; probation, typically three to five years; suspension; "
                "surrender; revocation. In four years of Board data there were "
                "three public reprovals in total across every license type, and "
                "between 7 and 26 revocations a year.",
        "ins": "A public reproval is still public, and still reportable to every "
               "payer panel and credentialing body you belong to. The cost of "
               "getting there &mdash; counsel, the response, the negotiation "
               "&mdash; is what board defense pays for, and the outcome is the "
               "argument for spending it.",
        "prevent": [
            "The distance between a reproval and probation is usually the quality "
            "of the response, not the gravity of the conduct. That response is "
            "the thing worth paying a licensing attorney for.",
        ],
    },

    # ============================================================== fitness
    {
        "slug": "discipline-case-ignoring-an-order-to-be-examined",
        "group": "fitness",
        "t": "The order to be examined is not a request",
        "dek": "Three cases, three revocations, and in one of them no &sect;4982 "
               "charge at all.",
        "role": "LMFT",
        "eff": "April 4, 2024; July 24, 2025; August 15, 2024",
        "case": "2002024000682, 2002021002700 and 2002023000786",
        "hear": None,
        "facts": [
            "In the first case, the Board issued an order in November 2023 "
            "compelling a mental or physical examination within 30 days, by a "
            "psychiatrist or psychologist of the Board's choosing. The licensee "
            "did not comply. The accusation contained a single cause: B&amp;P "
            "&sect;821. There was no &sect;4982 charge of any kind. The license "
            "was revoked.",
            "In the second, the same pattern followed a December 2023 order, "
            "charged under &sect;822. Revoked.",
            "In the third, an associate was charged under &sect;&sect;820 and "
            "822 &mdash; found unfit to practise &mdash; alongside a conviction "
            "count for vandalism and resisting arrest. Registration surrendered.",
        ],
        "charges": [
            ("B&amp;P &sect;820", leg("820"),
             "Where it appears a licensee may be unable to practise safely "
             "because of mental illness or physical illness affecting competency, "
             "the Board may order an examination."),
            ("B&amp;P &sect;821", leg("821"),
             "&ldquo;The licentiate's failure to comply with an order issued "
             "under Section 820 shall constitute grounds for the suspension or "
             "revocation of the licentiate's certificate or license.&rdquo; That "
             "is the whole section."),
            ("B&amp;P &sect;822", leg("822"),
             "Authority to revoke, suspend or restrict where the licensee is "
             "found unable to practise safely."),
        ],
        "outcome": "Two revocations and one surrender.",
        "cost": None,
        "rule": "&sect;821 is a standalone ground. It does not require the Board "
                "to prove you are unfit &mdash; only that it ordered an "
                "examination and you did not attend. The strategic trap is "
                "obvious in hindsight: a licensee who believes the underlying "
                "allegation is baseless declines to submit to an evaluation, and "
                "converts a case the Board might not have proved into one it "
                "cannot lose.",
        "ins": "The examination is at the licensee's own expense in practice, and "
               "the proceeding is a board matter, so the board-defense sublimit "
               "is what funds the lawyer who tells you to go to the appointment. "
               "This is the cheapest advice in the entire library and the most "
               "expensive to skip.",
        "prevent": [
            "Comply with the order and fight the conclusion. Those are two "
            "different things and only the first has a 30-day deadline.",
            "Call a licensing attorney the day a &sect;820 order arrives. Not the "
            "week it expires.",
        ],
    },

    # =========================================================== convictions
    {
        "slug": "discipline-case-two-duis-five-years-probation",
        "group": "conviction",
        "t": "Two DUIs, five years of probation: the most common case in California",
        "dek": "Sixty-two of 103 decisions cite &sect;4982(a). This is what the "
               "typical one looks like.",
        "role": "LMFT",
        "eff": "May 15, 2025",
        "case": "2002023000269",
        "hear": "OAH No. 2025010078",
        "facts": [
            "Two convictions for driving under the influence. The offences were "
            "in August 2022 and May 2023; the convictions came in February and "
            "April 2024.",
            "There was no client complaint, no clinical allegation, and nothing "
            "connected to the practice. The Board learned of both through the "
            "Department of Justice conviction notification feed.",
            "Each conviction was charged as a <b>separate cause for "
            "discipline</b>.",
        ],
        "charges": [
            ("B&amp;P &sect;&sect;490 and 4982(a), with 16 CCR &sect;1812",
             leg("490"),
             "Conviction of a substantially related crime &mdash; one cause per "
             "conviction."),
            ("B&amp;P &sect;4982(c)", leg("4982"),
             "Use of alcohol in a manner dangerous to self, others or the public."),
        ],
        "outcome": "Revocation stayed. Five years of probation.",
        "cost": "$2,201",
        "rule": "This is the modal California MFT discipline case and almost "
                "nobody expects it. It arrives from the Department of Justice, "
                "not from a client. The disciplinary guidelines set the floor for "
                "a substantially related conviction at stayed revocation, 60 days "
                "of suspension and five years of probation, and the standard "
                "probation conditions include telling your clients and your "
                "employer that you are on probation.",
        "ins": "Nothing. There is no claim, no claimant and no professional "
               "service involved, so the malpractice limit is irrelevant. Some "
               "programs will fund counsel for the administrative proceeding out "
               "of the board-defense sublimit; the $2,201 in cost recovery, the "
               "probation monitoring fees of roughly $1,200 a year, and five years "
               "of ordered treatment and reporting are all out of pocket.",
        "prevent": [
            "Report the conviction to the Board within 30 days yourself. The "
            "reporting failure is a separate cause and it is the difference "
            "between two counts and three.",
            "Understand what probation actually involves before you decide "
            "whether to fight: quarterly reports, notification to clients, "
            "notification to employers, and coursework that cannot be counted "
            "toward your continuing education.",
        ],
    },
    {
        "slug": "discipline-case-failing-to-report-your-own-conviction",
        "group": "conviction",
        "t": "A reckless driving conviction, charged six times",
        "dek": "Three causes on the MFT registration, then the same three "
               "repeated on the counsellor registration.",
        "role": "AMFT",
        "eff": "February 12, 2026",
        "case": "2002023001203",
        "hear": "OAH No. 2025060012",
        "facts": [
            "A reckless driving conviction in August 2024.",
            "Charged under &sect;490 and &sect;4982(a) for the conviction, under "
            "&sect;4982(c) for the substance use, and under a third cause for "
            "failing to report the conviction to the Board within 30 days.",
            "She also held a registration as an associate professional clinical "
            "counsellor. The <b>same three causes were repeated</b> against that "
            "registration under the parallel provisions of &sect;4999.90.",
        ],
        "charges": [
            ("B&amp;P &sect;&sect;490 and 4982(a)", leg("490"), "The conviction."),
            ("B&amp;P &sect;4982(c)", leg("4982"), "Substance use."),
            ("16 CCR &sect;1845(c)(1), via &sect;4982(e)", None,
             "Failure to report the conviction within 30 days."),
            ("B&amp;P &sect;4999.90(a) and (c)", leg("4999.90"),
             "The identical grounds, applied to the APCC registration."),
        ],
        "outcome": "Both registrations revoked, revocations stayed, five years of "
                   "probation.",
        "cost": "$2,578",
        "rule": "Holding two BBS registrations does not halve your exposure, it "
                "doubles it. Every cause is pleaded twice, the probation runs on "
                "both, and &sect;4982.25(b) separately makes BBS discipline on "
                "one of your licences unprofessional conduct as to the other.",
        "ins": "Confirm whether your policy covers you for <b>each</b> licence "
               "you hold or only for the profession named on the declarations "
               "page. Several therapist policies exclude practice outside the "
               "named profession outright, which for a dual LMFT/LPCC registrant "
               "is a live question rather than a technicality.",
        "prevent": [
            "The reportable event is the <b>conviction</b>, not the arrest, and "
            "the clock is 30 days from it.",
            "If you hold a second registration, notify both. There is no shared "
            "record between the two files even though they sit at the same board.",
        ],
    },
    {
        "slug": "discipline-case-a-forty-year-license-surrendered",
        "group": "conviction",
        "t": "Licensed since the 1980s, surrendered after one DUI",
        "dek": "Offence in April, conviction in June, license gone by February.",
        "role": "LMFT",
        "eff": "February 12, 2026",
        "case": "2002025002528",
        "hear": None,
        "facts": [
            "The licensee had held an LMFT licence issued in the 1980s.",
            "A single DUI offence in April 2025, conviction in June 2025.",
            "Charged under &sect;4982(a) with &sect;490, under &sect;4982(c), and "
            "under the general unprofessional conduct provision.",
            "The licence was surrendered eight months after the offence.",
        ],
        "charges": [
            ("B&amp;P &sect;&sect;490 and 4982(a)", leg("490"),
             "Conviction of a substantially related crime."),
            ("B&amp;P &sect;4982(c)", leg("4982"), "Alcohol use."),
        ],
        "outcome": "License surrendered.",
        "cost": "$2,090",
        "rule": "Forty years of clean practice is not a defence to &sect;4982(a); "
                "it is a mitigating factor at the penalty stage. 16 CCR "
                "&sect;1812 lists the number of years that have elapsed <b>since "
                "the offence</b> as a factor &mdash; not the years of practice "
                "before it.",
        "ins": "A therapist near the end of a career should be thinking about "
               "tail coverage rather than board defense, and the two are "
               "unrelated. If your policy is claims-made, retiring or "
               "surrendering without an extended reporting endorsement leaves you "
               "uncovered for anything reported afterwards. Occurrence policies "
               "do not have this problem, which is why they are worth the "
               "premium difference.",
        "prevent": [
            "The choice between fighting and surrendering is an economic one at "
            "this stage of a career, and it should be made with a licensing "
            "attorney who can price both. Surrender ends the proceeding; it also "
            "usually forecloses reinstatement.",
        ],
    },
    {
        "slug": "discipline-case-charged-without-a-conviction",
        "group": "conviction",
        "t": "Charged for conduct that was never prosecuted",
        "dek": "Two convictions, and then two more causes for incidents that "
               "produced no conviction at all.",
        "role": "LMFT",
        "eff": "January 18, 2024",
        "case": "2002023000103",
        "hear": "OAH No. 2023070232",
        "facts": [
            "Convictions for disobeying a court order and for criminal threats.",
            "The accusation then added independent causes for unprofessional "
            "conduct based on a petty theft incident and a sexual battery "
            "incident that <b>were not themselves convictions</b>.",
        ],
        "charges": [
            ("B&amp;P &sect;&sect;490 and 4982(a)", leg("490"),
             "The two convictions."),
            ("B&amp;P &sect;4982 (chapeau)", leg("4982"),
             "Unprofessional conduct, charged directly for the unprosecuted "
             "incidents."),
        ],
        "outcome": "Revocation stayed. Three years of probation.",
        "cost": "$5,083",
        "rule": "The opening words of &sect;4982 are &ldquo;unprofessional "
                "conduct includes, but is not limited to, the following.&rdquo; "
                "The list of subdivisions is not exhaustive, and the Board can "
                "and does charge conduct directly under the chapeau where no "
                "subdivision fits and no conviction exists. A dismissed charge, "
                "a case declined by the district attorney, or an arrest with no "
                "filing is all still available to the Board on its own evidence "
                "and its own standard of proof.",
        "ins": "The gap this exposes is that criminal defence counsel and "
               "licensing defence counsel are different jobs. A plea that is "
               "excellent criminally &mdash; a reduction, a diversion, a "
               "no-contest plea &mdash; can be terrible for the licence, because "
               "the Board is not bound by the disposition. Board-defense cover "
               "pays for the second lawyer, and the time to instruct them is "
               "before the plea, not after.",
        "prevent": [
            "Tell your criminal defence attorney you hold a licence, at the first "
            "meeting, and get a licensing attorney involved before any plea.",
            "Do not assume that a charge that goes away goes away.",
        ],
    },
    {
        "slug": "discipline-case-from-dui-to-surrender",
        "group": "conviction",
        "t": "The whole arc: conviction, probation, then surrender seven months later",
        "dek": "The clearest illustration in the dataset of what failing "
               "probation costs.",
        "role": "LMFT",
        "eff": "June 26, 2025, then February 12, 2026",
        "case": "2002024002022 and 2002026002142",
        "hear": "OAH No. 2024080354",
        "facts": [
            "A DUI, then a conviction involving diverted drugs. Charged under "
            "&sect;4982(a) with 16 CCR &sect;1812, under &sect;4982(c), and under "
            "16 CCR &sect;1845 for failing to provide arrest documentation within "
            "30 days of the Board's request.",
            "In June 2025 the outcome was revocation stayed with five years of "
            "probation.",
            "Seven months later the licence was <b>surrendered</b> under Condition "
            "19 of that same order &mdash; the surrender-in-lieu-of-revocation "
            "condition that appears in every probation order the Board writes.",
            "The surrender carries a three-year bar on reapplying and no right to "
            "petition for reinstatement.",
        ],
        "charges": [
            ("B&amp;P &sect;4982(a), with 16 CCR &sect;1812", leg("4982"),
             "Conviction of a substantially related crime."),
            ("B&amp;P &sect;4982(c)", leg("4982"), "Dangerous drugs."),
            ("16 CCR &sect;1845(d), via &sect;4982(e)", None,
             "Failure to provide arrest documentation within 30 days of a Board "
             "request."),
        ],
        "outcome": "Five years of probation, then surrender seven months in.",
        "cost": None,
        "rule": "Every probation order contains a surrender-in-lieu-of-revocation "
                "condition. When probation fails, the Board does not have to "
                "start again &mdash; it invokes the condition already in the "
                "order. That is why the fifteen standard probation conditions are "
                "worth reading before you agree to them, not after.",
        "ins": "Probation is the uninsured part of every case in this library. "
               "Monitoring costs of roughly $1,200 a year, ordered evaluations, "
               "supervised practice arrangements, remedial coursework that cannot "
               "count toward continuing education, and lost income during "
               "suspension are all borne by the licensee. Board-defense cover "
               "pays for the hearing, not for the sentence.",
        "prevent": [
            "Take the terms seriously as a five-year operating constraint on your "
            "practice, not as paperwork. In the Board's own figures, 18 to 28 "
            "probations are revoked every year against 74 to 132 probationers "
            "&mdash; roughly one in five fails.",
        ],
    },

    # ============================================================ probation
    {
        "slug": "discipline-case-four-ways-to-violate-probation",
        "group": "probation",
        "t": "Four ways to violate probation, and one of them is not paying",
        "dek": "Including failure to pay the cost recovery from the original "
               "order.",
        "role": "LMFT",
        "eff": "December 19, 2024",
        "case": "2002024002031",
        "hear": "OAH No. 2020120643",
        "facts": [
            "The original discipline rested on a conviction under &sect;4982(a), "
            "a dishonest act under &sect;4982(j) &mdash; concealing damage to a "
            "rental car with body filler &mdash; and &sect;4982(e) with 16 CCR "
            "&sect;1845 for never answering a Board inquiry.",
            "The petition to revoke probation alleged four separate failures: not "
            "completing the ordered psychological evaluation; not obeying all "
            "laws; not submitting quarterly reports; and <b>not paying the cost "
            "recovery</b>.",
            "On the obey-all-laws condition, police responded to his office, "
            "where he was screaming. He had been living in the office, had "
            "confronted his landlord with an axe, and refused officers' orders.",
        ],
        "charges": [
            ("Probation Condition 1", None, "Failure to complete the ordered "
             "psychological evaluation."),
            ("Probation Condition 6", None, "Failure to obey all laws."),
            ("Probation Condition 7", None, "Failure to submit quarterly reports."),
            ("Probation Condition 21", None, "Failure to pay cost recovery."),
        ],
        "outcome": "License revoked.",
        "cost": "$4,530",
        "rule": "Cost recovery is a probation condition, which means not paying "
                "it is a violation of probation and an independent ground to "
                "revoke. B&amp;P &sect;125.3 lets an administrative law judge "
                "order a licensee to pay the reasonable costs of investigating "
                "and enforcing the case, including the Attorney General's "
                "charges. The judge may reduce or eliminate the amount but "
                "<b>cannot increase it</b> beyond the certified cost statement.",
        "ins": "Cost recovery is not a defence cost and no sublimit pays it. This "
               "is the number to plan for: in this dataset it runs from $882 for "
               "a single settled DUI to $15,883 for a contested sexual misconduct "
               "case, and it is separate from your own lawyer.",
        "prevent": [
            "If you cannot pay the cost recovery, negotiate a payment schedule "
            "into the order at the settlement stage. It is far easier than "
            "responding to a petition to revoke.",
            "File the quarterly reports even in quarters where nothing happened. "
            "Missing them is the most common single probation violation in the "
            "data.",
        ],
    },
    {
        "slug": "discipline-case-when-the-judge-cuts-the-bill",
        "group": "probation",
        "t": "The Board asked for $10,778. The judge ordered $4,000.",
        "dek": "How &sect;125.3 cost recovery actually gets decided.",
        "role": "LMFT",
        "eff": "June 26, 2025",
        "case": "2002023002059",
        "hear": "OAH No. 2023110124",
        "facts": [
            "On a petition to revoke probation, the Board sought $10,778 in costs "
            "&mdash; the largest cost-recovery request in a probation matter in "
            "this dataset.",
            "The final order set the amount at $4,000 and reinstated probation "
            "for three years.",
        ],
        "charges": [
            ("B&amp;P &sect;125.3", leg("125.3"),
             "Cost recovery. The certified cost statement is prima facie evidence "
             "of reasonable costs; the ALJ may reduce or eliminate the award, but "
             "may not increase it."),
        ],
        "outcome": "Probation reinstated for three years. Costs reduced from "
                   "$10,778 to $4,000.",
        "cost": "$4,000, reduced from a $10,778 request.",
        "rule": "Cost recovery is genuinely contestable, and it is the part of a "
                "disciplinary case respondents most often concede without "
                "argument. The Board's own figures show why it matters: across "
                "four years it ordered $229,823 in cost recovery and collected "
                "$67,857. The published statement is a starting point, not an "
                "invoice.",
        "ins": "Since no policy pays cost recovery, every dollar argued off it is "
               "a dollar out of the licensee's own pocket. That makes it one of "
               "the few places where paying a lawyer has a directly measurable "
               "return.",
        "prevent": [
            "Ask for the certified cost statement and read it. It itemises "
            "investigator and Attorney General time, and the reasonableness of "
            "each line is the thing in issue.",
        ],
    },
    {
        "slug": "discipline-case-seven-years-under-supervision",
        "group": "probation",
        "t": "Seven years on probation and counting",
        "dek": "Three extension cases, and what an extension actually means.",
        "role": "LMFT",
        "eff": "April 4, 2024; September 25, 2025; December 4, 2025",
        "case": "Three separate matters",
        "hear": None,
        "facts": [
            "One licensee's probation was extended by eighteen months, with "
            "$3,432 of cost recovery from the original order still unpaid.",
            "A second was extended by eighteen months with $4,040 in cost "
            "recovery outstanding.",
            "A third was extended by one year. That probation began with a case "
            "filed in 2018 &mdash; by the extension, seven years under Board "
            "supervision, and still running.",
            "A separate order in this group recites that cost-recovery "
            "obligations &ldquo;remain in effect whether or not probation is "
            "tolled.&rdquo;",
        ],
        "charges": [
            ("Probation conditions", None,
             "Extension rather than revocation is the Board's usual first "
             "response to a violation, and it resets nothing."),
        ],
        "outcome": "Probation extended in each case, by twelve to eighteen months.",
        "cost": "$3,432 and $4,040 outstanding in two of the three.",
        "rule": "Probation is tolled when you are not practising, which sounds "
                "protective and is not: the clock stops, the obligations "
                "continue, and the end date moves. Combined with extensions, a "
                "five-year probation routinely becomes seven or eight years of "
                "quarterly reports, employer notifications, client "
                "notifications and monitoring fees.",
        "ins": "There is nothing to insure here and that is the point. The most "
               "expensive part of a disciplinary case is the years afterwards, "
               "and it falls entirely outside every policy sold to therapists.",
        "prevent": [
            "When you model the cost of a disciplinary matter, model the "
            "probation, not the hearing. Monitoring at roughly $1,200 a year over "
            "seven years, plus ordered coursework that does not count toward your "
            "continuing education, plus the professional cost of telling every "
            "employer and every client.",
        ],
    },
]

# ------------------------------------------------------ the aggregate picture
AGGREGATE = [
    ("2,127", "complaints received by BBS in FY 2023-24", "across all licence "
     "types &mdash; up from 1,803 three years earlier"),
    ("1,006", "of them came from government agencies", "more than the 952 that "
     "came from members of the public"),
    ("47", "accusations filed that year", "out of 2,127 complaints"),
    ("415", "days, on average, from complaint to formal discipline", "against a "
     "540-day target"),
    ("7", "malpractice settlement reports in four years", "averaging $360,000 "
     "paid on behalf of the licensee"),
    ("51%", "of cases settle", "219 settled against 210 that went to hearing "
     "over four years"),
]

# The five grounds BBS cites most often when issuing a citation, verbatim from
# the 2025 Sunset Review Report, Q43.
CITATION_GROUNDS = [
    "Failure to complete specific continuing education coursework requirements",
    "Failure to maintain patient confidentiality",
    "Providing services for which licensure is required &mdash; unlicensed "
    "practice, or practising on an expired license",
    "Misrepresentation as to the type or status of a license or registration held",
    "Misrepresentation as to the completion of continuing education requirements",
]

# §4982 subdivisions, counted across the 103 decisions read.
SUBD_COUNTS = [
    ("(a)", "Conviction of a substantially related crime", 62,
     "Overwhelmingly the most cited ground. Mostly DUI."),
    ("(c)", "Substance use dangerous to self or others", 32,
     "Almost always paired with (a)."),
    ("(i)", "Intentionally or recklessly causing emotional harm", 13,
     "The standard companion count in every boundary case."),
    ("(e)", "Violating the chapter or a Board regulation", 12,
     "The hook that pulls all of 16 CCR into &sect;4982."),
    ("(d)", "Gross negligence or incompetence", 9,
     "Every dual-relationship case."),
    ("(k)", "Sexual misconduct with a client or former client", 6, ""),
    ("(j)", "A dishonest, corrupt or fraudulent act", 5, ""),
    ("(m)", "Failure to maintain confidentiality", 4, ""),
    ("(b), (p), (u), (w), (y)", "Fraud in licensure, advertising, experience "
     "hours, child abuse reporting, records access", 1,
     "One case each &mdash; and each one is in this library."),
]

# The fifteen conditions that appear in essentially every probation order.
PROBATION_TERMS = [
    ("Obey All Laws", "Any new offence is a violation."),
    ("File Quarterly Reports", "The single most commonly missed condition."),
    ("Comply With the Probation Program", ""),
    ("Interviews With the Board", ""),
    ("Failure to Practice / Tolling", "Stop practising and the clock stops, but "
     "the obligations do not."),
    ("Notify the Board of Any Change of Employment or Residence", ""),
    ("Supervision of Unlicensed Persons", ""),
    ("Notification to Clients", "You must tell your clients you are on probation."),
    ("Notification to Employer", "And your employer."),
    ("Violation of Probation", ""),
    ("Maintain a Valid License", ""),
    ("Surrender in Lieu of Revocation", "The condition the Board invokes when "
     "probation fails, without starting a new case."),
    ("Coursework Does Not Count Toward CE", "You pay for the ordered coursework, "
     "and then you pay for your continuing education separately."),
    ("Reimbursement of Probation Program Costs", "Roughly $1,200 a year."),
    ("Cost Recovery", "Separate from everything above."),
]

COST_BANDS = [
    ("$882 &ndash; $2,500", "A single DUI, settled early"),
    ("$2,500 &ndash; $5,500", "Multiple convictions, or a settled boundary case"),
    ("$5,000 &ndash; $8,200", "A contested boundary or dual-relationship case"),
    ("$7,600 &ndash; $12,500", "Sexual misconduct, or a multi-client "
     "business-practice case"),
    ("$15,883", "The highest in three years &mdash; the residential-facility "
     "sexual misconduct case"),
]
