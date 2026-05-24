import network
import time
from secrets import WIFI_SSID, WIFI_PASSWORD

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

def install_packages():
    import mip
    packages = [
        "logging",
        "cbor2",
        "senml",
        "umqtt.simple",
        "umqtt.robust",
    ]

    for pkg in packages:
        try:
            print(f"Installing {pkg}...")
            mip.install(pkg)
        except Exception as e:
            print(f"  Failed: {e}")

install_packages()

