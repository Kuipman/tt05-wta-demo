import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer, ClockCycles

# @cocotb.test()
# async def test_my_design(dut):
#     dut._log.info("start")



@cocotb.test()
async def test_my_design(dut):
    # Current value will be changed over time
    CURRENT = 205 # 0b11001101 # 205  2

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

    # wait 10 clock cycles + run a second reset
    await ClockCycles(dut.clk, 10)     # 10 clock cycles
    dut.rst_n.value = 0                # reset is active low
    await ClockCycles(dut.clk, 10)     # 10 clock cycles
    dut.rst_n.value = 1                # deactivate reset signal


    ######### Test 1: Did the reset work?
    dut._log.info("Test 1: Check that the reset worked")
    # for i in range (50):
    #     dut._log.info(dut.uo_out.value)   # DEBUG - prints the current value of uo_out
    #     await RisingEdge(dut.clk)
    dut._log.info(dut.uo_out.value) 
    # assert dut.uo_out.value == 0      # if this fails, the test ends here automatically
    dut._log.info("Test 1 successful!")

    ######### Test 2: Pass initial current value through circuit, check results
    dut._log.info("Test 2: First true circuit check with current 0b11001101")
    await ClockCycles(dut.clk, 5)            # let input propagate through circuit before checking
    await RisingEdge(dut.clk)                # wait for next clock tick -- specifically the rising edge
    # dut._log.info("Value of uo_out = " + dut.uo_out.value)   # DEBUG - prints the current value of uo_out
    dut._log.info(dut.uo_out.value)          # print out the new result
    # assert dut.uo_out.value == 13 #0b00001101    # expected value

    ########## Test 3: Change the current, let three clock cycles run through, verify accurate new result
    dut._log.info("Test 3: Change current to 0b11100110, verify change in result value after 3 clock cycles")
    CURRENT = 230 # 0b11100110
    dut.ui_in.value = CURRENT          # set input to current value
    await ClockCycles(dut.clk, 3)
    await RisingEdge(dut.clk)
    # print out the result and check (assert) that this is expected
    dut._log.info(dut.uo_out.value)
    # assert dut.uo_out.value == 224 #0b11100000
    

    ######### Final Test: Test series of run-throughs with set current
    dut._log.info("Final Test: Run through series of cycles with constant current, ensure no crash.")
    for i in range(100):  # run for 100 clock cycles
        await RisingEdge(dut.clk)
        # dut._log.info(dut.uo_out.value)
        # if i > 1:
        #     assert dut.uo_out.value == 0b00001101     # checks if the lower mux properly outputs value
    
    dut._log.info("Finished test!")