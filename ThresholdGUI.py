from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
import numpy as np
import sys
from image_viewer import show_cv_image

class Ui_ThresholdGUI(object):
    def __init__(self, Dialog):
        self.dialog = Dialog

    # AdminHome sometimes calls processimg(), your traceback shows processing()
    def processimg(self):
        self.lineEdit.setText("images/FCM.jpg")


    def processing(self):
        self.processimg()

    def submit(self):
        try:
            import os
            import cv2
            import numpy as np

            bcet_path = os.path.join("images", "BCET.jpg")
            fcm_path  = os.path.join("images", "FCM.jpg")

            bcet = cv2.imread(bcet_path, cv2.IMREAD_GRAYSCALE)
            fcm  = cv2.imread(fcm_path,  cv2.IMREAD_GRAYSCALE)

            if bcet is None:
                raise Exception(f"Missing or unreadable: {bcet_path}")
            if fcm is None:
                raise Exception(f"Missing or unreadable: {fcm_path}")

            # 1) Ensure FCM is treated as a binary brain mask
            _, brain_mask = cv2.threshold(fcm, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # 2) Apply mask to BCET so thresholding happens only inside brain
            masked = cv2.bitwise_and(bcet, bcet, mask=brain_mask)

            # 3) Segment BRIGHT regions (tumor) instead of holes
            blur = cv2.GaussianBlur(masked, (5, 5), 0)

            # Use top-intensity tail as tumor (stable vs Otsu here)
            vals = blur[blur > 0]
            if vals.size == 0:
                raise Exception("Masked image is empty. FCM mask might be wrong.")

            t = np.percentile(vals, 92)  # tune 90-97 if needed
            _, tumor = cv2.threshold(blur, t, 255, cv2.THRESH_BINARY)

            # 4) Cleanup speckles and fill small holes
            kernel = np.ones((5, 5), np.uint8)
            tumor = cv2.morphologyEx(tumor, cv2.MORPH_OPEN, kernel, iterations=1)
            tumor = cv2.morphologyEx(tumor, cv2.MORPH_CLOSE, kernel, iterations=2)

            # Optional: keep only largest blob
            num, labels, stats, _ = cv2.connectedComponentsWithStats(tumor, connectivity=8)
            if num > 1:
                largest = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
                tumor = (labels == largest).astype(np.uint8) * 255

            out_path = os.path.join("images", "threshld.jpg")
            cv2.imwrite(out_path, tumor)

            self.showMessageBox("Information", f"Thresholding completed. Saved: {out_path}")
            show_cv_image("Threshold Output", tumor)
            self.dialog.hide()

        except Exception as e:
            print("Error=" + str(e))


    def showMessageBox(self, title, message):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec_()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowFlag(QtCore.Qt.Window)  # Fix: macOS red close button
        Dialog.resize(558, 409)
        Dialog.setStyleSheet("background-color: rgb(80, 20, 20);")

        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(130, 50, 401, 71))
        self.label.setStyleSheet("color: rgb(255, 255, 255);\nfont: 16pt \"Georgia\";")
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(110, 130, 250, 51))
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);\nfont: 12pt \"Georgia\";")
        self.label_2.setObjectName("label_2")

        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(110, 170, 411, 31))
        self.lineEdit.setStyleSheet("font: 75 10pt \"Verdana\";")
        self.lineEdit.setObjectName("lineEdit")

        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(230, 240, 121, 31))
        self.pushButton.setStyleSheet(
            "color: rgb(255, 255, 255);\nfont: 14pt \"Georgia\";\nbackground-color: rgb(170, 85, 0);"
        )
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.submit)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Thresholding"))
        self.label.setText(_translate("Dialog", "Thresholding Segmentation"))
        self.label_2.setText(_translate("Dialog", "Input Image (BCET output)"))
        self.pushButton.setText(_translate("Dialog", "Submit"))
