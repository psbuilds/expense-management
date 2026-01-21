from PIL import Image
import pytesseract
import io
from fastapi import UploadFile


def extract_text_from_image(file: UploadFile) -> str:
    """
    Extract text from an uploaded image using Tesseract OCR.
    """

    # Read raw bytes from UploadFile
    image_bytes = file.file.read()

    # Convert bytes to PIL Image
    image = Image.open(io.BytesIO(image_bytes))

    # Run OCR
    text = pytesseract.image_to_string(image)

    return text.strip()
