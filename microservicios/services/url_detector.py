import easyocr
import re

reader = easyocr.Reader(['es', 'en'])


def detectar_url(texto):
    patron_url = r'(?:https?://)?(?:www\.)?[\w-]+\.(?:com|net|org|edu|gov|mil|int|co|io|ai|biz|info|name|pro|us|uk|ca|au|de|fr|jp|cn|br|tech|blog|shop|app|store|design)(?:/[\w/.-]*)*(?:\?[\w=&%-]*)?'
    urls_encontradas = re.findall(patron_url, texto)

    return urls_encontradas


def url_detector(path):
    url_detectado = False
    path_info = reader.readtext(path)

    for ubicacion, texto, accuracy in path_info:

        if detectar_url(texto):
            url_detectado = True
            break

    return url_detectado
