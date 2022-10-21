
import verilog_reader.inputs_parser as verilog_parser
import tcl_builder.maker as tcl_maker
from transition_getter.get_transition import get_net_transition

lib_dir = "src/lib"
verilog_init_data = 'src/v/lib_sample.v'
clock_names = ['CLK']

design_name, inputs = verilog_parser.get_module_inputs(verilog_init_data.split())

print(design_name)

# transitions = [0.0100, 0.0282, 0.0794, 0.2236, 0.6300, 0.7748, 5.0000]
lib_path = r"C:/Users/avcolgate/Documents/.work/LIB_SAMPLE/INNOVUS/synopsys/lib_sample_PssV081Tm40.lib"
netlist_path = r"C:/Users/avcolgate/Documents/.work/LIB_SAMPLE/INNOVUS/rtl_v/lib_sample.v"

transitions = get_net_transition(lib_dir)

print(transitions)
tcl_maker.make_tcl(design_name, inputs, clock_names, transitions, lib_path, netlist_path)
