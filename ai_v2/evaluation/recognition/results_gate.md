# Dog or not: first stage of recognition

Share of images taken for a dog, measured on held out images (odd numbered). Targets: dog sets at least 95%; people, person heads and scenes without animals at most 2%. Cats are reported without a target (later version).

| set | images | A. YOLO only | B. YOLO, then CLIP scene check | C. CLIP scene check only |
|---|---|---|---|---|
| dog_faces, clean | 100 | 65.0% (miss) | 100.0% | 100.0% |
| dog_faces, feeder | 100 | 0.0% (miss) | 100.0% | 100.0% |
| whole_dogs, clean | 73 | 76.7% (miss) | 93.2% (miss) | 89.0% (miss) |
| whole_dogs, feeder | 73 | 5.5% (miss) | 75.3% (miss) | 75.3% (miss) |
| cats, clean | 86 | 3.5% (no target) | 5.8% (no target) | 2.3% (no target) |
| cats, feeder | 86 | 1.2% (no target) | 7.0% (no target) | 5.8% (no target) |
| people, clean | 100 | 1.0% | 1.0% | 0.0% |
| people, feeder | 100 | 0.0% | 0.0% | 0.0% |
| person_heads, clean | 83 | 0.0% | 0.0% | 0.0% |
| person_heads, feeder | 83 | 0.0% | 1.2% | 1.2% |
| scenes_no_animal, clean | 100 | 0.0% | 0.0% | 0.0% |
| scenes_no_animal, feeder | 100 | 0.0% | 3.0% (miss) | 3.0% (miss) |

CLIP dog probability threshold (chosen on even numbered images): B. YOLO, then CLIP scene check: 0.89, C. CLIP scene check only: 0.89

