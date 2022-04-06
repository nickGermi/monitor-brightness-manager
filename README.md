# monitor-brightness-manager

## Automatically adjust monitor brightness based on ambient light on a Windows PC using inexpensive hardware that you'll be building yourself!

* No coding or programming skills required
* No soldering
* Inexpensive plug-n-play hardware

### Hardware you'll need to get
* [Adafruit MCP2221A](https://www.adafruit.com/product/4471)
* [Adafruit TSL2591](https://www.adafruit.com/product/1980)
* [STEMMA QT 50mm cable](https://www.adafruit.com/product/4399)
* [Black Nylon Machine Screw and Stand-off Set – M2.5 Thread](https://www.adafruit.com/product/3299) `optional`
* USB C cable to connect to your computer
* Monitor with DDC/CI capabilities (most modern monitors)
* PC

![hardware screenshot](https://github.com/nickGermi/monitor-brightness-manager/raw/main/mcp2221a-tsl2591.jpg)

### Software requirements

* [Python 3.x](https://www.python.org/downloads/)
* [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

#### After installing Python and C++ Build Tools, you'll need to install following Python libraries

* screen_brightness_control
* setuptools
* hidapi
* adafruit-blinka
* adafruit_tsl2591

##### To install above libraries in command prompt execute following commands:
```
pip3 install --upgrade screen_brightness_control
pip3 install --upgrade setuptools
pip3 install --upgrade hidapi
pip3 install --upgrade adafruit-blinka
pip3 install --upgrade adafruit_tsl2591
```

### Script Configuration
Download monitor_brightness_manager.py file and edit it in a notepad or editor of your choice and edit following as you see fit and save the file:
```
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
```
* `BLINKA_MCP2221` needs to be `1`, this is required by BLINKA library
* `BLINKA_MCP2221_RESET_DELAY` value should be `-1` for Windows 11, you can try `0.5` or higher if getting errors
* `lux_range` this is where you can configure what brightness should your monitor use based on what ambient light condition, values are: (`lux_start`, `lux_end`, `increament_by`): `brightness`. For example, first one defines for ambient light value (lux) between 0 and 25, set brightness to 10%.
* `average_lux_count` is amount of seconds to hold lux values before taking average of, if your monitor's brightness is changing too slow or too rapidly, adjust this value. Lower value will cause brightness to change more rapidly, higher value will make it slower.

### Usage

To run the script, in command prompt enter:
```
python monitor_brightness_manager.py
```

If you've saved the file in `C:\` drive, you'll need to execute the command as `python C:\monitor_brightness_manager.py`

## Demo

![demo gif](https://github.com/nickGermi/monitor-brightness-manager/raw/main/demo.gif)

## Troubleshooting, additional references & information

* [Setting up MCP2221A](https://learn.adafruit.com/circuitpython-libraries-on-any-computer-with-mcp2221/windows)
* [Screen brightness control library used in this script](https://pypi.org/project/screen-brightness-control/)
* [C++ based monitor configuration utility, for example you can also change contrast](https://github.com/scottaxcell/winddcutil?msclkid=4472c115b29411eca79cd7052c4b75a4)
* On an older monitor that I tested (Dell U2312HM which is more than 10 years old), changing contrast has a better effect than changing brightness
* Script will restart itself after 5 seconds if it encounters any issues

## License

[MIT License](https://github.com/nickGermi/monitor-brightness-manager/blob/main/LICENSE)
