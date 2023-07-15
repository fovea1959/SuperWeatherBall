import time
import board
import os

import socketpool
import wifi
import adafruit_minimqtt.adafruit_minimqtt as MQTT
import adafruit_logging as logging

logger = logging.getLogger('test')

logger.setLevel(logging.INFO)

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
        
        self.temp = label.Label(terminalio.FONT, text='', color=0xff8080)
        self.group.append(self.temp)
        
        self.templow = label.Label(terminalio.FONT, text='', color=0x8080ff)
        self.templow.y = 20
        self.group.append(self.templow)

        self.dt = label.Label(terminalio.FONT, text='', color=0x808080)
        self.dt.y = 200
        self.group.append(self.dt)
        
        g.append(self.group)
    
    def update(self, u):
        temp = float(u['temperature'])
        self.temp.text = str(temp)

        templow = float(u['templow'])
        self.templow.text = str(templow)

        self.dt.text = u['datetime']

forecast_panes = []
forecast_panes.append(ForecastPane(x=0, y=10))
forecast_panes.append(ForecastPane(x=200, y=10))
                                
display.show(g)

# Connect to WiFi
#print("Connecting to %s" % secrets["ssid"])
#wifi.radio.connect(secrets["ssid"], secrets["password"])
#print("Connected to %s!" % secrets["ssid"])

# Initialize MQTT interface with the esp interface
pool = socketpool.SocketPool(wifi.radio)

# Set up a MiniMQTT Client
mqtt_client = MQTT.MQTT(
  broker=os.getenv("MQTT"),
  socket_pool=pool
)
mqtt_client.logger = logger

def connected(client, userdata, flags, rc):
  ta_status.text = "Connected"
  ta_status.color = 0x00ff00
  
  # This function will be called when the client is connected
  # successfully to the broker.
  print(f"Connected to MQTT broker! rc={rc}")
  # Subscribe to all changes on the default_topic feed.
  #client.subscribe(('openweathermap/update_forecast_0', 'openweathermap/update_forecast_1'))
  client.subscribe('superweatherball')

def disconnected(client, userdata, rc):
  # This method is called when the client is disconnected
  print("Disconnected from MQTT Broker!")
  ta_status.text = "Disconnected"
  ta_status.color = 0xff0000

def message(client, topic, message):
  """Method callled when a client's subscribed feed has a new
  value.
  :param str topic: The topic of the feed with a new value.
  :param str message: The new value
  """
  print("New message on topic {0}: {1}".format(topic, message))

  payload = json.loads(message)
  for i, f in enumerate(payload['forecast']):
      forecast_panes[i].update(f)


# Setup the callback methods above
mqtt_client.on_connect = connected
mqtt_client.on_disconnect = disconnected
mqtt_client.on_message = message

# Connect the client to the MQTT broker.
print("Connecting to MQTT broker...")
mqtt_client.connect()
print("Connected to MQTT broker...")

# Start a blocking message loop...
# NOTE: NO code below this loop will execute
# NOTE: Network reconnection is handled within this loop
while True:
  try:
    mqtt_client.loop()
  except OSError as e:
    print("Failed to get data, retrying\n", e)
  except (ValueError, RuntimeError) as e:
    print("Failed to get data, retrying\n", e)
    # wifi.radio.reset()
    mqtt_client.reconnect()
    time.sleep(1)