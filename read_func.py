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
# bad name
# no value 
# bad values in define size (only unsigned integer < 100 000)
def append_defines(lines, module):

    for line_num, curr_line in enumerate(lines):
        line = Line(curr_line)
        line.erase_comment()

        if line.is_define_section():
            define = Define()
            temp = line.content.replace('\t', ' ')

            temp = temp.replace('`define', '').strip()

            if ' ' in temp:
                temp_name, temp_size = temp.split(' ')
            else:
               print("fatal: bad define, line %i\n" % (line_num + 1))
               exit()

            if str(temp_size).isdigit() and int(temp_size) > 0 and int(temp_size) < 100000:
                define.name = str(temp_name)
                define.value = int(temp_size)
            else:
                print("fatal: define '%s' must be positive integer, line %i\n" % (temp_name, line_num + 1))
                exit()

            for d in module.defines:
                if d.name == define.name:
                    print("fatal: duplicate define '%s', line %i\n" % (temp_name, line_num + 1))
                    exit()

            if not is_good_name(define.name):
                print("fatal: bad define name '%s', line %i\n" % (temp_name, line_num + 1))
                exit()

            module.append_defines(define)
            continue

        elif line.is_module_section():
            break


# * fatals: 
# duplicate name
# duplicate name in one string
# unknown mathematical operation in parameter size
# unknown subparameter in parameter size
# negative values in parameter size
# float values in parameter size
# difficult expression in parameter size
# too large parameter size
# too large argument in '<<' operation
def read_section_params(line, param_list, define_list, line_num):
    param_name = ''
    param_expr = ''
    param_value = 0
    param_arr = []
    temp_param_arr = []
    param_names_arr = []

    param = line.content.replace('parameter', '')
    param = re.sub("[;| |\t]", "", param)
    # print(param) # size=32,size2=32

    # several parameters in string
    if ',' in param:
        temp_param_arr = param.split(',')
        # print(temp_param_arr) # ['size=32', 'size2=32']

        # check for duplicate names in one string
        for par in temp_param_arr:
            if '=' in par:
                param_name, param_expr = par.split('=')
                if not param_name in param_names_arr:
                    param_names_arr.append(param_name)
                else:
                    print("fatal: duplicate parameter '%s', line %i\n" % (param_name, line_num + 1))
                    exit()
            else:
                print("fatal: bad parameter, line %i\n" % (line_num + 1))
                exit()
    # one parameter in string                    
    else:
        temp_param_arr.append(param)


    for param in temp_param_arr:
        parameter = Parameter()
    
        if '=' in param:
            param_name, param_expr = param.split('=')
        else:
            print("fatal: bad parameter '%s', line %i\n" % (param_name, line_num + 1))
            exit()

        for par in param_list:
            if par.name == param_name:
                print("fatal: duplicate parameter '%s', line %i\n" % (param_name, line_num + 1))
                exit()
                
        if not is_good_name(param_name):
            print("fatal: bad parameter name '%s', line %i\n" % (param_name, line_num + 1))
            exit()

        # * parametric size of parameter
        if not is_number(param_expr):

            # <digit>'<base> <number>
            if '\'' in param_expr:
                size_digit, size_val = param_expr.split('\'')
                size_val = str(size_val).lower()
                my_base = size_val[0]

                param_value = convert_number(size_val, my_base, param_name, line_num)

            elif '<<' in param_expr:
                val_left, val_right = param_expr.split('<<')

                val_left, val_right = define_expression(val_left, val_right, param_list, define_list, line_num)

                if str(val_left).isdigit() and str(val_right).isdigit():
                    if int(val_right) > 20:
                        print("fatal: the argument is too large. Parameter '%s', line %i\n" % (param_name, line_num + 1))
                        exit()
                    else:
                        param_value = int(val_left) << int(val_right)
                else:
                    print("fatal: arguments in '<<' operation must be positive integer. Parameter '%s', line %i\n" % (param_name, line_num + 1))
                    exit()

            elif '>>' in param_expr:
                val_left, val_right = param_expr.split('>>')
                
                val_left, val_right = define_expression(val_left, val_right, param_list, define_list, line_num)

                if str(val_left).isdigit() and str(val_right).isdigit():
                    param_value = int(val_left) >> int(val_right)
                else:
                    print("fatal: arguments in '>>' operation must be positive integer. Parameter '%s', line %i\n" % (param_name, line_num + 1))
                    exit()
                
            elif '+' in param_expr:
                val_left, val_right = param_expr.split('+')
                
                val_left, val_right = define_expression(val_left, val_right, param_list, define_list, line_num)

                if str(val_left).isdigit() and str(val_right).isdigit():
                    param_value = int(val_left) + int(val_right)
                else:
                    print("fatal: arguments in '+' must be positive integer. Parameter '%s', line %i\n" % (param_name, line_num + 1))
                    exit()    

            elif '-' in param_expr:
                val_left, val_right = param_expr.split('-')
                
                val_left, val_right = define_expression(val_left, val_right, param_list, define_list, line_num)

                if str(val_left).isdigit() and str(val_right).isdigit():
                    param_value = int(val_left) - int(val_right)
                else:
                    print("fatal: arguments in '-' must be positive integer. Parameter '%s', line %i\n" % (param_name, line_num + 1))
                    exit()

            elif '*' in param_expr:
                val_left, val_right = param_expr.split('*')
                
                val_left, val_right = define_expression(val_left, val_right, param_list, define_list, line_num)

                if str(val_left).isdigit() and str(val_right).isdigit():
                    param_value = int(val_left) * int(val_right)
                else:
                    print("fatal: arguments in '*' must be positive integer. Parameter '%s', line %i\n" % (param_name, line_num + 1))
                    exit()

            elif '/' in param_expr:
                val_left, val_right = param_expr.split('/')
                
                val_left, val_right = define_expression(val_left, val_right, param_list, define_list, line_num)

                if str(val_left).isdigit() and str(val_right).isdigit():
                    if int(val_left) % int(val_right) == 0:
                        param_value = int(int(val_left) / int(val_right))
                    else:
                        print("fatal: parameter '%s' must be positive integer, line %i\n" % (param_name, line_num + 1))
                        exit()
                else:
                    print("fatal: unknown expression in size of parameter '%s', line %i\n" % (param_name, line_num + 1))
                    exit()

            elif str(param_expr).isalpha():
                val, check = define_param_define(param_expr, param_list, define_list)

                if check < 1:
                    print("fatal: unknown parameter in size of parameter '%s', line %i\n" % (param_name, line_num + 1))
                    exit()
                else:
                    param_value = int(val)

            else:
                print("fatal: unknown expression in parameter value %s, line %i\n" % (param_name, line_num + 1))
                exit()
        
        # * simple parameter size
        else:
            param_value = param_expr

        if str(param_value).isdigit() and int(param_value) >= 0 and int(param_value) < 100000:
            parameter.name =  param_name
            parameter.value = int(param_value)
        else:
            print("fatal: parameter '%s' must be not negative integer, line %i\n" % (param_name, line_num + 1))
            exit()
        param_arr.append(parameter)
    
    return param_arr


# * fatals:
# duplicate name
# unknown parameter in pin size
# negative pin size
# negitive pin size values
# unknown expression in pin size values (not +/-) => unknown parameter
# float pin size
# * warnings:
# equal limits in pin size
def read_section_pins(line, param_list, define_list, pin_list, line_num):
    pin_arr = []
    pin_size = ''
    pin_direction = 'NaN'
    k = 1

    temp = line.content.strip().replace('\t', ' ')

    pin_direction_name = re.sub(r'\[[^()]*\]', '', temp) # substracting size

    pin_direction = pin_direction_name[:pin_direction_name.find(' ')] # input | output | inout

    pin_size = temp[temp.find('['):temp.find(']') + 1] # [...]
    
    temp_name = pin_direction_name.replace(pin_direction, '').strip()

    temp_name = temp_name.replace('reg', '').replace('wire', '').replace('tri', '').replace('integer', '')
    temp_name = temp_name.strip()

    # check if there is a bad type in temp_name (whitespace between)
    if ' ' in temp_name and not ',' in temp_name:
        print("fatal: bad pin type '%s', line %i\n" % (temp_name, line_num + 1))
        exit()  

    temp_name = re.sub("[;| |\t]", "", temp_name) # name1,name2,..
    if ',' in temp_name:
        temp_name_arr = temp_name.split(',')
    else:
        temp_name_arr = [temp_name]
    temp_name_arr = list(filter(None, temp_name_arr))  # deleting '' names
    # print('temp_name_arr:', temp_name_arr) # names array

    # check for duplicate and bad name
    for name in temp_name_arr:
            if not is_good_name(name):
                print("fatal: bad pin name '%s', line %i\n" % (name, line_num + 1))
                exit()
    for pin in pin_list:
        for name in temp_name_arr:
            if pin.name == name:
                print("fatal: duplicate pin name '%s', line %i\n" % (name, line_num + 1))
                exit()   


    # * parametric size
    if pin_size:

        pin_size = re.sub("[\[|\]| |\t]", "", pin_size)  # deleting [] and whitespaces
        if ':' in pin_size:
            left_val, right_val = pin_size.split(':')
        else:
            print("fatal: bad pin size '%s', line %i\n" % (name, line_num + 1))
            exit()
        # print('temp_size_arr:', temp_size_arr) # sizes array
        
        left_val = calc_pin_size_expression(left_val, param_list, define_list, temp_name, line_num)

        right_val = calc_pin_size_expression(right_val, param_list, define_list, temp_name, line_num)

        if int(left_val) < 0 or int(right_val) < 0:
            print("fatal: limits in pin size must be positive integer. Pin '%s', line %i\n" % (temp_name, line_num + 1))
            exit()

        if left_val == right_val:
            print("warning: equal limits in the pin size. Pin '%s', line %i\n" % (temp_name, line_num + 1))

        pin_true_size = int(left_val) - int(right_val) + 1

        if pin_true_size < 1:
            print("fatal: pin size must be positive integer. Pin '%s', line %i\n" % (temp_name, line_num + 1))
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
# specified module not found
# two or more non-callable modules
# two or more modules modules have the maximum number of attachments
def get_top_module(lines, specified_name = ''):
    module_list = []
    top_module = Module()
    found_specified = False

    # collecting module names and it's content
    module_fs = Module_for_search() #TODO можно без создания объекта?
    temp_name = ''
    is_module_section = False

    # collecting bodies of each module
    for line_num, line in enumerate(lines):
        
        line = skip_comment(line)
        line = line.replace('\t', ' ')
        if line == ' ' or '`define' in line:
            continue

        # outside module section -- searching start line of a module
        if not is_module_section:
            if ('module' in line or 'macromodule' in line) \
            and not 'endmodule' in line:

                module_fs = Module_for_search()
                temp_name = ''
                start_line = line_num
                module_fs.offset = line_num
                is_module_section = True
            else:
                continue

        # inside module section -- adding each line
        if is_module_section:
            temp_line = line.strip()
            module_fs.text += temp_line + ' '
            module_fs.text_arr.append(temp_line)

        # getting module name
        if not module_fs.name:
            temp_name += temp_line + ' '

            # note: ';' is end of module string
            if ';' in temp_line:
                temp_name = re.sub(r'\([^()]*\)', '', temp_name)
                temp_name = temp_name.replace('module', '')
                temp_name = re.sub('[;| ]', '', temp_name)
                module_fs.name = temp_name
                temp_name = ''

        if is_module_section and 'endmodule' in line:
            for mod in module_list:
                if mod.name == module_fs.name:
                    print("fatal: duplicate module name '%s', line %i\n" % (module_fs.name, start_line + 1))
                    exit() 

            is_module_section = False
            module_list.append(module_fs)
    
    if not module_list:
        print('fatal: no modules in file\n')
        exit()

    #* MANUAL mode: return module with specified name
    if specified_name:
        for mod in module_list:
            if mod.name == specified_name:
                found_specified = True
                top_module = mod
                return top_module

        if not found_specified:
            print("fatal: specified module '%s' not found\n" % (specified_name))
            exit() 

    #* AUTOMATIC mode: define top module
    # searching attachments in each module
    for mod in module_list:
        for submod in module_list:
            if submod.name in mod.text and submod.name != mod.name and submod.name not in mod.attachments:
                mod.attachments.append(submod.name)
                mod.attach_num += 1
                submod.called = True
    
    max_att = -1
    count_non_callable = 0
    for mod in module_list:
        if not mod.called:
            count_non_callable += 1
            # print(mod.name)
            if mod.attach_num > max_att:
                max_att = mod.attach_num

    if count_non_callable > 1:
        print('fatal: there are two or more non-callable modules\n')
        exit()


    # choosing top module as non-callable module
    count_top = 0
    for mod in module_list:
        if not mod.called and mod.attach_num == max_att:
            top_module = mod
            count_top += 1

    if count_top > 1:
        print('fatal: there are two or more non-callable modules modules have the maximum number of attachments\n')
        exit()

    return top_module
    