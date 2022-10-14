from pydoc import describe
import sys
from verilog_get_inputs import get_module_inputs

sys.argv.append('src/lib_sample.v')

str_inputs = ''
inputs = get_module_inputs(sys.argv)
for i in inputs:
    str_inputs += i + ' '

str_inputs = str_inputs.strip()

transitions = [0.0100, 0.0282, 0.0794, 0.2236, 0.6300, 0.7748, 5.0000]
lib_path = r"C:\Users\avcolgate\Documents\.work\LIB_SAMPLE\INNOVUS\synopsys\lib_sample_PssV081Tm40.lib".replace('\\','/')
v_path = r"C:\Users\avcolgate\Documents\.work\LIB_SAMPLE\INNOVUS\rtl_v\lib_sample.v".replace('\\','/')
design_name = "lib_sample"

print(str_inputs, transitions)

output_tcl = open('tcl/test.tcl', 'w')

output_tcl.write('read_liberty %s\n' % lib_path)
output_tcl.write('read_verilog %s\n' % v_path)
output_tcl.write('link_design %s\n' % design_name)

for i in range(len(transitions)):
    output_tcl = open('tcl/%f.tcl' % transitions[i], 'w')

    output_tcl.write('read_liberty %s\n' % lib_path)
    output_tcl.write('read_verilog %s\n' % v_path)
    output_tcl.write('link_design %s\n' % design_name)
    
    output_tcl.write('set_input_transition %f [get_ports {%s}]\n' % (transitions[i], str_inputs))

    output_tcl.write('write_timing_model %s\n' % 'PATH')
    output_tcl.write('exit')
    
        
