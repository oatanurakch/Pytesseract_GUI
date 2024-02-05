from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QFileDialog
import sys
import cv2

from ui import Ui_MainWindow
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()

import pytesseract
# Setting path of tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

class myapp(Ui_MainWindow):
    def __init__(self) -> None:
        super().setupUi(MainWindow)
        # Setup signal when interactive with UI
        self.setupSignal()

    # Setup signal when interactive with UI
    def setupSignal(self):
        # Select input button
        self.input_bt.clicked.connect(self.selectInput)

    # Select input button
    def selectInput(self):
        file = QFileDialog.getOpenFileName(caption = 'Choose image', filter = 'Image files (*.jpg *.png *.jpeg *.bmp)', directory = r'C:/')
        try:
            # Open image
            self.frame = cv2.imread(file[0])
            height, width, channel = self.frame.shape
            step = channel * width
            qImg = QImage(self.frame.data, width, height, step, QImage.Format_RGB888)
            # Set pixmap
            self.images.setPixmap(QPixmap.fromImage(qImg))
            # OCR process
            self.ocr()
        except:
            pass

    def ocr(self):
        # Convert image to gray
        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        # Convert image to binary
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        # Extract text from image
        text = pytesseract.image_to_string(gray, lang = 'eng')
        # Show text
        # self.result.setText(text)
        # OCR Box
        self.ocrBox(img = gray)
    
    def ocrBox(self, img):
        d = pytesseract.image_to_data(img, output_type = pytesseract.Output.DICT)
        # Check Key of dict
        # print(d.keys())
        nbox = len(d['text'])
        text = ''
        for i in range(nbox):
            if int(float(d['conf'][i])) > 60:
                (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                # cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
                text += d['text'][i] + ' '
        height, width, channel = self.frame.shape
        step = channel * width
        qImg = QImage(self.frame.data, width, height, step, QImage.Format_RGB888)
        # Set pixmap
        self.images.setPixmap(QPixmap.fromImage(qImg))
        self.result.setText(text)
        
obj = myapp()

if __name__ == "__main__":
    MainWindow.show()
    sys.exit(app.exec_())