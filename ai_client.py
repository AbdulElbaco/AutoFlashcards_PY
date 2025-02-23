"""
AI Client Module

This module handles interactions with AI services for text processing and flashcard generation.
It uses OpenRouter API to access AI models for text cleaning and flashcard creation.

Dependencies:
    - requests
    - json
    - Global_Variables (for API keys and configuration)
"""
import Global_Variables
from openai import OpenAI


def get_clients_response(prompt: str):
    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=Global_Variables.openrouterAPI_Key,
    )

    completion = client.chat.completions.create(
  model=Global_Variables.LLM_AI_model,
  messages=[
    {
      "role": Global_Variables.role,
      "content": [
        {
          "type": "text",
          "text": prompt
        }
      ]
    }
  ]
)
    if completion is not None:
        return completion.choices[0].message.content
    else:
        print(completion.error)
        return None

def CleanAndFormatTextWithAI(text: str, page_number: int) -> str:
    """
    Cleans and formats extracted text using AI processing.

    Args:
        text (str): Raw text extracted from PDF.
        page_number (int): Page number being processed (for context).

    Returns:
        str: Cleaned and formatted text.

    Raises:
        RuntimeError: If AI service fails to process the text.
        requests.RequestException: If API call fails.
        ValueError: If response is invalid.
    """
    #Prepare prompt
    prompt = f"Return only the cleaned and well-formatted version of the following text. Ensure proper spacing, punctuation, and readability while preserving the original meaning.\n\nText:\n{text}"
    #Get response from AI
    text = get_clients_response(prompt)
    if page_number is None:
        #Trim and return
        return text.strip()
    else:
        #Trim and save
        with open(f"{Global_Variables.Temp_Cleaned_Text_Files}/{page_number}.txt", "w", encoding="utf-8", errors="ignore") as f:
            f.write(text.strip())
        return text.strip()

def GetListOfNotes_From_AI(text: str, page_number: int) -> list:
    """
    Generates flashcards from text using AI processing.

    Args:
        text (str): Cleaned text to generate flashcards from.

    Returns:
        list: List of dictionaries containing flashcard data.
            Each dictionary has:
            - 'Front': str (question/prompt)
            - 'Back': str (answer)
            - 'deckName': str (always 'TempDeck')
            - 'modelName': str (always 'Basic')

    Raises:
        json.JSONDecodeError: If AI response is not valid JSON.
        requests.RequestException: If API call fails.
        ValueError: If response format is invalid.
    """
    #Prepare prompt
    prompt = (
    "Generate as many high-quality flashcards as possible from the given text.\n"
    "Ensure that each flashcard is clear, concise, and directly relevant to the content.\n"
    "\n"
    "### Flashcard Format:\n"
    "Each flashcard must follow JSON format like in the example below:\n"
    "{\"deckName\": \"TempDeck\",\"modelName\": \"Basic\",\"fields\": {\"Front\": \"Front content goes here\",\"Back\": \"Back content goes here\"}}"
    "\n"
    "### Additional Guidelines:\n"
    "- **Consistency:** Use 'TempDeck' as the deckName and 'Basic' as the modelName for all flashcards.\n"
    "- **Separation:** Separate each flashcard with '$$$$'.\n"
    "- **Content Quality:** The questions should be meaningful and structured to promote effective learning.\n"
    "- **Avoid extraneous content:** Do not include comments, explanations, or any additional text outside the flashcards.\n"
    "- **Textual Focus:** Ensure the 'Front' field contains a well-formed question or prompt, and the 'Back' field contains a precise answer extracted from the text.\n"
    "\n"
    f"### Text to Process:\n{text}"
)
    #Get response from AI
    response = get_clients_response(prompt)
    if response is None or response == "":
        return []
    else:
        #Save the response in text file for the developer to check later
        with open(f"{Global_Variables.Temp_Notes_Json_Files}/Notes_list({page_number}).txt", "w", encoding="utf-8", errors="ignore") as f:
            f.write(response)
        #Retrun results List
        return response.split("$$$$")