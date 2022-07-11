
//////////////////////////////////
module NAND (x,y,f);              //NAND

  input x,y;
  output f;
 
  assign f=~(x&y);
  
endmodule 
//////////////////////////////////
module INV (x,f);                 //INV
  
  input x;
  output f;
  
  assign f=~x;
  
endmodule
//////////////////////////////////
module RS (S,R,Q,Q1);             //Обычная защелка
  
  input S,R;
  output Q,Q1;
  
  NAND N1 (S,Q1,Q);
  NAND N2 (Q,R,Q1);
  
  
endmodule
//////////////////////////////////
module Dtrig(D,clk,Q,Q1);         //D-триггер
                                  //
  input D,clk;
  output Q,Q1;
  wire Y1,Y2;
  
  NAND N3 (D,clk,Y1);
  NAND N4 (Y1,clk,Y2);
  
  RS RS1 (Y1,Y2,Q,Q1);
  
endmodule
//////////////////////////////////
module TRIGGERUP(D,clk,Q);          //Триггер по переднему

  input D,clk;
  output Q;
  wire Y,Y1,Y2,Y3;
  
  INV INV1 (clk,Y);
  Dtrig Dtrig1 (D,Y,Y1,Y2);
  Dtrig Dtrig2 (Y1,clk,Q,Y3);
  
endmodule
/////////////////////////////////
module etbits(D,clk,Q0,Q1,Q2,Q3,Q4,Q5,Q6,Q7); //Сдвиговый регистр 8 бит
  
  input D,clk;
  output Q0,Q1,Q2,Q3,Q4,Q5,Q6,Q7;
  wire Y0,Y1,Y2,Y3,Y4,Y5,Y6,Y7;
  
  TRIGGERUP T0 (D,clk,Q0);
  TRIGGERUP T1 (Q0,clk,Q1);
  TRIGGERUP T2 (Q1,clk,Q2);
  TRIGGERUP T3 (Q2,clk,Q3);
  TRIGGERUP T4 (Q3,clk,Q4);
  TRIGGERUP T5 (Q4,clk,Q5);
  TRIGGERUP T6 (Q5,clk,Q6);
  TRIGGERUP T7 (Q6,clk,Q7);
  
endmodule
//////////////////////////////////
module TRIGGERDOWN(D,clk,Q);          //Триггер по заднему

  input D,clk;
  output Q;
  wire Y,Y1,Y2,Y3;
  
  INV INV1 (clk,Y);
  Dtrig Dtrig1 (D,clk,Y1,Y2);
  Dtrig Dtrig2 (Y1,Y,Q,Y3);
  
endmodule
/////////////////////////////////
module CT(C,Q0,Q1,Q2,Q);
  
  input C;
  output Q0,Q1,Q2,Q;
  
  TRIGGERDOWN T1(~Q0,C,Q0);
  TRIGGERDOWN T2(~Q1,Q,Q1);
  TRIGGERDOWN T3(~Q2,Q1,Q2);
endmodule
