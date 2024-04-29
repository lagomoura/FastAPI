import easyocr

reader = easyocr.Reader(['es','en'])

def detectar_texto(path):
  texto_marcaAgua_detectado = False
  
  resultado = reader.readtext(path)
  
  if len(resultado) > 0:
      texto_marcaAgua_detectado = True
      
    
  return texto_marcaAgua_detectado