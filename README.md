# Hardware Testing Library

A helper library for creating HW tests for embedded devices. This repository
also contains tests for various boards developed for the project Deadlock.

## Usage

### Dependencies

You will need `arm-none-eabi-gdb` debugger, `stlink`, `python` 2.7 and `virtualenv`.

### Setup

Create a new virtual environment and install everything from `requirements.txt`,
activate it.

### Running tests

To run a test on a board, connect the board to the debugger and launch `st-util`.
Then select the test and run `./execute tests/name_of_the_test.py`.

### Interactive mode

For debugging, developing tests or just playing directly with MCUs peripherals
you can run this utility in the `interactive` mode. It will open a new
interactive Python console. The device object will be available as `dev` variable.

## Implemented tests

TODO

## Writing tests

### Device object

TODO

### Test sequencer

TODO
