# Deep-research spec for California MFT program pages

You are researching ONE OR MORE California graduate programs that lead to MFT
licensure. The output is a JSON file per school, written to
`/home/claude/work/mftguide/depth/<slug>.json`.

The reader is a prospective student choosing where to spend two to three years
and $40,000–$120,000. They already know the program's name, units, length and
format — that is on the page. What they cannot get anywhere is **what it is
actually like, and what makes it different from the twelve others they are
looking at.**

## THE ONE RULE

**Nothing invented.** Every course code, course title, unit count, curriculum
sequence, cohort size and practicum detail must come from a page you actually
fetched, and you must record that URL. If you cannot find it, the field is
`null` and you say so in `gaps`. A plausible-sounding fabricated course
description is the worst possible failure here — worse than an empty section.

Do not paraphrase a course description so loosely that it becomes generic. If a
catalog says a course "uses the T-group method: an unstructured small group in
which members study their own interaction as it happens," that specificity is
the whole point. Keep it. Quote up to ~40 words verbatim where the wording
itself is the information, and mark it `"verbatim": true`.

## HOW TO RESEARCH

Work in this order. Do not stop at the marketing page.

1. **The program's own page** (given in your assignment). Read it fully.
2. **The academic catalog.** This is where the real substance is. Search
   `<school> academic catalog marriage family therapy course descriptions`,
   `<school> catalog MFT curriculum`, `site:catalog.<school>.edu`. Most schools
   publish a full course-description catalog; find it. This is the single
   highest-value source and the one that makes the page worth reading.
3. **The curriculum / plan of study / course sequence page** — the term-by-term
   grid. Often a PDF.
4. **The practicum / traineeship / field placement page.** Who finds the site,
   when it starts, how many hours, whether the school has affiliated clinics.
5. **The student handbook** (often PDF) — cohort size, sequence, requirements.
6. **Discussion and reviews:** Reddit (r/therapists, r/askatherapist,
   r/MFT, r/GradSchool, school-specific subs), Student Doctor Network,
   The GradCafe, Niche, GradReports, Reddit search via
   `site:reddit.com <school> MFT`. Also alumni blog posts and YouTube student
   vlogs if they are substantive.
7. **A freely-licensed photo**: search Wikimedia Commons for the campus or a
   named building. ONLY accept CC-BY, CC-BY-SA, CC0 or public domain. Record
   the direct file URL, the Commons page URL, the license string and the
   required attribution exactly. If there is no verifiable free image, set
   `photo: null` — do NOT hotlink a copyrighted university photo.

## OUTPUT SCHEMA

Write valid JSON. Every URL must be one you actually fetched or that a search
result surfaced with a matching title.

```json
{
  "institution": "<EXACT string from your assignment — must match byte-for-byte>",
  "character": [
    "Paragraph on what actually distinguishes this program. Concrete, not brochure language. Name the theoretical orientation, the clinic it runs, the population it trains you for, the thing that shows up in its course list and nowhere else.",
    "A second paragraph if there is a second real thing to say. Two to three paragraphs maximum. If the program is genuinely unremarkable — a solid, conventional CACREP-shaped curriculum with no distinctive commitment — SAY THAT plainly. That is useful information, not a failure."
  ],
  "orientation": "One short phrase for the theoretical center of gravity, e.g. 'Depth/Jungian', 'Systemic/structural family therapy', 'Integrative with a somatic emphasis', 'Christian integration', 'Generalist CBT-forward'. null if it is genuinely eclectic and says so.",
  "signature": [
    {
      "code": "MCP 5301",
      "title": "Exact course title",
      "units": "3",
      "desc": "The catalog description, quoted or tightly paraphrased. 25–60 words.",
      "verbatim": true,
      "why": "One or two sentences: what this course tells a prospective student about the program. This is your analysis, and it should be specific — 'this is one of very few CA programs requiring a full semester of experiential group process' beats 'shows a focus on groups'.",
      "src": "https://..."
    }
  ],
  "curriculum": {
    "note": "One sentence on how the sequence works (cohort, lockstep, part-time option, summers).",
    "total_units": "60",
    "terms": [
      {"label": "Year 1 — Fall", "courses": ["MCP 5301 Foundations of Counseling (3)", "..."]}
    ],
    "src": "https://..."
  },
  "practicum": {
    "starts": "Second year, fall term",
    "hours": "Minimum 300 face-to-face client hours across three semesters",
    "who_places": "program-placed | student-finds | mixed",
    "clinic": "Name of any in-house training clinic, or null",
    "detail": "Two to four sentences on how it actually works.",
    "src": "https://..."
  },
  "admissions": {
    "cohort_size": "About 40 per year, two cohorts",
    "gre": "Not required",
    "prereqs": "...",
    "deadline": "...",
    "src": "https://..."
  },
  "voices": [
    {
      "text": "A short paraphrase or <=35-word quote of what someone actually said about the experience.",
      "who": "Reddit, r/therapists, 2024",
      "sentiment": "positive | negative | mixed | info",
      "url": "https://..."
    }
  ],
  "photo": {
    "file": "https://upload.wikimedia.org/...",
    "page": "https://commons.wikimedia.org/wiki/File:...",
    "license": "CC BY-SA 4.0",
    "credit": "Photo by X, via Wikimedia Commons",
    "caption": "What the picture shows"
  },
  "gaps": ["Anything you looked for and could not find, named plainly."],
  "sources": [{"label": "Academic catalog 2026–27", "url": "https://..."}]
}
```

## QUALITY BAR

- 3–6 `signature` courses. Pick the ones that are DISTINCTIVE, not the ones
  every program has. Every CA program teaches Law and Ethics; almost none
  teaches a semester-long unstructured T-group. Lead with what is rare.
- `curriculum.terms` should cover the whole program if the sequence is
  published. If only a course list exists with no sequence, use a single term
  labelled "Required coursework" and say so in `curriculum.note`.
- `voices`: 2–6. Include critical ones. If nothing credible exists, `[]`.
- `character` must not be reusable for another school. If you could paste it
  onto a different program's page unchanged, it is not specific enough.
- Prefer the 2026–27 catalog; note the year you used.

Write the file, then reply with ONE line per school:
`<institution> — <n> courses, <n> terms, <n> voices, photo: yes/no, gaps: <n>`
