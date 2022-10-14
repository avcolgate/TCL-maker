from verilog_get_inputs import get_module_inputs

verilog_init_data = 'src/spm.v -m spm'
design_name, inputs = get_module_inputs(verilog_init_data.split())

transitions = [0.0100, 0.0282, 0.0794, 0.2236, 0.6300, 0.7748, 5.0000]
lib_path = r"C:\Users\avcolgate\Documents\.work\LIB_SAMPLE\INNOVUS\synopsys\lib_sample_PssV081Tm40.lib".replace('\\','/')
netlist_path = r"C:\Users\avcolgate\Documents\.work\LIB_SAMPLE\INNOVUS\rtl_v\lib_sample.v".replace('\\','/')

clocked_design = False
clock_names = []
port_names = []
clock_period = 10.0000 #?
clock_transition = 0.1000 #?

print(design_name, inputs, transitions)

for i in inputs:
    if str(i).lower() == 'clk':
        clocked_design = True
        clock_names.append(str(i))
    else:
        port_names.append(str(i))


str_clocks = ' '.join(clock_names)
str_ports = ' '.join(port_names)


for i in range(len(transitions)):
    output_tcl = open('tcl/%f.tcl' % transitions[i], 'w')

    output_tcl.write('read_liberty %s\n' % lib_path)
    output_tcl.write('read_verilog %s\n' % netlist_path)
    output_tcl.write('link_design %s\n' % design_name)
    
    if clocked_design:
        output_tcl.write('create_clock -name CLK -period %f [get_ports {%s}]\n' % (clock_period, str_clocks)) #? several clocks
        output_tcl.write('set_clock_transition %f [get_clocks {%s}]\n' % (clock_transition, str_clocks))

    output_tcl.write('set_input_transition %f [get_ports {%s}]\n' % (transitions[i], str_ports))

    output_tcl.write('write_timing_model %s\n' % 'PATH')
    output_tcl.write('exit')
    