import aspose.pdf as ap
import os
import io
import Global_Variables

def ExtractTextFromPDF(inputFile):
    # Load PDF
    document = ap.Document(inputFile)

    # Ensure the PDF has at least one page
    if len(document.pages) == 0:
        raise ValueError("The PDF is empty, no pages to extract.")

    # Hardcoded output directory
    os.makedirs(Global_Variables.Temp_Extracted_Text_Files, exist_ok=True)  # Create folder if it doesn't exist

    # Extract filename without extension
    pdf_name = os.path.splitext(os.path.basename(inputFile))[0]

    # Define output file path
    outputFile = os.path.join(Global_Variables.Temp_Extracted_Text_Files, f"{pdf_name}.txt")

    # Extract text from the first page
    textDevice = ap.devices.TextDevice()
    textDevice.process(document.pages[1], outputFile)