import board
import busio
import digitalio
from digitalio import DigitalInOut
import adafruit_scd30
import time
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
#import adafruit_sdcard
import microcontroller
import storage
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.roundrect import RoundRect
from adafruit_display_shapes.triangle import Triangle
from adafruit_display_shapes.line import Line
from adafruit_display_shapes.polygon import Polygon
import math
from analogio import AnalogIn
from adafruit_display_shapes.sparkline import Sparkline

import random
from adafruit_debouncer import Debouncer

vbat_voltage = AnalogIn(board.VOLTAGE_MONITOR)

def get_voltage(pin):
    return (pin.value * 3.3) / 65536 * 2


q1 = digitalio.DigitalInOut(board.A2)
q1.direction = digitalio.Direction.OUTPUT
q1.value = True

time.sleep(2)

button_A_pin = digitalio.DigitalInOut(board.A4)
button_A_pin.direction = digitalio.Direction.INPUT
button_A_pin.pull = digitalio.Pull.UP
button_A = Debouncer(button_A_pin)

button_B_pin = digitalio.DigitalInOut(board.A5)
button_B_pin.direction = digitalio.Direction.INPUT
button_B_pin.pull = digitalio.Pull.UP
button_B = Debouncer(button_B_pin)

scd = adafruit_scd30.SCD30(board.I2C())

import displayio
import terminalio
#import neopixel
from adafruit_display_text import label
import adafruit_displayio_ssd1306

displayio.release_displays()

i2c = board.I2C()
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)


time.sleep(1)

exception_count = 0
sample_recorded_count = 0

time_init=time.monotonic()

interval_seconds = 2

WIDTH = 128
HEIGHT = 64  # Change to 64 if needed
BORDER = 1

SCREEN = 0

font = terminalio.FONT

line_color = 0xFFFFFF

WHITE = 0x000000

chart_width = display.width - 40
chart_height = display.height - 10

sparkline1 = Sparkline(width=chart_width, height=chart_height, max_items=40, y_min=0, y_max=1000, x=35, y=5, color=line_color)

text_xoffset = -10
text_label1a = label.Label(
    font=font, text=str(sparkline1.y_top), color=line_color
)  # yTop label
text_label1a.anchor_point = (1, 0.5)  # set the anchorpoint at right-center
text_label1a.anchored_position = (
    sparkline1.x + text_xoffset,
    sparkline1.y,
)  # set the text anchored position to the upper right of the graph

text_label1b = label.Label(
    font=font, text=str(sparkline1.y_bottom), color=line_color
)  # yTop label
text_label1b.anchor_point = (1, 0.5)  # set the anchorpoint at right-center
text_label1b.anchored_position = (
    sparkline1.x + text_xoffset,
    sparkline1.y + chart_height,
)  # set the text anchored position to the upper right of the graph

text_label1c = label.Label(
    font=font, text=str(sparkline1.y_top // 2), color=line_color
)  # yTop label
text_label1c.anchor_point = (1, 0.5)  # set the anchorpoint at right-center
text_label1c.anchored_position = (
    sparkline1.x + text_xoffset,
    sparkline1.y + chart_height/2,
)  # set the text anchored posi


bounding_rectangle = Rect(
    sparkline1.x, sparkline1.y, chart_width, chart_height, outline=line_color
)

text_label1d = label.Label(
    font=font, text="---", color=line_color
)  # yTop label
text_label1d.anchor_point = (1, 0.5)  # set the anchorpoint at right-center
text_label1d.anchored_position = (
    #sparkline1.x + chart_width + text_xoffset,
    WIDTH * 4.5 // 5, 
    4 
)  # set the text anchored posi


# Create a group to hold the sparkline, text, rectangle and tickmarks
# append them into the group (my_group)
#
# Note: In cases where display elements will overlap, then the order the
# elements are added to the group will set which is on top.  Latter elements
# are displayed on top of former elemtns.
rad = 2 
posx = WIDTH - rad*2 
posy = rad*2 

circle = Circle(posx, posy, rad)
circle1 = Circle(posx,HEIGHT-posy,rad)
y_axis = Line(sparkline1.x,sparkline1.y,sparkline1.x,sparkline1.y+chart_height,color=line_color)
x_axis = Line(sparkline1.x,sparkline1.y+chart_height,sparkline1.x+chart_width,sparkline1.y+chart_height,color=line_color)

my_group = displayio.Group()

my_group.append(sparkline1)
my_group.append(text_label1a)
my_group.append(text_label1b)
my_group.append(text_label1c)
#my_group.append(text_label1d)
#my_group.append(bounding_rectangle)
my_group.append(y_axis)
#my_group.append(x_axis)
my_group.append(circle)

calibration_text = displayio.Group()
text="CALIBRATION"
calibration_label = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=20, y=15)
calibration_text.append(calibration_label)

big_text = displayio.Group()
text = "PVOS.ORG\nCO2 Monitor\nREV_W"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=20, y=15)
big_text.append(text_area)
batt_label = label.Label(
    font=font, text="", color=line_color
)  # yTop label
batt_label.anchor_point = (1, 0.5)  # set the anchorpoint at right-center
batt_label.anchored_position = (
    #sparkline1.x + chart_width + text_xoffset,
    WIDTH * 4.5 // 5, 
    4 
)  # set the text anchored posi
big_text.append(batt_label)
#big_text.append(circle1)

total_ticks = 2 

for i in range(total_ticks + 1):
    x_start = sparkline1.x - 5
    x_end = sparkline1.x
    y_both = int(round(sparkline1.y + (i * (chart_height) / (total_ticks))))
    if y_both > sparkline1.y + chart_height - 1:
        y_both = sparkline1.y + chart_height - 1
    my_group.append(Line(x_start, y_both, x_end, y_both, color=line_color))

# Set the display to show my_group that contains the sparkline and other graphics
display.show(my_group)
display.show(big_text)

#SCREEN = 0 # 0: big_text; 1: mygroup
time.sleep(1)
text_area.text=""
text_area.x=30
text_area.y=45
text_area.font=bitmap_font.load_font("/lib/Junction-regular-24.bdf")
#text_area.font=bitmap_font.load_font("/lib/LeagueSpartan-Bold-16.bdf")

DISPLAY_ON = 1

while True:

    button_A.update()
    button_B.update()
    """if button_B.fell:
        DISPLAY_ON= not DISPLAY_ON
        if(DISPLAY_ON):
            display.wake()
        else:
            display.sleep()"""
    if button_B.fell:
        calibration_label.text="CALIBRATION"
        display.show(calibration_text)
        calibration_index=6
        now = time.monotonic()  # Time in seconds since power on
        calibrated=False
        while(calibration_index>0):
            button_B.update()
            if button_B.fell:
                #calibration_label.text="Calibrating!"
                scd.forced_recalibration_reference=420
                calibrated=True
                calibration_label.text="Calibrated to 410 ppm"
                time.sleep(2)
                break
            if (now + 1) < time.monotonic(): # 1 second has elapsed
                now = time.monotonic()
                calibration_index=calibration_index-1
                calibration_label.text="Press again within\n"+str(calibration_index)+" seconds\nto calibrate!"
                if(calibration_index==0):
                    calibration_label.text="Cancelled."
                    time.sleep(2)            
        display.show(big_text)

    if button_A.fell:
        DISPLAY_ON = 1
        display.wake()
        SCREEN = not SCREEN 
        if(SCREEN==0):
            display.show(big_text)
        else:
            display.show(my_group)

    #w.feed()
    current_time = time.monotonic()-time_init 


    if (scd.data_available and ((current_time > interval_seconds) or sample_recorded_count < 1)):

        try:
            battery_voltage = get_voltage(vbat_voltage)
            batt_str = "{:.2f}V".format(battery_voltage)
            temp_str = "{:.0f}C".format(scd.temperature)
            humid_str = "{:.0f}RH".format(scd.relative_humidity)

            if (scd.CO2>1):
                print(round(scd.CO2))

                if(SCREEN==0):
                    #circle1.fill=line_color
                    #time.sleep(.05)
                    #circle1.fill=WHITE
                    display.auto_refresh = False
                    text_area.text=str(round(scd.CO2))
                    batt_label.text="  " + temp_str+"  " + humid_str + "  " + batt_str
                    sparkline1.add_value(round(scd.CO2))
                    display.auto_refresh = True

                else:
                    circle.fill=line_color
                #text_label1d.text="CO2_PPM:"+str(round(scd.CO2))
                    time.sleep(.1)
                    circle.fill=WHITE

                    display.auto_refresh = False
    
                    sparkline1.add_value(round(scd.CO2))
                
                    print(sparkline1.values())

                    max_co2 = max(sparkline1.values())
                    sparkline1.y_max = round(math.ceil(max_co2 / 1000.0) * 1000.0)
                    sparkline1.update()
                    text_label1a.text=str(sparkline1.y_top)
                    text_label1c.text=str(sparkline1.y_top // 2)
                    text_label1d.text="CO2: "+str(round(scd.CO2))

                    #text_label1d.text=batt_str+"  |  CO2: "+str(round(scd.CO2))
                    text_label1d.text="CO2: "+str(round(scd.CO2)) + "  |  " + batt_str

                    #sparkline1.add_value(random.uniform(0, 1000))
                    sparkline1.add_value(round(scd.CO2))
                    #co2_reading.text = str(round(scd.CO2))

                    #if(SCREEN==0):
                    #    display.show(big_text)
                    #else:
                    #    display.show(my_group)

                    display.auto_refresh = True

                    time.sleep(0.01)

                sample_recorded_count = sample_recorded_count + 1
                print(sample_recorded_count)
                time_init=time.monotonic()
                """ 
                if(sample_recorded_count % 10 == 0):
                    fet.value = False
                    display.sleep()
                    for i in range(0,10):
                        print("co2 off, display off")
                        time.sleep(1)
                    print ("co2 on, display on")
                    fet.value = True
                    display.wake()
                    time.sleep(1)
                    scd = adafruit_scd30.SCD30(board.I2C())
                    time.sleep(3)
                """

        except Exception as e:
            print("*** Exception: " + str(e))
            exception_count += 1
            # break
