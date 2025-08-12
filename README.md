# Docker Tutorial of SegRap2025
This repository provides a template to build Docker for SegRap2025 final submission, which you can use as a 
starting point to develop your own final submitted algorithm.

## Description of the File Structure During the Final Test
The test set of **Task01: GTV segmentation** consist of paired CT and ceCT images from two cohorts, and the image are organized as follows:
```
test
 ├──input
 |   ├──Cohort1
 |   |   └──image
 |   |       ├──segrap_****
 |   |       |   ├──image.nii.gz
 |   |       |   └──image_contrast.nii.gz
 |   |       └──...
 |   └──Cohort2
 |       └──image
 |           ├──segrap_****
 |           |   ├──image.nii.gz
 |           |   └──image_contrast.nii.gz
 |           └──...
 └──output
```
The test set of **Task02: LN CTV Segmentation** consist of three kinds of cases: paired CT and ceCT (segrap_\*\*\*\*), only CT (segrap_nc_\*\*\*\*), and only ceCT (segrap_ce_\*\*\*\*).
```
test
 ├──input
 |   └──image
 |       ├──segrap_****
 |       |   ├──image.nii.gz
 |       |   └──image_contrast.nii.gz
 |       ├──segrap_nc_****
 |       |   └──image.nii.gz
 |       ├──segrap_ce_****
 |       |   └──image_contrast.nii.gz
 |       └──...
 └──output
```

## Challenge and Dataset
For any information about the challenge, please visit the [official website](https://hilab-git.github.io/SegRap2025_Challenge/index.html).

