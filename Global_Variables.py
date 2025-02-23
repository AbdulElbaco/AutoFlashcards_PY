"""
Global Variables and Configuration

This module contains all global configuration variables used across the application.
It includes API keys, file paths, and other configuration settings.

Configuration Categories:
    - AI Service Configuration: Settings for OpenRouter AI API
    - File System Paths: Temporary file storage locations
    - External Tools Configuration: Paths to required external tools
    - Anki Connect Configuration: Settings for Anki integration

Note:
    All paths should be absolute paths to prevent any path resolution issues.
    Make sure all external tools (Tesseract, Poppler) are installed at the specified paths.
"""

# AI Service Configuration
LLM_AI_model: str = "google/gemini-2.0-flash-lite-preview-02-05:free"  # AI model identifier
role: str = "user"  # User role for AI interactions
url: str = "https://openrouter.ai/api/v1/chat/completions"  # API endpoint URL
openrouterAPI_Key: str = "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"  # API authentication key

# External Tools Configuration
tesseract_cmd: str = r"C:/Program Files/Tesseract-OCR/tesseract.exe"  # Tesseract OCR path
poppler_path: str = r"C:/Program Files/poppler/Library/bin"  # Poppler utilities path

# Temporary File Paths
Temp_Searchable_PDF: str = r"C:\Users\ccxvc\source\repos\AutoFlashcards_PY\Temp\Temp_Searchable_PDF.pdf"  # Temporary searchable PDF
Temp_Splited_Pages: str = r"C:\Users\ccxvc\source\repos\AutoFlashcards_PY\Temp\Temp_Splited_Pages"  # Split PDF pages directory
Temp_Extracted_Text_Files: str = r"C:\Users\ccxvc\source\repos\AutoFlashcards_PY\Temp\Temp_Extracted_Text_Files"  # Extracted text directory
Temp_Cleaned_Text_Files: str = r"C:\Users\ccxvc\source\repos\AutoFlashcards_PY\Temp\Temp_Cleaned_Text_Files"  # Cleaned text directory
Temp: str = r"C:\Users\ccxvc\source\repos\AutoFlashcards_PY\Temp"  # Temp directory
Temp_Notes_Json_Files: str = r"C:\Users\ccxvc\source\repos\AutoFlashcards_PY\Temp\Temp_Notes_Json_Files"  # JSON notes directory

# Anki Connect Configuration
Ankiconnect_Address: str = 'http://127.0.0.1:8765'  # AnkiConnect API address
StandardTempDeckName: str = "TempDeck"  # Default deck name for imported cards