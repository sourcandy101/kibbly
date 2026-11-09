# Recognition evaluation

Step 4 of the AI rebuild, 9 November 2026. Full tables: `results_recognition.md` (identity), `results_gate.md` (dog or not), `results_detector.md` (detector and speed), `training_projection.json` (learned layer).

## How to run

From `ai_v2` (needs DogFaceNet in `D:\kibbly_data\dogfacenet` and COCO val2017 in `D:\kibbly_data\coco`; see `../../data_collection_guide.md` for our own data):

| Command | Time on the team laptop |
|---|---|
| `.venv\Scripts\python.exe evaluation\recognition\embed_dataset.py` | 50 minutes once (vectors cached in `D:\kibbly_data\cache`) |
| `.venv\Scripts\python.exe evaluation\recognition\train_projection.py` | 20 seconds |
| `.venv\Scripts\python.exe evaluation\recognition\evaluate_recognition.py` | 5 minutes |
| `.venv\Scripts\python.exe evaluation\recognition\gate_check.py` | 15 minutes once, then seconds |
| `.venv\Scripts\python.exe evaluation\recognition\detector_check.py` | 2 minutes |

## Method in short

1. DogFaceNet (CC BY 4.0): 8,363 face images of 1,393 dogs, split three ways with no overlap: **train dogs** (only for the learned layer), **calibration dogs** (choose thresholds), **test dogs** (every number below).
2. 1,500 simulated homes of 2 to 4 dogs per setting. Each dog is enrolled with 1, 3 or 5 clean photos. Six stranger dogs per home try to eat.
3. Queries are clean, or pass through a feeder camera simulation (half resolution, blur, dim light, color cast, strong JPEG compression).
4. Look alike homes: dogs with the most similar coat colors, chosen without the models.
5. Targets: right dog accepted at least 90% at the first check; strangers and wrong dogs accepted at most 2%.

## Findings

Identity numbers: feeder camera simulation, 3 enrollment photos, 2 photos per check, test dogs, unless stated.

| # | Finding | Evidence |
|---|---|---|
| 1 | **DINOv2 small (class token) is the best pretrained image model.** CLIP is not usable for telling dogs apart. | 1 photo per check: DINOv2 77.2%, CLIP 17.9% right dog accepted |
| 2 | **A small learned layer on top of DINOv2 reaches the 90% target** at feeder quality. It is one 384 x 384 matrix trained in 20 seconds on train dogs only, so that clean and degraded photos of the same dog match. | 82.2% without, **91.3%** with; gains of 6 to 12 points in every setting |
| 3 | **Wrong dog feeding is practically zero.** Biscuit is almost never taken for Mochi. | 0.0% to 0.2% in every DINOv2 setting |
| 4 | **Strangers are held at about 2%** (threshold chosen on calibration dogs, measured on test dogs). | 1.5% to 2.2%; 2.1% at the operating point, just above the target |
| 5 | **Two photos per check help** (about 3 points). More than 3 enrollment photos does not help on this data. | Table 2 of `results_recognition.md` |
| 6 | **Look alike homes lose about 5 points**, and still do not feed the wrong dog. | 86.6% right, 0.0% wrong |
| 7 | **YOLO alone misses close up faces**, all of them at feeder quality (often calls them "person"). | `results_detector.md`: 64% clean, 0% at feeder quality |
| 8 | **Fixed with a scene check**: when YOLO finds no dog, CLIP judges the whole photo (dog, cat, person or nothing). CLIP is weak at telling two dogs apart but strong at this question. | `results_gate.md`: close up dog faces found 100% clean and at feeder quality |
| 9 | People are still refused; empty scenes at feeder quality are taken for a dog 3% of the time (target 2%; 3 images out of 100). | Acceptable: the ultrasonic sensor must also see something, and the identity check then treats it as unknown. |
| 10 | **Cats are often taken for dogs** (about 6% to 7%). No target yet, since cats are a later version; a cat then counts as an unknown dog. | `results_gate.md` |
| 11 | **Speed is fine.** | Full pipeline 267 ms median on a 640 x 480 photo, CPU (plus about 120 ms when the scene check runs) |

## Operating point (defaults in `kibbly_ai/perception/recognizer.py`)

| Stage | Setting |
|---|---|
| Find the dog | YOLO11n box (confidence 0.35 or more), else CLIP scene check with dog probability 0.89 or more |
| Describe | DINOv2 small class token followed by the learned layer (`kibbly_ai/perception/weights/dinov2_projection.npz`) |
| Match | At least 3 enrollment photos, 2 photos per check, accept score 0.485, margin 0.08 |

A refused dog is not a failure: nothing is served and the feeder checks again a few seconds later. A refused dog waits; a wrongly accepted dog eats someone else's food. The settings favor waiting.

## Limits of this evaluation

1. DogFaceNet faces are clean, aligned, frontal phone photos. Real feeder photos will show heads from above, eating, partly hidden. Our own data (friends' dogs, then the real ESP32-CAM) is needed to confirm.
2. The feeder camera simulation is an estimate. The learned layer was trained on this same simulation, so its gain on the real camera may be smaller.
3. 5 enrollment photos are measured on fewer dogs (only dogs with 7 or more images), so they are not directly comparable to 1 or 3.
4. Look alike is based on coat color only; breed labels are not available in DogFaceNet.

## Next actions

| # | Action | Owner |
|---|---|---|
| 1 | Detector gap: **done** (finding 8) | Zaineb |
| 2 | Feeder quality accuracy: **done on simulated images** (finding 2) | Zaineb |
| 3 | Camera position: far enough to see the whole head, not only the muzzle | Youssef |
| 4 | Real photos: friends' dogs videos, then real ESP32-CAM shots; retrain the learned layer with them | Zaineb with Youssef and Hedi |
| 5 | Colored collar tiebreaker (step 4.8), once real photos with collars exist | Zaineb |
