import os.path
import sys

from read_func import *

MANUAL = True

def main():
    print('MANUAL MODE\n') if MANUAL else print('AUTOMATIC MODE\n')

    if len(sys.argv) < 2:
        print('fatal: the path is not specified\n')
        exit()
    elif os.path.exists(sys.argv[1]):
        path = sys.argv[1].replace('\\', '/')
        if os.stat(path).st_size == 0:
            print('fatal: input file is empty\n')
            exit() 
    else:
        print('fatal: input file does not exist\n')
        exit()
        

    with open(file=path, mode='rt') as file:
        module = Module()
        is_module_section = False
        
        lines = file.read().split('\n')

        append_defines(lines, module)

        if MANUAL:
            # module name is specified
            if len(sys.argv) > 2:
                specified_name = sys.argv[2]
                if not is_good_name(specified_name):
                    print("fatal: bad specified module name '%s'\n" % (specified_name))
                    exit()
                else:
                    top_module = get_top_module(lines, specified_name)

            # module name is not specified   
            else:
                print('fatal: module name is not specified\n')
                exit()

        #* AUTOMATIC
        else:
            if len(sys.argv) > 2:
                print('warning: module name is not necessary in AUTOMATIC mode. It will be chosen automatically\n')
            top_module = get_top_module(lines)

        module_name = top_module.name
        module_body = top_module.text_arr
        module_offset = top_module.offset + 1


        for line_num, curr_line in enumerate(module_body): # TODO сделать отдельную функцию
            line = Line(curr_line)

            line.erase_comment()
            
            if not is_module_section:
                if line.is_name_section(module_name, module_body, line_num):
                    # print(line.content)
                    module.append_name(module_name)
                    is_module_section = True
                    continue

            else:
                if line.is_param_section():
                    # print(line.content)
                    param = read_section_params(line, module.params, line_num + module_offset)
                    module.append_params(param)
                    continue

                if line.is_pin_section():
                    # print(line.content)
                    pin_arr = read_section_pins(line, module.params, module.defines, module.pins, line_num + module_offset)
                    for pin in pin_arr:
                        module.append_pin(pin)
                    continue

                if line.is_endmodule_section():
                    # print(line.content)
                    is_module_section = False
                    break

    module.print()


if __name__ == "__main__":
    main()
