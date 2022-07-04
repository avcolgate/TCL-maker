from calendar import c
import re
from operator import mod
from module_class import *

PATH = './src/spm.v'
top_module = 'TCMP'
got_name = False
# lines = []

def read_section_name(curr_line):
    if 'module ' + top_module in curr_line:
        module.name = top_module
        # print('Created module: ' + module.name)
        return True
    else:
        return False
    
    
def read_section_params(curr_line):
    if 'parameter' in curr_line:
        # print (curr_line)
        temp_name = curr_line.split()[1:2]         # picking <name>
        temp_name = temp_name[0]
        module.param_name.append(temp_name)
        # print('param_name: ', module.param_name)

        temp_size = curr_line.split()[-1:]         # last word
        temp_size = temp_size[0][:-1]              # removing ';'
        module.param_size.append(int(temp_size))        
        # print('param_size: ', module.param_size)

def read_section_pins(curr_line):
    print('pin line')


with open(PATH, 'rt') as file:
    module = Module()
    text = file.read()

    lines=text.split('\n')

    # print(lines)

    for curr_line in lines:
        
        if read_section_name(curr_line):
            got_name = True
            continue
            
        if got_name and 'parameter' in curr_line:
            # print(curr_line)
            read_section_params(curr_line)
            if not 'parameter' in curr_line:
                continue

        if got_name and ('input' in curr_line or 'output' in curr_line):
            read_section_pins(curr_line)
            if not ('input' in curr_line or 'output' in curr_line):
                    continue

        if got_name and curr_line == 'endmodule':
            print('\nEOF found\n')
            break

        # if 'module ' + module_name in curr_line:
        #     print (curr_line)
        #     module  = Module(module_name)
        #     print('Created module: ' + module.name)

##################################################################################


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

print('\n\n\n')
print('Created module: ' + module.name)
print('param_name: ', module.param_name)
print('param_size: ', module.param_size)