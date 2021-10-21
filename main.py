import os
import json
import helpers
import mwclient
from imslp.client import ImslpClient
from imslp.interfaces import scraping

DIRPATH = os.path.abspath(os.path.dirname(__file__))
IMSLP_JSON_PATH = DIRPATH + '/imslp_json/{composer}.json'
LIST_JSON_PATH = DIRPATH + '/composers.json'


def fetch_imslp_json(composer):
    client = ImslpClient()
    PATH = IMSLP_JSON_PATH

    works = list(client.search_works(composer=composer))
    return helpers.interact_with_json_file(
        PATH.format(composer=composer),
        "w",
        lambda f: f.write(json.dumps(works)))

# returns dict of composer according to local id


def local_composer_list():
    return helpers.read_json(LIST_JSON_PATH)

# returns dict of composition from local ids


def composition_list(composer_id):
    composer_object_name = helpers.read_json(LIST_JSON_PATH)[composer_id]['name']
    return helpers.read_json(IMSLP_JSON_PATH.format(composer=composer_object_name))

# method called to add new composer to local library
# invokes IMSLP package
# name must be properly formatted IMSLP category name


def add_new_composer(composer):
    #imslp_package client
    client = ImslpClient()

    #ensure needed directories exist
    try:
        helpers.directory_check()
    except:
        print("Error with directories")
        return None
    
    works = list(client.search_works(composer=composer))
    works.sort(key=lambda x: x['intvals']['worktitle'])

    
    #change id a local integer id
    counter = 0 
    for x in works:
        x['id'] = counter
        counter += 1

    helpers.interact_with_json_file(IMSLP_JSON_PATH.format(
        composer=composer),
        "w",
        lambda f: f.write(json.dumps(works)))
    
    composers = helpers.read_json(LIST_JSON_PATH)
    composers.append(
        {
            "id": len(composers),  # local ID for composer
            "name": composer,
        }
    )
    helpers.interact_with_json_file(
        LIST_JSON_PATH,
        "w",
        lambda f: f.write(json.dumps(composers)))
    

def remove_composer(composer):
    composers = local_composer_list()
    new_list = []
    counter = 0
    for x in composers:
        if(x['name'] == composer):
            continue
        new_list.append(
            {
                "id": counter,
                "name" : x['name'],
            }
        )
        counter+=1
    helpers.interact_with_json_file(
        LIST_JSON_PATH,
        "w",
        lambda f: f.write(json.dumps(new_list)))

