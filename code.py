# SPDX-FileCopyrightText: Brent Rubell for Adafruit Industries
# SPDX-License-Identifier: MIT
import supervisor
supervisor.disable_autoreload()


import time
from microcontroller import cpu
import board
import busio
from digitalio import DigitalInOut
from adafruit_esp32spi import adafruit_esp32spi
from adafruit_esp32spi import adafruit_esp32spi_wifimanager
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
import adafruit_minimqtt.adafruit_minimqtt as MQTT
from adafruit_io.adafruit_io import IO_MQTT

from buzzersongs import BuzzerSongs
import digitalio
from lcd1602 import LCD
import adafruit_rgbled
from rainbowio import colorwheel
import adafruit_thermistor

### WiFi ###

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

# Raspberry Pi RP2040
esp32_cs = DigitalInOut(board.GP13)
esp32_ready = DigitalInOut(board.GP14)
esp32_reset = DigitalInOut(board.GP15)


spi = busio.SPI(board.GP10, board.GP11, board.GP12)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

wifi = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(esp, secrets)

# Configure the RP2040 Pico LED Pin as an output
led_pin = DigitalInOut(board.LED)
led_pin.switch_to_output()

# Configure other peripherals
lcd = LCD()

song = BuzzerSongs(board.GP16)

red = board.GP7
green = board.GP8
blue = board.GP9
led = adafruit_rgbled.RGBLED(red, blue, green)
led.color = (222, 49, 99)

thermo = adafruit_thermistor.Thermistor(board.GP26, 10000.0, 10000.0, 25.0, 3950.0, high_side=False)


# Define callback functions which will be called when certain events happen.
# pylint: disable=unused-argument
def connected(client):
    # Connected function will be called when the client is connected to MQTT Broker.
    print("Connected to MQTT Broker! ")


def subscribe(client, userdata, topic, granted_qos):
    # This method is called when the client subscribes to a new feed.
    print("Subscribed to {0} with QOS level {1}".format(topic, granted_qos))


# pylint: disable=unused-argument
def disconnected(client):
    # Disconnected function will be called when the client disconnects.
    print("Disconnected from MQTT Broker!")


def on_led_msg(client, topic, message):
    # Method called whenever user/feeds/reiley/led has a new value
    print("New message on topic {0}: {1} ".format(topic, message))
    if message == "ON":
        led_pin.value = True
    elif message == "OFF":
        led_pin.value = False
    else:
        print("Unexpected message on LED feed.")

def on_song_msg(client, topic, message):
    # Methoc called whenever user/feeds/reiley/song has a new value
    print("New message on topic {0}: {1} ".format(topic, message))
    song.play(message)

def on_lcd_msg(client, topic, message):
    # Methoc called whenever user/feeds/reiley/lcd has a new value
    print("New message on topic {0}: {1} ".format(topic, message))
    lcd.clear()
    message = str(message)
    lcd.message(message.replace('\\n','\n'))

def on_color_msg(client, topic, message):
    # Methoc called whenever user/feeds/reiley/color has a new value
    print("New message on topic {0}: {1} ".format(topic, message))
    led.color = eval(message)
    


# Connect to WiFi
print("Connecting to WiFi...")
wifi.connect()
print("Connected!")

# Initialize MQTT interface with the esp interface
MQTT.set_socket(socket, esp)

# Initialize a new MQTT Client object
mqtt_client = MQTT.MQTT(
    broker=secrets["mqtt_broker"],
    port=8883,
    username=secrets["mqtt_username"],
    password=secrets["mqtt_password"],
)

# Initialize an MQTT Client
io = IO_MQTT(mqtt_client)

# Connect the callback methods defined above to MQTT Broker
io.on_connect = connected
io.on_disconnect = disconnected
io.on_subscribe = subscribe

# Set up a callbacks
io.add_feed_callback("reiley/led", on_led_msg)
io.add_feed_callback("reiley/song", on_song_msg)
io.add_feed_callback("reiley/lcd", on_lcd_msg)
io.add_feed_callback("reiley/color", on_color_msg)

# Connect to Adafruit IO
print("Connecting to MQTT Broker...")
io.connect()

# Subscribe to all messages on the feeds
io.subscribe("reiley/led")
io.subscribe("reiley/song")
io.subscribe("reiley/lcd")
io.subscribe("reiley/color")

prv_refresh_time = 0.0
while True:
    # Poll for incoming messages
    try:
        io.loop()
    except (ValueError, RuntimeError) as e:
        print("Failed to get data, retrying\n", e)
        wifi.reset()
        wifi.connect()
        io.reconnect()
        continue
    # Send a new temperature reading to IO every 30 seconds
    if (time.monotonic() - prv_refresh_time) > 30:
        # take the cpu's temperature
        cpu_temp = cpu.temperature
        thermo_temp = thermo.temperature
        # truncate to two decimal points
        cpu_temp = str(cpu_temp)[:5]
        thermo_temp = str(thermo_temp)[:5]
        print("CPU temperature is %s degrees C" % cpu_temp)
        print("Thermistor temperature is %s degrees C" % thermo_temp)
        # publish it to io
        print("Publishing %s to temperature feed..." % cpu_temp)
        print("Publishing %s to thermo temp feed..." % thermo_temp)
        io.publish("reiley/temperature", cpu_temp)
        io.publish("reiley/thermotemp", thermo_temp)
        print("Published!")
        prv_refresh_time = time.monotonic()
    time.sleep(0.01)
