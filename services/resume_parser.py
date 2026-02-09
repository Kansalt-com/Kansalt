"""
Resume parsing and text extraction from PDF/DOCX.
"""
import re
from io import BytesIO
from typing import Optional
from PyPDF2 import PdfReader
import docx
from utils.logger import get_logger

logger = get_logger(__name__)


class ResumeParser:
    """Parse resume files (PDF/DOCX) and extract metadata."""

    @staticmethod
    def extract_text_from_pdf(file_bytes: bytes) -> str:
        """Extract text from PDF file."""
        try:
            reader = PdfReader(BytesIO(file_bytes))
            text = ""
            for page in reader.pages:
                page_text = page.extract_text() or ""
                text += page_text + "\n"
            logger.debug(f"Extracted {len(text)} chars from PDF")
            return text
        except Exception as e:
            logger.error(f"PDF extraction error: {e}")
            raise

    @staticmethod
    def extract_text_from_docx(file_bytes: bytes) -> str:
        """Extract text from DOCX file."""
        try:
            doc = docx.Document(BytesIO(file_bytes))
            text = "\n".join([p.text for p in doc.paragraphs])
            logger.debug(f"Extracted {len(text)} chars from DOCX")
            return text
        except Exception as e:
            logger.error(f"DOCX extraction error: {e}")
            raise

    @staticmethod
    def extract_email(text: str) -> Optional[str]:
        """Extract first email from text."""
        try:
            matches = re.findall(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", text)
            result = matches[0] if matches else None
            logger.debug(f"Extracted email: {result}")
            return result
        except Exception as e:
            logger.error(f"Email extraction error: {e}")
            return None

    @staticmethod
    def extract_phone(text: str) -> Optional[str]:
        """Extract first phone number from text."""
        try:
            matches = re.findall(r"(\+?\d[\d\s\-()]{8,}\d)", text)
            result = matches[0].strip() if matches else None
            logger.debug(f"Extracted phone: {result}")
            return result
        except Exception as e:
            logger.error(f"Phone extraction error: {e}")
            return None

    @staticmethod
    def extract_name(text: str) -> Optional[str]:
        """Extract first non-empty line as candidate name."""
        try:
            for line in text.splitlines():
                line = line.strip()
                # Skip empty lines and header keywords
                if len(line) >= 3 and any(c.isalpha() for c in line):
                    if not any(skip in line.lower() for skip in ["resume", "cv", "curriculum", "vitae"]):
                        name = line[:80]
                        logger.debug(f"Extracted name: {name}")
                        return name
            return None
        except Exception as e:
            logger.error(f"Name extraction error: {e}")
            return None
