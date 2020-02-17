#!/usr/bin/env python
import uart_driver
import time
import struct


def main():
    '''
    If run as standalone script connected to Arduino Uno, messages will be sent and received sequentially.
    '''

    uart = uart_driver.UARTDriver('COM3', 57600)
    motor1 = struct.pack('H', 500)
    motor2 = struct.pack('H', 300)
    data = motor1 + motor2
    
    time.sleep(7)
    print("Transmitting Data")
    val = 0.2
    # uart.transmit(b'\x01', data)
    # time.sleep(val)
    uart.transmit(b'\x02', data)
    # time.sleep(val)
    # uart.transmit(b'\x01', data)
    # time.sleep(val)
    uart.transmit(b'\x02', data)
    # time.sleep(val)
    # uart.transmit(b'\x01', data)
    # time.sleep(val)
    # uart.transmit(b'\x02', data)
    # line = []
    # time.sleep(1)
    # while(uart.ser.inWaiting()):
    #     char = uart.ser.readline()
    #     print(char, end=' ')

    time.sleep(10)
    uart.shutdown()



if __name__ == "__main__":
    main()