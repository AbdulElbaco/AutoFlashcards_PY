import os
from Text_lib import ExtractTextFromPDF
from PDF_lib import convert_unsearchable_to_searchable
from PDF_lib import split_pdf
from ai_client import CleanAndFormatTextWithAI
from ai_client import GetListOfNotes_JsonFormat_From_AI
from AnkiConnect import AddNotes
import Global_Variables

def main():
    # First Make the PDF file searchable
    inputfile =r"C:\Users\ccxvc\Downloads\38833FF26BA1D.UnigramPreview_g9c9v27vpyspw!App\18-C#.pdf"
    convert_unsearchable_to_searchable(inputfile, Global_Variables.Temp_Searchable_PDF)

    #Split the searchable PDF file into individual pages, and return the number of pages for further processing
    NumOfPages = split_pdf(Global_Variables.Temp_Searchable_PDF, Global_Variables.Temp_Splited_Pages)
    

    #Extract text from the Pages that were split, they were named as 1.pdf, 2.pdf, 3.pdf, etc.
    for i in range(NumOfPages):
        ExtractTextFromPDF(f"{Global_Variables.Temp_Splited_Pages}/{i+1}.pdf")

    #Open and read a text file
    for i in range(NumOfPages):
        with open(f"{Global_Variables.Temp_Extracted_Text_Files}/{i+1}.txt", "r") as ExtractedTextFile:
            Text =ExtractedTextFile.read()
            Text = CleanAndFormatTextWithAI(Text, i+1)
            #Save text in a txt file
            with open(f"{Global_Variables.Temp_Cleaned_Text_Files}/{i+1}.txt", "r+") as CleanedTextFile:
                Text =ExtractedTextFile.read()
                Text = CleanAndFormatTextWithAI(Text, i+1)
                CleanedTextFile.seek(0)  # Seek to the beginning of the file
                CleanedTextFile.write(Text)  # Write to the file
                CleanedTextFile.truncate()  # Truncate the file to the current position

    #Close the files
    ExtractedTextFile.close()
    CleanedTextFile.close()

    #Create list of notes using AI from the cleaned text
    NotesList = []
    for i in range(NumOfPages):
        with open(f"{Global_Variables.Temp_Cleaned_Text_Files}/{i+1}.txt", "r") as CleanedTextFile:
            NotesList.append(GetListOfNotes_JsonFormat_From_AI(CleanedTextFile.read()))

            CleanedTextFile.close()
    
    #Add notes to Anki
    AddNotes(NotesList)
    print("All notes added successfully!")


if __name__ == '__main__':
    main()