"""M2: a tiny localhost server for rendering the Siddham seed syllables with a real shaping engine.

Pillow on this machine has no raqm (no complex shaping), so Siddham conjuncts (TRAH, HRIH) and mark placement need a
browser: Chromium shapes text with HarfBuzz, also on <canvas>. The page spikes/M2/render_bonji.html loads
research/fonts/notosanssiddham/NotoSansSiddham-Regular.ttf, draws each syllable white on black, and POSTs the PNG
back here; the server writes it to research/materials/bonji_masks/<name>.png (the committed source masks that
make_m1_materials.grave_layout pastes into the atlas).

  python spikes/M2/bonji_server.py [port]      (default 8765, localhost only; stop it with Ctrl+C / TaskStop)
"""
import http.server
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(DEV, "research", "materials", "bonji_masks")
FILES = {"/": (os.path.join(HERE, "render_bonji.html"), "text/html; charset=utf-8"),
         "/font.ttf": (os.path.join(DEV, "research", "fonts", "notosanssiddham", "NotoSansSiddham-Regular.ttf"),
                       "font/ttf")}


class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        p = self.path.split("?")[0]
        if p not in FILES:
            self.send_error(404)
            return
        fn, ct = FILES[p]
        data = open(fn, "rb").read()
        self.send_response(200)
        self.send_header("Content-Type", ct)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        m = re.match(r"^/save/([a-z0-9_]+)\.png$", self.path)
        if not m:
            self.send_error(400)
            return
        n = int(self.headers.get("Content-Length", 0))
        data = self.rfile.read(n)
        os.makedirs(OUT, exist_ok=True)
        with open(os.path.join(OUT, m.group(1) + ".png"), "wb") as f:
            f.write(data)
        self.send_response(200)
        self.send_header("Content-Length", "2")
        self.end_headers()
        self.wfile.write(b"ok")


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    http.server.ThreadingHTTPServer(("127.0.0.1", port), H).serve_forever()
