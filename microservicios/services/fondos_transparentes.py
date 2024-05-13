import rembg
import numpy as np
from PIL import Image
import os
from datetime import datetime

def quitar_fondos(path):
  fondo_quitado = False

  if path.endswith('jpg') or path.endswith('jpeg'):
    
    input_img = Image.open(path)

    input_array = np.array(input_img) #.Pasando img a array

    #.Eliminando fondo
    output_array = rembg.remove(input_array)

    #.Nueva img sin bg - Asignando RGBA para poder trabajar con la transparecia de fondo
    output_img = Image.fromarray(output_array, "RGBA")

    carpeta_destino = 'src/imgs_sin_fondo'
    
    if not os.path.exists(carpeta_destino):
      os.makedirs(carpeta_destino)

  #! ACA TENGO PROBLEMA. GUARDAR EL IMAGEN EN FORMATO PNG.
    #.Guardando img en formato .png
    
    print(output_img)
    
    ruta_salida = os.path.join(carpeta_destino, os.path.splitext(os.path.basename(path))[0] + '.png')
    output_img.save(ruta_salida)
    
    fondo_quitado = True
    
  return fondo_quitado


