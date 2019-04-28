#!/usr/bin/python
# -*- coding:utf-8 -*-

import epd2in7
import traceback

try:
    epd = epd2in7.EPD()
    epd.init()
    epd.Clear(0xFF)
    
    epd.sleep()
        
except:
    print('traceback.format_exc():\n%s',traceback.format_exc())
    exit()

