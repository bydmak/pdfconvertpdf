import fitz
import os

pdf_document = fitz.open("TestPDF.pdf")

path = "imagepdf"
try:
    os.mkdir(path)
except OSError:
    None
# for current_page in range(len(pdf_document)):
#     for image in pdf_document.getPageImageList(current_page):
#         xref = image[0]
#         pix = fitz.Pixmap(pdf_document, xref)
#         if pix.n < 5:        # this is GRAY or RGB
#             pix.writePNG("%s.png" % (current_page))
#         else:                # CMYK: convert to RGB first
#             pix1 = fitz.Pixmap(fitz.csRGB, pix)
#             pix1.writePNG("%s.png" % (current_page))
#             pix1 = None
#         pix = None