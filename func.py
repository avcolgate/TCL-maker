from keywords import keyword_list

# True for int, float any sign
def is_number(str):
    try:
        float(str)
        return True
    except ValueError:
        return False

def is_good_name(name):
    if name in keyword_list:
        return 0

    if not (str(name[0]).isalpha() or str(name[0]) == '_'):
        return 0
    return 1

def skip_comment(line):
    if '//' in line:
        line = line[:line.find('//')]

    return line