#!/usr/bin/env python
import uart_driver
import time
import struct

COMMAND_MOVE_HOME = b'\x01'
COMMAND_MOVE_HAPPY = b'\x02'
COMMAND_MOVE_EXCITED = b'\x03'
COMMAND_MOVE_IDLE = b'\x04'

def main():
    '''
    If run as standalone script connected to Arduino Uno, messages will be sent and received sequentially.
    '''

    uart = uart_driver.UARTDriver('COM3', 57600)

    time.sleep(10)

    try:
        while (1):
            value = input("Please enter command:\n")
            if (value == str(1)):
                print("MOVE HOME")
                uart.transmit(COMMAND_MOVE_HOME, [])
            elif (value == str(2)):
                print("MOVE_HAPPY")
                uart.transmit(COMMAND_MOVE_HAPPY, [])
            elif (value == str(3)):
                print("MOVE_EXCITED")
                uart.transmit(COMMAND_MOVE_EXCITED, [])
            elif (value == str(4)):
                print("MOVE_IDLE")
                uart.transmit(COMMAND_MOVE_IDLE, [])

    except KeyboardInterrupt:
        uart.shutdown()

if __name__ == "__main__":
    main()