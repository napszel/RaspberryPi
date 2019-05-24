from lib import epd2in7, epdconfig
from PIL import Image, ImageFont, ImageDraw

import urllib, json

import RPi.GPIO as GPIO
import sched, time

GPIO.setmode(GPIO.BCM)

epd = epd2in7.EPD()
epd.init()

cryptoUrl = "http://api.coinmarketcap.com/v1/ticker/"
s = sched.scheduler(time.time, time.sleep)

font60 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 60)
font30 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 30)
font18 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 18)
font16 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 16)

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
    welcomeMessage.text((0, 0), 'Welcome to Nilcons\' SMART OFFICE', font = font16, fill=0)
    welcomeMessage.text((0, 25), 'display. Please select the ambience', font = font16, fill=0)
    welcomeMessage.text((0, 50), 'of the room.', font = font16, fill = 0) 
    welcomeMessage.text((0, 75), '1. Welcome menu card', font = font16, fill = 0)
    welcomeMessage.text((0, 100), '2. Present current ETH/BTC prices', font = font16, fill = 0)
    welcomeMessage.text((0, 125), '3. Motivational ship conquer scene ', font = font16, fill = 0)
    welcomeMessage.text((0, 150), '4. Relaxing meditation waves', font = font16, fill = 0)

    epd.display(epd.getbuffer(welcome))

def getPrice(cryptoName):
    url = "http://api.coinmarketcap.com/v1/ticker/" + cryptoName
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    price = int(round(float(data[0]["price_usd"])))
    return str(price)

def cryptoTextGet():
    text = Image.new('1', (epd2in7.EPD_HEIGHT, epd2in7.EPD_WIDTH), 255)
    draw = ImageDraw.Draw(text)

    draw.text((0, 0), "Click 2. button again to update.", font = font18, fill = 0)
    draw.text((0, 25), "ETH", font = font30, fill = 0)
    draw.text((60, 35), getPrice("ethereum") + " $", font = font60, fill = 0)
    draw.text((0, 100), "BTC", font = font30, fill = 0)
    draw.text((60, 115), getPrice("bitcoin") + " $", font = font60, fill = 0)

    return text

def cryptoOnceDisplay():
    epd.display(epd.getbuffer(cryptoTextGet()))
    
def cryptoScheduledDisplay(sc):
    epd.display(epd.getbuffer(cryptoTextGet()))

    s.enter(5, 1, cryptoScheduledDisplay, (sc,))

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
        if key2state == False:
            cryptoOnceDisplay()
            #s.enter(5, 1, cryptoScheduledDisplay, (s,))
            #s.run()
        if key3state == False:
            printImage('images/boat.bmp')
        if key4state == False:
            printImage('images/wave.bmp')

if __name__ == '__main__':
    main()
