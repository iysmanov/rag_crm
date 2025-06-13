from paddleocr import PaddleOCR
from PIL import Image
import numpy as np

# Инициализация OCR один раз (русский + английский)
ocr = PaddleOCR(use_angle_cls=True, lang='ru')

def extract_text_from_image(image_path):
    """
    Распознаёт текст на изображении (скриншоте) с помощью PaddleOCR.
    Возвращает распознанный текст одной строкой.
    """
    result = ocr.ocr(image_path, cls=True)
    lines = []
    for line in result:
        for (bbox, text, conf) in line:
            lines.append(text[0])
    return '\n'.join(lines) 