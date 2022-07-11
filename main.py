import sys
import os.path

from class_module import *
from class_line import *
from read_func import *

def main():
    if len(sys.argv) < 2:
        print('No path!')
        return

    if os.path.exists(sys.argv[1]):
        PATH = sys.argv[1].replace('\\', '/')
    else:
        print('No input file!')
        return

    with open(file = PATH, mode='rt') as file:
        module = Module()
        lines = file.read().split('\n')

        module_name = get_module_name(lines)                #TODO предусмотреть ошибки

        for curr_line in lines:
            line = Line(curr_line)

            if line.is_comment():
                continue
            
            if line.is_name_section(module_name):
                name = read_section_name(line)
                module.append_name(name)
                continue

            if module.name:
                if line.is_param_section():
                    param = read_section_params(line)
                    module.append_params(param)

                if line.is_pin_section():
                    pin_arr = read_section_pins(line, module.params)
                    for pin in pin_arr:
                        module.append_pin(pin)

                if line.is_endmodule_section():
                    break

        module.print()

if __name__ == "__main__":
    main()