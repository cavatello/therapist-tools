#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""See the site break, instead of hearing about it.

WHAT WAS THERE BEFORE: nothing. No `window.onerror`, no `unhandledrejection`,
no resource-error handler, on any of 166 pages. A JavaScript error on the
practice simulator - the kind that leaves the numbers frozen at zero while the
page looks completely normal - produced exactly one signal: a reader who left.
In the reports that is indistinguishable from a reader who was not interested.

That matters more here than on most sites, because this one has already shipped
the specific failure it describes in its own notes: a widget that silently did
not initialise "looks exactly like a widget that has not been built yet". There
was no way to find out except by looking.

WHAT IT SENDS

  js_error          an uncaught exception: message, file, line, and the page
  promise_error     an unhandled rejection - the shape a failed fetch takes
  resource_error    a script, stylesheet or image that did not load
  rage_click        four clicks on the same element inside two seconds

WHY rage_click IS HERE AND dead_click IS NOT

A rage click is cheap and unambiguous: the reader is hitting something that is
not responding. It is the single best "this is broken and nobody reported it"
signal available from a snippet this size.

A dead click - a click on something that looks interactive and is not - needs
to know what the page *should* have done, and getting it wrong fills the
reports with noise. Microsoft Clarity computes it properly from the session
recording, so it is left to Clarity.

WHAT IS DELIBERATELY NOT SENT

No stack traces. A stack from a minified file is unreadable, and on a page
where a reader has typed their income into the form, a stack can incidentally
capture a variable holding it. Message, file and line are enough to find any of
these, and none of them can carry a figure.

Errors are also capped at five per page. Without a cap, one exception thrown
inside a scroll handler sends a thousand events, and GA4 silently drops the rest
of the session - so the cap protects the rest of the measurement, not the quota.

Idempotent, guarded. Run after analytics.py, in the STRUCTURE stage.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training")
MARK = "/* _dev/error_tracking.py */"

JS = """<script>%(mark)s
(function(){
  var CAP = 5, sent = 0;

  function send(name, params){
    if (sent >= CAP) return;
    sent++;
    try {
      params = params || {};
      params.page = location.pathname.slice(0, 100);
      window.dataLayer = window.dataLayer || [];
      if (typeof window.gtag === 'function') { window.gtag('event', name, params); }
      else { window.dataLayer.push(['event', name, params]); }
    } catch (e) {}
  }

  // Strip anything that could carry a figure a reader typed. A message like
  // "Cannot read properties of undefined" is what is wanted; a message that has
  // interpolated a value is not.
  function clean(s){
    return String(s == null ? '' : s).replace(/\\s+/g, ' ').slice(0, 140);
  }
  function fileOf(src){
    // The last path segment alone is often useless: gtag loads from
    // ".../gtag/js?id=G-..." and reports as "js", which names nothing. Keep the
    // last two segments when the final one is short or extensionless.
    try {
      var parts = String(src || '').split('?')[0].split('/').filter(Boolean);
      var tail = parts.pop() || '';
      if (tail.length < 6 || tail.indexOf('.') === -1) {
        tail = (parts.pop() || '') + '/' + tail;
      }
      return tail.replace(/^\//, '').slice(0, 60) || 'unknown';
    } catch (e) { return 'unknown'; }
  }

  // ------------------------------------------------------ uncaught errors
  window.addEventListener('error', function(e){
    // An error event on an element rather than the window is a resource that
    // failed to load - a different problem with a different fix.
    if (e && e.target && e.target !== window && e.target.tagName){
      var t = e.target;
      send('resource_error', {
        kind: t.tagName.toLowerCase(),
        file: fileOf(t.src || t.href)
      });
      return;
    }
    send('js_error', {
      message: clean(e && e.message),
      file: fileOf(e && e.filename),
      line: (e && e.lineno) || 0
    });
  }, true);

  window.addEventListener('unhandledrejection', function(e){
    var r = e && e.reason;
    send('promise_error', {
      message: clean(r && (r.message || r)),
      file: fileOf(r && r.fileName)
    });
  });

  // ---------------------------------------------------------- rage clicks
  var last = null, count = 0, first = 0;
  document.addEventListener('click', function(e){
    var el = e.target;
    if (!el || !el.tagName) return;
    var t = Date.now();
    // Structural identity only. Element TEXT is deliberately not included: on a
    // calculator page an arbitrary element can contain a figure the reader
    // typed, and a rage click is exactly the moment they are typing.
    var near = el.closest && el.closest('[id]');
    var key = el.tagName + '#' + (el.id || '') + '.'
            + ((el.className || '') + '').trim().split(/\s+/)[0].slice(0, 24)
            + (near && near.id && near.id !== el.id ? ' in#' + near.id.slice(0, 24) : '');
    if (key === last && (t - first) < 2000){
      count++;
      if (count === 4){
        send('rage_click', {target: key.slice(0, 90)});
      }
    } else {
      last = key; count = 1; first = t;
    }
  }, true);
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


def main():
    js = JS % {"mark": MARK}
    n = skipped = 0
    for rel in pages():
        p = os.path.join(SITE, rel)
        s = open(p, encoding="utf-8").read()
        if "sitenav" not in s:
            continue
        orig = s
        s = re.sub(r"\n?<script>" + re.escape(MARK) + r"[\s\S]*?</script>\n?", "", s)
        if "gtag/js?id=" not in s:
            # Nothing to send through. Recorded rather than silently skipped,
            # because a page with no tag is itself a finding.
            skipped += 1
            if s != orig:
                open(p, "w", encoding="utf-8").write(s)
            continue
        i = s.lower().rfind("</body>")
        if i < 0:
            continue
        s = s[:i] + js + "\n" + s[i:]
        if s != orig:
            open(p, "w", encoding="utf-8").write(s)
            n += 1
    print("%d page(s) now report their own errors" % n)
    if skipped:
        print("%d page(s) skipped - no gtag to send through" % skipped)

    # ------------------------------------------------------------- guards
    bad = 0
    covered = 0
    for rel in pages():
        s = open(os.path.join(SITE, rel), encoding="utf-8").read()
        if "sitenav" not in s or "gtag/js?id=" not in s:
            continue
        covered += 1
        if s.count(MARK) != 1:
            print("GUARD %s: %d copies" % (rel, s.count(MARK)))
            bad += 1

    # No stack traces, and nothing that could carry a typed figure.
    for pat, why in ((r"\.stack\b", "a stack trace, which can capture a "
                                    "variable holding a reader's figure"),
                     (r"\.value\b", "a field value"),
                     (r"location\.hash", "the share hash, which encodes the "
                                         "reader's whole setup"),
                     (r"location\.search", "the query string")):
        if re.search(pat, JS):
            print("GUARD: the error script reads %s" % why)
            bad += 1
    if "sent >= CAP" not in JS:
        print("GUARD: no per-page cap. One error in a scroll handler would send "
              "thousands and GA4 would drop the rest of the session.")
        bad += 1

    names = sorted(set(re.findall(r"send\('([a-z_]+)'", JS)))
    if names != ["js_error", "promise_error", "rage_click", "resource_error"]:
        print("GUARD: unexpected event set %s" % names)
        bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean - %d page(s) covered, events: %s"
          % (covered, ", ".join(names)))
    print("no stack traces, no values, capped at 5 per page")


if __name__ == "__main__":
    main()
