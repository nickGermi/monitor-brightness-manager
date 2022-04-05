import os, threading, time, datetime, screen_brightness_control, sys

###################
## CONFIGURATION ##
###################
# BLINKA_MCP2221 needs to be 1
# BLINKA_MCP2221_RESET_DELAY value should be -1 in Windows 11, you can try 0.5 or higher if getting errors
# Define your preferred range here (lux_start, lux_end, increament_by): brightness
# "average_lux_count" is amount of seconds to hold lux values before taking average
config = {
    "BLINKA_MCP2221": "1",
    "BLINKA_MCP2221_RESET_DELAY": "-1",
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
    "average_lux_count": 10
}
################
## END CONFIG ##
################

def getscript(script):
    if(initial_run):
        return script.replace('\\','\\\\')
    else:
        return script

def restart(delay):
    while delay in range(delay, 0, -1):
        print("Restarting script in "+str(delay)+" seconds", end="\r")
        delay=delay-1
        time.sleep(1)
    os.system("Python " + script)

def connect_device():
    try:
        import board
        time.sleep(1)
        return board.I2C()
    except Exception as e:
        print('exception during connect_device..', e)
        restart(5)

def connect_sensor():
    try:
        import adafruit_tsl2591
        return adafruit_tsl2591
    except Exception as e:
        print('exception during connect_sensor..', e)
        restart(5)

def get_sensor_values():
    board_i2c = connect_device()
    sensor = connect_sensor()
    try:
        sensor_values = sensor.TSL2591(board_i2c)
        return sensor_values
    except Exception as e:
        print('exception during get_sensor_values..', e)
        restart(5)

def generate_value_array(delay, run_event, sensor):
    while run_event.is_set():
        try:
            if sensor.lux:
                if isinstance(sensor.lux, float):
                    if sensor.lux > 0:
                        if (len(values) >= config["average_lux_count"]):
                            values.pop(0)
                        values.append(int(sensor.lux))
                        time.sleep(delay)
        except Exception as e:
            print('exception during generate_value_array..', e)
            restart(5)


def average(lst):
    return int(round(sum(lst) / len(lst)))

# Gets brightness of primary monitor (display=0), to set to a different monitor
# use screen_brightness_control.get_brightness(display=1)[0]
def get_brightness():
    try:
        return screen_brightness_control.get_brightness()[0]
    except Exception as e:
        print('exception during get_brightness..', e)
        print('re-trying in 1 second')
        time.sleep(1)
        get_brightness()

# Sets brightness of primary monitor, to set to a different monitor
# use screen_brightness_control.set_brightness(brvalue, display=1)
def set_brightness(brvalue):
    global cb
    try:
        screen_brightness_control.set_brightness(brvalue)
        cb = brvalue
    except Exception as e:
        print('exception during set_brightness..', e)
        print('re-trying in 1 second')
        time.sleep(1)
        set_brightness(brvalue)

def switcher(argument):
    for key in config["lux_range"]:
        if type(key) is range and argument in key and cb != config["lux_range"][key]:
            print(CSI + "33;40m" + datetime.datetime.today().strftime("%H:%M:%S%p") + CSI + "0m Last {0} seconds average Lux is {1} setting brightness to {2}%".format(config["average_lux_count"], argument, config["lux_range"][key]))
            set_brightness(config["lux_range"][key])

def print_initial_status(args):
    if(args[0] and args[1] > 0):
        print(CSI + "33;40m" + datetime.datetime.today().strftime("%H:%M:%S%p") + CSI + "0m Current brightness is set to {0}% and current lux is {1}.".format(args[0], int(round(float(args[1])))))
    else:
        print('could not get initial value, re-trying in 1 second')
        time.sleep(1)
        print_initial_status(args)

if __name__ == '__main__':
    os.system('cls')
    initial_run = 1
    script = sys.argv[0]
    os.environ['BLINKA_MCP2221'] = config["BLINKA_MCP2221"]
    os.environ['BLINKA_MCP2221_RESET_DELAY'] = config["BLINKA_MCP2221_RESET_DELAY"]
    CSI = "\x1B["
    scriptheader = """┌────────────────────────────────────────┐
│  Monitor Brightness Manager v0.3       │
│  Light sensor: TSL2591                 │
│  USB 2.0 to I2C converter: MCP2221A    │
└────────────────────────────────────────┘"""
    print(CSI + "33;40m" + scriptheader + CSI + "0m")
    values = []
    cb = 0
    average_lux = 0
    sensor = get_sensor_values()
    run_event = threading.Event()
    run_event.set()
    sensor_values = threading.Thread(target=generate_value_array, args=(1, run_event, sensor))
    sensor_values.start()
    cb = get_brightness()
    print_initial_status([cb, sensor.lux])
    try:
        while True:
            if (len(values) > 0):
                switcher(average(values))
            time.sleep(1)
    except KeyboardInterrupt:
        print("Attempting to close threads..")
        run_event.clear()
        sensor_values.join()
        print("Threads successfully closed.")
