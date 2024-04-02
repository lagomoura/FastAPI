import easyocr
import re
import json

reader = easyocr.Reader(['es','en']) # this needs to run only once to load the model into memory

def detectar_email(texto):
  #.Regex para deteccion de correo
  patron_email = r'\b[A-Za-z0-9._%+-]*[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

  correos_encontrados = re.findall(patron_email, texto)

  return correos_encontrados

def email_detector(resultado):
  resultado_email = []
  
  for ubicacion, texto, accuracy in resultado:

    emails = detectar_email(texto)
    
    print(emails)

    if emails:
      resultado_email.append({
        "Email": emails[0],
        "Ubicacion" : ubicacion,
        "Accuracy" : round(accuracy * 100)
      })

  if len(resultado_email) == 0:
    print("Sin deteccion de email")
    
  return resultado_email

def main():
  resultado = reader.readtext('src/imgs/text2.jpeg')
  email_detector(resultado)

resultado_json = json.dumps(main())

print(resultado_json)