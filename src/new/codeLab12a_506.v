module mult
  (
  input logic a,
  input logic b,
  input logic c,
  input logic d,
  input logic [1:0] sel,    
  output logic out
  );
    
  assign out = (sel=='b11)? a : (sel=='b10)? b:(sel=='b01)?c:d;
  
endmodule

