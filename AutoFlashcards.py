import os
from Text_lib import ExtractTextFromPDF
from PDF_lib import convert_unsearchable_to_searchable, split_pdf
from ai_client import CleanAndFormatTextWithAI, GetListOfNotes_From_AI
from AnkiConnect import addnotes
import Global_Variables

def prepare_pdf(input_file: str) -> int:
    """
    Convert PDF to searchable format and split it into individual pages.

    Args:
        input_file (str): Path to the input PDF file.

    Returns:
        int: Number of pages in the PDF.

    Raises:
        FileNotFoundError: If input_file doesn't exist.
        ValueError: If the PDF is empty or corrupted.
        RuntimeError: If conversion or splitting fails.
    """
    # Make the PDF file searchable
    convert_unsearchable_to_searchable(input_file, Global_Variables.Temp_Searchable_PDF)
    
    # Split the searchable PDF file into individual pages
    return split_pdf(Global_Variables.Temp_Searchable_PDF, Global_Variables.Temp_Splited_Pages)

def extract_text_from_pages(num_pages: int) -> None:
    """
    Extract text content from each page of the split PDF files.

    Args:
        num_pages (int): Total number of pages to process.

    Raises:
        ValueError: If a page is empty or cannot be processed.
        IOError: If there are issues reading the PDF files.
    """
    for page_num in range(num_pages):
        pdf_path = f"{Global_Variables.Temp_Splited_Pages}/{page_num+1}.pdf"
        ExtractTextFromPDF(pdf_path)

def process_text_with_ai(num_pages: int) -> None:
    """
    Clean and format extracted text using AI for each page.

    Args:
        num_pages (int): Total number of pages to process.

    Raises:
        IOError: If there are issues reading or writing text files.
        RuntimeError: If AI processing fails.
        FileNotFoundError: If input text files don't exist.
    """
    # Initialize input and output paths variables
    input_path = ""
    output_path = ""

    # Process each page
    for page_num in range(num_pages):
        input_path = f"{Global_Variables.Temp_Extracted_Text_Files}/{page_num+1}.txt"
        output_path = f"{Global_Variables.Temp_Cleaned_Text_Files}/{page_num+1}.txt"
        # Read extracted text
        with open(input_path, "r", encoding="utf-8", errors="ignore") as input_file:
            text = input_file.read()
            cleaned_text = CleanAndFormatTextWithAI(text, page_num+1)
            
            # Save cleaned text
            with open(output_path, "w", encoding="utf-8", errors="ignore") as output_file:
                output_file.write(cleaned_text)

def generate_anki_notes(num_pages: int) -> list:
    """
    Generate Anki flashcard notes from cleaned text files.

    Args:
        num_pages (int): Total number of pages to process.

    Returns:
        list: List of dictionaries containing Anki note data.
            Each dictionary has 'Front', 'Back', 'deckName', and 'modelName' keys.

    Raises:
        IOError: If there are issues reading text files.
        JSONDecodeError: If AI response is not valid JSON.
        FileNotFoundError: If cleaned text files don't exist.
    """
    #initialize notes list
    notes_list = []
    notes = []
    for page_number in range(num_pages):
        with open(f"{Global_Variables.Temp_Cleaned_Text_Files}/{page_number+1}.txt", "r", encoding="utf-8", errors="ignore") as file:
            notes = GetListOfNotes_From_AI(file.read(), page_number)
            notes_list.extend(notes)

    return notes_list

def cleanup_temp_files() -> None:
    """
    Clean up all temporary files and folders created during processing.

    This includes:
    - Split PDF pages
    - Extracted text files
    - Cleaned text files
    - Searchable PDF file

    Raises:
        PermissionError: If files are locked or permission is denied.
        OSError: If there are issues deleting files or folders.
    """
    #Clear Temp_Searchable_PDF
    if os.path.exists(Global_Variables.Temp_Searchable_PDF):
        os.remove(Global_Variables.Temp_Searchable_PDF)

    temp_folders = [
        Global_Variables.Temp_Splited_Pages,
        Global_Variables.Temp_Extracted_Text_Files,
        Global_Variables.Temp_Cleaned_Text_Files,
        Global_Variables.Temp_Notes_Json_Files
    ]
    
    for folder in temp_folders:
        if os.path.exists(folder):
            for file in os.listdir(folder):
                try:
                    os.remove(os.path.join(folder, file))
                except Exception as e:
                    print(f"Warning: Could not delete {file}: {e}")

def main():
    """
    Main function to orchestrate the PDF to Anki flashcard conversion process.

    The process follows these steps:
    1. Clean up temporary files
    2. Convert PDF to searchable format and split into pages
    3. Extract text from each page
    4. Clean and format text using AI
    5. Generate Anki notes from processed text
    6. Add notes to Anki
    7. Clean up temporary files

    Raises:
        Exception: Any exception that occurs during processing will be caught,
                  cleanup will be attempted, and the exception will be re-raised.
    """
    try:
        # Step 1: Clean up temporary files
        cleanup_temp_files()
        
        # Input PDF file path
        input_file = r"C:\Users\ccxvc\Downloads\38833FF26BA1D.UnigramPreview_g9c9v27vpyspw!App\الكورس_السادس_سي++_المستوى_الثاني_.pdf"
        
        # Step 2: Prepare PDF
        num_pages = prepare_pdf(input_file)
        ##For debugging only
        num_pages = 6
        
        # Step 3: Extract text from pages
        extract_text_from_pages(num_pages)
        
        # Step 4: Process text with AI
        process_text_with_ai(num_pages)
        
        # Step : Generate Anki 
        notes_list = []
        notes_list = generate_anki_notes(num_pages)
        
        # Step 6: Add notes to Anki
        addnotes(notes_list)
        
        # Step 7: Cleanup
        #cleanup_temp_files()
        
    except Exception as e:
        print(f"Error in processing: {str(e)}")
        cleanup_temp_files()  # Attempt cleanup even if there's an error
        raise

if __name__ == '__main__':
    main()