#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The discussion layer for `case_data_more.py`.

Same separation as `case_depth.py` and for the same reason: the record file
says what the decision says, and this one says what it means. Keeping them
apart is what stops an interpretation from hardening into a fact the next time
somebody edits the record.

Keyed by slug. Every slug in `case_data_more.py` must appear here, and
`build_cases.py` fails the build if one does not.
"""

MORE_DEPTH = {
    "discipline-case-billed-for-sessions-that-never-happened": {
        "why": "It is the clearest example in the library of one course of billing "
            "conduct charged under five different subdivisions at once, with a "
            "records-destruction count that was entirely avoidable.",
        "disc": [
            "The headline is fraud, but the charging is what repays study. "
                "The Board pleaded the same billing conduct four ways &mdash; "
                "gross negligence, incompetence, dishonesty, and a catch-all "
                "chapter violation &mdash; because the subdivisions do "
                "different work. Gross negligence and incompetence under "
                "&sect;4982(d) do not require proof of intent. Dishonesty under "
                "&sect;4982(j) does. Pleading both means the case stands even "
                "if intent is contested at hearing, and it is why a therapist "
                "who thinks &ldquo;my billing was sloppy, not dishonest&rdquo; "
                "is describing a defense to one count and not to the others.",
            "The records count is the one most likely to catch a therapist "
                "who has done nothing else wrong. She repaid the payor in full "
                "and then destroyed the files &mdash; which reads, if you "
                "squint, like closing out a settled matter. It is not. Section "
                "4980.49 runs seven years from termination regardless of what "
                "happens with an insurer, and the shredding removed the only "
                "documents that could have supported her account of what care "
                "was delivered. Destroying records after an audit converts a "
                "billing dispute into a records case you cannot win.",
            "The emotional-harm count under &sect;4982(i) is worth sitting "
                "with, because the harm is financial in form and clinical in "
                "effect: a patient&rsquo;s annual benefit was consumed by "
                "sessions she never attended, so when the retreat did not help "
                "and she went looking for a different therapist, there was no "
                "coverage left to pay one. And the advertising count shows that "
                "an outcome claim &mdash; a weekend &ldquo;equivalent to one or "
                "more years&rdquo; of therapy &mdash; is independently "
                "chargeable under &sect;651 even where the person quoting it "
                "believed it.",
            "Finally, the aggravation. A 1999 citation carrying a $500 "
                "penalty for fraudulent billing to an employee assistance "
                "program was pleaded twenty-three years later, because it "
                "established that she had been told once already. Surrender is "
                "not the soft landing it sounds like: she cannot petition for "
                "reinstatement, must reapply from scratch after three years, "
                "must pay <b>$32,956</b> before any new license issues, and "
                "every allegation is deemed admitted in any proceeding to deny "
                "that application.",
        ],
        "ask": [
            "The respondent repaid the payor in full before the Board "
                "filed. What work does restitution do, and not do, in a "
                "disciplinary analysis &mdash; and how should a board weigh "
                "full repayment against a prior citation for the same kind of "
                "billing?",
            "Her advertisement claimed the weekend was equivalent to one or "
                "more years of therapy, and attributed the claim to past "
                "participants and to other professionals. What would a "
                "therapist need in hand before a claim like that stops being "
                "false advertising under &sect;651, and does attributing it to "
                "clients change the analysis?",
            "One patient&rsquo;s insurance allowance was exhausted by "
                "sessions she never attended, so she could not afford another "
                "therapist. Where does that consequence belong &mdash; as "
                "financial harm, as clinical harm, or as both &mdash; and what "
                "would you have to show to prove it?",
        ],
    },
    "discipline-case-a-decade-of-employer-warnings": {
        "why": "It shows how long a pattern can run inside employer HR processes "
            "before a single Board case gathers eleven years of it into one "
            "accusation.",
        "disc": [
            "What is unusual is not the conduct but the timeline. Four "
                "employers documented boundary problems and four responded "
                "internally: a suspension with mandated therapy, a law and "
                "ethics course, and a reflective paper in 2010; probationary "
                "status and a forced resignation in 2017; termination in 2020; "
                "a performance improvement plan, boundary trainings, and a site "
                "transfer in 2021. Each employer solved its own problem. He "
                "kept working, and the next employer started the clock again "
                "with no visibility into the last one. The Board&rsquo;s file "
                "was assembled only after the fact, out of records those "
                "employers had kept all along.",
            "Read the First Cause carefully. It is pleaded as sexual "
                "contact under &sect;726(a) and &sect;4982(k), but most of the "
                "underlying facts are touching, questioning, and texting. That "
                "is not a drafting stretch: &sect;4982(k) reaches solicitation "
                "and &ldquo;sexual misconduct,&rdquo; and does not require "
                "intercourse. The clinical setting is what gives the conduct "
                "its weight. Two of these clients were in treatment for "
                "domestic violence and sexual abuse, and the accusation says in "
                "terms that his abuse of power &ldquo;mirrors the coercive and "
                "controlling aspect of a domestic violence perpetrator&rdquo; "
                "&mdash; the harm was not incidental to the treatment, it "
                "reproduced the thing being treated.",
            "The Fourth Cause is the sleeper. Dishonesty under "
                "&sect;4982(j) was charged not for the conduct with clients but "
                "for what he told the investigator: a false account of how a "
                "job ended, a denial of prior employer discipline, and an "
                "account blaming clients for raising sexual topics. What you "
                "say during an investigation is itself chargeable, and it can "
                "stand even if the underlying allegations are contested. He was "
                "self-represented for the whole proceeding.",
            "The disposition also teaches something. His registration had "
                "already been canceled in July 2021 and could not be renewed "
                "&mdash; there was, in a practical sense, nothing left to take. "
                "Sections 118(b) and 4990.33 exist so that this does not end "
                "the matter: the surrender is what puts the discipline on the "
                "permanent record, makes every charge admitted against any "
                "future application, and attaches <b>$33,704</b> in costs that "
                "must be paid before any new registration or license can issue.",
        ],
        "ask": [
            "Four employers documented boundary complaints and none of them "
                "reported to the Board. Where in California law does an "
                "obligation to report a therapist&rsquo;s conduct sit, who "
                "actually holds it, and what should a clinical director do at "
                "the first complaint of this kind?",
            "The 2010 remediation was personal therapy, a law and ethics "
                "course, and a written paper about the incident. On what "
                "evidence, if any, should a program conclude that remediation "
                "of a boundary problem has worked well enough to restore client "
                "contact?",
            "The accusation treats his statements to the investigator as an "
                "independent dishonest act. How should a therapist under "
                "investigation describe a prior termination truthfully without "
                "waiving defenses &mdash; and what does that imply about "
                "answering an investigator before speaking to counsel?",
        ],
    },
    "discipline-case-underground-psychedelics-and-two-clients": {
        "why": "It is the library&rsquo;s clearest statement that the "
            "controlled-substance charge stands entirely on its own, "
            "independent of any finding about sex.",
        "disc": [
            "This is usually told as a psychedelics case, and the charging "
                "structure shows why that is only half right. The Board pleaded "
                "the drugs and the sexual conduct as separate causes, and the "
                "drug cause does not depend on the other. Section 4982(c) makes "
                "administering a controlled substance to a client "
                "unprofessional conduct, and closes with a mandatory revocation "
                "clause for anyone who uses or offers to use drugs in the "
                "course of performing therapy. Strip out every fact about "
                "touching and the license is still gone.",
            "The most useful detail for an ordinary therapist is where each "
                "relationship started. One client met him when he was the "
                "teaching assistant in her class and disclosed a rape in that "
                "setting; the other met him when he was a trainee at a center "
                "attached to her own graduate program. Neither began as "
                "therapy. Everything that followed &mdash; the retreat, the "
                "visit she paid for, the sessions that ran from morning to "
                "evening, the drives home, the dinner &mdash; was continuous "
                "with a relationship formed in a role that already carried "
                "authority. Boundary cases rarely begin with a boundary being "
                "crossed; they begin with a role being blurred.",
            "The language is worth teaching directly. Asking a client to "
                "&ldquo;give into the erotic transference&rdquo; while she is "
                "under psilocybin is not an interpretation of transference, it "
                "is an enactment of it dressed in clinical vocabulary. And "
                "telling a client that a &ldquo;connection was bigger than the "
                "rules of the BBS&rdquo; is a compact statement of exactly the "
                "reasoning those rules exist to defeat. The aftermath is part "
                "of the record too: therapy material used as leverage, 50 calls "
                "in two months, contact continuing after she asked him to stop, "
                "and a subsequent therapist documenting that he had tried to "
                "recast her wish to leave as pathology.",
            "Had this gone to hearing and produced a finding of sexual "
                "contact, &sect;4982.26 would have compelled revocation and "
                "forbidden any stay. A stipulated surrender avoids the finding "
                "but lands in much the same place: no reinstatement petition, "
                "reapplication only after three years as a new applicant, "
                "<b>$14,486</b> payable first, and every charge deemed admitted "
                "against that application.",
        ],
        "ask": [
            "Both relationships began in a teaching or trainee role rather "
                "than a clinical one. At what point does a role like teaching "
                "assistant, group facilitator, or peer supervisor become one "
                "from which you can never ethically accept a client, and what "
                "makes that line defensible?",
            "The respondent framed sexual contact as working with erotic "
                "transference. What distinguishes an interpretation of "
                "transference from an enactment of it, and what supervision or "
                "documentation would let a third party tell the difference "
                "after the fact?",
            "Section 4982(c) makes administering a controlled substance to "
                "a client grounds for discipline regardless of consent or "
                "perceived benefit. As legally sanctioned psychedelic-assisted "
                "therapy expands elsewhere, what conditions would have to exist "
                "before a California therapist could take part &mdash; and who "
                "should decide that a client is able to consent to it?",
        ],
    },
    "discipline-case-a-felony-assault-and-a-default": {
        "why": "A revocation that turned as much on a missed 15-day deadline as on "
            "the conviction behind it.",
        "disc": [
            "Two separate things are happening in this document, and they "
                "are worth pulling apart. One is a felony conviction. The other "
                "is a default. He filed no notice of defense within 15 days of "
                "service, which under Government Code &sect;11506(c) waives the "
                "right to a hearing, and the Board then proceeded under "
                "&sect;11520 on a default decision investigatory evidence "
                "packet, finding the allegations true by clear and convincing "
                "evidence without hearing a witness. Nothing about the "
                "conviction required that result; the silence did.",
            "Service was at the address of record, which is where the "
                "procedural trap sits. Section 136 makes maintaining that "
                "address an affirmative obligation, and service there is "
                "effective by operation of law. His registration had already "
                "expired in 2019, four years before the accusation was filed, "
                "but &sect;4990.33 keeps the Board&rsquo;s jurisdiction alive "
                "over an expired registration. A registrant who leaves the "
                "field, stops renewing, and stops updating an address has not "
                "exited the system &mdash; he has only stopped receiving mail "
                "from it, while the file stays open and the outcome becomes "
                "automatic.",
            "The substantial-relationship analysis is what converts a "
                "criminal case into a licensing case, and it is not "
                "self-evident here. The offense of conviction was assault by "
                "means likely to produce great bodily injury &mdash; a violence "
                "charge, not a professional one, arising from conduct that had "
                "nothing to do with a client. Section 490 and &sect;4999.90(a) "
                "require the crime to be substantially related to the functions "
                "of the license, and 16 CCR &sect;1812 defines that as "
                "evidencing present or potential unfitness. The circumstances "
                "the Board recited &mdash; a sexual assault that ended in "
                "strangulation, a second victim found by a human trafficking "
                "task force, a sentence including sex offender counseling and "
                "stay-away orders &mdash; are what supply the relationship.",
            "It is also a study in what rehabilitation evidence is for. "
                "Section 482 and 16 CCR &sect;1814 direct the Board to weigh "
                "completion of the sentence, compliance with probation, elapsed "
                "time, and whatever the licensee puts forward. In a default, "
                "nothing is put forward. Whatever mitigation existed went "
                "unsaid, and a default decision is a full revocation on the "
                "public record, with a seven-day window to move to vacate and "
                "no hearing on the merits at all.",
        ],
        "ask": [
            "The Board resolved this on default, without testimony. What is "
                "lost &mdash; for the registrant, for the public record, and "
                "for the next case that cites this one &mdash; when the facts "
                "are established by an investigative packet rather than at "
                "hearing?",
            "Section 490 requires that the crime be substantially related "
                "to the functions of the license. Build the strongest argument "
                "in both directions for a conviction arising from conduct with "
                "no client involved, and identify the single fact that decides "
                "it.",
            "The registration expired in 2019 and the accusation arrived in "
                "2023. What does a registrant who has left the profession owe "
                "the Board about an expired registration, an open "
                "investigation, and an address of record &mdash; and what would "
                "you advise a supervisee who says she is simply letting hers "
                "lapse?",
        ],
    },
    "discipline-case-letting-a-registration-lapse-on-probation": {
        "why": "It is the case that shows a probation can be reopened and "
            "lengthened with no new clinical misconduct at all.",
        "disc": [
            "The violation here is as small as a violation gets. Condition "
                "14 of her probation required her to keep a current and active "
                "registration. Hers had expired in August 2019 &mdash; more "
                "than two years before the probation even began &mdash; and was "
                "never renewed. That is the whole of the petition: one "
                "condition, no new clients, no new conduct, no complaint. She "
                "was notified in October 2022 that she was out of compliance, "
                "and under Condition 13 that notice alone extended her "
                "probation automatically.",
            "The underlying case is worth knowing because it is equally "
                "non-clinical. She was convicted of felony forgery for "
                "depositing five checks totaling <b>$19,000</b> drawn on the "
                "account of the father of a former partner, taken during a few "
                "unaccompanied minutes in his house, and she was separately "
                "charged under 16 CCR &sect;1845(h) for not producing arrest "
                "documentation to the Board after its request. No client was "
                "involved in any of it. The route from that conduct to a "
                "registration runs through &sect;4982(a) and the 16 CCR "
                "&sect;1812 substantial-relationship test, which reaches "
                "dishonesty wherever it occurs.",
            "The arithmetic of the outcome is the lesson for anyone "
                "currently on probation. Three years&rsquo; probation with "
                "$1,855 in cost recovery became a fresh stayed revocation and "
                "<b>42 months</b> &mdash; and the clock restarted on "
                "everything. A new psychological or psychiatric evaluation at "
                "her own expense, with binding recommendations. Weekly "
                "psychotherapy with a Board-approved clinician who reports "
                "quarterly on her fitness. A graduate law and ethics course "
                "that cannot count toward continuing education. Fingerprints, "
                "quarterly declarations under penalty of perjury, employer and "
                "client notification, no supervising anyone&rsquo;s hours, no "
                "teaching continuing education, and $1,200 a year in "
                "monitoring. A missed renewal bought all of that.",
            "The structural traps are the part to teach. Condition 13 "
                "extends probation automatically the moment a new petition is "
                "filed, or even requested from the Attorney General&rsquo;s "
                "office, so the end date on the paper is always provisional. "
                "Condition 14 says that when an expired registration is renewed "
                "it comes back subject to every term not yet satisfied. And the "
                "non-practice clause names the conditions that keep running "
                "whether or not you see a client. Together they mean the only "
                "exits from a probation are completing it or surrendering "
                "&mdash; and surrender is itself discipline, with no route back "
                "except reapplying from scratch.",
        ],
        "ask": [
            "The only proven violation was administrative: the registration "
                "was not kept current. Should an administrative lapse carry the "
                "same revocation exposure as clinical misconduct, and what does "
                "a board gain, or lose, by treating them alike?",
            "The underlying conviction was forgery against a private "
                "individual, with no client and no practice setting involved. "
                "Articulate the theory that connects it to fitness to practice "
                "therapy &mdash; and then say where that theory should stop.",
            "The respondent represented herself in both the original "
                "accusation and the petition to revoke. What could counsel "
                "realistically have changed at each stage, and how should a "
                "low-paid associate weigh the cost of representation against 42 "
                "months of monitored probation?",
        ],
    },
    "discipline-case-a-battery-conviction-and-a-default": {
        "why": "It shows that conduct with no connection to a client, outside "
            "working hours, can end a registration, and that not responding to "
            "an accusation is itself a decision with a fixed deadline.",
        "disc": [
            "The Board was not deciding whether the battery happened. Under "
                "Business and Professions Code section 493 the record of "
                "conviction settles that, and only that. The live questions "
                "were whether a misdemeanor battery against a former partner is "
                "substantially related to the duties of a clinical social "
                "worker, and what discipline that warranted. Both were decided "
                "on paper. Because the respondent defaulted, the Board weighed "
                "the conviction against nothing.",
            "That is the real lesson of the procedural posture. The "
                "regulations require the Board to consider rehabilitation "
                "criteria before revoking: the severity of the act, time "
                "elapsed, whether the licensee complied with criminal "
                "probation, expungement, and any rehabilitation evidence the "
                "licensee submits. She had a 104-hour domestic violence "
                "counseling requirement and a probation term that ran into late "
                "2022, which is exactly the material those criteria are built "
                "to receive. None of it was before the Board.",
            "One detail worth noticing: the accusation quoted title 16 "
                "section 1881(s)(1), the rule requiring a registrant to report "
                "any felony or misdemeanor conviction to the Board within 30 "
                "days, in its regulatory provisions, but the pleading contained "
                "only a single cause for discipline, based on the conviction. "
                "The Board reached her registration through the conviction "
                "alone. That the reporting rule was set out and not charged "
                "does not make it optional, and in other cases it is charged "
                "separately.",
            "The arrest was under Penal Code sections 243(e)(1) and "
                "417(a)(1); the conviction was under section 242. The plea to a "
                "lesser charge did not change the disciplinary analysis, "
                "because 242 is still a crime of violence and the Board may "
                "inquire into the circumstances surrounding the offense to fix "
                "the degree of discipline.",
        ],
        "ask": [
            "Section 493 makes the record of conviction conclusive proof "
                "that a conviction occurred, but only of that fact. What "
                "evidence about the surrounding circumstances would you want a "
                "board to hear before concluding that a misdemeanor battery "
                "shows unfitness to practice clinical social work?",
            "The regulation asks whether an act evidences &ldquo;present or "
                "potential unfitness.&rdquo; Construct the strongest argument "
                "that violence in a domestic dispute bears directly on an "
                "associate&rsquo;s clinical duties, and then the strongest "
                "argument that it does not.",
            "A newly arrested registrant faces a 30-day duty to report to "
                "the Board and a criminal defense attorney who will tell her to "
                "say nothing to anyone. How should she reconcile those "
                "obligations, and who should she consult before she writes "
                "anything down?",
        ],
    },
    "discipline-case-falsified-course-certificates-end-a-probation": {
        "why": "It is the clearest example of a probation that was substantively "
            "survivable and collapsed over paperwork, payments, and the way the "
            "respondent handled being caught.",
        "disc": [
            "The posture matters more than the headline. This was a "
                "petition to revoke probation, not an accusation. The Board was "
                "not asking whether the supervision misconduct occurred; that "
                "was admitted in 2021 and the revocation was already on the "
                "books, merely stayed. The only question was compliance. The "
                "decision spells out the consequence: an accusation must be "
                "proved by clear and convincing evidence, but a petition to "
                "revoke probation need only be proved by a preponderance. A "
                "probationer facing a violation is in a much weaker evidentiary "
                "position than she was the first time around.",
            "Read the timeline and most of it is recoverable. Conditions 1 "
                "and 2 were late, then cured, and the judge expressly found no "
                "evidence of non-compliance after February 11, 2022 and "
                "September 8, 2021 respectively. What was not recoverable was "
                "the education condition, because of how she tried to satisfy "
                "it. The Board&rsquo;s adopted decision made a technical change "
                "to one date, moving the submission of the certificates from "
                "December 30, 2021 to <b>April 14, 2023</b>. That single "
                "correction reorders the story: the certificates were not filed "
                "a year before the non-compliance notice, they were filed "
                "months after it. She described panicking when the notice "
                "arrived.",
            "The financial findings are the part most therapists will "
                "recognize. Around $20,000 of annual income, a divorce, "
                "repossessed cars, two dependent teenagers, and a probation "
                "that costs $800 a month in required therapy and supervision "
                "plus $1,200 a year in monitoring fees plus $170 a month in "
                "cost recovery. The judge did not dismiss any of that. What "
                "defeated it was the eight months after she took a better "
                "paying job in May 2023, during which nothing changed, and a "
                "request at hearing to extend probation rather than any showing "
                "of what she had already done.",
            "The evaluation section turns on candor, not hardship. Blaming "
                "the probation monitor for the signed orientation notes and for "
                "the falsified certificates is what the judge singled out as "
                "making further probation unsuitable. In a probation-violation "
                "hearing the respondent&rsquo;s own account of the violations "
                "is a large share of the evidence about whether supervision can "
                "work going forward.",
        ],
        "ask": [
            "Why should the standard of proof be lower in a petition to "
                "revoke probation than in the original accusation? What does "
                "that difference mean practically for a probationer deciding "
                "whether to contest an alleged violation or concede it?",
            "The underlying case was about supervising an associate and an "
                "out-of-date address of record. Which of these probation "
                "conditions were tailored to that misconduct and which were "
                "standard issue? What does the mismatch suggest about how "
                "probation programs are designed and what they are actually "
                "measuring?",
            "The order contained a voluntary surrender provision for a "
                "probationer unable to satisfy the terms. Compare what "
                "surrender would have cost this respondent against what "
                "revocation cost her, and identify the point in the timeline at "
                "which you would have advised her to consider it.",
        ],
    },
    "discipline-case-psychology-probation-reaches-a-second-license": {
        "why": "It is the cleanest illustration of the two-for-one problem: one "
            "set of clinical facts produced discipline on two licenses, plus a "
            "separate charge for saying nothing about the first.",
        "disc": [
            "This Board was not deciding whether she was negligent with her "
                "patients between 2018 and 2020. Those allegations were "
                "resolved by the Board of Psychology, and the statute makes a "
                "certified copy of that decision conclusive evidence of the "
                "discipline. The proceeding here is derivative by design. Once "
                "the first decision exists, the only real questions for the "
                "second board are what consequence follows on the second "
                "license and whether the licensee met her own reporting duty.",
            "The second cause is the one entirely within a licensee&rsquo;s "
                "control. The psychology discipline became effective March 28, "
                "2024 from a settlement she had personally signed. Thirty-one "
                "days later, on April 28, 2024, the report had still not been "
                "made, and the Board pleaded it. That is the trap: the "
                "reporting deadline falls in the exact period when a licensee "
                "is most absorbed by the first case and most likely to assume "
                "everyone already knows.",
            "The remedy shows some coordination between the two agencies. "
                "Her supervised practice condition here is expressly deemed "
                "satisfied by the supervision she is already performing under "
                "the psychology probation, so she is not paying twice for the "
                "same hour. She is, however, paying <b>$2,000</b> in cost "
                "recovery to this Board, plus $1,200 a year in monitoring, on "
                "top of whatever the psychology probation costs. Her "
                "educational psychology probation runs three years and the "
                "psychology probation runs four, and either can be extended "
                "automatically if a new pleading is filed against her during "
                "the term.",
            "For anyone doing educational assessment work, the underlying "
                "allegations are worth reading on their own. Two of the six "
                "concern records rather than treatment: failing to produce "
                "records to the regulator, and failing to transmit an "
                "independent educational evaluation report within 15 days of "
                "written requests from a parent. Turnaround obligations on "
                "assessment reports are a real disciplinary exposure and rarely "
                "feel like one at the time.",
        ],
        "ask": [
            "A certified copy of another board&rsquo;s decision is "
                "conclusive evidence of that discipline. If a licensee believes "
                "the first board got the facts wrong, what is genuinely left to "
                "argue in the second proceeding, and where should that argument "
                "be aimed?",
            "The 30-day reporting duty ran from an order the respondent had "
                "signed herself. What system would you build in a solo practice "
                "so that a self-reporting deadline survives the distraction of "
                "the case that created it?",
            "Her probation here is three years while her psychology "
                "probation is four, with the supervision term shared between "
                "them. What are the arguments for and against boards formally "
                "coordinating overlapping probations, and who bears the cost of "
                "the current arrangement?",
        ],
    },
    "discipline-case-a-mandated-report-never-filed": {
        "why": "It shows the mandated reporter duty tested against a year of "
            "session notes the clinician wrote herself, and how discipline on "
            "one healing arts license travels automatically to the other.",
        "disc": [
            "This Board never found that she failed to report. Its "
                "accusation contained one cause: her psychologist license had "
                "been disciplined, which section 4982.25(a) makes "
                "unprofessional conduct on its own. The facts came from a "
                "three-day hearing at the other board, and a certified copy of "
                "that decision is conclusive. That is why the entire substance "
                "of this file is a recitation of someone else&rsquo;s findings, "
                "and why the respondent had almost nothing left to contest by "
                "the time she was served.",
            "The evidence that decided the underlying case was her own "
                "charting. Her February 27, 2019 note records that the boy said "
                "&ldquo;dad was choking him&rdquo; and that the mother had seen "
                "the father pull the boys&rsquo; hair. Her April 29, 2019 note "
                "records a slap. Her September 4, 2019 note records a kick and "
                "a slap that left a red mark. At the hearing she argued the "
                "client had given less detail in session than she gave in "
                "testimony, but the notes answered that. Careful documentation "
                "of disclosures is the right practice; it also means the record "
                "of what you knew is written in your own hand.",
            "One note stands out. She wrote that she told the client to "
                "warn the father that if he leaves marks and the boys need "
                "medical care, she will have to tell the doctor what he did and "
                "the doctor will be legally obligated to call CPS. That is an "
                "accurate description of someone else&rsquo;s mandated "
                "reporting duty, offered in place of her own. The other board "
                "treated her lack of knowledge of her obligations as a "
                "competence problem rather than a lapse, which is a harsher "
                "finding than negligence about a single incident.",
            "The two dispositions are strikingly different. The board that "
                "actually heard the evidence imposed <b>three years of "
                "probation</b> and let her keep practicing. The board that "
                "inherited the finding as conclusive accepted a surrender. "
                "Surrender is discipline: it is public, it forecloses any "
                "reinstatement petition, it allows reapplication only after "
                "three years as a brand new applicant, it requires the $3,854 "
                "to be paid before any new license issues, and it provides that "
                "every charge in the accusation is deemed admitted in any "
                "future application proceeding before either board.",
        ],
        "ask": [
            "The clinician&rsquo;s progress notes were the central evidence "
                "in the underlying case. What does that imply about how to "
                "document a disclosure that you are not yet certain rises to "
                "reasonable suspicion, and how would you write such a note?",
            "She advised her client to warn the father that a physician "
                "would be obligated to call CPS. Identify precisely where that "
                "advice fails as a matter of the reporting law, and separately "
                "where it fails clinically for the client and the children.",
            "One board heard three days of evidence and imposed probation; "
                "the other treated the same facts as conclusive and accepted a "
                "surrender of the license. What explains that gap, and how "
                "should a dually licensed clinician evaluate a surrender offer "
                "from the second board?",
        ],
    },
    "discipline-case-two-nursing-actions-before-registration": {
        "why": "It shows how a second license&rsquo;s disciplinary history &mdash; "
            "here two nursing board actions in under three years &mdash; "
            "becomes the entire substance of a behavioral sciences application "
            "case, and how the Board answers with conditions rather than a "
            "closed door.",
        "disc": [
            "The Board was not deciding whether the respondent had done "
                "anything wrong as a therapist. She had never practiced as one. "
                "It was deciding a prediction question: whether two proven "
                "nursing board actions say enough about how she will behave as "
                "a marriage and family therapist to justify keeping her out. "
                "Title 16 sections 1812 and 1813 are the machinery for that "
                "question &mdash; 1812 asks whether the conduct evidences "
                "present or potential unfitness, and 1813 lists the "
                "rehabilitation factors that can offset it.",
            "The Board&rsquo;s answer was not no. It was a structured yes, "
                "and the structure is worth reading. Both nursing findings "
                "centered on false or grossly incorrect entries in hospital "
                "records. The education condition is <b>two graduate semester "
                "units in medical recordkeeping and documentation</b>, and the "
                "order says course content must be pertinent to the violation. "
                "The Board did not order a general ethics refresher; it ordered "
                "the specific skill that failed, and it put a supervisor with "
                "access to her fiscal and client records in the room once a "
                "week to watch it.",
            "The sequence matters more than it looks. The Board denied the "
                "application on September 17, 2024. The second nursing action "
                "&mdash; the surrender &mdash; issued on October 7, 2024, after "
                "the denial, and appears in the Statement of Issues filed the "
                "following February. An applicant who assumes the file closed "
                "when the denial letter arrived would be wrong.",
            "Note also what the probation does not end at. The order says "
                "probation continues on the same terms if she is later granted "
                "a subsequent registration, becomes licensed, or receives any "
                "other registration or license the Board regulates during the "
                "period, and that hours supervised under probation cannot be "
                "counted as experience toward licensure. The two years are two "
                "years of supervised practice that buys her nothing toward the "
                "3,000 hours.",
        ],
        "ask": [
            "The nursing findings were about charting and about medication "
                "given without physician orders. What in the daily work of an "
                "associate marriage and family therapist do those findings "
                "actually predict, and what do they not predict?",
            "The Board could have denied outright and required the "
                "respondent to reapply after a documented period of "
                "rehabilitation. Instead it issued the registration and "
                "controlled it for two years. Which route protects clients "
                "better, and what does each cost the applicant in time, money, "
                "and career?",
            "Section 4982.25(a) makes a certified copy of another "
                "board&rsquo;s decision conclusive evidence of the discipline. "
                "If an applicant believes the other board reached the wrong "
                "facts, where in this process, if anywhere, can that be argued "
                "&mdash; and should there be somewhere?",
        ],
    },
    "discipline-case-felony-child-endangerment-never-reported": {
        "why": "It is the clearest demonstration in the library that not answering "
            "an accusation is itself the losing move &mdash; the Board took "
            "every allegation as true without hearing a word from the "
            "respondent.",
        "disc": [
            "There is no rehabilitation analysis in this decision, and that "
                "is the point. The Board applied Government Code section 11520, "
                "which lets an agency decide a case on the evidence in its file "
                "when the respondent does not file a notice of defense. "
                "Everything that might have mattered &mdash; that the felony "
                "count was structured to drop to a misdemeanor after two years "
                "of successful probation, that she was already in a one-year "
                "child abuse treatment program and a 52-week domestic violence "
                "program, whatever a supervisor or colleague might have said "
                "&mdash; never reached a decisionmaker.",
            "The child endangerment count is the one worth sitting with. It "
                "came out of a family-court dispute over her own daughter, "
                "under a temporary guardianship order, with no client anywhere "
                "in the story. Section 4992.3(a) does not ask whether the crime "
                "happened at work. It asks whether the crime is substantially "
                "related, and title 16 section 1812 defines that as conduct "
                "evidencing present or potential unfitness. For a license whose "
                "holder works with families, children, and court-ordered "
                "arrangements, defying a custody order is not peripheral to the "
                "license &mdash; it sits close to its center.",
            "The third cause is the transferable one. Two criminal cases "
                "resolved on the same day, June 24, 2022, and both were "
                "reportable within the same 30 days. She reported neither, and "
                "she did not produce arrest documentation when the Board asked. "
                "Under section 4992.3(f), violating a Board regulation is its "
                "own cause for discipline, so the failure to report would have "
                "supported action even if the underlying convictions somehow "
                "had not.",
            "Her registration had already expired on December 31, 2021 "
                "&mdash; before either conviction was entered &mdash; and she "
                "never renewed it. Section 4990.33 made that irrelevant. "
                "Letting a registration lapse does not close a Board file, and "
                "a revocation entered against an expired registration is a "
                "permanent disciplinary record that any later application to "
                "any California health care board will have to answer.",
        ],
        "ask": [
            "The child endangerment conviction arose from a guardianship "
                "dispute over the respondent&rsquo;s own child, with no client "
                "involved. Under the &ldquo;substantially related&rdquo; test "
                "in title 16 section 1812, what is the argument that it bears "
                "on fitness to practice, and what is the strongest argument the "
                "other way?",
            "Her registration had expired before the convictions were "
                "entered, yet section 4990.33 preserved the Board&rsquo;s "
                "jurisdiction. What does an associate actually gain or lose by "
                "letting a registration lapse once they know an investigation "
                "is coming?",
            "The 30-day clock runs from the plea &mdash; often the moment a "
                "criminal defense lawyer tells a client the matter is finished. "
                "How should a supervisor prepare a supervisee, before anything "
                "happens, for the day they have to write that letter to the "
                "Board?",
        ],
    },
    "discipline-case-signed-her-supervisors-name": {
        "why": "It is the rare case where the Board rejected its own "
            "administrative law judge&rsquo;s proposed decision, decided the "
            "matter itself, and still gave a registrant who admitted forging a "
            "signature a supervised path back into practice.",
        "disc": [
            "The Board was deciding two questions from a single act. First, "
                "whether to revoke a registration that had already cancelled on "
                "its own at the six-year limit &mdash; section 4990.33 "
                "preserved jurisdiction, and the revocation matters because it "
                "stays in her license history permanently. Second, whether to "
                "grant the new registration she needed in order to work at all. "
                "It answered yes to both, which is why the order reads "
                "strangely: it revokes and grants in the same breath.",
            "The mitigation analysis rewards close reading. The Board found "
                "<b>a single act involving deliberate misrepresentation</b> "
                "whose impact was minimal, because the documents she signed "
                "were identical to unsigned copies the supervisor had already "
                "seen and accurately reflected the experience the supervisor "
                "had in fact supervised. In the same decision it noted that the "
                "supervisor could not confirm the forms&rsquo; accuracy at "
                "hearing, because she no longer had access to the "
                "agency&rsquo;s client records. The Board accepted that the "
                "harm was small while recording that nobody could any longer "
                "prove it &mdash; which is itself the argument for why the "
                "signature rule is absolute.",
            "Procedurally, this is a reminder that a proposed decision is a "
                "proposal. The administrative law judge heard the witnesses "
                "over two days and wrote a decision; the Board declined to "
                "adopt it, ordered written argument, and issued its own "
                "decision on the transcript under Government Code section "
                "11517. Either side can find the result changed after the "
                "hearing room empties.",
            "Costs are the last turn. The Board established $10,650 in "
                "prosecution costs and found the figure reasonable. Under "
                "Zuckerman v. State Bd. of Chiropractic Examiners (2002) 29 "
                "Cal.4th 32, a board must consider the licensee&rsquo;s "
                "good-faith belief in her position, whether she raised a "
                "colorable challenge, her ability to pay, and whether the "
                "investigation was disproportionate &mdash; so that a cost "
                "award does not punish people for asking for a hearing. Citing "
                "that she had been out of work since her registration cancelled "
                "and that the misconduct was a single act with minimal impact, "
                "the Board reduced the award to <b>$3,000</b>.",
        ],
        "ask": [
            "The Board called the impact of the misrepresentation minimal "
                "because the forged forms matched documents the supervisor had "
                "already reviewed. If the content was accurate, what exactly "
                "was the harm, and to whom?",
            "She admitted what she had done the same evening she learned "
                "the Board had contacted her supervisor. Title 16 section 1814 "
                "asks whether a person tried to correct a falsehood or tried to "
                "conceal it. Where on that line does a same-day admission after "
                "being caught fall, and how much weight should it carry?",
            "The Board rejected the administrative law judge&rsquo;s "
                "proposed decision and decided the case on the written record "
                "without seeing the witnesses. What is gained and what is lost "
                "when the body that sets the discipline is not the body that "
                "heard the testimony?",
        ],
    },
    "discipline-case-probation-traded-for-surrender": {
        "why": "It puts the two reporting deadlines, a below-guideline probation "
            "earned by a real rehabilitation record, and the true price of "
            "surrendering mid-probation into one file.",
        "disc": [
            "The substantive question was never seriously in doubt &mdash; "
                "a drunk driving collision at 0.15 percent is substantially "
                "related, and section 4982(c) separately reaches using alcohol "
                "in a manner dangerous to yourself or others. What the "
                "administrative law judge actually decided was how much "
                "discipline. The Board&rsquo;s own disciplinary guidelines set "
                "a minimum of revocation stayed with a 60-day actual suspension "
                "plus supervised practice, and for alcohol cases add testing "
                "and a rehabilitation program. The judge imposed the substance "
                "conditions and expressly declined the suspension, the "
                "supervised practice, and the rehabilitation program.",
            "What bought that departure is on the record: four years of "
                "testimony and a letter from her clinical supervisor, letters "
                "from four more colleagues, a completed work alternative "
                "program and DUI classes, twice-weekly attendance at a 12-step "
                "program, sustained abstinence, and a finding that no client "
                "had been exposed to harm. Against it, the decision is blunt "
                "about the aggravating side &mdash; a collision, phone use "
                "while driving, physical resistance to arrest, and a 2005 "
                "alcohol conviction that had already produced Board discipline. "
                "The word the judge used for the circumstances was "
                "&ldquo;troubling.&rdquo;",
            "The reporting counts are the most transferable part. The Board "
                "learned of the arrest from the Department of Justice within "
                "two days, so the reporting rule was never a discovery "
                "mechanism; it is a test of whether you told them yourself. She "
                "did not report the January 8, 2020 conviction, did not answer "
                "the April 15, 2020 letter within its 30 days, and said nothing "
                "until August 24, 2020. Each failure was found as an "
                "independent cause for discipline, standing next to the "
                "conviction rather than folded into it, and the Penal Code "
                "section 1203.4 dismissal she earned in March 2021 undid none "
                "of it.",
            "The ending is the reason this case is worth the space. Cost "
                "recovery was waived outright: the Department of Justice had "
                "billed the Board <b>$4,373.75</b> and the judge found the "
                "figure reasonable, then ordered nothing, because she was "
                "living paycheck to paycheck &mdash; the ability-to-pay factor "
                "that Zuckerman v. Board of Chiropractic Examiners requires a "
                "board to weigh. Then, before the three years ran, she took "
                "Condition 18. Surrender is written into every probation order "
                "as the humane exit, and it is: it stops the testing, the "
                "reports, and the bills. It is also recorded as discipline, "
                "blocks any reinstatement petition, bars any Board application "
                "for three years, and deems every charge in the case true and "
                "admitted if she ever applies again.",
        ],
        "ask": [
            "The judge found $4,373.75 in enforcement costs reasonable and "
                "then ordered the respondent to pay nothing, based on her "
                "ability to pay. What are the arguments for and against a board "
                "absorbing costs it has proven, and who ends up carrying them?",
            "The Board&rsquo;s guidelines set a floor of a 60-day actual "
                "suspension plus supervised practice, and the judge imposed "
                "neither. What evidence in this record justified going below "
                "the Board&rsquo;s own minimum, and what would you have wanted "
                "to see before agreeing?",
            "Surrender under a probation condition is voluntary, permanent, "
                "and recorded as discipline. What should a therapist weigh "
                "&mdash; financially, clinically, and in terms of future work "
                "&mdash; before choosing it over finishing probation?",
        ],
    },
    "discipline-case-thirty-four-year-sentence-then-registration": {
        "why": "It shows that the seven-year window in section 480 runs from "
            "release from incarceration rather than conviction, and that even a "
            "serious violent felony can end in a conditional yes rather than a "
            "permanent no.",
        "disc": [
            "On its face a 2003 conviction is two decades outside section "
                "480&rsquo;s seven-year window, and a reader could be forgiven "
                "for wondering how the Board had jurisdiction to deny at all. "
                "The answer is in the second half of subdivision (a)(1), which "
                "also opens the window for an applicant presently incarcerated "
                "for a substantially related crime, or released from "
                "incarceration for one within the preceding seven years. "
                "Discharged from parole in July 2021 and applying in August "
                "2023, he was well inside it. Anyone advising a returning "
                "citizen about when a record stops counting should read that "
                "sentence carefully: the clock most people assume runs from the "
                "conviction actually runs from getting out.",
            "The turn is what the Board did with the power once it had it. "
                "It denied the application in June 2024 and filed a Statement "
                "of Issues asking for denial. It then settled by granting the "
                "registration. The stipulation is not a finding that the "
                "conviction was minor &mdash; he admitted every allegation and "
                "agreed the application was deniable &mdash; it is a judgment "
                "that five years of monitored, supervised practice protects "
                "clients better than a closed door. Sections 481(c) and "
                "493(b)(2) push in the same direction by forbidding a "
                "categorical bar and requiring rehabilitation to be weighed.",
            "The conditions are the substance of the deal, and they are "
                "written to the offense rather than pulled off a shelf. A "
                "psychological or psychiatric evaluation comes first, within 90 "
                "days, with the respondent bound to comply with the "
                "evaluator&rsquo;s recommendations and the order providing that "
                "if the evaluator finds a need for supervised practice, that "
                "term gets added. Two graduate semester units in anger "
                "management, with course content required to be pertinent to "
                "the violation. Supervised practice &mdash; an hour a week, "
                "face to face, with an independent supervisor who gets access "
                "to his fiscal and client records &mdash; attaches once he "
                "reaches full licensure, and those supervised hours cannot be "
                "counted toward licensure experience. Five years is the longest "
                "probationary term in this group of cases.",
            "Two details matter for any applicant reading this. He waived a "
                "hearing and admitted the allegations, which converted a denial "
                "he would have had to litigate into a registration he could "
                "use, at the price of a five-year record and a conclusive "
                "admission. And the order provides that probation continues on "
                "the same terms if he is later granted a subsequent "
                "registration, becomes licensed, or receives any other "
                "Board-regulated license during the period &mdash; the five "
                "years follow the person, not the piece of paper.",
        ],
        "ask": [
            "Section 480 measures its seven-year window from release from "
                "incarceration rather than from conviction. What is the policy "
                "justification for measuring it that way, and what does it mean "
                "for an applicant who served a long sentence and has been out "
                "for three years?",
            "The Board must consider rehabilitation and may not bar an "
                "applicant categorically by conviction type. What specific "
                "evidence of rehabilitation would you want from an applicant "
                "with a violent felony before supporting registration, and "
                "whose job is it to assemble that record?",
            "The order requires a psychological evaluation, graduate "
                "coursework, weekly supervision, and five years of monitoring, "
                "all at the respondent&rsquo;s expense, at the entry level of "
                "the profession. At what point do conditions designed to "
                "protect clients become a financial barrier that screens by "
                "wealth rather than by risk?",
        ],
    },
    "discipline-case-eight-weeks-without-a-therapist": {
        "why": "It shows that probation is usually lost to administrative slippage "
            "rather than clinical misconduct, and that the slippage costs real "
            "time.",
        "disc": [
            "None of the three violations involved a client. One was a gap "
                "in her own therapy that opened when her therapist became "
                "unavailable, one was late paperwork about a job change, one "
                "was a late payment. That is the ordinary shape of a probation "
                "violation. The Board is not asking whether the registrant is a "
                "danger; it is asking whether the monitoring arrangement is "
                "working, and monitoring only works if every piece of it "
                "arrives on time.",
            "The psychotherapy condition is worth reading closely, because "
                "the burden it creates is one-sided. The registrant has to find "
                "a licensed therapist with no prior business, professional, or "
                "personal relationship with her, who is not her supervisor, who "
                "is willing to write quarterly reports to a licensing board "
                "about her fitness to practice, and who has to be approved "
                "before the first session. When that person becomes "
                "unavailable, the clock keeps running. Eight weeks passed "
                "between the last session and the replacement proposal, and the "
                "Board treated the whole gap as non-compliance. The condition "
                "also served two purposes at once &mdash; treatment and "
                "surveillance &mdash; and the second purpose is why a missed "
                "month counted even after the Board itself had relaxed the "
                "frequency to monthly.",
            "The non-practice condition catches people whose work is "
                "unstable. Notice is due 30 days <b>before</b> the gap, which "
                "means you have to predict it. She stopped on June 1, went back "
                "on July 18, and told the Board on August 30. The consequence "
                "was not just the violation: the seven weeks did not count "
                "toward her probation, so the end date had already moved from "
                "July 9, 2024 to August 24, 2024 before the petition was even "
                "filed.",
            "The disposition is the part to notice. The Board had the power "
                "to lift the stay and revoke the registration outright, which "
                "is what the petition asked for. Instead it revoked probation, "
                "stayed that revocation too, and added a consecutive year. A "
                "registrant who has slipped on compliance is not automatically "
                "finished; but the term grew from four years to five, and every "
                "condition, including the monthly therapy and the annual fee, "
                "ran for the extra year as well.",
        ],
        "ask": [
            "Condition 2 made the respondent responsible for keeping an "
                "approved therapist in place, but the therapist&rsquo;s "
                "availability was outside her control. Where should a licensing "
                "board place that risk, and how would you redraft the condition "
                "so it still protects the public?",
            "The Board reduced the therapy requirement from weekly to "
                "monthly and then treated two missed months as grounds to "
                "revoke. What purpose is the psychotherapy condition serving at "
                "that point, and can a single condition honestly serve both "
                "treatment and surveillance?",
            "The conduct underlying the original discipline was theft from "
                "a school district employer, with no clinical component and no "
                "client involved. Build the strongest case that four years of "
                "monitored practice was proportionate, and then the strongest "
                "case that it was not.",
        ],
    },
    "discipline-case-road-rage-and-a-default-revocation": {
        "why": "Two misdemeanors from a parking-lot argument would have been a "
            "contested case; the silence turned it into a revocation with no "
            "hearing at all.",
        "disc": [
            "The interesting question in this file is the one nobody got to "
                "argue. Section 493 and title 16, section 1812 require the "
                "Board to weigh the nature and gravity of the offense, the "
                "number of years elapsed, and the nature and duties of the "
                "profession before calling a crime substantially related, and "
                "section 493(b)(2) forbids categorically barring someone on the "
                "type of conviction without considering rehabilitation. Section "
                "1814 sets out a nine-factor rehabilitation analysis for "
                "exactly this situation, including whether the criminal "
                "sentence was completed without a violation of probation. None "
                "of that machinery ran. He defaulted, so the allegations were "
                "deemed true and the Board decided on its own evidence packet.",
            "The second cause is independent of the first. Even if he had "
                "argued successfully that a misdemeanor assault in a "
                "drive-through lane was not substantially related to sitting "
                "with clients, the failure-to-report violation would have stood "
                "on its own. The regulation runs from the date of conviction, "
                "not from the end of criminal probation, and the Board&rsquo;s "
                "two letters &mdash; five months apart &mdash; each triggered a "
                "separate 30-day production deadline. This is the trap for "
                "anyone whose criminal defense attorney has told them to say "
                "nothing to anyone.",
            "The registration expiring did not rescue him either. It "
                "expired on May 31, 2024, two weeks after service and before "
                "the decision issued, and was not eligible for renewal. The "
                "Board proceeded anyway under sections 118(b) and 4990.33, so "
                "the revocation is now permanently on his license history "
                "rather than a lapse that quietly disappeared.",
            "There is a narrow door left open. Government Code section "
                "11520(c) lets a defaulted respondent move to vacate within "
                "seven days of service of the decision on a showing of good "
                "cause, and the order says so expressly. Seven days is not "
                "long, and it starts running from service at the same address "
                "of record the previous three letters went to.",
        ],
        "ask": [
            "Section 493 directs a board to weigh the nature and gravity of "
                "the offense, the years elapsed, and the duties of the "
                "profession. Construct the professional-fitness argument "
                "connecting an off-duty assault in a drive-through lane to "
                "clinical work with clients, and then the strongest rebuttal.",
            "The racial slur appears in the factual allegations but is not "
                "itself a charged violation. What work is it doing in the "
                "document, and is it legitimate for uncharged conduct to shape "
                "a penalty?",
            "The reporting regulation runs from the date of conviction, "
                "while criminal defense counsel routinely advise saying nothing "
                "until the case is fully resolved. How should a registrant "
                "resolve that conflict, and whose job is it to tell them the "
                "two systems have different clocks?",
        ],
    },
    "discipline-case-almost-forty-years-of-rehabilitation": {
        "why": "It is the case that answers whether the door is open at all for an "
            "applicant with the most serious kind of record, and shows exactly "
            "what the Board weighed to open it.",
        "disc": [
            "The decision does two separate things, and readers who stop at "
                "the first will misread it. First, cause. Applying title 16, "
                "section 1812, the judge held the conviction substantially "
                "related, writing that the respondent committed the most "
                "serious crime of all, and found cause to deny the application. "
                "Nothing in the rehabilitation record disturbed that "
                "conclusion, and nothing was supposed to. Then the second "
                "question, which is the one the case is actually about: whether "
                "the applicant had shown enough rehabilitation that issuing a "
                "registration would protect the public. The purpose of a "
                "licensing proceeding is not to punish, and once the analysis "
                "reached that question the conviction stopped being the whole "
                "answer.",
            "Time did a lot of work, but not alone. Almost 40 years had "
                "passed since the crime, 13 since release, and 8 since "
                "discharge from parole, and the authorities the judge relied on "
                "treat the evidentiary significance of misconduct as greatly "
                "diminished by the passage of time and by the absence of "
                "similar, more recent misconduct, with sustained good conduct "
                "over an extended period the most crucial indicator. What made "
                "the time count was what filled it. The judge specifically "
                "noted that rehabilitation started inside: two degrees, AA, "
                "group and individual therapy, and giving up alcohol around "
                "1998, more than a decade before release. Then a parole term "
                "completed without a single violation, a support group he "
                "helped start for others coming off life sentences, a marriage, "
                "two more degrees, ongoing therapy, and continuous work. On top "
                "of that, an unqualified acknowledgment of wrongfulness &mdash; "
                "he had told police at the time that the victim never "
                "threatened him, and he did not walk that back &mdash; which "
                "the case law treats as an essential step toward rehabilitation "
                "rather than a nicety.",
            "The outcome is not an unrestricted registration, and the "
                "conditions are the honest part of the story. Five years of "
                "probation, a psychological or psychiatric evaluation within 90 "
                "days at his own cost with a duty to follow the "
                "evaluator&rsquo;s recommendations, weekly Board-approved "
                "psychotherapy with quarterly reports from the therapist, "
                "quarterly self-reports under penalty of perjury, notice to "
                "every employer and to clients whose therapy is affected, a bar "
                "on supervising anyone, in-person interviews on request, and "
                "reimbursement of the Board&rsquo;s monitoring costs. Those "
                "terms follow him if he later becomes a licensed professional "
                "clinical counselor.",
            "The Board&rsquo;s one edit is worth as much as the rest. It "
                "adopted the Proposed Decision but struck condition 3, the "
                "clinical diagnostic evaluation, which would have automatically "
                "suspended the registration for at least a month and required "
                "random drug testing twice a week. Nothing in the record "
                "connected this applicant to current substance use; he had not "
                "had a drink since about 1998. Removing a boilerplate condition "
                "that the facts did not support is the Board matching the order "
                "to the file rather than to the headline &mdash; and it is a "
                "reminder to anyone negotiating or contesting a proposed order "
                "that individual conditions can be argued separately from the "
                "penalty as a whole. The other procedural lesson is the "
                "plainest one in the file: he was denied on paper in July 2023 "
                "and had the right to appeal that denial; the registration "
                "exists because he asked for a hearing. The age of the "
                "conviction did not shield him &mdash; the seven-year lookback "
                "in section 480 does not apply to a serious felony &mdash; so "
                "the years were an argument to be made, not a bar the Board "
                "could not cross.",
        ],
        "ask": [
            "The decision holds both that the crime evidences present or "
                "potential unfitness and that the applicant is rehabilitated "
                "enough to register. Explain how those findings coexist, and "
                "identify precisely what the second one measures that the first "
                "does not.",
            "The rehabilitation authorities weigh elapsed time heavily. If "
                "this same evidence and this same testimony were offered 15 "
                "years after the offense rather than 39, which specific "
                "criteria in title 16, section 1813 would come out differently, "
                "and would the outcome change?",
            "The Board deleted the clinical diagnostic evaluation "
                "condition, with its automatic suspension and twice-weekly drug "
                "testing, from an otherwise standard order. Make the argument "
                "that a probation condition unsupported by the record is not "
                "merely unnecessary but affirmatively harmful, and propose a "
                "test for which standard conditions a board should apply.",
        ],
    },
    "discipline-case-serious-felonies-ignore-the-seven-year-rule": {
        "why": "It marks exactly where the seven-year lookback stops, and shows "
            "that a Statement of Issues can end in a registration rather than a "
            "denial.",
        "disc": [
            "Most of what people believe about section 480 comes from the "
                "2020 amendments, which cut boards back to convictions within "
                "the preceding seven years. The carve-out is less well known "
                "and is the whole case here. Subdivision (a)(1)(A) removes the "
                "seven-year limit for a serious felony as defined by Penal Code "
                "section 1192.7 and for offenses requiring sex offender "
                "registration. The Board cited two definitions of serious "
                "felony, and only one of them is dramatic: (c)(9) is attempted "
                "murder, but (c)(23) is any felony in which the defendant "
                "personally used a dangerous or deadly weapon. Under (c)(23), "
                "an ordinary assault-with-a-deadly-weapon count carries the "
                "same consequence. The practical rule for an applicant is that "
                "a weapon in the record probably means no clock is running.",
            "What this document does not contain is as instructive as what "
                "it does. It is a stipulated settlement, so there are no "
                "findings about the years between 2008 and 2024: no treatment "
                "record, no employment history, no letters, no testimony, no "
                "analysis under the rehabilitation criteria in title 16, "
                "section 1813. That is the trade a stipulation makes. The "
                "respondent admitted the allegations and accepted conditions "
                "rather than putting on a rehabilitation case at hearing, and "
                "in exchange he got a registration without the risk of an "
                "outright denial. Whether that was the right trade depends on "
                "evidence that is not in the file, which is exactly why the "
                "decision is silent about it.",
            "The conditions are the substance of what he agreed to. Three "
                "years of probation; a psychological or psychiatric evaluation "
                "within 90 days at his own cost, with a duty to follow the "
                "evaluator&rsquo;s recommendations and to stop practicing if "
                "the evaluator says he cannot practice safely; weekly "
                "psychotherapy with a Board-approved therapist who files "
                "quarterly reports on his fitness to practice; quarterly "
                "self-reports under penalty of perjury; written notice of any "
                "change of employer or residence within 30 days; a copy of the "
                "decision to every current and future employer before starting "
                "work; notice to any client whose therapy or confidentiality is "
                "affected, signed by the client; no supervising anyone toward "
                "licensure; and $1,200 a year for monitoring. The order also "
                "says probation continues on the same terms if he later becomes "
                "licensed, so a three-year term that starts as an associate "
                "follows him into LCSW licensure.",
            "No investigation-and-enforcement cost recovery was ordered in "
                "this decision; the monitoring fee is a probation condition "
                "rather than a penalty. That is a small point with a large "
                "practical edge: the recurring cost of a probationary "
                "registration is predictable and it is his to carry for the "
                "full term, on top of paying for the evaluation and for weekly "
                "therapy.",
        ],
        "ask": [
            "Section 480(a)(1)(A) leaves a serious felony available to a "
                "board indefinitely while an ordinary felony ages out in seven "
                "years. What is the policy justification for that line, and "
                "does Penal Code section 1192.7(c)(23) &mdash; any felony "
                "involving personal use of a dangerous or deadly weapon &mdash; "
                "actually track it?",
            "This case settled, so the record contains no findings about "
                "what the respondent did in the years after the conviction. "
                "What does an applicant give up by stipulating, what does the "
                "public lose, and under what conditions is that trade "
                "defensible?",
            "The probation follows the respondent into full licensure and "
                "requires him to notify clients whose therapy is affected by "
                "its terms. Draft what you think that notification should say, "
                "and defend the line you drew between the client&rsquo;s right "
                "to know and the associate&rsquo;s privacy.",
        ],
    },
}
