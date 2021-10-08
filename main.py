import os
import json
import json_helpers

from imslp import client

DIRPATH = os.path.abspath(os.path.dirname(__file__))
IMSLP_JSON_PATH = DIRPATH + '/imslp_json/{composer}.json'
LOCAL_JSON_PATH = DIRPATH + '/local_json/{composer}.json'
LIST_JSON_PATH = DIRPATH + '/composers.json'

client = client.ImslpClient


#Main method for getting and storing IMSLP composer information
def process_composer(composer):
    fetch_imslp_json(composer) #calls IMSLP package
    cleaned_compositions = []
    compositions = json_helpers.read_json(
        IMSLP_JSON_PATH.format(composer=composer))
    compositions.sort(key=lambda x: x['intvals']['worktitle']) #sorts by worktitle name

    for index in range(len(compositions)):
        #stores desired information from IMSLP package search 
        #cat would be the official catalog number of composition, if it exists(not intval icatno)
        #for purpose of url_images see get_images()
        cleaned_compositions.append(
            {
                'id':   index,
                'title': compositions[index]['intvals']['worktitle'],
                'permlink': compositions[index]['permlink'],
                'cat': "",
                'url_images': []
            }
        )

    json_helpers.interact_with_json_file(LOCAL_JSON_PATH.format(
        composer=composer),
        "w",
        lambda f: f.write(json.dumps(cleaned_compositions)))


def fetch_imslp_json(composer):
    PATH = IMSLP_JSON_PATH

    works = list(client.search_works(composer=composer))
    return json_helpers.interact_with_json_file(
        PATH.format(composer=composer),
        "w",
        lambda f: f.write(json.dumps(works)))

#returns dict of composer according to local id

def local_composer_list():
    return json_helpers.read_json(LIST_JSON_PATH)

#returns dict of composition from local ids
def get_local_composition(composer_id, composition_id):

    try:
        composer_object_name = json_helpers.read_json(LIST_JSON_PATH)[composer_id]['name']
        return json_helpers.read_json(LOCAL_JSON_PATH.format(composer=composer_object_name))[composition_id]
    except IndexError:
        print("get_local_composition : index error")
        return None


#method called to add new composer to local library
#invokes IMSLP package
#name must be properly formatted IMSLP category name

def addNewComposer(name):
    PATH = LIST_JSON_PATH  
    composers = json_helpers.read_json(PATH)
    composers.append(
        {
            "id": len(composers), #local ID for composer
            "name": name,
        }
    )
    json_helpers.interact_with_json_file(
        PATH,
        "w",
        lambda f: f.write(json.dumps(composers)))
    process_composer(name)

#addNewComposer("Brahms, Johannes")


#example of desired features
def get_images(composition):
    #method would expect a local composition dictionary
    #and from its permlink(stored IMSLP package's permlink) would request image links from IMSLP
    #and store them in the local dictionary attributed to each composition(created in process_composer)

    link = composition['permlink']
    #client.get_images(link) 
    pass