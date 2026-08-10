# -*- coding: utf-8 -*-
"""The discussion layer for the case library. Analysis, kept apart from record.

WHY THIS IS A SEPARATE FILE FROM `case_data.py`

`case_data.py` holds what the signed decisions say. Its whole value is that a
reader can trust every sentence in it to be traceable to a public document, and
the guards in `build_cases.py` exist to keep it that way.

What follows is not that. It is commentary - what the case is doing in the
library, what the Board was actually deciding, what a reader should carry away.
It is argued rather than sourced, and mixing it into the record file would have
quietly made the record file untrustworthy. So it lives here, is rendered in a
visually distinct block, and is labelled on the page as analysis.

The rule for writing anything in this file: it may interpret a fact that is
already in `case_data.py`, and it may not introduce a new one. If a paragraph
here needs a fact the record does not contain, the fact goes in the record
first, with its source, or the paragraph does not get written.

WHAT EACH ENTRY CARRIES

  why    One sentence. Why this case earns a page, said plainly.
  disc   Two to four paragraphs of discussion.
  ask    Three questions. These exist because the library is used to teach -
         graduate law-and-ethics courses and licensing-exam study - and a case
         study with no question at the end is just a story.
"""

DEPTH = {

    # ------------------------------------------------------------- sexual
    "discipline-case-sex-with-a-residential-client": {
        "why": "It is the ceiling. Every other case in the library is somewhere "
               "below this one, and the cost recovery is the largest in three "
               "years of California MFT discipline.",
        "disc": [
            "The striking thing about this decision is not the conduct, which "
            "needs no analysis. It is the <b>stay</b>. Section 4982.26 says that "
            "where a decision contains any finding of fact that the licensee "
            "engaged in sexual contact as defined in &sect;729, the Board shall "
            "revoke and the revocation shall not be stayed &mdash; not by the "
            "administrative law judge and not by the Board itself. This licensee "
            "kept a license, on probation. That is only possible because the "
            "matter resolved as a stipulated settlement whose findings were "
            "written so as not to contain the finding that triggers &sect;4982.26.",
            "That is worth sitting with, because it is the single most "
            "counter-intuitive mechanic in California discipline. The severity "
            "of the sanction is not a direct function of the severity of the "
            "conduct. It is a function of <b>what the document says</b>. A "
            "settlement is a negotiated text, and which findings appear in it "
            "decides which mandatory provisions switch on.",
            "The second thing the decision teaches is that the money is a "
            "separate violation from the sex. The client sent at least $14,500 "
            "that had nothing to do with therapy, and the request for $5 million "
            "was framed by the therapist as protection against losing her "
            "license. Under &sect;4982(j) that is a dishonest act, chargeable on "
            "its own facts. Strip out every sexual element and the money alone "
            "would still have supported discipline.",
        ],
        "ask": [
            "The revocation here was stayed even though the conduct is what "
            "&sect;4982.26 was written for. Explain the mechanism, and say what "
            "a respondent's counsel is negotiating over when they negotiate "
            "findings of fact.",
            "The client's own text message in the record reads &ldquo;Wait this "
            "is illegal.&rdquo; What does it tell you about capacity to consent "
            "that the client, not the clinician, is the one who names the "
            "problem?",
            "Identify every cause for discipline that would still exist if no "
            "sexual contact had ever occurred.",
        ],
    },

    "discipline-case-the-two-year-rule-is-not-a-loophole": {
        "why": "The two-year rule is the most widely misunderstood sentence in "
               "&sect;4982, and this case shows what the misunderstanding costs.",
        "disc": [
            "Therapists read &sect;4982(k) as a waiting period: end therapy, "
            "wait two years, and a relationship becomes permissible. The statute "
            "does not work that way, and this decision is the cleanest available "
            "illustration. Terminating therapy <i>in order to</i> begin a "
            "relationship is the exact fact pattern &sect;729 identifies by name. "
            "The termination does not start a clock; it is itself part of the "
            "conduct.",
            "The second mechanic here is quieter and worse. The therapist's own "
            "chart documented mood lability, feelings of emptiness and elevated "
            "suicide risk, and the accusation used that chart to characterise "
            "the client as vulnerable to exploitation. The record the therapist "
            "wrote to meet the standard of care became the evidence that she "
            "knew who she was dealing with. Good documentation is not a defence "
            "against a boundary violation. It is proof of knowledge.",
            "And note the timing of the first chargeable act. The sentence in "
            "session &mdash; that they could pursue a relationship if they ended "
            "therapy &mdash; was a solicitation, and &sect;4982(k) reaches "
            "solicitation. Everything after it aggravated a violation that had "
            "already happened.",
        ],
        "ask": [
            "At what precise moment did the first chargeable violation occur? "
            "Justify your answer from the text of &sect;4982(k).",
            "The therapist's clinical documentation was used against her. Does "
            "that create any tension with the duty to keep accurate records, and "
            "if not, why not?",
            "The cost recovery was ordered payable in full before any new "
            "license could ever issue. What does that condition do that a plain "
            "money judgment would not?",
        ],
    },

    "discipline-case-three-days-after-the-last-session": {
        "why": "Pre-licensure conduct follows the license, and the reason he "
               "gave for not consulting his supervisor is the reason most people "
               "give.",
        "disc": [
            "He was an intern when this began and an LMFT when it was charged. "
            "The discipline attached to the license he eventually held. There is "
            "a widespread assumption that pre-licensure conduct is somehow "
            "outside the Board's reach because there was no license to discipline "
            "at the time; there is nothing in the statute that supports it, and "
            "&sect;4982(u) separately makes violating the rules governing the "
            "gaining and supervision of experience its own ground.",
            "The line the decision records &mdash; that he did not raise any of "
            "it with his clinical supervisor <i>for fear of being fired</i> "
            "&mdash; is the most repeatable sentence in the entire library. It "
            "appears in different words in several other cases here. The "
            "structural point is that supervision is the mechanism the "
            "profession relies on to catch exactly this, and the mechanism has a "
            "known failure mode: the supervisee's employment depends on the "
            "person they are supposed to disclose to.",
            "Three days is not a gap. It is a continuation with a break in it, "
            "and the decision treats it that way.",
        ],
        "ask": [
            "If a supervisee's honest disclosure could cost them their job, the "
            "supervisory relationship has a built-in conflict. What would you "
            "change about how supervision is structured to reduce it?",
            "The relationship ran for more than two years. Would waiting the "
            "full two years from termination have made it lawful on these facts? "
            "Explain.",
            "Which cause for discipline attaches to the supervision failure "
            "rather than to the relationship?",
        ],
    },

    "discipline-case-eight-years-of-escalation": {
        "why": "The controlled-substance provision has no clinical-context "
               "exception, which matters to every therapist working anywhere "
               "near psychedelic-assisted practice.",
        "disc": [
            "Eight years, one client, and a continuous therapeutic relationship "
            "that crossed a trainee registration, an internship and a license. "
            "There is no point in this timeline at which a new relationship "
            "begins; the decision treats it as one relationship, and every stage "
            "of it is inside the Board's reach.",
            "The provision to read closely is &sect;4982(c). Its second sentence "
            "is mandatory rather than discretionary: the Board <b>shall</b> deny "
            "or revoke where a licensee uses or offers a controlled substance in "
            "the course of performing marriage and family therapy services. "
            "There is no clinical-context exception in the text, no research "
            "carve-out, and no exemption for a substance the client asked for. "
            "Anyone practising in or adjacent to psychedelic-assisted therapy "
            "should be able to recite that sentence.",
            "The escalation is also a study in how physical boundaries erode "
            "without a decision ever being made. Hugs, then lying together on a "
            "couch, then contact the client could not mistake. No single step in "
            "that sequence looks like the step that ends a career, which is "
            "precisely why the sequence works.",
        ],
        "ask": [
            "Read &sect;4982(c) and identify every element the Board must "
            "establish. Which of them is contested in a case like this one?",
            "The relationship spanned trainee, intern and licensed status. What "
            "would each of those three supervisors or employers have needed to "
            "see to interrupt it?",
            "Is there any legal route in California by which a therapist could "
            "administer a controlled substance in session? What does your answer "
            "imply for a clinician recruited into a ketamine or psilocybin "
            "practice?",
        ],
    },

    "discipline-case-denied-it-then-admitted-it": {
        "why": "One of the very few cases in the dataset proved at a full "
               "hearing rather than settled, so it shows what the evidentiary "
               "standard actually looks like.",
        "disc": [
            "Almost everything else in this library is a stipulated settlement, "
            "in which the licensee does not admit the allegations and agrees "
            "only that the Board could establish a prima facie case. This one "
            "went to hearing and was proved by <b>clear and convincing "
            "evidence</b>. That is a meaningfully higher standard than the "
            "preponderance test used in ordinary civil matters, and it is worth "
            "knowing that the Board met it here.",
            "Five months is not two years. The clock in &sect;4982(k) runs from "
            "termination, and there is no consent form, consultation or waiting "
            "list that shortens it. The arithmetic in this case is not "
            "difficult, which suggests the miscalculation was not really about "
            "arithmetic.",
            "The denials are the part worth teaching. She denied it to her "
            "employer, denied it again to an investigator the employer retained, "
            "and admitted it two days later. Her stated reason &mdash; fear of "
            "losing her job and her registration &mdash; is the same reason the "
            "intern in another case here gave for saying nothing at all. The "
            "denial did not prevent the outcome. It removed the only mitigation "
            "she had.",
        ],
        "ask": [
            "Compare the evidentiary posture of a stipulated settlement with a "
            "contested hearing. What does a respondent give up, and get, by "
            "settling?",
            "She denied the relationship to a private investigator retained by "
            "her employer, not by the Board. Does that matter to the Board's "
            "case? Should it?",
            "What advice would you give a colleague who told you, in confidence, "
            "what she told her coworker?",
        ],
    },

    "discipline-case-the-slow-boil": {
        "why": "The most carefully reconstructed escalation in the dataset, and "
               "the case where a single unrelated detail would have been "
               "chargeable on its own.",
        "disc": [
            "The decision reconstructs three years month by month, and reading "
            "it in order is the point. Texting between sessions. Then daily "
            "texting. Gifts. Hugs. A pet name. Sessions running for hours, at "
            "night. Self-disclosure about the therapist's own affair. Then "
            "clothing, photographs, a third party, a theme park, a hotel, a "
            "shared bed. No step in that sequence is more than a small "
            "increment on the one before it, and there is no moment at which a "
            "decision was made.",
            "Buried in a case about escalation is a violation that has nothing "
            "to do with it. The therapist took calls from other clients in this "
            "client's presence and used their names. That is a &sect;4982(m) "
            "confidentiality breach with its own penalty range in the "
            "disciplinary guidelines &mdash; stayed revocation, 60 to 90 days of "
            "suspension, three to five years of probation. It would have "
            "supported an accusation on its own, in an otherwise unremarkable "
            "practice, and it is the kind of thing a busy clinician does without "
            "registering it as anything.",
            "The client presented with a history of sexual abuse and "
            "exploitation. The decision does not need to argue that the "
            "therapist knew this; the intake record establishes it.",
        ],
        "ask": [
            "Pick the earliest point in the sequence at which you would expect a "
            "consultation group to intervene, and say what the therapist would "
            "have had to disclose for that to happen.",
            "The confidentiality count is unrelated to the boundary conduct. Why "
            "does the Board charge it anyway, and what does its presence do to "
            "the penalty analysis?",
            "&ldquo;There would never be a final therapy session between "
            "us.&rdquo; What clinical function does that statement serve for the "
            "therapist, and what does it do to the client?",
        ],
    },

    # --------------------------------------------------------------- dual
    "discipline-case-pseudonyms-and-sleepovers": {
        "why": "The findings in this decision are the clearest statement of the "
               "California dual-relationship standard anywhere in the dataset, "
               "and they are auditable against your own practice.",
        "disc": [
            "Two elements appear in the findings, and both can be checked "
            "against a caseload this afternoon. The therapist &ldquo;engaged in "
            "an <b>avoidable</b> dual relationship&rdquo; that ran alongside and "
            "then beyond the therapeutic one, and she &ldquo;fostered "
            "dependency&hellip; by engaging in <b>frequent, non-urgent, and "
            "casual</b> telephone, text message, and in-person "
            "communications.&rdquo; Avoidable, and non-urgent. Those are the two "
            "words to keep.",
            "The pseudonyms are the tell. &ldquo;Hope&rdquo; and "
            "&ldquo;Faith&rdquo; existed so that nobody would know the contact "
            "was continuing. Concealment is not an aggravating flourish on the "
            "underlying conduct; it is evidence that the clinician knew the "
            "conduct would not survive being seen. A useful working test is "
            "whether you would describe the arrangement, in those words, to your "
            "supervisor.",
            "Note also that she discussed her other clients with this client, by "
            "name &mdash; the same independent confidentiality breach that "
            "appears in the slow-boil case, in a completely different fact "
            "pattern. Eight causes for discipline in total, from what began as "
            "informal texting during treatment.",
        ],
        "ask": [
            "Apply the two findings &mdash; avoidable, and non-urgent &mdash; to "
            "three real contacts from a caseload you know. Which survive?",
            "The facility terminated her employment before the Board acted. What "
            "obligations does an employer have when it discovers this, and what "
            "obligations does the clinician have at that point?",
            "Why does using code names in text messages make the case worse "
            "rather than merely stranger?",
        ],
    },

    "discipline-case-disciplined-for-emails": {
        "why": "Nothing physical happened. No meetings, no money, no sex &mdash; "
               "and it is still three years of probation and $7,644.",
        "disc": [
            "This is the most useful case on the site for an ordinary therapist, "
            "because there is no dramatic act to point at and disown. The entire "
            "factual record is an email correspondence. If your defence against "
            "the rest of this library is that you would never do <i>that</i>, "
            "this is the case that does not let you off.",
            "The quoted language sorts into four kinds, and it is worth naming "
            "them. <b>Terms of endearment</b>: &ldquo;Dear One,&rdquo; &ldquo;My "
            "Candle Light.&rdquo; <b>Personal fondness</b>: &ldquo;I will always "
            "be your Hero.&rdquo; <b>Prescriptive daily directives</b>: "
            "&ldquo;Light a candle. Take a hot shower.&rdquo; And <b>merger "
            "language</b>: &ldquo;I am with you,&rdquo; &ldquo;You're still all "
            "around me.&rdquo; Any one of those, once, is a style choice. All "
            "four, repeatedly, several times a day, is a finding of fostered "
            "dependency.",
            "The most damaging single line is &ldquo;If you were the "
            "professional practitioner then you could make that decision.&rdquo; "
            "It is not affectionate at all. It relocates the client's judgement "
            "into the therapist, which is the substance of what the standard of "
            "care prohibits. Warmth is not the violation. Volume, merger and "
            "the transfer of decision-making are.",
        ],
        "ask": [
            "Draft an email to a struggling client that is genuinely warm and "
            "contains none of the four features identified above.",
            "Nothing in &sect;4982 requires physical contact. Where, then, does "
            "the standard of care come from in a case like this, and how is it "
            "proved?",
            "The therapist plainly believed she was helping. Does sincerity "
            "matter to the cause of action? To the penalty?",
        ],
    },

    "discipline-case-cannabis-with-a-client": {
        "why": "A refused offer is still a cause for discipline, and the "
               "therapist's own words did most of the Board's work.",
        "disc": [
            "The client declined the Xanax. It is still chargeable. Section "
            "4982(e) reaches violating, <i>attempting</i> to violate, or "
            "conspiring to violate any provision of the chapter or any Board "
            "regulation, and it is also the hook that pulls the whole of title "
            "16 of the California Code of Regulations into &sect;4982. Whether "
            "the client accepted has nothing to do with whether the offer "
            "happened.",
            "The record here is unusual in that the associate's own statements "
            "supply the findings. &ldquo;I did put us in danger driving&hellip; "
            "my judgment gets impaired when I'm using.&rdquo; That is an "
            "admission of impairment, in his words, in a document he later "
            "signed a settlement on. Read alongside the denial case in this "
            "library, the two make a matched pair: one licensee denied and lost "
            "the mitigation, another admitted and lost the argument.",
            "And again the supervisor was never told. That is now three cases in "
            "this group with the same structural failure, which stops being a "
            "coincidence and starts being a finding about how supervision works "
            "in practice.",
        ],
        "ask": [
            "Explain how &sect;4982(e) converts a Board <i>regulation</i> into a "
            "ground for discipline under the <i>statute</i>. Why does that "
            "matter for a clinician trying to know what the rules are?",
            "The client said she felt unsafe and wanted to return to telehealth. "
            "What was the therapist obliged to do at that moment?",
            "He characterised three outings as social and &ldquo;not "
            "therapy.&rdquo; Does that characterisation help him or hurt him?",
        ],
    },

    "discipline-case-asking-a-client-where-to-buy-drugs": {
        "why": "Asking a client not to report you is not damage control. It is "
               "an additional charge.",
        "disc": [
            "After 54 documented sessions, a single text message opens a "
            "conversation that ends a registration. The content is bad enough on "
            "its own, but the instructive part comes at the end: fired by her "
            "employer, she asked the client not to report her to the Board.",
            "That request is not treated as panic. It goes in the accusation. "
            "Title 16 &sect;1845 makes failure to cooperate with a Board "
            "investigation unprofessional conduct in its own right, and the "
            "Board treats interference with its own process as a distinct "
            "category of misconduct with its own penalty range. The instinct to "
            "contain the damage by talking to the person who could report you is "
            "close to universal, and it reliably makes the case worse.",
            "Note the insistence that the friendship be kept secret. Concealment "
            "appears in this library so often &mdash; pseudonyms, secrecy, a "
            "denial to an investigator &mdash; that it functions as a diagnostic "
            "sign rather than an aggravating detail.",
        ],
        "ask": [
            "A client tells you they intend to complain to the Board about you. "
            "List everything you may do, and everything you may not.",
            "Where in the chain of events did this become unrecoverable? Was "
            "there a point at which self-reporting would have changed the "
            "outcome?",
            "The employer terminated her before any Board involvement. What is "
            "the employer's own reporting duty here?",
        ],
    },

    "discipline-case-drinking-at-lunch": {
        "why": "One afternoon. No client complaint, no harm alleged, no pattern "
               "&mdash; and four years of probation.",
        "disc": [
            "This is the shortest factual record in the library that still "
            "produced serious discipline, and it is here to correct a common "
            "assumption. Section 4982(c) does not require a diagnosis, a "
            "pattern, a client complaint or a demonstrated harm. It requires use "
            "in a manner <i>dangerous or injurious to the licensee or others, or "
            "to an extent that impairs the ability to practise safely</i>. One "
            "session is enough to satisfy that.",
            "The disciplinary guidelines put the floor for impaired ability at "
            "stayed revocation with 60 to 90 days of suspension and five years "
            "of probation. The outcome here &mdash; four years, no suspension "
            "recited &mdash; sits at or below that floor, which tells you "
            "something about how the guidelines function in settlement. They are "
            "the Board's opening position, not a statutory minimum.",
            "The report came from staff, not from a client. That is the pattern "
            "the whole library keeps returning to: the complaint that ends a "
            "career usually does not come from the person in the chair.",
        ],
        "ask": [
            "Read &sect;4982(c). What would the Board have to prove on these "
            "facts, and what would it not?",
            "A colleague returns from lunch and you believe they have been "
            "drinking. What is your obligation as a colleague, as a supervisor, "
            "and as an employer? Are they the same?",
            "No client alleged harm. Why does the statute not require it?",
        ],
    },

    # ------------------------------------------------------------ records
    "discipline-case-the-custody-letter": {
        "why": "Three separate rules break in one case, and each of them is a "
               "rule ordinary therapists get asked to break every year.",
        "disc": [
            "The request will sound familiar to anyone who has treated a couple. "
            "An ex-spouse calls after termination, describes a frightening "
            "situation, and asks for something in writing. Everything about the "
            "framing invites help. The therapist wrote a To Whom It May Concern "
            "letter setting out the former client's diagnosis, suicide attempts "
            "and treatment, with no consent, no court appointment and no request "
            "from the family court. Confidentiality survives termination, and it "
            "survives the other spouse asking nicely.",
            "The second rule is about records. When the Board investigated, the "
            "documents the therapist produced differed from the client's copies "
            "&mdash; different handwriting, marks on different pages, checklist "
            "entries bearing the same date. A record is a contemporaneous "
            "document. A later version that does not match the copy the client "
            "already holds is evidence of a dishonest act under &sect;4982(j), "
            "not a correction. If a record genuinely needs amending, the "
            "amendment is dated and additive.",
            "The third is the one most likely to be missed on a first reading. "
            "Told that the ex-spouse feared he might kill the children, the "
            "therapist made no child abuse report. The mandated reporting duty "
            "is triggered by a reasonable suspicion arising from information "
            "received in a professional capacity &mdash; including information "
            "from a third party, and including about the household of a former "
            "client. The duty did not end with the therapy.",
        ],
        "ask": [
            "Draft the response you would send to the ex-spouse. What can you "
            "say, and to whom?",
            "The therapist arguably believed she was protecting children. "
            "Reconcile that belief with the outcome: what should a clinician who "
            "genuinely fears for a child do instead?",
            "Distinguish a lawful late entry in a clinical record from an "
            "alteration. What does the lawful version look like on the page?",
        ],
    },

    "discipline-case-seven-business-practice-failures": {
        "why": "An outright revocation with no stay and no probation, and not "
               "one clinical allegation in the whole accusation.",
        "disc": [
            "There is no sexual misconduct here, no substance use, and no "
            "clinical error alleged at all. Seven causes for discipline, every "
            "one of them administrative, and the licence was revoked outright "
            "&mdash; no stay, no probation, which puts this among a handful of "
            "unstayed revocations in three years of data. That combination is "
            "the argument for reading the whole case: the Board's most severe "
            "available sanction, imposed for how a practice was run.",
            "Take the counts one at a time and each is preventable with a "
            "template or a calendar reminder. Section 4982(n) requires the fee, "
            "or the basis on which it will be computed, to be disclosed <i>before "
            "treatment commences</i>. Health &amp; Safety Code &sect;123110 gives "
            "a client the right to inspect records within five working days and "
            "to receive copies within fifteen &mdash; here a request from a "
            "client's attorney went unanswered for six months and was never "
            "fully answered. Section 4982(p) requires advertising under the name "
            "on the licence. Six sessions were provided while the licence was "
            "not valid.",
            "The count that turned a difficult case into a hopeless one is the "
            "last. The Board investigator's calls, letters and emails went "
            "unanswered for over a year. Title 16 &sect;1845 makes ignoring the "
            "Board its own violation, independent of the merits of whatever was "
            "being investigated. Every other count here had an explanation "
            "available; silence removed the opportunity to give one.",
        ],
        "ask": [
            "Audit a real or imagined private practice against the four "
            "administrative duties named above. Which would fail today?",
            "A client's attorney requests records. Diagram the deadlines and "
            "what must be produced at each.",
            "Why might the Board treat non-response to an investigation more "
            "severely than the underlying conduct?",
        ],
    },

    "discipline-case-the-address-of-record": {
        "why": "The shortest case in the library, and the structural reason so "
               "many of the others contain a failure-to-cooperate count.",
        "disc": [
            "There is almost nothing to this decision, and that is why it is "
            "here. Alongside the substantive charges sits a separate count for "
            "failing to maintain a current address of record with the Board. "
            "Title 16 &sect;1804 requires it, and it is the address the Board "
            "uses to serve you.",
            "Follow the consequence. An accusation served on a stale address is "
            "still served. The clock on a response runs whether or not the "
            "envelope reached a human being. Read the failure-to-cooperate "
            "counts across the rest of this library and a striking number of "
            "them begin with correspondence sent to an address the licensee had "
            "moved out of &mdash; not with a decision to stonewall.",
            "It is a fifteen-minute administrative task that quietly determines "
            "whether you get to participate in your own case.",
        ],
        "ask": [
            "What is the practical difference between a licensee who refuses to "
            "answer the Board and one who never received the letter? Does the "
            "record distinguish them?",
            "List every entity that needs to be told when a therapist moves "
            "office, and the deadline for each.",
            "Why does the Board make the address a licensee's duty rather than "
            "attempting service by other means?",
        ],
    },

    # -------------------------------------------------------------- money
    "discipline-case-forged-supervisor-signature": {
        "why": "A settlement that landed below the disciplinary guidelines' "
               "published minimum &mdash; which tells you what the guidelines "
               "actually are.",
        "disc": [
            "The situation was real and the pressure was real. Her supervisor of "
            "record had died, and the hours still needed signing. What she did "
            "next &mdash; per the accusation, forging that supervisor's "
            "signature on an In-State Experience Verification form and a Weekly "
            "Summary submitted with her exam eligibility application &mdash; is "
            "fraud in securing a licence.",
            "The disciplinary guidelines set the minimum penalty for that at "
            "outright revocation. This settlement produced stayed revocation and "
            "three years of probation. That is <b>below the published "
            "minimum</b>, and it is one of the most practically useful facts in "
            "this library: the guidelines are the Board's starting point in "
            "settlement negotiation, not a floor beneath which a case cannot "
            "land.",
            "The email chain is the other lesson. The decision reproduces it in "
            "full, including her requests to agency staff to sign on the "
            "deceased supervisor's behalf and a clinical director's reply of "
            "&ldquo;Here you go.&rdquo; Everything about the problem was "
            "documented in writing before anyone thought of it as evidence.",
        ],
        "ask": [
            "Your supervisor of record dies with hours unsigned. Set out the "
            "lawful path, step by step, and identify who has authority to do "
            "what.",
            "The clinical director wrote &ldquo;Here you go.&rdquo; What is that "
            "person's exposure?",
            "If the guidelines are only a starting point, what does that imply "
            "about how a respondent should approach a first settlement offer?",
        ],
    },

    "discipline-case-twenty-three-sessions-in-one-day": {
        "why": "Billing fraud at a scale that is arithmetically impossible to "
               "explain, and a separate count for not reporting the conviction.",
        "disc": [
            "The numbers are the case. Twenty-three individual 45-minute "
            "sessions in a single day is 17.25 hours of psychotherapy. More than "
            "ten hours of Medi-Cal billing on 22 different days, including two "
            "days of 20.5 hours. More than 24 sessions a day on 75 different "
            "dates. One patient billed for 51 sessions, having been seen once. "
            "No account of a clinical practice reconciles with those figures, "
            "which is what makes billing data such effective evidence.",
            "This case also entered the Board's world the way most conviction "
            "cases do: through the criminal system, not through a client. A "
            "Department of Justice Medi-Cal Fraud and Elder Abuse investigation "
            "produced seven felony counts of presenting false claims and seven "
            "of insurance fraud, with aggravating allegations for planning and "
            "sophistication, monetary value, and taking advantage of a position "
            "of trust. She pleaded nolo contendere to one count.",
            "Then the separate count. Title 16 &sect;1845 requires a licensee to "
            "report any felony or misdemeanor conviction to the Board within 30 "
            "days &mdash; independently of the Department of Justice, which "
            "reports it anyway. Not reporting adds a cause with its own penalty "
            "range and removes any argument about candour. She also ignored the "
            "Board's request for an explanation and tried to withdraw her "
            "renewal application, neither of which stopped anything.",
        ],
        "ask": [
            "The Board would have learned of the conviction regardless. Why does "
            "the reporting duty exist, and why is breaching it charged "
            "separately?",
            "A nolo contendere plea is not an admission of guilt in the criminal "
            "matter. What effect does it have in the administrative one?",
            "What would an employer's or payer's routine audit have caught, and "
            "when?",
        ],
    },

    "discipline-case-embezzlement-outside-the-practice": {
        "why": "No client, no session, no connection to therapy at all &mdash; "
               "and the registration went anyway.",
        "disc": [
            "She was an accounts payable clerk at a plumbing company. Sixty-two "
            "checks to herself, $183,200, 33 felony counts of grand theft by "
            "embezzlement plus money laundering and an aggravated white-collar "
            "enhancement. Not one element of it touches a client or a therapy "
            "room.",
            "The bridge is the phrase &ldquo;substantially related.&rdquo; Title "
            "16 &sect;1812 defines it as conduct that to a substantial degree "
            "evidences present or potential unfitness, judged on three factors: "
            "the nature and gravity of the offence, the number of years since it "
            "happened, and the nature and duties of a marriage and family "
            "therapist. Sustained dishonesty involving money and a position of "
            "trust clears that bar comfortably, because the duties of the "
            "profession include handling other people's vulnerability honestly.",
            "This is worth internalising because it is the answer to the "
            "question therapists actually ask, which is whether something in "
            "their private life is the Board's business. The test is not "
            "location. It is what the conduct evidences.",
        ],
        "ask": [
            "Apply the three &sect;1812 factors to a hypothetical shoplifting "
            "conviction from eleven years ago. Reach a conclusion and defend it.",
            "Is there conduct serious enough to be criminal that is <i>not</i> "
            "substantially related to the practice of marriage and family "
            "therapy? Give an example and justify it.",
            "What obligation did she have to the Board, and when did it start?",
        ],
    },

    # ------------------------------------------------------------ another
    "discipline-case-discipline-follows-your-other-license": {
        "why": "Dual-licensed clinicians consistently underestimate "
               "&sect;4982.25, and it is not a re-hearing.",
        "disc": [
            "The Board of Psychology disciplined the psychologist licence; BBS "
            "then filed its own accusation against the marriage and family "
            "therapist licence on the basis of that discipline, plus a separate "
            "count for the underlying violations. Two boards, one course of "
            "conduct, two disciplinary records.",
            "The mechanism matters. Section 4982.25 is not an opportunity to "
            "relitigate. A certified copy of the other board's decision is "
            "<b>conclusive evidence of the facts found</b>, so the only live "
            "issue in the California proceeding is the penalty. A clinician who "
            "plans to fight on the facts has one chance to do it, in whichever "
            "forum acts first, and does not get a second.",
            "Subdivision (b) does the same thing for discipline by BBS itself on "
            "another BBS licence you hold &mdash; which is how holding an MFT "
            "licence and an LPCC registration turns one incident into two "
            "proceedings.",
        ],
        "ask": [
            "You hold licences from two boards and one of them opens an "
            "investigation. How does &sect;4982.25 change your strategy in that "
            "first proceeding?",
            "Why would the legislature make another board's findings conclusive "
            "rather than merely admissible?",
            "What is left to argue in the second proceeding?",
        ],
    },

    "discipline-case-thirty-days-to-report-discipline": {
        "why": "The reporting duty in 16 CCR &sect;1845 is the most frequently "
               "missed obligation in the entire dataset.",
        "disc": [
            "The underlying discipline came from the Board of Psychology. The "
            "additional cause came from not telling BBS within 30 days. It is "
            "difficult to imagine a more avoidable count.",
            "Title 16 &sect;1845 sets out five separate duties and most "
            "licensees can name none of them. Within 30 days you must report "
            "(1) any felony or misdemeanor conviction and (2) discipline by "
            "another licensing entity. You must give the Board records within 15 "
            "days of a request, provide arrest documentation within 30 days of a "
            "request, and cooperate with any investigation. Four of the five are "
            "deadlines, and a deadline is the easiest kind of rule to comply "
            "with and the easiest to miss.",
            "A note for anyone reading the primary documents: accusations filed "
            "between 2023 and 2025 cite the older lettering &mdash; "
            "&sect;1845(g)(1) and &sect;1845(h) for the conviction-reporting and "
            "arrest-document duties &mdash; while the current published text "
            "puts them at (c)(1) and (d). The duty did not change; the "
            "subdivision letters did.",
        ],
        "ask": [
            "Write the five &sect;1845 duties as a one-page checklist a solo "
            "practitioner could keep by the desk.",
            "The Board would likely have learned of the other board's action "
            "anyway. Why is the self-report still required?",
            "Which of the five duties has the shortest deadline, and what is the "
            "practical consequence of missing it?",
        ],
    },

    "discipline-case-out-of-state-discipline": {
        "why": "A licence you keep current in another state is a live exposure "
               "in California, with no California client required.",
        "disc": [
            "Arizona's Board of Behavioral Health Examiners disciplined the "
            "Arizona licence. BBS charged that discipline under &sect;4982.25(a) "
            "and the California licence was surrendered.",
            "Read the statutory language: &ldquo;another state, territory, or "
            "any other governmental agency.&rdquo; It does not require that you "
            "were practising in California, that any California client was "
            "affected, or that the other state's rule has a California "
            "equivalent. Where the conduct would not be a violation here, that "
            "goes to the penalty rather than to whether there is a cause of "
            "action at all.",
            "The practical implication is about dormant licences. Clinicians "
            "keep an out-of-state licence current for the sake of optionality "
            "&mdash; a possible move, occasional telehealth, an employer's "
            "preference &mdash; without registering that they are also keeping a "
            "second regulator with authority to act, whose action lands here.",
        ],
        "ask": [
            "You hold a licence in a state you no longer practise in. List the "
            "arguments for keeping it current and the arguments for letting it "
            "lapse.",
            "Another state disciplines you for conduct that is lawful in "
            "California. What is left to argue in the California proceeding?",
            "How would interstate telehealth practice change your analysis?",
        ],
    },

    "discipline-case-the-only-public-reproval": {
        "why": "The mildest formal discipline available, and the only one issued "
               "to an MFT in three years of data &mdash; which is why the whole "
               "sanction ladder is worth knowing.",
        "disc": [
            "Most therapists have heard of revocation and of probation and know "
            "nothing in between. The ladder, in ascending order, runs: a "
            "citation and fine, which is not formal discipline at all; a public "
            "reproval; probation, typically three to five years; suspension; "
            "surrender; revocation. In four years of Board data there were three "
            "public reprovals across every licence type the Board regulates, and "
            "between 7 and 26 revocations a year.",
            "The origin of this one is the same pattern as the two cases before "
            "it: the Medical Board publicly reprimanded a physician's "
            "certificate, and BBS charged that discipline under &sect;4982.25(a) "
            "against the MFT licence. Three cases in this group, three different "
            "originating boards, one statute.",
            "A public reproval is still public and still formal. It appears on "
            "the licence record and is disclosable. It is the floor, not an "
            "absence of consequence.",
        ],
        "ask": [
            "Place each sanction on the ladder and say what a licensee may still "
            "do at each level.",
            "Given how rare a public reproval is, what would you infer about the "
            "circumstances required to obtain one?",
            "How does a citation and fine differ from formal discipline in terms "
            "of what a future employer or payer can see?",
        ],
    },

    # ------------------------------------------------------------ fitness
    "discipline-case-ignoring-an-order-to-be-examined": {
        "why": "Three cases in one, and in the first of them the accusation "
               "contains no &sect;4982 charge of any kind.",
        "disc": [
            "The first accusation here has a single cause: Business and "
            "Professions Code &sect;821. Not gross negligence, not "
            "unprofessional conduct, no subdivision of &sect;4982. The Board "
            "ordered an examination, the licensee did not attend, and the licence "
            "was revoked on that alone.",
            "Section 821 is a standalone ground. It does not require the Board "
            "to prove that the licensee is unfit &mdash; only that it ordered an "
            "examination and the order was not complied with. The trap is easy "
            "to walk into and obvious afterwards: a licensee who believes the "
            "underlying allegation is baseless declines to submit to an "
            "evaluation, and in doing so converts a case the Board might not "
            "have proved into one it cannot lose.",
            "The second case follows the identical pattern under &sect;822. The "
            "third pairs &sect;&sect;820 and 822 with a conviction count. Three "
            "matters, two revocations and a surrender, and in none of them did "
            "the substance of the original concern ever get decided.",
        ],
        "ask": [
            "You receive an order to submit to a psychological examination and "
            "believe the complaint behind it is meritless. What do you do, and "
            "why?",
            "What is the Board's burden under &sect;821, and how does it differ "
            "from its burden under &sect;4982?",
            "Is there a route to challenge the order itself? What would that "
            "look like procedurally?",
        ],
    },

    # --------------------------------------------------------- convictions
    "discipline-case-two-duis-five-years-probation": {
        "why": "This is the modal California MFT discipline case, and almost "
               "nobody expects it.",
        "disc": [
            "Sixty-two of the 103 decisions read for this library cite "
            "&sect;4982(a), a substantially related conviction. Most of those "
            "are a DUI. If you want to know what discipline in California "
            "usually looks like, it looks like this: two convictions, no client "
            "complaint, no clinical allegation, nothing connected to the "
            "practice at all.",
            "The route in is the part worth knowing. The Board learned of both "
            "convictions through the Department of Justice conviction "
            "notification feed under Penal Code &sect;11105.2, which reports "
            "automatically. There is no discretion about whether the Board finds "
            "out and no complaint anyone could have withdrawn. Each conviction "
            "was charged as a separate cause.",
            "The guidelines set the floor for a substantially related conviction "
            "at stayed revocation, 60 days of suspension and five years of "
            "probation &mdash; and the standard probation conditions include "
            "notifying your clients and your employer that you are on probation. "
            "For a solo practitioner, that condition is frequently the most "
            "consequential part of the entire order.",
        ],
        "ask": [
            "Trace the path from a Saturday-night arrest to an accusation. Who "
            "tells whom, and when is the licensee first obliged to act?",
            "The probation conditions require telling clients. What are the "
            "clinical implications of that disclosure, and how would you handle "
            "it?",
            "Why does the Board treat a DUI as substantially related to the "
            "practice of therapy? Construct the strongest argument on each side.",
        ],
    },

    "discipline-case-failing-to-report-your-own-conviction": {
        "why": "Two registrations, and every cause pleaded twice.",
        "disc": [
            "A single reckless driving conviction produced three causes on the "
            "associate MFT registration: the conviction itself under &sect;490 "
            "and &sect;4982(a), the substance use under &sect;4982(c), and the "
            "failure to report the conviction within 30 days. Then the same "
            "three causes were repeated against her associate professional "
            "clinical counsellor registration under the parallel provisions of "
            "&sect;4999.90. One conviction, six causes.",
            "Holding two BBS registrations does not spread your risk; it "
            "doubles it. Every cause is pleaded twice, probation runs on both, "
            "and &sect;4982.25(b) separately makes BBS discipline on one of your "
            "licences unprofessional conduct as to the other. The dual "
            "registration that looked like career flexibility is a multiplier on "
            "a single bad night.",
            "The reporting count is the avoidable one, and it is the count that "
            "recurs most often across this library. Thirty days, in writing, "
            "whether or not you think the Board already knows.",
        ],
        "ask": [
            "Map the six causes against the two registrations. Which are "
            "genuinely independent and which are the same conduct charged twice?",
            "Weigh the professional benefits of holding both an AMFT and an APCC "
            "registration against the exposure this case illustrates.",
            "What is the reporting deadline, what form does the report take, and "
            "what should it contain?",
        ],
    },

    "discipline-case-charged-without-a-conviction": {
        "why": "The Board does not need a conviction, and it does not need a "
               "subdivision either.",
        "disc": [
            "There were two convictions here &mdash; disobeying a court order, "
            "and criminal threats. What makes the case instructive is the two "
            "additional causes: unprofessional conduct based on a petty theft "
            "incident and a sexual battery incident that produced no conviction "
            "at all.",
            "The opening words of &sect;4982 are &ldquo;unprofessional conduct "
            "includes, but is not limited to, the following.&rdquo; The list of "
            "subdivisions is not exhaustive. The Board can and does charge "
            "conduct directly under that chapeau where no subdivision fits and "
            "no conviction exists, proving it on its own evidence to the "
            "administrative standard rather than the criminal one.",
            "So a dismissed charge, a case the district attorney declined, or an "
            "arrest with no filing all remain available to the Board. A criminal "
            "outcome in your favour ends the criminal matter. It does not end "
            "the administrative one, and the two proceedings answer different "
            "questions on different standards of proof.",
        ],
        "ask": [
            "Contrast the burden of proof in a criminal prosecution with the "
            "burden in a BBS disciplinary proceeding. What follows for a "
            "licensee facing both?",
            "Is there anything objectionable about disciplining a licensee for "
            "conduct that was never prosecuted? Argue both sides.",
            "Your criminal case is dismissed. What do you now owe the Board, if "
            "anything?",
        ],
    },

    # ---------------------------------------------------------- probation
    "discipline-case-four-ways-to-violate-probation": {
        "why": "One of the four ways to violate probation is simply not paying "
               "the bill from the first order.",
        "disc": [
            "The petition to revoke probation alleged four failures: not "
            "completing the ordered psychological evaluation, not obeying all "
            "laws, not submitting quarterly reports, and not paying the cost "
            "recovery. Only the second of those involves anything anyone would "
            "recognise as misconduct. The other three are administrative, and "
            "any one of them is enough.",
            "Cost recovery is a probation condition. That single structural fact "
            "changes what it is: not a debt that can be carried and negotiated "
            "in the ordinary way, but an obligation whose breach is independent "
            "grounds to revoke the licence. Section 125.3 lets the administrative "
            "law judge order the reasonable costs of investigation and "
            "enforcement including the Attorney General's charges; the judge may "
            "reduce or eliminate the amount but cannot increase it beyond the "
            "certified cost statement.",
            "The obey-all-laws condition is what it sounds like. Police "
            "responded to his office, where he was screaming; he had been living "
            "there, had confronted his landlord with an axe, and refused "
            "officers' orders. The condition converts conduct that might "
            "otherwise never reach the Board into a probation violation "
            "immediately.",
        ],
        "ask": [
            "Read the fifteen standard probation conditions. Which three would "
            "be hardest for a solo practitioner to satisfy, and why?",
            "Cost recovery is a condition rather than a debt. What practical "
            "difference does that make to someone who cannot pay?",
            "Should inability to pay be a defence to this kind of violation? "
            "Argue it.",
        ],
    },

    "discipline-case-when-the-judge-cuts-the-bill": {
        "why": "The Board asked for $10,778 and the judge ordered $4,000. Cost "
               "recovery is contestable, and it is the part respondents most "
               "often concede without argument.",
        "disc": [
            "This is a small decision with an outsized practical lesson. On a "
            "petition to revoke probation the Board sought $10,778 &mdash; the "
            "largest cost-recovery request in a probation matter in this dataset "
            "&mdash; and the final order set it at $4,000 while reinstating "
            "probation for three years. The figure moved by more than sixty per "
            "cent because someone argued about it.",
            "The Board's own aggregate numbers show why this matters at scale. "
            "Across four years it ordered $229,823 in cost recovery and "
            "collected $67,857. A published cost statement is a starting "
            "position supported by a certification, not an invoice, and "
            "&sect;125.3 expressly permits the administrative law judge to "
            "reduce or eliminate it.",
            "Set this beside the probation-violation case in the same group, "
            "where non-payment was one of four grounds to revoke. The two "
            "together make the argument: contest the amount at the time it is "
            "set, because after it is set it becomes a condition you can lose "
            "your licence over.",
        ],
        "ask": [
            "On what basis can a respondent challenge a certified cost "
            "statement? What evidence would you want?",
            "The Board collects under a third of what it orders. What does that "
            "gap suggest about how the amounts are set?",
            "Why might a respondent facing revocation not bother arguing about "
            "costs, and why is that a mistake?",
        ],
    },

    "discipline-case-seven-years-under-supervision": {
        "why": "Probation tolling sounds protective and is the opposite: the "
               "clock stops, the obligations continue, and the end date moves.",
        "disc": [
            "Three extension cases. One probation extended by eighteen months "
            "with $3,432 of cost recovery still unpaid, a second extended by "
            "eighteen months with $4,040 outstanding, a third extended by a year "
            "&mdash; and that third began with a case filed in 2018, which by "
            "the extension is seven years under Board supervision and still "
            "running.",
            "Tolling is the mechanism most licensees misunderstand when they "
            "agree to a settlement. Probation is tolled when you are not "
            "practising. That sounds like relief, and it is not: the clock "
            "stops, the obligations do not, and the end date moves out by "
            "however long you were away. One order in this group recites "
            "explicitly that cost-recovery obligations remain in effect whether "
            "or not probation is tolled.",
            "Combine tolling with extensions and a five-year probation routinely "
            "becomes seven or eight years of quarterly reports, employer "
            "notifications, client notifications and monitoring fees of roughly "
            "$1,200 a year. None of it is insured. When a therapist weighs a "
            "settlement offer against the cost of fighting, this is the part of "
            "the ledger that usually goes uncounted.",
        ],
        "ask": [
            "Calculate the full out-of-pocket cost of a five-year probation that "
            "tolls for eighteen months and is then extended by a year.",
            "Tolling exists so that a licensee cannot run out the clock while "
            "not practising. Is the current design fair? What would you change?",
            "How should the prospect of tolling and extension affect the advice "
            "given to someone deciding whether to settle?",
        ],
    },
}


# --------------------------------------------------- the second collection
from case_depth_more import MORE_DEPTH  # noqa: E402

DEPTH.update(MORE_DEPTH)
