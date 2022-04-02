# monitor-brightness-manager
Automatically adjust monitor brightness based on ambient light on a Windows PC

Hardware
- Adafruit MCP2221A (https://www.adafruit.com/product/4471)
- Adafruit TSL2591 (https://www.adafruit.com/product/1980)
- STEMMA QT 50mm cable (https://www.adafruit.com/product/4399)
- USB C cable to connect to your computer
- Monitor with DDC/CI capabilities (most modern monitors)
- PC

Optional hardware:
- Black Nylon Machine Screw and Stand-off Set – M2.5 Thread (https://www.adafruit.com/product/3299)

![hardware screenshot](https://github.com/nickGermi/monitor-brightness-manager/raw/main/mcp2221a-tsl2591.jpg)

Software requirements:
- Python 3.x
- Windows 11 (On other versions of Windows you might have to adjust `BLINKA_MCP2221_RESET_DELAY` value setting it to `0.5` or higher)
- Microsoft Visual C++ 14.0 or greater (You can get this by installing Microsoft Visual Studio and installing Build Tools for Visual Studio 2019)

Python libraries:
- screen_brightness_control
- setuptools
- hidapi
- adafruit-blinka
- adafruit_tsl2591

To install above libraries use pip3 which comes with Python 3.x installation, for example, in command prompt execute:

`pip3 install --upgrade screen_brightness_control`

To run the script, in command prompt execute:

`python mc2221a.py`

Demo:

![demo gif](https://github.com/nickGermi/monitor-brightness-manager/raw/main/demo.gif)
