#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Measure how the calculators are actually used, without collecting a value.

THE GAP THIS FILLS

`_dev/analytics.py` puts GA4 on all 166 pages and `_dev/analytics_events.py`
instruments the six forms. Between them they answer "did anyone arrive" and
"did anyone subscribe".

Nothing answers the question the site is actually for. There are seven
calculators carrying about 130 inputs between them, and not one of them emitted
a single event. GA4 could tell you that practice-simulator.html was viewed 400
times. It could not tell you whether anybody typed anything into it, which
field they gave up on, or whether they ever saw a result. A tool site with no
tool instrumentation is measuring its brochure and calling it a product.

THE PRIVACY LINE, WHICH IS THE WHOLE DESIGN CONSTRAINT

The site tells readers, in print: "No account and no database. Nothing you type
is sent anywhere." That is a promise, and it is a large part of why a therapist
will put their real income into a page on the open web.

So this pass sends **field names, never field values**. It records that
`i-clients` was edited. It does not record that it was set to 18. There is a
guard at the bottom that reads the emitted JavaScript and fails the build if it
finds any expression that could put a form value into an event payload - which
is the only way to keep this true through future edits, because the mistake
would be one word long and completely invisible in the reports.

Concretely, what leaves the browser:

    tool_start      which tool, and which field was touched first
    tool_field      which field was edited (once per field, capped at 25)
    tool_result     a result appeared, and how many ms after the first input
    tool_section    a <details> block was opened, and which one
    tool_share      the reader copied a link, printed, or emailed a setup
    tool_depth      on leaving: fields touched, active seconds, reached result

WHY tool_depth IS THE IMPORTANT ONE

The others are counts. `tool_depth` is the shape of a session: it carries
whether the reader reached a result, so the ratio of "started" to "reached a
result" becomes a funnel, and the abandoned sessions carry the number of fields
they managed before they stopped. That is the number that tells you a tool is
too long.

ACTIVE TIME, NOT WALL TIME

GA4's own engagement time counts a tab that is open behind another tab. This
counts seconds where the page was visible AND the reader interacted within the
previous 30 seconds, which is the only version of "time on tool" worth having.

Sent on `visibilitychange` -> hidden rather than on `unload`, because `unload`
does not fire reliably on mobile Safari, which is where a large share of these
readers are.

Idempotent, guarded. Run after analytics.py, in the STRUCTURE stage.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training")
MARK = "/* _dev/tool_analytics.py */"

# The pages that are tools. Instrumenting every page would emit tool_start on an
# article the moment somebody clicked the newsletter box.
TOOLS = {
    "practice-simulator.html": "practice-simulator",
    "therapist-tax-strategy-california.html": "tax-strategy",
    "grow-your-therapy-practice.html": "grow-practice",
    "associate-mft-job-advisor.html": "job-advisor",
    "amft-3000-hours-california.html": "hours-3000",
    "therapist-cost-of-living-california.html": "cost-of-living",
    "therapist-working-remotely-california.html": "working-remotely",
    "calculators.html": "calculator-index",
}

# The index page lists the calculators; it does not compute anything, so it has
# no result node and must not be held to the guard that every tool has one.
NO_RESULT = {"calculators.html"}

JS = """<script>%(mark)s
(function(){
  var TOOL = %(tool)s;
  if (!TOOL) return;

  // ---------------------------------------------------------------- send
  // Mirrors the queueing in _dev/analytics_events.py: if gtag has not loaded,
  // or an extension has blocked it, push to dataLayer so a blocked loader
  // costs the event rather than throwing inside a change handler.
  function send(name, params){
    try {
      params = params || {};
      params.tool = TOOL;
      window.dataLayer = window.dataLayer || [];
      if (typeof window.gtag === 'function') { window.gtag('event', name, params); }
      else { window.dataLayer.push(['event', name, params]); }
    } catch (e) {}
  }

  // ------------------------------------------------------------- identity
  // A field is identified by its id with the builders' "i-" prefix removed.
  // This is a NAME. There is no path in this file from a value to a payload,
  // and the build guard enforces that.
  function fieldName(el){
    var id = el.id || el.name || '';
    return id.replace(/^i-/, '').slice(0, 40) || (el.type || el.tagName).toLowerCase();
  }

  // The newsletter and contact forms are already measured by
  // _dev/analytics_events.py. Counting them here too would inflate every tool's
  // field count by whatever the footer happens to contain.
  function isToolField(el){
    if (!el || !el.tagName) return false;
    if (!/^(INPUT|SELECT|TEXTAREA)$/.test(el.tagName)) return false;
    if (el.type === 'submit' || el.type === 'button' || el.type === 'hidden') return false;
    if (el.closest('form')) return false;
    return true;
  }

  // ---------------------------------------------------------------- state
  var started = false, startedAt = 0, resulted = false;
  var touched = Object.create(null), touchedCount = 0, sentFields = 0;
  var activeMs = 0, lastTick = 0, lastInteract = 0, visible = !document.hidden;

  var FIELD_CAP = 25;          // GA4 quotas, and the tail is not informative
  var IDLE_MS = 30000;         // interaction older than this is not "active"

  function now(){ return Date.now(); }

  function tick(){
    var t = now();
    if (lastTick && visible && (t - lastInteract) < IDLE_MS) activeMs += (t - lastTick);
    lastTick = t;
  }
  setInterval(tick, 1000);

  function interacted(){ lastInteract = now(); if (!lastTick) lastTick = now(); }

  // --------------------------------------------------------------- events
  function onField(el){
    interacted();
    var name = fieldName(el);
    if (!started){
      started = true; startedAt = now();
      send('tool_start', {first_field: name});
    }
    if (!touched[name]){
      touched[name] = 1; touchedCount++;
      if (sentFields < FIELD_CAP){ sentFields++; send('tool_field', {field: name, seq: touchedCount}); }
    }
  }

  document.addEventListener('change', function(e){
    if (isToolField(e.target)) onField(e.target);
  }, true);

  // `input` fires per keystroke. It is used only to mark the session active and
  // to catch the first touch of a field the reader never blurs - the per-field
  // event still goes out once, from the dedupe above.
  var inputTimer = null;
  document.addEventListener('input', function(e){
    if (!isToolField(e.target)) return;
    var el = e.target;
    interacted();
    clearTimeout(inputTimer);
    inputTimer = setTimeout(function(){ onField(el); }, 700);
  }, true);

  // --------------------------------------------------------------- result
  // A result is "the reader got an answer". Detected by watching the output
  // nodes for text that is neither empty nor a zero placeholder, which is what
  // every one of these tools renders before anything is entered.
  var OUT = %(outsel)s;
  function looksLikeAnswer(t){
    t = (t || '').trim();
    if (!t) return false;
    if (/^[\\s$0.,\\-—–%%]*$/.test(t)) return false;   // $0, 0, -, blank
    return /\\d/.test(t);
  }
  function checkResult(){
    if (resulted || !started) return;
    var nodes = document.querySelectorAll(OUT);
    for (var i = 0; i < nodes.length; i++){
      if (looksLikeAnswer(nodes[i].textContent)){
        resulted = true;
        send('tool_result', {ms_to_result: Math.max(0, now() - startedAt)});
        return;
      }
    }
  }
  if (window.MutationObserver){
    var mo = new MutationObserver(function(){ checkResult(); });
    try { mo.observe(document.body, {subtree: true, childList: true, characterData: true}); }
    catch (e) {}
  }

  // -------------------------------------------------------------- sections
  document.addEventListener('toggle', function(e){
    var d = e.target;
    if (!d || d.tagName !== 'DETAILS' || !d.open) return;
    var s = d.querySelector('summary');
    interacted();
    send('tool_section', {section: ((s && s.textContent) || '').trim().slice(0, 60)});
  }, true);

  // ---------------------------------------------------------------- share
  document.addEventListener('click', function(e){
    var a = e.target.closest && e.target.closest('a, button');
    if (!a) return;
    var label = ((a.textContent || '') + ' ' + (a.className || '')).toLowerCase();
    var how = null;
    if (/copy/.test(label)) how = 'copy_link';
    else if (/print/.test(label)) how = 'print';
    else if (/email|mailto/.test(label) || (a.href || '').indexOf('mailto:') === 0) how = 'email';
    else if (/reset/.test(label)) how = 'reset';
    if (how){ interacted(); send('tool_share', {method: how}); }
  }, true);

  // ----------------------------------------------------------- the summary
  // One event that carries the shape of the visit. Sent when the page is
  // hidden, not on unload - unload does not fire reliably on mobile Safari,
  // which is a large share of this audience.
  var summarySent = false;
  function summary(){
    if (summarySent || !started) return;
    summarySent = true;
    tick();
    send('tool_depth', {
      fields_touched: touchedCount,
      active_seconds: Math.round(activeMs / 1000),
      reached_result: resulted ? 'yes' : 'no'
    });
  }
  document.addEventListener('visibilitychange', function(){
    visible = !document.hidden;
    if (document.hidden) summary(); else { lastTick = now(); }
  });
  window.addEventListener('pagehide', summary);
})();
</script>"""


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return out


def out_selector(s):
    """The result nodes on this page, as a CSS selector.

    Read off the page rather than configured, because the seven tools were
    written by different builders and use different id conventions. Anything
    that looks like an output gets watched; a false positive costs one early
    tool_result, a false negative costs the whole funnel."""
    ids = set(re.findall(r'id="([a-zA-Z0-9_-]*'
                         r'(?:out|net|total|res|sum|verdict|answer|month|year'
                         r'|plan|gates|week|note|next)'
                         r'[a-zA-Z0-9_-]*)"', s, re.I))
    ids = {i for i in ids if not i.startswith(("i-", "ft-", "nav"))}
    sels = ["#" + i for i in sorted(ids)]
    # The class convention was the thing the first version missed. `.num` and
    # `.verdict` are how every one of these builders renders a computed figure,
    # and three tools watched ZERO nodes because the selector only looked at
    # ids. A tool that watches nothing still emits tool_start and tool_field,
    # so the funnel looked fine and the result step was simply always zero -
    # the same shape of bug as every other one in this project's history: the
    # check and the thing being checked were looking at different places.
    sels += [".num", ".verdict", ".cnum", ".tcnum",
             ".out", ".result", "[data-out]", "output"]
    return ", ".join(sels)


def main():
    print("tool instrumentation, behaviour only - no field VALUE is ever sent:")
    written = 0
    for rel in pages():
        base = os.path.basename(rel)
        p = os.path.join(SITE, rel)
        s = open(p, encoding="utf-8").read()
        if "sitenav" not in s:
            continue
        orig = s
        s = re.sub(r"\n?<script>" + re.escape(MARK) + r"[\s\S]*?</script>\n?", "", s)

        if base in TOOLS:
            js = JS % {"mark": MARK,
                       "tool": '"%s"' % TOOLS[base],
                       "outsel": '"%s"' % out_selector(s)}
            i = s.lower().rfind("</body>")
            if i < 0:
                continue
            s = s[:i] + js + "\n" + s[i:]
            print("  %-46s %d output node(s) watched"
                  % (base, out_selector(s).count("#")))

        if s != orig:
            open(p, "w", encoding="utf-8").write(s)
            written += 1
    print("\n%d page(s) written, %d of them tools" % (written, len(TOOLS)))

    # ------------------------------------------------------------- guards
    bad = 0
    live = [rel for rel in pages() if os.path.basename(rel) in TOOLS]
    for rel in live:
        s = open(os.path.join(SITE, rel), encoding="utf-8").read()
        if s.count(MARK) != 1:
            print("GUARD %s: %d copies" % (rel, s.count(MARK)))
            bad += 1
        if "gtag/js?id=" not in s:
            print("GUARD %s: no gtag on the page, so nothing can send" % rel)
            bad += 1
    for rel in pages():
        base = os.path.basename(rel)
        s = open(os.path.join(SITE, rel), encoding="utf-8").read()
        if base not in TOOLS and MARK in s:
            print("GUARD %s: instrumented but not a tool" % rel)
            bad += 1
        # A tool that watches no output node can never emit tool_result. It
        # would still emit tool_start and tool_field, so the reports would look
        # populated and the funnel would silently read 0% for that tool for as
        # long as nobody checked. Three tools shipped exactly that.
        if base in TOOLS and base not in NO_RESULT:
            m = re.search(r'var OUT = "([^"]*)"', s)
            watched = len([x for x in (m.group(1).split(",") if m else [])
                           if x.strip().startswith("#")])
            if watched == 0:
                print("GUARD %s: 0 output nodes watched - tool_result can never "
                      "fire, so this tool would report a 0%% completion rate "
                      "forever" % rel)
                bad += 1

    # THE GUARD THIS PASS EXISTS FOR.
    #
    # The site promises "Nothing you type is sent anywhere". Breaking that would
    # take one word - `el.value` instead of `el.id` - and it would look
    # completely normal in the reports, because a number in a chart does not
    # announce where it came from. So the emitted JavaScript is read back and
    # any expression that could carry a field value into a payload fails the
    # build.
    js_only = JS
    for pat, why in (
        (r"\.value\b", "a field's value"),
        (r"\bvalueAsNumber\b", "a field's numeric value"),
        (r"\bFormData\b", "the contents of a form"),
        (r"\bcheckState\b|\.checked\b", "a checkbox state"),
        (r"location\.hash", "the share hash, which encodes every entered figure"),
        (r"\.search\b", "the query string, which can carry entered figures"),
    ):
        if re.search(pat, js_only):
            print("GUARD: the tracking script reads %s. The site promises "
                  "\"Nothing you type is sent anywhere\"." % why)
            bad += 1

    # And the events must be the ones documented, so a stray name cannot appear
    # in GA4 without also appearing in this file's docstring.
    names = set(re.findall(r"send\('([a-z_]+)'", js_only))
    expected = {"tool_start", "tool_field", "tool_result", "tool_section",
                "tool_share", "tool_depth"}
    if names != expected:
        print("GUARD: events emitted %s, documented %s"
              % (sorted(names), sorted(expected)))
        bad += 1
    for n in names:
        if len(n) > 40:
            print("GUARD: %s exceeds GA4's 40-character event name limit" % n)
            bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean - %d event(s): %s" % (len(names), ", ".join(sorted(names))))
    print("no expression in the emitted script can carry a typed value")


if __name__ == "__main__":
    main()
