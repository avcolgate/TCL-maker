module rom (
  
  input [1:0] addr,
  output reg [7:0] data

);

always @(addr)
  begin
    case (addr)
      0: data = 8'd05;  
      1: data = 8'd10;
      2: data = 8'd15;
      3: data = 8'd20;
    endcase  
  end
endmodule
