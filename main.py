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
    temp=re.sub("[;| ]","", temp)

    temp_name, temp_size = temp.split('=')

    module.param_name.append(temp_name)
    module.param_value.append(int(temp_size))  

def read_section_pins(curr_line):
    temp = curr_line

    if 'input' in temp:      # type detection
        pin_type = 'input'
    elif 'output' in temp:
        pin_type = 'output'
    temp = temp.replace(pin_type, '').replace('reg', '')
    print(pin_type, end=' ')

    temp_size = temp[temp.find('['):temp.find(']')+1]

    # print('temp_size =' + temp_size + '///')

    if (temp_size):                                                   # with parametric size

        temp_name = temp[temp.find(']')+1:]       # copying names only
        temp_name=re.sub("[;| ]","", temp_name)
        temp_name_arr = temp_name.split(',')
        # print('temp_name_arr:', temp_name_arr) # names array

        temp_size = re.sub("[\[|\]| ]","", temp_size) # deleting [] and whitespaces
        temp_size_arr = temp_size.split(':')
        start_val, end_val = temp_size_arr
        # print('temp_size_arr:', temp_size_arr)     # sizes array
        print(temp_name)

        if not start_val.isdigit():                             # parameter in LEFT part

            if '-' in start_val:                      # substract
                start_val = start_val.split('-')
                start_val_left, start_val_right = start_val

                if not start_val_left.isdigit():                  # parameter in left subpart
                    val_ind = module.param_name.index(start_val_left)
                    start_val_left = module.param_value[val_ind]

                if not start_val_right.isdigit():                 # parameter in right subpart
                    val_ind = module.param_name.index(start_val_right)
                    start_val_right = module.param_value[val_ind]

                start_val = int(start_val_left) - int(start_val_right)
                # print('(-) start_val = ', start_val)

            elif '+' in start_val:                    # add (???)
                start_val = start_val.split('+')
                start_val_left, start_val_right = start_val

                if not start_val_left.isdigit():                  # parameter in left subpart
                    val_ind = module.param_name.index(start_val_left)
                    start_val_left = module.param_value[val_ind]

                if not start_val_right.isdigit():                 # parameter in right subpart
                    val_ind = module.param_name.index(start_val_right)
                    start_val_right = module.param_value[val_ind]

                start_val = int(start_val_left) + int(start_val_right)
                # print('(+) start_val = ', start_val)


        if not end_val.isdigit():                               # parameter in RIGHT part

            if '-' in end_val:                      # substract
                end_val = end_val.split('-')
                end_val_left, end_val_right = end_val

                if not end_val_left.isdigit():                  # parameter in left subpart
                    val_ind = module.param_name.index(end_val_left)
                    end_val_left = module.param_value[val_ind]

                if not end_val_right.isdigit():                 # parameter in right subpart
                    val_ind = module.param_name.index(end_val_right)
                    end_val_right = module.param_value[val_ind]

                end_val = int(end_val_left) - int(end_val_right)
                # print('(-) end_val = ', end_val)

            elif '+' in end_val:                    # add (???)
                end_val = end_val.split('+')
                end_val_left, end_val_right = end_val

                if not end_val_left.isdigit():                  # parameter in left subpart
                    val_ind = module.param_name.index(end_val_left)
                    end_val_left = module.param_value[val_ind]

                if not end_val_right.isdigit():                 # parameter in right subpart
                    val_ind = module.param_name.index(end_val_right)
                    end_val_right = module.param_value[val_ind]

                end_val = int(end_val_left) + int(end_val_right)
                # print('(+) end_val = ', end_val)


        delta_val = abs(int(end_val) - int(start_val)) + 1
        # print('delta_val = ', delta_val)

        for pin in temp_name_arr:
            module.input_name.append(pin)
            module.input_size.append(delta_val)

    else:                                                                                # w/o  parametric size (=1)

        temp_name = re.sub("[;| ]", "", temp)
        print(temp_name)

        for i in temp_name.split(','):
            if pin_type == 'input':
                module.input_name.append(i)
                module.input_size.append(1)
            elif pin_type == 'output':
                module.output_name.append(i)
                module.output_size.append(1)


with open(PATH, 'rt') as file:
    module = Module()
    text = file.read()

    lines=text.split('\n')

    # print(lines)

    for curr_line in lines:

        if curr_line.replace(' ', '').find('//') == 0:
            # print(curr_line + 'ignored')
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
                print('\nEOF\n')
                break


print('Created module: ' + module.name)
print('param_name: ', module.param_name)
print('param_value: ', module.param_value, end='\n\n')

print('Inputs.name:', module.input_name)
print('Inputs.size:', module.input_size, end='\n\n')

print('Outputs.name:', module.output_name)
print('Outputs.size:', module.output_size, end='\n\n')

print(module)