# Hands on test tools

Test the recognition with the real ESP32-CAM. First flash the camera with `firmware/esp32_camera_test` (see its README) and note the IP address it prints.

Run every command from `D:\kibbly\ai_v2`. The first command of a session loads the models (about 20 seconds).

## 1. Camera check

```
.venv\Scripts\python.exe tools\camera_check.py --ip 192.168.43.120
```

Prints the camera status, takes 3 photos, and for each one: size, transfer time, what YOLO found, and the scene check (dog, cat, person, nothing). Add `--flash` in dim light.

## 2. Enroll dogs

Use at least 2 dogs, so the test shows that the AI tells them apart.

| Source | Command |
|---|---|
| The ESP32-CAM | `.venv\Scripts\python.exe tools\enroll.py --dog biscuit --camera 192.168.43.120 --count 15` |
| A folder of phone photos | `.venv\Scripts\python.exe tools\enroll.py --dog biscuit --photos D:\photos\biscuit` |
| A short phone video | `.venv\Scripts\python.exe tools\enroll.py --dog biscuit --video D:\videos\biscuit.mp4` |
| See the enrolled dogs | `.venv\Scripts\python.exe tools\enroll.py --list` |
| Remove a dog | `.venv\Scripts\python.exe tools\enroll.py --remove biscuit` |

At least 3 usable photos are needed; 10 to 15 varied ones are better (front, both sides, from above). Enrolling a dog again replaces its references.

## 3. Live test

Guided (recommended): the script says which dog to show, waits for Enter before each group, marks every check RIGHT or WRONG and prints the score. `unknown` means a dog that was never enrolled. `--wait` sets the seconds between checks of a group (2 by default).

```
.venv\Scripts\python.exe tools\live_test.py --ip 192.168.43.120 --meal-dog biscuit --plan biscuit:4,mochi:4,unknown:4
```

Free run (no instructions, runs until Ctrl+C):

```
.venv\Scripts\python.exe tools\live_test.py --ip 192.168.43.120 --meal-dog biscuit
```

Every check takes 2 photos, like the feeder, and prints for example:

```
check   1: Biscuit        confidence 0.78  lead 0.51  found by detector    photos 0.3 s  AI 0.4 s  -> SERVE
check   2: Mochi          confidence 0.76  lead 0.48  found by scene_check photos 0.3 s  AI 0.6 s  -> BLOCK (not this dog's meal)
check   3: unknown_dog    confidence 0.31  lead 0.31  found by detector    photos 0.3 s  AI 0.4 s  -> unknown dog: small portion
```

| Column | Meaning |
|---|---|
| confidence | Similarity to the closest enrolled photo of that dog; accepted at 0.485 or more |
| lead | How far ahead of the second dog; needs 0.08 or more, otherwise "unsure" |
| found by | `detector` (YOLO box) or `scene_check` (CLIP judged the whole photo, usual for close ups) |
| last part | What the feeder would do during the meal of `--meal-dog` |

Stop with Ctrl+C, or use `--checks 20`.

## What gets saved

Every session goes to `D:\kibbly_data\real\<date>_<kind>\`: the photos and, for live tests, `results.jsonl` with every answer. Fill the `truth` field (the dog really in front of the camera) afterwards: these are the first real ESP32-CAM data, used to measure real accuracy and to retrain the learned layer.

## No dog today?

1. Show dog photos on a phone screen or printed photos in front of the camera. Good enough to test the whole chain; accuracy will be lower than with a real dog.
2. Rehearse without the board: `.venv\Scripts\python.exe tools\fake_camera.py --folder D:\some\dog\photos`, then use `--ip 127.0.0.1:8090` in the commands above.

## Test plan for the first session

| # | Test | Expected |
|---|---|---|
| 1 | Nothing in front of the camera | `not_a_dog` |
| 2 | A person (hand, face) | `not_a_dog` |
| 3 | Enrolled dog A, meal of A | `SERVE` |
| 4 | Enrolled dog A, meal of B | `BLOCK` |
| 5 | A dog that is not enrolled | `unknown dog` |
| 6 | Dim light, then `--flash` | Note the difference |
| 7 | Camera low (bowl height) and camera higher | Note which angle gives higher confidence (for Youssef) |
