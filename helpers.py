import os
import json
from json.decoder import JSONDecodeError
from urllib.request import urlopen

from bs4 import BeautifulSoup

#method to take care of both read/write for JSON.
#rwmethod is either f.read() or f.write()
#rwoption is a flag
def interact_with_json_file(path, rwoption, rwmethod):
    try:
        with open(path, rwoption) as f:
            return rwmethod(f)
    except FileNotFoundError:
        return None
# expects a path to json file,returns "decoded" json

def read_json(path):
    try :
        json_str = interact_with_json_file(path, "r", lambda f: f.read())
        if(json_str is None):
            return None
        return json.loads(json_str)
    except JSONDecodeError:
        print("json_str_to_list(): str is improper JSON, returning None")
        return None

def write_to_json(path, list):
    return interact_with_json_file(path,
        "w",
        lambda f: f.write(json.dumps(list)))

def composer_directory_check():

    if not os.path.exists('composer_json/'):
        os.makedirs('composer_json')

def add_id_to_list_dict(list):
    counter = 0 
    for x in list:
        x['id'] = counter
        counter += 1
    return list


def scrape_general_information():
    html = urlopen("https://imslp.org/index.php?title=Symphony_No.9_in_D_minor%2C_WAB_109%2F143_(Bruckner%2C_Anton)&customcat=ccperson1")
    content = html.read()
    soup = BeautifulSoup(content)
    div_table = soup.find('div',class_="wi_body")
    table = div_table.table
    rows = table.findAll("tr")
    
    