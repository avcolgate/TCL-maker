module apb (

input logic         pclk,         // ????
input logic         preset,       // reset

output logic        psel,         // ?????????
output logic        penable,      // ????????????? ????????? 
output logic [31:0] paddr,        // ?????, ??????? ?????????? ????? ?????????? 
                                  //????? ?????????????, ???? ????? ????? + ?? ?????? ???? ??????????
output logic        pwrite,       // write=1, read=0
output logic [31:0] pwdata,       // ?
input  logic [31:0] prdata,       // ?
input  logic        pready,       // ????????? ????????

input  logic [1:0]  add           // ??? ?????????? IDLE, ????? ???????? ??????? ? SETUP ??? IDLE
                                  // 00-nothing, 01-READ, 11-WRITE

);

typedef enum logic [1:0] {IDLE, SETUP, ACCESS} abp_state;

abp_state state_q;
abp_state next_state;

logic next_pwrite;
logic pwrite_q;

logic next_rdata;
logic rdata_q;

always_ff @(posedge pclk or negedge preset)
  if(~preset)
    state_q <= IDLE;
  else 
    state_q <= next_state;
    
always_comb begin
 next_pwrite = pwrite_q;            // ?? ?????? ?????? 
 next_rdata = rdata_q;
  case(state_q)
  IDLE:  
    if(add[0])begin
      next_state = SETUP;
      next_pwrite = add[1];
    end else begin 
      next_state = IDLE;
    end
  SETUP: 
      next_state = ACESS
  ACCESS: 
    if (pready)
      if(~pwrite_q)
        next_rdata = prdata; 
      next_state=IDLE;
    else
      next_state = ACCESS;
  default: next_state = IDLE;
  end  
  
  
    assign psel = (state_q==SETUP)|(state_q==ACCESS); 
    assign penable = (state_q==ACCESS);
    
    //APB addres
    assign paddr = {32{state_q==ACCESS}} & 32'hA000;
    
    //APB PWRITE control signal
    
    always_ff @(posedge pclk or negedge preset)
      if (~preset)
        pwrite_q <= 1'b0;
      else
        pwrite_q <= next_pwrite;
    
    assign pwrite = pwrite_q;
    //APB PWDATA data signal
    
     always_ff @(posedge pclk or negedge preset)
    if (~preset)
      rdata_q <= 32'h0;
  	else
      rdata_q <= nxt_rdata;
    
    
endmodule