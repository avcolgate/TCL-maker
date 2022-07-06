import re
from module_class import *
from module_line import *

PATH = './src/spm.v'
top_module_name = 'spm'
    
def read_section_params(curr_line):
    temp = curr_line.replace('parameter', '')
    temp = re.sub("[;| |\t]","", temp)

    temp_name, temp_size = temp.split('=')

    parameter = Param(temp_name, int(temp_size))
    module.params.append(parameter)

def read_section_pins(curr_line):
    temp = curr_line

    if 'input' in temp:      # type detection
        pin_type = 'input'
    elif 'output' in temp:
        pin_type = 'output'
    temp = temp.replace(pin_type, '').replace('reg', '')
    # print(pin_type, end=' ')

    temp_size = temp[temp.find('['):temp.find(']')+1]

    if (temp_size):                                            # with parametric size

        temp_name = temp[temp.find(']')+1:]       # copying names only
        temp_name=re.sub("[;| |\t]","", temp_name)
        temp_name_arr = temp_name.split(',')
        # print('temp_name_arr:', temp_name_arr) # names array

        temp_size = re.sub("[\[|\]| |\t]","", temp_size) # deleting [] and whitespaces
        temp_size_arr = temp_size.split(':')
        start_val, end_val = temp_size_arr
        # print('temp_size_arr:', temp_size_arr)     # sizes array

        if not start_val.isdigit():                             # if parameter in LEFT part

            if '-' in start_val:                      # substract
                start_val = start_val.split('-')
                start_val_left, start_val_right = start_val

                if not start_val_left.isdigit():                  # parameter in left subpart
                    for param in module.params:
                        if param.name == start_val_left:
                            start_val_left = param.value

                if not start_val_right.isdigit():                 # parameter in right subpart
                    for param in module.params:
                        if param.name == start_val_right:
                            start_val_right = param.value

                start_val = int(start_val_left) - int(start_val_right)

            elif '+' in start_val:                    # add (???)
                start_val = start_val.split('+')
                start_val_left, start_val_right = start_val

                if not start_val_left.isdigit():                  # parameter in left subpart
                    for param in module.params:
                        if param.name == start_val_left:
                            start_val_left = param.value

                if not start_val_right.isdigit():                 # parameter in right subpart
                    for param in module.params:
                        if param.name == start_val_right:
                            start_val_right = param.value

                start_val = int(start_val_left) + int(start_val_right)


        if not end_val.isdigit():                               # if parameter in RIGHT part

            if '-' in end_val:                      # substract
                end_val = end_val.split('-')
                end_val_left, end_val_right = end_val

                if not end_val_left.isdigit():                  # parameter in left subpart
                    for param in module.params:
                        if param.name == end_val_left:
                            end_val_left = param.value

                if not end_val_right.isdigit():                 # parameter in right subpart
                    for param in module.params:
                        if param.name == end_val_right:
                            end_val_right = param.value

                end_val = int(end_val_left) - int(end_val_right)
                
            elif '+' in end_val:                    # add (???)
                end_val = end_val.split('+')
                end_val_left, end_val_right = end_val

                if not end_val_left.isdigit():                  # parameter in left subpart
                    for param in module.params:
                        if param.name == end_val_left:
                            end_val_left = param.value

                if not end_val_right.isdigit():                 # parameter in right subpart
                    for param in module.params:
                        if param.name == end_val_right:
                            end_val_right = param.value

                end_val = int(end_val_left) + int(end_val_right)
                

        delta_val = abs(int(end_val) - int(start_val)) + 1
        
        for pin_name in temp_name_arr:
            pin = Pin(pin_name, int(delta_val))

            if pin_type == 'input':
                module.inputs.append(pin)
            elif pin_type == 'output':
                module.outputs.append(pin)

    else:                                                      # w/o  parametric size (=1)

        temp_name = re.sub("[;| |\t]", "", temp)
        # print(temp_name)

        for pin_name in temp_name.split(','):
            pin = Pin(pin_name, 1)
            
            if pin_type == 'input':
                module.inputs.append(pin)
            elif pin_type == 'output':
                module.outputs.append(pin)


with open(PATH, 'rt') as file:
    module = Module()

    lines = file.read().split('\n')

    for curr_line in lines:

        line = Line(curr_line)

        if line.is_comment():
            continue
        
        if line.is_name_section(top_module_name):
            module.append_name(top_module_name)
            continue

        if module.name:

            if 'parameter' in line.content:
                read_section_params(line.content)

            if ('input' in line.content or 'output' in line.content):
                read_section_pins(line.content)

            if 'endmodule' == line.content:
                break

module.print()