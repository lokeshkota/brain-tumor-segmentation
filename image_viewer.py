"""
image_viewer.py — cross-platform replacement for cv2.imshow() + cv2.waitKey()
Displays OpenCV images inside a proper PyQt5 modal dialog so that the macOS
red close button works and no windows get stuck.
"""

import cv2
from PyQt5 import QtCore, QtGui, QtWidgets


def show_cv_image(title: str, cv_img):
    """
    Display an OpenCV image (grayscale or BGR) in a closeable PyQt5 dialog.
    Blocks until the user closes the window (like cv2.waitKey(0)),
    but the close button works correctly on macOS.
    """
    # Convert to RGB for Qt
    if cv_img is None:
        return
    if len(cv_img.shape) == 2:                          # grayscale
        rgb = cv2.cvtColor(cv_img, cv2.COLOR_GRAY2RGB)
    else:                                                # BGR colour
        rgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)

    h, w, ch = rgb.shape
    qt_img = QtGui.QImage(rgb.data.tobytes(), w, h, ch * w, QtGui.QImage.Format_RGB888)
    pixmap = QtGui.QPixmap.fromImage(qt_img)

    dlg = QtWidgets.QDialog()
    dlg.setWindowFlag(QtCore.Qt.Window)
    dlg.setWindowTitle(title)
    dlg.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    lbl = QtWidgets.QLabel(dlg)
    lbl.setPixmap(pixmap)
    lbl.setScaledContents(False)

    layout = QtWidgets.QVBoxLayout(dlg)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(lbl)
    dlg.setLayout(layout)
    dlg.resize(w, h)

    dlg.exec_()   # modal: blocks until user closes the window
