"""Tests for the revA circuit board of the 'reader'.

These tests will test the expected functionality of 'reader-revA'
(https://github.com/fmfi-svt-deadlock/reader-hw/releases/tag/revA).
They are intended to be run once on new boards before the FW is loaded
and the device is deployed
"""

import mempoke
import serial
from test_sequencer import run, ask, askForString, say
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

    for bit in dev.RCC.APB1RSTR_bits.values():
        dev.RCC.APB1RSTR |= (1 << bit)
        dev.RCC.APB1RSTR &= ~(1 << bit)


def led1():
    """Tests green LED1"""
    reset_peripherals()

    turn_on_led('B', 1)
    error = None
    if not ask('Is LED1 green?'):
        error = 'Green LED1 problem'
    reset_peripherals()
    return error


def led2():
    """Tests green LED2"""
    reset_peripherals()

    turn_on_led('A', 8)
    error = None
    if not ask('Is LED2 green?'):
        error = 'Green LED2 problem'
    reset_peripherals()
    return error


def test_reader():
    """Tests communication with the RFID module"""
    reset_peripherals()

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
    # This is undoable in the current board revision. USART 2 Tx shares pin with SWCLK, we would
    # loose the debug link
    pass


def usart_receive():
    """Tests functionality of the RS232 interface direction reader <- controller."""
    reset_peripherals()

    port_name = askForString("Serial port name to use")
    port = serial.Serial(port_name, 9600)
    say("pySerial is using port " + port.name)

    # Enable GPIO A (USART Rx is using GPIOA 15)
    dev.RCC.AHBENR |= (1 << dev.RCC.AHBENR_bits["IOPAEN"])
    # Alternate function 1 for GPIOA 15 (USART 2 Rx)
    dev.GPIO['A'].MODER |= (dev.GPIO['A'].MODE_bits["ALT"] << 15*2)
    dev.GPIO['A'].AFRH |= (1 << 28)
    # Enable clock to USART 2
    dev.RCC.APB1ENR |= (1 << dev.RCC.APB1ENR_bits["USART2EN"])
    # Set baud rate: clock in debug config is 8MHz => 833
    dev.USART[2].BRR = 833
    # Enable receiver and enable USART 2
    dev.USART[2].CR1 |= (1 << dev.USART[2].CR1_bits["RE"]) | (1 << dev.USART[2].CR1_bits["UE"])

    # Check 'Receiver Enable Acknowledge'
    if not dev.USART[2].ISR & (1 << dev.USART[2].ISR_bits["REACK"]):
        reset_peripherals()
        return "Error enabling USART 2 receiver!"

    # Check for possible Rx overflow due to previous unintended transmissions
    if dev.USART[2].ISR & (1 << dev.USART[2].ISR_bits["ORE"]):
        dev.USART[2].ICR |= (1 << dev.USART[2].ICR_bits["ORECF"])

    # Empty the Rx buffer (limit: 30 times)
    for i in range(0, 30):
        if dev.USART[2].ISR & dev.USART[2].ISR_bits["RXNE"]:
            dev.USART[2].RDR
        else:
            break

    if dev.USART[2].ISR & dev.USART[2].ISR_bits["RXNE"]:
        reset_peripherals()
        return "USART is receiving something, we are not transmitting. Noise?"

    # Clear possible leftover error flags
    dev.USART[2].ICR |= (1 << dev.USART[2].ICR_bits["PECF"]) | (1 << dev.USART[2].ICR_bits["FECF"])

    # Check whether we have idle line and are ready to receive
    if not dev.USART[2].ISR & (1 << dev.USART[2].ISR_bits["IDLE"]):
        reset_peripherals()
        return "USART is not idle, but we are not transmitting. Dry joint?"

    string = "DEADLOCK"

    for i, letter in enumerate(string):
        # Transmit it
        port.write(letter)
        port.flush()

        # Wait for reception
        for i in range(0, 10):
            if dev.USART[2].ISR & (1 << dev.USART[2].ISR_bits["RXNE"]):
                break

        # Check reception
        if dev.USART[2].ISR & (1 << dev.USART[2].ISR_bits["RXNE"]):
            if dev.USART[2].RDR == ord(letter):
                continue
            else:
                reset_peripherals()
                return "USART received something else than what we sent"
        else:
            reset_peripherals()
            return "USART has not received letter " + str(i) + " (" + letter + ")"

    # All done
    reset_peripherals()

tests = [usart_receive]
# tests = [test_reader, led1, led2]
run(tests)
