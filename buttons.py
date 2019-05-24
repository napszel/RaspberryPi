from lib import epd2in7, epdconfig
from PIL import Image, ImageFont, ImageDraw

import json, time, urllib

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

epd = epd2in7.EPD()
epd.init()

ethereum = "price_eth.json"
bitcoin = "price_btc.json"

currentlyShownETH = 0
curentlyShownBTC = 0

inCryptoDisplay = False

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
    with open(cryptoName) as pricefile:
        data = json.load(pricefile)
        price = int(round(float(data["price_usd"])))
        return price

def cryptoPriceChanged():
    newPriceETH = getPrice(ethereum)
    newPriceBTC = getPrice(bitcoin)
    global currentlyShownETH
    global currentlyShownBTC
    
    if newPriceETH != currentlyShownETH or newPriceBTC != currentlyShownBTC:
        currentlyShownETH = newPriceETH
        currentlyShownBTC = newPriceBTC
        return True
    else:
        return False
    
def cryptoTextGet():
    text = Image.new('1', (epd2in7.EPD_HEIGHT, epd2in7.EPD_WIDTH), 255)
    draw = ImageDraw.Draw(text)

    draw.text((0, 0), "ETH", font = font30, fill = 0)
    draw.text((60, 15), str(currentlyShownETH) + " $", font = font60, fill = 0)
    draw.text((0, 100), "BTC", font = font30, fill = 0)
    draw.text((60, 115), str(currentlyShownBTC) + " $", font = font60, fill = 0)
    
    return text

def setCryptoDisplay():
    epd.display(epd.getbuffer(cryptoTextGet()))

def updateCryptoPricesRightNow():
    global currentlyShownBTC
    global currentlyShownETH

    url = "http://api.coinmarketcap.com/v1/ticker/ethereum/"
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    ethprice = int(round(float(data[0]["price_usd"])))
    currentlyShownETH = ethprice

    url = "http://api.coinmarketcap.com/v1/ticker/bitcoin/"
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    btcprice = int(round(float(data[0]["price_usd"])))
    currentlyShownBTC = btcprice

    setCryptoDisplay()

    
def printImage(filename):
    image = Image.new('1', (epd2in7.EPD_HEIGHT, epd2in7.EPD_WIDTH), 255)

    bmp = Image.open(filename)
    image.paste(bmp, (0,0))
    
    epd.display(epd.getbuffer(image))

    
def main():
    printWelcomeMessage()

    global currentlyShownETH
    curentlyShownETH = getPrice(ethereum)
    global currentlyShownBTC
    currentlyShownBTC = getPrice(bitcoin)

    global inCryptoDisplay
    
    while True:
        key1state = GPIO.input(key1)
        key2state = GPIO.input(key2)
        key3state = GPIO.input(key3)
        key4state = GPIO.input(key4)

        if key1state == False:
            inCryptoDisplay = False
            printWelcomeMessage()
        if key2state == False:
            inCryptoDisplay = True
            updateCryptoPricesRightNow()
        if key3state == False:
            inCryptoDisplay = False
            printImage('images/boat.bmp')
        if key4state == False:
            inCryptoDisplay = False
            printImage('images/wave.bmp')

        time.sleep(0.05)
        if inCryptoDisplay and cryptoPriceChanged():
            setCryptoDisplay()
            
if __name__ == '__main__':
    main()
