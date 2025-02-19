# AutoFlashcards_PY

## Description
AutoFlashcards_PY is a Python-based tool designed to automate the creation of flashcards from various text sources. By leveraging natural language processing and integration with platforms like Anki, it streamlines the learning process by generating flashcards efficiently.

## Features
- **Text Extraction**: Utilize `PDF_lib.py` and `Text_lib.py` to extract text from PDFs and other formats.
- **Flashcard Generation**: Automatically generate flashcards using `AutoFlashcards.py`.
- **Anki Integration**: Seamlessly add flashcards to Anki decks via `AnkiConnect.py`.
- **AI Assistance**: Enhance flashcard content with AI through `ai_client.py`.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/AbdulElbaco/AutoFlashcards_PY.git
   cd AutoFlashcards_PY
   ```

2. **Set Up Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   Ensure you have **Python 3.10 - 3.11** installed, then install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Configure Global Variables**:
   - Edit `Global_Variables.py` to set paths and other configurations as needed.

2. **Run the Main Script**:
   ```bash
   python AutoFlashcards.py
   ```

   This will initiate the process of generating flashcards from your specified text sources.

## Dependencies
The project relies on the following libraries:
- `aspose-pdf==25.1.0`
- `cffi==1.17.1`
- `charset-normalizer==3.4.1`
- `cryptography==44.0.1`
- `pip==25.0.1`
- `pycparser==2.22`
- `pycryptodome==3.21.0`
- `PyPDF2==3.0.1`
- `setuptools==65.5.0`

For a complete list, refer to `requirements.txt`.

## Contributing
Contributions are welcome! Feel free to fork the repository, make enhancements, and submit pull requests.

## License
This project is licensed under the MIT License.