"""Live recognition test with the ESP32-CAM: 2 photos per check, as the feeder will do.

  .venv\\Scripts\\python.exe tools\\live_test.py --ip 192.168.43.120 [--checks 20] [--meal-dog biscuit] [--flash]

Each check prints who is at the bowl, the confidence, the lead over the second dog, how the
dog was found (YOLO box or scene check) and the time. With --meal-dog it also prints what the
feeder would do (serve, block, unknown portion, nothing).

Guided mode, to test several dogs in a row without a time limit:

  .venv\\Scripts\\python.exe tools\\live_test.py --ip 192.168.43.120 --meal-dog biscuit --plan biscuit:4,mochi:4,unknown:4

Before each group the script says which dog to show and waits for Enter. It fills the 'truth'
field itself and prints the score at the end. 'unknown' means a dog that was never enrolled.

Every photo and every answer is saved in D:\\kibbly_data\\real\\<date>_live\\ (photos plus
results.jsonl) to measure real accuracy later. Stop with Ctrl+C.
"""

import argparse
import json
import pathlib
import time

from common import DEFAULT_GALLERY, fetch_photo, load_gallery, load_models, session_folder


def feeder_action(result, meal_dog):
    if result.classification == "not_a_dog":
        return "nothing (no dog)"
    if result.classification == "unknown_dog":
        return "unknown dog: small portion" if "unsure" not in result.reason else "wait and check again (unsure)"
    if meal_dog is None:
        return "known dog"
    return "SERVE" if result.dog_id == meal_dog else "BLOCK (not this dog's meal)"


def parse_plan(text, dog_ids):
    """'biscuit:4,mochi:4,unknown:4' into [('biscuit', 4), ('mochi', 4), ('unknown', 4)]."""
    plan = []
    for part in text.split(","):
        dog, _, count = part.strip().partition(":")
        if dog != "unknown" and dog not in dog_ids:
            raise SystemExit(f"'{dog}' is not enrolled. Use one of: {', '.join(dog_ids)}, or 'unknown'.")
        plan.append((dog, int(count) if count else 4))
    return plan


def is_correct(result, truth):
    if truth == "unknown":
        return result.classification == "unknown_dog"
    return result.dog_id == truth


def main():
    parser = argparse.ArgumentParser(description="Live dog recognition with the ESP32-CAM.")
    parser.add_argument("--ip", required=True)
    parser.add_argument("--checks", type=int, default=0, help="number of checks (0 means until Ctrl+C)")
    parser.add_argument("--meal-dog", help="dog id whose meal it is, to print the feeder decision")
    parser.add_argument("--gap", type=float, default=0.3, help="seconds between the 2 photos of a check")
    parser.add_argument("--plan", help="guided test, for example biscuit:4,mochi:4,unknown:4")
    parser.add_argument("--wait", type=float, default=None,
                        help="seconds between checks (default 2 in guided mode, 0 otherwise)")
    parser.add_argument("--flash", action="store_true")
    parser.add_argument("--gallery", default=str(DEFAULT_GALLERY))
    args = parser.parse_args()

    gallery, names = load_gallery(pathlib.Path(args.gallery))
    if not gallery.dog_ids:
        print("No dog enrolled. Run tools\\enroll.py first.")
        return
    plan = parse_plan(args.plan, gallery.dog_ids) if args.plan else None
    wait = args.wait if args.wait is not None else (2.0 if plan else 0.0)
    if plan:
        args.checks = sum(count for _, count in plan)
    print(f"Enrolled: {', '.join(names.get(d, d) for d in gallery.dog_ids)}. Loading the models (about 20 s)")
    from kibbly_ai.perception.recognizer import Recognizer
    detector, scene, embedder = load_models()
    recognizer = Recognizer(detector, embedder, gallery, scene=scene)
    folder = session_folder("live")
    log = (folder / "results.jsonl").open("a", encoding="utf-8")
    print(f"Saving photos and results in {folder}. Stop with Ctrl+C.\n")

    # One entry per check in guided mode: (dog really shown, first check of its group, group size)
    steps = [(dog, i == 0, count) for dog, count in plan for i in range(count)] if plan else []
    check = 0
    score = {}  # truth: [right, total]
    try:
        while args.checks == 0 or check < args.checks:
            truth = None
            if plan:
                truth, first, count = steps[check]
                if first:
                    label = "a dog that was NEVER enrolled" if truth == "unknown" else names.get(truth, truth).upper()
                    print(f"\n>>> Show {label} in front of the camera ({count} checks).")
                    input(">>> Press Enter when it is in place... ")
                elif wait > 0:
                    time.sleep(wait)
            elif check > 0 and wait > 0:
                time.sleep(wait)
            check += 1
            frames, files, transfer = [], [], 0.0
            for n in range(2):
                image, data, seconds = fetch_photo(args.ip, flash=args.flash)
                name = f"check_{check:04d}_{n + 1}.jpg"
                (folder / name).write_bytes(data)
                frames.append(image)
                files.append(name)
                transfer += seconds
                if n == 0:
                    time.sleep(args.gap)
            start = time.perf_counter()
            result = recognizer.recognize_frames(frames)
            ai_seconds = time.perf_counter() - start
            who = names.get(result.dog_id, result.dog_id) if result.dog_id else result.classification
            found_by = result.detection.source if result.detection else "none"
            conf = f"{result.confidence:.2f}" if result.confidence is not None else "  -  "
            lead = f"{result.margin:.2f}" if result.margin is not None else "  -  "
            mark = ""
            if plan:
                ok = is_correct(result, truth)
                score.setdefault(truth, [0, 0])
                score[truth][0] += ok
                score[truth][1] += 1
                mark = "  RIGHT" if ok else "  WRONG"
            print(f"check {check:3d}: {who:<14} confidence {conf}  lead {lead}  found by {found_by:<11} "
                  f"photos {transfer:.1f} s  AI {ai_seconds:.1f} s  -> {feeder_action(result, args.meal_dog)}{mark}")
            log.write(json.dumps({"check": check, "files": files, "classification": result.classification,
                                  "dog_id": result.dog_id, "confidence": result.confidence, "margin": result.margin,
                                  "found_by": found_by, "reason": result.reason,
                                  "scores": {m.dog_id: round(m.score, 4) for m in result.matches},
                                  "transfer_s": round(transfer, 3), "ai_s": round(ai_seconds, 3),
                                  "meal_dog": args.meal_dog,
                                  "truth": ("unknown_dog" if truth == "unknown" else truth)}) + "\n")
            log.flush()
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        log.close()
    if score:
        print("\nScore")
        for truth, (ok, total) in score.items():
            label = "never enrolled dog" if truth == "unknown" else names.get(truth, truth)
            print(f"  {label:<20} {ok}/{total} right")
        right = sum(s[0] for s in score.values())
        total = sum(s[1] for s in score.values())
        print(f"  {'all':<20} {right}/{total} right ({100 * right / total:.0f} %)")
        print(f"{check} check(s) saved in {folder}, with the truth already filled.")
    else:
        print(f"{check} check(s) saved in {folder}. Write the real dog in the 'truth' field later to measure accuracy.")


if __name__ == "__main__":
    main()
