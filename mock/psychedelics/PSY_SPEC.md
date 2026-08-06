# Deep-research spec: psychedelic-assisted therapy trainings and certificates

You are researching training programs and certificates in psychedelic-assisted
therapy. The audience is a **California-licensed therapist (LMFT, LCSW, LPCC,
psychologist) or an associate on the way to licensure** who is considering
spending $5,000–$20,000 and one to two years on one of these.

Output: one JSON file per program at
`/home/claude/work/psychedelics/data/<slug>.json`.

## THE TWO RULES

**1. Nothing invented.** Every price, hour count, module name, prerequisite and
date must come from a page you actually fetched, with the URL recorded. If a
program does not publish its price, the field is `null` and it goes in `gaps`.
Never estimate a tuition figure. Never invent a curriculum module name.

**2. The scope question is the whole point.** The single most important thing
this research must answer, for every program, is:

> **"When I finish this, what am I actually allowed to do?"**

Prospective students routinely believe a certificate confers a legal ability to
administer psychedelics. In almost every case it does not. Be rigorous and
plain about this. Specifically establish, per program:

- Does completing it change your **license or scope of practice**? (Almost
  always: no. A certificate is a credential from a school, not from a
  regulator. California's BBS does not recognise or require it.)
- What can a holder **legally do in California today**? The honest baseline:
  **ketamine** is a legal, FDA-approved anaesthetic that clinicians prescribe
  off-label, so ketamine-assisted psychotherapy (KAP) is the only modality a
  California therapist can practise now — and the therapist does not prescribe;
  a physician, NP or PA does. **Psilocybin and MDMA remain Schedule I federally
  and are not legal for therapeutic use in California.** Verify the current
  status as of 2026 — check for any change in California law, any FDA action on
  MDMA-assisted therapy after the August 2024 complete response letter, and the
  status of Oregon's and Colorado's regulated programs (which are the only
  places a US facilitator credential currently does anything).
- Does it qualify a holder for **Oregon psilocybin facilitator licensure** or
  **Colorado facilitator licensure**? Only state-approved curricula do. Check
  whether the program appears on the Oregon Health Authority's approved
  training list or Colorado's DORA list. That is a hard, checkable fact and
  it is the difference between a credential that does something and one that
  does not.
- What does it realistically get you: **integration work** (legal, no special
  credential needed), **KAP practice**, **research roles**, **being credible to
  a clinic that hires**, **being positioned for a future legal framework**?
- Any **preparation/integration-only** framing the program itself uses.

Write this up per program in `scope`, and make it concrete: literally the
sentences that complete "With this certificate I can…" and "With this
certificate I still cannot…".

## HOW TO RESEARCH

1. The program's own site: curriculum, cost, dates, prerequisites, admissions,
   hours, format, faculty.
2. The FAQ page — this is usually where the scope disclaimers live. Read it and
   quote the disclaimer verbatim if there is one.
3. Any state approval list (Oregon Health Authority training programs; Colorado
   DORA). Verify presence or absence.
4. Discussion: Reddit (r/PsychedelicTherapy, r/therapists, r/Psychedelics),
   Psychedelic Support, professional Facebook groups indexed publicly, Trustpilot,
   and any journalism about the program. Include criticism where it is sourced.
   NOTE: reddit.com is likely blocked from this environment — do not burn many
   tool calls on it. Use Google/Bing search result snippets and other sources.
5. Any journalism on the field's problems — the field has had real ethics
   scandals (the MAPS Phase 2 boundary-violation case; the FDA's 2024 rejection
   of MDMA-assisted therapy; concerns about unlicensed practice). Where a
   program's own materials address these, note it.

## OUTPUT SCHEMA

```json
{
  "name": "Certificate in Psychedelic-Assisted Therapies and Research",
  "slug": "<given in your assignment>",
  "org": "California Institute of Integral Studies",
  "location": "San Francisco, CA — hybrid",
  "url": "https://...",
  "one_line": "One sentence a reader can scan in the directory.",
  "summary": ["Two to four paragraphs. What it is, who it is for, what the year actually looks like. Concrete."],
  "modality": ["Which substances the training addresses: e.g. 'Ketamine', 'Psilocybin', 'MDMA', 'General/substance-agnostic'"],
  "cost": {"amount": 10995, "currency": "USD", "note": "2026 cohort; deposit $500; payment plan available", "src": "https://..."},
  "length": "Approximately 12 months",
  "hours": "~150 hours, of which 6 in-person residential days",
  "format": "Online synchronous + two in-person retreats",
  "eligibility": "Who can apply. Be exact — several programs recently changed this.",
  "curriculum": [
    {"module": "Module title", "detail": "What it covers, from the program's own description.", "src": "https://..."}
  ],
  "scope": {
    "changes_license": false,
    "can": ["Concrete things a holder can legally do.", "..."],
    "cannot": ["Concrete things it does NOT authorise.", "..."],
    "or_licensure": "yes | no | not-applicable — whether it is an Oregon Health Authority approved psilocybin facilitator training",
    "co_licensure": "yes | no | not-applicable",
    "disclaimer_quote": "Verbatim scope disclaimer from the program's own materials, if one exists, else null",
    "src": "https://..."
  },
  "faculty": ["Named faculty worth knowing, with why", "..."],
  "voices": [{"text": "...", "who": "source, year", "sentiment": "positive|negative|mixed|info", "url": "..."}],
  "status_2026": "Enrolling | Paused | Waitlist | Unknown — with the date you verified it and a source.",
  "video": {"url": "https://www.youtube.com/watch?v=...", "title": "...", "who": "channel", "why": "why it is worth watching"},
  "gaps": ["What you looked for and could not find."],
  "sources": [{"label": "...", "url": "..."}]
}
```

For `video`: only include a YouTube URL you actually verified exists and is
about this specific program (search `<program name> site:youtube.com`, or check
the org's own channel). A wrong video is worse than none. `null` if unsure.

## TONE FOR THE PROSE FIELDS

Plain, concrete, skeptical-but-fair. The reader is a working clinician deciding
where to put $10,000. Do not use the field's own marketing register
("journey", "sacred container", "medicine") except in quotation marks when
reporting what a program calls itself. Where a program makes a claim about
outcomes or employability, say who is making the claim.

Write the file, then reply with ONE line per program:
`<name> — cost: <figure or none>, <n> modules, <n> voices, OR-approved: y/n, video: y/n, gaps: <n>`
