import os
# board needs this
os.environ['BLINKA_MCP2221'] = "1"
# if can't connect to board, change this value to 0.5 or higher
os.environ['BLINKA_MCP2221_RESET_DELAY'] = "-1"

# Define your preferred range here
# if lux within range of 0-25 increament by 1 then set to 10% brightness
# average_lux_count is amount of seconds to hold lux values
config = {
    "lux_range": {
        range(0, 25, 1): 10,
        range(25, 50, 1): 20,
        range(50, 100, 1): 30,
        range(100, 150, 1): 40,
        range(150, 200, 1): 50,
        range(200, 250, 1): 60,
        range(250, 300, 1): 70,
        range(300, 350, 1): 80,
        range(350, 400, 1): 90,
        range(400, 5500, 1): 100
    },
    "average_lux_count": 15
}

import threading
import board
import adafruit_tsl2591
import time
from datetime import datetime
import screen_brightness_control

def connect_sensor():
    global sensor
    i2c = board.I2C()
    try:
        sensor = adafruit_tsl2591.TSL2591(i2c)
        pass
    except:
        print("can't connect")
    return sensor

def generate_value_array(delay, run_event, sensor):
    while run_event.is_set():
        lux = sensor.lux
        if isinstance(lux, float):
            if lux > 0:
                if (len(values) >= config["average_lux_count"]):
                    values.pop(0)
                values.append(int(lux))
        time.sleep(delay)

def average(lst):
    return int(round(sum(lst) / len(lst)))

# Gets brightness of primary monitor (display=0), to set to a different monitor
# use screen_brightness_control.get_brightness(display=1)[0]
# refer to https://pypi.org/project/screen-brightness-control/
def get_brightness():
    return screen_brightness_control.get_brightness()[0]

# Sets brightness of primary monitor, to set to a different monitor
# use screen_brightness_control.set_brightness(brvalue, display=1)
# refer to https://pypi.org/project/screen-brightness-control/
def set_brightness(brvalue):
    global cb
    screen_brightness_control.set_brightness(brvalue)
    cb = brvalue

def switcher(argument):
    for key in config["lux_range"]:
        if type(key) is range and argument in key and cb != config["lux_range"][key]:
            print(CSI + "90;40m " + datetime.today().strftime("%I:%M%p") + CSI + "0m Last {0} seconds average Lux is {1} setting brightness to {2}%".format(config["average_lux_count"], argument, config["lux_range"][key]))
            set_brightness(config["lux_range"][key])

if __name__ == '__main__':
    os.system('cls')
    CSI = "\x1B["
    scriptheader = """
 ┌────────────────────────────────────────┐
 │     $$\   $$\ $$$$$$\ $$\   $$\        │
 │     $$$\  $$ |\_$$  _|$$ |  $$ |       │
 │     $$$$\ $$ |  $$ |  \$$\ $$  |       │
 │     $$ $$\$$ |  $$ |   \$$$$  /        │
 │     $$ \$$$$ |  $$ |   $$  $$<         │
 │     $$ |\$$$ |  $$ |  $$  /\$$\        │
 │     $$ | \$$ |$$$$$$\ $$ /  $$ |       │
 │     \__|  \__|\______|\__|  \__|       │
 ├────────────────────────────────────────┤
 │  Monitor Brightness Manager v0.2       │
 │  Light sensor: TSL2591                 │
 │  USB 2.0 to I2C converter: MCP2221A    │
 └────────────────────────────────────────┘"""
    print(CSI + "33;40m" + scriptheader + CSI + "0m")
    values = []
    cb = 0
    average_lux = 0
    sensor = connect_sensor()
    run_event = threading.Event()
    run_event.set()
    sensor_values = threading.Thread(target=generate_value_array, args=(0.5, run_event, sensor))
    sensor_values.start()
    cb = get_brightness()
    print(CSI + "90;40m " + datetime.today().strftime("%I:%M%p") + CSI + "0m Current brightness is set to {0}% and average lux is {1}.".format(cb, average(values)))
    try:
        while True:
            if (len(values) > 0):
                switcher(average(values))
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nAttempting to close threads..")
        run_event.clear()
        sensor_values.join()
        print("Threads successfully closed.")
