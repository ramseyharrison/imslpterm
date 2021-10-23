import os
from typing import Type
import helpers
from helpers import add_id_to_list_dict,read_json,write_to_json
from imslp.interfaces import scraping

DIRPATH = os.path.abspath(os.path.dirname(__file__))
IMSLP_JSON_PATH = DIRPATH + '/composer_json/{composer}.json'
LIST_JSON_PATH = DIRPATH + '/composers.json'
SAVED_JSON_PATH = DIRPATH + '/saved.json'
# returns dict of composer according to local id

def imslp_list(x) : return add_id_to_list_dict(list(scraping.fetch_category_table(category_name = x)))

def get_local_list(x) : return read_json(IMSLP_JSON_PATH.format(composer=x))

#returns list of locally stored composers
def local_composer_list():
    return helpers.read_json(LIST_JSON_PATH)

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

def composition_list(composer):
    compositions = lambda y, x : y(x)
    method = imslp_list #default method
    data = composer
    
    try:
        composer = int(composer) #check to see if CL argument was a local "id"
        list = local_composer_list()
        composer_object = {}
        try:
            composer_object = list[composer]
        except TypeError:
            print("No Saved Composers")
            return None
        except IndexError:
            print("ID doesn't exist")
            return None
        method = get_local_list
        data = composer_object['name']
    except ValueError:
        if(is_local(composer)):
            method = get_local_list

    return compositions(method,data)


def add_new_composer(composer):

    # ensure needed directories exist
    try:
        helpers.composer_directory_check()
    except:
        print("Error with directories")
        return None

    try:
        works = composition_list(composer)
    except ConnectionError:
        print("Invalid Composer Name")
        return None 

    works = helpers.add_id_to_list_dict(works)
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


