import board

import terminalio
import displayio
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
from adafruit_bitmap_font import bitmap_font

import adafruit_datetime

FONT24 = bitmap_font.load_font("fonts/SegoeUI-24.pcf")
FONT48 = bitmap_font.load_font("fonts/SegoeUI-48.pcf")

class Display:
    def __init__(self):
        # Release the existing display, if any	
        #displayio.release_displays()
        
        display = board.DISPLAY

        # Set text, font, and color
        font = terminalio.FONT
        color = 0x0000FF

        g = displayio.Group(x=0, y=0)

        # Create the text label and set the location
        self.ta_status = label.Label(font, text='This is a test', color=color, anchor_point=(0.5, 1.0), anchored_position=(display.width/2, display.height))
        
        g.append(label.Label(FONT24, text='High', color=0x808080, anchor_point=(0.5, 0.5), anchored_position=(display.width/2, 30)))
        g.append(label.Label(FONT24, text='Low', color=0x808080, anchor_point=(0.5, 0.5), anchored_position=(display.width/2, 90)))
        g.append(self.ta_status)
        
        self.forecast_panes = []
        self.forecast_panes.append(ForecastPane(supergroup=g, x=0, y=0))
        self.forecast_panes.append(ForecastPane(supergroup=g, x=display.width - ForecastPane.WIDTH, y=0)) # 320 - (80 width)
                                
        display.show(g)
        
    def update_status(self, text, color=0xffffff):
        self.ta_status.color = color
        self.ta_status.text = text
    
    def update_forecast(self, i, forecast):
        self.forecast_panes[i].update(forecast)
        

class ForecastPane:
    WIDTH = 120
    def __init__(self, supergroup=None, x=0, y=0):
        group = displayio.Group(x=x, y=y)
        
        group.append (Rect(0, 0, self.WIDTH, 60, fill=0x100000))
        group.append (Rect(0, 60, self.WIDTH, 120, fill=0x000010))
        
        self.temp = label.Label(FONT48, text='', color=0xff8080, anchor_point=(0.5, 0.5), anchored_position=(self.WIDTH/2, 30))
        group.append(self.temp)
        
        self.templow = label.Label(FONT48, text='', color=0x8080ff, anchor_point=(0.5, 0.5), anchored_position=(self.WIDTH/2, 90))
        group.append(self.templow)

        self.dt = label.Label(FONT24, text='', color=0x808080, anchor_point=(0.5, 0.5), anchored_position=(self.WIDTH/2, 140))
        group.append(self.dt)

        supergroup.append(group)
    
    def update(self, u):
        temp = u['temperature']
        self.temp.text = str(temp)

        templow = u['templow']
        self.templow.text = str(templow)

        z = adafruit_datetime.datetime.fromisoformat(u['datetime'])
        tt = z.timetuple()
        dow = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][tt[6]]
        self.dt.text = dow

def main():
    import time
    d = Display()
    
    i = 0
    while True:
        d.update_status("Disconnected" if i % 2 == 0 else "Connected")
        
        d.update_forecast(0, { 'datetime': '2023-06-27T17:00:00+00:00', 'temperature': -i, 'templow': i-100 })
        d.update_forecast(1, { 'datetime': '2023-06-27T17:00:00+00:00', 'temperature': i, 'templow': i-1 })
        
        i = i + 1
        time.sleep(1)


if __name__ == '__main__':
    main()
