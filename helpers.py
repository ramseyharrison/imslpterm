import os
import json
from json.decoder import JSONDecodeError

#method to take care of both read/write for JSON.
#rwmethod is either f.read() or f.write()
#rwoption is a flag
def interact_with_json_file(path, rwoption, rwmethod):
    try:    
        with open(path, rwoption) as f:
            return rwmethod(f)
    except FileNotFoundError:
        print(rwoption + " fail for path " + path)
        return None

# expects a path to json file,returns "decoded" json

def read_json(path):
    try :
        return json.loads(interact_with_json_file(path, "r", lambda f: f.read()))
    except JSONDecodeError:
        print("json_str_to_list(): str is improper JSON, returning None")
        return None


def directory_check():
    if not os.path.exists('imslp_json/'):
        os.makedirs('imslp_json')
    