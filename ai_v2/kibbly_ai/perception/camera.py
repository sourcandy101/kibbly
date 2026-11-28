"""Talk to the ESP32-CAM over WiFi.

The camera runs a small HTTP server (firmware/esp32_camera_test): GET /status for board
status and GET /capture for a fresh JPEG (add ?flash=1 for the LED). The AI server pulls
photos from it with these helpers. This is the pull path used for the demo; the push path
(the ESP32-CAM POSTing to /recognize) is the next firmware step.
"""

import io
import time
import urllib.request

from PIL import Image


def camera_url(ip: str, path: str) -> str:
    host = ip if ip.startswith("http") else f"http://{ip}"
    return host.rstrip("/") + path


def fetch_status(ip: str, timeout: float = 5.0) -> dict:
    import json

    with urllib.request.urlopen(camera_url(ip, "/status"), timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_frame(ip: str, flash: bool = False, timeout: float = 10.0):
    """Return (PIL image in RGB, seconds taken)."""
    start = time.perf_counter()
    url = camera_url(ip, "/capture" + ("?flash=1" if flash else ""))
    with urllib.request.urlopen(url, timeout=timeout) as response:
        data = response.read()
    return Image.open(io.BytesIO(data)).convert("RGB"), time.perf_counter() - start


def fetch_frames(ip: str, frames: int = 2, gap: float = 0.3, flash: bool = False, timeout: float = 10.0):
    """Fetch several photos of one visit, as the feeder does (2 by default). Returns (images, seconds)."""
    images, total = [], 0.0
    for index in range(max(1, frames)):
        image, seconds = fetch_frame(ip, flash=flash, timeout=timeout)
        images.append(image)
        total += seconds
        if index < frames - 1 and gap > 0:
            time.sleep(gap)
    return images, total
