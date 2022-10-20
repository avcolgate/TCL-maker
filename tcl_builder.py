from verilog_get_inputs import get_module_inputs

verilog_init_data = 'src/lib_sample.v'
design_name, inputs = get_module_inputs(verilog_init_data.split())

transitions = [0.0100, 0.0282, 0.0794, 0.2236, 0.6300, 0.7748, 5.0000]
lib_path = r"C:\Users\avcolgate\Documents\.work\LIB_SAMPLE\INNOVUS\synopsys\lib_sample_PssV081Tm40.lib".replace('\\','/')
netlist_path = r"C:\Users\avcolgate\Documents\.work\LIB_SAMPLE\INNOVUS\rtl_v\lib_sample.v".replace('\\','/')

clocks_arr = ['CLK']
ports_arr = []
clock_period = 10.0000 #?
clock_transition = 0.1000 #?

print(design_name, inputs, transitions)

for port in inputs:
    if str(port) not in clocks_arr:
        ports_arr.append(port)


str_clocks = ' '.join(clocks_arr)
str_ports = ' '.join(ports_arr)


for i in range(len(transitions)):
    output_tcl = open('tcl/transition%i_%f.tcl' % (i, transitions[i]), 'w')

    output_tcl.write('read_liberty %s\n' % lib_path)
    output_tcl.write('read_verilog %s\n' % netlist_path)
    output_tcl.write('link_design %s\n\n' % design_name)
    
    
    for num, clock in enumerate(clocks_arr):
        output_tcl.write('create_clock -name clk_%i -period %f [get_ports {%s}]\n' % (num, clock_period, clock))

    output_tcl.write('set_clock_transition %f [get_clocks {%s}]\n' % (clock_transition, str_clocks))

    output_tcl.write('set_input_transition %f [get_ports {%s}]\n\n' % (transitions[i], str_ports))

    output_tcl.write('write_timing_model %s\n' % 'PATH')
    output_tcl.write('exit')
    