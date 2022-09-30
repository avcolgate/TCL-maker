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


def define_expression(val_left, val_right, param_list, define_list, line_num):
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

    if check < 2:
        print("fatal: unknown parameter in pin size, line %i\n" % (line_num + 1))
        exit()

    return val_left, val_right


def define_param_define(val, param_list, define_list):
    check = 0

    if not is_number(val):
        for par in param_list:
            if val == par.name:
                val = par.value
                check += 1
                break
        for define in define_list:
            if '`' + define.name == val:
                val = define.value
                check += 1
                break
    else:
        check += 1

    return val, check

def convert_number(size_val, my_base, param_name, line_num):
    my_dict = {'d': 10, 'b': 2, 'h': 16, 'o': 8}
    param_value = size_val[size_val.find(my_base)+1:]

    try:
        param_value = int(param_value, base=my_dict[my_base])
    except:
        print("fatal: the size of parameter '%s' does not belong to it's notation system, line %i\n" % (param_name, line_num + 1))
        exit()
    
    return param_value

def calc_pin_size_expression(value, param_list, define_list, temp_name, line_num):

    #TODO добавить << >>
    char_minus, char_plus, char_mul, char_div = ['-', '+', '*', '/']

    if not is_number(value):

        if char_minus in value:
            left_part, right_part = value.split(char_minus)
            left_part, right_part = define_expression(left_part, right_part, param_list, define_list, line_num)
            value = int(left_part) - int(right_part)

        elif char_plus in value:
            left_part, right_part = value.split(char_plus)
            left_part, right_part = define_expression(left_part, right_part, param_list, define_list, line_num)
            value = int(left_part) + int(right_part)

        elif char_mul in value:
            left_part, right_part = value.split(char_mul)
            left_part, right_part = define_expression(left_part, right_part, param_list, define_list, line_num)
            value = int(left_part) * int(right_part)

        elif char_div in value:
            left_part, right_part = value.split(char_div)
            left_part, right_part = define_expression(left_part, right_part, param_list, define_list, line_num)
            if int(right_part) != 0:
                value = int(left_part) / int(right_part)
            else:
                print("fatal: dividing by 0 in size of pin '%s', line %i\n" % (temp_name, line_num + 1))
                exit()
                
        else:
            value, check = define_param_define(value, param_list, define_list)
            print(value)
            if not str(value).isdigit():
                print("fatal: unknown operation in size of pin '%s', line %i\n" % (temp_name, line_num + 1))
                exit()
        
        if value < 0:
            print("fatal: arguments in size must be positive integer. Pin '%s', line %i\n" % (temp_name, line_num + 1))
            exit()

    return value