import re
from keywords import keyword_list

# True for int, float any sign
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


def define_expression(val_left, val_right, param_list, define_list):
    check = 0

    if not is_number(val_left):
        for par in param_list:
            if val_left == par.name:
                val_left = par.value
                check += 1
                break
        for define in define_list:
            if '`' + define.name == val_left:
                val_left = define.value
                check += 1
                break
    else:
        check += 1

    if not is_number(val_right):
        for par in param_list:
            if val_right == par.name:
                val_right = par.value
                check += 1
                break
        for define in define_list:
            if '`' + define.name == val_right:
                val_right = define.value
                check += 1
                break
    else:
        check += 1

    return val_left, val_right, check