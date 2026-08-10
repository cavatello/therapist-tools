#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The In-short card stops repeating the headline it sits under.

REPORTED

  "why do u say same thing twice — h1 what gets therapist disciplined is
   listed twice"

Correct, and it is not one page. On the discipline hub the H1 reads *What
actually gets a California therapist disciplined* and the card directly beneath
it opens with *What actually gets a California therapist disciplined?* — the
same words, twice, in the first two lines of the page.

Measured across the site: **68 of the 167 pages carrying an In-short card have a
`<q>` that duplicates the `<h1>`.** Every one of the 48 discipline case pages,
every school page whose H1 is just the school's name, and the hub.

WHY IT HAPPENS

The card is built from `ts:question` and `ts:outcome`. That is the right source
— the question is the page's reason to exist, and it drives the questions index
and the hub cards too. But on a page whose H1 *is* the question, printing it
again adds nothing and costs the reader the first screen of the page.

WHAT THIS DOES

Drops the `<q>` when it is the same as the H1, and keeps the answer and the
figure. The card still reads correctly:

    IN SHORT
    Forty-eight real cases, the exact code section each was charged under,
    and what each one cost
    48 written up in full

Not deleted — dropped only on the pages where it repeats. On the ~99 pages
where the question genuinely differs from the headline, the card is unchanged.

The comparison is on normalised text: tags stripped, entities resolved,
punctuation and case discarded, and a substring match in either direction, so
that *Antioch University Los Angeles* matches an H1 of the same name and
*…disciplined* matches *…disciplined?*.

WHERE THE FIX SITS

In `pixel_concepts.py`, which writes the card, rather than in the meta of 68
pages. The meta is right; the rendering was.

Idempotent, guarded.
"""
import os, sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
P = "pixel_concepts.py"
s = open(P, encoding="utf-8").read()

HELPER = '''
def _plain(x):
    """Normalised for comparison only: no tags, no entities, no punctuation."""
    x = re.sub(r"<[^>]+>", " ", str(x))
    x = html.unescape(x)
    x = re.sub(r"[^a-z0-9 ]", " ", x.lower())
    return re.sub(r"\\s+", " ", x).strip()


def echoes_h1(q, page_html):
    """Does this question just say the H1 again?

    68 of the 167 pages with an In-short card did, including all 48 discipline
    case pages - the headline, then the same sentence with a question mark, in
    the first two lines. Substring either way, because an H1 of "Antioch
    University Los Angeles" and a question of the same words are the same
    problem as "...disciplined" and "...disciplined?".
    """
    m = re.search(r"<h1[^>]*>([\\s\\S]*?)</h1>", page_html or "")
    if not m:
        return False
    a, b = _plain(m.group(1)), _plain(q)
    if not a or not b:
        return False
    return a == b or a in b or b in a

'''

OLD = '''    # ---- 07, in short
    if q and out:
        fig = ('<span class="tsfig">%s</span>' % raw(num)) if num else ""
        top.append('<div class="tsshort"><p class="tsk">In short</p>'
                    "<q>%s</q><p class=\\"tsa\\">%s</p>%s</div>"
                    % (raw(q), raw(out), fig))'''

NEW = '''    # ---- 07, in short
    if q and out:
        fig = ('<span class="tsfig">%s</span>' % raw(num)) if num else ""
        # The question is dropped where it only repeats the headline the card
        # sits under. See echoes_h1() - this was 68 of 167 pages, and on the
        # discipline hub it put the same sentence in the page's first two
        # lines. The answer and the figure carry the card on their own.
        head = "" if echoes_h1(q, s) else "<q>%s</q>" % raw(q)
        top.append('<div class="tsshort"><p class="tsk">In short</p>'
                    "%s<p class=\\"tsa\\">%s</p>%s</div>"
                    % (head, raw(out), fig))'''

if s.count(OLD) != 1:
    sys.exit("patch_tsshort: the card block matched %d times, expected 1"
             % s.count(OLD))
s = s.replace(OLD, NEW, 1)

if "def echoes_h1(" not in s:
    anchor = "\ndef esc("
    if s.count(anchor) != 1:
        sys.exit("patch_tsshort: no single esc() to anchor the helper to")
    s = s.replace(anchor, "\n" + HELPER + "\ndef esc(", 1)

open(P, "w", encoding="utf-8").write(s)
print("pixel_concepts.py: the In-short card no longer repeats the H1")
