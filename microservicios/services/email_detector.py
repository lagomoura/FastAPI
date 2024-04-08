import re
import easyocr

reader = easyocr.Reader(['es','en'], gpu=False) # Esto solo necesita ejecutarse una vez para cargar el modelo en memoria

def detectar_email(texto):
    # Patrón de regex para detección de correos electrónicos
    patron_email = r'\b[A-Za-z0-9._%+-]*[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    correos_encontrados = re.findall(patron_email, texto)
    return correos_encontrados

def email_detector(path):
    for ubicacion, texto, accuracy in path:
        if " com" in texto:
            texto = texto.replace(" com", ".com")
        emails = detectar_email(texto)
        if emails:
            return f"Detectado: {emails[0]}"
    
    return "La imagen no contiene correos electrónicos detectados"

def main():
    path = reader.readtext('src/imgs/text2.jpeg')
    resultado = email_detector(path)
    print(resultado)

main()