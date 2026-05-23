#
# Example. Using I2C at P9, P10
#
from machine import I2C, Pin
from bme280_float import *
from utime import sleep

SDA=Pin(4)
SCL=Pin(5)

i2c=I2C(0,sda=SDA,scl=SCL)

bme280 = BME280(i2c=i2c)

while True:
    print(bme280.values)
    sleep(1)

