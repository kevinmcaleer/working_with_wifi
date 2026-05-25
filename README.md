# Arduino IoT Cloud + MicroPython + BME280

Publish temperature, humidity, and pressure from a BME280 sensor to the
[Arduino IoT Cloud](https://cloud.arduino.cc/) from a MicroPython device
(e.g. Raspberry Pi Pico W, ESP32).

## Hardware

- A MicroPython-capable board with Wi-Fi
- A BME280 sensor wired over I2C:
  - `SDA` → GPIO 4
  - `SCL` → GPIO 5
  - `VCC` → 3V3
  - `GND` → GND

Adjust the `SDA` / `SCL` pins in `main.py` to match your wiring.

## Files

| File | Purpose |
| --- | --- |
| `main.py` | Connects to Wi-Fi, syncs NTP time, reads BME280, publishes to Arduino IoT Cloud |
| `just_wifi.py` | Minimal Wi-Fi connect example (useful for sanity checking the network) |
| `install_requirements.py` | Connects to Wi-Fi and `mip`-installs the required packages on the device |
| `bmetest.py` | Standalone BME280 read loop, no cloud |
| `bme280_float.py` | BME280 driver (floating-point variant) |
| `arduino_iot_cloud` | The Arduino IoT Cloud Python client |

## Setup

### 1. Create the cloud Thing

In the [Arduino IoT Cloud](https://cloud.arduino.cc/things) dashboard, create a
Thing with three variables that match the names in `main.py`:

- `temperature` (float)
- `humidity` (float)
- `pressure` (int)

Note the **Device ID** and **Secret Key** shown when you associate a device.

### 2. Add your secrets

Create a `secrets.py` file next to `main.py` (it is `.gitignore`d — do not commit it):

```python
WIFI_SSID = "your-wifi-ssid"
WIFI_PASSWORD = "your-wifi-password"
DEVICE_ID = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
SECRET_KEY = "your-arduino-iot-cloud-secret-key"
```

### 3. Copy the code to the device

Copy the following onto the board (e.g. via Thonny, `mpremote`, or `rshell`):

- `main.py`
- `bme280_float.py`
- `secrets.py`
- `arduino_iot_cloud/` (as `arduino_iot_cloud/` on the device)

### 4. Install the required MicroPython packages

Run `install_requirements.py` once on the device to `mip`-install the
dependencies (`logging`, `cbor2`, `senml`, `umqtt.simple`, `umqtt.robust`).

### 5. Run

Reset the board. `main.py` will:

1. Connect to Wi-Fi
2. Sync time via NTP (required for TLS to the Arduino IoT Cloud broker)
3. Read the BME280 every second
4. Publish `temperature`, `humidity`, and `pressure` to the cloud

## Troubleshooting

- **TLS handshake failures** — usually means the clock isn't set. `main.py`
  tries several NTP servers; if all fail, check outbound UDP/123.
- **`MQTTException`** — verify `DEVICE_ID` and `SECRET_KEY`, and that the
  Thing's variables are named exactly `temperature`, `humidity`, `pressure`.
- **Sensor reads zero / errors** — confirm the BME280 address and wiring;
  run `bmetest.py` to isolate from the cloud code.
