import requests
import Global_Variables
import json

def get_clients_response(prompt: str):
    response = requests.post(
        url= Global_Variables.url,
        headers={
            "Authorization": f"Bearer {Global_Variables.openrouterAPI_Key}",
            "Content-Type": "application/json"
        },
        json={
            "model": Global_Variables.LLM_AI_model,
            "messages": [
                {
                    "role": Global_Variables.role,
                    "content": prompt  # Using the parameter here
                }
            ]
        }
    )

    if response.status_code == 200:
        data = response.json()
        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError):
            return "Error: Unexpected response format"
    else:
        return f"Error {response.status_code}: {response.text}"

def CleanAndFormatTextWithAI(text: str, DocumentNumber = None):
  #Prepare prompt
  prompt = f"Return only the cleaned and well-formatted version of the following text. Ensure proper spacing, punctuation, and readability while preserving the original meaning.\n\nText:\n{text}"
  #Get response from AI
  text = get_clients_response(prompt)
  if DocumentNumber is None:
    #Trim and return
    return text.strip()
  else:
    #Trim and save
    with open(f"{Global_Variables.Temp_Cleaned_Text_Files}/{DocumentNumber}.txt", "w") as f:
         f.write(text.strip())
         return text.strip()

def GetListOfNotes_JsonFormat_From_AI(text: str):
    #Prepare prompt
    prompt = (
        "Generate as many high-quality flashcards as possible from the following text.\n\n"
        "Format the output as a valid JSON list of flashcards.\n"
        "Each flashcard should have a 'Front' field (question or prompt) and a 'Back' field (answer).\n"
        "Each flashcard should have a 'deckName' field (hard-coded as 'TempDeck') and a 'modelName' field (hard-coded as 'Basic').\n"
        "If no flashcards can be created, return an empty JSON array [].\n\n"
        f"Text to process:\n{text}"
    )
    #Get response from AI
    response = get_clients_response(prompt)
    #Save response in txt file
    with open(f"{Global_Variables.Temp_Cleaned_Text_Files}/NotesList.txt", "w") as f:
         f.write(response)
    if response is None or response == "":
        return []
    # Convert string to JSON list (Python list)
    try:
        json_list = json.loads(response)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return []
    #Retrun results List
    return json_list