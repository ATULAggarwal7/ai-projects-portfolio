from pypdf import PdfReader
from utils.logger import logger


def extract_resume_text(file_path):
    try:
        reader = PdfReader(file_path)
        text = ""

        for page in reader.pages:
            text += page.extract_text() + "\n"

        logger.info("Resume text extracted successfully")
        return text

    except Exception as e:
        logger.warning(f"Resume parsing failed: {e}")
        return ""