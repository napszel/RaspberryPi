from lib import epd2in7, epdconfig
from PIL import Image, ImageFont, ImageDraw

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

epd = epd2in7.EPD()
epd.init()

font18 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 18)

key1 = 5
key2 = 6
key3 = 13
key4 = 19

GPIO.setup(key1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(key2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(key3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(key4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def printWelcomeMessage():
    welcome = Image.new('1', (epd2in7.EPD_HEIGHT, epd2in7.EPD_WIDTH), 255)

    welcomeMessage = ImageDraw.Draw(welcome)
    welcomeMessage.text((30, 60), 'Press a button', font = font18, fill = 0)
    welcomeMessage.line((0, 10, 28, 65), fill=0)
    welcomeMessage.line((0, 70, 28, 65), fill=0)
    welcomeMessage.line((0, 130, 28, 65), fill=0)
    welcomeMessage.line((0, 179, 28, 65), fill=0)

    epd.display(epd.getbuffer(welcome))

def writeOnDisplay(string):
    text = Image.new('1', (epd2in7.EPD_HEIGHT, epd2in7.EPD_WIDTH), 255)
    draw = ImageDraw.Draw(text)

    draw.text((10, 0), string, font = font18, fill = 0)
    epd.display(epd.getbuffer(text))

def printImage(filename):
    image = Image.new('1', (epd2in7.EPD_HEIGHT, epd2in7.EPD_WIDTH), 255)

    bmp = Image.open(filename)
    image.paste(bmp, (0,0))
    epd.display(epd.getbuffer(image))

def main():
    printWelcomeMessage()

    while True:
        key1state = GPIO.input(key1)
        key2state = GPIO.input(key2)
        key3state = GPIO.input(key3)
        key4state = GPIO.input(key4)

        if key1state == False:
            printWelcomeMessage()
            time.sleep(0.2)
        if key2state == False:
            writeOnDisplay('Button 2? Interesting choice.')
            time.sleep(0.2)
        if key3state == False:
            printImage('images/boat.bmp')
            time.sleep(0.2)
        if key4state == False:
            printImage('images/wave.bmp')
            time.sleep(0.2)

if __name__ == '__main__':
    main()
