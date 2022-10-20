
def make_tcl(design_name, inputs, clocks_arr, transitions, lib_path, netlist_path):
    
    ports_arr = []
    clock_period = max(transitions)*4
    clock_tran = 0.1000 #?

    for port in inputs:
        if str(port) not in clocks_arr:
            ports_arr.append(port)


    str_clocks = ' '.join(clocks_arr)
    str_ports = ' '.join(ports_arr)


    for num, tran in enumerate(transitions):
        output_tcl = open('tcl/transition%i_%f.tcl' % (num, tran), 'w')

        output_tcl.write('read_liberty %s\n' % lib_path)
        output_tcl.write('read_verilog %s\n' % netlist_path)
        output_tcl.write('link_design %s\n\n' % design_name)
        
        
        for clk_num, clock in enumerate(clocks_arr):
            output_tcl.write('create_clock -name clk_%i -period %f [get_ports {%s}]\n' % (clk_num, clock_period, clock))

        output_tcl.write('set_clock_transition %f [get_clocks {%s}]\n' % (clock_tran, str_clocks))
        output_tcl.write('set_input_transition %f [get_ports {%s}]\n\n' % (tran, str_ports))

        output_tcl.write('write_timing_model %s\n' % 'PATH')
        output_tcl.write('exit')
