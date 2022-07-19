import os.path
import sys

from read_func import *


MANUAL = False

def main():
    print('MANUAL MODE\n') if MANUAL else print('AUTOMATIC MODE\n')

    if len(sys.argv) < 2:
        print('fatal: the path is not specified')
        exit()

    if os.path.exists(sys.argv[1]):
        path = sys.argv[1].replace('\\', '/')
    else:
        print('fatal: input file does not exist')
        exit()

    with open(file=path, mode='rt') as file:
        is_module_section = False
        module = Module()
        lines = file.read().split('\n')

        if MANUAL:
            if len(sys.argv) > 2:
                module_name = sys.argv[2]
            else:
                print('fatal: module name is not specified')
                exit()
        else:
            module_name = get_module_name(lines)

        # lines = list(filter(None, lines))  # deleting '' lines #!!

        for line_num, curr_line in enumerate(lines):
            line = Line(curr_line)

            if line.is_comment():
                continue

            if '//' in line.content:
                line.content = line.content[:line.content.find('//')]
            
            if line.is_name_section(module_name):
                module.append_name(module_name)
                is_module_section = True
                continue

            if is_module_section:
                if line.is_param_section():
                    param = read_section_params(line, module.params, line_num)
                    module.append_params(param)
                    continue

                if line.is_pin_section():
                    pin_arr = read_section_pins(line, module.params, module.pins, line_num)
                    for pin in pin_arr:
                        module.append_pin(pin)
                    continue

                if line.is_endmodule_section():
                    is_module_section = False
                    break

        module.print()


if __name__ == "__main__":
    main()
