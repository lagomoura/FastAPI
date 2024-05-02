import torch
from PIL import Image
from transformers import AutoModelForImageClassification, ViTImageProcessor
from clip import clip


def detectar_humano(path):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device)

    image = preprocess(Image.open(path)).unsqueeze(0).to(device)
    text = clip.tokenize(["a human", "a manikin"]).to(
        device)  # ! Rever los tokens de busqueda

    with torch.no_grad():
        logits_per_image, logits_per_text = model(image, text)
        probs = logits_per_image.softmax(dim=-1).cpu().numpy()

    if probs[0][0] >= 0.6:  # ! Delimitar un % adecuado
        es_humano = True
        nsfw = detectar_nsfw(path)
        if nsfw:
            nsfw = True
    else:
        es_humano = False
        nsfw = False

    return es_humano, nsfw


def detectar_nsfw(image_path):

    nsfw = False
    img = image_path

    # .Modelo preentrenado
    model = AutoModelForImageClassification.from_pretrained(
        # carga el modelo desde la ubicación especificada
        "Falconsai/nsfw_image_detection")

    # .Carga un procesador específico para el modelo de detección de contenido
    processor = ViTImageProcessor.from_pretrained(
        'Falconsai/nsfw_image_detection')

    # .Upload Image
    img = Image.open(img)

    # .Operacion de inferencia sin calculo de gradiente
    with torch.no_grad():
        # pt = tensor pytorch
        inputs = processor(images=img, return_tensors="pt")
        outputs = model(**inputs)
        logits = outputs.logits

    predicted_label = logits.argmax(-1).item()
    if predicted_label == 1:  # ! 1=nsfw / 0=normal
        nsfw = True

    return nsfw
