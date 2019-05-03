#!/usr/bin/python
# -*- coding:utf-8 -*-

from lib import epdconfig
from lib import epd2in7
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

try:
    epd = epd2in7.EPD()
    epd.init()
    # If called on white screen this blinks the screen black twice then leaves it white
    epd.Clear(0xFF)

    # Creates an Image object (all white with size of screen); use 0 as last argument for black screen
    myImage = Image.new('1', (epd2in7.EPD_HEIGHT, epd2in7.EPD_WIDTH), 255)

    # Creating an ImageDraw object that can draw stuff on an Image object; will be edited in place
    drawings = ImageDraw.Draw(myImage)
    
    font24 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 24)

    drawings.text((10, 0), 'hello world', font = font24, fill = 0)
    # line
    drawings.line((20, 50, 70, 100), fill = 0)
    # rectangle around the line
    drawings.rectangle((20, 50, 70, 100), outline = 0)
    # empty circle
    drawings.arc((140, 50, 190, 100), 0, 360, fill = 0)
    # filled circle
    drawings.chord((200, 50, 250, 100), 0, 360, fill = 0)
    # horizontal line
    drawings.line((10, 100, 400, 100), fill=0)

    # Display the Image object on the screen; it also prints 'Horizontal' on the console
    epd.display(epd.getbuffer(myImage))
#    time.sleep(2)
    
    epd.sleep()
        
except:
    print('traceback.format_exc():\n%s',traceback.format_exc())
    exit()

