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
    print(pin_type)

    new_temp_size = temp[temp.find('['):temp.find(']')+1]

    print('new_temp_size =' + new_temp_size + '///')


    if ('[' in temp) or (']' in temp):                                                   # with parametric size

        
        temp_name  = temp.split(']')[-1]                  # copying names only
        
        temp_name = temp_name.replace(';', '')
        temp_name = temp_name.replace(' ', '')

        temp_name = temp_name.split(',')
        # print('split temp_name:', temp_name) # names array

        
        temp_size = temp.split(']')[0].replace('[', '')   # copying sizes only
        temp_size = temp_size.replace(' ', '')

        temp_size = temp_size.split(':')

        start_val = temp_size[0]     # левая часть
        end_val   = temp_size[-1]    # правая часть
        
        print('start_val, end_val: ', start_val, end_val)



        if not start_val.isdigit():                             # если ЛЕВАЯ часть содержит параметр

            if '-' in start_val:                      # вычитание
                start_val = start_val.split('-')
                start_val_left = start_val[0]
                start_val_right = start_val[-1]

                if not start_val_left.isdigit():                  # если левое число через параметр
                    val_num = module.param_name.index(start_val_left)
                    start_val_left = module.param_value[val_num]

                if not start_val_right.isdigit():                 # если правое число через параметр
                    val_num = module.param_name.index(start_val_right)
                    start_val_right = module.param_value[val_num]

                start_val = abs(int(start_val_right) - int(start_val_left))
                print('(-) start_val = ', start_val)

            elif '+' in start_val:                    # сложение (???)
                start_val = start_val.split('+')
                start_val_left = start_val[0]
                start_val_right = start_val[-1]

                if not start_val_left.isdigit():                  # если левое число через параметр
                    val_num = module.param_name.index(start_val_left)
                    start_val_left = module.param_value[val_num]

                if not start_val_right.isdigit():                 # если правое число через параметр
                    val_num = module.param_name.index(start_val_right)
                    start_val_right = module.param_value[val_num]

                start_val = abs(int(start_val[-1]) + int(start_val[0]))
                print('(+) start_val = ', start_val)



        if not end_val.isdigit():                             # если ПРАВАЯ часть содержит параметр

            if '-' in end_val:                      # вычитание
                end_val = end_val.split('-')
                end_val_left = end_val[0]
                end_val_right = end_val[-1]

                if not end_val_left.isdigit():                  # если левое число через параметр
                    val_num = module.param_name.index(end_val_left)
                    end_val_left = module.param_value[val_num]

                if not end_val_right.isdigit():                 # если правое число через параметр
                    val_num = module.param_name.index(end_val_right)
                    end_val_right = module.param_value[val_num]

                end_val = abs(int(end_val_right) - int(end_val_left))
                print('(-) end_val = ', end_val)

            elif '+' in end_val:                    # сложение (???)
                end_val = end_val.split('+')
                end_val_left = end_val[0]
                end_val_right = end_val[-1]

                if not end_val_left.isdigit():                  # если левое число через параметр
                    val_num = module.param_name.index(end_val_left)
                    end_val_left = module.param_value[val_num]

                if not end_val_right.isdigit():                 # если правое число через параметр
                    val_num = module.param_name.index(end_val_right)
                    end_val_right = module.param_value[val_num]

                end_val = abs(int(end_val[-1]) + int(end_val[0]))
                print('(+) end = ', end_val)


        delta_val = abs(int(end_val) - int(start_val)) + 1
        print('delta_val = ', delta_val)

        for pin in temp_name:
            module.input_name.append(pin)
            module.input_size.append(delta_val)

       
    else:                                                                                # w/o  parametric size (=1)
        # for x in temp:
        #     if x in marks:                          # сделать !!! тест с пробелами
        #         temp = temp.replace(x, '')

        print(temp)

        for i in temp.split():
            if pin_type == 'input':
                module.input_name.append(i)
                module.input_size.append(1)
            elif pin_type == 'output':
                module.output_name.append(i)
                module.output_size.append(1)

    print(temp)


with open(PATH, 'rt') as file:
    module = Module()
    text = file.read()

    lines=text.split('\n')

    # print(lines)

    for curr_line in lines:
        
        if read_section_name(curr_line):
            got_name = True
            continue

        if got_name:

            if 'parameter' in curr_line:
                read_section_params(curr_line)

            if ('input' in curr_line or 'output' in curr_line):
                read_section_pins(curr_line)

            if 'endmodule' == curr_line:
                print('\nEOF found\n')
                break

# print('\n')
# print('Created module: ' + module.name)
# print('param_name: ', module.param_name)
# print('param_value: ', module.param_value, end='\n\n')

# print('Inputs.name:', module.input_name)
# print('Inputs.size:', module.input_size, end='\n\n')

# print('Outputs.name:', module.output_name)
# print('Outputs.size:', module.output_size, end='\n\n')

print(module)