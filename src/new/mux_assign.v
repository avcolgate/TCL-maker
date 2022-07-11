module mult_assign  // ????????? ?????????
  (
  input a,
  input b,
  input c,
  input d,
  input [1:0] sel,    
  output wire out
  );
    
  assign out = (sel=='b11)? a : (sel=='b10)? b:(sel=='b01)?c:d;
  
endmodule
