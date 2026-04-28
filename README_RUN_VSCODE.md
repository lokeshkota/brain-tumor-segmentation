# How to run in VS Code

## 1) Open the folder
- Open **VS Code** → **File → Open Folder…** → select the folder: `D7 Program code`

## 2) Create & select a virtual environment (recommended)
- Open the VS Code terminal (``Ctrl+` ``)
- Create venv:
  - **Windows (PowerShell)**:
    ```pwsh
    py -3 -m venv .venv
    .venv\Scripts\Activate.ps1
    ```
  - **macOS / Linux**:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
- In VS Code, select the interpreter: **Ctrl+Shift+P → Python: Select Interpreter → .venv**

## 3) Install dependencies
```bash
pip install -r requirements.txt
```

If OpenCV wheels fail on Apple Silicon, try:
```bash
pip install opencv-python
# or, headless if GUI backends conflict:
# pip install opencv-python-headless
```

## 4) Run
Use one of the two options:
- **Green Run button** (the repo already includes `.vscode/launch.json`):
  - Choose **Run Main.py** to start the full app.
  - Alternatively **Run FuzzyGUI.py** if you want to launch that module directly.
- **Or via terminal**:
  ```bash
  python Main.py
  ```

> Working directory is set to the app folder so relative asset paths like `images/…` and `testimages/…` resolve correctly.

## 5) Optional: Troubleshooting
- If you see Qt platform errors on Linux:
  ```bash
  sudo apt-get install -y libxcb-xinerama0
  ```
- If `cv2` import fails, ensure you are inside the venv and reinstall OpenCV:
  ```bash
  pip uninstall -y opencv-python && pip install opencv-python
  ```

## Notes
- Detected external libs: PyQt5, OpenCV (cv2), imutils, numpy, matplotlib, scikit-image, scikit-fuzzy.
- Likely entry points: `Main.py` (primary), `FuzzyGUI.py`, `ImageAcquisition.py`.
- Assets expected under `images/` and `testimages/`.
