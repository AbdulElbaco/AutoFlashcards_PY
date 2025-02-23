"""
PDF Processing Library with optimized memory usage and error handling.
"""
from typing import Optional
import os
import gc
from contextlib import contextmanager
from pypdf import PdfReader, PdfWriter
from pdf2image import convert_from_path
import pytesseract
import io
from exceptions import PDFProcessingError
import Global_Variables
from logger import logger

# Set Tesseract path (Windows only)
pytesseract.pytesseract.tesseract_cmd = Global_Variables.tesseract_cmd

@contextmanager
def pdf_resource_manager():
    """Context manager for PDF resources to ensure proper cleanup"""
    try:
        yield
    finally:
        gc.collect()

def convert_unsearchable_to_searchable(input_pdf_path: str, output_pdf_path: str = Global_Variables.Temp) -> None:
    """
    Converts an unsearchable PDF to a searchable format using batched OCR processing for memory efficiency.
    """
    if not os.path.isfile(input_pdf_path):
        raise PDFProcessingError(f"Input PDF not found: {input_pdf_path}")

    output = PdfWriter()

    try:
        # Convert PDF pages to images
        images = convert_from_path(input_pdf_path, poppler_path=Global_Variables.poppler_path, dpi=300)

        # Process pages efficiently
        for image in images:
            text_pdf_bytes = pytesseract.image_to_pdf_or_hocr(image, extension='pdf')
            pdf_reader = PdfReader(io.BytesIO(text_pdf_bytes))
            output.add_page(pdf_reader.pages[0])

        # Save the searchable PDF
        with open(output_pdf_path, 'wb') as f:
            output.write(f)

    except Exception as e:
        raise PDFProcessingError(f"Failed to convert PDF: {e}")

    finally:
        output.close()
        gc.collect()

def split_pdf(file_path: str, output_folder: str = Global_Variables.Temp_Splited_Pages) -> int:
    """
    Splits PDF into pages with optimized memory usage.
    """
    os.makedirs(output_folder, exist_ok=True)
    num_pages = 0

    try:
        with open(file_path, "rb") as pdf_file:
            reader = PdfReader(pdf_file)
            num_pages = len(reader.pages)

            for i in range(num_pages):
                with pdf_resource_manager():
                    output_path = os.path.join(output_folder, f"{i+1}.pdf")
                    writer = PdfWriter()
                    writer.add_page(reader.pages[i])
                    
                    with open(output_path, "wb") as output_file:
                        writer.write(output_file)
                    
                    writer.close()
                    del writer

    except Exception as e:
        raise PDFProcessingError(f"Failed to split PDF: {str(e)}")

    return num_pages