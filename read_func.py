from class_module import *
from class_line import *


def read_section_name(line):  # ? delete??
    temp = line.content
    if temp.find('(') != -1:  # '(' exist
        name = temp[temp.find('module') + len('module') + 1:temp.find('(')]
    else:  # '(' don't exist
        name = temp[temp.find('module') + len('module') + 1:]

    return name


def read_section_params(line, param_list):
    param = Param()

    if '//' in line.content:
        temp = line.content[:line.content.find('//')]
    else:
        temp = line.content

    temp = temp.replace('parameter', '')
    temp = re.sub("[;| |\t|,]", "", temp)
    
    temp_name, temp_size = temp.split('=')

    # * parametric size of parameter
    if not temp_size.isdigit():
        temp_value = temp_size

        if '<<' in temp_value:
            val_left, val_right = temp_value.split('<<')

            if not val_left.isdigit():
                for par in param_list:
                    if val_left == par.name:
                        val_left = par.value

            if not val_right.isdigit():
                for par in param_list:
                    if val_right == par.name:
                        val_right = par.value

            temp_size = int(val_left) << int(val_right)

        elif '>>' in temp_value:
            val_left, val_right = temp_value.split('>>')

            if not val_left.isdigit():
                for par in param_list:
                    if val_left == par.name:
                        val_left = par.value

            if not val_right.isdigit():
                for par in param_list:
                    if val_right == par.name:
                        val_right = par.value

            temp_size = int(val_left) >> int(val_right)

        elif '+' in temp_value:
            val_left, val_right = temp_value.split('+')

            if not val_left.isdigit():
                for par in param_list:
                    if val_left == par.name:
                        val_left = par.value

            if not val_right.isdigit():
                for par in param_list:
                    if val_right == par.name:
                        val_right = par.value

            temp_size = int(val_left) + int(val_right)

        elif '-' in temp_value:
            val_left, val_right = temp_value.split('-')

            if not val_left.isdigit():
                for par in param_list:
                    if val_left == par.name:
                        val_left = par.value

            if not val_right.isdigit():
                for par in param_list:
                    if val_right == par.name:
                        val_right = par.value

            temp_size = int(val_left) - int(val_right)

        elif '*' in temp_value:
            val_left, val_right = temp_value.split('*')

            if not val_left.isdigit():
                for par in param_list:
                    if val_left == par.name:
                        val_left = par.value

            if not val_right.isdigit():
                for par in param_list:
                    if val_right == par.name:
                        val_right = par.value

            temp_size = int(val_left) * int(val_right)

        elif '/' in temp_value:
            val_left, val_right = temp_value.split('/')

            if not val_left.isdigit():
                for par in param_list:
                    if val_left == par.name:
                        val_left = par.value

            if not val_right.isdigit():
                for par in param_list:
                    if val_right == par.name:
                        val_right = par.value

            temp_size = int(val_left) / int(val_right)

        else:
            param.name = '! unsupported expr'
            param.value = 0
            return param
            
    
    param.name =  temp_name
    param.value = int(temp_size)

    return param


def read_section_pins(line, param_list):
    pin_arr = []
    pin_direction = ''
    k = 1

    if '//' in line.content:
        temp = line.content[:line.content.find('//')].strip()
    else:
        temp = line.content.strip()

    temp_direction_name = re.sub(r'\[[^()]*\]', '', temp) # substracting size

    pin_direction = temp_direction_name[:temp_direction_name.find(' ')] # input | output | inout

    pin_size = temp[temp.find('['):temp.find(']') + 1] # [...]

    temp_name = temp_direction_name.replace(pin_direction, '')
    temp_name = re.sub("[;| |\t]", "", temp_name) # name1,name2,..
    temp_name_arr = temp_name.split(',')
    temp_name_arr = list(filter(None, temp_name_arr))  # deleting '' names
    # print('temp_name_arr:', temp_name_arr) # names array

    if not (pin_direction == 'input' or pin_direction == 'output' or pin_direction == 'inout'):
        print('fatal: wrong type of pin %s' %temp_name)
        exit()

    temp = temp.replace(pin_direction, '').replace('reg', '')  # ? ignore   'reg'?
    temp = temp.replace(pin_direction, '').replace('wire', '')  # ? ignore  'wire'?
    temp = temp.replace(pin_direction, '').replace('logic', '')  # ? ignore 'logic'?
    # print(pin_direction, end=' ')

    # * parametric size
    if pin_size:

        pin_size = re.sub("[\[|\]| |\t]", "", pin_size)  # deleting [] and whitespaces
        temp_size_arr = pin_size.split(':')
        start_val, end_val = temp_size_arr
        # print('temp_size_arr:', temp_size_arr) # sizes array

        if not start_val.isdigit():  # if parameter in LEFT part

            if '-' in start_val:
                start_val = start_val.split('-')
                k = -1

            elif '+' in start_val:
                start_val = start_val.split('+')
                k = 1

            start_val_left, start_val_right = start_val

            if not start_val_left.isdigit():  # parameter in left subpart
                for param in param_list:
                    if param.name == start_val_left:
                        start_val_left = param.value

            if not start_val_right.isdigit():  # parameter in right subpart
                for param in param_list:
                    if param.name == start_val_right:
                        start_val_right = param.value

            start_val = int(start_val_left) + int(start_val_right) * k

        if not end_val.isdigit():  # if parameter in RIGHT part

            if '-' in end_val:
                end_val = end_val.split('-')
                k = -1

            elif '+' in end_val:
                end_val = end_val.split('+')
                k = 1

            end_val_left, end_val_right = end_val

            if not end_val_left.isdigit():  # parameter in left subpart
                for param in param_list:
                    if param.name == end_val_left:
                        end_val_left = param.value

            if not end_val_right.isdigit():  # parameter in right subpart
                for param in param_list:
                    if param.name == end_val_right:
                        end_val_right = param.value

            end_val = int(end_val_left) + int(end_val_right) * k

        pin_true_size = abs(int(end_val) - int(start_val)) + 1

    # * simple size (=1)
    else:
        pin_true_size = 1

    for pin_name in temp_name_arr:
        pin = Pin(pin_name, pin_direction, pin_true_size)
        pin_arr.append(pin)

    return pin_arr


def get_module_name(lines):
    names = []
    module_list = []
    module_name = ''
    attachments_list = []

    # getting list of module names
    for line in lines:
        if 'module ' in line:
            if line.find('(') != -1:
                name = line[line.find('module') + len('module') + 1:line.find('(')]
            else:
                name = line[line.find('module') + len('module') + 1:]
            names.append(name)
    if not names:
        return


    # for each module in file
    for module_name in names:
        module_lines = []
        is_module_section = False
        module = Module(module_name)

        # getting module text -> module_lines
        for line in lines:
            if 'module ' + module.name in line and not is_module_section:  # found start point of section
                is_module_section = True
                continue
            elif is_module_section and 'endmodule' in line:  # found end point of section
                is_module_section = False
                continue
            elif is_module_section:
                if '//' in line:
                    line = line[:line.find('//')]
                line = re.sub("[\t]", "", line)
                line = line.replace('  ', '')
                module_lines.append(line)

        # getting list of attachments (searching another modules in module_lines)
        for att in names:
            for line in module_lines:
                if att in line and att != module.name and att not in attachments_list:
                    # print(line)
                    attachments_list.append(att)

        # adding modules with name only to list 
        module_list.append(module)

    # entering info if module is callable (is it in attachment list?)
    for mod in module_list:
        for att in attachments_list:
            if mod.name == att:
                mod.called = True


    # choosing top module as not callable module (first in file (?))
    for mod in module_list:
        if not mod.called:
            module_name = mod.name
            break

    return module_name
