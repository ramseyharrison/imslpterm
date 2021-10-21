import sys
import main
from collections import deque

ID_STR_FMT = "{} : {}"

COMPOSER_LIST = "list-composers"
COMPOSITION_LIST = "list-compositions"
ADD_COMPOSER = "add-composer"
REMOVE_COMPOSER = "remove-composer"
COMPOSITION_PAGE = "composition"

def id_str_fmt(tuple):
    return ID_STR_FMT.format(*tuple)

def list_table_output(list, format_tuple):
    str = ""
    for x in list:
        str += id_str_fmt(format_tuple(x)) + "\n"
    return str

def parse(args: list) -> str:
    command = args.popleft()
    return_msg = ""
    if(command == COMPOSER_LIST):
        method = main.local_composer_list()
        def tuple(x): return (x['id'], x['name'])
        return_msg = list_table_output(method, tuple)
    elif(command == COMPOSITION_LIST):
        method = main.composition_list(int(args.popleft()))
        def tuple(x): return (x['id'], x['intvals']['worktitle'])
        return_msg = list_table_output(method, tuple)

    elif(command == ADD_COMPOSER):
        composer_name = args.popleft()
        try:
            print("Calling IMSLP package for " + composer_name)
            main.add_new_composer(composer_name)
        except:
            main.remove_composer(composer_name)
        return_msg = "Succesfully Added " + composer_name

    elif(command == REMOVE_COMPOSER):
        composer_id = int(args.popleft())
        composer = main.local_composer_list()[composer_id]['name']
        main.remove_composer(composer)
        return_msg = "Removed " + composer

    elif(command == COMPOSITION_PAGE):
        composition_data = list(map(int, args.popleft().split(".")))
        try:
            composer = main.local_composer_list()[composition_data[0]]
            composition = main.composition_list(composition_data[0])[composition_data[1]]
            return_msg += composition['intvals']['worktitle'] + "\n"
            return_msg += composer['name'] + "\n"
            return_msg += "local id " + str(composition['id']) + "\n"
        except IndexError:
            return_msg = "Composition/Composer doesn't exist\n"
    return return_msg

queue = deque(sys.argv)
queue.popleft()
sys.stdout.write(parse(queue))
