# The rule for adding content to therapistsupport.org

Two things have to stay true every time a page is added, and neither of them
can depend on anyone remembering:

1. **The sitemap includes it.** Nobody maintains a list.
2. **It follows the SEO rules the rest of the site follows.** Publishing checks.

Both are now enforced by the build, not by discipline.

---

## The short version

```bash
python3 _dev/ship.py                     # build everything, in order, then verify
./_dev/publish.sh "what changed"         # commit and push
```

`ship.py` runs about twenty-five passes in a sequence that matters, ending with
`discovery.py`, which regenerates `sitemap.xml` from the pages that exist at the
moment it runs. Then it runs the two read-only checks. If anything fails it
stops there, because every pass after a failure would build on a half-finished
site.

`publish.sh` runs `discovery.py` and `seo_rules.py` again immediately before it
commits, so the sitemap cannot go stale and a new SEO regression cannot be
pushed even if `ship.py` was skipped.

---

## Why the sitemap is generated and not written

It used to be hand-written. When the site had 15 pages that was fine. At 59 it
listed 15 — every page added in between was invisible to search, including a
whole directory and 37 school pages. It also listed a redirect stub at priority
0.9, ranked above the page it redirected to.

`_dev/discovery.py` now derives the sitemap from the directory listing, with
`lastmod` from each file's own modification time. **A page cannot be forgotten,
because nobody is remembering.** Three pages are excluded on purpose and each
one carries its reason in the code: a redirect stub, a layout scratchpad, and a
visual mockup with no real numbers behind it.

If you add a page that should *not* be indexed, add it to `EXCLUDE` in
`discovery.py`. Two other files keep their own copy of that list — `seo_head.py`
and `seo_rules.py` — and both have a guard that tells you when the three have
drifted apart.

---

## The SEO rules, and how they are enforced

`_dev/seo_rules.py` reads every page and checks eighteen things. It is
read-only; it never edits a page.

It works against a **baseline**, in `_dev/_snap/seo_rules.json`. A fresh audit
of 163 pages returns a long list, most of it pre-existing and none of it caused
by whatever you are publishing right now — and a guard that blocks on all of
that gets switched off within a day. So the baseline records what is wrong
today, and only **new** findings fail.

```bash
python3 _dev/seo_rules.py            # what got worse since the baseline
python3 _dev/seo_rules.py --all      # everything, baseline included
python3 _dev/seo_rules.py --strict   # no baseline; every finding fails
python3 _dev/seo_rules.py --accept   # adopt the current state as the baseline
```

Run `--accept` after you have deliberately fixed or deliberately accepted
something. Never run it to make a red build go green.

### What it checks, and what each one cost when it went wrong here

| Rule | Why it is on the list |
|---|---|
| exactly one `h1` | Two h1s has always meant a builder emitted its hero into a page that already had one |
| title present, 15–68 chars, unique | 93 titles were over 68; the truncated part was the part that identified the page |
| description present, 70–168 chars, unique | 104 were over; same failure |
| canonical present | Four real pages had none |
| canonical on-host | The migration bug — a canonical naming the old GitHub host took the whole site out of the index |
| canonical names itself | A canonical naming a *different* page silently deindexes the page carrying it. `practice-simulator.html` was pointing at the homepage |
| `<html lang>` | One attribute; it is what says this is English |
| every internal link resolves | — |
| no extensionless relative href | `href="page"` with the `.html` outside the quotes renders as a link and 404s. It shipped on thirty links at once |
| in the sitemap, both directions | No page missing, no phantom URL |
| not an orphan | A page nothing links to is a page nothing crawls |
| JSON-LD parses | An unparseable block is worse than none, because it looks done |
| images have alt | — |
| American spellings | This site is for Californians, and the Board issues a *license* |

---

## The two passes that fix rather than report

- **`_dev/seo_head.py`** — adds a canonical and a `lang` to any published page
  missing one, derived from the path. It will not overwrite a canonical that
  already points somewhere else; that is an editorial decision, so it reports it
  instead.
- **`_dev/seo_meta.py`** — brings over-long titles and descriptions inside the
  length a search result shows. Never by truncating mid-sentence and never with
  an ellipsis: it drops a site suffix, drops a long parenthetical, or cuts at a
  boundary the author already placed. If none of those works it leaves the page
  alone and reports it, because a hard-truncated title is worse than a long one.

---

## Adding a page: the checklist

1. Write the builder in `_dev/`, or add the page by hand.
2. Emit, in the `<head>`: `<title>` (≤68), `<meta name="description">` (≤168),
   `<link rel="canonical">`, and the `ts:` meta the site's routers read
   (`ts:topic`, `ts:format`, `ts:question`, `ts:outcome`, `ts:number`,
   `ts:weight`, `ts:stale`).
3. Link to it from somewhere. If it belongs in the nav, add it to the right list
   in `_dev/restyle.py`. If nothing links to it, `seo_rules.py` will call it an
   orphan.
4. If you assemble the page from another page's chrome, **take that page's
   end-of-body scripts too.** The nav panel's binding lives after `</footer>`;
   a header slice alone ships a masthead where every button is dead, with no
   console error and no failing guard.
5. `python3 _dev/ship.py`
6. `./_dev/publish.sh "what changed"`

---

## The order in `ship.py`, and why it is an order

Each pass is idempotent and guarded on its own. None of them says what has to
run before it. Run them in the wrong order and nothing errors — you get a site
that is subtly wrong while every guard still says "clean", because each guard
checks its own pass and nothing checked the sequence.

    builders        write raw pages from data, carrying borrowed chrome
    structure       chrome, nav, cross-links, the blocks that carry meaning
                    footer_band inserts ABOVE the up-link;
                    footer_order later MOVES it down against the footer,
                    so it must run after footer_band and pixel_concepts
    floors          contrast, tap area, spacing - they read finished markup
    seo             canonical, lang, title and description lengths
    css             extract_css hoists shared <style> blocks; it must run
                    after every pass that emits one, and css_dedupe after it
    last            discovery.py - the sitemap, derived from what exists NOW.
                    Nothing may add or rename a page after this point
    verify          linkcheck and seo_rules. Read-only

---

## One habit worth more than any of the above

The recurring bug on this site has one shape, and it has appeared at least six
times: **the check and the change were looking at different things.**

- `node --check` passed on JSX that parsed and rendered nowhere.
- A guard asserted an attribute was present, and happily passed one that was
  present and wrong.
- A contrast pass measured a class that lives on two different backgrounds.
- A nav guard checked the markup and not the behaviour.
- A link guard looked only at hrefs already ending in `.html`, so thirty links
  missing their extension were invisible to it.
- A description was truncated by slicing the argument instead of the result, so
  the template's tail was welded onto a fragment.

So after any change: **open the page and confirm the specific thing you touched
actually appears.** A green guard is necessary and it is not sufficient.
