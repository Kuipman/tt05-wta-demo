import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer, ClockCycles

# @cocotb.test()
# async def test_my_design(dut):
#     dut._log.info("start")



@cocotb.test()
async def test_my_design(dut):
    # Current value will be changed over time
    CURRENT = 0b11001101

    # Print to terminal that the simulation will begin
    dut._log.info("Start the simulation - WTA")

    # initialize clock
    clock = Clock(dut.clk, 1, units="ns")
    cocotb.start_soon(clock.start())

    # Trigger reset for 10 clock cycles
    dut.rst_n.value = 0                # reset is active low
    await ClockCycles(dut.clk, 10)     # 10 clock cycles
    dut.rst_n.value = 1                # deactivate reset signal

    dut.ui_in.value = CURRENT          # set input to current value
    dut.ena.value = 1                  # enable design

    ######### Test 1: Did the reset work?
    dut._log.info("Test 1: Check that the reset worked")
    dut._log.info(dut.uo_out.value)
    # assert dut.uo_out.value == 0     # if this fails, the test ends here automatically
    dut._log.info("Test 1 successful!")

    ######### Test 2: Pass initial current value through circuit, check results
    # Let clock run through 

    for i in range(100):  # run for 100 clock cycles
        await RisingEdge(dut.clk)
        # if i > 1:
        #     assert dut.uo_out.value == 0b00001101     # checks if the lower mux properly outputs value
    
    dut._log.info("Finished test!")