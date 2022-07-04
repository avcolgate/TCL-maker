import re
from module_class import *

marks = ';,=[]'
PATH = './src/spm.v'
top_module = 'spm'
got_name = False
# lines = []
print('')

def read_section_name(curr_line):
    if 'module ' + top_module in curr_line:
        module.name = top_module
        # print('Created module: ' + module.name)
        return True
    else:
        return False
    
def read_section_params(curr_line):
    # print (curr_line)
    temp = curr_line

    temp = temp.replace('parameter', '')

    for x in temp:
        if x in marks:
            temp = temp.replace(x, '')

    temp = temp.split()
    # print(temp)

    module.param_name.append(temp[0])
    module.param_value.append(int(temp[1]))  

def read_section_pins(curr_line):
    temp = curr_line

    if 'input' in temp:      # type detection
        pin_type = 'input'
    elif 'output' in temp:
        pin_type = 'output'

    temp = temp.replace(pin_type, '')
    print('pin_type=', pin_type)

    if ('[' in temp) or (']' in temp):                    # with parametric size







        

        pass
    else:                                                 # w/o  parametric size
        for x in temp:
            if x in marks:
                temp = temp.replace(x, '')

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

            # if 'parameter' in curr_line:
            #     read_section_params(curr_line)

            if ('input' in curr_line or 'output' in curr_line):
                read_section_pins(curr_line)

            if 'endmodule' == curr_line:
                print('\nEOF found\n')
                break

            
        # if got_name and 'parameter' in curr_line:
        #     # print(curr_line)
        #     read_section_params(curr_line)
        #     if not 'parameter' in curr_line:
        #         continue

        # if got_name and ('input' in curr_line or 'output' in curr_line):
        #     read_section_pins(curr_line)
        #     if not ('input' in curr_line or 'output' in curr_line):
        #             continue

        # if got_name and curr_line == 'endmodule':
        #     print('\nEOF found\n')
        #     break

        # if 'module ' + module_name in curr_line:
        #     print (curr_line)
        #     module  = Module(module_name)
        #     print('Created module: ' + module.name)

##########################################################################


        # if 'input'in curr_line:
        #     #print (curr_line)
        #     temp = curr_line.split()[1:]       # removing 'input'
        #     for i in temp:
        #         i = re.sub("[;|,]", "", i)
        #         print(i)


            


        # if 'output'in curr_line:
        #     #print (curr_line)
        #     temp = curr_line.split()
        #     #print(temp[1:])

        # if curr_line == 'endmodule':
        #     break


# module = Module('mod1')
# tempPin = Pin('input', 'clk')
#print(tempPin.__dict__)
#module.pins.append(tempPin)

#print(module.pins[0].type)

print('\n')
print('Created module: ' + module.name)
print('param_name: ', module.param_name)
print('param_size: ', module.param_value, end='\n\n')

print('module.inputs.name:', module.input_name)
print('module.inputs.size:', module.input_size, end='\n\n')

print('module.inputs.name:', module.output_name)
print('module.inputs.size:', module.output_size, end='\n\n')