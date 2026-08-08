import io, sys

p = sys.argv[1]
s = io.open(p, encoding="utf-8").read()

# THE LEGEND WAS UNREADABLE, AND IT WAS A MARKUP CHOICE, NOT A STYLE ONE.
#
# Each row was a single <p> with the badge as the first inline child, so the
# pill sat ON the baseline of the sentence it labelled and the sentence started
# hard against its right edge with no gap. At 2000px the badge and the text
# visually merged into one run. Pills are objects, not words: they need their
# own column.
a = '''<div class="tblegend">
<p><span class="tsbadge full">Verified to source</span>Every figure was
re-checked against the statute, schedule or filing it cites. These pages cite
three or more primary sources &mdash; the Board, the IRS, CMS, the Legislature
&mdash; rather than somebody&rsquo;s summary of them.</p>
<p><span class="tsbadge part">Figures checked, narrative not re-read</span>The
numbers are current. The surrounding argument has not been reviewed since it
was written.</p>
<p><span class="tsbadge thin">Published sources only</span>Built from what an
institution publishes about itself. Nothing on the page is independently
verified, and where the institution publishes nothing the page says so rather
than filling the gap.</p>
<p><span class="tsbadge gap">Known gap</span>Something on the page could not be
established. It is named, in full, under &ldquo;What I could not establish&rdquo;.</p>
</div>'''
b = '''<div class="tblegend">
<div><span class="tsbadge full">Verified to source</span><p>Every figure was
re-checked against the statute, schedule or filing it cites. These pages cite
three or more primary sources &mdash; the Board, the IRS, CMS, the Legislature
&mdash; rather than somebody&rsquo;s summary of them.</p></div>
<div><span class="tsbadge part">Figures checked, narrative not re-read</span>
<p>The numbers are current. The surrounding argument has not been reviewed
since it was written.</p></div>
<div><span class="tsbadge thin">Published sources only</span><p>Built from what
an institution publishes about itself. Nothing on the page is independently
verified, and where the institution publishes nothing the page says so rather
than filling the gap.</p></div>
<div><span class="tsbadge gap">Known gap</span><p>Something on the page could
not be established. It is named, in full, under &ldquo;What I could not
establish&rdquo;.</p></div>
</div>'''
assert a in s, "legend markup"
s = s.replace(a, b, 1)

# THE BADGE'S EXPLANATION WAS STILL UNREADABLE ON DARK HEROES.
#
# The previous fix gave .tsdepth a card of its own "when it is first" -
# `.tsdepth:first-child`. That is a position test, and on about.html the block
# is preceded by the hero's standfirst, so .tsdepth is NOT the first child of
# its parent: the rule never matched, the background stayed transparent, and
# #5A5647 body grey printed on a dark green band.
#
# Position is the wrong thing to test. What actually decides whether the badge
# needs its own background is whether it is INSIDE the meta card, and that is a
# containment question. So the default is a card, and the meta card's copy is
# the exception - which is also the version that cannot be broken by adding a
# sibling above it.
a = """.tsdepth{margin:11px 0 0;padding:10px 0 0;border-top:2px dashed #D9D0BA;
  background:transparent}
.tsdepth:first-child{margin:0;padding:0;border-top:none;background:#FBF9F3;
  border:2px solid #16211B;border-radius:12px;box-shadow:3px 3px 0 #16211B;
  padding:12px 15px}"""
b = """/* Standing on its own, it carries its own background - a hero band may be any
   colour and this text is fixed. */
.tsdepth{margin:14px 0 0;background:#FBF9F3;border:2px solid #16211B;
  border-radius:12px;box-shadow:3px 3px 0 #16211B;padding:12px 15px}
/* Inside the meta card it is a section of that card, not a card of its own. */
.tsmeta .tsdepth{margin:11px 0 0;padding:10px 0 0;background:transparent;
  border:none;border-radius:0;box-shadow:none;
  border-top:2px dashed #D9D0BA}"""
assert a in s, "tsdepth"
s = s.replace(a, b, 1)

a = """@media (max-width:620px){
  .tsmeta .tsrow{gap:4px 14px}"""
b = """/* The legend on about.html. Two columns, badge and meaning, so the pill is
   never on the same baseline as the sentence it labels. */
.tblegend>div{display:grid;grid-template-columns:210px minmax(0,1fr);
  gap:6px 18px;align-items:start;padding:11px 0;border-top:2px dashed #D9D0BA}
.tblegend>div:first-child{border-top:none}
.tblegend .tsbadge{margin:1px 0 0;justify-self:start}
.tblegend p{margin:0;font-size:13.6px;line-height:1.6;color:#3A3529;max-width:62ch}
@media (max-width:760px){
  .tblegend>div{grid-template-columns:minmax(0,1fr);gap:8px}
}
@media (max-width:620px){
  .tsmeta .tsrow{gap:4px 14px}"""
assert a in s, "legend css"
s = s.replace(a, b, 1)

io.open(p, "w", encoding="utf-8").write(s)
print("patched")
