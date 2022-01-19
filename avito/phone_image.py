import pytesseract, os
from PIL import Image
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
img = Image.open('Без названия.png')
# custom_config = r'--oem 3 --psm 13'
custom_config = r'digits --oem 1 --psm 7 -c tessedit_char_whitelist=0123456789'
text = pytesseract.image_to_string(img).strip().replace('-','').replace(' ','')
os.remove('Без названия.png')
# print('7' + text.strip()[1:], len(text), 'need to be - 11')
print(text.strip(), len(text), 'need to be - 11')
# print('http://wa.me/7' + text[1:], len(text))