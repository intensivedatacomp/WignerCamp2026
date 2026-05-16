import numpy as np
from scipy.signal import find_peaks

#|%%--%%| <AdpaCiBCw2|CNsNDF7L4c>
# ==============================================================
# height parameter
# ==============================================================

x = np.array([1, 3, 1, 4, 1, 2, 1])
# Peaks at indices 1 (value 3), 3 (value 4), 5 (value 2).

peaks, _ = find_peaks(x, height=2.5)
print("height=2.5:      ", peaks)   # [1, 3]

peaks, _ = find_peaks(x, height=(2.0, 3.5))
print("height=(2.0,3.5):", peaks)   # [1, 5]

#|%%--%%| <CNsNDF7L4c|ZcrmmHVA5A>
# ==============================================================
# threshold parameter
# ==============================================================

x = np.array([0, 2, 1, 3, 0])
# Peak at index 1: left drop=2, right drop=1.
# Peak at index 3: left drop=2, right drop=3.

peaks, _ = find_peaks(x, threshold=1.5)
print("\nthreshold=1.5:   ", peaks)  # [3]

#|%%--%%| <ZcrmmHVA5A|Q2lmhpcYXZ>
# ==============================================================
# distance parameter
# ==============================================================

x = np.array([0, 3, 1, 4, 1, 3, 0])
# Peaks at indices 1 (3), 3 (4), 5 (3).

peaks, _ = find_peaks(x)
print("\ndistance=None:   ", peaks)  # [1, 3, 5]

peaks, _ = find_peaks(x, distance=3)
print("distance=3:      ", peaks)   # [3]

#|%%--%%| <Q2lmhpcYXZ|uybcaQIII5>
# ==============================================================
# prominence parameter
# ==============================================================

x = np.array([0, 1, 0, 5, 1, 4, 0])
# Prominences: index 1 -> 1.0, index 3 -> 5.0, index 5 -> 3.0.

peaks, props = find_peaks(x, prominence=2)
print("\nprominence=2:    ", peaks)              # [3, 5]
print("prominences:     ", props['prominences']) # [5. 3.]

#|%%--%%| <uybcaQIII5|QUgVvYh6Jm>
# ==============================================================
# width and rel_height parameters
# ==============================================================

x = np.array([0, 0, 5, 0, 0])
# Single sharp peak at index 2, prominence=5.

peaks, props = find_peaks(x, width=0, rel_height=0.5)
print("\nwidth=0, rel_height=0.5: width =", props['widths'])  # ~1.0

peaks, props = find_peaks(x, width=0, rel_height=0.9)
print("width=0, rel_height=0.9: width =", props['widths'])   # ~1.8

#|%%--%%| <QUgVvYh6Jm|pAVDrjlGhA>
# ==============================================================
# plateau_size parameter
# ==============================================================

x = np.array([0, 2, 2, 2, 0, 3, 0])
# Flat-top peak at indices 1-3 (plateau size 3).
# Sharp peak at index 5 (plateau size 1).

peaks, _ = find_peaks(x, plateau_size=2)
print("\nplateau_size=2:  ", peaks)  # [2]

#|%%--%%| <pAVDrjlGhA|lpV2lFOAA7>
# ==============================================================
# Combining multiple parameters
# ==============================================================

rng = np.random.default_rng(42)
t = np.linspace(0, 10 * np.pi, 500)
x = np.sin(t) + 0.3 * rng.standard_normal(500)

peaks, props = find_peaks(
    x,
    height=0.5,
    distance=20,
    prominence=0.5,
    width=3
)
print("\nCombined filtering:")
print("peaks:", peaks)

#|%%--%%| <lpV2lFOAA7|0zV8vkqdJ3>
# ==============================================================
# Exercise 1 -- Predict the output
# ==============================================================

x = np.array([0, 1, 0, 3, 2, 4, 0, 2, 0])

peaks, _ = find_peaks(x, height=2.5)
print("\nEx1 (a) height=2.5:    ", peaks)  # [3, 5]

peaks, _ = find_peaks(x, threshold=1.5)
print("Ex1 (b) threshold=1.5: ", peaks)   # [5, 7]

#|%%--%%| <0zV8vkqdJ3|3GKom3L4FO>
# ==============================================================
# Exercise 2 -- Prominence by hand
# ==============================================================

x = np.array([0, 4, 1, 3, 0])

peaks, props = find_peaks(x, prominence=0)
print("\nEx2 all peaks:   ", peaks)
print("prominences:     ", props['prominences'])  # [4. 2.]

peaks, _ = find_peaks(x, prominence=2.5)
print("Ex2 prominence=2.5:", peaks)  # [1]

#|%%--%%| <3GKom3L4FO|uUMLZRezqD>
# ==============================================================
# Exercise 3 -- Choose the right parameters
# ==============================================================

x = np.array([0, 2, 0, 1, 0, 3, 0, 7, 0, 2, 0, 6, 0, 1, 0])

peaks, _ = find_peaks(x, height=3.5)
print("\nEx3 (a) height=3.5:     ", peaks)  # [7, 11]

peaks, _ = find_peaks(x, prominence=3.5)
print("Ex3 (b) prominence=3.5: ", peaks)   # [7, 11]

