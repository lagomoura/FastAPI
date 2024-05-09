import cv2
import pytesseract
import re
from PIL import Image

#! NO ESTA UBICANDO TESSERACT

def address_phone_detector(img_path):
    
    img = cv2.imread(img_path)

    img_gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Umbralizacion
    thresh = cv2.threshold(
        img_gris, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract'

    # Detectando texto
    texto = pytesseract.image_to_string(thresh)

    # Regex direcciones
    regex_dire = r'\b(?:\d+\s*(?:[a-zA-Z]+\s*){1,2}|[a-zA-Z]+\s*(?:\d+\s*){1,2})\b'
    direcciones_encontradas = re.findall(regex_dire, texto)

    # regex fone
    regex_fone = r'\b(?:\+\d{1,3}\s*)?(?:\(\d{1,4}\)\s*)?\d{1,3}(?:[\s.-]?\d{2,4}){2,3}\b'
    fones_encontrados = re.findall(regex_fone, texto)

    if len(direcciones_encontradas) > 0 or len(fones_encontrados) > 0:
        address_phone_detector = True
    else:
        address_phone_detector = False

    return address_phone_detector
