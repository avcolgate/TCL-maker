from class_module import *
from class_line import *
from func import *


def read_section_name(line):  # ? delete??
    temp = line.content
    if temp.find('(') != -1:  # '(' exist
        name = temp[temp.find('module') + len('module') + 1:temp.find('(')]
    else:  # '(' don't exist
        name = temp[temp.find('module') + len('module') + 1:]

    return name


# * fatals: 
# duplicate name
# unknown mathematical operation in parameter size
# unknown subparameter in parameter size
# negative values in parameter size
# float values in parameter size
# difficult expression in parameter size
# too large parameter size
# too large argument in '<<' operation
def read_section_params(line, param_list, line_num):
    param = Param()

    temp = line.content
    temp = temp.replace('parameter', '')
    temp = re.sub("[;| |\t|,]", "", temp)
    
    temp_name, temp_expr = temp.split('=')

    for par in param_list:
        if par.name == temp_name:
            print("fatal: duplicate parameter '%s', line %i" % (temp_name, line_num + 1))
            exit()

    # * parametric size of parameter
    if not is_number(temp_expr):

        if '<<' in temp_expr:
            val_left, val_right = temp_expr.split('<<')
            check = 0

            if not is_number(val_left):
                for par in param_list:
                    if val_left == par.name:
                        val_left = par.value
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
            else:
                check += 1

            # check if every parameter is a number now
            if check < 2:
                print("fatal: unknown parameter in size of parameter '%s', line %i" % (temp_name, line_num + 1))
                exit()

            if str(val_left).isdigit() and str(val_right).isdigit():
                if int(val_right) > 20:
                    print("fatal: the argument is too large. Parameter '%s', line %i" % (temp_name, line_num + 1))
                    exit()
                else:
                    temp_size = int(val_left) << int(val_right)
            else:
                print("fatal: arguments in '<<' operation must be positive integer. Parameter '%s', line %i" % (temp_name, line_num + 1))
                exit()

        elif '>>' in temp_expr:
            val_left, val_right = temp_expr.split('>>')
            check = 0

            if not is_number(val_left):
                for par in param_list:
                    if val_left == par.name:
                        val_left = par.value
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
            else:
                check += 1

            if check < 2:
                print("fatal: unknown parameter in size of parameter '%s', line %i" % (temp_name, line_num + 1))
                exit()

            if str(val_left).isdigit() and str(val_right).isdigit():
                temp_size = int(val_left) >> int(val_right)
            else:
                print("fatal: arguments in '>>' operation must be positive integer. Parameter '%s', line %i" % (temp_name, line_num + 1))
                exit()
            
        elif '+' in temp_expr:
            val_left, val_right = temp_expr.split('+')
            check = 0

            if not is_number(val_left):
                for par in param_list:
                    if val_left == par.name:
                        val_left = par.value
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
            else:
                check += 1

            if check < 2:
                print("fatal: unknown parameter in size of parameter '%s', line %i" % (temp_name, line_num + 1))
                exit()

            if str(val_left).isdigit() and str(val_right).isdigit():
                temp_size = int(val_left) + int(val_right)
            else:
                print("fatal: arguments in '+' must be positive integer. Parameter '%s', line %i" % (temp_name, line_num + 1))
                exit()    

        elif '-' in temp_expr:
            val_left, val_right = temp_expr.split('-')
            check = 0

            if not is_number(val_left):
                for par in param_list:
                    if val_left == par.name:
                        val_left = par.value
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
            else:
                check += 1

            if check < 2:
                print("fatal: unknown parameter in size of parameter '%s', line %i" % (temp_name, line_num + 1))
                exit()

            if str(val_left).isdigit() and str(val_right).isdigit():
                temp_size = int(val_left) - int(val_right)
            else:
                print("fatal: arguments in '-' must be positive integer. Parameter '%s', line %i" % (temp_name, line_num + 1))
                exit()

        elif '*' in temp_expr:
            val_left, val_right = temp_expr.split('*')
            check = 0

            if not is_number(val_left):
                for par in param_list:
                    if val_left == par.name:
                        val_left = par.value
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
            else:
                check += 1

            if check < 2:
                print("fatal: unknown parameter in size of parameter '%s', line %i" % (temp_name, line_num + 1))
                exit()

            if str(val_left).isdigit() and str(val_right).isdigit():
                temp_size = int(val_left) * int(val_right)
            else:
                print("fatal: arguments in '*' must be positive integer. Parameter '%s', line %i" % (temp_name, line_num + 1))
                exit()

        elif '/' in temp_expr:
            val_left, val_right = temp_expr.split('/')
            check = 0

            if not is_number(val_left):
                for par in param_list:
                    if val_left == par.name:
                        val_left = par.value
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
            else:
                check += 1

            if check < 2:
                print("fatal: unknown parameter in size of parameter '%s', line %i" % (temp_name, line_num + 1))
                exit()

            if str(val_left).isdigit() and str(val_right).isdigit():
                if int(val_left) % int(val_right) == 0:
                    temp_size = int(int(val_left) / int(val_right))
                else:
                    print("fatal: parameter '%s' must be positive integer, line %i" % (temp_name, line_num + 1))
                    exit()
            else:
                print("fatal: unknown expression in size of parameter '%s', line %i" % (temp_name, line_num + 1))
                exit()

        else:
            print('fatal: unknown expression in parameter value %s, line %i' % (temp_name, line_num + 1))
            exit()
    
    # * simple parameter size
    else:
        temp_size = temp_expr

    if str(temp_size).isdigit() and int(temp_size) > 0 and int(temp_size) < 100000:
        param.name =  temp_name
        param.value = int(temp_size)
    else:
        print("fatal: parameter '%s' must be positive integer and less than 100000, line %i" % (temp_name, line_num + 1))
        exit()
    
    return param


# * fatals:
# duplicate name
# unknown parameter in pin size
# negative pin size
# negitive pin size values
# unknown expression in pin size values (not +/-) => unknown parameter
# float pin size
# * warnings:
# equal limits in pin size
def read_section_pins(line, param_list, pin_list, line_num):
    pin_arr = []
    pin_direction = 'NaN'
    k = 1

    temp = line.content.strip()

    temp_direction_name = re.sub(r'\[[^()]*\]', '', temp) # substracting size

    pin_direction = temp_direction_name[:temp_direction_name.find(' ')] # input | output | inout

    pin_size = temp[temp.find('['):temp.find(']') + 1] # [...]

    temp_name = temp_direction_name.replace(pin_direction, '')
    temp_name = temp_name.replace('reg', '').replace('wire', '') #? also delete SystemVerilog's 'logic'?
    temp_name = re.sub("[;| |\t]", "", temp_name) # name1,name2,..
    temp_name_arr = temp_name.split(',')
    temp_name_arr = list(filter(None, temp_name_arr))  # deleting '' names
    # print('temp_name_arr:', temp_name_arr) # names array

    for pin in pin_list:
        for name in temp_name_arr:
            if pin.name == name:
                print("fatal: duplicate pin name '%s', line %i" % (name, line_num + 1))
                exit()    

    # * parametric size
    if pin_size:

        pin_size = re.sub("[\[|\]| |\t]", "", pin_size)  # deleting [] and whitespaces
        temp_size_arr = pin_size.split(':')
        start_val, end_val = temp_size_arr
        # print('temp_size_arr:', temp_size_arr) # sizes array

        if not is_number(start_val):  # if parameter in LEFT part

            if '-' in start_val:
                start_val = start_val.split('-')
                start_val_left, start_val_right = start_val
                k = -1
            elif '+' in start_val:
                start_val = start_val.split('+')
                start_val_left, start_val_right = start_val
                k = 1
            else:
                start_val_left = start_val
                start_val_right = 0
                k = 1

            check = 0

            if not is_number(start_val_left):  # parameter in left subpart
                for param in param_list:
                    if param.name == start_val_left:
                        start_val_left = param.value
                        check += 1
                        break
            else:
                check += 1

            if not is_number(start_val_right):  # parameter in right subpart
                for param in param_list:
                    if param.name == start_val_right:
                        start_val_right = param.value
                        check += 1
                        break
            else:
                check += 1

            if check < 2:
                print("fatal: unknown parameter in pin size, line %i" % (line_num + 1))
                exit()
            
            if str(start_val_left).isdigit() and str(start_val_right).isdigit():
                start_val = int(start_val_left) + k * int(start_val_right) 
                if start_val < 0:
                    print("fatal: arguments in size must be !positive integer. Pin '%s', line %i" % (temp_name, line_num + 1))
                    exit()
            else:
                print("fatal: arguments in size must be positive !integer. Pin '%s', line %i" % (temp_name, line_num + 1))
                exit()

        if not is_number(end_val):  # if parameter in RIGHT part

            if '-' in end_val:
                end_val = end_val.split('-')
                end_val_left, end_val_right = end_val
                k = -1
            elif '+' in end_val:
                end_val = end_val.split('+')
                end_val_left, end_val_right = end_val
                k = 1
            else:
                end_val_left = end_val
                end_val_right = 0
                k = 1

            check = 0

            if not is_number(end_val_left):  # parameter in left subpart
                for param in param_list:
                    if param.name == end_val_left:
                        end_val_left = param.value
                        check += 1
                        break
            else:
                check += 1

            if not is_number(end_val_right):  # parameter in right subpart
                for param in param_list:
                    if param.name == end_val_right:
                        end_val_right = param.value
                        check += 1
                        break
            else:
                check += 1

            if check < 2:
                print("fatal: unknown parameter in pin size, line %i" % (line_num + 1))
                exit()

            if str(start_val_left).isdigit() and str(start_val_right).isdigit():
                end_val = int(end_val_left) + k * int(end_val_right)
                if end_val < 0:
                    print("fatal: arguments in size must be !positive integer. Pin '%s', line %i" % (temp_name, line_num + 1))
                    exit()
            else:
                print("fatal: arguments in size must be positive !integer. Pin '%s', line %i" % (temp_name, line_num + 1))
                exit()

        if start_val == end_val:
            print("warning: equal limits in the pin size. Pin '%s', line %i" % (temp_name, line_num + 1))

        pin_true_size = int(start_val) - int(end_val) + 1

        if pin_true_size < 1:
            print("fatal: pin size must be positive integer. Pin '%s', line %i" % (temp_name, line_num + 1))
            exit()

    # * simple size (=1)
    else:
        pin_true_size = 1

    for pin_name in temp_name_arr:
        pin = Pin(pin_name, pin_direction, pin_true_size)
        pin_arr.append(pin)

    return pin_arr


#* fatals:
# no modules in file
# duplicate module name
# two or more modules modules have the maximum number of attachments
#
#* warning:
# two or more non-callable modules. Top module will be chosen as module with the most attachments
def get_module_name(lines):
    names = []
    module_list = []
    top_module_name = ''
    attachments_list = []
    # getting list of module names
    for line_num, line in enumerate(lines):
        line = line.strip()

        if 'module ' in line or 'macromodule ' in line:
            if line.find('(') != -1:
                name = line[line.find(' ') + 1:line.find('(')]
            else:
                name = line[line.find(' ') + 1:]

            if name in names:
                print('fatal: duplicate module name %s, line %i' % (name, line_num + 1))
                exit()

            names.append(name)

    if not names:
        print('fatal: no modules in file')
        exit()
    

    # for each module in file
    for module_name in names:
        module_lines = []
        is_module_section = False
        module_fs = Module_for_search(module_name)

        # getting module text -> module_lines
        for line in lines:
            #   vvvv includes 'macromodule'
            if 'module ' + module_fs.name in line and not is_module_section:  # found start point of section
                is_module_section = True
                continue
            elif is_module_section and 'endmodule' in line:  # found end point of section
                is_module_section = False
                continue
            elif is_module_section:
                line = re.sub("[\t]", "", line)
                line = line.replace('  ', '')
                module_lines.append(line)

        # getting list of attachments (searching another modules in module_lines)
        for att in names:
            for line in module_lines:
                if att in line and att != module_fs.name and att not in module_fs.attachments:
                    # print(line)
                    attachments_list.append(att)
                    module_fs.attachments.append(att)
                    module_fs.count_att += 1

        # adding modules with name only to list 
        module_list.append(module_fs)

    # getting info if module is callable (is it in attachment list?)
    for mod in module_list:
        for att in attachments_list:
            if mod.name == att:
                mod.called = True
    
    max_att = -1
    count_non_callable = 0
    for mod in module_list:
        if not mod.called:
            count_non_callable += 1
            # print(mod.name)
        if not mod.called and len(mod.attachments) > max_att:
            max_att = len(mod.attachments)

    if count_non_callable > 1:
        print('warning: there are two or more non-callable modules. Top module will be chosen as module with the most attachments')

    count_top = 0
    # choosing top module as non-callable module
    for mod in module_list:
        if not mod.called and len(mod.attachments) == max_att:
            top_module_name = mod.name
            count_top += 1

    if count_top > 1:
        print('fatal: there are two or more non-callable modules modules have the maximum number of attachments')
        exit()

    return top_module_name
