"""A fake ESP32-CAM on the laptop, to rehearse the tools without the board.

  .venv\\Scripts\\python.exe tools\\fake_camera.py --folder D:\\some\\dog\\photos [--port 8090]

Serves /status and /capture like the real camera (photos from the folder, in turn, resized
to 640 x 480). Then use --ip 127.0.0.1:8090 with the other tools.
"""

import argparse
import io
import itertools
import json
import pathlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from PIL import Image

PHOTO_TYPES = {".jpg", ".jpeg", ".png"}


def make_handler(photos):
    cycle = itertools.cycle(photos)

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def do_GET(self):
            if self.path.startswith("/status"):
                body = json.dumps({"ip": "127.0.0.1", "rssi_dbm": -50, "frame_size": "640x480",
                                   "psram": True, "fake": True}).encode()
                kind = "application/json"
            elif self.path.startswith("/capture"):
                buffer = io.BytesIO()
                Image.open(next(cycle)).convert("RGB").resize((640, 480)).save(buffer, "JPEG", quality=80)
                body, kind = buffer.getvalue(), "image/jpeg"
            else:
                self.send_error(404)
                return
            self.send_response(200)
            self.send_header("Content-Type", kind)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    return Handler


def serve(folder, port):
    photos = sorted(p for p in pathlib.Path(folder).iterdir() if p.suffix.lower() in PHOTO_TYPES)
    if not photos:
        raise SystemExit(f"no photos in {folder}")
    server = ThreadingHTTPServer(("127.0.0.1", port), make_handler(photos))
    return server, len(photos)


def main():
    parser = argparse.ArgumentParser(description="Fake ESP32-CAM serving photos from a folder.")
    parser.add_argument("--folder", required=True)
    parser.add_argument("--port", type=int, default=8090)
    args = parser.parse_args()
    server, count = serve(args.folder, args.port)
    print(f"Fake camera with {count} photo(s) at http://127.0.0.1:{args.port}  (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
