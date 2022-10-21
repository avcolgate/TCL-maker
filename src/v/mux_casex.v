  smodule mux_casex
(
	input		d3,d2,d1,d0, 	// data	
	input		c2,c1,c0,	// control
	output	reg y
);
 
	always @*
	casex ({c2, c1, c0})
		3'b??1: y = d0;
		3'b?10: y = d1;
		3'b100: y = d2;
		3'b000: y = d3;
	endcase
 
endmodule
