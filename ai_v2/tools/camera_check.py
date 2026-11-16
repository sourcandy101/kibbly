"""Check the ESP32-CAM from the laptop: is it reachable, how fast, and does the AI see a dog?

  .venv\\Scripts\\python.exe tools\\camera_check.py --ip 192.168.43.120 [--photos 3] [--flash]

Saves the photos in D:\\kibbly_data\\real\\<date>_check\\ and prints, for each photo:
transfer time, size, what YOLO found, and the CLIP scene check (dog, cat, person, nothing).
"""

import argparse
import time

from common import fetch_photo, fetch_status, load_models, session_folder


def main():
    parser = argparse.ArgumentParser(description="Check the ESP32-CAM and the dog finder.")
    parser.add_argument("--ip", required=True, help="IP address printed by the ESP32-CAM serial monitor")
    parser.add_argument("--photos", type=int, default=3)
    parser.add_argument("--flash", action="store_true", help="light the white LED for each photo")
    args = parser.parse_args()

    print(f"1. Camera status at {args.ip}")
    try:
        status = fetch_status(args.ip)
    except OSError as exc:
        print(f"   Cannot reach the camera: {exc}")
        print("   Check: laptop and ESP32-CAM on the same hotspot, the IP from the serial monitor, the board is powered.")
        return
    print(f"   {status}")
    if status.get("rssi_dbm", 0) < -75:
        print("   Weak WiFi signal: bring the phone closer to the camera.")

    print("2. Loading the models (about 20 s the first time)")
    detector, scene, _ = load_models(with_embedder=False)

    folder = session_folder("check")
    print(f"3. Taking {args.photos} photo(s), saved in {folder}")
    for i in range(args.photos):
        image, data, seconds = fetch_photo(args.ip, flash=args.flash)
        path = folder / f"photo_{i + 1:02d}.jpg"
        path.write_bytes(data)
        start = time.perf_counter()
        boxes = [(d.label, round(d.confidence, 2)) for d in detector.detect(image)]
        probs = scene.classify([image])[0]
        ai_seconds = time.perf_counter() - start
        top = max(probs, key=probs.get)
        print(f"   photo {i + 1}: {image.width} x {image.height}, {len(data) // 1024} KB, transfer {seconds:.2f} s, "
              f"AI {ai_seconds:.2f} s")
        print(f"      YOLO: {boxes or 'nothing'}")
        print(f"      scene check: {top} ({', '.join(f'{k} {v:.2f}' for k, v in probs.items())})")
    print("Done. Open the folder to look at the photos: framing, light and sharpness matter for recognition.")


if __name__ == "__main__":
    main()
