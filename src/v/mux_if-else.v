module mux_if_else
(
	input		d3,d2,d1,d0, 	// data	
	input		c2,c1,c0,		// control
	output	reg y
);
	always @*
	if (c0)
		y = d0;
	else if (c1)
		y = d1;	
	else if (c2)
		y = d2;
	else 
		y = d3;
 
endmodule