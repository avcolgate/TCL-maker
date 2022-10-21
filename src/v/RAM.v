module ram #(
        parameter ADDR_WIDTH = 4,   // ???? ??????
        parameter DATA_WIDTH = 8,   // ???? ??????
        parameter DEPTH = 16        // ???????

)
(
input clk ,
input [ADDR_WIDTH-1:0] addr,
input [DATA_WIDTH-1:0] i_data,
output [DATA_WIDTH-1:0] o_data,
input we

/////////////////////////////////////////////////////////////////////
   // APB
   input             pclk,            
   input      [ 4:0] paddr,   
   input             pwrite,
   input             psel,
   input             penable,
   input      [31:0] pwdata,
   output reg [31:0] prdata,
   output            pready,
   output            pslverr,

   // Interface
   input      [31:0] status32,
   input      [15:0] status16,
   input      [ 7:0] status8,
   output reg [31:0] control32,
   output reg [15:0] control16,
   output reg [ 7:0] control8
///////////////////////////////////////////////////////////////////

);

reg [DATA_WIDTH-1:0] mem [DEPTH-1:0];     
                                        
                                        
always @(posedge clk)
  begin 
    if (we) 
      mem[addr]= i_data;

  end   
  
assign o_data = mem[addr];

endmodule                                 