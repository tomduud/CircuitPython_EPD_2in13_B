# Introduction
This is a simple Circuitpython library to use Waveshare 2.13 inch ePaper display with Raspberry Pico W. This uses `adafruit_framebuf` framebuffer library so you can use any of its drawing methods. 
This is a just simple conversion from Waveshare Micropython code to work with Circuitpython.

More information about the ePaper module this works with:
* Waveshare 2.13inch E-Paper E-Ink Display Module (B) for Raspberry Pi Pico https://www.waveshare.com/pico-epaper-2.13-b.htm
* Waveshare 2.13inch E-Paper wiki https://www.waveshare.com/wiki/Pico-ePaper-2.13-B
* Display module specification sheet https://www.waveshare.com/w/upload/d/d8/2.13inch_e-Paper_%28B%29_V3_Specification.pdf
* Waveshare ePaper github pages https://github.com/waveshare/Pico_ePaper_Code

# Dependencies
This library depends on:
* Adafruit CircuitPython https://github.com/adafruit/circuitpython

# Install 
To use with Circuitpython Copy `epd_2in13_b.py` or `epd_2in13_b.mpy` into `lib` folder of `CIRCUITPY` drive. 

Make sure you have also this library on your `lib` directory:

* adafruit_framebuf.mpy https://github.com/adafruit/Adafruit_CircuitPython_Bundle

and

* `font5x8.bin` in same directory as your code. You can download the font here :
https://github.com/adafruit/Adafruit_CircuitPython_framebuf/blob/main/examples/font5x8.bin




# Usage Example

This uses adafruit_framebuf framebuffer library. Please see more information about 'adafruit_framebuf' library drawing methods: 
https://docs.circuitpython.org/projects/framebuf/en/latest/ and https://github.com/adafruit/Adafruit_CircuitPython_framebuf 

```python


from epd_2in13_b import EPD_2in13_B

try:
    #initialise class with rotation:  rotation = 0 portrait, 1= landscape, 
    # 2 portrait upside down, 3= landscape upside down
    epd = EPD_2in13_B(1)
    #clear class
    epd.Clear(0x00, 0x00)
    # Clear black framebuffer
    epd.framebuffer_black.fill(0x00)
    # Clear red framebuffer
    epd.framebuffer_red.fill(0x00)
    # Write text to black framebuffer
    epd.framebuffer_black.text('Black text in 0,0 position.', 0, 0, 0xff)
    # Write text red framebuffer
    epd.framebuffer_red.text('Red text', 20, 20, 0xff)
    # Draw red circle on coordinate 50,50 with 20 radius
    epd.framebuffer_red.circle(45, 50, 20, 0xff)
    # Draw everything to display, this will take around 15 sec per layer
    epd.display()
    # put the display on the sleep mode
    epd.sleep();

except KeyboardInterrupt:
    print ("exception")
```

Another example with rotated red frame buffer layer
```python
from epd_2in13_b import EPD_2in13_B

try:
    #initialise class with rotation:  rotation = 0 portrait, 1= landscape, 
    # 2 portrait upside down, 3= landscape upside down
    epd = EPD_2in13_B(1)
    #clear class
    epd.Clear(0x00, 0x00)
    # Clear black framebuffer
    epd.framebuffer_black.fill(0x00)
    # Clear red framebuffer
    epd.framebuffer_red.fill(0x00)
    # Write text to black framebuffer
    epd.framebuffer_black.text('Black text in 0,0 position.', 0, 0, 0xff)
    # Write text red framebuffer

    # Change red framebuffer rotation to upside down
    epd.framebuffer_red.rotation = 3
    # draw text now upside down..
    epd.framebuffer_red.text('red text in 0,0 position.', 0, 8, 0xff)

    # Draw everything to display, this will take around 15 sec per layer
    epd.display()
    # put the display on the sleep mode
    epd.sleep();

except KeyboardInterrupt:
    print ("exception")
```




