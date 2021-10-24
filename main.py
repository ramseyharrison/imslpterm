import os
from typing import Type

from requests.api import get
import helpers
from helpers import add_id_to_list_dict,read_json,write_to_json
from imslp.interfaces import scraping

DIRPATH = os.path.abspath(os.path.dirname(__file__))
IMSLP_JSON_PATH = DIRPATH + '/composer_json/{composer}.json'
LIST_JSON_PATH = DIRPATH + '/composers.json'
SAVED_JSON_PATH = DIRPATH + '/saved.json'

def get_imslp_list(x) : return add_id_to_list_dict(list(scraping.fetch_category_table(category_name = x)))

def get_local_list(x) : return read_json(IMSLP_JSON_PATH.format(composer=x))

def local_composer_list(): return helpers.read_json(LIST_JSON_PATH)

def list_by_id(id):
    try:
        composer = local_composer_list()[id]
        return get_local_list(composer['name'])
    except:
        print("ID doesn't exist")
        
#checks if composer name is local
def is_local(composer_name):
    names = []
    list = local_composer_list()
    if(list is None):
        return False
    for x in list:
        names.append(x['name'])
    return composer_name in names

#returns list of compositions for composer name
#excepts either a local ID generated upon add_new_composer
#or a IMSLP composer name


def add_new_composer(composer):

    # ensure needed directories exist
    try:
        helpers.composer_directory_check()
    except:
        print("Error with directories")
        return None
    try:
        works = get_imslp_list(composer)
    except ConnectionError:
        print("Invalid Composer Name")
        return None 

    composers = local_composer_list()
    if(composers is None):
        composers = []
        f = open(LIST_JSON_PATH, 'w')

    composers.append(
        {
            "id": len(composers),  # local ID for composer
            "name": composer,
        }
    )
   
    write_to_json(LIST_JSON_PATH,composers)
    write_to_json(IMSLP_JSON_PATH.format(composer=composer),works)

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
                "name": x['name'],
            }
        )
        counter += 1
    write_to_json(LIST_JSON_PATH,new_list)
