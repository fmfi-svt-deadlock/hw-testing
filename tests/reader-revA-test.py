"""Tests for the revA circuit board of the 'reader'.

These tests will test the expected functionality of 'reader-revA'
(https://github.com/fmfi-svt-deadlock/reader-hw/releases/tag/revA).
They are intended to be run once on new boards before the FW is loaded
and the device is deployed
"""

import mempoke
from test_sequencer import run, ask
from devices.stm32f0 import STM32F0


dev = STM32F0(mempoke.DeviceMemory())


def turn_on_led(port, pin):
    """Helper function for testing LEDs"""
    dev.RCC.AHBENR |= (1 << dev.RCC.AHBENR_bits["IOP" + port + "EN"])
    dev.GPIO[port].MODER |= (dev.GPIO[port].MODE_bits["OUTPUT"] << pin*2)
    dev.GPIO[port].ODR |= (1 << pin)


def reset_peripherals():
    """Resets used peripherals, teardown function"""
    for i in ['A', 'B', 'C', 'D', 'E', 'F']:
        dev.RCC.AHBRSTR |= (1 << dev.RCC.AHBRSTR_bits["IOP" + i + "RST"])
        dev.RCC.AHBRSTR &= ~(1 << dev.RCC.AHBRSTR_bits["IOP" + i + "RST"])


def led1():
    """Tests green LED1"""
    turn_on_led('B', 1)
    error = None
    if not ask('Is LED1 green?'):
        error = 'Green LED1 problem'
    reset_peripherals()
    return error


def led2():
    """Tests green LED2"""
    turn_on_led('A', 8)
    error = None
    if not ask('Is LED2 green?'):
        error = 'Green LED2 problem'
    reset_peripherals()
    return error

tests = [led1, led2]
run(tests)
