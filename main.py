import os.path
import sys
import datetime

from read_func import *
#*          0      1    2     3
#* AUTO:  main.py PATH
#* MANUAL main.py PATH -m MODULE_NAME

def main():

    path, specified_name = define_init_data(sys.argv)

    with open(file=path, mode='rt') as file:
        module = Module()
        is_module_section = False
        
        lines = file.read().split('\n')
        file.close()

        top_module = get_top_module(lines, specified_name)

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

        time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        out_path = 'runs/' + module.name + '-' + time + '.txt'
        log_path = 'logs/' + module.name + '-' + time + '.log'

        log_file = open(log_path, 'w')
        module.print(log_file)

        output_file = open(out_path, 'w')
        for pin in module.pins:
            if pin.direction == 'input':
                output_file.write(pin.name + ' ')


if __name__ == "__main__":
    main()
