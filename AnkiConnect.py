import json
import urllib.request
import Global_Variables

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
        raise Exception(response['error'])
    return response['result']

def create_standard_temp_deck_if_not_exists():
    existing_decks = invoke('deckNames')
    if Global_Variables.StandardTempDeckName not in existing_decks:
        invoke('createDeck', deck=Global_Variables.StandardTempDeckName)

def AddNotes(NotesList):
    create_standard_temp_deck_if_not_exists()
    
    if not isinstance(NotesList, list):
        raise TypeError("Expected a list of notes")
    else:
        invoke('addNotes',notes=NotesList)