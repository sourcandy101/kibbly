# Dog recognition evaluation

Timestamp: 2026-11-09T17:35:09  
Data: DogFaceNet (CC BY 4.0), 301 calibration dogs and 302 different test dogs, 1500 simulated homes per setting, seed 7.

Targets: right dog accepted at least 90.0%, strangers and wrong dogs accepted at most 2.0%. Thresholds are chosen on calibration dogs and measured on test dogs.
## 1. Model comparison

3 enrollment photos, 1 photo per check, feeder camera simulation, normal homes.
| model | right dog accepted | stranger accepted | wrong dog accepted | threshold | margin | meets targets |
|---|---|---|---|---|---|---|
| dinov2_small_cls_proj | 88.6% | 2.2% | 0.1% | 0.490 | 0.02 | no |
| dinov2_small_cls | 77.2% | 1.7% | 0.1% | 0.615 | 0.02 | no |
| dinov2_small_cls_mean | 72.1% | 1.6% | 0.1% | 0.680 | 0.04 | no |
| clip_b32 | 17.9% | 2.0% | 0.8% | 0.900 | 0.00 | no |

Best model: **dinov2_small_cls_proj**.

## 2. dinov2_small_cls_proj: photos per dog, photos per check, image quality

Normal homes.
| enroll photos | photos per check | query images | right dog accepted | stranger accepted | wrong dog accepted | threshold | margin | meets targets |
|---|---|---|---|---|---|---|---|---|
| 1 | 1 | clean | 89.3% | 2.2% | 0.2% | 0.490 | 0.02 | no |
| 1 | 1 | feeder | 83.2% | 2.2% | 0.1% | 0.460 | 0.06 | no |
| 1 | 2 | clean | 90.8% | 1.5% | 0.0% | 0.490 | 0.00 | yes |
| 1 | 2 | feeder | 85.6% | 1.6% | 0.0% | 0.450 | 0.08 | no |
| 3 | 1 | clean | 93.8% | 1.8% | 0.0% | 0.530 | 0.04 | yes |
| 3 | 1 | feeder | 88.6% | 2.2% | 0.1% | 0.490 | 0.02 | no |
| 3 | 2 | clean | 96.6% | 1.8% | 0.0% | 0.525 | 0.00 | yes |
| 3 | 2 | feeder | 91.3% | 2.1% | 0.0% | 0.485 | 0.08 | no |
| 5 | 1 | clean | 92.8% | 1.6% | 0.0% | 0.550 | 0.06 | yes |
| 5 | 1 | feeder | 85.3% | 1.7% | 0.1% | 0.515 | 0.00 | no |
| 5 | 2 | clean | 94.4% | 1.5% | 0.0% | 0.560 | 0.00 | yes |
| 5 | 2 | feeder | 86.7% | 1.5% | 0.0% | 0.515 | 0.00 | no |

## 3. dinov2_small_cls_proj: look alike homes (similar coat colors)

Same thresholds as normal homes, feeder camera simulation.
| enroll photos | photos per check | homes | right dog accepted | stranger accepted | wrong dog accepted | threshold | margin | meets targets |
|---|---|---|---|---|---|---|---|---|
| 1 | 1 | normal | 83.2% | 2.2% | 0.1% | 0.460 | 0.06 | no |
| 1 | 1 | look_alike | 76.8% | 2.1% | 0.4% | 0.460 | 0.06 | no |
| 1 | 2 | normal | 85.6% | 1.6% | 0.0% | 0.450 | 0.08 | no |
| 1 | 2 | look_alike | 80.3% | 1.7% | 0.1% | 0.450 | 0.08 | no |
| 3 | 1 | normal | 88.6% | 2.2% | 0.1% | 0.490 | 0.02 | no |
| 3 | 1 | look_alike | 84.1% | 1.8% | 0.2% | 0.490 | 0.02 | no |
| 3 | 2 | normal | 91.3% | 2.1% | 0.0% | 0.485 | 0.08 | no |
| 3 | 2 | look_alike | 86.6% | 1.8% | 0.0% | 0.485 | 0.08 | no |
| 5 | 1 | normal | 85.3% | 1.7% | 0.1% | 0.515 | 0.00 | no |
| 5 | 1 | look_alike | 81.1% | 1.9% | 0.2% | 0.515 | 0.00 | no |
| 5 | 2 | normal | 86.7% | 1.5% | 0.0% | 0.515 | 0.00 | no |
| 5 | 2 | look_alike | 82.7% | 1.5% | 0.0% | 0.515 | 0.00 | no |

## 4. All models, every setting

| model | enroll | frames | images | homes | right dog accepted | stranger accepted | wrong dog accepted | threshold | margin | meets targets |
|---|---|---|---|---|---|---|---|---|---|---|
| dinov2_small_cls_proj | 1 | 1 | clean | normal | 89.3% | 2.2% | 0.2% | 0.490 | 0.02 | no |
| dinov2_small_cls_proj | 1 | 1 | clean | look_alike | 85.4% | 2.1% | 0.5% | 0.490 | 0.02 | no |
| dinov2_small_cls_proj | 1 | 1 | feeder | normal | 83.2% | 2.2% | 0.1% | 0.460 | 0.06 | no |
| dinov2_small_cls_proj | 1 | 1 | feeder | look_alike | 76.8% | 2.1% | 0.4% | 0.460 | 0.06 | no |
| dinov2_small_cls | 1 | 1 | clean | normal | 79.6% | 2.0% | 0.1% | 0.635 | 0.06 | no |
| dinov2_small_cls | 1 | 1 | clean | look_alike | 74.0% | 1.7% | 0.4% | 0.635 | 0.06 | no |
| dinov2_small_cls | 1 | 1 | feeder | normal | 71.4% | 2.0% | 0.2% | 0.585 | 0.04 | no |
| dinov2_small_cls | 1 | 1 | feeder | look_alike | 63.9% | 2.0% | 0.6% | 0.585 | 0.04 | no |
| dinov2_small_cls_mean | 1 | 1 | clean | normal | 70.6% | 2.0% | 0.1% | 0.690 | 0.10 | no |
| dinov2_small_cls_mean | 1 | 1 | clean | look_alike | 62.5% | 1.7% | 0.2% | 0.690 | 0.10 | no |
| dinov2_small_cls_mean | 1 | 1 | feeder | normal | 63.9% | 2.2% | 0.1% | 0.650 | 0.08 | no |
| dinov2_small_cls_mean | 1 | 1 | feeder | look_alike | 55.1% | 1.9% | 0.4% | 0.650 | 0.08 | no |
| clip_b32 | 1 | 1 | clean | normal | 39.9% | 2.0% | 0.4% | 0.910 | 0.02 | no |
| clip_b32 | 1 | 1 | clean | look_alike | 33.1% | 1.6% | 1.0% | 0.910 | 0.02 | no |
| clip_b32 | 1 | 1 | feeder | normal | 15.1% | 2.3% | 1.0% | 0.890 | 0.00 | no |
| clip_b32 | 1 | 1 | feeder | look_alike | 12.6% | 2.1% | 1.9% | 0.890 | 0.00 | no |
| dinov2_small_cls_proj | 1 | 2 | clean | normal | 90.8% | 1.5% | 0.0% | 0.490 | 0.00 | yes |
| dinov2_small_cls_proj | 1 | 2 | clean | look_alike | 87.8% | 1.6% | 0.3% | 0.490 | 0.00 | no |
| dinov2_small_cls_proj | 1 | 2 | feeder | normal | 85.6% | 1.6% | 0.0% | 0.450 | 0.08 | no |
| dinov2_small_cls_proj | 1 | 2 | feeder | look_alike | 80.3% | 1.7% | 0.1% | 0.450 | 0.08 | no |
| dinov2_small_cls | 1 | 2 | clean | normal | 82.3% | 1.3% | 0.1% | 0.630 | 0.00 | no |
| dinov2_small_cls | 1 | 2 | clean | look_alike | 79.0% | 1.6% | 0.4% | 0.630 | 0.00 | no |
| dinov2_small_cls | 1 | 2 | feeder | normal | 75.7% | 1.6% | 0.1% | 0.565 | 0.10 | no |
| dinov2_small_cls | 1 | 2 | feeder | look_alike | 67.5% | 1.7% | 0.1% | 0.565 | 0.10 | no |
| dinov2_small_cls_mean | 1 | 2 | clean | normal | 75.2% | 1.6% | 0.0% | 0.680 | 0.08 | no |
| dinov2_small_cls_mean | 1 | 2 | clean | look_alike | 69.7% | 1.9% | 0.2% | 0.680 | 0.08 | no |
| dinov2_small_cls_mean | 1 | 2 | feeder | normal | 67.1% | 1.7% | 0.0% | 0.635 | 0.10 | no |
| dinov2_small_cls_mean | 1 | 2 | feeder | look_alike | 58.4% | 1.7% | 0.1% | 0.635 | 0.10 | no |
| clip_b32 | 1 | 2 | clean | normal | 43.0% | 1.5% | 0.1% | 0.900 | 0.04 | no |
| clip_b32 | 1 | 2 | clean | look_alike | 33.7% | 1.5% | 0.3% | 0.900 | 0.04 | no |
| clip_b32 | 1 | 2 | feeder | normal | 15.2% | 2.0% | 0.6% | 0.880 | 0.00 | no |
| clip_b32 | 1 | 2 | feeder | look_alike | 13.6% | 1.9% | 1.5% | 0.880 | 0.00 | no |
| dinov2_small_cls_proj | 3 | 1 | clean | normal | 93.8% | 1.8% | 0.0% | 0.530 | 0.04 | yes |
| dinov2_small_cls_proj | 3 | 1 | clean | look_alike | 91.3% | 1.7% | 0.1% | 0.530 | 0.04 | yes |
| dinov2_small_cls_proj | 3 | 1 | feeder | normal | 88.6% | 2.2% | 0.1% | 0.490 | 0.02 | no |
| dinov2_small_cls_proj | 3 | 1 | feeder | look_alike | 84.1% | 1.8% | 0.2% | 0.490 | 0.02 | no |
| dinov2_small_cls | 3 | 1 | clean | normal | 87.8% | 1.6% | 0.1% | 0.670 | 0.00 | no |
| dinov2_small_cls | 3 | 1 | clean | look_alike | 85.1% | 1.8% | 0.3% | 0.670 | 0.00 | no |
| dinov2_small_cls | 3 | 1 | feeder | normal | 77.2% | 1.7% | 0.1% | 0.615 | 0.02 | no |
| dinov2_small_cls | 3 | 1 | feeder | look_alike | 71.0% | 1.8% | 0.4% | 0.615 | 0.02 | no |
| dinov2_small_cls_mean | 3 | 1 | clean | normal | 82.0% | 1.7% | 0.1% | 0.720 | 0.00 | no |
| dinov2_small_cls_mean | 3 | 1 | clean | look_alike | 78.2% | 1.8% | 0.4% | 0.720 | 0.00 | no |
| dinov2_small_cls_mean | 3 | 1 | feeder | normal | 72.1% | 1.6% | 0.1% | 0.680 | 0.04 | no |
| dinov2_small_cls_mean | 3 | 1 | feeder | look_alike | 65.1% | 1.6% | 0.2% | 0.680 | 0.04 | no |
| clip_b32 | 3 | 1 | clean | normal | 53.2% | 1.6% | 0.1% | 0.920 | 0.02 | no |
| clip_b32 | 3 | 1 | clean | look_alike | 44.0% | 1.5% | 0.4% | 0.920 | 0.02 | no |
| clip_b32 | 3 | 1 | feeder | normal | 17.9% | 2.0% | 0.8% | 0.900 | 0.00 | no |
| clip_b32 | 3 | 1 | feeder | look_alike | 15.0% | 2.0% | 1.6% | 0.900 | 0.00 | no |
| dinov2_small_cls_proj | 3 | 2 | clean | normal | 96.6% | 1.8% | 0.0% | 0.525 | 0.00 | yes |
| dinov2_small_cls_proj | 3 | 2 | clean | look_alike | 94.9% | 1.9% | 0.1% | 0.525 | 0.00 | yes |
| dinov2_small_cls_proj | 3 | 2 | feeder | normal | 91.3% | 2.1% | 0.0% | 0.485 | 0.08 | no |
| dinov2_small_cls_proj | 3 | 2 | feeder | look_alike | 86.6% | 1.8% | 0.0% | 0.485 | 0.08 | no |
| dinov2_small_cls | 3 | 2 | clean | normal | 91.8% | 1.8% | 0.1% | 0.660 | 0.00 | yes |
| dinov2_small_cls | 3 | 2 | clean | look_alike | 89.9% | 1.9% | 0.2% | 0.660 | 0.00 | no |
| dinov2_small_cls | 3 | 2 | feeder | normal | 82.2% | 1.9% | 0.0% | 0.600 | 0.06 | no |
| dinov2_small_cls | 3 | 2 | feeder | look_alike | 74.3% | 1.8% | 0.1% | 0.600 | 0.06 | no |
| dinov2_small_cls_mean | 3 | 2 | clean | normal | 87.3% | 1.8% | 0.1% | 0.710 | 0.02 | no |
| dinov2_small_cls_mean | 3 | 2 | clean | look_alike | 83.0% | 2.2% | 0.1% | 0.710 | 0.02 | no |
| dinov2_small_cls_mean | 3 | 2 | feeder | normal | 78.2% | 2.0% | 0.2% | 0.665 | 0.00 | no |
| dinov2_small_cls_mean | 3 | 2 | feeder | look_alike | 70.1% | 2.2% | 0.3% | 0.665 | 0.00 | no |
| clip_b32 | 3 | 2 | clean | normal | 54.8% | 1.6% | 0.0% | 0.910 | 0.04 | no |
| clip_b32 | 3 | 2 | clean | look_alike | 43.8% | 1.1% | 0.0% | 0.910 | 0.04 | no |
| clip_b32 | 3 | 2 | feeder | normal | 21.9% | 2.4% | 0.2% | 0.885 | 0.02 | no |
| clip_b32 | 3 | 2 | feeder | look_alike | 17.5% | 1.9% | 0.7% | 0.885 | 0.02 | no |
| dinov2_small_cls_proj | 5 | 1 | clean | normal | 92.8% | 1.6% | 0.0% | 0.550 | 0.06 | yes |
| dinov2_small_cls_proj | 5 | 1 | clean | look_alike | 91.6% | 1.8% | 0.0% | 0.550 | 0.06 | yes |
| dinov2_small_cls_proj | 5 | 1 | feeder | normal | 85.3% | 1.7% | 0.1% | 0.515 | 0.00 | no |
| dinov2_small_cls_proj | 5 | 1 | feeder | look_alike | 81.1% | 1.9% | 0.2% | 0.515 | 0.00 | no |
| dinov2_small_cls | 5 | 1 | clean | normal | 88.0% | 1.7% | 0.0% | 0.680 | 0.06 | no |
| dinov2_small_cls | 5 | 1 | clean | look_alike | 85.5% | 1.7% | 0.1% | 0.680 | 0.06 | no |
| dinov2_small_cls | 5 | 1 | feeder | normal | 74.5% | 2.0% | 0.2% | 0.630 | 0.00 | no |
| dinov2_small_cls | 5 | 1 | feeder | look_alike | 68.3% | 1.7% | 0.4% | 0.630 | 0.00 | no |
| dinov2_small_cls_mean | 5 | 1 | clean | normal | 82.1% | 2.0% | 0.1% | 0.730 | 0.02 | no |
| dinov2_small_cls_mean | 5 | 1 | clean | look_alike | 78.2% | 1.9% | 0.2% | 0.730 | 0.02 | no |
| dinov2_small_cls_mean | 5 | 1 | feeder | normal | 70.3% | 2.0% | 0.0% | 0.690 | 0.04 | no |
| dinov2_small_cls_mean | 5 | 1 | feeder | look_alike | 63.3% | 1.7% | 0.2% | 0.690 | 0.04 | no |
| clip_b32 | 5 | 1 | clean | normal | 49.9% | 1.4% | 0.2% | 0.925 | 0.00 | no |
| clip_b32 | 5 | 1 | clean | look_alike | 44.2% | 1.6% | 0.5% | 0.925 | 0.00 | no |
| clip_b32 | 5 | 1 | feeder | normal | 17.0% | 2.0% | 0.4% | 0.900 | 0.02 | no |
| clip_b32 | 5 | 1 | feeder | look_alike | 14.3% | 2.0% | 0.7% | 0.900 | 0.02 | no |
| dinov2_small_cls_proj | 5 | 2 | clean | normal | 94.4% | 1.5% | 0.0% | 0.560 | 0.00 | yes |
| dinov2_small_cls_proj | 5 | 2 | clean | look_alike | 93.3% | 1.6% | 0.0% | 0.560 | 0.00 | yes |
| dinov2_small_cls_proj | 5 | 2 | feeder | normal | 86.7% | 1.5% | 0.0% | 0.515 | 0.00 | no |
| dinov2_small_cls_proj | 5 | 2 | feeder | look_alike | 82.7% | 1.5% | 0.0% | 0.515 | 0.00 | no |
| dinov2_small_cls | 5 | 2 | clean | normal | 88.9% | 1.5% | 0.0% | 0.680 | 0.08 | no |
| dinov2_small_cls | 5 | 2 | clean | look_alike | 88.1% | 1.6% | 0.0% | 0.680 | 0.08 | no |
| dinov2_small_cls | 5 | 2 | feeder | normal | 74.2% | 1.4% | 0.0% | 0.620 | 0.10 | no |
| dinov2_small_cls | 5 | 2 | feeder | look_alike | 67.4% | 1.4% | 0.0% | 0.620 | 0.10 | no |
| dinov2_small_cls_mean | 5 | 2 | clean | normal | 83.6% | 1.5% | 0.0% | 0.730 | 0.04 | no |
| dinov2_small_cls_mean | 5 | 2 | clean | look_alike | 81.3% | 1.7% | 0.0% | 0.730 | 0.04 | no |
| dinov2_small_cls_mean | 5 | 2 | feeder | normal | 72.1% | 1.8% | 0.1% | 0.680 | 0.00 | no |
| dinov2_small_cls_mean | 5 | 2 | feeder | look_alike | 66.0% | 1.7% | 0.1% | 0.680 | 0.00 | no |
| clip_b32 | 5 | 2 | clean | normal | 49.6% | 1.1% | 0.0% | 0.915 | 0.04 | no |
| clip_b32 | 5 | 2 | clean | look_alike | 42.3% | 1.1% | 0.0% | 0.915 | 0.04 | no |
| clip_b32 | 5 | 2 | feeder | normal | 17.4% | 1.8% | 0.1% | 0.890 | 0.02 | no |
| clip_b32 | 5 | 2 | feeder | look_alike | 15.1% | 1.4% | 0.2% | 0.890 | 0.02 | no |

## Definitions

1. **right dog accepted**: a home dog is recognized as itself at the first check.
2. **wrong dog accepted**: a home dog is recognized as another home dog (it would eat the other dog's meal).
3. **stranger accepted**: a dog from outside the home is recognized as a home dog.
4. Not accepted means unknown: nothing is served and the feeder checks again a few seconds later.
