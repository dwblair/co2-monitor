# SPDX-FileCopyrightText: 2020 by Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
import time
import board
import busio
import adafruit_scd30
import terminalio
from adafruit_display_text import bitmap_label

# SCD-30 has tempremental I2C with clock stretching, datasheet recommends
# starting at 50KHz
i2c = busio.I2C(board.SCL, board.SDA, frequency=50000)
scd = adafruit_scd30.SCD30(i2c)
scale = 2

text = "Starting up ..."
text_area = bitmap_label.Label(terminalio.FONT, text=text, scale=scale)
text_area.x = 10
text_area.y = 20
board.DISPLAY.show(text_area)

while True:
    # since the measurement interval is long (2+ seconds) we check for new data before reading
    # the values, to ensure current readings.
    if scd.data_available:
        text_area.scale=5
        #print("Data Available!")
        print("CO2: %d PPM" % scd.CO2)
        text_area.text=str(round(scd.CO2))
        #print("Temperature: %0.2f degrees C" % scd.temperature)
        #print("Humidity: %0.2f %% rH" % scd.relative_humidity)
        #print("")
        #print("Waiting for new data...")
        #print("")

    time.sleep(0.5)
