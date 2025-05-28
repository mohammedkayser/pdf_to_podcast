import fitz  # PyMuPDF
import PyPDF2
from tqdm import tqdm

class PDFProcessor:
    def __init__(self, max_pages: int = 50):
        self.max_pages = max_pages

    def extract_text_pymupdf(self, pdf_path: str) -> str:
        doc = fitz.open(pdf_path)
        text = ""
        for page_num in tqdm(range(min(len(doc), self.max_pages)), desc="Extracting PDF text"):
            page = doc.load_page(page_num)
            text += page.get_text() + "\n\n"
        doc.close()
        return text.strip()

    def extract_text_pypdf2(self, pdf_path: str) -> str:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num in tqdm(range(min(len(reader.pages), self.max_pages)), desc="Extracting PDF text"):
                text += reader.pages[page_num].extract_text() + "\n\n"
        return text.strip()

    def extract_text(self, pdf_path: str) -> str:
        try:
            text = self.extract_text_pymupdf(pdf_path)
            if len(text.strip()) < 100:
                raise ValueError("Insufficient text from PyMuPDF")
            return text
        except Exception:
            return self.extract_text_pypdf2(pdf_path)
