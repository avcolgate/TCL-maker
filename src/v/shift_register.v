module shift_register #(

parameter OUT = 8

)

(
  
  input clk,
  input in,
  output y,
  output reg [OUT-1:0] out 
  
  );


always @(posedge clk)
  begin
  out = out << 1;
  out[0]= in;
  end
 assign y = out[OUT-1];
endmodule

 
