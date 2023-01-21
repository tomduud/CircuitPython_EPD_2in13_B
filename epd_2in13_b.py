# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Waveshare team, 2023 Mikko Pitkänen
#
# SPDX-License-Identifier: MIT
"""
`epd_2in13_b`
================================================================================

Circuitpython library to use Waveshare 2.13 inch ePaper display with Raspberry Pico W


* Author(s): Waveshare team, Mikko Pitkänen

Implementation Notes
--------------------

This is a Circuitpython version of Waveshare 2.13" epaper display lib for Raspberry Pi Pico based on Waveshare team's micropython class/example.


**Hardware:**

* `Waveshare 2.13inch E-Paper E-Ink Display Module (B) for Raspberry Pi Pico https://www.waveshare.com/pico-epaper-2.13-b.htm`_
* `Waveshare 2.13inch E-Paper wiki https://www.waveshare.com/wiki/Pico-ePaper-2.13-B`_
* `Display module specification sheet https://www.waveshare.com/w/upload/d/d8/2.13inch_e-Paper_%28B%29_V3_Specification.pdf`_
* `Waveshare ePaper github pages https://github.com/waveshare/Pico_ePaper_Code`_


**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads



# * Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice


"""

# imports

__version__ = "0.0.1+auto.0"
__repo__ = "https://github.com/tomduud/CircuitPython_EPD_2in13_B.git"

import time

import digitalio
import busio
import adafruit_framebuf
import board


#define constant pins for pico
RST_PIN         = board.GP12 
DC_PIN          = board.GP8 
CS_PIN          = board.GP9 
BUSY_PIN        = board.GP13 

EPD_WIDTH       = 104
EPD_HEIGHT      = 212

class EPD_2in13_B:
    def __init__(self, rotation):
        # create the spi device and pins we will need
        self.spi = busio.SPI(clock=board.GP10, MOSI=board.GP11)

        self.cs = digitalio.DigitalInOut(CS_PIN)
        self.cs.direction = digitalio.Direction.OUTPUT
        self.dc = digitalio.DigitalInOut(DC_PIN)
        self.dc.direction = digitalio.Direction.OUTPUT
        self.rst = digitalio.DigitalInOut(RST_PIN)
        self.rst.direction = digitalio.Direction.OUTPUT
        self.busy = digitalio.DigitalInOut(BUSY_PIN)
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT

        self.framebuffer_black_array = bytearray(self.height * self.width // 8)
        self.framebuffer_red_array = bytearray(self.height * self.width // 8)
        self.framebuffer_black = adafruit_framebuf.FrameBuffer(self.framebuffer_black_array, self.width, self.height, adafruit_framebuf.MHMSB)
        self.framebuffer_red = adafruit_framebuf.FrameBuffer(self.framebuffer_red_array, self.width, self.height, adafruit_framebuf.MHMSB)

        self.framebuffer_black.rotation=rotation
        self.framebuffer_red.rotation=rotation

        self.init()

    def init(self):
        self.reset()
        self.send_command(0x04)
        self.ReadBusy()  # waiting for the electronic paper IC to release the idle signal

        self.send_command(0x00)  # panel setting
        self.send_data(0x0f)  # LUT from OTP,128x296
        self.send_data(0x89)  # Temperature sensor, boost and other related timing settings

        self.send_command(0x61)  # resolution setting
        self.send_data(0x68) # resolution setting
        self.send_data(0x00) # resolution setting
        self.send_data(0xD4) # resolution setting

        self.send_command(0x50)  # VCOM AND DATA INTERVAL SETTING
        self.send_data(0x87) # data Inteval

        print('Display initialized')

        return 0

    # Hardware reset
    def reset(self):
        self.digital_write(self.rst, True)
        self.delay_ms(50)
        self.digital_write(self.rst, False)
        self.delay_ms(2)
        self.digital_write(self.rst, True)
        self.delay_ms(50)

    def send_command(self, command):
        self.digital_write(self.dc, False)
        self.digital_write(self.cs, False)
        self.spi_writebyte([command])
        self.digital_write(self.cs, True)

    def digital_write(self, pin, value):
        pin.value = value

    def digital_read(self, pin):
        return pin.value

    def delay_ms(self, delaytime):
        time.sleep(delaytime / 1000.0)

    def spi_writebyte(self, data):
        while not self.spi.try_lock():
            pass
        try:
            self.spi.configure(baudrate=40000000, phase=0, polarity=0)
            self.cs.value = False
            self.spi.write(bytearray(data))
            self.cs.value = True
        finally:
            self.spi.unlock()

    def ReadBusy(self):
        print('Display busy')
        self.send_command(0x71)
        while (self.digital_read(self.busy) == 0):
            self.send_command(0x71)
            self.delay_ms(10)
        print('Display free')

    def send_data(self, data):
        self.digital_write(self.dc, True )
        self.digital_write(self.cs, False)
        self.spi_writebyte([data])
        self.digital_write(self.cs, True)

    def Clear(self, colorblack, colorred):
        self.send_command(0x10)
        for j in range(0, self.height):
            for i in range(0, int(self.width / 8)):
                self.send_data(colorblack)
        self.send_command(0x13)
        for j in range(0, self.height):
            for i in range(0, int(self.width / 8)):
                self.send_data(colorred)

        self.TurnOnDisplay()

    def TurnOnDisplay(self):
        self.send_command(0x12)
        self.ReadBusy()

    def sleep(self):
        self.send_command(0X50)
        self.send_data(0xf7)
        self.send_command(0X02)
        self.ReadBusy()
        self.send_command(0x07)  # DEEP_SLEEP
        self.send_data(0xA5)  #TODO check this code
        self.delay_ms(2000)

    def display(self):
        self.send_command(0x10)
        for j in range(0, self.height):
            for i in range(0, int(self.width / 8)):
                self.send_data(self.framebuffer_black_array[i + j * int(self.width / 8)])
        self.send_command(0x13)
        for j in range(0, self.height):
            for i in range(0, int(self.width / 8)):
                self.send_data(self.framebuffer_red_array[i + j * int(self.width / 8)])
        self.TurnOnDisplay()

