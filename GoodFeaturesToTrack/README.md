# goodFeaturesToTrack – OpenCV

## Overview

`goodFeaturesToTrack` is a feature detection algorithm in OpenCV used to identify strong, trackable points (corners) in an image. These points are typically used as input for tracking algorithms such as optical flow (e.g., Lucas-Kanade method).

It is commonly used in computer vision tasks where stable visual features are required across multiple frames.

---

## What it does

The function analyzes an image and selects pixels that:

- Have high intensity variation in multiple directions
- Represent corners or distinct texture points
- Are stable enough to be tracked over time

These points are often called **keypoints** or **feature points**.

---

## Typical Use Cases

- Object tracking in video sequences
- Motion estimation
- Camera stabilization
- Structure from motion (SfM)
- Augmented reality tracking systems

---

## How it works (conceptually)

The algorithm is based on the idea that good features are points where the image gradient changes significantly in both x and y directions.

In simplified terms:

1. Compute image gradients
2. Evaluate corner strength (Shi-Tomasi or Harris-like scoring)
3. Select strongest points
4. Apply non-maximum suppression to avoid clustered points

---

## OpenCV Function Signature

```python
cv2.goodFeaturesToTrack(
    image, #input gray scale image
    maxCorners, #maximum number of corners to return
    qualityLevel, #minimum accepted quality (0-1)
    minDistance, #minimim distens between detected corners
    mask=None, #optinal region of intrest
    blockSize=3, #Neighborhood size used for computing derivatives
    useHarrisDetector=False, #If true, uses Harris corner detector instead of Shi-Tomasi
    k=0.04 #Harris detector free parameter
)