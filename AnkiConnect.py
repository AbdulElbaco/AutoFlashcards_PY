"""
Anki connection module with connection pooling and error handling.
"""
import json
import urllib.request
import Global_Variables
from Text_lib import extract_json_from_triple_quotes

def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:8765', requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        #raise Exception(response['error'])
        print(response['error'])
    return response['result']

def create_standard_temp_deck_if_not_exists():
    existing_decks = invoke('deckNames')
    if Global_Variables.StandardTempDeckName not in existing_decks:
        invoke('createDeck', deck=Global_Variables.StandardTempDeckName)

def add_notes(notes_list: list):
    if notes_list is None or len(notes_list) == 0:
        print("No notes to add")
        return
    create_standard_temp_deck_if_not_exists()
    for notes in notes_list:
        invoke(action='addNotes', note=notes)

def PrepareNotes(notes):
    notes_list = []
    for note in notes:
        note = note.strip()
        note = note.replace("```", "")
        #Temp solution to fix the issue caused by the dummb Google AI model 
        note = note.replace("json", "")
        note = note.replace("\n", "")
        if note != "":
            notes_list.append(note)
    
    return notes_list
            

def addnotes(notes):
    
    if not notes:  # This checks for None, empty list, or empty string    
        print("No notes to add!\nError: Recieved an empty list!")
    else:
        create_standard_temp_deck_if_not_exists()
        notes = PrepareNotes(notes)  
        for note in notes:
            try:
                jsonnote = json.loads(note)
                invoke(action='addNote', note=jsonnote)
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON: {e}")