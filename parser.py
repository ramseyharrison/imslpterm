import sys
from main import add_new_composer, get_imslp_list, get_local_list,local_composer_list,list_by_id, is_local
import argparse
ID_STR_FMT = "{} : {}"

def fmt_tuple_id_name(name): return lambda x : (x['id'], x[name])

def list_table_output(list, fmt_str, fmt_tuple):
    str = ""
    for x in list:
        str += fmt_str.format(*fmt_tuple(x)) + "\n"
    return str

parser = argparse.ArgumentParser()
parser.add_argument("composer")
parser.add_argument("-s","--save", action="store_true")
parser.add_argument("-c","--composition")
args = parser.parse_args()
name = ''
output = ""
data = []
if(args.save):
    add_new_composer(args.composer)
# elif(args.composition):
#     data.append(composition_list(args.composer)[int(args.composition)])
#     name = 'Page Name'
else:
    if(args.composer == "list"):
        data = local_composer_list()
        name = 'name'
    elif(args.composer.isnumeric()):            
        data = list_by_id(int(args.composer))
        name = 'Page Name'
    else:
        if(is_local(args.composer)):
            data = get_local_list(args.composer)
        else:
            data = get_imslp_list(args.composer)

        name = 'Page Name'
if(data):
    output = list_table_output(data,ID_STR_FMT, fmt_tuple_id_name(name))
    sys.stdout.write(output)