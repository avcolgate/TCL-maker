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
# unknown mathematical operation  in parameter size
# unknown subparameter in parameter size
# negative value of parameter
# float value of parameter
# difficult expression in parameter size
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
            check = False

            if not is_number(val_left):
                for par in param_list:
                    if val_left == par.name:
                        val_left = par.value
                        check = True
                        break
            elif not is_number(val_right):
                for par in param_list:
                    if val_right == par.name:
                        val_right = par.value
                        check = True
                        break
            else:
                check = True

            if not check:
                print("fatal: unknown parameter in size of parameter '%s', line %i" % (temp_name, line_num + 1))
                exit()

            if str(val_left).isdigit() and str(val_right).isdigit():
                temp_size = int(val_left) << int(val_right)
            else:
                print("fatal: arguments in '<<' operation must be positive integer. Parameter '%s', line %i" % (temp_name, line_num + 1))
                exit()

        elif '>>' in temp_expr:
            val_left, val_right = temp_expr.split('>>')
            check = False

            if not is_number(val_left):
                for par in param_list:
                    if val_left == par.name:
                        val_left = par.value
                        check = True
                        break
            elif not is_number(val_right):
                for par in param_list:
                    if val_right == par.name:
                        val_right = par.value
                        check = True
                        break
            else:
                check = True

            if not check:
                print("fatal: unknown parameter in size of parameter '%s', line %i" % (temp_name, line_num + 1))
                exit()

            if str(val_left).isdigit() and str(val_right).isdigit():
                temp_size = int(val_left) >> int(val_right)
            else:
                print("fatal: arguments in '>>' operation must be positive integer. Parameter '%s', line %i" % (temp_name, line_num + 1))
                exit()
            
        elif '+' in temp_expr:
            val_left, val_right = temp_expr.split('+')
            check = False

            if not is_number(val_left):
                for par in param_list:
                    if val_left == par.name:
                        val_left = par.value
                        check = True
                        break
            elif not is_number(val_right):
                for par in param_list:
                    if val_right == par.name:
                        val_right = par.value
                        check = True
                        break
            else:
                check = True

            if not check:
                print("fatal: unknown parameter in size of parameter '%s', line %i" % (temp_name, line_num + 1))
                exit()

            if str(val_left).isdigit() and str(val_right).isdigit():
                temp_size = int(val_left) + int(val_right)
            else:
                print("fatal: arguments in '+' must be positive integer. Parameter '%s', line %i" % (temp_name, line_num + 1))
                exit()    

        elif '-' in temp_expr:
            val_left, val_right = temp_expr.split('-')

            check = False

            if not is_number(val_left):
                for par in param_list:
                    if val_left == par.name:
                        val_left = par.value
                        check = True
                        break
            elif not is_number(val_right):
                for par in param_list:
                    if val_right == par.name:
                        val_right = par.value
                        check = True
                        break
            else:
                check = True

            if not check:
                print("fatal: unknown parameter in size of parameter '%s', line %i" % (temp_name, line_num + 1))
                exit()

            if str(val_left).isdigit() and str(val_right).isdigit():
                temp_size = int(val_left) - int(val_right)
            else:
                print("fatal: arguments in '-' must be positive integer. Parameter '%s', line %i" % (temp_name, line_num + 1))
                exit()

        elif '*' in temp_expr:
            val_left, val_right = temp_expr.split('*')
            check = False

            if not is_number(val_left):
                for par in param_list:
                    if val_left == par.name:
                        val_left = par.value
                        check = True
                        break
            elif not is_number(val_right):
                for par in param_list:
                    if val_right == par.name:
                        val_right = par.value
                        check = True
                        break
            else:
                check = True

            if not check:
                print("fatal: unknown parameter in size of parameter '%s', line %i" % (temp_name, line_num + 1))
                exit()

            if str(val_left).isdigit() and str(val_right).isdigit():
                temp_size = int(val_left) * int(val_right)
            else:
                print("fatal: arguments in '*' must be positive integer. Parameter '%s', line %i" % (temp_name, line_num + 1))
                exit()

        elif '/' in temp_expr:
            val_left, val_right = temp_expr.split('/')
            check = False

            if not is_number(val_left):
                for par in param_list:
                    if val_left == par.name:
                        val_left = par.value
                        check = True
                        break
            elif not is_number(val_right):
                for par in param_list:
                    if val_right == par.name:
                        val_right = par.value
                        check = True
                        break
            else:
                check = True

            if not check:
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
    
    # * simple size of parameter
    else:
        temp_size = temp_expr

    if not str(temp_size).isdigit() or int(temp_size) <= 0:
        print("fatal: parameter '%s' must be positive integer, line %i" % (temp_name, line_num + 1))
        exit()
    
    param.name =  temp_name
    param.value = int(temp_size)

    return param

# * fatals:
# wrong type of pin
def read_section_pins(line, param_list):
    pin_arr = []
    pin_direction = ''
    k = 1

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


#* fatals:
# no modules in file
# duplicate name of module
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
