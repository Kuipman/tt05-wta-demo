`default_nettype none    // no unintended nets made

// THIS REPLACES DECODER.V

module lif (
    input wire [7:0] current,
    input wire       clk,
    input wire       rst_n,      // resets state into known state
    output wire      spike,      // doesn't need to be stored
    output reg [7:0] state       // we ARE storing this value
);

    reg [7:0] next_state, threshold;

    always @(posedge clk) begin
        if (!rst_n) begin        // rst_n is active low
            state <= 0;
            threshold <= 127;
        end else begin
            state <= next_state;
        end

    // next_state logic
    //assign next_state = current + (state * beta)
    assign next_state = current + (state >> 1)     // equivalent to beta = 0.5 -- division by 2

    // spiking logic
    assign spike = (state >= threshold);

    end

endmodule

