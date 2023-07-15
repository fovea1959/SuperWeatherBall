import time
import board
import os

import socketpool
import wifi
import adafruit_minimqtt.adafruit_minimqtt as MQTT
import adafruit_logging as logging

import json

import superweatherball_display


def connected(client, userdata, flags, rc):
    """
    This function will be called when the client is connected
    successfully to the broker.
    """
    
    swbd.update_status("Connected", color=0x00ff00)
    print(f"Connected to MQTT broker! rc={rc}")
  
    # Subscribe to all changes on the default_topic feed.
    client.subscribe('superweatherball')

def disconnected(client, userdata, rc):
    """
    This method is called when the client is disconnected
    """
    
    swbd.update_status("Disconnected", color=0xff0000)
    print("Disconnected from MQTT Broker!")

def message(client, topic, message):
    """
    Method callled when a client's subscribed feed has a new value.
    :param str topic: The topic of the feed with a new value.
    :param str message: The new value
    """

    print("New message on topic {0}: {1}".format(topic, message))

    payload = json.loads(message)
    for i, f in enumerate(payload['forecast']):
        swbd.update_forecast(i, f)


def main():
    global swbd
    swbd = superweatherball_display.Display()

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
    
    logger = logging.getLogger('mqtt')
    logger.setLevel(logging.INFO)
    mqtt_client.logger = logger
    
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
        
if __name__ == '__main__':
    main()
