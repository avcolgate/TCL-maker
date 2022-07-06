from module_class import *
from module_line import *
from read_func import *

PATH = './src/spm.v'
top_module_name = 'spm'

with open(PATH, 'rt') as file:
    module = Module()

    lines = file.read().split('\n')

    for curr_line in lines:
        line = Line(curr_line)

        if line.is_comment():
            continue
        
        if line.is_name_section(top_module_name):
            module.append_name(top_module_name)
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