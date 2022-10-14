import sys
from datetime import datetime

from verilog_func import define_init_data
from verilog_read import get_top_module, parse_body

#*         0    1     2
#* AUTO:  PATH
#* MANUAL PATH -m MODULE_NAME

def get_module_inputs(init_data = []):

    input_arr = []
    path, specified_name = define_init_data(init_data)

    with open(file=path, mode='rt') as file:
        
        lines = file.read().split('\n')
        file.close()

        temp_module = get_top_module(lines, specified_name)

        module = parse_body(temp_module)

        time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        out_path = 'runs/' + module.name + '-' + time + '.txt'
        log_path = 'logs/' + module.name + '-' + time + '.log'

        log_file = open(log_path, 'w')
        module.print(log_file)

        output_file = open(out_path, 'w')
        for pin in module.pins:
            if pin.direction == 'input':
                output_file.write(pin.name + ' ')
                input_arr.append(pin.name)

    return input_arr


# if __name__ == "__main__":
#     get_module_inputs(sys.argv)
