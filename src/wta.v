`default_nettype none

module wta ( 
    input wire [7:0] current,
    input wire       clk,
    input wire       rst_n,
    output reg [7:0] u_out
);

    wire comparator;       // comparison of 4 MSBs vs 4 LSBs
    reg [7:0] result;

    always @(posedge clk) begin
        if (!rst_n) begin
            result <= 0;
            u_out <= 0;
        end else begin
            u_out <= result;
            result[7:4] <= (comparator ? current[7:4] : 0);
            result[3:0] <= (comparator ? 0 : current[3:0]);
        end
    end

    // if bits [7:4] are greater than bits [3:0] comparator returns 1, otherwise 0
    assign comparator = (current[7:4] >= current[3:0]);

endmodule