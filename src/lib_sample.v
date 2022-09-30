
`define WIDTH 3
`define LENGTH 999  //new

module lib_sample (
	CLK,
	RST_B,
	SELECT_3,
	EN_G,
	BYPASS,
	CLK_OUT_DIV,
	CLK_OUT_G,
	CNTR_OUT1,
	CNTR_OUT2,
	CNTR_OUT3
	);
	
	parameter size = 32;
	parameter size0 = size, size1 = 32, size3 = 33, size4 = 2; //new
	
	parameter s0 = 3'd0, s1 = 3'b1111, s2 = 3'hFFA1, s3 = 3'o7, s4 = 3'd4, s5 = 3'd5;

input	CLK;
input	RST_B;
input	SELECT_3;
input	EN_G;
input [`WIDTH+`LENGTH:`LENGTH]	BYPASS;
output	reg CLK_OUT_DIV;
output	CLK_OUT_G;
output [`WIDTH-1:0] 	CNTR_OUT1;
output [`WIDTH-1:0] 	CNTR_OUT2;
output [`WIDTH-1:0] 	CNTR_OUT3;

reg [`WIDTH-1:0] CNTR1;
reg [`WIDTH-1:0] CNTR2;
reg [`WIDTH-1:0] CNTR3;

//cntr1
always @(posedge CLK) begin
	CNTR1<=CNTR1+1;
end

//cntr2 
always @(posedge CLK or negedge RST_B) begin
	if (!RST_B)  CNTR2<=0;
	else CNTR2<=CNTR2+1;
end
//cntr3 
always @(posedge CLK or negedge RST_B) begin
	if (!RST_B)  CNTR3<=0;
	else CNTR3<=CNTR3+1;
end

assign CNTR_OUT1 = CNTR1;
assign CNTR_OUT2 = CNTR2;
assign CNTR_OUT3 = SELECT_3 ? CNTR3 : BYPASS;

always @(posedge CLK) CLK_OUT_DIV<=~CLK_OUT_DIV;

assign CLK_OUT_G = EN_G && CLK_OUT_DIV;

endmodule
