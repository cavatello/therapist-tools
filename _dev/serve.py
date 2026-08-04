#!/usr/bin/env python3
"""
Local dev server for the Therapy Practice Simulator.

Serves the site folder (this script's parent) and live-reloads the browser
whenever a source file changes on disk.

The reload snippet is injected into HTML *as it is served* -- your real
index.html / rates.html / concepts.html files are never modified, so nothing
dev-only can ever leak into a Netlify deploy.

Usage:   python3 _dev/serve.py [port] [lan]
Default port 8080, bound to this machine only.  Ctrl-C to stop.

Add the word "lan" to also serve on your local network, so a phone or tablet
on the same Wi-Fi can open the site:   python3 _dev/serve.py 8080 lan
Anyone on that network can then reach it, so only do this on a network you trust.
"""

import functools
import http.server
import os
import socket
import socketserver
import sys
import webbrowser

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
WATCH_EXT = (".js", ".html", ".css")

RELOAD_SNIPPET = """
<script>
(function () {
  var current = null, pending = null, stable = 0;
  function poll() {
    fetch('/__dev/version', { cache: 'no-store' })
      .then(function (r) { return r.text(); })
      .then(function (v) {
        if (current === null) { current = v; return; }
        if (v === current) { pending = null; stable = 0; return; }
        // A file changed. Wait until the fingerprint stops moving before
        // reloading, so we never fetch a half-written file mid-save.
        if (v === pending) { stable++; } else { pending = v; stable = 0; }
        if (stable >= 1) { location.reload(); }
      })
      .catch(function () { /* server restarting; ignore */ });
  }
  setInterval(poll, 700);
  poll();
})();
</script>
""".strip()


def version_stamp():
    """Cheap fingerprint of every watched file's size + mtime."""
    parts = []
    for name in sorted(os.listdir(ROOT)):
        if not name.endswith(WATCH_EXT):
            continue
        try:
            st = os.stat(os.path.join(ROOT, name))
        except OSError:
            continue
        parts.append("%s:%d:%f" % (name, st.st_size, st.st_mtime))
    return "|".join(parts)


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/__dev/version"):
            body = version_stamp().encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
            return

        path = self.translate_path(self.path)
        if os.path.isdir(path):
            path = os.path.join(path, "index.html")

        if path.endswith(".html") and os.path.isfile(path):
            with open(path, "rb") as fh:
                body = fh.read()
            if b"</body>" in body:
                body = body.replace(
                    b"</body>", RELOAD_SNIPPET.encode("utf-8") + b"\n</body>", 1
                )
            else:
                body += RELOAD_SNIPPET.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
            return

        return super().do_GET()

    def end_headers(self):
        # never cache app.js, or edits won't show up
        if self.path.endswith(".js"):
            self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def guess_type(self, path):
        base = super().guess_type(path)
        if str(path).endswith(".js"):
            return "text/javascript; charset=utf-8"
        return base

    def log_message(self, fmt, *args):
        if "/__dev/version" in (args[0] if args else ""):
            return  # don't spam the terminal with poll requests
        sys.stderr.write("  %s\n" % (fmt % args))


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


def lan_ip():
    """Best-effort local network address. No packets are actually sent."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except Exception:
        return None
    finally:
        s.close()


def main():
    args = [a.lower() for a in sys.argv[1:]]
    lan = "lan" in args
    ports = [a for a in args if a.isdigit()]
    port = int(ports[0]) if ports else 8080
    host = "0.0.0.0" if lan else "127.0.0.1"
    handler = functools.partial(Handler, directory=ROOT)
    try:
        httpd = Server((host, port), handler)
    except OSError as exc:
        print("\n  Could not start on port %d: %s" % (port, exc))
        print("  Something else is probably using it. Try:  python3 _dev/serve.py 8081\n")
        sys.exit(1)

    url = "http://localhost:%d/" % port
    print("")
    print("  Therapy Practice Simulator - local dev server")
    print("  " + "-" * 44)
    print("  Serving:   %s" % ROOT)
    print("  Simulator: %s#sim" % url)
    print("  Grow:      %s#grow" % url)
    print("  Field Notes: %srates.html" % url)
    print("  Concepts:  %sconcepts.html" % url)
    print("")
    if lan:
        ip = lan_ip()
        print("  ON YOUR PHONE (same Wi-Fi):")
        if ip:
            print("    http://%s:%d/#sim" % (ip, port))
        else:
            print("    could not detect this Mac's network address -")
            print("    System Settings > Wi-Fi > Details, then use http://<that IP>:%d/#sim" % port)
        print("    Live reload works there too. Anyone on this network can reach it.")
        print("")
    else:
        print("  This machine only. To view on a phone on the same Wi-Fi:")
        print("    python3 _dev/serve.py %d lan" % port)
        print("")
    print("  Live reload is ON - the page refreshes itself when a file changes.")
    print("  Ctrl-C to stop.")
    print("")
    try:
        webbrowser.open(url + "#sim")
    except Exception:
        pass
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n  Stopped.\n")


if __name__ == "__main__":
    main()
