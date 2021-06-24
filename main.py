import pytesseract
import os 
from PIL import Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4

img = Image.open('page0-5.png')

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

custom_config = r'--oem 3 --psm 6'

text = pytesseract.image_to_string(img, lang='rus', config= custom_config)

with open('Text.txt', 'w', encoding="cp1251") as text_file:
    text_file.write(text)
    
sumtext = sum(1 for line in open('Text.txt'))
l = []
c = canvas.Canvas("Результат.pdf", pagesize=A4)
pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))
c.setFont('FreeSans', 12)
i = 29.0
with open('Text.txt', 'r+') as sumtext:  
    for l in sumtext:
        i = i - 0.5
        c.drawString(0.5 * cm, i * cm, l.rstrip())
    c.save()

if os.path.isfile('Text.txt'): 
    os.remove('Text.txt') 
    print("success") 
else: print("File doesn't exists!")



# detector = UniversalDetector()
# with open('Text.txt', 'rb') as fh:
#     for line in fh:
#         detector.feed(line)
#         if detector.done:
#             break
#     detector.close()
# print(detector.result)