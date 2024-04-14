import re
import easyocr

reader = easyocr.Reader(['es','en'], gpu=False) # Esto solo necesita ejecutarse una vez para cargar el modelo en memoria

def detectar_email(texto):
    # Patrón de regex para detección de correos electrónicos
    patron_email = r'\b[A-Za-z0-9._%+-]*[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    correos_encontrados = re.findall(patron_email, texto)
    return correos_encontrados

def email_detector(path):
    email_detectado = False
    path_info = reader.readtext(path)
    
    for ubicacion, texto, accuracy in path_info:
        if " com" in texto:
            texto = texto.replace(" com", ".com")
        if detectar_email(texto):
            email_detectado = True
            break
            
    return email_detectado