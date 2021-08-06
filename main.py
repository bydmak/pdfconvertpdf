import pytesseract
import os 
import sys
from PIL import Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
import fitz
import shutil

from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMessageBox

class Form(QMainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        

        getFileNameButton = QPushButton("Выбрать файл")
        getFileNameButton.clicked.connect(self.getFileName)
        getFileNameButton.setFixedSize(160,160)

        layoutV = QVBoxLayout()
        layoutV.addWidget(getFileNameButton)

        layoutH = QHBoxLayout()
        layoutH.addLayout(layoutV)

        centerWidget = QWidget()
        centerWidget.setLayout(layoutH) 
        self.setCentralWidget(centerWidget)
        
        self.resize(200,200)
        self.setWindowTitle("PdfReader")

    def getFileName(self):
        filename, filetype = QFileDialog.getOpenFileName(self,
                             "Выбрать файл",
                             ".",
                             "PDF Files(*.pdf)")
        
        
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

        pdf_document = fitz.open(filename)

        try:
            os.mkdir("imagepdf")
        except OSError:
            None
        os.chdir("imagepdf")

        for current_page in range(len(pdf_document)):
            for image in pdf_document.getPageImageList(current_page):
                xref = image[0]
                pix = fitz.Pixmap(pdf_document, xref)
                if pix.n < 5:        # this is GRAY or RGB
                    pix.writePNG("%s.png" % (current_page))
                else:                # CMYK: convert to RGB first
                    pix1 = fitz.Pixmap(fitz.csRGB, pix)
                    pix1.writePNG("%s.png" % (current_page))
                    pix1 = None
                pix = None
        os.chdir('..')

        c = canvas.Canvas("Результат.pdf", pagesize=A4)      
                    
        for k in range(len(pdf_document)):
            os.chdir("imagepdf")
            img = Image.open(str(k) + '.png')
            os.chdir('..')

            custom_config = r'--oem 3 --psm 6'

            text = pytesseract.image_to_string(img, lang='rus', config= custom_config)

            with open('Text.txt', 'w', encoding="cp1251") as text_file:
                text_file.write(text)
            
            sumtext = sum(1 for line in open('Text.txt'))
            l = []
            pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))
            c.setFont('FreeSans', 14)
            i = 29.0
            with open('Text.txt', 'r+') as sumtext:  
                for l in sumtext:
                    i = i - 0.5
                    c.drawString(0.5 * cm, i * cm, l.rstrip())
            if os.path.isfile('Text.txt'): 
                os.remove('Text.txt') 
            else: print("File doesn't exists!")
            c.showPage()
            m = k + 1
            
            
            if m == len(pdf_document):
                QMessageBox.about(self, "Выполнено", "Выполнено")
                c.save()
            
        shutil.rmtree("imagepdf") #удалить директорию с фото

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Form()
    ex.show()
    sys.exit(app.exec_())
