import network
import time
from secrets import WIFI_SSID, WIFI_PASSWORD
from machine import Pin

# Create the WiFi interface
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Connect to your network
wlan.connect(WIFI_SSID, WIFI_PASSWORD)

# Wait for connection
while not wlan.isconnected():
    time.sleep(1)
    print("Connecting...")
    
print("Connected")
print(wlan.ifconfig()) # Shows IP Address