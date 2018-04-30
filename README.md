# PROJECT MOVED

This repository is now hosted here: https://gitlab.com/project-deadlock/hw-testing

# Hardware Testing Library

A helper library for creating HW tests for embedded devices. This repository
also contains tests for various boards developed for the project Deadlock.

For the project overview, and more information about how this testing library
works, what it is being used for and how to extend it
see https://github.com/fmfi-svt-deadlock/server/wiki.

## Usage

### Dependencies

You will need `arm-none-eabi-gdb` debugger, `stlink`, `python` 2.7 and `virtualenv`.

### Setup

Create a new virtual environment and install everything from `requirements.txt`,
activate it.

```
$ virtualenv-2.7 venv
New python executable in venv/bin/python2
Also creating executable in venv/bin/python
Installing setuptools, pip, wheel...done.

$ source venv/bin/activate

$ pip install -r requirements.txt
```

### Running tests

To run a test on a board, connect the board to the debugger and launch `st-util`.
Then select the test and run `./execute tests/name_of_the_test.py`.

### Interactive mode

For debugging, developing tests or just playing directly with MCUs peripherals
you can run this utility in the `interactive` mode. It will open a new
interactive Python console. The device object will be available as `dev` variable.
For more information about what the device object is, please read the documentation
here: https://github.com/fmfi-svt-deadlock/server/wiki/Hardware-testing-library.

## Implemented features

### Supported devices

  - STM32F0 MCU (most peripherals: RCC, GPIO, ADC, DAC, USART, SPI, USB)

### Implemented tests

For more detailed information about each test please refer to the documentation
of the Python test file itself.

  - `tests/reader-revA-test.py` - Tests most essential functions of the Reader(+) revA
    board (SPI, USART, LEDs).
