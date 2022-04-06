###################
## CONFIGURATION ##
###################
# BLINKA_MCP2221 needs to be 1
# BLINKA_MCP2221_RESET_DELAY value should be -1 in Windows 11, you can try 0.5 or higher if getting errors
# lux_range is your preferred brightness vs ambient light config, (lux_start, lux_end, increament_by): brightness
# "average_lux_count" is amount of seconds to hold lux values before taking average
# display_id is your monitor's ID, primary monitor is 0 and is set by default
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
    "average_lux_count": 10,
    "display_id": 0
}
################
## END CONFIG ##
################

import os, threading, time, datetime, screen_brightness_control, sys

def getscript(script):
    if(initial_run):
        return script.replace("\\","\\\\")
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
        print("exception during connect_device..", e)
        restart(5)

def connect_sensor():
    try:
        import adafruit_tsl2591
        return adafruit_tsl2591
    except Exception as e:
        print("exception during connect_sensor..", e)
        restart(5)

def get_sensor_value():
    board_i2c = connect_device()
    sensor = connect_sensor()
    try:
        sensor_values = sensor.TSL2591(board_i2c)
        return sensor_values
    except Exception as e:
        print("exception during get_sensor_value..", e)
        restart(5)

def generate_value_array(delay, run_event, sensor):
    while run_event.is_set():
        try:
            values.pop(0)
            values.append(int(float(sensor.lux)))
            time.sleep(delay)
        except Exception as e:
            print("exception during generate_value_array..", e)
            restart(5)

def average(lst):
    return int(round(sum(lst) / len(lst)))

def get_brightness():
    try:
        return screen_brightness_control.get_brightness(display=config["display_id"])[0]
    except Exception as e:
        print("exception during get_brightness..", e)
        print("re-trying in 1 second")
        time.sleep(1)
        get_brightness()

def set_brightness(brvalue):
    global cb
    try:
        screen_brightness_control.fade_brightness(brvalue, cb, display=config["display_id"], blocking=False)
        cb = brvalue
    except Exception as e:
        print("exception during set_brightness..", e)
        print("re-trying in 1 second")
        time.sleep(1)
        set_brightness(brvalue)

def print_status(argument):
    print("\x1B[33;40m" + datetime.datetime.today().strftime("%I:%M:%S%p") + "\x1B[0m Average Lux is {0}, brightness is set to {1}%.".format(argument[0], argument[1]))

def switcher(argument):
    for key in config["lux_range"]:
        if type(key) is range and argument in key and cb != config["lux_range"][key]:
            print_status([argument, config["lux_range"][key]])
            set_brightness(config["lux_range"][key])

if __name__ == "__main__":
    os.system("cls")
    initial_run = 1
    script = sys.argv[0]
    os.environ["BLINKA_MCP2221"] = config["BLINKA_MCP2221"]
    os.environ["BLINKA_MCP2221_RESET_DELAY"] = config["BLINKA_MCP2221_RESET_DELAY"]
    print("\x1B[33;40mgithub.com/nickGermi/monitor-brightness-manager\nMonitor Brightness Manager v0.5\nI2C converter: MCP2221A\nLight sensor: TSL2591\n\n\x1B[0m")
    cb = get_brightness()
    sensor = get_sensor_value()
    lux = int(float(sensor.lux))
    values = [lux] * config["average_lux_count"]
    run_event = threading.Event()
    run_event.set()
    sensor_values = threading.Thread(target=generate_value_array, args=(1, run_event, sensor))
    sensor_values.start()
    print_status([lux, cb])
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
