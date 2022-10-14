
import os
from verilog_keywords import keyword_list

def define_init_data(init_data):
    if len(init_data) < 1:
        print('fatal: a path is not specified\n')
        exit()
    elif os.path.exists(init_data[0]):
        path = init_data[0].replace('\\', '/')
        if os.stat(path).st_size == 0:
            print('fatal: input file is empty\n')
            exit()
    else:
        print('fatal: input file does not exist or bad name of file\n')
        exit()


    # only path specified
    if len(init_data) == 1:
        specified_name = ''
    
    # manual mode and module name is specified
    elif len(init_data) == 3 and (init_data[1] == '-m' or init_data[1] == '--manual'):
        specified_name = init_data[2]
        if not is_good_name(specified_name):
            print("fatal: bad specified module name '%s'\n" % (specified_name))
            exit()
    else:
        print('fatal: bad command line arguments\n')
        exit()

    return path, specified_name

# True for int and float any sign
def is_number(str):
    try:
        float(str)
        return True
    except ValueError:
        return False

def is_good_name(name):
    # cannot be a keyword
    if name in keyword_list:
        return 0

    # can include only letters, digits, _, $
    for letter in name:
        if letter.isalpha() or letter.isdigit() or letter == '_' or letter == '$':
            continue
        else:
            return 0

    # starts with alpha
    if not str(name[0]).isalpha():
        return 0

    # cannot start with dollar
    if str(name[0]) == '$':
        return 0

    return 1

def skip_comment(line):
    if '//' in line:
        line = line[:line.find('//')]

    return line
