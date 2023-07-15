import time
import board

import socketpool
import wifi
import adafruit_minimqtt.adafruit_minimqtt as MQTT

import json

import terminalio
import displayio
from adafruit_display_text import label

# Release the existing display, if any
#displayio.release_displays()

display = board.DISPLAY

# Set text, font, and color
font = terminalio.FONT
color = 0x0000FF

# Create the text label
ta_status = label.Label(font, text='This is a test', color=color)

# Set the location
ta_status.x = 140
ta_status.y = 10

g = displayio.Group(x=0, y=0)

g.append(ta_status)

class ForecastPane:
    def __init__(self,x=0, y=0):
        self.group = displayio.Group(x=x, y=y)
        self.temp = label.Label(terminalio.FONT, text='', color=0xffffff)
        self.group.append(self.temp)
        g.append(self.group)
    
    def update(self, i):
        self.temp.text = str(i)

p = []
p.append(ForecastPane(x=0, y=10))
p.append(ForecastPane(x=200, y=10))
                                
display.show(g)

i = 0
while True:
    print(i)
    ta_status.text = str(i)
    p[0].update(i)
    p[1].update(-i)
    time.sleep(1)
    i = i + 1