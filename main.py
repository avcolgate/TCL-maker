import re
from module_class import *

marks = ';,[]='
PATH = './src/spm.v'
top_module = 'spm'
got_name = False
print('')

def read_section_name(curr_line):
    if 'module ' + top_module in curr_line:
        module.name = top_module
        return True
    else:
        return False
    
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
                    for i in module.params:
                        if i.name == start_val_left:
                            start_val_left = i.value

                if not start_val_right.isdigit():                 # parameter in right subpart
                    for i in module.params:
                        if i.name == start_val_right:
                            start_val_right = i.value

                start_val = int(start_val_left) - int(start_val_right)

            elif '+' in start_val:                    # add (???)
                start_val = start_val.split('+')
                start_val_left, start_val_right = start_val

                if not start_val_left.isdigit():                  # parameter in left subpart
                    for i in module.params:
                        if i.name == start_val_left:
                            start_val_left = i.value

                if not start_val_right.isdigit():                 # parameter in right subpart
                    for i in module.params:
                        if i.name == start_val_right:
                            start_val_right = i.value

                start_val = int(start_val_left) + int(start_val_right)


        if not end_val.isdigit():                               # if parameter in RIGHT part

            if '-' in end_val:                      # substract
                end_val = end_val.split('-')
                end_val_left, end_val_right = end_val

                if not end_val_left.isdigit():                  # parameter in left subpart
                    for i in module.params:
                        if i.name == end_val_left:
                            end_val_left = i.value

                if not end_val_right.isdigit():                 # parameter in right subpart
                    for i in module.params:
                        if i.name == end_val_right:
                            end_val_right = i.value

                end_val = int(end_val_left) - int(end_val_right)
                
            elif '+' in end_val:                    # add (???)
                end_val = end_val.split('+')
                end_val_left, end_val_right = end_val

                if not end_val_left.isdigit():                  # parameter in left subpart
                    for i in module.params:
                        if i.name == end_val_left:
                            end_val_left = i.value

                if not end_val_right.isdigit():                 # parameter in right subpart
                    for i in module.params:
                        if i.name == end_val_right:
                            end_val_right = i.value

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
    text = file.read()

    lines=text.split('\n')

    # print(lines)

    for curr_line in lines:

        if curr_line.replace(' ', '').find('//') == 0:
            continue
        
        if read_section_name(curr_line):
            got_name = True
            continue

        if got_name:

            if 'parameter' in curr_line:
                read_section_params(curr_line)

            if ('input' in curr_line or 'output' in curr_line):
                read_section_pins(curr_line)

            if 'endmodule' == curr_line:
                break


print('# Name')
print(module.name)

if len(module.params):
    print('# Parameters')
for i in module.params:
    print('%s: %i' % (i.name, i.value))

if len(module.inputs):
    print('# Inputs')
for i in module.inputs:
    print('%4s: %2i (%s)' % (i.name, i.size, i.type))

if len(module.outputs):
    print('# Outputs')
for i in module.outputs:
    print('%4s: %2i (%s)' % (i.name, i.size, i.type))