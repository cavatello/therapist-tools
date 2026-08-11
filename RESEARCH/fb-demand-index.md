# What the California therapist groups actually say — first sweep

**Captured 11 August 2026.** 14 records from two groups, four search queries.
Corpus: `_dev/data/fb-research.jsonl`. Schema and method:
`fb-research-schema.md`. Names and identifying details deliberately excluded.

This supersedes nothing — it extends `claude/facebook-group-observed-demand.md`
(10 Aug) with vendor-specific and hours-tracking findings that sweep didn't
reach.

---

## The five things that change decisions

### 1. There are far more competitors than the web sweep found — and one is being born in the group

The published-web competitive analysis found seven products. This sweep found
**three more in four queries**, two of them invisible to search engines because
they market inside Facebook groups rather than on the open web:

- **SupTrack (SüpTrack)** — posting commercially, and positioned at
  **supervisors**, not associates. A different wedge into the same market.
- **LicenseTrack Pro** — CEU and multi-state licence-renewal tracking. Adjacent,
  and the natural product for someone *after* they license.
- **An unnamed entrant being built right now.** A software developer posted that
  he's building a tracker after watching his partner's cohort struggle —
  **11 reactions, 4 comments**, the highest engagement of any vendor post in the
  sweep. He names the same two pains: *"Spreadsheets stretched to their limits.
  Chasing supervisors for signatures (or literally mailing documents)."*

**Implication.** Barrier to entry is near zero and the window is narrow. Whatever
advantage exists is not the feature set — four teams shipped the same feature set
in six months. It's trust, ranking, and distribution.

### 2. TrackYourHours is losing on support, and users say so publicly

Three independent complaints in two groups, none of them about features:

> *"it bothers me that they don't offer phone support. I put in a support ticket
> and it took 3 days to get a response."*

> *"Is it down at the moment? If anyone has had any tech issues — are they easy
> to get a hold of? They said my email is invalid/account invalid (doesn't
> expire till December)."*

> *"Where do you put your hours in for free client consultations and calling
> insurance to verify eligibility? I use [it] and can't decide where it makes
> sense to categorize."* — **unanswered**

The incumbent's weakness is **reachability and in-product clarity**, not
functionality. That is precisely what a named human and contextual help beat.

### 3. The incumbent's category design is *causing* errors

> *"Can you count duplicate hours for individual therapy if it was done via
> telehealth counseling? The first half of my practicum was done all via
> telehealth."* — **unanswered, 5 reactions**

TrackYourHours lists **"Telehealth Counseling" as its own row** alongside
"Individual Counseling or Psychotherapy." So a user genuinely cannot tell whether
a telehealth individual session belongs in one row, the other, or both — and
nobody answered them.

**Do not replicate that taxonomy.** Telehealth is a *modality*, not a category;
the Board counts the service. If a modality flag is needed, it's a checkbox on
the row, never a parallel row. This is a design bug producing support tickets and
mis-logged hours, and it's fixable by construction.

### 4. "My supervisor won't sign" is the nightmare — and the strongest sales argument

> *"She is refusing to sign my BBS Timesheets and my BBS Experience Verification
> Form. All my hours were completed in good faith, are not under dispute and I
> have the completed Supervision agreement."* — **11 comments**

> *"My old company changed their name half way through... my W-2 still reflects
> the old name. I am afraid to get audited."* — **9 reactions, 5 comments**

Both people are reconstructing a defence *after* the fact. A contemporaneous,
timestamped record — showing not just the hours but **when each entry was made**
and what the supervisor saw and acknowledged — is exactly the artefact they
wish they had.

**This reframes the product.** It is not a convenience tool for logging. It is
**evidence**, assembled continuously, for a moment of dispute or audit that a
meaningful minority will face. That is a much stronger thing to sell, and it
justifies a higher price than "a nicer spreadsheet" ever will.

### 5. Annual-only prepay is a live objection, in the buyer's words

> *"I was doing their free trial, but it felt really expensive to commit to a
> full year, or even more. [The alternative] was a lot more affordable and has
> monthly plans, even a lifetime subscription too."*

Someone switched away from the incumbent **primarily over billing shape, not
price level.** Directly relevant to the $50-vs-$99 question: the objection isn't
only the number, it's the size of the single commitment. Offer a monthly option
even if the annual price is where you want people to land.

---

## Ranked by engagement — what this profession argues about

Combining this sweep with the 10 Aug one:

| Topic | Reactions | Comments | Status |
|---|---|---|---|
| Wage claims for unpaid non-clinical hours | 77 | 86 | page shipped |
| Passing the clinical exam (celebration) | 282 | 47 | — |
| AMFT hired 1099 vs W-2 | 6 | 33 | page shipped |
| **Supervisor refusing to sign forms** | 3 | **11** | **unwritten** |
| New tracker being built by a developer | 11 | 4 | — |
| **Employer name change → audit fear** | **9** | 5 | **unwritten** |
| **Hours tracker with e-signature — which one?** | 1 | **8** | **unwritten** |
| **Which platform? incumbent support is slow** | 1 | 4 | **unwritten** |
| **Telehealth double-counting** | 5 | 0 | **unanswered** |
| **Free consults / insurance calls — which box?** | 0 | 0 | **unanswered** |

**Every bolded row is unwritten and every one of them routes to the tracker.**

---

## Content backlog this produces

1. **`hours-tracker-comparison-california`** — the honest comparison. Named
   humans, real prices, who is contactable, domain ages, what each actually
   does. This is the page the 8-comment thread was asking for, and no one can
   write it credibly except someone willing to name themselves.
2. **`supervisor-refuses-to-sign-hours-california`** — what recourse exists, what
   documentation the Board will accept, what to do before it happens.
3. **`what-counts-bbs-hour-categories`** — free consultations, insurance
   verification, no-shows, note-writing. Both unanswered questions land here.
4. **`does-telehealth-count-bbs-hours`** — and specifically, it is not a separate
   category.
5. **`bbs-audit-what-actually-happens`** — the fear is real and nothing addresses
   it.
6. **`finding-a-clinical-supervisor-california`** — a member launched a WordPress
   directory to solve this. Partner, don't compete.

---

## The emotional register, which should govern the copy

> *"Can we talk about how lonely the prelicensed years actually are? You can't
> ask your supervisor everything because you're being evaluated. You can't ask
> your peers because everyone's pretending they have it together."*

That sentence is the argument for contextual in-app help in one line. **The
person who can't ask their supervisor whether something counts is the person
who needs the answer next to the field.** Not in a knowledge base, not in a
support ticket — right there, where nobody is watching them ask.

---

## Coverage and honest limits

**Queried so far:** `hours tracker`, `trackyourhours`, `supervisor sign`,
`hours tracking` — across two of four groups.

**Not yet queried:** the two remaining groups (1052481036084211,
3212462599059743), and roughly 30 further terms — `e-signature`, `37A-525`,
`experience verification`, `weekly log`, `audit`, `spreadsheet`, `Tevera`,
`license journey`, `sparkhours`, `supervision units`, `40 hour`, `pre-degree`,
`six year`, plus the non-tracker sitewide terms.

**This is a keyword sweep, not a census.** The chronological feed cannot be
paginated — confirmed twice, on 10 and 11 August. Facebook obfuscates post
timestamps with interleaved zero-width characters, so relative ages are
unreliable and are not recorded. Recurrence and engagement are trustworthy;
absence is not evidence.
