 
//serially programmable look-up table
module lut(
    input wire  ldclk, //clock used for image loading
    input wire  ldi,   //lut load data input
    output wire ldo,   //lut load data output
    input wire  lds,   //lut load data signal
   
    input wire [3:0]in,
    output wire out
);
 
reg [15:0]lut_reg;
always @(posedge ldclk)
    if(lds)
        lut_reg <= { lut_reg[14:0],ldi };
 
assign ldo = lut_reg[15];
assign out = lut_reg[in];
 
endmodule
 
//serially programmable multiplexor
module pmux8(
    input wire  ldclk, //clock used for image loading
    input wire  ldi, //load data input
    output wire ldo, //load data output
    input wire  lds, //load data signal
   
    input wire  [7:0]in,
    output wire out
);
 
reg [2:0]sel_reg;
always @(posedge ldclk)
    if(lds)
        sel_reg <= { sel_reg[1:0],ldi };
 
assign ldo = sel_reg[2];
assign out = (in[sel_reg] & (~lds));
 
endmodule
 
//serially programmable multiplexor
module pmux4(
    input wire  ldclk, //clock used for image loading
    input wire  ldi, //load data input
    output wire ldo, //load data output
    input wire  lds, //load data signal
   
    input wire  [3:0]in,
    output wire out
);
 
reg [1:0]sel_reg;
always @(posedge ldclk)
    if(lds)
        sel_reg <= { sel_reg[0],ldi };
 
assign ldo = sel_reg[1];
assign out = (in[sel_reg] & (~lds));
 
endmodule
 
//logic element
module le(
    input wire  ldclk,
    input wire  ldi, //load data input
    output wire ldo, //load data output
    input wire  lds, //load data signal
 
    input wire  sysclk,
    input wire  [3:0]in,
    input wire  rena,
    output wire rout, //reg out
    output wire lout, //lut out
    output wire pout  //pin out
);
 
wire lut_load_out;
wire lut_out;
lut lut_inst(
    .ldclk(ldclk),
    .ldi(ldi),
    .ldo(lut_load_out),
    .lds(lds),
    .in(in),
    .out(lut_out)
);
 
reg le_reg;
always @(posedge sysclk or posedge lds)
    if(lds)
        le_reg <= 0;
    else
    if(rena)
        le_reg <= lout;
 
reg pin_ctrl;
always @(posedge ldclk)
    if(lds)
        pin_ctrl <= lut_load_out;
 
assign ldo = pin_ctrl;
assign lout = lut_out &(~lds);
assign pout = pin_ctrl ? rout : lout;
assign rout = le_reg;
 
endmodule
 
module mini_cpld(
    input wire  ldclk,
    input wire  ldi, //load data input
    output reg  ldo, //load data output
    input wire  lds, //load data signal
 
    input wire clk,
    input wire [3:0]in_pin,
    output wire [3:0]out_pin
);
 
// Logic Element #0 and connections
 
//multiplexer for LE0 clk: can select from 3 regs output or system clock
wire serial_img0;
wire sysclk0;
pmux4 pmux_inst_clk0(
    .ldclk(ldclk),
    .ldi(ldi),
    .ldo(serial_img0),
    .lds(lds),
    .in( {clk, rout1, rout2, rout3} ),
    .out(sysclk0)
    );
 
wire serial_img1;
wire rena0;
pmux8 pmux_inst_ena0(
    .ldclk(ldclk),
    .ldi(serial_img0),
    .ldo(serial_img1),
    .lds(lds),
    .in( {in_pin[0], lout1, lout2, lout3, 1'b1, rout1, rout2, rout3} ),
    .out(rena0)
    );
 
wire serial_img2;
wire lut0_in0;
pmux8 pmux_inst_lut00(
    .ldclk(ldclk),
    .ldi(serial_img1),
    .ldo(serial_img2),
    .lds(lds),
    .in( {in_pin[0], lout1, lout2, lout3, rout0, rout1, rout2, rout3} ),
    .out(lut0_in0)
    );
 
wire serial_img3;
wire lut0_in1;
pmux8 pmux_inst_lut01(
    .ldclk(ldclk),
    .ldi(serial_img2),
    .ldo(serial_img3),
    .lds(lds),
    .in( {in_pin[1], lout1, lout2, lout3, rout0, rout1, rout2, rout3} ),
    .out(lut0_in1)
    );
 
wire serial_img4;
wire lut0_in2;
pmux8 pmux_inst_lut02(
    .ldclk(ldclk),
    .ldi(serial_img3),
    .ldo(serial_img4),
    .lds(lds),
    .in( {in_pin[2], lout1, lout2, lout3, rout0, rout1, rout2, rout3} ),
    .out(lut0_in2)
    );
 
wire serial_img5;
wire lut0_in3;
pmux8 pmux_inst_lut03(
    .ldclk(ldclk),
    .ldi(serial_img4),
    .ldo(serial_img5),
    .lds(lds),
    .in( {in_pin[3], lout1, lout2, lout3, rout0, rout1, rout2, rout3} ),
    .out(lut0_in3)
    );
 
wire serial_img6;
wire rout0, lout0;
le le_inst0(
    .ldclk(ldclk),
    .ldi(serial_img5),
    .ldo(serial_img6),
    .lds(lds),
 
    .sysclk(sysclk0),
    .in( {lut0_in0,lut0_in1,lut0_in2,lut0_in3} ),
    .rena(rena0),
    .rout(rout0),
    .lout(lout0),
    .pout(out_pin[0])
);
 
// Logic Element #1 and connections
 
//multiplexer for LE1 clk: can select from 3 regs output or system clock
wire serial_img7;
wire sysclk1;
pmux4 pmux_inst_clk1(
    .ldclk(ldclk),
    .ldi(serial_img6),
    .ldo(serial_img7),
    .lds(lds),
    .in( { rout0, clk, rout2, rout3} ),
    .out(sysclk1)
    );
 
wire serial_img8;
wire rena1;
pmux8 pmux_inst_ena1(
    .ldclk(ldclk),
    .ldi(serial_img7),
    .ldo(serial_img8),
    .lds(lds),
    .in( {lout0, in_pin[1], lout2, lout3, rout0, 1'b1, rout2, rout3} ),
    .out(rena1)
    );
 
wire serial_img9;
wire lut1_in0;
pmux8 pmux_inst_lut10(
    .ldclk(ldclk),
    .ldi(serial_img8),
    .ldo(serial_img9),
    .lds(lds),
    .in( { lout0, in_pin[0], lout2, lout3, rout0, rout1, rout2, rout3} ),
    .out(lut1_in0)
    );
 
wire serial_img10;
wire lut1_in1;
pmux8 pmux_inst_lut11(
    .ldclk(ldclk),
    .ldi(serial_img9),
    .ldo(serial_img10),
    .lds(lds),
    .in( { lout0, in_pin[1], lout2, lout3, rout0, rout1, rout2, rout3} ),
    .out(lut1_in1)
    );
 
wire serial_img11;
wire lut1_in2;
pmux8 pmux_inst_lut12(
    .ldclk(ldclk),
    .ldi(serial_img10),
    .ldo(serial_img11),
    .lds(lds),
    .in( { lout0, in_pin[2], lout2, lout3, rout0, rout1, rout2, rout3} ),
    .out(lut1_in2)
    );
 
wire serial_img12;
wire lut1_in3;
pmux8 pmux_inst_lut13(
    .ldclk(ldclk),
    .ldi(serial_img11),
    .ldo(serial_img12),
    .lds(lds),
    .in( { lout0, in_pin[3], lout2, lout3, rout0, rout1, rout2, rout3} ),
    .out(lut1_in3)
    );
 
wire serial_img13;
wire rout1, lout1;
le le_inst1(
    .ldclk(ldclk),
    .ldi(serial_img12),
    .ldo(serial_img13),
    .lds(lds),
 
    .sysclk(sysclk1),
    .in( {lut1_in0,lut1_in1,lut1_in2,lut1_in3} ),
    .rena(rena1),
    .rout(rout1),
    .lout(lout1),
    .pout(out_pin[1])
);
 
// Logic Element #2 and connections
 
//multiplexer for LE2 clk: can select from 3 regs output or system clock
wire serial_img14;
wire sysclk2;
pmux4 pmux_inst_clk2(
    .ldclk(ldclk),
    .ldi(serial_img13),
    .ldo(serial_img14),
    .lds(lds),
    .in( { rout0, rout1, clk, rout3} ),
    .out(sysclk2)
    );
 
wire serial_img15;
wire rena2;
pmux8 pmux_inst_ena2(
    .ldclk(ldclk),
    .ldi(serial_img14),
    .ldo(serial_img15),
    .lds(lds),
    .in( {lout0, lout1, in_pin[2], lout3, rout0, rout1, 1'b1, rout3} ),
    .out(rena2)
    );
 
wire serial_img16;
wire lut2_in0;
pmux8 pmux_inst_lut20(
    .ldclk(ldclk),
    .ldi(serial_img15),
    .ldo(serial_img16),
    .lds(lds),
    .in( { lout0, lout1, in_pin[0], lout3, rout0, rout1, rout2, rout3} ),
    .out(lut2_in0)
    );
 
wire serial_img17;
wire lut2_in1;
pmux8 pmux_inst_lut21(
    .ldclk(ldclk),
    .ldi(serial_img16),
    .ldo(serial_img17),
    .lds(lds),
    .in( { lout0, lout1, in_pin[1], lout3, rout0, rout1, rout2, rout3} ),
    .out(lut2_in1)
    );
 
wire serial_img18;
wire lut2_in2;
pmux8 pmux_inst_lut22(
    .ldclk(ldclk),
    .ldi(serial_img17),
    .ldo(serial_img18),
    .lds(lds),
    .in( { lout0, lout1, in_pin[2], lout3, rout0, rout1, rout2, rout3} ),
    .out(lut2_in2)
    );
 
wire serial_img19;
wire lut2_in3;
pmux8 pmux_inst_lut23(
    .ldclk(ldclk),
    .ldi(serial_img18),
    .ldo(serial_img19),
    .lds(lds),
    .in( { lout0, lout1, in_pin[3], lout3, rout0, rout1, rout2, rout3} ),
    .out(lut2_in3)
    );
 
wire serial_img20;
wire rout2, lout2;
le le_inst2(
    .ldclk(ldclk),
    .ldi(serial_img19),
    .ldo(serial_img20),
    .lds(lds),
 
    .sysclk(sysclk2),
    .in( {lut2_in0,lut2_in1,lut2_in2,lut2_in3} ),
    .rena(rena2),
    .rout(rout2),
    .lout(lout2),
    .pout(out_pin[2])
);
 
// Logic Element #3 and connections
 
//multiplexer for LE3 clk: can select from 3 regs output or system clock
wire serial_img21;
wire sysclk3;
pmux4 pmux_inst_clk3(
    .ldclk(ldclk),
    .ldi(serial_img20),
    .ldo(serial_img21),
    .lds(lds),
    .in( { rout0, rout1, rout2, clk} ),
    .out(sysclk3)
    );
 
wire serial_img22;
wire rena3;
pmux8 pmux_inst_ena3(
    .ldclk(ldclk),
    .ldi(serial_img21),
    .ldo(serial_img22),
    .lds(lds),
    .in( {lout0, lout1, lout2, in_pin[3], rout0, rout1, rout2, 1'b1} ),
    .out(rena3)
    );
 
wire serial_img23;
wire lut3_in0;
pmux8 pmux_inst_lut30(
    .ldclk(ldclk),
    .ldi(serial_img22),
    .ldo(serial_img23),
    .lds(lds),
    .in( { lout0, lout1, lout2, in_pin[0], rout0, rout1, rout2, rout3} ),
    .out(lut3_in0)
    );
 
wire serial_img24;
wire lut3_in1;
pmux8 pmux_inst_lut31(
    .ldclk(ldclk),
    .ldi(serial_img23),
    .ldo(serial_img24),
    .lds(lds),
    .in( { lout0, lout1, lout2, in_pin[0], rout0, rout1, rout2, rout3} ),
    .out(lut3_in1)
    );
 
wire serial_img25;
wire lut3_in2;
pmux8 pmux_inst_lut32(
    .ldclk(ldclk),
    .ldi(serial_img24),
    .ldo(serial_img25),
    .lds(lds),
    .in( { lout0, lout1, lout2, in_pin[0], rout0, rout1, rout2, rout3} ),
    .out(lut3_in2)
    );
 
wire serial_img26;
wire lut3_in3;
pmux8 pmux_inst_lut33(
    .ldclk(ldclk),
    .ldi(serial_img25),
    .ldo(serial_img26),
    .lds(lds),
    .in( { lout0, lout1, lout2, in_pin[0], rout0, rout1, rout2, rout3} ),
    .out(lut3_in3)
    );
 
wire serial_img27;
wire rout3, lout3;
le le_inst3(
    .ldclk(ldclk),
    .ldi(serial_img26),
    .ldo(serial_img27),
    .lds(lds),
 
    .sysclk(sysclk3),
    .in( {lut3_in0,lut3_in1,lut3_in2,lut3_in3} ),
    .rena(rena3),
    .rout(rout3),
    .lout(lout3),
    .pout(out_pin[3])
);
 
always @(posedge ldclk)
    if(lds)
        ldo <= serial_img27;
 
endmodule
 