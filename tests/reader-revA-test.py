"""Tests for the revA circuit board of the 'reader'.

These tests will test the expected functionality of 'reader-revA'
(https://github.com/fmfi-svt-deadlock/reader-hw/releases/tag/revA).
They are intended to be run once on new boards before the FW is loaded
and the device is deployed
"""

import mempoke
import serial
import time
from test_sequencer import run, ask_YN, ask, say
from devices.stm32f0 import STM32F0


dev = STM32F0(mempoke.DeviceMemory())


def turn_on_led(port, pin):
    """Helper function for testing LEDs"""
    dev.RCC.AHBENR |= (1 << dev.RCC.AHBENR_bits["IOP" + port + "EN"])
    dev.GPIO[port].MODER |= (dev.GPIO[port].MODE_bits["OUTPUT"] << pin*2)
    dev.GPIO[port].ODR |= (1 << pin)


def reset_peripherals():
    """Resets *used* peripherals, teardown function."""

    ahbrst = 0
    for i in ['A', 'B', 'C', 'D', 'E', 'F']:
        ahbrst |= (1 << dev.RCC.AHBRSTR_bits["IOP" + i + "RST"])
    dev.RCC.AHBRSTR |= ahbrst
    dev.RCC.AHBRSTR &= ~ahbrst

    apb1rst = 0
    for bit in dev.RCC.APB1RSTR_bits.values():
        apb1rst |= (1 << bit)
    dev.RCC.APB1RSTR |= apb1rst
    dev.RCC.APB1RSTR &= ~apb1rst

    apb2rst = 0
    for bit in dev.RCC.APB2RSTR_bits.values():
        apb2rst |= (1 << bit)
    dev.RCC.APB2RSTR |= apb2rst
    dev.RCC.APB2RSTR &= ~apb2rst


def test_led1():
    """Tests green LED1"""
    reset_peripherals()

    turn_on_led('B', 1)
    error = None
    if not ask_YN('Is LED1 green?'):
        error = 'Green LED1 problem'
    reset_peripherals()
    return error


def test_led2():
    """Tests green LED2"""
    reset_peripherals()

    turn_on_led('A', 8)
    error = None
    if not ask_YN('Is LED2 green?'):
        error = 'Green LED2 problem'
    reset_peripherals()
    return error


def test_reader():
    """Tests communication with the RFID (MFRC522) module.

    This test verifies the presence and functionality of the MFRC522 module, as well as integrity
    of all SPI and RST signal paths.
    """
    reset_peripherals()

    RST_PIN = 3
    SS_PIN = 1

    # Enable port A GPIO for SPI usage
    dev.RCC.AHBENR |= (1 << dev.RCC.AHBENR_bits["IOPAEN"])
    # Set pins used by SPI1 to 'Alternate' mode
    moder_flags = 0
    for pin in [5, 6, 7]:
        moder_flags |= (dev.GPIO['A'].MODE_bits["ALT"] << pin*2)
    # Slave select is plain GPIO pin, as is RST
    moder_flags |= (dev.GPIO['A'].MODE_bits["OUTPUT"] << SS_PIN*2) | (dev.GPIO['A'].MODE_bits["OUTPUT"] << RST_PIN*2)
    dev.GPIO['A'].MODER |= moder_flags
    # Correct alternate function (AF-0) is already set up for all pins.

    # Enable the SPI 1
    dev.RCC.APB2ENR |= (1 << dev.RCC.APB2ENR_bits["SPI1EN"])

    # Use software slave management
    dev.SPI[1].CR1 |= (1 << dev.SPI[1].CR1_bits["SSM"])
    # Slowest comm speed (safest option) (0b111 to BR[2:0])
    dev.SPI[1].CR1 |= (0b111 << 3)
    # We are the master
    dev.SPI[1].CR1 |= (1 << dev.SPI[1].CR1_bits["MSTR"])
    # Clock phase and clock polarity is left default. Byte is sent MSB-first (also default)

    # 8-bit transfer data size
    dev.SPI[1].CR2 |= (0b0111 << 8)
    # Enable control of Slave Select pin
    dev.SPI[1].CR2 |= (1 << dev.SPI[1].CR2_bits["SSOE"])
    # Generate RX-Not-empty event when 8 bits were received
    dev.SPI[1].CR2 |= (1 << dev.SPI[1].CR2_bits["FRXTH"])

    # Enable the SPI
    dev.SPI[1].CR1 |= (1 << dev.SPI[1].CR1_bits["SPE"])

    # Power-up the reader and *un*select slave
    dev.GPIO['A'].ODR |= (1 << RST_PIN) | (1 << SS_PIN)

    # Transmit 0x82 0x00, which means "Read register 01h". That is the CommandReg of MFRC522. Its reset value is 0x20,
    # we will expect that as an answer
    response = []
    dev.GPIO['A'].ODR &= ~(1 << SS_PIN)
    for b in [0x82, 0x00]:
        dev.SPI[1].DR = b
        response.append(dev.SPI[1].DR)
    dev.GPIO['A'].ODR |= (1 << SS_PIN)

    reset_peripherals()

    if response[1] != 0x20:
        return "Error communicating with the MFRC522 module, or the module is not behaving properly!"


def test_usart_receive():
    """Tests USART Rx.

    This test verifies whether Controller is able to send data to the Reader. It assesses functionality of
    the IC4 and J1, as well as integrity of USART Rx signal path.
    If this test succeeds and there is no contact problem on the Tx path it is reasonable to assume that USART Tx
    will be working as well, as it cannot be tested directly.
    """
    reset_peripherals()

    port_name = ask("Serial port name to use")
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

    # Check that receiver has been enabled
    if not dev.USART[2].ISR & (1 << dev.USART[2].ISR_bits["REACK"]):
        reset_peripherals()
        return "Error enabling USART 2 receiver!"

    # Check for possible Rx overflow due to previous unintended transmissions
    if dev.USART[2].ISR & (1 << dev.USART[2].ISR_bits["ORE"]):
        dev.USART[2].ICR |= (1 << dev.USART[2].ICR_bits["ORECF"])

    # Empty the Rx buffer (limit: 30 times)
    for i in range(0, 30):
        if dev.USART[2].ISR & dev.USART[2].ISR_bits["RXNE"]:
            # Discard data from the RDR by reading it
            dev.USART[2].RDR
        else:
            break

    if dev.USART[2].ISR & dev.USART[2].ISR_bits["RXNE"]:
        reset_peripherals()
        return "USART is receiving something, but we are not transmitting. Noise?"

    # Clear possible leftover error flags
    dev.USART[2].ICR |= (1 << dev.USART[2].ICR_bits["PECF"]) | (1 << dev.USART[2].ICR_bits["FECF"])

    # Check whether we have idle line and are ready to receive
    if not dev.USART[2].ISR & (1 << dev.USART[2].ISR_bits["IDLE"]):
        reset_peripherals()
        return "USART is not idle, but we are not transmitting. Dry joint?"

    string = "DEADLOCK"

    for letter_num, letter in enumerate(string):
        # Transmit it
        port.write(letter)
        port.flush()

        # Wait for reception. At 9600 baud transmission should take ~0.8ms. We will wait 10ms
        # to be on the safe side.
        time.sleep(0.01)

        # Check reception
        if dev.USART[2].ISR & (1 << dev.USART[2].ISR_bits["RXNE"]):
            if dev.USART[2].RDR == ord(letter):
                continue
            else:
                reset_peripherals()
                return "USART received something else than what we sent"
        else:
            reset_peripherals()
            return "USART has not received letter {number} ({letter})".format(number=letter_num, letter=letter)

    # All done
    reset_peripherals()

tests = [test_led1, test_led2, test_reader, test_usart_receive]
run(tests)
