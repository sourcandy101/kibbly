# Detector and speed check

Detector: YOLO11n, dog accepted at confidence 0.35 or more. Sample: 400 DogFaceNet images.

| test | images | dog found | other result |
|---|---|---|---|
| close up dog faces, clean | 400 | 64.0% | dog: 49, nothing: 37, person: 36, cat: 22 |
| close up dog faces, feeder | 400 | 0.0% | nothing: 226, person: 170, cat: 2, dog: 2 |
| people (street photos) | 2 | 0 with a dog | must be 0 |
| empty scenes (plain, noise, dark) | 3 | 0 with a dog | must be 0 |

Full pipeline on a 640 x 480 photo (detect, crop, describe with DINOv2 small): median 267 ms, slowest 350 ms over 30 photos.
