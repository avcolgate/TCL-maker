from class_module import *
from class_line import *
from read_func import *

PATH = './src/spm.v'
top_module_name = 'spm'

def main():
    with open(PATH, 'rt') as file:
        module = Module()

        for curr_line in file.read().split('\n'):

            line = Line(curr_line)

            if line.is_comment():
                continue
            
            if line.is_name_section(top_module_name):
                name = read_section_name(line)
                module.append_name(name)
                continue

            if module.name:
                if line.is_param_section():
                    param = read_section_params(line)
                    module.append_param(param)

                if line.is_pin_section():
                    pin_arr = read_section_pins(line, module.params)
                    for pin in pin_arr:
                        module.append_pin(pin)

                if line.is_endmodule_section():
                    break

        module.print()

if __name__ == "__main__":
    main()