Troubleshooting
===============

Flashing problems can be fiddly to troubleshoot. Try the suggestions
here if you're having problems:

Bootloader won't respond
------------------------

If you see errors like "Failed to connect" then your chip is probably
not entering the bootloader properly:

-  Check you are passing the correct serial port on the command line.
-  Check you have permissions to access the serial port, and other
   software (such as modem-manager on Linux) is not trying to interact
   with it. A common pitfall is leaving a serial terminal accessing this
   port open in another window and forgetting about it.
-  Check the chip is receiving 3.3V from a stable power source (see
   `Insufficient Power`_ for more details.)
-  Check that all pins are connected as described in `Entering the
   bootloader`_. Check the voltages at each pin with a multimeter,
   "high" pins should be close to 3.3V and "low" pins should be close to
   0V.
-  If you have connected other devices to GPIO pins mentioned above
   section, try removing them and see if esptool.py starts working.
-  Try using a slower baud rate (``-b 9600`` is a very slow value that
   you can use to verify it's not a baud rate problem.)

write_flash operation fails part way through
--------------------------------------------

If flashing fails with random errors part way through, retry with a
lower baud rate.

Power stability problems may also cause this (see `Insufficient
Power`_.)

write_flash succeeds but program doesn't run
--------------------------------------------

If esptool.py can flash your module with ``write_flash`` but your
program doesn't run, try the following:

Wrong Flash Mode
^^^^^^^^^^^^^^^^

Some devices only support the ``dio`` flash mode. Writing to flash with
``qio`` mode will succeed but the chip can't read the flash back to run
- so nothing happens on boot. Try passing the ``-fm dio`` option to
write_flash.

See the `SPI Flash Modes`_ wiki page for a full description of the flash
modes and how to determine which ones are supported on your device.

Insufficient Power
^^^^^^^^^^^^^^^^^^

The 3.3V power supply for the ESP8266 and ESP32 has to supply large
amounts of current (up to 70mA continuous, 200-300mA peak, slightly
higher for ESP32). You also need sufficient capacitance on the power
circuit to meet large spikes of power demand.

Insufficient Capacitance
''''''''''''''''''''''''

If you're using a pre-made development board or module then the built-in
power regulator & capacitors are usually good enough, provided the input
power supply is adequate.

*This is not true for some very simple pin breakout modules -*\ `similar
to this`_\ *. These breakouts do not integrate enough capacitance to
work reliably without additional components.*. Surface mount OEM modules
like ESP-WROOM02 and ESP-WROOM32 require an external bulk capacitor on
the PCB to be reliable, consult the module datasheet.

Power Supply Rating
'''''''''''''''''''

It is possible to have a power supply that supplies enough current for
the serial bootloader stage with esptool.py, but not enough for normal
firmware operation. You may see the 3.3V VCC voltage droop down if you
measure it with a multimeter, but you can have problems even if this
isn't happening.

Try swapping in a 3.3V supply with a higher current rating, add
capacitors to the power line, and/or shorten any 3.3V power wires.

The 3.3V output from FTDI FT232R chips/adapters or Arduino boards *do
not* supply sufficient current to power an ESP8266 or ESP32 (it may seem
to work sometimes, but it won't work reliably). Other USB TTL/serial
adapters may also be marginal.

Missing bootloader
^^^^^^^^^^^^^^^^^^

Recent ESP8266 SDKs and the ESP32 ESP-IDF both use a small firmware
bootloader program. The hardware bootloader in ROM loads this firmware
bootloader from flash, and then it runs the program. On ESP8266.
firmware bootloader image (with a filename like ``boot_v1.x.bin``) has
to be flashed at offset 0. If the firmware bootloader is missing then
the ESP8266 will not boot. On ESP32, the bootloader image should be
flashed by ESP-IDF at offset 0x1000.

Refer to SDK or ESP-IDF documentation for details regarding which
binaries need to be flashed at which offsets.

SPI Pins which must be disconnected
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Compared to the ROM bootloader that esptool.py talks to, a running
firmware uses more of the chip's pins to access the SPI flash.

If you set "Quad I/O" mode (``-fm qio``, the esptool.py default) then
GPIOs 7, 8, 9 & 10 are used for reading the SPI flash and must be
otherwise disconnected.

If you set "Dual I/O" mode (``-fm dio``) then GPIOs 7 & 8 are used for
reading the SPI flash and must be otherwise disconnected.

Try disconnecting anything from those pins (and/or swap to Dual I/O mode
if you were previously using Quad I/O mode but want to attach things to
GPIOs 9 & 10). Note that if GPIOs 9 & 10 are also connected to input
pins on the SPI flash chip, they may still be unsuitable for use as
general purpose I/O.

In addition to these pins, GPIOs 6 & 11 are also used to access the SPI
flash (in all modes). However flashing will usually fail completely if
these pins are connected incorrectly.

Early stage crash
-----------------

Use a `serial terminal program`_ to view the boot log. (ESP8266 baud
rate is 74880bps, ESP32 is 115200bps). See if the program is crashing
during early startup or outputting an error message.

.. _serial terminal program: #serial-terminal-programs

.. _Insufficient Power: #insufficient-power
.. _Entering the bootloader: #entering-the-bootloader
.. _SPI Flash Modes: https://github.com/espressif/esptool/wiki/SPI-Flash-Modes
.. _similar to this: https://user-images.githubusercontent.com/205573/30140831-9da417a6-93ba-11e7-95c3-f422744967de.jpg