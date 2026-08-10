#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Eighteen more California BBS discipline cases, from a second collection.

WHERE THESE CAME FROM

`case_data.py` was built from one hundred and three decisions retrieved from
the Board's newsletters. This module is built from a second collection of one
hundred and five, downloaded separately, of which nineteen were not already in
the library and are not a DUI. The nineteenth is not here: it turned out to be
the same afternoon already written up as `discipline-case-drinking-at-lunch`,
and the richer account replaced the thin one in place rather than shipping
twice under two slugs.

WHY THE FILE IS GENERATED AND NOT HAND-WRITTEN

Because the redaction had to happen before the writing, not after it.

Every decision names the licensee in six predictable places - the caption, the
running footer, "Respondent Firstname Lastname (Respondent)", the criminal case
title, the home address, and the license number, which is a lookup key on the
Board's own site. Rather than trust an author to leave all six out, the text was
redacted at the door: `bbs/redact.py` finds the caption name, replaces every
form of it, strips addresses, license numbers, e-mail addresses, phone numbers,
and the names of the deputies attorney general and administrative law judges,
and then **verifies that the name it found does not survive anywhere in its own
output**. Only the redacted text was ever read. A hundred and five of a hundred
and five passed that check.

The write-ups were then checked again after authoring, against the original
unredacted documents, for any surviving form of any licensee's name and for any
license or registration number. Both scans came back empty.

WHAT IS NEW IN THIS SET, BEYOND VOLUME

  - **A ninth group: `applying`.** Five of these are a Statement of Issues
    rather than an Accusation - an applicant with a record, not a licensee who
    did something. Readers conflate the two constantly, and the outcomes are
    genuinely different: three of the five ended in a registration being
    ISSUED, on probation, including one for an applicant with a 1985 murder
    conviction. That case is the clearest published answer to "is the door open
    at all", and it was sitting unwritten in the corpus.
  - **The largest cost recovery in the library moves to $33,704**, from
    $15,883.
  - **Four defaults.** Four of these ended with the Board deciding on its own
    evidence packet because no notice of defense was filed within fifteen days.
    In every one of them the rehabilitation machinery the regulations require -
    a nine-factor analysis under 16 CCR &sect;1814 - never ran, because nobody
    was there to trigger it.

Ordering follows `case_data.py`: grouped, and within a group by how much of the
teaching is in the case rather than by date.

DO NOT EDIT BY HAND without also editing `case_depth.py`, which is keyed by the
same slugs, and `build_cases.py`, which asserts that every case has a discussion
block.
"""

MORE = [
    {
        # source: BBS decision 001.txt, redacted before it was read
        "slug": "discipline-case-billed-for-sessions-that-never-happened",
        "group": "money",
        "t": "Twenty-two sessions billed for a patient seen twice",
        "dek": "One payor&rsquo;s audit found <b>$35,329</b> in overcharges across "
            "559 claims; she repaid it, then shredded the files.",
        "role": "LMFT",
        "eff": "May 18, 2023",
        "case": "2002019002464",
        "hear": "OAH No. 2022080424",
        "facts": [
            "The respondent had held a marriage and family therapist "
                "license since 1975. Between 2016 and 2019 she billed insurers "
                "and a third-party claims administrator for sessions she had "
                "not provided. One patient saw her twice in January 2019; she "
                "billed for <b>22 sessions</b> spread over eight weeks. Another "
                "patient saw her three times in August 2016; she billed for 31. "
                "A third saw her twice; she billed for 21. A fourth was seen "
                "once, in February 2017; she billed for 36, and submitted "
                "progress notes to the payor for sessions that had not taken "
                "place. For a fifth patient the payor found she had billed 33 "
                "sessions and overbilled for 32 of them.",
            "A managed-care company audited her billing and determined she "
                "had overcharged it <b>$35,329</b> across 559 claims found to "
                "be in error. She reimbursed the company in full. In August "
                "2020, when a Department of Insurance investigator subpoenaed "
                "her records for four of those patients, she said the records "
                "had been shredded after she made the repayment. One patient "
                "was shown her own signed client-information sheet and noted "
                "that the date had been altered and that the handwriting was "
                "not hers; the same patient received a $350 bill from her "
                "health plan for sessions she had never attended and had to "
                "file an appeal to contest it.",
            "The advertising cause concerned a weekend retreat program the "
                "respondent ran. Her advertisement said a participant would be "
                "more &ldquo;emotionally healed and cleansed&rdquo; and that "
                "&ldquo;past participants and professional therapists have "
                "stated this weekend is equivalent to one or more years of "
                "individual and/or group therapy.&rdquo; She used one new "
                "patient&rsquo;s session to give a lengthy pitch for the "
                "program, telling him that any other counseling would be a "
                "waste of time, that his insurance was great, and that he had "
                "nothing to lose. Another patient attended after being told the "
                "<b>$1,500</b> cost would be covered by insurance. The retreat "
                "did not help her, and when she contacted her plan to find a "
                "different therapist she was told her therapy allowance was "
                "gone.",
            "In 2022 a married couple saw the respondent for a joint "
                "session. She obtained no information from them before "
                "starting, told them to stop talking, and said that their "
                "sharing their experiences was making &ldquo;her brain "
                "hurt.&rdquo; At an individual session five weeks later she "
                "again told the wife to stop talking and advised her to end her "
                "marriage. She then charged the couple for four dates on which "
                "she did not see them. In aggravation the Board pleaded a 1999 "
                "citation and $500 administrative penalty against her, then "
                "final, for submitting fraudulent billings to an employee "
                "assistance program and for disclosing a spouse&rsquo;s "
                "diagnosis and treatment plan without a signed authorization.",
        ],
        "charges": [
            [
                "B&amp;P &sect;4982(d)",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=4982&amp;lawCode=BPC",
                "Gross negligence or incompetence in the performance of "
                    "marriage and family therapy. Charged twice here on the "
                    "same billing conduct &mdash; once as gross negligence, "
                    "once as incompetence.",
            ],
            [
                "B&amp;P &sect;4982(i)",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=4982&amp;lawCode=BPC",
                "Intentionally or recklessly causing physical or emotional "
                    "harm to a client.",
            ],
            [
                "B&amp;P &sect;4982(j)",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=4982&amp;lawCode=BPC",
                "Any dishonest, corrupt, or fraudulent act substantially "
                    "related to the qualifications, functions, or duties of a "
                    "licensee.",
            ],
            [
                "B&amp;P &sect;4982(p)",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=4982&amp;lawCode=BPC",
                "Advertising in a manner that is false, fraudulent, "
                    "misleading, or deceptive, as defined in section 651.",
            ],
            [
                "B&amp;P &sect;651",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=651&amp;lawCode=BPC",
                "Makes it unlawful to disseminate any public communication "
                    "containing a false or misleading claim likely to induce "
                    "someone to buy professional services, including claims of "
                    "superior results that cannot be substantiated by objective "
                    "evidence.",
            ],
            [
                "B&amp;P &sect;4980.49(a)",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=4980.49&amp;lawCode=BPC",
                "Requires an MFT to retain a client&rsquo;s health service "
                    "records for at least seven years from termination of "
                    "therapy, or seven years past the client&rsquo;s eighteenth "
                    "birthday if the client is a minor.",
            ],
            [
                "B&amp;P &sect;4982(v)",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=4982&amp;lawCode=BPC",
                "Failure to keep records consistent with sound clinical "
                    "judgment, the standards of the profession, and the nature "
                    "of the services rendered.",
            ],
            [
                "B&amp;P &sect;4982(e)",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=4982&amp;lawCode=BPC",
                "Violating, attempting to violate, or conspiring to violate "
                    "any provision of the MFT chapter or any regulation adopted "
                    "by the Board.",
            ],
        ],
        "outcome": "License surrendered by stipulation after she had filed a notice of "
            "defense contesting an amended accusation. She may not petition for "
            "reinstatement, and may reapply only after three years as a new "
            "applicant &mdash; current education, current experience, and every "
            "examination required of new applicants &mdash; with all charges "
            "deemed admitted against any future application.",
        "cost": "$32,956",
        "rule": "A claim has to describe a service that actually happened, on the "
            "date it happened, to the person named on it. The progress note is "
            "the proof, which is why writing notes for sessions that did not "
            "occur is a separate wrong from billing for them. Records must be "
            "kept for at least seven years from the end of therapy &mdash; "
            "seven years past the eighteenth birthday for a minor &mdash; and "
            "repaying a payor does not shorten that clock or release the file "
            "for destruction; if anything, an audit is the moment the file "
            "becomes evidence. And anything you publish that is meant to induce "
            "someone to buy your services, a retreat brochure included, is a "
            "public communication under &sect;651: an outcome claim you cannot "
            "substantiate is disciplinable whether or not a client complains "
            "about it.",
        "ins": "None of this was insurable. Every professional liability policy "
            "excludes intentional acts, criminal acts, and fraud, so the "
            "overbilling, the restitution, and the destroyed records all sat "
            "outside coverage, and cost recovery under &sect;125.3 is not a "
            "defense cost &mdash; no sublimit pays it. What a policy does "
            "usually pay for is the defense of the licensing-board action "
            "itself: the attorney who answers the accusation, the hours spent "
            "responding to a subpoena, the negotiation of a stipulation. That "
            "benefit is capped, it is generally the smallest number on the "
            "declarations page, and it usually requires that you report the "
            "matter as soon as you learn of it &mdash; which in a case like "
            "this means the day the payor opens an audit, not the day the "
            "accusation arrives.",
        "prevent": [
            "Reconcile every claim against your appointment calendar and "
                "your notes before it is submitted, and keep the reconciliation "
                "as its own record.",
            "Never destroy a client record because a payor dispute closed "
                "&mdash; the seven-year clock runs from termination of therapy, "
                "not from settlement.",
            "Cut outcome comparisons from any workshop, retreat, or "
                "intensive marketing unless you can produce the evidence behind "
                "them on request.",
        ],
    },
    {
        # source: BBS decision 002.txt, redacted before it was read
        "slug": "discipline-case-a-decade-of-employer-warnings",
        "group": "sexual",
        "t": "Four employers acted on him before the Board ever did",
        "dek": "A 2010 suspension, a 2017 forced resignation, a 2020 termination "
            "and a 2021 improvement plan &mdash; all internal, none reported.",
        "role": "AMFT",
        "eff": "March 9, 2023",
        "case": "2002020001461",
        "hear": None,
        "facts": [
            "The respondent was registered as an associate marriage and "
                "family therapist in July 2015; his registration was canceled "
                "in July 2021 and was not eligible for renewal. The accusation "
                "gathered eleven years of conduct across four employers. At a "
                "counseling and education institute where he worked from 2010 "
                "to 2017, a complaint arrived in October 2010 that he had "
                "hugged a client in a way that made her uncomfortable and had "
                "offered to take her shopping and buy clothes for her children. "
                "He was suspended from providing therapy, required to enter his "
                "own therapy, to complete a law and ethics course, and to write "
                "a paper on his behavior. He was told that his &ldquo;personal "
                "need to comfort affected [his] ability to implement clear "
                "limits and boundaries that ensure client safety.&rdquo; He was "
                "reinstated in 2012 at his own request.",
            "In May 2017 a client of that same institute reported that "
                "during an in-home counseling session he asked her how often "
                "she felt aroused and how often she used a sex toy, called her "
                "&ldquo;guapa,&rdquo; and asked her to walk him to the door, "
                "where he hugged her. He was placed on probationary status with "
                "no client contact and reduced to part time; he resigned that "
                "June and his employment was recorded as terminated for "
                "&ldquo;high-risk behavior and poor judgment.&rdquo; At a youth "
                "counseling agency between 2017 and 2019 he was terminated over "
                "incorrect documentation and inappropriate billing; after he "
                "left, female staff complained he had made comments about their "
                "buttocks.",
            "From 2019 to 2020 he worked at a counseling agency serving "
                "domestic violence victims. In August 2019 a client complained "
                "that he asked inappropriate questions and texted her after a "
                "session to ask how many times she and her husband were "
                "intimate; she asked for a female therapist. In October 2019 a "
                "client seeking help with trauma from years of domestic "
                "violence attended a session while her young son waited outside "
                "for his own appointment. He locked the door, asked about her "
                "sex life, massaged her shoulders, asked her to close her eyes "
                "and do a breathing exercise, then rubbed and groped her "
                "breasts, squeezing them twice, and said, &ldquo;you "
                "aren&rsquo;t going to report me, right?&rdquo; She developed "
                "severe head pressure and stress requiring a doctor&rsquo;s "
                "care, and said she was afraid of his power to report her as a "
                "bad mother and of losing custody of her son. A third client "
                "complained in January 2020 that he had &ldquo;bombarded&rdquo; "
                "her with questions about her past and current sex life. He was "
                "terminated that May.",
            "At a substance abuse treatment center in 2021 he treated a "
                "client with a history of family abuse and of sexual abuse at a "
                "residential treatment center. She reported that he became "
                "increasingly physical over time, including hugging her behind "
                "the door. On June 4, 2021 he dimmed the lights, asked her to "
                "remove her mask by telling her she should not hide her "
                "beautiful face, removed his own, kissed her on the mouth, "
                "rubbed his body against hers, and told her to stand against "
                "the door in case someone tried to enter. She reported it and "
                "asked for a female therapist. The employer put him on a "
                "performance improvement plan about patient and clinician "
                "boundaries, required trainings in ethical decision-making, and "
                "moved him to a different site.",
            "The Board also charged him with dishonesty for what he said "
                "during the investigation: he gave a Division of Investigation "
                "investigator a false account of the terms of his termination, "
                "denied prior employer probation and reprimands, and blamed his "
                "clients for raising sexual topics and making him "
                "uncomfortable.",
        ],
        "charges": [
            [
                "B&amp;P &sect;726(a)",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=726&amp;lawCode=BPC",
                "Any act of sexual abuse, misconduct, or relations with a "
                    "patient or client is unprofessional conduct and grounds "
                    "for discipline for anyone licensed under the healing arts "
                    "division.",
            ],
            [
                "B&amp;P &sect;4982(k)",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=4982&amp;lawCode=BPC",
                "Sexual relations with a client or with a former client "
                    "within two years of termination, soliciting sexual "
                    "relations, or committing an act of sexual abuse or sexual "
                    "misconduct with a client. Intercourse is not required.",
            ],
            [
                "B&amp;P &sect;4982(d)",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=4982&amp;lawCode=BPC",
                "Gross negligence or incompetence &mdash; pleaded here as "
                    "the abuse of power itself: dissuading clients from "
                    "reporting, prioritizing his needs over theirs, and "
                    "entering a dual relationship.",
            ],
            [
                "B&amp;P &sect;4982(i)",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=4982&amp;lawCode=BPC",
                "Intentionally or recklessly causing physical or emotional "
                    "harm to a client.",
            ],
            [
                "B&amp;P &sect;4982(j)",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=4982&amp;lawCode=BPC",
                "A dishonest, corrupt, or fraudulent act &mdash; charged "
                    "for his statements to the Board&rsquo;s investigator, not "
                    "for the underlying conduct.",
            ],
            [
                "B&amp;P &sect;729",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=729&amp;lawCode=BPC",
                "Defines sexual exploitation by a psychotherapist, and "
                    "defines &ldquo;sexual contact&rdquo; as intercourse or the "
                    "touching of an intimate part for sexual arousal, "
                    "gratification, or abuse.",
            ],
        ],
        "outcome": "Registration surrendered by stipulation; he represented himself "
            "throughout. He may not petition for reinstatement and may reapply "
            "only after three years as a new applicant, with every charge "
            "deemed admitted against any future application to this Board or to "
            "the Board of Psychology.",
        "cost": "$33,704",
        "rule": "Sections 726 and 4982(k) reach a great deal short of intercourse. "
            "Soliciting sexual relations, sexual abuse, and sexual misconduct "
            "all count, and the conduct that builds toward them is the ordinary "
            "subject matter of these cases: hugging, massaging shoulders, "
            "locking a door, dimming lights, sexual-history questions with no "
            "treatment purpose, personal texts after hours. The second rule "
            "here is jurisdictional. An employer&rsquo;s response &mdash; a "
            "suspension, a required ethics course, a performance improvement "
            "plan, a transfer to another site, even a termination &mdash; "
            "resolves an employment problem and nothing more. It does not "
            "discharge the Board&rsquo;s interest, it does not restart "
            "anyone&rsquo;s clock, and under &sect;4990.33 it does not matter "
            "that the registration has since lapsed or been canceled.",
        "ins": "Sexual misconduct is the one allegation every California "
            "professional liability program treats differently: it is "
            "defense-only, capped, and never indemnified, because intentional "
            "and criminal acts are excluded from all of them. So the money "
            "question in a case like this is not what a policy would pay a "
            "client &mdash; it would pay nothing &mdash; but whether the "
            "board-defense benefit is available at all, and how early. The "
            "dishonesty count is the practical argument for calling your "
            "carrier before you speak to an investigator: statements made in an "
            "interview became an independent cause for discipline here, and "
            "that is exactly the point at which represented and unrepresented "
            "respondents diverge.",
        "prevent": [
            "Treat a client&rsquo;s request to switch to a therapist of a "
                "different gender as a clinical event: document it, escalate "
                "it, and find out what prompted it.",
            "Write your contact rules into the intake &mdash; who "
                "initiates, through what channel, about what &mdash; and put "
                "every text into the record.",
            "If an employer offers you a boundary-related improvement plan "
                "instead of a report, get independent advice on whether the "
                "underlying facts are separately reportable before you sign it.",
        ],
    },
    {
        # source: BBS decision 004.txt, redacted before it was read
        "slug": "discipline-case-underground-psychedelics-and-two-clients",
        "group": "sexual",
        "t": "He dosed two clients with MDMA and psilocybin, then slept with one",
        "dek": "Both relationships began before there was a therapy relationship "
            "&mdash; one in a classroom where he was the teaching assistant.",
        "role": "LMFT",
        "eff": "March 9, 2023",
        "case": "2002021002361",
        "hear": "OAH No. 2022070626",
        "facts": [
            "The respondent was licensed as an MFT in November 2019; most "
                "of the conduct occurred earlier, while he was a registered "
                "associate performing supervised therapy. He met the first "
                "client in the fall of 2017, when he was a teaching assistant "
                "in a graduate class she was taking. She disclosed in class "
                "that she had been raped. He told her he was an expert in "
                "treating victims of sexual abuse and encouraged her to begin "
                "seeing him for therapy.",
            "He introduced her to what the accusation calls underground "
                "psychedelic therapy, and in the summer of 2018 they attended "
                "an ayahuasca retreat together with other students. That July "
                "he flew to visit her and stayed two nights at her house; she "
                "paid for his plane ticket and his lunch, and during the visit "
                "he administered <b>MDMA</b> to her. He administered psilocybin "
                "to her that September. Weekly therapy sessions ran from about "
                "October 2018 to April 2019. At a session at his home office in "
                "January 2019 he gave her psilocybin again, and while she was "
                "under its influence he lay in bed with her, laid her head on "
                "his lap, hugged her, stroked her side and stomach, and kissed "
                "her cheek. He told her that his clients try to have sex with "
                "him and asked her to &ldquo;give into the erotic "
                "transference.&rdquo; The session ran from morning until "
                "evening; afterward he drove her home. When she tried to end "
                "therapy in April 2019, he screamed and yelled at her. She "
                "feared retaliation at school if she reported him.",
            "He met the second client in November 2016, while he was a "
                "trainee at a counseling center that served as a training site "
                "for his own graduate program; she was a graduate student there "
                "with a history of sexual assault, suicidality, and "
                "relationship concerns, and he held himself out as specializing "
                "in sexual issues. He treated her for three years. Over that "
                "period he administered MDMA to her on four occasions and "
                "psilocybin on four occasions, at times taking the same "
                "substances himself while doing so. He used touch during "
                "sessions &mdash; cradling her head in his lap, massaging her "
                "neck and shoulders, holding her hand, lying on the mattress "
                "with her and spooning her. Sessions sometimes ran from morning "
                "until evening; he regularly drove her home afterward and on "
                "one occasion shared dinner with her.",
            "In November 2019 he told her he had romantic feelings for her, "
                "began calling her regularly and meeting her outside scheduled "
                "sessions, and told her they &ldquo;had a spiritual connection "
                "and were meant to be together to teach each other "
                "something.&rdquo; While she was under the influence of "
                "controlled substances he told her that he loved her. When she "
                "asked whether he was crossing a boundary as her therapist, he "
                "told her their &ldquo;connection was bigger than the rules of "
                "the BBS.&rdquo; Her last session was in December 2019; they "
                "went to dinner afterward, had sex twice that month at his "
                "home, and traveled together at the end of the year to stay in "
                "his parents&rsquo; home in another state.",
            "When she asked for a break, he became psychologically and "
                "emotionally abusive, using material from therapy against her: "
                "he told her she was too traumatized by her past to accept his "
                "love, and that she had consented to their relationship in "
                "another lifetime. In January and February 2020 he called her "
                "on <b>50 separate occasions</b> and texted many more times. "
                "She asked him to stop in March 2020; he contacted her again in "
                "April and in May. She moved away to get away from him. Her new "
                "therapist recorded that he had tried to use his authority to "
                "recast her wish to end the relationship as a form of "
                "psychopathology, and that she was left with elevated anxiety "
                "and considerable trauma.",
        ],
        "charges": [
            [
                "B&amp;P &sect;4982(c)",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=4982&amp;lawCode=BPC",
                "Using or administering controlled substances or alcohol in "
                    "a way dangerous or injurious to oneself, a client, or the "
                    "public. The subdivision ends with a mandate: the Board "
                    "shall revoke the license of anyone who uses or offers to "
                    "use drugs in the course of performing MFT services.",
            ],
            [
                "B&amp;P &sect;726",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=726&amp;lawCode=BPC",
                "Any act of sexual abuse, misconduct, or relations with a "
                    "client is unprofessional conduct and grounds for "
                    "discipline.",
            ],
            [
                "B&amp;P &sect;4982(k)",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=4982&amp;lawCode=BPC",
                "Sexual relations with a client, or with a former client "
                    "within two years of termination; soliciting sexual "
                    "relations; sexual abuse or sexual misconduct with a "
                    "client.",
            ],
            [
                "B&amp;P &sect;4982.26",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=4982.26&amp;lawCode=BPC",
                "On any finding of fact that a licensee engaged in sexual "
                    "contact with a patient, the Board shall revoke &mdash; and "
                    "the revocation may not be stayed by the administrative law "
                    "judge or by the Board.",
            ],
            [
                "B&amp;P &sect;4982(d)",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=4982&amp;lawCode=BPC",
                "Gross negligence in the performance of marriage and family "
                    "therapy.",
            ],
            [
                "B&amp;P &sect;4982(i)",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=4982&amp;lawCode=BPC",
                "Intentionally or recklessly causing physical or emotional "
                    "harm to a client.",
            ],
            [
                "B&amp;P &sect;729",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=729&amp;lawCode=BPC",
                "Makes sexual contact between a psychotherapist and a "
                    "patient a public offense, and supplies the definition of "
                    "&ldquo;sexual contact&rdquo; used by the "
                    "mandatory-revocation provision.",
            ],
        ],
        "outcome": "License surrendered by stipulation after he had filed a notice of "
            "defense contesting the accusation. He may not petition for "
            "reinstatement and may reapply only after three years as a new "
            "applicant, with every charge deemed admitted against any future "
            "application.",
        "cost": "$14,486",
        "rule": "Two independent rules run through this case. First, administering "
            "a controlled substance to a client is disciplinable on its own "
            "under &sect;4982(c), and the subdivision does not stop at "
            "discretion: the Board shall revoke the license of anyone who uses "
            "or offers to use drugs in the course of performing therapy. The "
            "client&rsquo;s consent, her enthusiasm, and the therapist&rsquo;s "
            "belief in the benefit are not defenses, and no sexual finding is "
            "needed. Second, &sect;4982.26 makes revocation mandatory and "
            "unstayable on any finding of sexual contact with a patient &mdash; "
            "neither the administrative law judge nor the Board has discretion "
            "to soften it. Underneath both sits the ordinary rule this case "
            "keeps illustrating: a therapy relationship that grows out of a "
            "teaching, training, or supervisory role carries that earlier "
            "authority into the room, and the client cannot leave it at the "
            "door.",
        "ins": "Nothing in this case is insurable. Administering a Schedule I "
            "controlled substance is a criminal act, and criminal and "
            "intentional acts are excluded from every professional liability "
            "policy sold to California therapists; sexual misconduct is "
            "defense-only on all of them, never indemnified. That leaves the "
            "licensing-board defense benefit, which would have paid some of the "
            "cost of answering the accusation and negotiating a stipulation "
            "&mdash; but not the <b>$14,486</b> in cost recovery, because cost "
            "recovery is not a defense cost and no sublimit reaches it. A "
            "therapist considering any form of psychedelic-assisted work should "
            "ask the carrier, in writing and before starting, whether the "
            "policy responds at all; the usual answer is that it does not.",
        "prevent": [
            "Do not take on as a client anyone you already hold authority "
                "over as a teacher, teaching assistant, supervisor, or group "
                "leader; refer out, and document the referral and the reason.",
            "Keep sessions to a scheduled length and end them in the office "
                "&mdash; all-day sessions, rides home, and shared meals are the "
                "observable markers a Board looks for when reconstructing a "
                "boundary case.",
            "If a client asks whether something you are doing crosses a "
                "line, treat the question as the answer and take it to "
                "consultation that week.",
        ],
    },
    {
        # source: BBS decision 005.txt, redacted before it was read
        "slug": "discipline-case-a-felony-assault-and-a-default",
        "group": "conviction",
        "t": "A felony assault conviction, and no answer to the Board",
        "dek": "He filed no notice of defense within 15 days; the Board decided "
            "the case on the papers and revoked.",
        "role": "APCC",
        "eff": "May 18, 2023",
        "case": "2002019002856",
        "hear": None,
        "facts": [
            "The respondent was registered as an associate professional "
                "clinical counselor in May 2018. The registration expired in "
                "May 2019 and was never renewed, which under &sect;4990.33 did "
                "not remove him from the Board&rsquo;s jurisdiction.",
            "In August 2022, in San Diego County Superior Court, he was "
                "convicted on his own guilty plea of violating Penal Code "
                "&sect;245(a)(4), assault by means likely to produce great "
                "bodily injury, a felony. He was placed on two years of formal "
                "probation and committed to the custody of the sheriff for "
                "2,060 days with credit for 2,060 days served. Among the other "
                "terms, he was ordered to complete a sex offender counseling "
                "program, to pay court fees and restitution, and to stay away "
                "from two women identified in the case as Jane Doe 1 and Jane "
                "Doe 2.",
            "The conduct behind the plea occurred in April 2019. A woman "
                "reported that he solicited her for sex, that she got into his "
                "car, and that he drove to an isolated industrial area. He told "
                "her to get out of the car, then lifted her dress and groped "
                "her breasts over her bra. She insisted that he pay before sex; "
                "he refused and continued. When she became frightened and tried "
                "to push him away, he grabbed her by the neck and squeezed her "
                "larynx and trachea until she could not breathe, and a violent "
                "struggle followed before she fought him off and ran. A human "
                "trafficking task force investigated and located a second "
                "victim who had been assaulted in a similar way. He was "
                "arrested the following month.",
            "The Board filed its accusation in January 2023 and served it "
                "the next day by certified and first class mail at his address "
                "of record &mdash; the address B&amp;P &sect;136 requires every "
                "registrant to report and maintain. He filed no notice of "
                "defense within 15 days, which under Government Code "
                "&sect;11506(c) waived his right to a hearing. Under Government "
                "Code &sect;11520 the Board took the matter by default, decided "
                "it on a default decision investigatory evidence packet, and "
                "found the charges true by clear and convincing evidence.",
        ],
        "charges": [
            [
                "B&amp;P &sect;490",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=490&amp;lawCode=BPC",
                "A board may suspend or revoke a license on the ground that "
                    "the licensee was convicted of a crime substantially "
                    "related to the qualifications, functions, or duties of the "
                    "profession.",
            ],
            [
                "B&amp;P &sect;4999.90(a)",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=4999.90&amp;lawCode=BPC",
                "Unprofessional conduct for a professional clinical "
                    "counselor or associate includes conviction of a "
                    "substantially related crime; the record of conviction is "
                    "conclusive proof only that the conviction occurred, and "
                    "the Board may look behind it at the circumstances.",
            ],
            [
                "Penal Code &sect;245(a)(4)",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=245&amp;lawCode=PEN",
                "Assault upon another by any means of force likely to "
                    "produce great bodily injury. The offense of conviction "
                    "here, taken by guilty plea as a felony.",
            ],
            [
                "16 CCR &sect;1812",
                None,
                "Defines &ldquo;substantially related&rdquo; for BBS "
                    "licensees: a crime qualifies if to a substantial degree it "
                    "evidences present or potential unfitness to perform the "
                    "licensed functions consistently with public health, "
                    "safety, or welfare, weighing the nature and gravity of the "
                    "offense and the years elapsed.",
            ],
            [
                "16 CCR &sect;1814",
                None,
                "Sets the rehabilitation criteria the Board applies when "
                    "considering revocation for a conviction, including "
                    "completion of the criminal sentence without violation and "
                    "compliance with the terms of probation.",
            ],
            [
                "B&amp;P &sect;482",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=482&amp;lawCode=BPC",
                "Requires each board to develop criteria for evaluating "
                    "rehabilitation, and to consider a showing of "
                    "rehabilitation where the criminal sentence was completed "
                    "without a parole or probation violation.",
            ],
        ],
        "outcome": "Registration revoked by default decision. The Board separately "
            "found its actual costs of enforcement to be $4,551.25 as of March "
            "15, 2023; the order itself contains no payment term. He had seven "
            "days from service of the decision to move to have it vacated for "
            "good cause.",
        "cost": "$4,551.25",
        "rule": "A conviction supports discipline when it is substantially related "
            "to the qualifications, functions, or duties of the license &mdash; "
            "16 CCR &sect;1812 defines that as conduct evidencing, to a "
            "substantial degree, present or potential unfitness to practice "
            "consistently with public health, safety, or welfare &mdash; and "
            "the record of conviction is conclusive that it happened. The other "
            "half of this case is pure procedure, and it is the half that "
            "decides outcomes. Business and Professions Code &sect;136 requires "
            "you to report and maintain a current address of record; service "
            "there is effective as a matter of law whether or not you still "
            "live there. A notice of defense is due within 15 days of service. "
            "Missing it waives the hearing and lets the Board decide on "
            "affidavits and an investigative packet alone.",
        "ins": "A criminal defense is paid out of pocket &mdash; every "
            "professional liability policy excludes criminal and intentional "
            "acts, with no exception for a plea to a lesser count. The "
            "board-defense benefit is the only part of a policy that could have "
            "mattered here, and its reach is worth checking before you need it, "
            "because many programs tie it to allegations arising out of "
            "professional services and this conduct arose outside practice "
            "entirely. Even where the benefit applies, cost recovery under "
            "&sect;125.3 is not a defense cost and no sublimit pays it. And a "
            "default costs nothing to enter and everything to lose: there is no "
            "coverage question at all if no one files an answer.",
        "prevent": [
            "Keep your address of record current with the Board and keep "
                "reading that mailbox even after you stop practicing &mdash; "
                "service there is legally effective, and the Board&rsquo;s "
                "jurisdiction survives an expired registration.",
            "File a notice of defense within 15 days of any accusation, "
                "even if you intend to give the license up; it preserves a "
                "hearing you can still settle later.",
            "If you are convicted of anything, gather the court records and "
                "produce them &mdash; 16 CCR &sect;1814 makes compliance with "
                "the sentence and evidence of rehabilitation the criteria the "
                "Board actually applies.",
        ],
    },
    {
        # source: BBS decision 008.txt, redacted before it was read
        "slug": "discipline-case-letting-a-registration-lapse-on-probation",
        "group": "probation",
        "t": "Her registration lapsed while she was on probation for it",
        "dek": "No new clinical misconduct &mdash; one administrative condition "
            "breached turned three years of probation into forty-two months.",
        "role": "AMFT",
        "eff": None,
        "case": "2002023000887",
        "hear": None,
        "facts": [
            "The respondent was registered as an associate marriage and "
                "family therapist in August 2017. In a prior disciplinary case, "
                "decided effective December 8, 2021, the Board revoked her "
                "registration, stayed the revocation, and placed her on three "
                "years&rsquo; probation. That earlier case rested on a criminal "
                "conviction and on her failure to answer the Board.",
            "The conviction was for forgery. In October 2020, in Merced "
                "County Superior Court, she was convicted on her plea of "
                "violating Penal Code sections 470(d) and 473(a), forgery "
                "relating to an item exceeding $950, a felony; she was "
                "sentenced to 180 days in jail, three years of formal "
                "probation, and fees, fines, and restitution. Between November "
                "2018 and January 2019 she had deposited five forged checks "
                "totaling <b>$19,000</b> into her own bank account. The victim "
                "was the father of a man she had previously been in a "
                "relationship with. She had come to his home in September 2018 "
                "asking for help with her car, and while he was outside she "
                "asked to use the bathroom and was alone inside for a few "
                "minutes. He noticed months later that his account was low, and "
                "his bank traced five checks to her; surveillance video from "
                "the ATM confirmed she had deposited them. The Board separately "
                "charged her under 16 CCR &sect;1845(h) for failing to give it "
                "documentation about her arrest after a February 2020 request. "
                "That case carried $1,855 in cost recovery and $1,200 a year in "
                "probation monitoring costs.",
            "The violation charged in this case is administrative and "
                "singular. Probation Condition 14 required her to maintain a "
                "current and active registration with the Board at all times "
                "while on probation, including any period during which "
                "probation was tolled. Her registration had expired on August "
                "31, 2019 &mdash; more than two years before the probation "
                "began &mdash; and was never renewed. She was notified in "
                "October 2022 that she was out of compliance and that further "
                "disciplinary action would follow, which under Condition 13 "
                "automatically extended her probation. The petition to revoke "
                "probation was filed in December 2022; she filed a notice of "
                "defense contesting it, then admitted every allegation in a "
                "stipulated settlement. She represented herself in both "
                "proceedings.",
            "The Board did not revoke. It ordered the registration revoked, "
                "stayed the revocation again, and placed her on <b>42 "
                "months&rsquo;</b> probation on a fresh and longer set of "
                "conditions: a psychological or psychiatric evaluation by a "
                "Board-appointed evaluator within 90 days, at her expense, with "
                "compliance required with whatever the evaluator recommends; "
                "ongoing weekly psychotherapy with a Board-approved licensed "
                "clinician who files quarterly reports on her fitness to "
                "practice; a graduate-level law and ethics course equivalent to "
                "two semester units, completed within a year and not usable for "
                "continuing education credit; fingerprinting through the "
                "Department of Justice and the FBI, and written reporting of "
                "any violation of law within 72 hours; quarterly reports under "
                "penalty of perjury; in-person interviews on request; "
                "notification to every current and future employer and to any "
                "client whose therapy or confidentiality is affected; a bar on "
                "supervising anyone&rsquo;s hours toward licensure; a bar on "
                "teaching continuing education; and reimbursement of the "
                "Board&rsquo;s probation monitoring at $1,200 per year. If "
                "either the evaluator or the treating therapist concludes she "
                "cannot practice safely, she must stop immediately and may not "
                "resume until the Board says so.",
        ],
        "charges": [
            [
                "Probation Condition 14 &mdash; Maintain Valid Registration",
                None,
                "Requires a probationer to hold a current and active "
                    "registration at all times while on probation, including "
                    "any tolled period; on renewal the registration remains "
                    "subject to every term not already satisfied. The only "
                    "condition charged in this petition.",
            ],
            [
                "B&amp;P &sect;4982",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=4982&amp;lawCode=BPC",
                "The general disciplinary authority the Board invoked to "
                    "bring the petition and to reimpose discipline on the "
                    "underlying registration.",
            ],
            [
                "B&amp;P &sect;4990.33",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=4990.33&amp;lawCode=BPC",
                "Expiration, cancellation, forfeiture, or surrender of a "
                    "registration does not deprive the Board of jurisdiction to "
                    "investigate, to proceed, or to revoke &mdash; the "
                    "provision that makes a lapsed registration disciplinable "
                    "at all.",
            ],
            [
                "B&amp;P &sect;4982(a)",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=4982&amp;lawCode=BPC",
                "Conviction of a crime substantially related to the "
                    "qualifications, functions, or duties of a licensee or "
                    "registrant &mdash; the first cause in the underlying case.",
            ],
            [
                "B&amp;P &sect;4982(j)",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=4982&amp;lawCode=BPC",
                "Commission of a dishonest, corrupt, or fraudulent act "
                    "substantially related to the duties of a registrant "
                    "&mdash; the second cause in the underlying case.",
            ],
            [
                "B&amp;P &sect;490",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=490&amp;lawCode=BPC",
                "Authorizes suspension or revocation on the ground of a "
                    "substantially related conviction.",
            ],
            [
                "16 CCR &sect;1845(h)",
                None,
                "Makes it unprofessional conduct to fail to provide the "
                    "Board, within 30 days of a request, with documentation "
                    "regarding the arrest of a licensee or registrant. The "
                    "third cause in the underlying case.",
            ],
            [
                "Penal Code &sect;470(d)",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=470&amp;lawCode=PEN",
                "Forgery: passing, uttering, or attempting to pass a forged "
                    "check or other listed instrument with intent to defraud.",
            ],
            [
                "Penal Code &sect;473(a)",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=473&amp;lawCode=PEN",
                "The penalty provision for forgery, under which an "
                    "instrument exceeding $950 was charged as a felony here.",
            ],
        ],
        "outcome": "Registration revoked, revocation stayed, and probation reimposed "
            "for 42 months on expanded terms &mdash; longer than the three "
            "years she was already serving. The order contains no separate cost "
            "recovery term; probation monitoring is reimbursed at $1,200 a "
            "year, and the $1,855 in costs from the underlying case remained "
            "payable under that earlier decision.",
        "cost": None,
        "rule": "Every condition of a stayed-revocation probation is an "
            "independent, self-executing obligation, and the administrative "
            "ones are the easiest to breach precisely because they are not "
            "about clinical work. &ldquo;Maintain a current and active "
            "registration&rdquo; means renewing it on time, every time, "
            "including in periods when you are not practicing at all. The "
            "non-practice condition spells out what does not pause: obeying all "
            "laws, filing quarterly reports, complying with the probation "
            "program, maintaining a valid registration, and paying costs. A "
            "lapse does not put you outside the Board&rsquo;s reach &mdash; "
            "&sect;4990.33 keeps jurisdiction over an expired registration "
            "&mdash; and the filing of a petition to revoke automatically "
            "extends probation until the Board acts on it. You cannot wait out "
            "a probation by not working.",
        "ins": "Probation is the uninsured part of discipline. No policy pays for "
            "a Board-ordered psychological evaluation, for weekly psychotherapy "
            "you are required to attend, for a graduate law and ethics course "
            "that cannot count toward continuing education, for fingerprinting, "
            "or for the $1,200 a year in monitoring costs &mdash; and cost "
            "recovery is not a defense cost, so no sublimit reaches it either. "
            "The underlying conduct, forgery, is a criminal and intentional act "
            "excluded from every policy. What is genuinely worth asking your "
            "carrier in writing, before you need the answer, is whether the "
            "board-defense benefit extends to a petition to revoke probation at "
            "all: it is a second proceeding, arising after discipline is "
            "already on your record, and policies differ on whether that is a "
            "new covered claim or the continuation of an old one.",
        "prevent": [
            "Calendar every probation deadline &mdash; renewal, quarterly "
                "report, evaluation, coursework, payment &mdash; in the week "
                "the decision becomes effective, not in the month each falls "
                "due.",
            "Renew a registration or license on time even while suspended, "
                "between jobs, or not practicing; where probation requires "
                "currency, the lapse is itself the violation.",
            "Read the non-practice clause of your own order and highlight "
                "the conditions it does not toll; those are the ones that end "
                "probations early and badly.",
        ],
    },
    {
        # source: BBS decision 009.txt, redacted before it was read
        "slug": "discipline-case-a-battery-conviction-and-a-default",
        "group": "conviction",
        "t": "A battery conviction ends an associate&rsquo;s registration",
        "dek": "She never filed a notice of defense, so the Board decided the case "
            "without her.",
        "role": "ASW",
        "eff": "May 18, 2023",
        "case": "2002022002071",
        "hear": None,
        "facts": [
            "On February 18, 2022, at 4:34 p.m., police responded to a call "
                "about a domestic disturbance. The victim, the "
                "respondent&rsquo;s former romantic partner, said she assaulted "
                "him during an argument while he was moving out of their "
                "apartment. He said she struck him in the face and brandished a "
                "box cutter. The respondent admitted to officers only that she "
                "hit him. Officers searched the apartment and could not find "
                "the box cutters. They determined she was the primary aggressor "
                "and arrested her.",
            "On July 25, 2022, in the Superior Court of California, County "
                "of San Mateo, the respondent was convicted on her plea of "
                "guilty to violating Penal Code section 242, battery. She was "
                "sentenced to <b>18 months of formal probation</b> until "
                "November 26, 2022, followed by another 18 months of summary "
                "probation, and was ordered to complete 104 hours of domestic "
                "violence counseling, serve 10 days in jail with 4 days of "
                "credit, and pay fines and restitution.",
            "The Board had issued her Associate Clinical Social Worker "
                "registration on September 11, 2021, so the conviction came "
                "roughly ten months into her registration. The Board filed an "
                "accusation on January 19, 2023 and served it by certified and "
                "first class mail at her address of record, and again on "
                "January 30, 2023 at an alternate address.",
            "The respondent did not file a notice of defense within 15 days "
                "of service. Under Government Code section 11506, that waived "
                "her right to a hearing on the merits. The Board found her in "
                "default under Government Code section 11520, took official "
                "notice of its own records, and found the charges true by clear "
                "and convincing evidence on the investigatory evidence packet "
                "alone. Her registration was due to expire on September 30, "
                "2023; the Board noted that expiration would not have deprived "
                "it of jurisdiction.",
        ],
        "charges": [
            [
                "B&amp;P &sect;4992.3(a)",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=4992.3&lawCode=BPC",
                "Conviction of a crime substantially related to the "
                    "qualifications, functions, or duties of a licensee or "
                    "registrant is unprofessional conduct. A guilty plea counts "
                    "as a conviction, and later expungement under Penal Code "
                    "section 1203.4 does not undo it.",
            ],
            [
                "B&amp;P &sect;490(a)",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=490&lawCode=BPC",
                "Lets a board suspend or revoke a license on the ground "
                    "that the licensee was convicted of a substantially related "
                    "crime.",
            ],
            [
                "Penal Code &sect;242",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=242&lawCode=PEN",
                "Battery: any willful and unlawful use of force or violence "
                    "upon another person. A misdemeanor here, and the whole "
                    "substance of the disciplinary case.",
            ],
            [
                "16 CCR &sect;1812",
                None,
                "Defines &ldquo;substantially related&rdquo; for this "
                    "Board: a crime or act qualifies if to a substantial degree "
                    "it evidences present or potential unfitness to perform "
                    "licensed functions consistent with public health, safety, "
                    "or welfare.",
            ],
        ],
        "outcome": "Associate Clinical Social Worker registration revoked by default "
            "decision and order. The respondent had seven days after service of "
            "the decision to move to vacate it for good cause.",
        "cost": None,
        "rule": "A criminal conviction is a free-standing ground for discipline. "
            "The Board does not have to show that anything happened in a "
            "session, or that a client was involved at all; it has to show a "
            "conviction and that the crime is substantially related to the "
            "qualifications, functions, or duties of the profession. The record "
            "of conviction is conclusive evidence that the conviction occurred, "
            "and a guilty or no contest plea is a conviction for this purpose. "
            "What the Board can still weigh is the circumstances of the offense "
            "and the licensee&rsquo;s rehabilitation, using set criteria: the "
            "nature and severity of the act, how much time has passed, "
            "compliance with criminal probation, and any evidence of "
            "rehabilitation the licensee puts in front of it. That last part "
            "only happens if the licensee shows up.",
        "ins": "A professional liability policy will not defend or pay for a "
            "criminal case, and every such policy excludes intentional and "
            "criminal acts, so nothing about the battery itself is insurable. "
            "Conduct in a personal relationship also falls outside "
            "&ldquo;professional services&rdquo; entirely. What most policies "
            "do include is a license defense benefit, usually a fixed sublimit, "
            "that pays a lawyer to respond to a board accusation, and that is "
            "the coverage that matters here. It buys a timely notice of defense "
            "and someone to present rehabilitation evidence. It cannot help "
            "after a default is entered.",
        "prevent": [
            "If you are arrested, charged, or convicted of anything, report "
                "it to the Board in writing within 30 days and keep proof of "
                "what you sent and when.",
            "Keep your address of record current with the Board; service at "
                "that address is legally effective whether or not you actually "
                "read the mail.",
            "File a notice of defense within 15 days of being served with "
                "an accusation, even if you intend to settle. Missing that "
                "deadline forfeits the hearing, and with it every argument "
                "about rehabilitation.",
        ],
    },
    {
        # source: BBS decision 018.txt, redacted before it was read
        "slug": "discipline-case-falsified-course-certificates-end-a-probation",
        "group": "probation",
        "t": "Falsified course certificates end a stayed revocation",
        "dek": "Most of the violations were curable; typing her own certificates "
            "of completion was not.",
        "role": "LMFT",
        "eff": "June 13, 2024",
        "case": "2002023001526",
        "hear": "OAH No. 2023090380",
        "facts": [
            "The respondent was already on discipline. A stipulated "
                "settlement effective June 24, 2021 revoked her LMFT license, "
                "stayed the revocation, and placed her on three years of "
                "probation. The underlying accusation was about supervision: "
                "she had supervised an associate whose registration was "
                "delinquent, supervised by videoconference rather than face to "
                "face, supervised an associate who took payment directly from "
                "clients and worked as an independent contractor at a site that "
                "was not her place of business, failed to produce her "
                "supervisor training certificates when the Board asked, and "
                "failed to maintain a current address of record.",
            "The probation terms started coming due immediately, and she "
                "missed the first two. Her psychotherapy proposal was due July "
                "9, 2021 and was not filed; the Board issued a notice of "
                "non-compliance on August 16, 2021. Her supervision plan was "
                "due July 26, 2021, arrived incomplete on August 27, and was "
                "not approved until September 8. On December 10, 2021 she "
                "terminated her Board-approved therapist without telling the "
                "Board, which found out only when he filed his quarterly report "
                "on January 11, 2022. A replacement was approved February 11, "
                "2022. From those dates forward she stayed in compliance with "
                "both conditions, at a cost she testified was $800 a month.",
            "The education condition required the equivalency of two "
                "semester units in supervision, due December 26, 2022. On "
                "December 28, 2022 the Board issued a notice of non-compliance "
                "stating she had submitted only one certificate for six hours. "
                "She then sent her probation monitor certificates of completion "
                "showing <b>25 online contact hours</b> in five courses. The "
                "Board&rsquo;s adopted decision corrected the date of that "
                "submission to April 14, 2023. An audit produced the continuing "
                "education provider&rsquo;s own course list, which showed she "
                "had taken a different set of courses on December 29 and "
                "December 31, 2021, that the provider had not issued the "
                "certificates she submitted, and that she had never taken four "
                "of the five courses listed on them. At hearing she admitted "
                "typing the course names and hours onto the certificates "
                "herself.",
            "The money conditions went unpaid. She owed $1,200 a year for "
                "probation monitoring, first payment due June 24, 2022, and "
                "<b>$5,111.88</b> in cost recovery from the underlying case "
                "under a signed plan of $181.88 followed by 29 monthly payments "
                "of $170. On August 30, 2022 she made payments of one dollar "
                "and ten dollars toward each. Nothing after that. She testified "
                "her income at the time was about $20,000 a year, that her "
                "divorce finalized in March 2022, that her cars were "
                "repossessed, and that she was supporting two teenage children.",
            "The administrative law judge accepted the hardship as partial "
                "mitigation but not as an answer. The respondent had taken a "
                "better paying job in May 2023 and still completed no "
                "additional supervision coursework and made no payments before "
                "the February 2024 hearing. The judge also noted her testimony "
                "was evasive about not notifying the Board before terminating "
                "her therapist, and that she blamed her probation monitor both "
                "for &ldquo;making&rdquo; her sign the orientation notes and "
                "for the falsified certificates.",
        ],
        "charges": [
            [
                "Probation Condition 1 &mdash; Psychotherapy",
                None,
                "Weekly therapy with a Board-approved California licensed "
                    "mental health professional, proposed for approval within "
                    "15 days of the effective date, with quarterly reports from "
                    "the therapist to the Board.",
            ],
            [
                "Probation Condition 2 &mdash; Supervised Practice",
                None,
                "An independent Board-approved supervisor with no prior "
                    "relationship to her, one hour of individual face-to-face "
                    "supervision a week, proposed within 30 days, with "
                    "quarterly reports.",
            ],
            [
                "Probation Condition 3 &mdash; Education",
                None,
                "The equivalency of two semester units in supervision, "
                    "taken at graduate level or in a Board-approved course, "
                    "completed within 18 months of the effective date.",
            ],
            [
                "Probation Condition 7 &mdash; Comply with Probation "
                    "Program",
                None,
                "A catch-all: comply with the probation program and "
                    "cooperate with Board representatives monitoring and "
                    "investigating compliance. Breaching other conditions "
                    "breaches this one too.",
            ],
            [
                "Probation Condition 19 &mdash; Reimbursement of Probation "
                    "Program",
                None,
                "$1,200 a year to reimburse the Board for the cost of "
                    "monitoring the probation.",
            ],
            [
                "Probation Condition 20 &mdash; Cost Recovery",
                None,
                "$5,111.88 for the investigation and prosecution of the "
                    "underlying case, on a Board-approved payment plan. "
                    "Non-payment is expressly a probation violation, and "
                    "probation cannot terminate until it is paid.",
            ],
            [
                "Probation Condition 14 &mdash; Violation of Probation",
                None,
                "The enforcement lever: if the respondent violates any "
                    "condition, the Board may set aside the stay and impose the "
                    "revocation already ordered in the underlying decision.",
            ],
        ],
        "outcome": "The petition was granted. Probation was revoked, the stay was "
            "lifted, and the LMFT license was revoked.",
        "cost": None,
        "rule": "A stayed revocation is a revocation that has already been ordered "
            "and is being held back on conditions. Each condition stands on its "
            "own, and the standard conditions are not all clinical: therapy, "
            "supervision, coursework, quarterly reports under penalty of "
            "perjury, annual monitoring fees, and a cost recovery payment plan "
            "all carry equal weight, and non-payment is written into the order "
            "as a violation. Because the discipline was already imposed, a "
            "petition to revoke probation asks only whether the conditions were "
            "met. The board does not have to prove the original misconduct "
            "again, and it proves the breach by a preponderance of the evidence "
            "rather than by clear and convincing evidence.",
        "ins": "Nothing in this case is insurable. Probation monitoring fees, cost "
            "recovery, court-ordered coursework, and the therapy and "
            "supervision a probation requires are all payable by the licensee, "
            "and no professional liability policy reimburses them; submitting "
            "altered documents to a regulator is an intentional act excluded "
            "everywhere. The license defense benefit that a policy provides is "
            "spent on the original accusation, which is precisely when it is "
            "worth using. The practical insurance lesson is upstream: a "
            "well-defended accusation that settles on lighter terms produces a "
            "probation you can actually complete.",
        "prevent": [
            "On the day you sign your probation orientation notes, put "
                "every deadline in the same calendar you use for clients: "
                "proposal dates, coursework completion dates, quarterly report "
                "dates, and every payment date.",
            "Never stop seeing a Board-approved therapist or supervisor "
                "before the replacement is approved in writing. Notify the "
                "Board first, in writing, and keep the acknowledgement.",
            "If you cannot make a payment, write to the Board and ask to "
                "extend the payment plan before you miss it. The order allows "
                "the Enforcement Manager to extend a plan for good cause, and "
                "the order also allows a probationer who cannot satisfy the "
                "terms to request voluntary surrender rather than default into "
                "revocation.",
        ],
    },
    {
        # source: BBS decision 034.txt, redacted before it was read
        "slug": "discipline-case-psychology-probation-reaches-a-second-license",
        "group": "another",
        "t": "Psychology board probation reaches a second license",
        "dek": "The 30-day duty to report the first board&rsquo;s discipline "
            "became its own cause for discipline.",
        "role": "LEP",
        "eff": "July 24, 2025",
        "case": "2002024002213",
        "hear": "OAH No. 2024070097",
        "facts": [
            "The respondent had held a Licensed Educational Psychologist "
                "license from this Board since July 1, 2002. She also held a "
                "psychologist license from the Board of Psychology.",
            "On March 28, 2024 the Board of Psychology resolved a first "
                "amended accusation against her by stipulated settlement: her "
                "psychologist license was revoked, the revocation was stayed, "
                "and she was placed on four years of probation. The allegations "
                "behind it were that she committed gross negligence in treating "
                "two patients between 2018 and 2019; committed repeated "
                "negligent acts in treating those patients; committed a "
                "dishonest, corrupt, or fraudulent act in misrepresenting to a "
                "patient who her assistant was and what authority that "
                "individual had; committed unprofessional conduct by failing to "
                "timely produce records to the Board of Psychology; committed "
                "repeated negligent acts in treating an 11-year-old patient "
                "between 2019 and 2020; and committed unprofessional conduct by "
                "failing to promptly transmit that patient&rsquo;s independent "
                "educational evaluation report within 15 days after receiving "
                "written requests for it from the patient&rsquo;s father.",
            "A regulation requires a licensee of this Board to report any "
                "disciplinary action by another licensing entity within 30 "
                "days. As of April 28, 2024, she had not reported the "
                "psychology discipline to this Board. The Board filed its "
                "accusation on June 11, 2024, with two causes: the fact of the "
                "other board&rsquo;s discipline, and the failure to report it.",
            "She was served on June 13, 2024, timely filed a notice of "
                "defense contesting the accusation, and was represented by "
                "counsel. The matter settled. She agreed that at a hearing the "
                "complainant could establish a factual basis for the charges "
                "and gave up her right to contest them, without admitting them. "
                "The Board adopted the stipulation on June 24, 2025.",
        ],
        "charges": [
            [
                "B&amp;P &sect;4989.54(h)",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=4989.54&lawCode=BPC",
                "Denial, revocation, suspension, restriction, or any other "
                    "disciplinary action imposed by another state or by any "
                    "other governmental agency, on a license to practice "
                    "educational psychology or any other healing art, is itself "
                    "unprofessional conduct. A certified copy of that action is "
                    "conclusive evidence of it.",
            ],
            [
                "16 CCR &sect;1858(e)(2)",
                None,
                "Requires a licensee to report to the Board within 30 days "
                    "any disciplinary action taken by another licensing entity "
                    "or authority of this state, another state, a federal "
                    "agency, or the United States military. Charged in "
                    "conjunction with B&amp;P &sect;4989.54 as unprofessional "
                    "conduct.",
            ],
        ],
        "outcome": "Licensed Educational Psychologist license revoked, the revocation "
            "stayed, and three years of probation imposed. The supervised "
            "practice condition is deemed satisfied by the supervised practice "
            "she is already doing under the Board of Psychology probation.",
        "cost": "$2,000.00",
        "rule": "If you hold more than one license or registration in the healing "
            "arts, discipline on one is, by statute, unprofessional conduct on "
            "the others. The second board does not relitigate the underlying "
            "facts: a certified copy of the first decision is conclusive "
            "evidence of the discipline. Separately, and independently, you "
            "have an affirmative duty to report that discipline to every board "
            "that licenses you, within 30 days. The clock starts with the other "
            "agency&rsquo;s action, not with the date the second board finds "
            "out, and the failure to report is charged as its own cause for "
            "discipline, carrying its own consequences even if the derivative "
            "discipline would have arrived anyway.",
        "ins": "Professional liability coverage does not respond to a derivative "
            "disciplinary action of this kind; the loss is the license, not a "
            "claim by a client, and the misconduct alleged in the first "
            "proceeding included a dishonest or fraudulent act, which every "
            "policy excludes. The license defense benefit will normally pay "
            "counsel for a board proceeding, but many policies apply a single "
            "sublimit per policy period, so a licensee facing two boards over "
            "the same events can exhaust it on the first and pay for the second "
            "herself. Read the sublimit and the aggregation language before you "
            "need them.",
        "prevent": [
            "If you hold a second license, certificate, or registration, "
                "calendar a written report to every board that licenses you on "
                "the day any discipline becomes effective, and send it with "
                "proof of delivery.",
            "Assume the second board will learn of the first board&rsquo;s "
                "action; the failure to report is a separate charge that you "
                "control entirely, unlike the underlying discipline.",
            "When you settle with one board, negotiate knowing a second "
                "proceeding is coming, and ask whether the second board&rsquo;s "
                "conditions can be made to run concurrently with the first, as "
                "the supervision term was here.",
        ],
    },
    {
        # source: BBS decision 036.txt, redacted before it was read
        "slug": "discipline-case-a-mandated-report-never-filed",
        "group": "another",
        "t": "A year of abuse disclosures, no report filed",
        "dek": "The psychology board heard the evidence and imposed probation; the "
            "BBS case ended in surrender.",
        "role": "LMFT",
        "eff": "May 15, 2025",
        "case": "2002024002543",
        "hear": None,
        "facts": [
            "The respondent held an LMFT license from this Board issued May "
                "15, 2008, and also held a psychologist license. Between "
                "February 5 and November 5, 2019, a client attended individual "
                "therapy with her two to three times a month. The client had "
                "two sons, aged six and ten, and was then married to their "
                "father.",
            "Across those months the client described her husband&rsquo;s "
                "violence toward the boys. In February 2019 the older boy said "
                "his father choked him while brushing his teeth on vacation; "
                "his voice was raspy and his face red. On April 25, 2019 both "
                "boys said their father slapped the older boy outside a "
                "restaurant. On May 27, 2019 the younger boy said their father "
                "had slammed the older boy&rsquo;s head into a car window and "
                "strangled him in the car; the mother photographed the injury. "
                "On August 30, 2019 the older boy said his father kicked him in "
                "the back and the younger boy said his father slapped him, "
                "leaving a red handprint the mother also photographed. The "
                "respondent&rsquo;s own clinical notes recorded the February, "
                "April, and August accounts in her own words.",
            "On September 19, 2019 the mother and both children attended a "
                "session together. The children told the respondent they had "
                "been kicked and slapped, that it happened about once a month, "
                "and that they felt scared when alone with their father. She "
                "documented all of it. Her November 5, 2019 note recorded that "
                "the younger boy had choked a classmate at school and had told "
                "his mother he thought it was acceptable because he had seen "
                "his father choke his brother. She never reported the suspected "
                "abuse to Child Protective Services or to any other government "
                "or law enforcement agency.",
            "The mother complained to the Board of Psychology on July 8, "
                "2020. That board filed an accusation on July 6, 2023 and, "
                "after a three-day hearing, found that the information reported "
                "to her required a child abuse report, that her failure to file "
                "one was an extreme departure from the standard of care "
                "amounting to gross negligence, that she violated the APA "
                "ethics standards, and that her lack of knowledge of her "
                "mandated reporter obligations demonstrated a lack of "
                "competence to practice psychology. It adopted the proposed "
                "decision on April 3, 2024, effective May 3, 2024, and placed "
                "her psychologist license on three years of probation. She had "
                "admitted at the hearing that she should have filed a report "
                "after several of the incidents.",
            "This Board filed its accusation on September 19, 2024, "
                "charging her LMFT license on the single ground that another "
                "healing arts board had disciplined her. She was served, timely "
                "filed a notice of defense, was represented by counsel, and "
                "then signed a stipulated surrender of her license.",
        ],
        "charges": [
            [
                "B&amp;P &sect;4982(e)",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=4982&lawCode=BPC",
                "Violating, attempting to violate, or conspiring to violate "
                    "any provision of the marriage and family therapy chapter "
                    "or any regulation adopted by the Board.",
            ],
            [
                "B&amp;P &sect;4982.25(a)",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=4982.25&lawCode=BPC",
                "Discipline imposed by another state, territory, or any "
                    "other governmental agency on a license to practice "
                    "marriage and family therapy or any other healing art "
                    "constitutes unprofessional conduct, and a certified copy "
                    "of that decision is conclusive evidence of it.",
            ],
        ],
        "outcome": "The LMFT license was surrendered and the surrender accepted by the "
            "Board, which is itself the imposition of discipline and part of "
            "her permanent license history. She lost all rights as an LMFT on "
            "the effective date, may not petition for reinstatement, and may "
            "reapply only after three years, meeting all current requirements "
            "including examinations.",
        "cost": "$3,854.00",
        "rule": "Mandated reporting is triggered by reasonable suspicion, not by "
            "proof, and it attaches to information you receive in your "
            "professional capacity, including an account given to you by one "
            "parent about the other. The duty is personal and non-delegable: "
            "telling a client to tell a doctor, a school, or the other parent "
            "does not discharge it, and neither does the fact that someone else "
            "might report. Separately, if you hold a second healing arts "
            "license, discipline imposed by that other board is itself "
            "unprofessional conduct here, established conclusively by a "
            "certified copy of the other board&rsquo;s decision, with no need "
            "to prove the underlying facts a second time.",
        "ins": "A failure to report suspected child abuse is one of the few things "
            "a professional liability policy may actually engage with on the "
            "civil side, since it can be framed as a negligent act in the "
            "rendering of professional services rather than an intentional or "
            "criminal one, though a knowing failure to report is a misdemeanor "
            "and the criminal exposure is uninsurable. What matters more here "
            "is the license defense benefit, which pays counsel for board "
            "proceedings. This respondent used it twice, through a three-day "
            "hearing before one board and a negotiated surrender before "
            "another. No policy restores a surrendered license or pays the "
            "$3,854 that must be cleared before any new license issues.",
        "prevent": [
            "Report on reasonable suspicion, not on certainty. If you are "
                "weighing whether an account is detailed enough to justify a "
                "call, that hesitation is the signal to make it.",
            "Never route a suspected abuse report through anyone else, "
                "including a physician, a school, or the non-offending parent. "
                "The duty is yours personally and advice to a client is not a "
                "report.",
            "Write down the date and time you filed each report and keep "
                "the confirmation with the chart. This respondent&rsquo;s own "
                "progress notes became the strongest evidence against her, "
                "precisely because they recorded the disclosures and nothing "
                "about a report.",
        ],
    },
    {
        # source: BBS decision 040.txt, redacted before it was read
        "slug": "discipline-case-two-nursing-actions-before-registration",
        "group": "applying",
        "t": "Two nursing board actions, then an MFT application",
        "dek": "The Board denied the application, then agreed to issue the "
            "registration under two years&rsquo; probation and a recordkeeping "
            "course.",
        "role": "AMFT",
        "eff": "July 24, 2025",
        "case": "2002024001842",
        "hear": None,
        "facts": [
            "The respondent held a California registered nurse license. On "
                "or about April 5, 2022 the Board of Registered Nursing issued "
                "a disciplinary decision placing that license on <b>two "
                "years&rsquo; probation</b>, effective May 5, 2022. The nursing "
                "board had found that in a 2019 incident, while working as a "
                "registered nurse, she engaged in conduct demonstrating "
                "incompetence and made false or grossly incorrect entries in a "
                "hospital record.",
            "On November 13, 2023 she signed an application for an "
                "Associate Marriage and Family Therapist registration, "
                "certifying under penalty of perjury that every statement, "
                "answer, and representation in it was true. The Board of "
                "Behavioral Sciences received the application on December 26, "
                "2023 and denied it on September 17, 2024.",
            "Three weeks after that denial, on or about October 7, 2024, "
                "the nursing board issued a second decision in a separate case. "
                "The respondent surrendered her registered nurse license, "
                "effective the same day, on findings that in 2021, while "
                "working as a registered nurse, she obtained, possessed, "
                "furnished, or administered medication to patients without the "
                "required physician orders, and again made false or grossly "
                "incorrect entries in hospital records.",
            "The Board filed a Statement of Issues seeking denial of the "
                "registration and served it on February 10, 2025. The "
                "respondent represented herself, chose not to use counsel, "
                "admitted the truth of every charge and allegation, waived her "
                "right to a hearing, and settled.",
        ],
        "charges": [
            [
                "B&amp;P &sect;480(a)(2)",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=480&lawCode=BPC",
                "Lets a board deny a license where the applicant has been "
                    "formally disciplined by a licensing board inside or "
                    "outside California within the seven years before the "
                    "application, for professional misconduct that would have "
                    "been cause for discipline before the board applied to and "
                    "is substantially related to that profession.",
            ],
            [
                "B&amp;P &sect;4982.25(a)",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=4982.25&lawCode=BPC",
                "Makes disciplinary action imposed by another state, "
                    "territory, or any other governmental agency on a license "
                    "in marriage and family therapy or any other healing art "
                    "unprofessional conduct in itself; a certified copy of that "
                    "decision is conclusive evidence that the action occurred.",
            ],
            [
                "16 CCR &sect;1812",
                None,
                "Defines when a crime, act, or instance of professional "
                    "misconduct is &ldquo;substantially related&rdquo; &mdash; "
                    "whether to a substantial degree it evidences present or "
                    "potential unfitness to perform the licensed functions "
                    "consistent with public health, safety, or welfare.",
            ],
            [
                "16 CCR &sect;1813",
                None,
                "Sets the rehabilitation criteria the Board applies to an "
                    "applicant: the nature and gravity of the misconduct, "
                    "anything committed since, the time elapsed, compliance "
                    "with any probation or other sanctions, and the "
                    "applicant&rsquo;s own evidence of rehabilitation.",
            ],
        ],
        "outcome": "The Board ordered that the registration be issued once the "
            "respondent completes all registration requirements, then "
            "immediately revoked, with the revocation stayed and the respondent "
            "placed on two years&rsquo; probation. Conditions include at least "
            "one hour a week of individual face-to-face supervision by an "
            "independent Board-approved supervisor, two graduate semester units "
            "in medical recordkeeping and documentation within 18 months, "
            "notification of every employer, quarterly reports under penalty of "
            "perjury, and $1,200 a year in probation monitoring costs.",
        "cost": None,
        "rule": "Discipline on any other license follows you into a Board of "
            "Behavioral Sciences application. Business and Professions Code "
            "section 480(a)(2) lets the Board deny an application when the "
            "applicant has been formally disciplined by a licensing board in or "
            "outside California within the seven years before the application, "
            "for professional misconduct substantially related to the "
            "profession now being sought; the clock runs from the date of the "
            "other board&rsquo;s discipline to the date of your application, "
            "not from the underlying conduct. Section 4982.25(a) goes further "
            "and makes discipline by another state, territory, or governmental "
            "agency on any healing-arts license unprofessional conduct in its "
            "own right, with a certified copy of the other board&rsquo;s "
            "decision treated as conclusive evidence that it happened &mdash; "
            "so the facts behind it are not open to relitigation here. The duty "
            "to disclose binds applicants, not just licensees, and it does not "
            "stop when you hit send: an application stays open until the Board "
            "acts, and discipline that lands while it is pending becomes part "
            "of the case.",
        "ins": "Nothing about this case is insurable. A professional liability "
            "policy pays for negligent acts, errors, and omissions in providing "
            "professional services; it excludes intentional acts, criminal "
            "acts, and fraud, and falsifying a chart entry is intentional by "
            "definition. There was also no client claim here and no damages to "
            "indemnify. What a policy sold to a California therapist usually "
            "does include is a license-defense benefit &mdash; a capped "
            "reimbursement for the lawyer who answers a Board investigation "
            "letter, negotiates a stipulation, or appears at an administrative "
            "hearing. That benefit generally attaches to a licensee or "
            "registrant, so an applicant who has not yet been registered often "
            "has no coverage at all for exactly the proceeding described here, "
            "and pays out of pocket.",
        "prevent": [
            "If you hold or have ever held another health care license, "
                "disclose every disciplinary action on your Board application "
                "and attach the decisions yourself. The Board obtains certified "
                "copies regardless, and a certified copy is conclusive proof of "
                "the discipline.",
            "Tell the Board in writing about any discipline that lands "
                "after you file. An application is not a snapshot; a second "
                "action arriving mid-review becomes part of the same case.",
            "When the other board&rsquo;s findings were about "
                "documentation, fix documentation before you apply. Take the "
                "recordkeeping coursework voluntarily and file the certificate "
                "with the application rather than waiting to be ordered into "
                "it.",
        ],
    },
    {
        # source: BBS decision 044.txt, redacted before it was read
        "slug": "discipline-case-felony-child-endangerment-never-reported",
        "group": "conviction",
        "t": "Felony child endangerment, and no answer to the Board",
        "dek": "She filed no notice of defense, so every allegation was taken as "
            "true and the registration was revoked by default.",
        "role": "ASW",
        "eff": "December 14, 2023",
        "case": "2002022000859",
        "hear": None,
        "facts": [
            "The Board issued the respondent an Associate Clinical Social "
                "Worker registration on or about December 13, 2019. It expired "
                "on December 31, 2021 and was never renewed.",
            "On or about October 9, 2021, in violation of a temporary "
                "guardianship order that had awarded custody of her daughter to "
                "the child&rsquo;s grandmother, the respondent took the child "
                "from the grandmother&rsquo;s residence without the "
                "guardian&rsquo;s permission or knowledge and refused to return "
                "her to the guardian.",
            "On November 11, 2021, during a domestic argument with her "
                "husband, the respondent drove erratically and at high speed on "
                "a freeway onramp. She stopped, got out, and struck him "
                "repeatedly. She then resumed driving and hit him with the "
                "vehicle, causing him to roll onto the hood and windshield. He "
                "climbed into the car, and she drove away from the collision "
                "before being stopped by the California Highway Patrol. She "
                "told officers she did not know why she had been detained and "
                "denied hitting him. On arrest she refused to follow "
                "directions, attempted to escape, and made repeated profane "
                "comments to the officers.",
            "On June 24, 2022 she was convicted in two Riverside County "
                "Superior Court cases. In the first, she was convicted of "
                "felony child endangerment under Penal Code section 273a(a) "
                "&mdash; a count set to be reduced to a misdemeanor after two "
                "years of successful probation &mdash; and was ordered to serve "
                "jail time, to complete <b>four years of formal probation</b> "
                "and a one-year child abuse treatment program, and to pay "
                "fines, fees, and restitution. In the second, she was convicted "
                "of felony assault with a deadly weapon other than a firearm "
                "under Penal Code section 245(a)(1) and misdemeanor resisting "
                "arrest under Penal Code section 148(a)(1), and was ordered to "
                "serve jail time, complete three years of probation, a 52-week "
                "domestic violence program, a counseling and rehabilitation "
                "program, and 20 hours of community service, and pay fines, "
                "fees, and restitution.",
            "She did not report either conviction to the Board within 30 "
                "days and did not provide the Board with documentation about "
                "her arrests. The Board filed an Accusation on June 8, 2023 and "
                "served it by certified and first class mail at her address of "
                "record. She filed no notice of defense within the 15 days "
                "allowed, which waived her right to a hearing. The Board found "
                "her in default and found the charges true by clear and "
                "convincing evidence on the investigatory evidence packet "
                "alone.",
        ],
        "charges": [
            [
                "B&amp;P &sect;4992.3(a)",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=4992.3&lawCode=BPC",
                "Conviction of a crime substantially related to the "
                    "qualifications, functions, or duties of a clinical social "
                    "worker or associate is unprofessional conduct. The record "
                    "of conviction proves only that the conviction occurred; "
                    "the Board may look behind it at the circumstances to fix "
                    "the degree of discipline.",
            ],
            [
                "B&amp;P &sect;490",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=490&lawCode=BPC",
                "General authority for any Department of Consumer Affairs "
                    "board to suspend or revoke a license for a substantially "
                    "related conviction, including a conviction following a "
                    "plea of no contest, and independent of the practice act.",
            ],
            [
                "B&amp;P &sect;493",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=493&lawCode=BPC",
                "The record of conviction is conclusive evidence that the "
                    "conviction occurred but only of that fact, and a board may "
                    "not categorically bar someone by conviction type without "
                    "considering rehabilitation.",
            ],
            [
                "B&amp;P &sect;4992.3(f)",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=4992.3&lawCode=BPC",
                "Violating, attempting to violate, or conspiring to violate "
                    "the licensing chapter or any regulation the Board has "
                    "adopted &mdash; the hook that turns a reporting regulation "
                    "into a cause for discipline.",
            ],
            [
                "16 CCR &sect;1881(s)(1)",
                None,
                "Requires a clinical social worker licensee or registrant "
                    "to report any felony or misdemeanor conviction to the "
                    "Board within 30 days. A conviction includes a verdict of "
                    "guilty or a plea of guilty or no contest.",
            ],
            [
                "16 CCR &sect;1881(t)",
                None,
                "Requires the licensee or registrant to provide "
                    "documentation about their arrest to the Board within 30 "
                    "days of the Board&rsquo;s request.",
            ],
            [
                "16 CCR &sect;1812",
                None,
                "Defines &ldquo;substantially related&rdquo; as conduct "
                    "that to a substantial degree evidences present or "
                    "potential unfitness to practice consistent with public "
                    "health, safety, or welfare.",
            ],
            [
                "16 CCR &sect;1814(a)",
                None,
                "Lists the rehabilitation criteria the Board weighs before "
                    "revoking: severity, later conduct, time elapsed, "
                    "compliance with probation, any Penal Code section 1203.4 "
                    "expungement, and the licensee&rsquo;s own evidence.",
            ],
            [
                "B&amp;P &sect;4990.33",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=4990.33&lawCode=BPC",
                "The expiration, cancellation, forfeiture, suspension, or "
                    "voluntary surrender of a license or registration does not "
                    "deprive the Board of jurisdiction to investigate or to "
                    "revoke.",
            ],
            [
                "Pen. Code &sect;273a(a)",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=273a&lawCode=PEN",
                "Child endangerment: willfully causing or permitting a "
                    "child to suffer, or to be placed in a situation "
                    "endangering health or person, under circumstances likely "
                    "to produce great bodily harm or death.",
            ],
            [
                "Pen. Code &sect;245(a)(1)",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=245&lawCode=PEN",
                "Assault with a deadly weapon or instrument other than a "
                    "firearm.",
            ],
            [
                "Pen. Code &sect;148(a)(1)",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=148&lawCode=PEN",
                "Willfully resisting, delaying, or obstructing a peace "
                    "officer in the discharge of duty.",
            ],
        ],
        "outcome": "The Board found the respondent in default under Government Code "
            "section 11520, found every charge true by clear and convincing "
            "evidence, and revoked the Associate Clinical Social Worker "
            "registration effective December 14, 2023. She had seven days after "
            "service of the decision to move to have it vacated for good cause.",
        "cost": None,
        "rule": "Every California behavioral sciences registrant and licensee must "
            "report any felony or misdemeanor conviction to the Board in "
            "writing within 30 days. For clinical social workers and associates "
            "the rule is title 16, California Code of Regulations, section "
            "1881(s)(1); the identical duty for marriage and family therapists "
            "sits at section 1845(g)(1). The clock starts at the conviction, "
            "and the regulation defines a conviction to include a verdict of "
            "guilty or a plea of guilty or no contest &mdash; not sentencing, "
            "not the end of an appeal, and not the later reduction of a felony "
            "to a misdemeanor. A separate subdivision, section 1881(t), gives "
            "you 30 days from the date the Board asks to produce documentation "
            "about an arrest. The duty binds you whether or not the crime "
            "touched your practice, whether or not the Board already knows "
            "through its fingerprint subscription, and, under Business and "
            "Professions Code section 4990.33, whether or not the registration "
            "has since expired.",
        "ins": "A professional liability policy will not touch the conduct here. "
            "Every policy excludes intentional acts, criminal acts, and fraud, "
            "and there is no version of a felony assault or a child "
            "endangerment conviction that reads as a negligent professional "
            "service. What such a policy does routinely include is a "
            "license-defense benefit that reimburses the cost of a lawyer to "
            "respond to a Board investigation and represent you at an "
            "administrative hearing &mdash; and that is the part of this case "
            "that was actually available and went unused. The respondent never "
            "filed a notice of defense, so no hearing happened and no defense "
            "was mounted. The most valuable thing a policy can buy in a "
            "criminal-conviction case is the person who makes sure the 15-day "
            "deadline is met and the mitigation gets in front of the Board.",
        "prevent": [
            "Calendar 30 days from any plea or verdict and report it to the "
                "Board in writing before that date, even when the charge is a "
                "wobbler that will be reduced later and even when your criminal "
                "lawyer treats the matter as closed.",
            "Keep your address of record current with the Board. Service at "
                "that address is legally effective whether or not the mail "
                "reaches you, and a notice you never opened still starts the "
                "15-day clock.",
            "File a notice of defense within 15 days of service, even if "
                "you intend to settle or to surrender. Filing preserves the "
                "hearing and every argument that goes with it; not filing "
                "forfeits all of them at once.",
        ],
    },
    {
        # source: BBS decision 045.txt, redacted before it was read
        "slug": "discipline-case-signed-her-supervisors-name",
        "group": "applying",
        "t": "She wrote her supervisor&rsquo;s name on the hours forms",
        "dek": "The Board revoked her registration, granted her a new one on three "
            "years&rsquo; probation, and cut the cost award from $10,650 to "
            "$3,000.",
        "role": "APCC",
        "eff": "January 18, 2024",
        "case": "2002022001395",
        "hear": "OAH No. 2022050774",
        "facts": [
            "The Board issued the respondent an Associate Professional "
                "Clinical Counselor registration on October 18, 2016. On June "
                "7, 2021 it received her application for licensure as a "
                "professional clinical counselor, and on October 18, 2021 it "
                "received additional documents supporting that application, "
                "including an In-State Experience Verification form and Weekly "
                "Summary of Experience Hours forms signed by her former "
                "clinical supervisor.",
            "Board staff concluded the documents were inadequate to "
                "establish the required supervised hours and sent a letter on "
                "July 2, 2021 describing the deficiencies. The respondent "
                "revised the forms and asked her former supervisor, who had by "
                "then left the agency and moved out of state, to sign them. The "
                "supervisor was on an extended vacation and returned the signed "
                "revisions in mid-August 2021. Staff then asked for a further "
                "revision. The respondent prepared a third set, sent it for "
                "signature, and afterward realized she had not obtained the "
                "supervisor&rsquo;s signature on all of the documents staff had "
                "asked her to revise.",
            "Rather than ask again, the respondent wrote the "
                "supervisor&rsquo;s name on copies of the remaining documents "
                "and submitted them to the Board as if they bore the "
                "supervisor&rsquo;s true signature. The supervisor had not "
                "authorized her to sign in her stead.",
            "On November 22, 2021 Board staff emailed the supervisor to "
                "confirm the supervision and the signatures. The supervisor "
                "confirmed she had supervised the respondent but said the "
                "documents did not carry her signature. She texted the "
                "respondent the same day to say the Board had contacted her. "
                "That evening the respondent emailed Board staff admitting she "
                "had &ldquo;made mistakes on my supervisor&rsquo;s "
                "signature,&rdquo; describing the anxiety and pressure she felt "
                "to be approved for the remaining licensure examination, and "
                "asking for a second chance.",
            "The Board filed an Accusation on March 25, 2022. Her "
                "registration cancelled on October 31, 2022 on reaching its "
                "six-year limit. The Board denied her August 2022 application "
                "for a subsequent associate registration on October 3, 2022, "
                "and on October 28, 2022 filed a combined first amended "
                "accusation and statement of issues. An administrative law "
                "judge heard the matter on February 2 and May 25, 2023. The "
                "Board rejected the proposed decision on August 24, 2023 and "
                "decided the case itself on the transcript and written argument "
                "under Government Code section 11517.",
        ],
        "charges": [
            [
                "B&amp;P &sect;4999.90(b)",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=4999.90&lawCode=BPC",
                "Securing a license or registration by fraud, deceit, or "
                    "misrepresentation on any application submitted to the "
                    "Board &mdash; whether the person doing it is the applicant "
                    "or a licensee acting in support of an application.",
            ],
            [
                "B&amp;P &sect;4999.90(j)",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=4999.90&lawCode=BPC",
                "The commission of any dishonest, corrupt, or fraudulent "
                    "act substantially related to the qualifications, "
                    "functions, or duties of a licensee or registrant.",
            ],
            [
                "B&amp;P &sect;4990.33",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=4990.33&lawCode=BPC",
                "Expiration, cancellation, or surrender of a registration "
                    "does not deprive the Board of jurisdiction to proceed "
                    "&mdash; which is how a registration already cancelled at "
                    "its six-year limit could still be revoked.",
            ],
            [
                "B&amp;P &sect;4990.34",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=4990.34&lawCode=BPC",
                "Lets the Board place a registrant or applicant on "
                    "probation instead of revoking or denying, where public "
                    "welfare can be protected without keeping the person out of "
                    "practice altogether.",
            ],
            [
                "16 CCR &sect;1812",
                None,
                "Defines &ldquo;substantially related&rdquo; as conduct "
                    "that to a substantial degree evidences present or "
                    "potential unfitness to practice consistent with public "
                    "health, safety, or welfare.",
            ],
            [
                "16 CCR &sect;1813(c)",
                None,
                "The rehabilitation criteria the Board applies to an "
                    "applicant when the denial rests on professional misconduct "
                    "rather than a completed criminal sentence.",
            ],
            [
                "16 CCR &sect;1814(c)",
                None,
                "The rehabilitation criteria on revocation, including how "
                    "unintentional or immaterial a false statement was and "
                    "whether the person tried to correct it or instead tried to "
                    "conceal the truth.",
            ],
            [
                "B&amp;P &sect;125.3",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=125.3&lawCode=BPC",
                "Authorizes the Board to recover the reasonable costs of "
                    "investigating and enforcing a case from a licentiate found "
                    "to have violated the licensing act.",
            ],
        ],
        "outcome": "The Associate Professional Clinical Counselor registration was "
            "revoked. The application for a subsequent associate registration "
            "was granted: the registration issues on completion of all "
            "requirements, is then immediately revoked, that revocation is "
            "stayed, and the respondent is on three years&rsquo; probation with "
            "weekly psychotherapy, two graduate semester units in law and "
            "ethics, supervised practice once she is licensed, and $1,200 a "
            "year in monitoring costs.",
        "cost": "$3,000.00",
        "rule": "Every signature on a document you send the Board must be made by "
            "the person whose name it is. Business and Professions Code section "
            "4999.90(b) reaches fraud, deceit, or misrepresentation on any "
            "application for licensure or registration or on the documents "
            "supporting it, and it binds two people at once &mdash; the "
            "applicant who submits the form and the licensee who signs in "
            "support of it. Subdivision (j) reaches any dishonest act "
            "substantially related to the license, whether or not it works. The "
            "supervisor&rsquo;s signature on an experience verification form is "
            "the only independent confirmation the Board has that the hours are "
            "real, so what is being certified is the signature and not the "
            "arithmetic; it was no defense here that the numbers were accurate "
            "and identical to what the supervisor had already reviewed. The "
            "parallel provisions for the other Board licenses are sections "
            "4982(b) and (k) for marriage and family therapists and 4992.3(b) "
            "and (l) for clinical social workers, and section 4990.33 means a "
            "registration that has expired or hit its six-year cap is still "
            "within reach.",
        "ins": "A forged signature is an intentional act, and every professional "
            "liability policy excludes intentional acts, dishonesty, and fraud "
            "from indemnity. There is nothing here for a policy to pay on the "
            "merits. Where a policy would have helped is the part of the case "
            "that actually cost money: the license-defense benefit, which "
            "reimburses the fee of a lawyer to answer the accusation, prepare "
            "the mitigation record, and appear at hearing. This matter ran to a "
            "two-day administrative hearing followed by written argument to the "
            "Board, and the respondent was represented by counsel throughout. "
            "Read the sublimit on your own policy and note that it is usually a "
            "fixed dollar cap, not a percentage &mdash; a contested two-day "
            "hearing can exhaust a small one.",
        "prevent": [
            "Never sign, trace, type, or otherwise supply another "
                "person&rsquo;s name on a Board document, even when you hold "
                "their signed original for identical content and are certain of "
                "what they would sign.",
            "When Board staff ask for revised forms, ask in writing exactly "
                "which documents need a fresh signature, then route every one "
                "of them back to the supervisor and wait. A supervisor on "
                "vacation is a scheduling problem, not an emergency, and no "
                "examination deadline is worth the alternative.",
            "At the end of any supervision relationship, get complete "
                "signed verification forms and keep copies. Supervisors leave, "
                "move states, and lose access to the records that prove your "
                "hours &mdash; which is exactly what happened here.",
        ],
    },
    {
        # source: BBS decision 048.txt, redacted before it was read
        "slug": "discipline-case-probation-traded-for-surrender",
        "group": "conviction",
        "t": "A 0.15 breath test and two missed 30-day deadlines",
        "dek": "She won a probation lighter than the Board&rsquo;s own guideline "
            "minimum, then surrendered the registration less than two years "
            "into it.",
        "role": "AMFT",
        "eff": "December 14, 2023",
        "case": "2002024000775",
        "hear": "OAH No. 2021030051",
        "facts": [
            "On September 13, 2019 police responded to a report of a "
                "vehicle collision and found the respondent at the scene. She "
                "was swaying, had droopy eyelids, and smelled of alcohol. She "
                "said she had been checking her phone while driving and had "
                "drunk three glasses of wine over two hours, the last about 30 "
                "minutes earlier. She could not complete field sobriety tests.",
            "When officers moved to handcuff her she pulled her arm away, "
                "kicked one officer&rsquo;s leg, and pinched his thumb. She "
                "stood on the running board of the patrol car and locked her "
                "legs to keep officers from putting her inside, then yelled and "
                "screamed once she was in. Two breath tests at the Highway "
                "Patrol office established a blood alcohol level of <b>0.15 "
                "percent</b>.",
            "The Board received notice of the arrest from the Department of "
                "Justice on September 15, 2019 &mdash; two days later. On "
                "January 8, 2020 the respondent pleaded no contest in Alameda "
                "County Superior Court to reckless driving with alcohol "
                "involvement, the disposition commonly called a wet reckless. "
                "She was sentenced to 30 days in jail or a work alternative "
                "program, three years of probation, a three-month DUI program, "
                "alcohol testing, and fines and fees. She completed every term "
                "and received a Penal Code section 1203.4 dismissal on March 3, "
                "2021.",
            "On April 15, 2020 the Board wrote asking for documentation "
                "about the arrest and told her she had 30 days to respond. She "
                "did not respond in time. She testified that she notified the "
                "Board on August 24, 2020 &mdash; more than 30 days after the "
                "arrest, more than 30 days after the Board&rsquo;s letter, and "
                "more than 30 days after the conviction. She also had a 2005 "
                "conviction for driving with a blood alcohol level of 0.08 "
                "percent or higher, which she had disclosed when she registered "
                "and which had already produced a Board action.",
            "An administrative law judge heard the matter on August 23, "
                "2021, with the respondent representing herself. The Board "
                "adopted the proposed decision with one wording change, "
                "effective January 6, 2022. In 2023 the respondent invoked the "
                "license-surrender condition of her own probation order and "
                "asked to give up the registration; the Board accepted the "
                "surrender in a separate case, effective December 14, 2023.",
        ],
        "charges": [
            [
                "B&amp;P &sect;4982(a)",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=4982&lawCode=BPC",
                "Conviction of a crime substantially related to the "
                    "qualifications, functions, or duties of a marriage and "
                    "family therapist or associate, including a conviction "
                    "following a plea of no contest, and irrespective of a "
                    "later Penal Code section 1203.4 dismissal.",
            ],
            [
                "B&amp;P &sect;4982(c)",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=4982&lawCode=BPC",
                "Using alcohol or a controlled substance to an extent or in "
                    "a manner dangerous or injurious to yourself, another "
                    "person, or the public, or to the extent that it impairs "
                    "your ability to practice safely.",
            ],
            [
                "B&amp;P &sect;490",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=490&lawCode=BPC",
                "General authority for a board to suspend or revoke a "
                    "license for a substantially related conviction, as an "
                    "independent basis from the practice act.",
            ],
            [
                "16 CCR &sect;1845(g)(1)",
                None,
                "Requires a marriage and family therapist licensee or "
                    "registrant to report any felony or misdemeanor conviction "
                    "to the Board within 30 days. A conviction includes a "
                    "verdict of guilty or a plea of guilty or no contest.",
            ],
            [
                "16 CCR &sect;1845(h)",
                None,
                "Requires the licensee or registrant to provide "
                    "documentation about their arrest to the Board within 30 "
                    "days of the Board&rsquo;s request.",
            ],
            [
                "Veh. Code &sect;23103",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=23103&lawCode=VEH",
                "Reckless driving: driving with willful or wanton disregard "
                    "for the safety of persons or property.",
            ],
            [
                "Veh. Code &sect;23103.5",
                None,
                "The wet reckless provision: when a drunk driving charge is "
                    "reduced to reckless driving, the prosecutor states on the "
                    "record that the offense involved alcohol, and that "
                    "statement is recorded on the driver&rsquo;s history.",
            ],
            [
                "B&amp;P &sect;125.3",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=125.3&lawCode=BPC",
                "Authorizes the Board to recover the reasonable costs of "
                    "investigation and enforcement, subject to the discretion a "
                    "board must exercise before imposing them.",
            ],
        ],
        "outcome": "The registration was revoked, the revocation stayed, and the "
            "respondent placed on three years&rsquo; probation with a "
            "psychological or psychiatric evaluation, weekly psychotherapy, "
            "total abstinence from alcohol and controlled substances with "
            "random testing, an addictive behavior support group, and two "
            "graduate semester units in substance abuse; no actual suspension "
            "and no supervised practice were imposed. Less than two years in "
            "she invoked the order&rsquo;s license-surrender condition, and the "
            "Board accepted the surrender effective December 14, 2023, barring "
            "her from applying for any Board registration or license for three "
            "years and deeming every charge admitted against any future "
            "application.",
        "cost": None,
        "rule": "Two separate 30-day clocks run in a California criminal case, and "
            "they are independent of each other and of how the criminal case "
            "ends. Title 16, California Code of Regulations, section 1845(g)(1) "
            "requires a marriage and family therapist licensee or registrant to "
            "report any felony or misdemeanor conviction to the Board within 30 "
            "days, and the regulation counts a verdict of guilty or a plea of "
            "guilty or no contest as the conviction &mdash; so the clock starts "
            "at the plea, not at sentencing and not when criminal probation "
            "ends. Section 1845(h) gives you 30 days from the date the Board "
            "asks to produce documentation about your arrest. The parallel "
            "rules for clinical social workers are sections 1881(s)(1) and (t). "
            "Neither duty is excused because the Board already knows &mdash; "
            "here it had the arrest from the Department of Justice two days "
            "after it happened &mdash; and neither is erased by a later Penal "
            "Code section 1203.4 dismissal, which the respondent obtained and "
            "which sections 490 and 4982(a) expressly disregard.",
        "ins": "Drunk driving is a criminal act, and no professional liability "
            "policy indemnifies a criminal act, an intentional act, or the "
            "consequences of either. There was no client claim in this case and "
            "nothing for a policy to pay in damages. The coverage that mattered "
            "is the license-defense benefit: reimbursement for a lawyer to "
            "respond to the Board, negotiate, and appear at hearing. The "
            "respondent represented herself at a contested hearing and, on the "
            "strength of what she put in, avoided both an actual suspension and "
            "a supervised-practice requirement &mdash; but note that no policy "
            "covers the cost of probation itself. The evaluation, the weekly "
            "therapy, the random testing, the graduate coursework, and the "
            "annual monitoring fee were all hers to pay, and that recurring "
            "expense is a large part of why people surrender.",
        "prevent": [
            "Report a conviction to the Board within 30 days of the plea, "
                "even when the Department of Justice has already told them and "
                "even when the plea is a reduced charge such as a wet reckless.",
            "Answer a Board letter inside the window the letter states. A "
                "missed response is its own cause for discipline, wholly "
                "separate from whatever the Board was asking about.",
            "Read the license-surrender condition in a probation order "
                "before you agree to the probation. It is the exit, and it is "
                "permanent: no reinstatement petition, a fixed bar on "
                "reapplying, and every charge deemed true and admitted if you "
                "ever come back.",
        ],
    },
    {
        # source: BBS decision 063.txt, redacted before it was read
        "slug": "discipline-case-thirty-four-year-sentence-then-registration",
        "group": "applying",
        "t": "A 34-year prison sentence, then a social work application",
        "dek": "The Board denied the application, then settled by issuing the "
            "registration under five years&rsquo; probation and a psychological "
            "evaluation.",
        "role": "ASW",
        "eff": "March 6, 2025",
        "case": "2002024001328",
        "hear": None,
        "facts": [
            "The acts underlying the respondent&rsquo;s conviction occurred "
                "on or about January 25, 2002. On or about July 1, 2003, in Los "
                "Angeles County Superior Court, he was convicted of two felony "
                "counts of violating Penal Code section 245(d)(2), assault on a "
                "peace officer or firefighter with a semiautomatic firearm, and "
                "admitted a special allegation under Penal Code section "
                "12022.53(c) that he personally and intentionally discharged a "
                "firearm in the commission of the crime.",
            "The court sentenced him to <b>34 years in prison</b>, with a "
                "recommendation that he receive schooling and job training. He "
                "was discharged from parole on or about July 26, 2021.",
            "On August 8, 2023 he signed an application for an Associate "
                "Clinical Social Worker registration, certifying under penalty "
                "of perjury that every statement, answer, and representation in "
                "it was true. The Board received the application on September "
                "1, 2023 and denied it on June 5, 2024.",
            "The Board filed a Statement of Issues on October 4, 2024 "
                "seeking denial, and served it on October 8, 2024. The "
                "respondent represented himself, chose not to use counsel, "
                "admitted the truth of every charge and allegation, agreed that "
                "his registration was subject to denial, waived his right to a "
                "hearing, and settled on probationary terms.",
        ],
        "charges": [
            [
                "B&amp;P &sect;480(a)",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=480&lawCode=BPC",
                "Lets a board deny a license where the applicant was "
                    "convicted of a substantially related crime within the "
                    "seven years before the application, or is presently "
                    "incarcerated for such a crime, or was released from "
                    "incarceration for one within those seven years; "
                    "subdivision (a)(1)(A) singles out serious felonies as "
                    "defined in Penal Code section 1192.7.",
            ],
            [
                "B&amp;P &sect;481",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=481&lawCode=BPC",
                "Requires every board to publish criteria for whether a "
                    "crime is substantially related &mdash; gravity, years "
                    "elapsed, and the duties of the profession &mdash; and "
                    "forbids denying a license in whole or in part on a "
                    "conviction without considering the applicant&rsquo;s "
                    "rehabilitation evidence.",
            ],
            [
                "B&amp;P &sect;493",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=493&lawCode=BPC",
                "The record of conviction is conclusive evidence that the "
                    "conviction occurred but only of that fact, and a board may "
                    "not categorically bar an applicant based solely on the "
                    "type of conviction.",
            ],
            [
                "B&amp;P &sect;4992.3(a)",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=4992.3&lawCode=BPC",
                "Conviction of a crime substantially related to the "
                    "qualifications, functions, or duties of a clinical social "
                    "worker or associate is unprofessional conduct and grounds "
                    "to deny a registration.",
            ],
            [
                "16 CCR &sect;1812",
                None,
                "Defines &ldquo;substantially related&rdquo; as conduct "
                    "that to a substantial degree evidences present or "
                    "potential unfitness to perform the licensed functions "
                    "consistent with public health, safety, or welfare.",
            ],
            [
                "16 CCR &sect;1813",
                None,
                "Sets out how the Board evaluates rehabilitation on an "
                    "application, including whether the criminal sentence was "
                    "completed without a parole or probation violation, the "
                    "length and terms of supervision, the time elapsed, and the "
                    "applicant&rsquo;s own evidence.",
            ],
            [
                "Pen. Code &sect;245(d)(2)",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=245&lawCode=PEN",
                "Assault with a semiautomatic firearm on a peace officer or "
                    "firefighter engaged in the performance of duty, where the "
                    "person knows or reasonably should know the victim is such "
                    "an officer.",
            ],
            [
                "Pen. Code &sect;12022.53(c)",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=12022.53&lawCode=PEN",
                "A sentence enhancement for personally and intentionally "
                    "discharging a firearm during the commission of specified "
                    "felonies.",
            ],
        ],
        "outcome": "The Board ordered that the registration be issued once the "
            "respondent completes all registration requirements, then "
            "immediately revoked, with the revocation stayed and the respondent "
            "placed on five years&rsquo; probation. Conditions include a "
            "psychological or psychiatric evaluation within 90 days and "
            "periodically after, compliance with the evaluator&rsquo;s "
            "recommendations, two graduate semester units in anger management "
            "within 18 months, supervised practice once he is licensed as a "
            "clinical social worker, reporting any violation of law within 72 "
            "hours, and $1,200 a year in monitoring costs.",
        "cost": None,
        "rule": "A conviction does not have to be recent to reach a license "
            "application. Business and Professions Code section 480(a)(1) lets "
            "the Board deny where the applicant was convicted of a "
            "substantially related crime within the seven years before the "
            "application &mdash; but the same subdivision also reaches an "
            "applicant who is presently incarcerated for such a crime, or who "
            "was released from incarceration for one within those seven years. "
            "The window therefore runs from release, not from conviction, which "
            "is why a 2003 conviction was still live against a 2023 "
            "application; serious felonies as defined in Penal Code section "
            "1192.7 are drawn out for separate treatment. What the statute does "
            "not permit is an automatic no: sections 481(c) and 493(b)(2) both "
            "forbid the Board from denying on a conviction, or categorically "
            "barring an applicant by conviction type, without weighing the "
            "rehabilitation evidence the applicant files under the criteria in "
            "title 16 section 1813. That evidence has to come from the "
            "applicant, and the Board can only weigh what is in front of it.",
        "ins": "There is no insurance for this. A professional liability policy "
            "responds to negligent acts, errors, and omissions in providing "
            "professional services, and it excludes criminal acts and "
            "intentional acts entirely; a conviction and the licensing "
            "consequences of a conviction are outside every policy sold to a "
            "California therapist. The license-defense benefit that policies do "
            "carry is the one part of the market that touches Board "
            "proceedings, but it is written for licensees and registrants "
            "defending conduct during a policy period &mdash; an applicant "
            "contesting a denial over a pre-existing conviction has no policy "
            "yet and nothing to claim under. An applicant in this position pays "
            "for their own counsel, or, as here, represents themselves. Buy the "
            "policy when the registration issues, and read what its "
            "license-defense section actually covers before you need it.",
        "prevent": [
            "Disclose every conviction on the application, with the court, "
                "the counts, the sentence, and the discharge date. The Board "
                "fingerprints every applicant, so the record arrives either "
                "way; what you control is whether your account of it arrives "
                "with it.",
            "Build the rehabilitation record before you apply, not after "
                "the denial: proof that parole or probation was completed "
                "without violation, the years elapsed, coursework, work "
                "history, and letters. The Board is required by statute to "
                "consider it and can consider only what you file.",
            "Expect conditions written to the offense. A conviction "
                "involving violence drew a psychological evaluation, an anger "
                "management requirement, and five years of monitoring at the "
                "respondent&rsquo;s own expense &mdash; plan and budget for "
                "that rather than being surprised by it.",
        ],
    },
    {
        # source: BBS decision 073.txt, redacted before it was read
        "slug": "discipline-case-eight-weeks-without-a-therapist",
        "group": "probation",
        "t": "Eight weeks without a therapist, and a year added to probation",
        "dek": "The gap opened when her own Board-approved therapist became "
            "unavailable, and the Board counted it as a violation anyway.",
        "role": "ASW",
        "eff": "September 28, 2023",
        "case": "2002023002018",
        "hear": "OAH No. 2023050773",
        "facts": [
            "The respondent applied for an Associate Clinical Social Worker "
                "registration in August 2019. The Board denied the application "
                "in November 2019 because of an October 1, 2014 conviction on "
                "one interlineated felony count of Penal Code section 487(a), "
                "grand theft. The conduct behind it ran from June 6, 2008 to "
                "December 2, 2010, while she worked as a library media "
                "assistant and librarian for a school district: she "
                "requisitioned and misdirected district textbooks for her own "
                "financial gain and took kickbacks from a district-authorized "
                "vendor. The court sentenced her to 365 days in jail, three "
                "years of criminal probation, 100 hours of community service, "
                "and <b>$14,214.00</b> in victim restitution. In June 2017 the "
                "court reduced the felony to a misdemeanor under Penal Code "
                "section 17(b)(3) and entered a civil judgment for the "
                "$15,298.40 of restitution still owed.",
            "She settled the resulting Statement of Issues. Effective July "
                "9, 2020, the registration was issued and immediately revoked, "
                "the revocation was stayed, and she was placed on four years of "
                "probation. The conditions included a psychological or "
                "psychiatric evaluation, ongoing psychotherapy with a "
                "Board-approved California-licensed therapist who filed "
                "quarterly reports on her fitness to practice, a graduate-level "
                "law and ethics course, quarterly reports under penalty of "
                "perjury, and $1,200 a year toward the cost of monitoring her "
                "probation.",
            "Three things went wrong. Her approved therapist held their "
                "last session on December 15, 2020 and then became unavailable; "
                "she did not submit a replacement therapist for the "
                "Board&rsquo;s approval until February 11, 2021, missing "
                "<b>eight weeks</b> of the required weekly sessions. After the "
                "Board reduced the requirement to once a month in September "
                "2021, her quarterly reports showed no session at all in March "
                "2022, which she attributed to scheduling conflicts, and none "
                "in May 2022.",
            "She also stopped practicing on June 1, 2022 and returned to "
                "work on July 18, 2022, but did not tell the Board until August "
                "30, 2022. Condition 8 required written notice 30 calendar days "
                "before a period of non-practice begins and before the return. "
                "The non-practice pushed her projected probation end date from "
                "July 9, 2024 to August 24, 2024. Separately, $1,200 in "
                "probation monitoring costs due no later than August 24, 2022 "
                "was not paid until March 27, 2023.",
            "The Board filed a Petition to Revoke Probation in April 2023. "
                "She filed a notice of defense contesting it, represented "
                "herself, and then settled, admitting the truth of every charge "
                "and allegation.",
        ],
        "charges": [
            [
                "B&amp;P &sect;4990.33",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=4990.33&lawCode=BPC",
                "The Board keeps jurisdiction to investigate and discipline "
                    "even after a license or registration expires, is "
                    "cancelled, or is voluntarily surrendered.",
            ],
            [
                "Probation Condition 2 &mdash; Psychotherapy",
                None,
                "Ongoing psychotherapy with a Board-approved "
                    "California-licensed therapist who has no prior "
                    "relationship with the registrant, at least weekly unless "
                    "the Board says otherwise, with quarterly written reports "
                    "from the therapist to the Board.",
            ],
            [
                "Probation Condition 8 &mdash; Failure to Practice",
                None,
                "Written notice to the Board 30 calendar days before any "
                    "period of non-practice longer than 30 days and before "
                    "returning; the time does not count toward the probation "
                    "term.",
            ],
            [
                "Probation Condition 18 &mdash; Reimbursement of Probation "
                    "Program",
                None,
                "$1,200 a year toward what it costs the Board to monitor "
                    "the probation, for the whole probation period.",
            ],
            [
                "B&amp;P &sect;480(a)(1)",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=480&lawCode=BPC",
                "The original ground for denial: a board may deny an "
                    "application because the applicant was convicted of a crime "
                    "substantially related to the profession.",
            ],
            [
                "B&amp;P &sect;4992.3(a)",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=4992.3&lawCode=BPC",
                "Conviction of a substantially related crime is "
                    "unprofessional conduct for a clinical social worker "
                    "applicant, registrant, or licensee.",
            ],
            [
                "16 CCR &sect;1812",
                None,
                "A crime is substantially related if to a substantial "
                    "degree it evidences present or potential unfitness to "
                    "practice consistent with public health, safety, or "
                    "welfare.",
            ],
        ],
        "outcome": "Probation revoked, the revocation stayed, and the original "
            "four-year term extended by one additional year from August 24, "
            "2024, to run consecutively with the probation already in effect. "
            "All original terms and conditions remained in force.",
        "cost": None,
        "rule": "A disciplinary probation is a set of dated obligations that run on "
            "their own clock, and each one is separately enforceable. Ongoing "
            "psychotherapy means a therapist the Board has approved in advance, "
            "at the frequency the Board sets, filing quarterly reports; a break "
            "in that arrangement is the registrant&rsquo;s problem to fix, not "
            "the therapist&rsquo;s. Non-practice conditions require written "
            "notice before the gap starts, which means a leave, a layoff, or a "
            "wait between jobs has to be reported ahead of time, and the gap "
            "does not shorten the probation. Monitoring fees are due on the "
            "dates in the order. Violating any of these lets the Board set "
            "aside the stay and impose the revocation that was held in reserve, "
            "and it can extend the term instead.",
        "ins": "Nothing here is an insurable loss. A professional liability policy "
            "pays for claims arising from professional services, and it "
            "excludes intentional acts, criminal acts, and fraud &mdash; the "
            "theft conviction that started this file would have been excluded "
            "outright. What most policies do include is license-defense or "
            "disciplinary-proceedings expense coverage, a separate limit that "
            "pays counsel to represent you in a Board investigation, an "
            "accusation, or a petition to revoke probation. That coverage is "
            "worth having and worth using early, but no policy pays your "
            "probation monitoring fees, your court-ordered therapy, or the year "
            "the Board adds to your term.",
        "prevent": [
            "If a Board-approved therapist or supervisor becomes "
                "unavailable, submit a replacement for approval that week; the "
                "requirement does not pause while you look for someone new.",
            "Send the written non-practice notice 30 days before you stop "
                "working, not after you come back, and treat parental leave, a "
                "layoff, and a gap between jobs as non-practice.",
            "On the day a decision takes effect, calendar every report "
                "date, payment date, and course deadline in it, and keep "
                "documentary proof that you met each one.",
        ],
    },
    {
        # source: BBS decision 076.txt, redacted before it was read
        "slug": "discipline-case-road-rage-and-a-default-revocation",
        "group": "conviction",
        "t": "A drive-through altercation, then no answer to the Board",
        "dek": "He never reported the conviction, never answered two letters, and "
            "never filed a notice of defense; the registration was revoked "
            "without a hearing.",
        "role": "AMFT",
        "eff": "August 15, 2024",
        "case": "2002023001429",
        "hear": None,
        "facts": [
            "On or about December 16, 2022, officers were dispatched to a "
                "fast-food restaurant to investigate an altercation in the "
                "drive-through lane. Witness statements, security footage, and "
                "mobile-phone footage showed that the respondent pulled his car "
                "in front of another driver&rsquo;s car and that she yelled at "
                "him. He got out, walked to her window, reached into her car, "
                "and tried to take the phone out of her hand. He fell, got up, "
                "and tried to take the phone again. He then called her a racial "
                "slur and told her to go back where she came from, or words to "
                "that effect.",
            "On April 13, 2023, in Orange County Superior Court, he was "
                "convicted on his plea of guilty of violating Penal Code "
                "section 240, assault, and Penal Code section 242, battery, "
                "both misdemeanors. The court granted one year of informal "
                "probation, during which he was to enroll in and complete a "
                "10-session anger management program, stay at least 100 yards "
                "from the location of the crime, and pay restitution, among "
                "other terms.",
            "He did not report the conviction to the Board. On May 23, 2023 "
                "and again on October 3, 2023, the Board wrote to his address "
                "of record asking for a description of the circumstances of the "
                "arrest, any evidence of rehabilitation, and proof that he had "
                "complied with the court&rsquo;s orders. He never responded to "
                "either letter and never notified the Board of the conviction.",
            "The Board filed an accusation on May 6, 2024 and served it on "
                "May 17, 2024 by certified and first class mail at the address "
                "of record he is required by law to keep current with the "
                "Board. He did not file a notice of defense within 15 days, "
                "which waived his right to a hearing on the merits. His "
                "registration expired on May 31, 2024 and was not eligible for "
                "renewal, which did not stop the proceeding.",
            "The Board took the case by default, found the allegations true "
                "by clear and convincing evidence on the investigatory evidence "
                "packet alone, and found the actual costs of investigation and "
                "enforcement to be <b>$2,597.50</b> as of June 11, 2024.",
        ],
        "charges": [
            [
                "B&amp;P &sect;490",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=490&lawCode=BPC",
                "A board may suspend or revoke a license because the "
                    "licensee was convicted of a crime substantially related to "
                    "the qualifications, functions, or duties of the "
                    "profession.",
            ],
            [
                "B&amp;P &sect;4982(a)",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=4982&lawCode=BPC",
                "Conviction of a substantially related crime is "
                    "unprofessional conduct for a marriage and family therapist "
                    "registrant or licensee; the record of conviction proves "
                    "only that the conviction happened, and the Board may "
                    "inquire into the surrounding circumstances.",
            ],
            [
                "16 CCR &sect;1845(g)(1)",
                None,
                "Failure to report any felony or misdemeanor conviction to "
                    "the Board within 30 days is itself unprofessional conduct; "
                    "a conviction includes a verdict of guilty and a plea of "
                    "guilty or no contest.",
            ],
            [
                "16 CCR &sect;1845(h)",
                None,
                "Failure to give the Board documentation about the "
                    "licensee&rsquo;s or registrant&rsquo;s arrest within 30 "
                    "days of a request is unprofessional conduct.",
            ],
            [
                "B&amp;P &sect;4990.33",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=4990.33&lawCode=BPC",
                "Expiration, cancellation, or surrender of a registration "
                    "does not deprive the Board of jurisdiction to start or "
                    "finish a disciplinary case.",
            ],
            [
                "B&amp;P &sect;125.3",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=125.3&lawCode=BPC",
                "The Board may seek the reasonable costs of investigating "
                    "and enforcing a case from a licensee found to have "
                    "violated the licensing act.",
            ],
        ],
        "outcome": "Registration revoked by default under Government Code section "
            "11520. The decision records investigation and enforcement costs of "
            "$2,597.50; the order itself directed revocation and gave him seven "
            "days after service to move to vacate the decision for good cause.",
        "cost": "$2,597.50",
        "rule": "A conviction creates two separate duties, and the second one is "
            "the one people miss. The first is substantive: a conviction "
            "substantially related to the profession is a ground for "
            "discipline, weighed on the nature and gravity of the offense, the "
            "years since it happened, and the duties of the profession. The "
            "second is procedural and absolute: within 30 days of any felony or "
            "misdemeanor conviction &mdash; including one entered on a plea of "
            "guilty or no contest &mdash; you must report it to the Board in "
            "writing, and within 30 days of a Board request you must produce "
            "documentation about an arrest. Both duties run to the address of "
            "record you are required to keep current, and service there is "
            "effective whether or not you open the mail. Failing to file a "
            "notice of defense within 15 days of an accusation waives the "
            "hearing and lets the Board decide the case on its own evidence "
            "packet.",
        "ins": "A professional liability policy would not have touched the "
            "underlying conduct. Assault and battery are intentional and "
            "criminal acts, excluded from every professional liability policy, "
            "and the incident had nothing to do with professional services in "
            "any event. What a policy usually does provide is a separate "
            "license-defense limit covering the cost of an attorney when the "
            "Board opens an investigation or files an accusation &mdash; which "
            "is precisely the point in a case like this. That coverage is only "
            "useful if you notify the carrier when the Board&rsquo;s first "
            "letter arrives; it cannot help after a default has been entered.",
        "prevent": [
            "Report any conviction &mdash; misdemeanor, "
                "infraction-adjacent, or no-contest plea &mdash; to the Board "
                "in writing within 30 days, without waiting for sentencing, "
                "expungement, or your criminal lawyer to finish.",
            "Keep the address of record current and read everything sent "
                "there; service at that address is legally effective even if "
                "the mail never reaches you.",
            "Answer a Board inquiry even when the facts are bad, and file "
                "the notice of defense within 15 days; a default gives up the "
                "hearing where rehabilitation would have been weighed.",
        ],
    },
    {
        # source: BBS decision 077.txt, redacted before it was read
        "slug": "discipline-case-almost-forty-years-of-rehabilitation",
        "group": "applying",
        "t": "A 1985 murder conviction, and a 2024 registration on probation",
        "dek": "The judge found cause to deny and granted the application anyway: "
            "nearly 40 years, a clean parole, and a master&rsquo;s degree in "
            "counseling.",
        "role": "APCC",
        "eff": "August 15, 2024",
        "case": "2002023002544",
        "hear": "OAH No. 2023100840",
        "facts": [
            "On November 1, 1985, the respondent, then 22, argued with a "
                "parking attendant in the lot next to the building where he "
                "worked nights cleaning a bank. He drove home, retrieved his "
                "gun, returned to the lot, and shot the attendant, who died. He "
                "then went inside and called the police to report what he had "
                "done. He later told police he shot the victim because he was "
                "angry over the argument and because the victim had called him "
                "a name, and he admitted that the victim had not threatened him "
                "verbally or physically. The Statement of Issues alleged six "
                "shots; the Proposed Decision says he shot the victim several "
                "times.",
            "On November 14, 1986, an Orange County jury convicted him of "
                "second degree murder under Penal Code section 187 and found "
                "that he had personally used a firearm in the commission of a "
                "felony under Penal Code section 12022.5. He was sentenced to "
                "<b>17 years to life</b> in state prison. He was released to "
                "parole on March 31, 2011 and was successfully discharged from "
                "parole on April 1, 2016, with no parole violations.",
            "He applied on April 19, 2023 for registration as an associate "
                "professional clinical counselor. The Board denied the "
                "application by letter on July 25, 2023 and told him he could "
                "appeal. He requested a hearing on August 12, 2023; the "
                "Executive Officer signed a Statement of Issues on September "
                "21, 2023; an administrative law judge heard the matter by "
                "videoconference on April 23, 2024. He represented himself.",
            "The rehabilitation record he put in: two associate degrees "
                "earned in prison, in welding and computer repair; Alcoholics "
                "Anonymous from the early 2000s while still incarcerated, plus "
                "group and individual therapy; no alcohol since about 1998 and "
                "no unprescribed controlled substances; help in founding a "
                "support group, modeled on AA, for people released after life "
                "terms, and continued attendance at its monthly meetings; "
                "steady employment since release, including construction; a "
                "marriage, and becoming a father and a grandfather; a "
                "bachelor&rsquo;s degree in May 2018, magna cum laude; a "
                "<b>master&rsquo;s degree in counseling in December 2022</b>; "
                "work as a substance abuse counselor at the pre-license level "
                "and as an employment coach for adults with autism spectrum "
                "disorder and Down syndrome; and monthly therapy since 2020. He "
                "submitted letters from his parole agent, two employers, his "
                "own therapist, a clinical supervisor who had overseen his "
                "student-intern field work, and friends. He has no other "
                "arrests or convictions.",
            "He expressed remorse, said he wanted to counsel people leaving "
                "prison, and described his crime as his driver for change. The "
                "judge found he testified in an open and forthright manner, "
                "consistent with one who is being truthful.",
        ],
        "charges": [
            [
                "B&amp;P &sect;480(a)(1)(A)",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=480&lawCode=BPC",
                "A board may deny an application for a substantially "
                    "related conviction; the ordinary seven-year lookback does "
                    "not apply where the conviction was for a serious felony as "
                    "defined in Penal Code section 1192.7.",
            ],
            [
                "B&amp;P &sect;4999.90(a)",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=4999.90&lawCode=BPC",
                "Conviction of a substantially related crime is "
                    "unprofessional conduct for a professional clinical "
                    "counselor applicant, registrant, or licensee, and a ground "
                    "to refuse a registration.",
            ],
            [
                "B&amp;P &sect;482",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=482&lawCode=BPC",
                "Every board must publish criteria for evaluating "
                    "rehabilitation and must consider whether the applicant "
                    "completed the criminal sentence without a parole or "
                    "probation violation.",
            ],
            [
                "B&amp;P &sect;493",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=493&lawCode=BPC",
                "The record of conviction proves only that the conviction "
                    "occurred; substantial relationship turns on the nature and "
                    "gravity of the offense, the years elapsed, and the duties "
                    "of the profession, and a board may not categorically bar "
                    "an applicant by conviction type without considering "
                    "rehabilitation.",
            ],
            [
                "16 CCR &sect;1812",
                None,
                "A crime is substantially related if to a substantial "
                    "degree it evidences present or potential unfitness to "
                    "perform the licensed functions consistent with public "
                    "health, safety, or welfare.",
            ],
            [
                "16 CCR &sect;1813",
                None,
                "The rehabilitation criteria a board must apply to an "
                    "applicant: nature and gravity of the crime, later acts, "
                    "time elapsed, compliance with the terms of probation or "
                    "parole, and the applicant&rsquo;s own evidence of "
                    "rehabilitation.",
            ],
            [
                "Pen. Code &sect;187",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=187&lawCode=PEN",
                "Murder.",
            ],
            [
                "Pen. Code &sect;12022.5",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=12022.5&lawCode=PEN",
                "Added prison time for personally using a firearm in the "
                    "commission of a felony.",
            ],
        ],
        "outcome": "The application was granted. The registration issues on completion "
            "of all requirements, is immediately revoked, the revocation is "
            "stayed, and the respondent is on five years of probation. Adopting "
            "the Proposed Decision, the Board reduced the penalty by deleting "
            "one condition, the clinical diagnostic evaluation, which would "
            "have carried an automatic one-month suspension and twice-weekly "
            "random drug testing.",
        "cost": None,
        "rule": "When a board denies an application, the applicant carries the "
            "burden of proving entitlement to the license by a preponderance of "
            "the evidence. Establishing cause to deny is the easy half for the "
            "board: a conviction is substantially related if it evidences "
            "present or potential unfitness, judged on the nature and gravity "
            "of the offense, the years elapsed, and the duties of the "
            "profession. The real case is the second half, rehabilitation, "
            "decided on the criteria in title 16, section 1813: what the crime "
            "was, what has happened since, how much time has passed, whether "
            "probation or parole was completed without violation, and whatever "
            "evidence the applicant chooses to put in. The governing purpose is "
            "protection of the public rather than punishment, so a board that "
            "can be satisfied by conditions is expected to impose conditions "
            "instead of refusing outright. Sustained good conduct over a long "
            "period is the strongest single indicator, and a full "
            "acknowledgment of wrongfulness is treated as a precondition to any "
            "finding of rehabilitation.",
        "ins": "Insurance is beside the point for the underlying conduct: a "
            "criminal act is excluded from every professional liability policy, "
            "and no policy existed. The coverage that matters at this stage is "
            "license-defense expense, sold as part of most professional "
            "liability policies to registrants and pre-licensed associates, "
            "which pays counsel to represent you before the Board and at an "
            "Office of Administrative Hearings hearing. An applicant who has "
            "not yet been issued a registration usually has no such policy in "
            "force, which is one reason applicants so often appear without "
            "counsel. The respondent here represented himself at a hearing "
            "where the burden of proof was on him.",
        "prevent": [
            "If you have a conviction, disclose it fully on the application "
                "and put the whole rehabilitation record in front of the Board "
                "before it decides; the applicant carries the burden and the "
                "Board rules on what it is given.",
            "Assemble evidence that maps onto the regulation: proof the "
                "sentence and parole were completed without violation, the "
                "dates, documented treatment, sustained employment, and letters "
                "from people who supervised your clinical work, not only from "
                "friends.",
            "State plainly what you did and that it was wrong; minimizing "
                "is treated in the case law as the absence of rehabilitation, "
                "not as advocacy.",
        ],
    },
    {
        # source: BBS decision 095.txt, redacted before it was read
        "slug": "discipline-case-serious-felonies-ignore-the-seven-year-rule",
        "group": "applying",
        "t": "Nearly sixteen years on, a 2008 conviction still reached the "
            "application",
        "dek": "The seven-year lookback in section 480 does not apply to serious "
            "felonies; the registration issued on three years of probation.",
        "role": "ASW",
        "eff": "December 4, 2025",
        "case": "2002024002349",
        "hear": None,
        "facts": [
            "On September 2, 2006, police responded to a bar in Orange "
                "County about a bar fight that ended with the respondent "
                "assaulting someone with a knife.",
            "On May 22, 2008, in Orange County Superior Court, he was found "
                "guilty and convicted of attempted murder under Penal Code "
                "sections 664(a) and 187(a), and of two counts of assault with "
                "a deadly weapon other than a firearm, great bodily injury "
                "likely, under Penal Code section 245(a)(1). All three counts "
                "were felonies. At a sentencing hearing on December 12, 2008 he "
                "was sentenced to <b>7 years to life</b> in state prison with "
                "credit for 250 days served.",
            "He filed an application for an Associate Clinical Social "
                "Worker registration with the Board on March 29, 2024, dated "
                "March 15, 2024. The Board denied it on April 15, 2025 on the "
                "basis of his criminal history. A Statement of Issues followed "
                "and was served on June 30, 2025. The stipulation notes that "
                "the Statement of Issues stated the application dates a year "
                "late.",
            "The Board&rsquo;s cause for denial rested on the exception in "
                "the statute rather than the ordinary rule. Section 480(a)(1) "
                "normally lets a board deny an application only for a "
                "conviction within the preceding seven years, and nearly "
                "sixteen years had passed. But the seven-year limit does not "
                "apply where the applicant was convicted of a serious felony as "
                "defined in Penal Code section 1192.7, and the Board cited two "
                "of that section&rsquo;s definitions: subdivision (c)(9), "
                "attempted murder, and subdivision (c)(23), any felony in which "
                "the defendant personally used a dangerous or deadly weapon.",
            "He was represented by counsel and settled, admitting the truth "
                "of every charge and allegation and agreeing to be bound by the "
                "Board&rsquo;s probationary terms. The decision contains no "
                "factual findings about anything he did between 2008 and the "
                "application.",
        ],
        "charges": [
            [
                "B&amp;P &sect;480(a)(1)",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=480&lawCode=BPC",
                "A board may deny an application for a substantially "
                    "related conviction within the preceding seven years "
                    "&mdash; except that the seven-year limit falls away for a "
                    "serious felony under Penal Code section 1192.7 or an "
                    "offense requiring sex offender registration.",
            ],
            [
                "B&amp;P &sect;4992.3(a)",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=4992.3&lawCode=BPC",
                "Conviction of a substantially related crime is "
                    "unprofessional conduct and a ground to deny a clinical "
                    "social worker registration; the Board may look into the "
                    "circumstances surrounding the crime to fix the degree of "
                    "discipline.",
            ],
            [
                "Pen. Code &sect;1192.7(c)",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=1192.7&lawCode=PEN",
                "Defines serious felony, including at (c)(9) attempted "
                    "murder and at (c)(23) any felony in which the defendant "
                    "personally used a dangerous or deadly weapon.",
            ],
            [
                "16 CCR &sect;1812",
                None,
                "A crime is substantially related if to a substantial "
                    "degree it evidences present or potential unfitness to "
                    "practice consistent with public health, safety, or "
                    "welfare, judged on nature and gravity, years elapsed, and "
                    "the duties of the profession.",
            ],
            [
                "16 CCR &sect;1813",
                None,
                "The rehabilitation criteria a board applies to an "
                    "applicant: nature and gravity, later acts, time elapsed, "
                    "compliance with probation or parole terms, and evidence of "
                    "rehabilitation submitted by the applicant.",
            ],
            [
                "Pen. Code &sect;664",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=664&lawCode=PEN",
                "Attempt to commit a crime.",
            ],
            [
                "Pen. Code &sect;187",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=187&lawCode=PEN",
                "Murder.",
            ],
            [
                "Pen. Code &sect;245(a)(1)",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=245&lawCode=PEN",
                "Assault with a deadly weapon other than a firearm, or by "
                    "means of force likely to produce great bodily injury.",
            ],
        ],
        "outcome": "The application was granted by stipulation. The registration "
            "issues on completion of all requirements, is immediately revoked, "
            "the revocation is stayed, and the respondent is on three years of "
            "probation, with $1,200 a year in probation monitoring costs.",
        "cost": None,
        "rule": "The seven-year lookback in section 480 is not a clean slate. For a "
            "serious felony as defined in Penal Code section 1192.7, and for "
            "offenses requiring sex offender registration, the time limit "
            "disappears and a conviction of any age remains a ground for "
            "denial. Subdivision (c)(23) of that definition sweeps in any "
            "felony in which the defendant personally used a dangerous or "
            "deadly weapon, so a weapon in the file is usually enough to remove "
            "the time bar entirely. Everything else still applies: the Board "
            "must still find the crime substantially related, must still work "
            "through the rehabilitation criteria, and cannot bar an applicant "
            "categorically by conviction type. The age of the conviction "
            "becomes an argument about rehabilitation rather than a limit on "
            "the Board&rsquo;s reach.",
        "ins": "There is nothing insurable in the criminal conduct; intentional "
            "acts, criminal acts, and fraud are excluded from every "
            "professional liability policy. The coverage that matters to a "
            "person in this position is license-defense expense, the separate "
            "limit inside most professional liability policies that pays an "
            "attorney to represent you in a Board matter. An applicant has no "
            "registration and usually no policy, so the legal fees in a "
            "Statement of Issues case come out of pocket &mdash; this "
            "respondent hired his own counsel. Once the registration issues, "
            "buy the policy immediately, and understand that the probation "
            "itself is a consequence, not a claim: no insurer reimburses the "
            "$1,200 annual monitoring fee, the psychological evaluation, or the "
            "weekly therapy the order requires.",
        "prevent": [
            "Do not assume an old conviction has aged out; check whether it "
                "is a serious felony under Penal Code section 1192.7 &mdash; "
                "which includes any felony involving personal use of a weapon "
                "&mdash; before you rely on the seven-year window.",
            "Disclose the whole criminal history on the application, with "
                "the disposition documents attached; the Board pulls the record "
                "either way, and a gap becomes a second, independent problem.",
            "Get counsel before you answer a Statement of Issues; a "
                "negotiated registration on probation is a real option, and "
                "most applicants do not know it exists.",
        ],
    },
]
