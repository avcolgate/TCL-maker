import os.path
import sys
import datetime

from read_func import *

MANUAL = False

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
        file.close()

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
        module_body_arr = top_module.text_arr
        module_offset = top_module.offset + 1


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

        if module.name != '':
            module.print()


        time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        output_path = 'runs/'
        output_name = module.name + '-' + time + '.txt'

        f = open(output_path + output_name, 'w')
        for pin in module.pins:
            if pin.direction == 'input':
                f.write(pin.name + ' ')


if __name__ == "__main__":
    main()
