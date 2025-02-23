"""
Text Extraction Library

This module handles text extraction from PDF files using Aspose.PDF.
It provides functionality to extract text content while maintaining formatting.

Dependencies:
    - aspose.pdf
    - os
    - io
    - Global_Variables
"""

import aspose.pdf as ap
import os
import io
import Global_Variables
from typing import Optional
from exceptions import TextExtractionError
from logger import logger
import re
import json

class TextExtractor:
    """Class to handle text extraction with resource management"""
    
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def extract_text(self, input_file: str, page_number: Optional[int] = None) -> str:
        """
        Extracts text from PDF with proper resource management.
        """
        try:
            document = ap.Document(input_file)
            
            if not document.pages:
                raise TextExtractionError("Empty PDF document")

            page_to_process = page_number if page_number is not None else 1
            if page_to_process > len(document.pages):
                raise TextExtractionError(f"Page {page_to_process} does not exist")

            output_file = self._get_output_path(input_file, page_number)
            
            text_device = ap.devices.TextDevice()
            text_device.process(document.pages[page_to_process], output_file)
            
            return output_file

        except Exception as e:
            raise TextExtractionError(f"Text extraction failed: {str(e)}")
        finally:
            if 'document' in locals():
                document.dispose()

    def _get_output_path(self, input_file: str, page_number: Optional[int]) -> str:
        """Generates output file path"""
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        page_suffix = f"_p{page_number}" if page_number is not None else ""
        return os.path.join(self.output_dir, f"{base_name}{page_suffix}.txt")

def ExtractTextFromPDF(inputFile: str) -> None:
    """
    Extracts text from a PDF file and saves it to a text file.
    Currently extracts text only from page 1 of the PDF.

    Args:
        inputFile (str): Path to the input PDF file.

    Raises:
        ValueError: If the PDF is empty (no pages).
        FileNotFoundError: If input file doesn't exist.
        IOError: If output directory cannot be created.
        aspose.pdf.exceptions.PdfException: If PDF processing fails.

    Note:
        This function currently only processes page 1 of the PDF.
        To process different pages, modify the page number in textDevice.process().
    """
    # Load PDF
    document = ap.Document(inputFile)

    # Ensure the PDF has at least one page
    if len(document.pages) == 0:
        raise ValueError("The PDF is empty, no pages to extract.")

    # Create output directory if it doesn't exist
    os.makedirs(Global_Variables.Temp_Extracted_Text_Files, exist_ok=True)

    # Extract filename without extension
    pdf_name = os.path.splitext(os.path.basename(inputFile))[0]

    # Define output file path
    outputFile = os.path.join(Global_Variables.Temp_Extracted_Text_Files, f"{pdf_name}.txt")

    # Extract text from the first page
    textDevice = ap.devices.TextDevice()
    textDevice.process(document.pages[1], outputFile)

def extract_json_from_triple_quotes(text: str):
    """
    Extracts JSON-like content enclosed in triple single quotes (''') from a given text.

    Parameters:
        text (str): The input text containing JSON inside triple quotes.

    Returns:
        dict or None: A Python dictionary if valid JSON is found, else None.
    """
    # Regular expression to capture content inside triple quotes
    pattern = r"'''{.*?}'''"
    match = re.search(pattern, text, re.DOTALL)

    if not match:
        print("No JSON found!")
        return None

    json_str = match.group(0).strip()  # Extract JSON without triple quotes

    # Debugging: Print extracted string before parsing
    print("Extracted JSON String:\n", json_str)

    try:
        json_data = json.loads(json_str)  # Convert string to Python dictionary
        print("Parsed JSON Successfully:", json_data)
        return json_data
    except json.JSONDecodeError as e:
        print("Invalid JSON:", e)
        return None