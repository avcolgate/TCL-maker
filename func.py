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