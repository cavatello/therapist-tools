#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Turn the hours ladder into something worth looking at.

The user's note, looking at the job advisor: "this page should really show some
cool visuals like a video game."

WHAT IS ALREADY THERE. Section 05 computes four gates - calendar weeks, total
hours, direct clinical hours, and relational hours - works out which one is
actually holding the licence date, and renders each as a labelled progress bar
with a projected date underneath. The arithmetic is the good part and it is
already right. What it looked like was a form summary.

WHY THIS IS A STYLESHEET AND NOT A REWRITE. The engine that produces those
gates is 867 lines and it is the thing the page exists for. A visual pass that
touches it can silently change a date. This pass adds CSS and one small
ornamental script; it reads no state, computes nothing, and cannot move a
number. If every rule here were deleted the page would still be correct.

THE FOUR MOVES.

  1. THE BOARD IS DARK. The gates sit on a deep pine panel with a pixel border
     rather than on paper. It reads as an instrument rather than as a printout,
     and it borrows the palette the site already uses for its own chrome, so it
     is a game console rather than a different website.

  2. THE BARS ARE SEGMENTED. A smooth fill says "roughly here". Twenty discrete
     blocks say "you have eleven of twenty", which is how someone actually
     holds a number in their head - and it is the visual grammar of every
     progress meter anyone has ever seen in a game.

  3. THE BLOCKING GATE IS THE BOSS. The engine already marks one gate as the
     one holding the date. It gets amber, a pulse, and a label saying so. That
     is the single most useful fact on the page and it was previously a
     slightly different background colour.

  4. THE DATE IS A PLAQUE. The projected licence date becomes the reward at the
     end of the board rather than another card.

Accessibility: the pulse is disabled under prefers-reduced-motion, the amber on
deep pine is well past AA, and nothing here conveys information by colour alone
- every state is also carried in text the engine already writes.

Idempotent. Style-only.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
PAGE = "associate-mft-job-advisor.html"
MARK = "/* _dev/quest_hud.py */"

CSS = """
/* ---------------------------------------------------------------- the board
   Wrapping the existing .gates grid rather than replacing it, so the engine's
   markup is untouched and every rule below is an override. */
#plan .gates{
  background:linear-gradient(160deg,#12281F 0%,#17352A 55%,#1B4536 100%);
  border:1px solid #2C6350;border-radius:18px;padding:18px;gap:10px;
  box-shadow:inset 0 1px 0 rgba(255,255,255,.06),0 14px 34px rgba(18,40,31,.22);
  position:relative}
#plan .gates::before{
  content:"FOUR GATES \\00B7 ALL FOUR MUST CLOSE";
  display:block;font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:9.4px;
  letter-spacing:.18em;color:#7FB79B;margin:2px 2px 13px}

/* ------------------------------------------------------------- each quest */
#plan .gate{
  background:rgba(255,255,255,.045);border:1px solid rgba(127,183,155,.28);
  border-radius:12px;padding:14px 16px 15px;color:#E7F1EB;position:relative;
  transition:border-color .25s ease}
#plan .gate:hover{border-color:rgba(127,183,155,.5)}
#plan .gatehead{display:flex;justify-content:space-between;align-items:baseline;
  gap:12px;flex-wrap:wrap}
#plan .gatehead b{font-family:Fraunces,Georgia,serif;font-size:16.5px;color:#fff;
  letter-spacing:-.01em}
#plan .gatehead .num{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:12.2px;
  color:#A9CFBC;letter-spacing:.02em;white-space:nowrap}

/* --------------------------------------------------- the segmented meter
   Twenty blocks, drawn with a repeating gradient over the fill rather than as
   twenty elements, so the engine keeps writing a single width percentage and
   the bar still animates when it changes. */
#plan .gtrack{height:20px;background:rgba(0,0,0,.34);border:1px solid rgba(127,183,155,.3);
  border-radius:6px;overflow:hidden;position:relative;margin-top:11px}
#plan .gtrack::after{
  content:"";position:absolute;inset:0;pointer-events:none;
  background:repeating-linear-gradient(90deg,
    rgba(0,0,0,0) 0,rgba(0,0,0,0) calc(5% - 2px),
    rgba(18,40,31,.85) calc(5% - 2px),rgba(18,40,31,.85) 5%)}
#plan .gtrack i{background:linear-gradient(90deg,#3F9577,#5EC49B);border-radius:0;
  box-shadow:0 0 14px rgba(94,196,155,.45)}

/* ------------------------------------------------------------- the boss gate
   The engine already decides which gate is holding the date. Previously that
   was a slightly different background; now it is the loudest thing on screen,
   because it is the most useful fact on the page. */
#plan .gate.block{background:rgba(246,197,96,.1);border-color:rgba(246,197,96,.6)}
#plan .gate.block .gtrack i{background:linear-gradient(90deg,#C98B4B,#F6C560);
  box-shadow:0 0 16px rgba(246,197,96,.5)}
#plan .gate.block .gatehead b{color:#F6C560}
#plan .gate.block::after{
  content:"HOLDING YOUR DATE";position:absolute;top:-9px;right:14px;
  font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:8.6px;letter-spacing:.14em;
  background:#F6C560;color:#3A2A08;padding:3px 9px;border-radius:20px;
  animation:qpulse 2.4s ease-in-out infinite}
@keyframes qpulse{0%,100%{opacity:1}50%{opacity:.62}}
@media (prefers-reduced-motion:reduce){
  #plan .gate.block::after{animation:none}
  #plan .gtrack i{transition:none}
}

/* the percentage chip, added by the script below */
#plan .qpc{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:10.4px;
  letter-spacing:.06em;background:rgba(0,0,0,.3);color:#A9CFBC;border-radius:20px;
  padding:2px 8px;margin-left:8px}
#plan .gate.block .qpc{background:rgba(246,197,96,.18);color:#F6C560}
#plan .gate.done .qpc{background:rgba(94,196,155,.18);color:#7FDDB6}

/* ---------------------------------------------------------------- the text */
#plan .gate p{color:#B7CFC3;font-size:12px;line-height:1.62}
#plan .gate .eta{color:#DCEAE2;font-size:12.4px}
#plan .gate .eta b{color:#F6C560}
#plan .gate.done .eta b{color:#7FDDB6}

/* ------------------------------------------------------------- the plaque */
#plan .finish{
  margin-top:14px;background:linear-gradient(150deg,#1B4536,#123026);
  border:1px solid rgba(246,197,96,.45);border-radius:18px;padding:22px 24px;
  position:relative;overflow:hidden}
#plan .finish::before{
  content:"";position:absolute;top:-40%;right:-8%;width:220px;height:220px;
  background:radial-gradient(circle,rgba(246,197,96,.18),transparent 68%);
  pointer-events:none}
#plan .finish em{color:#A9CFBC;font-size:9.4px;letter-spacing:.16em}
#plan .finish b{color:#F6C560;font-size:clamp(27px,4.2vw,42px)}
#plan .finish p{color:#C6DCD1;font-size:12.9px}
#plan .finish p b{color:#F6C560;font-size:inherit}

@media (max-width:560px){
  #plan .gates{padding:14px;border-radius:14px}
  #plan .gatehead .num{font-size:11.2px}
  #plan .gate.block::after{right:10px;font-size:8px}
}
"""

JS = """
(function(){
  /* Ornament only. Reads the width the engine already wrote onto each bar and
     shows it as a number; marks a finished gate so the palette can respond.
     It computes nothing and, if it throws, the page is exactly as correct as
     it was - which is why it is wrapped and why it never writes to state. */
  var plan = document.getElementById('plan');
  if (!plan || !('MutationObserver' in window)) return;
  function decorate(){
    try {
      plan.querySelectorAll('.gate').forEach(function(g){
        var fill = g.querySelector('.gtrack i');
        if (!fill) return;
        var pct = Math.max(0, Math.min(100, parseFloat(fill.style.width) || 0));
        g.classList.toggle('done', pct >= 100);
        var head = g.querySelector('.gatehead .num');
        if (head && !head.querySelector('.qpc')){
          var chip = document.createElement('span');
          chip.className = 'qpc';
          chip.textContent = Math.round(pct) + '%';
          head.appendChild(chip);
        } else if (head) {
          head.querySelector('.qpc').textContent = Math.round(pct) + '%';
        }
      });
    } catch (e) { /* ornament only - never break the page over it */ }
  }
  /* The observer must not watch what decorate() writes. The first version used
     {childList:true, subtree:true} and decorate() appends a chip element to a
     descendant - so every run triggered another run and the page hung hard
     enough to kill the browser tab on load. Nothing in a screenshot would have
     shown this; the tab simply never finished.

     Two defences, because one is not enough on a page whose engine also
     rewrites #plan wholesale:
       - observe childList on #plan ONLY, since drawHours replaces its innerHTML
         and that is the single event worth reacting to;
       - a re-entrancy flag, so even a future subtree observer cannot recurse. */
  var busy = false;
  var mo = new MutationObserver(function(){
    if (busy) return;
    busy = true;
    try { decorate(); } finally { busy = false; }
  });
  mo.observe(plan, {childList:true});
  decorate();
})();
"""


def main():
    path = os.path.join(SITE, PAGE)
    if not os.path.exists(path):
        sys.exit("quest_hud: %s not found" % PAGE)
    s = open(path, encoding="utf-8").read()

    # the engine must still be producing the markup this pass styles
    for needed in ('id="plan"', "gtrack", "gatehead", 'class="gate'):
        if needed not in s:
            sys.exit("quest_hud: the hours section no longer emits %r - "
                     "restyling it blind would be worse than leaving it" % needed)

    s = re.sub(r"\n?<style>" + re.escape(MARK) + r"[\s\S]*?/\* end quest \*/</style>\n?",
               "", s)
    s = re.sub(r"\n?<script>/\* quest \*/[\s\S]*?/\* end quest \*/</script>\n?", "", s)
    s = s.replace("</body>",
                  "\n<style>" + MARK + CSS + "/* end quest */</style>"
                  "\n<script>/* quest */" + JS + "/* end quest */</script>\n</body>", 1)
    open(path, "w", encoding="utf-8").write(s)
    print("%-44s hours ladder restyled as a quest board" % PAGE)

    # ---- guards
    s = open(path, encoding="utf-8").read()
    bad = 0
    if s.count(MARK) != 1:
        print("GUARD: %d stylesheets" % s.count(MARK)); bad += 1
    if s.count("/* quest */") != 1:
        print("GUARD: %d scripts" % s.count("/* quest */")); bad += 1
    if re.search(r"observe\([^)]*subtree\s*:\s*true", s):
        print("GUARD: the observer watches a subtree it writes into"); bad += 1
    # this pass must not have touched the engine
    if "drawHours" not in s:
        print("GUARD: drawHours is gone"); bad += 1
    for fig in ("1,750", "3,000", "104"):
        if fig not in s:
            print("GUARD: figure %s vanished" % fig); bad += 1
    if s.count("<h1") != 1:
        print("GUARD: %d h1" % s.count("<h1")); bad += 1
    # every rule must be scoped to #plan, so nothing leaks into the rest of the page
    # Strip comments before reading selectors. The first version matched the
    # text preceding each "{" and so treated every banner comment as a
    # selector, failing seven times on its own documentation.
    css_only = re.sub(r"/\*[\s\S]*?\*/", "", CSS)
    # At-rules are containers, not selectors - @media and @keyframes carry no
    # specificity of their own and their contents are checked on the next pass
    # of the same loop. The "@" was being eaten by the [^{}@;] class, which is
    # how "@keyframes qpulse" arrived here looking like an element selector.
    css_only = re.sub(r"@(media|keyframes|supports)[^{]*\{", "{", css_only)
    for m in re.finditer(r"([^{}@;]+)\{", css_only):
        parts = m.group(1).strip().splitlines()
        sel = parts[-1].strip() if parts else ""
        if not sel or sel.startswith(("#plan", "from", "to")) \
           or re.match(r"^[\d.,%\s]+$", sel):
            continue
        print("GUARD: unscoped selector %r" % sel[:44]); bad += 1
    if bad:
        sys.exit("quest_hud: %d guard failure(s)" % bad)
    print("guards clean")


if __name__ == "__main__":
    main()
