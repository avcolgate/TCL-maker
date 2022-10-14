import re

from verilog_classes import Line, Module, Module_for_search, Pin
from verilog_func import is_good_name, skip_comment

def parse_body(temp_module):
    module_name = temp_module.name
    module_body_arr = temp_module.text_arr
    module_offset = temp_module.offset + 1

    is_module_section = False
    module = Module()

    for line_num, curr_line in enumerate(module_body_arr): # TODO сделать отдельную функцию
        line = Line(curr_line)
        
        if not is_module_section and line.is_module_section():
            # print(line.content)
            module.append_name(module_name)
            is_module_section = True
            continue

        if is_module_section:
            if line.is_pin_section():
                # print(line.content)
                pin_arr = read_section_pins(line, module.pins, line_num + module_offset)
                for pin in pin_arr:
                    module.append_pin(pin)
                continue
            if line.is_endmodule_section():
                # print(line.content)
                is_module_section = False
                break
            
    return module

# * fatals:
# duplicate name
# unknown parameter in pin size
# negative pin size
# negitive pin size values
# unknown expression in pin size values (not +/-) => unknown parameter
# float pin size
# * warnings:
# equal limits in pin size
def read_section_pins(line, pin_list, line_num):
    pin_arr = []
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

        pin_wire_type = 'bus'
        
    # * simple size (=1)
    else:
        pin_wire_type = 'wire'

    for pin_name in temp_name_arr:
        pin = Pin(pin_name, pin_direction, pin_wire_type)
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
    