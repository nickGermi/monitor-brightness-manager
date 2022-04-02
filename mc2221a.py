import os
os.environ['BLINKA_MCP2221'] = "1"
os.environ['BLINKA_MCP2221_RESET_DELAY'] = "-1"

import threading
import board
import adafruit_tsl2591
import time
import screen_brightness_control

values = []
cb = 0
average_lux = 0
sensor = object

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
                if (len(values) > 9 ):
                    values.pop(0)
                values.append(int(lux))
        time.sleep(delay)

def average(lst):
    return int(round(sum(lst) / len(lst)))

def get_brightness():
    return screen_brightness_control.get_brightness()[0]

def set_brightness(brvalue):
    global cb
    screen_brightness_control.set_brightness(brvalue)
    cb = brvalue

def calculate():
    global cb
    global average_lux
    cbstr = str(cb)+"%"
    CSI = "\x1B["
    print(CSI+"37;40m" + "Brightness is", cbstr, "and Lux is", average_lux, "        " + CSI + "0m", end = "\r")
    if (average_lux in range(0, 25, 1)):
        if (cb != 10):
            set_brightness(10)
        return
    if (average_lux in range(25, 50, 1)):
        if (cb != 20):
            set_brightness(20)
        return
    if (average_lux in range(50, 100, 1)):
        if (cb != 30):
            set_brightness(30)
        return
    if (average_lux in range(100, 150, 1)):
        if (cb != 40):
            set_brightness(40)
        return
    if (average_lux in range(150, 200, 1)):
        if (cb != 50):
            set_brightness(50)
        return
    if (average_lux in range(200, 250, 1)):
        if (cb != 60):
            set_brightness(60)
        return
    if (average_lux in range(250, 300, 1)):
        if (cb != 70):
            set_brightness(70)
        return
    if (average_lux in range(300, 350, 1)):
        if (cb != 80):
            set_brightness(80)
        return
    if (average_lux in range(350, 400, 1)):
        if (cb != 90):
            set_brightness(90)
        return
    if (average_lux in range(400, 5500, 1)):
        if (cb != 100):
            set_brightness(100)
        return
    else:
        print("lux is not in range!")

if __name__ == '__main__':
    os.system('cls')
    CSI = "\x1B["
    scriptheader = """      ___                       ___     
     /__/\        ___          /__/|    
     \  \:\      /  /\        |  |:|    
      \  \:\    /  /:/        |  |:|    
  _____\__\:\  /__/::\      __|__|:|    
 /__/::::::::\ \__\/\:\__  /__/::::\____
 \  \:\~~\~~\/    \  \:\/\    ~\~~\::::/
  \  \:\  ~~~      \__\::/     |~~|:|~~ 
   \  \:\          /__/:/      |  |:|   
    \  \:\         \__\/       |  |:|   
     \__\/                     |__|/    """
    print(CSI + "33;40m" + scriptheader + CSI + "0m")
    print(CSI + "90;40m" + "=========================================" + CSI + "0m")
    print(CSI + "90;40m" + "==  Auto DDC/CI brightness manager     ==" + CSI + "0m")
    print(CSI + "90;40m" + "==  Light sensor: TSL2591              ==" + CSI + "0m")
    print(CSI + "90;40m" + "==  Controller chip: MCP2221A          ==" + CSI + "0m")
    print(CSI + "90;40m" + "=========================================" + CSI + "0m")
    sensor = connect_sensor()
    run_event = threading.Event()
    run_event.set()
    sensor_values = threading.Thread(target=generate_value_array, args=(0.5, run_event, sensor))
    sensor_values.start()
    cb = get_brightness()
    try:
        while True:
            if (len(values) > 0):
                average_lux = average(values)
                calculate()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nAttempting to close threads..")
        run_event.clear()
        sensor_values.join()
        print("Threads successfully closed.")