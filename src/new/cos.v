module cos #(
parameter ADDR_WIDTH = 4,
parameter DATA_WIDTH = 8,
parameter DEPTH = 16
) 

(
input clk,
input [ADDR_WIDTH-1:0] addr,
input [DATA_WIDTH-1:0] i_data,
output [DATA_WIDTH-1:0] o_data,
input we
	);

reg [DATA_WIDTH-1:0] mem [DEPTH-1:0];

always @(posedge clk)

begin
if (we) mem[addr]=i_data;
end
assign o_data =mem[addr] ;
endmodule