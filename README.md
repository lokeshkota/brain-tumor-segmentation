# 🧠 Brain Tumor Segmentation from MRI using Fuzzy C-Means Clustering

> **Published in AIP Conference Proceedings**  
> *Early Identification of Brain Tumors from MRI Images using Fuzzy C-Means Clustering — Lokesh Kota et al.*

![Accuracy](https://img.shields.io/badge/Accuracy-95.65%25-brightgreen)
![F1 Score](https://img.shields.io/badge/F1--Score-96.24%25-blue)
![IoU](https://img.shields.io/badge/IoU-0.927-orange)
![Publication](https://img.shields.io/badge/Published-AIP%20Conference%20Proceedings-red)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)

---

## 📘 Summary

A complete image-processing pipeline that combines **Fuzzy C-Means (FCM) clustering** with **Canny edge detection** to segment brain tumors in MRI images. The system proposes a hybrid approach — noise removal → contrast enhancement → fuzzy segmentation → thresholding → edge mapping — achieving **95.65% accuracy** and a **96.24% F1-score** across 300+ MRI scans.

The method outperforms traditional threshold-based segmentation and provides robust tumour boundaries even in noisy scans, with an **IoU of 0.927** — significantly above baseline Otsu thresholding (~8% improvement in overlap metrics).

> Submitted as a B.Tech Major Project — Department of Computer Science and Engineering

---

## 📄 Publication

**Early Identification of Brain Tumors from MRI Images using Fuzzy C-Means Clustering**  
Karthik Veeravalli, Lokesh Kota, Ankush Kappe, Rahul Kamishetty  
*AIP Conference Proceedings*  
> *(Add DOI / URL here once available)*

---


## 👥 Authors

| Name | Roll Number | Email |
|------|-------------|-------|
| Karthik Veeravalli | 18241A05N9 | karthikveervalli@gmail.com |
| Lokesh Kota | 18241A05L3 | lokeshkota2101@gmail.com |
| K. Ankush | 18241A05K2 | ankush44.k@gmail.com |
| Kamishetty Rahul | 18241A05K4 | Rahulkamishetty01@gmail.com |

---

## 📄 Abstract

Image processing plays a significant role in applications like computer vision, surveillance and security, video processing, pattern recognition, and more recently, it has gained massive backing in the healthcare industry. A tumor is an abnormal cell growth or mass in parts of the body. Early detection of tumors can have a significant impact on the outcome. Some tumors are benign (non-cancerous), while others are cancerous (malignant).

Conventionally, MRIs are preferred for diagnosing tumors because they produce more detailed images; however, CT scans and PET scans are also used. The task of identifying, segmenting, and detecting the infected area is time-consuming and tedious. This research proposes a method based on **noise removal**, followed by **image enhancement techniques**, and subsequently utilizes **image segmentation procedures** and **edge mapping methods** to identify and chart the delicate edges of an MRI scan — drastically reducing the time medical professionals need to study and comprehend tumors.

**Keywords:** tumor, image processing, Canny edge detection, BCET, healthcare, Fuzzy C-Means, MRI.

---

## 📌 Overview

This is a desktop GUI application built with **Python and PyQt5** implementing the hybrid pipeline proposed in the paper. It processes grayscale MRI brain scans through six sequential stages, progressively isolating tumour regions using classical image processing techniques — no deep learning required.

The system achieved a **95.65% identification accuracy** and an **IoU of 0.927** when tested against 300+ labelled MRI scans sourced from Kaggle.

---

## 🖥️ Application Workflow

```
MRI Image (input)
    │
    ▼
1. Image Acquisition      → Resize to 256×256, convert to grayscale
    │
    ▼
2. Preprocessing
    ├── AMF               → Adaptive Median Filter (noise removal)
    └── BCET              → Balance Contrast Enhancement Technique
    │
    ▼
3. Fuzzy C-Means Clustering → Segment brain tissue regions (2 clusters)
    │
    ▼
4. Thresholding           → Isolate high-intensity tumour regions
    │
    ▼
5. Segmentation           → Overlay FCM + Threshold maps (addWeighted)
    │
    ▼
6. Data Analysis          → Canny edge detection + JET colour map
```

---

## 🔬 Methodology

### Algorithm Overview

```
Step 1: Read the input MRI image of the human brain.
Step 2: Convert the MRI image into grayscale.
Step 3: Resize the grayscaled image to a 256×256 matrix.
Step 4: Remove noise using the Adaptive Median Filter (AMF).
Step 5: Enhance contrast using the Balance Contrast Enhancement Technique (BCET).
Step 6: Compute a global threshold for converting to a binary intensity image.
Step 7: Apply Fuzzy C-Means clustering for morphological segmentation.
Step 8: Detect tumour edges using the Canny edge detection algorithm.
```

---

### Stage 1 — Image Acquisition (`ImageAcquisition.py`)
- Loads the MRI image from disk using OpenCV
- Resizes to a fixed **256 × 256** resolution (`INTER_AREA` interpolation)
- Converts to **grayscale** (integer values 0–255; 0 = black, 255 = white)
- Saves the result as `images/resize.jpg`

---

### Stage 2 — Preprocessing (`Preprocessing.py`, `AMF.py`, `BCET.py`)

#### 2a. Adaptive Median Filter — AMF
- Removes **salt-and-pepper noise** from the grayscale MRI
- Categorises pixels as noise by comparing them to a **12×12 pixel neighbourhood**
- Pixels differing from the majority of neighbours are replaced by the local median
- Saves filtered output as `images/AMF.jpg`

#### 2b. Balance Contrast Enhancement Technique — BCET
- Enhances image contrast using a **parabolic transfer function**:

  ```
  y = a(x − b)² + c
  ```

  where coefficients `a`, `b`, `c` are derived from the image's statistical properties (min, max, mean, mean-square-sum). Target output mean is set to **85** (recommended for MRI).

- Compresses contrast range without altering the input image histogram
- Highlights the white-pixel region of interest relative to surrounding pixels
- Saves output as `images/BCET.jpg`

---

### Stage 3 — Fuzzy C-Means Clustering (`FuzzyClustering.py`, `FuzzyGUI.py`)
- Applies **Fuzzy C-Means (FCM)** clustering to the AMF-filtered image using `scikit-fuzzy`
- Configured with **2 clusters** (0 = brain, 1 = non-brain/skull), fuzziness exponent `m=2`, error tolerance `0.005`, max 1000 iterations
- Post-processing morphological pipeline:
  - **`bwareaopen`** — removes small artefact regions (< 500 px)
  - **`imclearborder`** — removes regions touching the image border
  - **`imfill`** — fills holes inside segmented regions using flood-fill
- Output saved as `images/FCM.jpg`

---

### Stage 4 — Thresholding (`ThresholdGUI.py`)
- Takes the BCET-enhanced image and FCM brain mask as inputs
- Applies **Otsu binarisation** to FCM output to create a binary brain mask
- Masks BCET image to restrict thresholding to the brain region only
- Applies a **92nd-percentile intensity threshold** to isolate bright tumour regions
- Morphological cleanup: **opening** (1 iteration) + **closing** (2 iterations)
- Retains only the **largest connected component** (tumour candidate)
- Output saved as `images/threshld.jpg`

---

### Stage 5 — Segmentation (`AdminHome.py`)
- Combines FCM map and threshold map using `cv2.addWeighted` (FCM: 0.5, threshold: 0.7)
- Produces the final merged segmentation image
- Output saved as `images/segimg.jpg`

---

### Stage 6 — Data Analysis (`AdminHome.py`)
- Applies **Canny edge detection** to the segmented image
- Generates a **JET colour map** overlay for visual tumour boundary analysis

---

## 📊 Results & Performance

Tested against **300+ labelled MRI scans** sourced from Kaggle. ~98% of test inputs matched expected outputs.

### Confusion Matrix

|               | Predicted Positive | Predicted Negative |
|---------------|-------------------|-------------------|
| **Actual Positive** | 64 (TP) | 3 (FN) |
| **Actual Negative** | 2 (FP)  | 46 (TN) |

### Performance Metrics

| Metric | Score |
|--------|-------|
| **Accuracy** | **95.65%** |
| Error Rate | 4.35% |
| **Sensitivity (Recall)** | **96.97%** |
| **Specificity** | **93.88%** |
| **Precision** | **95.52%** |
| **F1 Score (Dice Coefficient)** | **96.24%** |
| **IoU (Intersection-over-Union)** | **0.927** |

### Sample Experimental Results

| Image | Size | Result |
|-------|------|--------|
| IM_0099N | 409×442 | Tumor Absent |
| IM_0096N | 550×664 | Tumor Absent |
| IM_0012B | 825×993 | **Tumor Present** |
| IM_0090N | 630×630 | Tumor Absent |
| IM_0017C | 400×369 | **Tumor Present** |
| IM_0253Z | 283×338 | **Tumor Present** |

---

## 🗂️ Project Structure

```
Brain Tumor Detect/
│
├── Main.py                  # Entry point — main login screen
├── Admin.py                 # Admin login dialog (user: admin / pass: admin)
├── AdminHome.py             # Admin dashboard — triggers all pipeline stages
│
├── ImageAcquisition.py      # Stage 1: Load, resize & grayscale the MRI
├── Preprocessing.py         # Stage 2: AMF + BCET preprocessing GUI
├── FuzzyGUI.py              # Stage 3: Fuzzy C-Means GUI trigger
├── ThresholdGUI.py          # Stage 4: Thresholding GUI + logic
│
├── AMF.py                   # Algorithm: Adaptive Median Filter
├── BCET.py                  # Algorithm: Balance Contrast Enhancement
├── FuzzyClustering.py       # Algorithm: Fuzzy C-Means + morphological ops
├── Threshold.py             # Standalone threshold script (dev/reference)
├── Detetction.py            # Standalone detection script (dev/reference)
│
├── image_viewer.py          # Utility: PyQt5-based image display (macOS fix)
│
├── images/                  # Runtime output images (generated during pipeline)
├── testimages/              # Sample MRI test images
│
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.9 or higher
- macOS, Windows, or Linux

### 1. Clone the Repository
```bash
git clone https://github.com/lokeshkota/<repo-name>.git
cd <repo-name>
```

### 2. Create a Virtual Environment
```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

> **Note for Apple Silicon (M1/M2/M3):** Pin OpenCV to avoid numpy conflicts:
> ```bash
> pip install opencv-python==4.9.0.80 "numpy<2.0"
> ```

### 4. Run the Application
```bash
python Main.py
```

---

## 🔐 Login Credentials

| Field    | Value   |
|----------|---------|
| Username | `admin` |
| Password | `admin` |

---

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `PyQt5` | ≥ 5.15 | Desktop GUI framework |
| `opencv-python` | 4.9.0.80 | Image I/O and processing |
| `numpy` | < 2.0 | Numerical array operations |
| `scikit-fuzzy` | ≥ 0.4 | Fuzzy C-Means clustering |
| `scikit-image` | ≥ 0.24 | Image exposure utilities |
| `matplotlib` | ≥ 3.9 | Plotting support |
| `imutils` | ≥ 0.5 | OpenCV convenience utilities |

---

## 🖼️ Using the Application

1. **Launch** `python Main.py` — the main screen appears
2. **Click the doctor icon** to open the Admin Login
3. **Enter credentials** (`admin` / `admin`) and click Login
4. From **Admin Home**, run each stage **in order**:

| Button | What it does |
|--------|-------------|
| Image Acquisition | Load & prepare your MRI image (browse from `testimages/`) |
| Preprocessing → AMF | Apply Adaptive Median Filter (noise removal) |
| Preprocessing → BCET | Apply Balance Contrast Enhancement |
| Fuzzy C-Means | Run FCM clustering to segment brain tissue |
| Thresholding | Isolate the tumour region |
| Segmentation | Overlay FCM + threshold maps |
| Data Analysis | Canny edge map + JET colour visualisation |

> ⚠️ **Run stages in order** — each stage depends on the output image from the previous one stored in `images/`.

---

## 🐛 Platform Notes & Fixes

| Issue | Platform | Fix Applied |
|-------|----------|-------------|
| Image windows freeze / can't be closed | macOS | Replaced all `cv2.imshow()` + `cv2.waitKey(0)` with `image_viewer.py` (PyQt5-based display) |
| `QDialog` red close button unresponsive | macOS | Added `Qt.Window` flag in all `setupUi()` methods |
| `"Vani"` font warning at startup | macOS | Cosmetic only — falls back to system font, no impact on functionality |
| `numpy` conflict with `opencv-python ≥ 4.10` | All | Pin to `opencv-python==4.9.0.80` (supports `numpy < 2.0`) |

---

## 📚 References

1. [Brain Tumor: Statistics | Cancer.Net](https://www.cancer.net/cancer-types/brain-tumor/statistics)
2. [Brain Tumors and Brain Cancer | Johns Hopkins Medicine](https://www.hopkinsmedicine.org/health/conditions-and-diseases/brain-tumor)
3. Louis et al., "The 2021 WHO Classification of Tumors of the Central Nervous System," *Neuro-Oncology*, Vol. 23, Issue 8, Aug 2021, pp. 1231–1251.
4. Kovasznay & Joseph, "Image Processing," *Proceedings of the IRE*, vol. 43, no. 5, pp. 560–570, May 1955.
5. Abubakar, "A study of region-based and contour-based image segmentation," *Signal & Image Processing* 3.6 (2012): 15.
6. Kumar et al., "Brain Tumor Detection Using Image Processing."
7. [Self-organizing Maps (hmc.edu)](https://www.cs.hmc.edu/~kpang/nn/som.html)
8. Shah et al., "Brain Tumor Detection from MRI Images using Fuzzy C-Means Segmentation," *IJARCCE*, Vol. 5, Issue 6, June 2016.
9. [Balance Contrast Enhancement Technique (BCET) | imageeprocessing.com](http://www.imageeprocessing.com/2013/06/balance-contrast-enhancement-technique.html)
10. Sawant et al., "Brain cancer detection from MRI: A machine learning approach (TensorFlow)," *Brain* 5.04 (2018).
11. Abdel-Maksoud, Elmogy & Al-Awadi, "Brain tumor segmentation based on a hybrid clustering technique," *Egyptian Informatics Journal*, Vol. 16, Issue 1, 2015, pp. 71–81.
12. Pal, "Brain tumor detection using thresholding and watershed algorithm," *Journal Of Engineering & Technology*, Vol. 5, Issue 2, 2019.
13. Verma, Singh & Thoke, "An Enhancement in Adaptive Median Filter for Edge Preservation," *Procedia Computer Science*, Vol. 48, 2015, pp. 29–36.
14. Cannon, Dave & Bezdek, "Efficient implementation of the fuzzy c-means clustering algorithms," *IEEE TPAMI* 2 (1986): 248–255.
15. Ghosh & Dubey, "Comparative analysis of k-means and fuzzy c-means algorithms," *IJACSA* 4.4 (2013).
16. Oliva et al., "Multilevel thresholding segmentation based on harmony search optimization," *Journal of Applied Mathematics* 2013.
17. Xuan & Hong, "An improved Canny edge detection algorithm," *2017 8th IEEE ICSESS*, IEEE, 2017.
18. Mayer & Guderlei, "On Random Testing of Image Processing Applications," *QSIC 2006*, pp. 85–92.
19. [Brain MRI Images for Brain Tumor Detection | Kaggle](https://www.kaggle.com/navoneel/brain-mri-images-for-brain-tumor-detection)
20. [Brain Tumor MRI Dataset | Kaggle](https://www.kaggle.com/sartajbhuvaji/brain-tumor-classification-mri)
21. [guillaumefrd/brain-tumor-mri-dataset | GitHub](https://github.com/guillaumefrd/brain-tumor-mri-dataset)
22. Akar et al., "Fractal analysis of MR images in patients with Chiari malformation," *Biomedical Signal Processing and Control* 31 (2017): 63–70.
23. [Image Processing 101 Chapter 1.3: Color Space Conversion | Dynamsoft Blog](https://www.dynamsoft.com/blog/insights/image-processing/image-processing-101-color-space-conversion/)
24. [Brain Tumor Classification (MRI) | Kaggle](https://www.kaggle.com/sartajbhuvaji/brain-tumor-classification-mri)
25. [Generalized Intersection over Union (arxiv.org)](https://arxiv.org/abs/1902.09630)
26. Zou et al., "Statistical validation of image segmentation quality based on a spatial overlap index," *Acad Radiol.* 2004; 11(2):178–189.

---

## 📄 License

This project was developed for academic purposes as a B.Tech major project in the Department of Computer Science and Engineering. All rights reserved by the respective authors.

---

*For questions, open a GitHub issue or reach out to the authors directly via the emails listed above.*
