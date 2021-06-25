import pytesseract
import os 
from PIL import Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
import fitz
import shutil
import cv2

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

pdf_document = fitz.open("TestPDF.pdf")

try:
    os.mkdir("imagepdf")
except OSError:
    None
os.chdir("imagepdf")
l = 0
for current_page in range(len(pdf_document)):
    for image in pdf_document.getPageImageList(current_page):
        xref = image[0]
        pix = fitz.Pixmap(pdf_document, xref)
        if pix.n < 5:        # this is GRAY or RGB
            pix.writePNG("%s.png" % (current_page))
            if l == 0:
                print(pytesseract.image_to_osd(cv2.imread("0.png")))
                #if pytesseract.image_to_osd(cv2.rotate("0.png")) != 0:
                l = 1
            if l == 1:
                im = Image.open("%s.png" % (current_page))
                im_rotate = im.rotate(90)
                im_rotate.save("%s.png" % (current_page), quality=95)
                im.close()
        else:                # CMYK: convert to RGB first
            pix1 = fitz.Pixmap(fitz.csRGB, pix)
            pix1.writePNG("%s.png" % (current_page))
            pix1 = None
        pix = None
os.chdir('..')
#shutil.rmtree("imagepdf") - удалить директорию с фото






# img = Image.open('0.png')



# custom_config = r'--oem 3 --psm 6'

# text = pytesseract.image_to_string(img, lang='rus', config= custom_config)

# with open('Text.txt', 'w', encoding="cp1251") as text_file:
#     text_file.write(text)
    
# sumtext = sum(1 for line in open('Text.txt'))
# l = []
# c = canvas.Canvas("Результат.pdf", pagesize=A4)
# pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))
# c.setFont('FreeSans', 12)
# i = 29.0
# with open('Text.txt', 'r+') as sumtext:  
#     for l in sumtext:
#         i = i - 0.5
#         c.drawString(0.5 * cm, i * cm, l.rstrip())
#     c.save()

# if os.path.isfile('Text.txt'): 
#     os.remove('Text.txt') 
# else: print("File doesn't exists!")



# detector = UniversalDetector()
# with open('Text.txt', 'rb') as fh:
#     for line in fh:
#         detector.feed(line)
#         if detector.done:
#             break
#     detector.close()
# print(detector.result)