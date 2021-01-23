# This code is an example to run the Robogaia either the  6-axis encoder board
# using Python on the Raspberry Pi.
# Created: 9/16/2020
#
# Environment:
# - Raspian Buster
# - Python 3.7.3
# - SPI Enabled
# - spidev installed
#

import RPi.GPIO as GPIO
import spidev


class Encoder6:
    # iPin1, 2, and 3 are the chip select pins
    def __init__(self):
        GPIO.cleanup()
     
        self.max = 6 + 1
        self.pin1 = 40
        self.pin2 = 38
        self.pin3 = 36
        self.spi = spidev.SpiDev()

    # set the GPIO modes of the CS pins
    # initialize SPI
    #     BUS 0, DEVICE 1 (spidev0.1),
    #        note BUS 0 is the only one available on Raspberry Pi (although diagrams show a SPI 1)
    #        note DEVICE is the Chip Select pin which we will ignore and just not use in the circuit
    #             as we are manually setting the three CS pins
    #     Set Max Speed to 500KHz
    #     Set Mode to 0 (Clock Low Idle, Read Data on Rising Edge of Clock
    def InitializeEncoders(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin1, GPIO.OUT)
        GPIO.setup(self.pin2, GPIO.OUT)
        GPIO.setup(self.pin3, GPIO.OUT)
        self.EncoderDeselect()
        bus = 0
        # Device is the chip select pin. Set to 0 or 1, depending on the connections
        # Note we will leave the CS pin disconnected so this is just to satisfy the package
        device = 1
        # Enable SPI

        # Open a connection to a specific bus and device (chip select pin)
        self.spi.open(bus, device)

        # Set SPI speed and mode
        self.spi.max_speed_hz = 500000
        self.spi.mode = 0

        # initialize LSI chips, set to Quadrature mode and reset value
        for i in range(1, self.max):
            self.EncoderSetQuadrature(i)
            self.EncoderReset(i)

    # 0x88 is Write Mode Register 0
    # 0x03 sets the chip to Quadrature
    def EncoderSetQuadrature(self, iEncoder):
        self.EncoderSelect(iEncoder)
        msg = [0x88, 0x03]
        self.spi.xfer2(msg)
        self.EncoderDeselect()

    def EncoderReset(self, iEncoder):
        self.EncoderSelect(iEncoder)
        msg = [0x20]
        self.spi.xfer2(msg)
        self.EncoderDeselect()

    def EncoderSelect(self, iEncoder):
        
        if iEncoder == 1:
            GPIO.output(self.pin1, GPIO.LOW)
            GPIO.output(self.pin2, GPIO.LOW)
            GPIO.output(self.pin3, GPIO.LOW)
        elif iEncoder == 2:
            GPIO.output(self.pin1, GPIO.LOW)
            GPIO.output(self.pin2, GPIO.LOW)
            GPIO.output(self.pin3, GPIO.HIGH)
        elif iEncoder == 3:
            GPIO.output(self.pin1, GPIO.LOW)
            GPIO.output(self.pin2, GPIO.HIGH)
            GPIO.output(self.pin3, GPIO.LOW)
        elif iEncoder == 4:
            GPIO.output(self.pin1, GPIO.LOW)
            GPIO.output(self.pin2, GPIO.HIGH)
            GPIO.output(self.pin3, GPIO.HIGH)
        elif iEncoder == 5:
            GPIO.output(self.pin1, GPIO.HIGH)
            GPIO.output(self.pin2, GPIO.LOW)
            GPIO.output(self.pin3, GPIO.LOW)
        elif iEncoder == 6:
            GPIO.output(self.pin1, GPIO.HIGH)
            GPIO.output(self.pin2, GPIO.LOW)
            GPIO.output(self.pin3, GPIO.HIGH)

    def EncoderDeselect(self):
        GPIO.output(self.pin1, GPIO.HIGH)
        GPIO.output(self.pin2, GPIO.HIGH)
        GPIO.output(self.pin3, GPIO.HIGH)

    def ReadEncoder(self, iEncoder):
        self.EncoderSelect(iEncoder)
        msg = [0x60]
        self.spi.xfer2(msg)
        msg = [0x00, 0x00, 0x00, 0x00]
        result = self.spi.xfer2(msg)
        self.EncoderDeselect()
        value = (((result[0]*256+result[1])*256+result[2])*256+result[3])
        if value > 2147483647:
            value = value- 4294967295
        return value

    def Cleanup(self):
        GPIO.cleanup()

