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


def test_reader():
    """Tests communication with the RFID module"""
    # Enable port A GPIO for SPI usage
    dev.RCC.AHBENR |= (1 << dev.RCC.AHBRSTR_bits["IOPAEN"])
    # Set pins used by SPI1 to 'Alternate' mode
    for pin in [5, 6, 7, 1]:
        dev.GPIO['A'].MODER |= (1 << dev.GPIO['A'].MODE_bits["ALT"] << pin*2)

    # Use software slave management
    dev.SPI[1].CR1 |= (1 << dev.SPI[1].CR1_bits["SSM"])
    # Slowest comm speed (safest option) (0x111 to BR[2:0])
    dev.SPI[1].CR1 |= (0x111 << 3)
    # We are the master
    dev.SPI[1].CR1 |= (1 << dev.SPI[1].CR1_bits["MSTR"])
    # Clock phase and clock polarity is left on default

    # 8-bit transfer data size
    dev.SPI[1].CR2 |= (0x0111 << 8)
    # Enable control of Slave Select pin
    dev.SPI[1].CR2 |= (1 << dev.SPI[1].CR2_bits["SSOE"])
    # Generate RX-Not-empty event when 8 bits were received
    dev.SPI[1].CR2 |= (1 << dev.SPI[1].CR2_bits["FRXTH"])

    # Enable the SPI
    dev.SPI[1].CR1 |= (1 << dev.SPI[1].CR1_bits["SPE"])


def usart_transmit():
    """Tests functionality of the RS232 interface direction reader -> controller."""
    pass


def usart_receive():
    """Tests functionality of the RS232 interface direction reader <- controller."""
    # Set-up GPIO Rx pin (GPIOA 15?) as alternate
    # Set GPIOA 15 AF-1
    # Enable clock to USART 2
    # Set baud rate: clock in debug config is 8MHz => 833
    # Enable receiver and enable USART 2
    # Check RDR

tests = [usart_transmit]
# tests = [test_reader, led1, led2]
run(tests)
