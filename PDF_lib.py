import os
import gc
from pypdf import PdfReader, PdfWriter
from pdf2image import convert_from_path
from PyPDF2 import PdfReader, PdfWriter
import pytesseract
import io
import Global_Variables

# Set Tesseract path (Windows only)
pytesseract.pytesseract.tesseract_cmd = Global_Variables.tesseract_cmd

def convert_unsearchable_to_searchable(input_pdf_path, output_pdf_path):
    # Use PdfWriter for incremental writing (avoid keeping everything in memory)
    output = PdfWriter()
    
    # Process pages one by one to reduce memory usage
    for image in convert_from_path(input_pdf_path, poppler_path= Global_Variables.poppler_path, dpi=300):
        # Perform OCR and get searchable PDF content
        text_pdf_bytes = pytesseract.image_to_pdf_or_hocr(image, extension='pdf')
        
        # Directly load the OCR-generated PDF without storing it in memory unnecessarily
        pdf_reader = PdfReader(io.BytesIO(text_pdf_bytes))
        output.add_page(pdf_reader.pages[0])  # Append the OCR-processed page
    
    # Save the output PDF incrementally
    with open(output_pdf_path, 'wb') as f:
        output.write(f)

def split_pdf(file_path, output_folder= Global_Variables.Temp_Splited_Pages):
    """
    Splits a PDF into individual pages and saves them as separate PDF files.
    Uses extreme memory optimization by processing raw bytes per page.

    Args:
        file_path (str): The full path to the input PDF file.
        output_folder (str, optional): The folder where split pages will be saved. 
                                       Defaults to "C:\\Users\\ccxvc\\source\\repos\\AutoFlashcards_PY\\SplitPDF".

    Returns:
        number of the saved PDF pages.
    """
    os.makedirs(output_folder, exist_ok=True)

    with open(file_path, "rb") as pdf_file:
        reader = PdfReader(pdf_file)
        num_pages = len(reader.pages)

        for i in range(len(reader.pages)):
            output_path = os.path.join(output_folder, f"{i+1}.pdf")

            # Open output file directly to minimize memory usage
            with open(output_path, "wb") as f:
                writer = PdfWriter()
                writer.add_page(reader.pages[i])
                writer.write(f)
                writer.close()  # Immediately close to release memory
                f.close()

            # Force release of memory
            del writer  
            gc.collect()

        # Close input PDF file stream
        del reader
        gc.collect()

    return num_pages