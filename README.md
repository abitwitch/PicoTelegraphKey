# PicoTelegraphKey
Making a Striaght Telegraph Keyboard emulator using a Raspberry Pi Pico.

## Setup
1) Download and install Thonny `sudo apt install thonny`
2) Open Thonny with `sudo thonny`
3) Download and install Circuit Python onto the pico, by going (here) [https://circuitpython.org/board/raspberry_pi_pico/] and installing the latest stable release
4) Connect the Pico while holding BOOTSEL and copy over the UFC file. Restart the Pico
5) In Thonny select "Run > Select Interpreter > CircuitPython (generic)"
6) Go to (Adafruit's CircuitPython HID page) [https://github.com/adafruit/Adafruit_CircuitPython_HID]
7) Select a stable release under tags and download the "adafruit_hid" folder. Copy it to the "lib" folder on the Pico
8) Copy/overwrite both the "code.py" and "boot.py" files to the root level of the Pico
9) Connect your straight telegraph key from GP16 to 3V3(OUT).



