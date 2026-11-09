# Dog recognition evaluation

Timestamp: 2026-11-09T17:04:48  
Data: DogFaceNet (CC BY 4.0), 602 calibration dogs and 603 different test dogs, 1500 simulated homes per setting, seed 7.

Targets: right dog accepted at least 90.0%, strangers and wrong dogs accepted at most 2.0%. Thresholds are chosen on calibration dogs and measured on test dogs.
## 1. Model comparison

3 enrollment photos, 1 photo per check, feeder camera simulation, normal homes.
| model | right dog accepted | stranger accepted | wrong dog accepted | threshold | margin | meets targets |
|---|---|---|---|---|---|---|
| dinov2_small_cls | 78.6% | 1.9% | 0.1% | 0.620 | 0.06 | no |
| dinov2_small_cls_mean | 73.4% | 1.7% | 0.1% | 0.685 | 0.04 | no |
| clip_b32 | 16.9% | 1.6% | 0.3% | 0.900 | 0.02 | no |

Best model: **dinov2_small_cls**.

## 2. dinov2_small_cls: photos per dog, photos per check, image quality

Normal homes.
| enroll photos | photos per check | query images | right dog accepted | stranger accepted | wrong dog accepted | threshold | margin | meets targets |
|---|---|---|---|---|---|---|---|---|
| 1 | 1 | clean | 78.5% | 1.6% | 0.1% | 0.645 | 0.06 | no |
| 1 | 1 | feeder | 68.7% | 1.5% | 0.1% | 0.595 | 0.10 | no |
| 1 | 2 | clean | 83.9% | 1.8% | 0.0% | 0.630 | 0.04 | no |
| 1 | 2 | feeder | 74.6% | 1.6% | 0.1% | 0.580 | 0.00 | no |
| 3 | 1 | clean | 88.1% | 1.7% | 0.0% | 0.675 | 0.08 | no |
| 3 | 1 | feeder | 78.6% | 1.9% | 0.1% | 0.620 | 0.06 | no |
| 3 | 2 | clean | 91.5% | 1.6% | 0.0% | 0.665 | 0.10 | yes |
| 3 | 2 | feeder | 81.5% | 1.6% | 0.0% | 0.610 | 0.08 | no |
| 5 | 1 | clean | 88.3% | 2.0% | 0.1% | 0.685 | 0.02 | no |
| 5 | 1 | feeder | 75.9% | 2.1% | 0.0% | 0.625 | 0.10 | no |
| 5 | 2 | clean | 92.2% | 2.1% | 0.0% | 0.675 | 0.08 | no |
| 5 | 2 | feeder | 79.6% | 1.8% | 0.0% | 0.620 | 0.06 | no |

## 3. dinov2_small_cls: look alike homes (similar coat colors)

Same thresholds as normal homes, feeder camera simulation.
| enroll photos | photos per check | homes | right dog accepted | stranger accepted | wrong dog accepted | threshold | margin | meets targets |
|---|---|---|---|---|---|---|---|---|
| 1 | 1 | normal | 68.7% | 1.5% | 0.1% | 0.595 | 0.10 | no |
| 1 | 1 | look_alike | 60.8% | 1.3% | 0.3% | 0.595 | 0.10 | no |
| 1 | 2 | normal | 74.6% | 1.6% | 0.1% | 0.580 | 0.00 | no |
| 1 | 2 | look_alike | 68.0% | 1.4% | 0.9% | 0.580 | 0.00 | no |
| 3 | 1 | normal | 78.6% | 1.9% | 0.1% | 0.620 | 0.06 | no |
| 3 | 1 | look_alike | 69.7% | 1.7% | 0.2% | 0.620 | 0.06 | no |
| 3 | 2 | normal | 81.5% | 1.6% | 0.0% | 0.610 | 0.08 | no |
| 3 | 2 | look_alike | 72.2% | 1.3% | 0.0% | 0.610 | 0.08 | no |
| 5 | 1 | normal | 75.9% | 2.1% | 0.0% | 0.625 | 0.10 | no |
| 5 | 1 | look_alike | 66.0% | 1.6% | 0.1% | 0.625 | 0.10 | no |
| 5 | 2 | normal | 79.6% | 1.8% | 0.0% | 0.620 | 0.06 | no |
| 5 | 2 | look_alike | 70.7% | 1.7% | 0.0% | 0.620 | 0.06 | no |

## 4. All models, every setting

| model | enroll | frames | images | homes | right dog accepted | stranger accepted | wrong dog accepted | threshold | margin | meets targets |
|---|---|---|---|---|---|---|---|---|---|---|
| dinov2_small_cls | 1 | 1 | clean | normal | 78.5% | 1.6% | 0.1% | 0.645 | 0.06 | no |
| dinov2_small_cls | 1 | 1 | clean | look_alike | 73.0% | 1.4% | 0.5% | 0.645 | 0.06 | no |
| dinov2_small_cls | 1 | 1 | feeder | normal | 68.7% | 1.5% | 0.1% | 0.595 | 0.10 | no |
| dinov2_small_cls | 1 | 1 | feeder | look_alike | 60.8% | 1.3% | 0.3% | 0.595 | 0.10 | no |
| dinov2_small_cls_mean | 1 | 1 | clean | normal | 71.2% | 1.6% | 0.2% | 0.700 | 0.02 | no |
| dinov2_small_cls_mean | 1 | 1 | clean | look_alike | 66.1% | 1.7% | 1.0% | 0.700 | 0.02 | no |
| dinov2_small_cls_mean | 1 | 1 | feeder | normal | 61.2% | 1.4% | 0.3% | 0.665 | 0.00 | no |
| dinov2_small_cls_mean | 1 | 1 | feeder | look_alike | 56.0% | 1.6% | 1.5% | 0.665 | 0.00 | no |
| clip_b32 | 1 | 1 | clean | normal | 40.8% | 2.0% | 0.4% | 0.910 | 0.02 | no |
| clip_b32 | 1 | 1 | clean | look_alike | 34.5% | 1.6% | 1.3% | 0.910 | 0.02 | no |
| clip_b32 | 1 | 1 | feeder | normal | 13.1% | 1.5% | 0.6% | 0.890 | 0.02 | no |
| clip_b32 | 1 | 1 | feeder | look_alike | 11.2% | 1.9% | 1.4% | 0.890 | 0.02 | no |
| dinov2_small_cls | 1 | 2 | clean | normal | 83.9% | 1.8% | 0.0% | 0.630 | 0.04 | no |
| dinov2_small_cls | 1 | 2 | clean | look_alike | 78.9% | 1.6% | 0.5% | 0.630 | 0.04 | no |
| dinov2_small_cls | 1 | 2 | feeder | normal | 74.6% | 1.6% | 0.1% | 0.580 | 0.00 | no |
| dinov2_small_cls | 1 | 2 | feeder | look_alike | 68.0% | 1.4% | 0.9% | 0.580 | 0.00 | no |
| dinov2_small_cls_mean | 1 | 2 | clean | normal | 77.7% | 2.0% | 0.0% | 0.680 | 0.10 | no |
| dinov2_small_cls_mean | 1 | 2 | clean | look_alike | 66.8% | 1.5% | 0.2% | 0.680 | 0.10 | no |
| dinov2_small_cls_mean | 1 | 2 | feeder | normal | 67.8% | 1.8% | 0.1% | 0.645 | 0.06 | no |
| dinov2_small_cls_mean | 1 | 2 | feeder | look_alike | 58.3% | 1.2% | 0.4% | 0.645 | 0.06 | no |
| clip_b32 | 1 | 2 | clean | normal | 46.9% | 2.4% | 0.3% | 0.900 | 0.02 | no |
| clip_b32 | 1 | 2 | clean | look_alike | 37.5% | 1.9% | 1.0% | 0.900 | 0.02 | no |
| clip_b32 | 1 | 2 | feeder | normal | 15.0% | 1.7% | 0.3% | 0.875 | 0.04 | no |
| clip_b32 | 1 | 2 | feeder | look_alike | 10.1% | 1.4% | 0.6% | 0.875 | 0.04 | no |
| dinov2_small_cls | 3 | 1 | clean | normal | 88.1% | 1.7% | 0.0% | 0.675 | 0.08 | no |
| dinov2_small_cls | 3 | 1 | clean | look_alike | 81.6% | 1.4% | 0.2% | 0.675 | 0.08 | no |
| dinov2_small_cls | 3 | 1 | feeder | normal | 78.6% | 1.9% | 0.1% | 0.620 | 0.06 | no |
| dinov2_small_cls | 3 | 1 | feeder | look_alike | 69.7% | 1.7% | 0.2% | 0.620 | 0.06 | no |
| dinov2_small_cls_mean | 3 | 1 | clean | normal | 82.3% | 1.7% | 0.0% | 0.725 | 0.08 | no |
| dinov2_small_cls_mean | 3 | 1 | clean | look_alike | 73.6% | 1.4% | 0.1% | 0.725 | 0.08 | no |
| dinov2_small_cls_mean | 3 | 1 | feeder | normal | 73.4% | 1.7% | 0.1% | 0.685 | 0.04 | no |
| dinov2_small_cls_mean | 3 | 1 | feeder | look_alike | 64.2% | 1.6% | 0.4% | 0.685 | 0.04 | no |
| clip_b32 | 3 | 1 | clean | normal | 56.5% | 1.7% | 0.3% | 0.920 | 0.00 | no |
| clip_b32 | 3 | 1 | clean | look_alike | 46.4% | 2.0% | 1.6% | 0.920 | 0.00 | no |
| clip_b32 | 3 | 1 | feeder | normal | 16.9% | 1.6% | 0.3% | 0.900 | 0.02 | no |
| clip_b32 | 3 | 1 | feeder | look_alike | 12.8% | 1.6% | 1.0% | 0.900 | 0.02 | no |
| dinov2_small_cls | 3 | 2 | clean | normal | 91.5% | 1.6% | 0.0% | 0.665 | 0.10 | yes |
| dinov2_small_cls | 3 | 2 | clean | look_alike | 85.6% | 1.4% | 0.0% | 0.665 | 0.10 | no |
| dinov2_small_cls | 3 | 2 | feeder | normal | 81.5% | 1.6% | 0.0% | 0.610 | 0.08 | no |
| dinov2_small_cls | 3 | 2 | feeder | look_alike | 72.2% | 1.3% | 0.0% | 0.610 | 0.08 | no |
| dinov2_small_cls_mean | 3 | 2 | clean | normal | 85.8% | 1.4% | 0.0% | 0.715 | 0.10 | no |
| dinov2_small_cls_mean | 3 | 2 | clean | look_alike | 76.6% | 1.3% | 0.0% | 0.715 | 0.10 | no |
| dinov2_small_cls_mean | 3 | 2 | feeder | normal | 76.0% | 1.5% | 0.0% | 0.675 | 0.04 | no |
| dinov2_small_cls_mean | 3 | 2 | feeder | look_alike | 67.7% | 1.5% | 0.2% | 0.675 | 0.04 | no |
| clip_b32 | 3 | 2 | clean | normal | 56.0% | 1.4% | 0.0% | 0.910 | 0.04 | no |
| clip_b32 | 3 | 2 | clean | look_alike | 41.2% | 1.3% | 0.1% | 0.910 | 0.04 | no |
| clip_b32 | 3 | 2 | feeder | normal | 17.5% | 1.4% | 0.2% | 0.890 | 0.02 | no |
| clip_b32 | 3 | 2 | feeder | look_alike | 12.9% | 1.2% | 0.7% | 0.890 | 0.02 | no |
| dinov2_small_cls | 5 | 1 | clean | normal | 88.3% | 2.0% | 0.1% | 0.685 | 0.02 | no |
| dinov2_small_cls | 5 | 1 | clean | look_alike | 85.0% | 1.9% | 0.3% | 0.685 | 0.02 | no |
| dinov2_small_cls | 5 | 1 | feeder | normal | 75.9% | 2.1% | 0.0% | 0.625 | 0.10 | no |
| dinov2_small_cls | 5 | 1 | feeder | look_alike | 66.0% | 1.6% | 0.1% | 0.625 | 0.10 | no |
| dinov2_small_cls_mean | 5 | 1 | clean | normal | 82.5% | 1.9% | 0.0% | 0.730 | 0.08 | no |
| dinov2_small_cls_mean | 5 | 1 | clean | look_alike | 75.3% | 1.7% | 0.1% | 0.730 | 0.08 | no |
| dinov2_small_cls_mean | 5 | 1 | feeder | normal | 70.9% | 2.0% | 0.2% | 0.695 | 0.00 | no |
| dinov2_small_cls_mean | 5 | 1 | feeder | look_alike | 64.4% | 1.6% | 0.8% | 0.695 | 0.00 | no |
| clip_b32 | 5 | 1 | clean | normal | 53.2% | 1.7% | 0.3% | 0.925 | 0.00 | no |
| clip_b32 | 5 | 1 | clean | look_alike | 45.2% | 1.4% | 1.5% | 0.925 | 0.00 | no |
| clip_b32 | 5 | 1 | feeder | normal | 16.6% | 1.8% | 0.2% | 0.895 | 0.04 | no |
| clip_b32 | 5 | 1 | feeder | look_alike | 11.3% | 1.4% | 0.4% | 0.895 | 0.04 | no |
| dinov2_small_cls | 5 | 2 | clean | normal | 92.2% | 2.1% | 0.0% | 0.675 | 0.08 | no |
| dinov2_small_cls | 5 | 2 | clean | look_alike | 88.5% | 1.7% | 0.0% | 0.675 | 0.08 | no |
| dinov2_small_cls | 5 | 2 | feeder | normal | 79.6% | 1.8% | 0.0% | 0.620 | 0.06 | no |
| dinov2_small_cls | 5 | 2 | feeder | look_alike | 70.7% | 1.7% | 0.0% | 0.620 | 0.06 | no |
| dinov2_small_cls_mean | 5 | 2 | clean | normal | 87.2% | 2.2% | 0.0% | 0.720 | 0.08 | no |
| dinov2_small_cls_mean | 5 | 2 | clean | look_alike | 81.6% | 1.6% | 0.0% | 0.720 | 0.08 | no |
| dinov2_small_cls_mean | 5 | 2 | feeder | normal | 77.1% | 2.2% | 0.0% | 0.675 | 0.06 | no |
| dinov2_small_cls_mean | 5 | 2 | feeder | look_alike | 67.7% | 1.7% | 0.1% | 0.675 | 0.06 | no |
| clip_b32 | 5 | 2 | clean | normal | 58.0% | 2.1% | 0.0% | 0.910 | 0.04 | no |
| clip_b32 | 5 | 2 | clean | look_alike | 43.9% | 1.4% | 0.1% | 0.910 | 0.04 | no |
| clip_b32 | 5 | 2 | feeder | normal | 20.2% | 2.4% | 0.8% | 0.890 | 0.00 | no |
| clip_b32 | 5 | 2 | feeder | look_alike | 15.7% | 2.1% | 1.8% | 0.890 | 0.00 | no |

## Definitions

1. **right dog accepted**: a home dog is recognized as itself at the first check.
2. **wrong dog accepted**: a home dog is recognized as another home dog (it would eat the other dog's meal).
3. **stranger accepted**: a dog from outside the home is recognized as a home dog.
4. Not accepted means unknown: nothing is served and the feeder checks again a few seconds later.
