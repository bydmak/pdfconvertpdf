import fitz
import os
from PIL import Image
import shutil
import cv2
import pytesseract

pdf_document = fitz.open("Новый документ (31).pdf")

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

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
            print(pytesseract.image_to_osd(cv2.imread("%s.png" % (current_page))))
        else:                # CMYK: convert to RGB first
            pix1 = fitz.Pixmap(fitz.csRGB, pix)
            pix1.writePNG("%s.png" % (current_page))
            pix1 = None
        pix = None
os.chdir('..')
#shutil.rmtree("imagepdf")




# os.chdir("imagepdf") - разворот
# im = Image.open('0.png')
# im_rotate = im.rotate(90)
# im_rotate.save('0.png', quality=95)
# im.close()