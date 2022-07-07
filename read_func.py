import re
from class_module import *
from class_line import *

def read_section_name(line):
    temp = line.content
    name = temp[temp.find('module')+len('module')+1:temp.find('(')]

    return name

def read_section_params(line):
    temp = line.content
    temp = temp.replace('parameter', '')
    temp = re.sub("[;| |\t]","", temp)
    temp_name, temp_size = temp.split('=')

    param = Param(temp_name, int(temp_size))
    return param

def read_section_pins(line, param_list):
    temp = line.content
    pin_arr = []

    if 'input' in temp:      # detection of direction 
        pin_direction = 'input'
    elif 'output' in temp:
        pin_direction = 'output'
    temp = temp.replace(pin_direction, '').replace('reg', '')  # ? ignore 'reg'?
    # print(pin_direction, end=' ')

    temp_size = temp[temp.find('['):temp.find(']')+1]

    if (temp_size):                                            # * parametric size

        temp_name = temp[temp.find(']')+1:]       # copying names only
        temp_name=re.sub("[;| |\t]","", temp_name)
        temp_name_arr = temp_name.split(',')
        # print('temp_name_arr:', temp_name_arr) # names array

        temp_size = re.sub("[\[|\]| |\t]","", temp_size) # deleting [] and whitespaces
        temp_size_arr = temp_size.split(':')
        start_val, end_val = temp_size_arr
        # print('temp_size_arr:', temp_size_arr) # sizes array

        if not start_val.isdigit():                             # if parameter in LEFT part

            if '-' in start_val:                      # substract
                start_val = start_val.split('-')
                start_val_left, start_val_right = start_val

                if not start_val_left.isdigit():                  # parameter in left subpart
                    for param in param_list:
                        if param.name == start_val_left:
                            start_val_left = param.value

                if not start_val_right.isdigit():                 # parameter in right subpart
                    for param in param_list:
                        if param.name == start_val_right:
                            start_val_right = param.value

                start_val = int(start_val_left) - int(start_val_right)

            elif '+' in start_val:                    # add (???)
                start_val = start_val.split('+')
                start_val_left, start_val_right = start_val

                if not start_val_left.isdigit():                  # parameter in left subpart
                    for param in param_list:
                        if param.name == start_val_left:
                            start_val_left = param.value

                if not start_val_right.isdigit():                 # parameter in right subpart
                    for param in param_list:
                        if param.name == start_val_right:
                            start_val_right = param.value

                start_val = int(start_val_left) + int(start_val_right)


        if not end_val.isdigit():                               # if parameter in RIGHT part

            if '-' in end_val:                        # substract
                end_val = end_val.split('-')
                end_val_left, end_val_right = end_val

                if not end_val_left.isdigit():                  # parameter in left subpart
                    for param in param_list:
                        if param.name == end_val_left:
                            end_val_left = param.value

                if not end_val_right.isdigit():                 # parameter in right subpart
                    for param in param_list:
                        if param.name == end_val_right:
                            end_val_right = param.value

                end_val = int(end_val_left) - int(end_val_right)
                
            elif '+' in end_val:                      # add (???)
                end_val = end_val.split('+')
                end_val_left, end_val_right = end_val

                if not end_val_left.isdigit():                  # parameter in left subpart
                    for param in param_list:
                        if param.name == end_val_left:
                            end_val_left = param.value

                if not end_val_right.isdigit():                 # parameter in right subpart
                    for param in param_list:
                        if param.name == end_val_right:
                            end_val_right = param.value

                end_val = int(end_val_left) + int(end_val_right)
                

        delta_val = abs(int(end_val) - int(start_val)) + 1
        
        for pin_name in temp_name_arr:
            pin = Pin(pin_name, pin_direction, int(delta_val))
            pin_arr.append(pin)

    else:                                                      # * simple size (=1)

        temp_name = re.sub("[;| |\t]", "", temp)
        temp_name_arr = temp_name.split(',')
        # print(temp_name_arr)

        for pin_name in temp_name_arr:
            pin = Pin(pin_name, pin_direction, 1)
            pin_arr.append(pin)

    return pin_arr
