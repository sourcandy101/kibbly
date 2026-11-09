# Recognition evaluation

Step 4.5 and 4.6 of the AI rebuild, 9 November 2026. Full tables: `results_recognition.md` (identity) and `results_detector.md` (detector and speed).

## How to run

From `ai_v2` (needs DogFaceNet in `D:\kibbly_data\dogfacenet`, see `../../data_collection_guide.md` for our own data):

| Command | Time on the team laptop |
|---|---|
| `.venv\Scripts\python.exe evaluation\recognition\embed_dataset.py` | 50 minutes once (vectors cached in `D:\kibbly_data\cache`) |
| `.venv\Scripts\python.exe evaluation\recognition\evaluate_recognition.py` | 3 minutes |
| `.venv\Scripts\python.exe evaluation\recognition\detector_check.py` | 2 minutes |

## Method in short

1. DogFaceNet (CC BY 4.0): 8,363 face images of 1,393 dogs. Dogs with at least 4 images are split in two: calibration dogs choose the threshold, different test dogs measure it.
2. 1,500 simulated homes of 2 to 4 dogs per setting. Each dog is enrolled with 1, 3 or 5 clean photos. Six stranger dogs per home try to eat.
3. Queries are clean, or pass through a feeder camera simulation (half resolution, blur, dim light, color cast, strong JPEG compression).
4. Look alike homes: dogs with the most similar coat colors, chosen without the models.
5. Targets: right dog accepted at least 90% at the first check; strangers and wrong dogs accepted at most 2%.

## Findings

| # | Finding | Evidence |
|---|---|---|
| 1 | **DINOv2 small (class token) is the best image model.** CLIP is not usable for telling dogs apart. | Feeder images, 3 photos: DINOv2 78.6%, CLIP 16.9% right dog accepted |
| 2 | **Wrong dog feeding is practically zero.** Biscuit is almost never taken for Mochi. | Wrong dog accepted 0.0% to 0.1% in every DINOv2 setting |
| 3 | **Strangers are held at 2% by design** (the threshold is chosen for it on other dogs, and it holds on test dogs). | 1.6% to 2.1% |
| 4 | **Clean photos meet every target; feeder quality photos do not.** | 3 photos, 2 per check: clean 91.5%, feeder simulation 81.5% right dog accepted |
| 5 | **Two photos per check help** (about 3 to 6 points). More than 3 enrollment photos does not help on this data. | Table 2 |
| 6 | **Look alike homes lose about 9 points**, but still do not feed the wrong dog. | Feeder, 3 photos, 2 per check: 72.2% vs 81.5%, wrong dog 0.0% |
| 7 | **The detector is the weak link.** YOLO11n, trained on whole dogs, misses close up faces, and misses all of them at feeder quality (often calls them "person"). The identity results above skip the detector because DogFaceNet images are already face crops. | Dog found: 64% clean close ups, 0% feeder close ups |
| 8 | **Speed is fine.** | Full pipeline 267 ms median on a 640 x 480 photo, CPU |

## Operating point (set as default in `kibbly_ai/perception/recognizer.py`)

DINOv2 small class token, at least 3 enrollment photos, 2 photos per check, accept score 0.61, margin 0.08.

A refused dog is not a failure: nothing is served and the feeder checks again a few seconds later. A refused dog waits; a wrongly accepted dog eats someone else's food. The settings favor waiting.

## Limits of this evaluation

1. DogFaceNet faces are clean, aligned, frontal phone photos. Real feeder photos will show heads from above, eating, partly hidden. Our own data (friends' dogs, then the real ESP32-CAM) is needed to confirm.
2. The feeder camera simulation is an estimate, not a measurement of the real camera.
3. 5 enrollment photos are measured on fewer dogs (only dogs with 7 or more images), so they are not directly comparable to 1 or 3.
4. Look alike is based on coat color only; breed labels are not available in DogFaceNet.

## Next actions

| # | Action | Owner |
|---|---|---|
| 1 | Fix the detector gap (fallback when no dog box is found, or a detector that handles close ups) | Zaineb |
| 2 | Raise feeder quality accuracy toward 90% (a small learned layer on top of DINOv2, trained on clean and degraded pairs of other dogs) | Zaineb |
| 3 | Camera position: far enough to see the whole head, not only the muzzle | Youssef |
| 4 | Real photos: friends' dogs videos, then real ESP32-CAM shots | Zaineb with Youssef and Hedi |
