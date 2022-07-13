module b1_enc_assign(
 input [15:0] in,
 output [3:0] binary_out,
 input enable
 );
 assign binary_out[0] = (in[1] | in[3] | in[5] | in[7] | in[9] | in[11] | in[13] | in[15]) & enable;
 assign binary_out[1] = (in[2] | in[3] | in[6] | in[7] | in[10] | in[11] |   in[14] | in[15]) & enable;
 assign binary_out[2] = (in[4] | in[5] | in[6] | in[7] | in[12] | in[13] | in[14] | in[15]) & enable;
 assign binary_out[3] = (in[8] | in[9] | in[10] | in[11] | in[12] | in[13] | in[14] | in[15]) & enable;
endmodule