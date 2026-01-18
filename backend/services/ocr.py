import os
import io
from PIL import Image
import pytesseract


def extract_text_from_image(image_bytes: bytes) -> str:
    """
    Extract text from an image using Tesseract OCR.
    Tesseract path is read from environment if provided.
    """
    tesseract_cmd = os.getenv("TESSERACT_CMD")
    if tesseract_cmd:
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    image = Image.open(io.BytesIO(image_bytes))
    image = image.convert("L")
    text = pytesseract.image_to_string(image)

    return text.strip()
