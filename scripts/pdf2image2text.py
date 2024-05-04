import os
from pdf2image import convert_from_path
import pytesseract

from skillixir.utils import remove_hyphens


filePath = '../data/main.pdf'
doc = convert_from_path(filePath, fmt='png')
path, fileName = os.path.split(filePath)
fileBaseName, fileExtension = os.path.splitext(fileName)

for page_number, page_data in enumerate(doc):
	txt = pytesseract.image_to_string(page_data)
	print(txt)
	print('Page # {} - {}'.format(str(page_number), remove_hyphens(txt)))
