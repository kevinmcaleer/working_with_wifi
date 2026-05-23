import network
from time import sleep, ticks_ms, ticks_diff
from secrets import WIFI_SSID, WIFI_PASSWORD, DEVICE_ID, SECRET_KEY
import ntptime
import logging
from machine import Pin, I2C
from bme280_float import *
from arduino_iot_cloud import ArduinoCloudClient

# Setup BME280 sensor
SDA=4
SCL=5
i2c=I2C(0,sda=SDA,scl=SCL)
bme280 = BME280(i2c=i2c)

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Create the WiFi interface
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_SSID, WIFI_PASSWORD)

# Wait for connection
while not wlan.isconnected():
    time.sleep(1)
    print("Connecting...")
    
print("Connected")
print(wlan.ifconfig()) # Shows IP Address

# Sync time via NTP with retries and fallback servers
def sync_time():
    servers = [
        "pool.ntp.org",
        "time.google.com",
        "time.cloudflare.com",
        "uk.pool.ntp.org",  # closer to you in the UK
    ]
    for server in servers:
        try:
            ntptime.host = server
            print(f"Trying NTP server: {server}")
            ntptime.settime()
            print(f"✓ Time synced via {server}")
            print(f"Current UTC time: {time.localtime()}")
            return True
        except Exception as e:
            print(f"  Failed: {e}")
    return False

if not sync_time():
    print("⚠️ NTP sync failed - TLS will likely fail")

# 1. Create a client object, which is used to connect to the IoT cloud and link local
# objects to cloud objects. Note a username and password can be used for basic authentication
# on both CPython and MicroPython. For more advanced authentication methods, please see the examples.
client = ArduinoCloudClient(device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY, sync_mode=True)

# 2. Register cloud objects.
# Note: The following objects must be created first in the dashboard and linked to the device.
# When the switch is toggled from the dashboard, the on_switch_changed function is called with
# the client object and new value args.

client.register("temperature", value=None)
client.register("humidity", value=None)
client.register("pressure", value=None)

# 3. Start the Arduino cloud client.
client.start()

last_update = ticks_ms()
update_interval = 5 # Update every 5 seconds

while True:
    try:
        current_time = ticks_ms()
        
        # Update sensors at regular intervals
        if ticks_diff(current_time, last_update) >= update_interval * 1000:
            temperature, pressure, humidity = bme280.read_compensated_data()
            print(f"temperature is: {temperature}, humidity is: {humidity}, pressure is: {pressure}")
            client['temperature'] = round(temperature, 1)
            client['humidity'] = humidity
            client['pressure'] = pressure // 100
            print(f"Updated: Temp={temperature:.1f}°C")
            last_update = current_time
            
        # keep the client running (process callbacks)
        client.update()
        sleep(0.1)
        
    except Exception as e:
        print(f"Error: {e}")
        sleep(3)