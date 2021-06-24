from pickle import UNICODE
import pytesseract
from PIL import Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
from reportlab.pdfbase.ttfonts import TTFont
from chardet.universaldetector import UniversalDetector
#from fpdf import FPDF


img = Image.open('1Test.png')

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

custom_config = r'--oem 3 --psm 6'

text = pytesseract.image_to_string(img, lang='rus', config= custom_config)
with open('Text.txt', 'w') as text_file:
    text_file.write(text)
sumtext = sum(1 for line in open('Text.txt'))
fileText = open('Text.txt', 'r')

#pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))
l = []
c = canvas.Canvas("hello.pdf")
c.setFont("Times-Roman", 14)
i = 29.0
with open('Text.txt') as sumtext:
    
    for l in sumtext:
        i = i - 1.0
       # print(i, l)
        #l.encode('utf-8', 'replace')
        c.drawString(0.5 * cm, i * cm, l)
        print(l)
    c.save()

detector = UniversalDetector()
with open('test.txt', 'rb') as fh:
    for line in fh:
        detector.feed(line)
        if detector.done:
            break
    detector.close()
print(detector.result)

# pdf = FPDF()
# pdf.add_page()
# pdf.set_font("Arial", size=12)
# line_no = 1
# pdf.cell(txt = fileText.readline())
# for i in range(sumtext):
#         print(fileText.readline())
        # pdf.cell(0, 100, txt=fileText.readline().format(line_no), ln=1)
        # line_no += 1
# pdf.output("simple_demo.pdf")

#print(sumtext)
