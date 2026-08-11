# Facebook group research corpus — schema and method

**File:** `_dev/data/fb-research.jsonl`
**Format:** JSON Lines — one self-describing JSON object per line, append-only.
**Started:** 11 August 2026.

This corpus is for the whole of `therapistsupport.org`, not just the hours
tracker. It records what California mental-health professionals actually ask,
argue about and complain about, so content and product decisions come from
observed demand rather than inference.

---

## Privacy rules — non-negotiable

**No individual is identifiable in this file.** Enforce on every write:

- **No names.** Not posters, not commenters, not people named inside a post.
- **No profile links, no post URLs, no member lists, no photos.**
- **No employer, school or clinic names** where they would identify one person.
  Institutions may be recorded only when the post is *about* the institution
  (e.g. an accreditation issue) and the poster is not identifiable from it.
- **Vendor and business names ARE recorded.** A company posting commercially, or
  being reviewed by name, is not a private individual.
- **Quotes are lightly redacted verbatim.** Preserve the person's own words —
  that is the point — but replace identifying nouns with `[vendor]`,
  `[school]`, `[employer]`. Never smooth the grammar or the feeling.
- **Dates are coarse.** Capture date only. Never a timestamp that, combined with
  a group, pins a specific post.

If a record cannot be written without identifying someone, don't write it.

---

## Record shape

```json
{
  "id": "P0001",
  "group": "ca-mft-therapists-supporters",
  "group_members": 12500,
  "captured": "2026-08-11",
  "query": "hours tracker",
  "type": "question",
  "themes": ["hours-tracking", "vendor-selection"],
  "topics": ["e-signature", "vendor-trust"],
  "track": ["amft"],
  "engagement": { "reactions": 1, "comments": 8 },
  "answered": "partial",
  "vendors": [
    { "name": "SparkHours", "sentiment": "negative", "reason": "no contactable company" }
  ],
  "quote": "verbatim, de-identified",
  "product_signal": "what this implies for the product",
  "content_opportunity": "slug-of-page-that-would-answer-this"
}
```

### Field definitions

| Field | Values / notes |
|---|---|
| `id` | `P####`, sequential, synthetic. **Not** a Facebook ID. |
| `group` | Slug. Never the numeric group ID — that plus a quote could locate a post. |
| `query` | The search term that surfaced it. Records *how* it was found, so coverage gaps are visible. |
| `type` | `question` · `vent` · `crisis` · `job` · `resource` · `promo` · `announcement` |
| `themes` | Broad buckets. Keep the vocabulary small and reuse it. |
| `topics` | Specific and freer. This is where the long tail lives. |
| `track` | `amft` · `asw` · `apcc` · `amft-trainee` · `prelicensed` · `licensed` · `supervisor` · `unspecified` |
| `engagement` | `reactions` and `comments` as integers. **This is the ranking signal** — it says what the profession actually argues about. |
| `answered` | `resolved` · `partial` · `unanswered` · `conflicting` · `n/a`. An unanswered high-engagement question is the highest-value content target there is. |
| `vendors` | Array. `sentiment`: `positive` · `negative` · `neutral` · `self-promo`. `reason` in the poster's terms. |
| `quote` | De-identified verbatim. Used for copy, never republished attributed. |
| `product_signal` | What this implies to build, or not build. |
| `content_opportunity` | Page slug that would answer it, or `null`. |

---

## Method, and its honest limits

**Collection is by group search, one query at a time**, reading what the page
renders. Two constraints shape everything here:

1. **The chronological feed does not paginate.** Facebook's lazy-loaded
   skeletons never resolve for automated reading — confirmed independently on
   10 Aug and again on 11 Aug 2026. There is no way to walk the feed in order.
2. **Automated scroll-and-harvest loops are blocked**, both by tooling and by
   Facebook's own defences (post timestamps are deliberately obfuscated with
   interleaved zero-width characters).

**So this is a keyword sweep, not a census.** It biases toward recurring topics
and away from one-off posts. For demand measurement that bias is acceptable and
arguably helpful — recurrence is the thing being measured.

**Coverage is tracked by the `query` field.** To find gaps, group by `query` and
see which terms have been run against which groups.

### Groups in scope

| Slug | Members | Character |
|---|---|---|
| `ca-mft-therapists-supporters` | 12.5K | Advocacy and job sharing. Heavy job/CE/promo noise; licensed and pre-licensed mixed. |
| `ca-amft-apcc-asw-registration-support` | — | Registration-focused. Highest concentration of hours and forms questions. |
| *(two further groups queued)* | — | 1052481036084211, 3212462599059743 |

---

## Working with it

```bash
# every hours-tracking record, ranked by comments
jq -c 'select(.themes|index("hours-tracking"))' fb-research.jsonl \
  | jq -s 'sort_by(-.engagement.comments)'

# unanswered questions — the content backlog, ranked
jq -c 'select(.answered=="unanswered" or .answered=="partial")' fb-research.jsonl

# every vendor mention and why
jq -c '.vendors[]? | {name, sentiment, reason}' fb-research.jsonl

# coverage: which queries have been run
jq -r '.query' fb-research.jsonl | sort -u
```

Convert to SQLite if it outgrows `jq`:

```bash
python3 -c "import json,sqlite3,sys; ..."   # trivial; JSONL → rows
```

**Do not convert to CSV as the primary store.** Quotes contain commas, quotation
marks and newlines; the corpus loses fidelity on the first round trip.

---

## Adding to it

Append lines. Never rewrite the file. Bump the `id` counter from the last line:

```bash
tail -1 fb-research.jsonl | jq -r .id
```

After each session, regenerate the digest (`fb-demand-index.md`) and write that
to the project. The digest is what future sessions read first; the corpus is
what they query when the digest isn't enough.
