import cv2
import os
from datetime import datetime


def efecto_blur(img, puntos):
    # .coordenadas del rectangulo
    x, y, w, h = cv2.boundingRect(puntos)

    # .identificando region de interes (ROI)
    roi = img[y:y+h, x:x+w]

    # .Aplicando blur al roi en cascada
    for i in range(3):
        roi_blur = cv2.GaussianBlur(roi, (11, 11), 50)

        # .Reemplazando zona roi por zona con blur
        img[y:y+h, x:x+w] = roi_blur

    return img


def qr_detector(path):
    qr_detectado = False

    # .ruta de la img
    img = cv2.imread(path)

    # .Convertiendo a escala de grises
    img_gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # .Inicilizando el detector de QR
    detector_qr = cv2.QRCodeDetector()

    # .Detector
    exito, puntos, qr_info = detector_qr.detectAndDecode(img_gris)

    # .Mostrando info qr
    if exito:
        qr_detectado = True
        img = efecto_blur(img, puntos)
        print('Blur aplicado')
        
        # .Creando carpeta
        carpeta_destino = 'src/imgs_qr_blur'
        if not os.path.exists(carpeta_destino):
            os.makedirs(carpeta_destino)

        tag_tiempo = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        nombre_img = f"img_qr_detectado.{tag_tiempo}.jpg"
        ruta_img = os.path.join(carpeta_destino, nombre_img)
        cv2.imwrite(ruta_img, img)

    return qr_detectado
