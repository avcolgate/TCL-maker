
import verilog_reader.inputs_parser as verilog_parser
import tcl_builder.maker as tcl_maker

verilog_init_data = 'src/v/lib_sample.v'
design_name, inputs = verilog_parser.get_module_inputs(verilog_init_data.split())

transitions = [0.0100, 0.0282, 0.0794, 0.2236, 0.6300, 0.7748, 5.0000]
lib_path = r"C:\Users\avcolgate\Documents\.work\LIB_SAMPLE\INNOVUS\synopsys\lib_sample_PssV081Tm40.lib".replace('\\','/')
netlist_path = r"C:\Users\avcolgate\Documents\.work\LIB_SAMPLE\INNOVUS\rtl_v\lib_sample.v".replace('\\','/')
clocks = ['CLK']

tcl_maker.make_tcl(design_name, inputs, clocks, transitions, lib_path, netlist_path)
