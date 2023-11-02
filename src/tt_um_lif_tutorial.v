`default_nettype none

module tt_um_lif (
    input  wire [7:0] ui_in,    // Dedicated inputs - connected to the input switches
    output wire [7:0] uo_out,   // Dedicated outputs - connected to the 7 segment display
    input  wire [7:0] uio_in,   // IOs: Bidirectional Input path
    output wire [7:0] uio_out,  // IOs: Bidirectional Output path
    output wire [7:0] uio_oe,   // IOs: Bidirectional Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // will go high when the design is enabled
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

    // Inputs = 0, Outputs = 1
    // use bidirectionals as outputs
    // oe = output enable
    assign uio_oe = 8'b11111111;

module lif (
    input wire [7:0] current,
    input wire       clk,
    input wire       rst_n,      // resets state into known state
    output wire      spike,      // doesn't need to be stored
    output reg [7:0] state       // we ARE storing this value
);


    // instantiate lif neuron
    // copy this line as many times as needed to create multiple neurons
    lif lif1(.current(ui_in), .clk(clk), .rst_n(rst_n), .spike(uio_out[7]), .state(uo_out));

endmodule
