espefuse.py
===========

``espefuse.py`` is a tool for communicating with an Espressif chip and
reading/writing ("burning") the one-time-programmable efuses values.

.. warning::

    **IMPORTANT: Because efuse is one-time-programmable, it is possible to
    permanently damage or "brick" your ESP32 using this tool. Use it with
    great care.**

For more details about ESP32 efuse features, see the `Technical
Reference
Manual <http://espressif.com/en/support/download/documents>`__.

``espefuse.py`` is installed alongside ``esptool.py``, so if
``esptool.py`` (v2.0 or newer) is available on the PATH then
``espefuse.py`` should be as well.

Display efuse summary
---------------------

::

    espefuse.py --port /dev/ttyUSB1 summary

The options ``--port`` and ``--before`` can be supplied, and are
identical to the equivalent ``esptool.py`` options.

Output from the summary command will look like this:

::

    espefuse.py v2.6-beta1
    Connecting........_____.
    EFUSE_NAME             Description = [Meaningful Value] [Readable/Writeable] (Hex Value)
    ----------------------------------------------------------------------------------------
    Security fuses:
    FLASH_CRYPT_CNT        Flash encryption mode counter                     = 0 R/W (0x0)
    FLASH_CRYPT_CONFIG     Flash encryption config (key tweak bits)          = 0 R/W (0x0)
    CONSOLE_DEBUG_DISABLE  Disable ROM BASIC interpreter fallback            = 1 R/W (0x1)
    ABS_DONE_0             secure boot enabled for bootloader                = 0 R/W (0x0)
    ABS_DONE_1             secure boot abstract 1 locked                     = 0 R/W (0x0)
    JTAG_DISABLE           Disable JTAG                                      = 0 R/W (0x0)
    DISABLE_DL_ENCRYPT     Disable flash encryption in UART bootloader       = 0 R/W (0x0)
    DISABLE_DL_DECRYPT     Disable flash decryption in UART bootloader       = 0 R/W (0x0)
    DISABLE_DL_CACHE       Disable flash cache in UART bootloader            = 0 R/W (0x0)
    BLK1                   Flash encryption key
      = 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 R/W
    BLK2                   Secure boot key
      = 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 R/W
    BLK3                   Variable Block 3
      = 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 R/W

    Efuse fuses:
    WR_DIS                 Efuse write disable mask                          = 0 R/W (0x0)
    RD_DIS                 Efuse read disablemask                            = 0 R/W (0x0)
    CODING_SCHEME          Efuse variable block length scheme                = 0 R/W (0x0)
    KEY_STATUS             Usage of efuse block 3 (reserved)                 = 0 R/W (0x0)

    Config fuses:
    XPD_SDIO_FORCE         Ignore MTDI pin (GPIO12) for VDD_SDIO on reset    = 0 R/W (0x0)
    XPD_SDIO_REG           If XPD_SDIO_FORCE, enable VDD_SDIO reg on reset   = 0 R/W (0x0)
    XPD_SDIO_TIEH          If XPD_SDIO_FORCE & XPD_SDIO_REG, 1=3.3V 0=1.8V   = 0 R/W (0x0)
    SPI_PAD_CONFIG_CLK     Override SD_CLK pad (GPIO6/SPICLK)                = 0 R/W (0x0)
    SPI_PAD_CONFIG_Q       Override SD_DATA_0 pad (GPIO7/SPIQ)               = 0 R/W (0x0)
    SPI_PAD_CONFIG_D       Override SD_DATA_1 pad (GPIO8/SPID)               = 0 R/W (0x0)
    SPI_PAD_CONFIG_HD      Override SD_DATA_2 pad (GPIO9/SPIHD)              = 0 R/W (0x0)
    SPI_PAD_CONFIG_CS0     Override SD_CMD pad (GPIO11/SPICS0)               = 0 R/W (0x0)
    DISABLE_SDIO_HOST      Disable SDIO host                                 = 0 R/W (0x0)

    Identity fuses:
    MAC                    MAC Address
      = 30:ae:a4:c3:86:94 (CRC 99 OK) R/W
    CHIP_VER_REV1          Silicon Revision 1                                = 1 R/W (0x1)
    CHIP_VERSION           Reserved for future chip versions                 = 2 R/W (0x2)
    CHIP_PACKAGE           Chip package identifier                           = 1 R/W (0x1)

    Calibration fuses:
    BLK3_PART_RESERVE      BLOCK3 partially served for ADC calibration data  = 0 R/W (0x0)
    ADC_VREF               Voltage reference calibration                     = 1093 R/W (0x11)

    Flash voltage (VDD_SDIO) determined by GPIO12 on reset (High for 1.8V, Low/NC for 3.3V).

On relatively new chip, most efuses are unburned (value 0).

In espefuse.py v2.6 and newer, read-protected efuse values are displayed
as question marks (??). On earlier versions, they are displayed as
zeroes.

For details on the meaning of each efuse value, refer to the Technical
Reference Manual.

Dump raw efuse registers
------------------------

To display raw efuse register values, use the ``dump`` subcommand:

::

    espefuse.py --port /dev/ttyUSB1 dump
    espefuse.py v2.0-dev
    Connecting....
    EFUSE block 0:
    00000000 c40042xx xxxxxxxx 00000000 00000033 00000000 00000000
    EFUSE block 1:
    00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000
    EFUSE block 2:
    00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000
    EFUSE block 3:
    00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000

Output corresponds directly to efuse register values in the `register
space <https://github.com/espressif/esp-idf/blob/master/components/soc/esp32/include/soc/efuse_reg.h#L19>`__.

Burning an efuse
----------------

**This command can brick your ESP32**

To burn an efuse to a new value, use the ``burn_efuse`` command:

::

    espefuse.py --port /dev/DONOTDOTHIS burn_efuse JTAG_DISABLE 1

The arguments to ``burn_efuse`` are the name of the efuse (as shown in
summary output) and the new value.

New values can be a numeric value in decimal or hex (with 0x prefix).
Efuse bits can only be burned from to 0 to 1, attempting to set any back
to 0 will have no effect. Most efuses have a limited bit width (many are
only 1-bit flags).

Longer efuses (MAC addresses, keys) cannot be set via this command.

By default, ``espefuse.py`` will ask you to type BURN before it
permanently sets an efuse. The ``--do-not-confirm`` option allows you to
bypass this.

Setting Flash Voltage (VDD\_SDIO)
---------------------------------

After reset, the default ESP32 behaviour is to enable and configure the
flash voltage regulator (VDD\_SDIO) based on the level of the MTDI pin
(GPIO12).

The default behaviour on reset is:

+----------------------+--------------------------------+
| MTDI (GPIO12) Pin    | VDD\_SDIO Internal Regulator   |
+======================+================================+
| Low or unconnected   | Enabled at 3.3V                |
+----------------------+--------------------------------+
| High                 | Enabled at 1.8V                |
+----------------------+--------------------------------+

Consult ESP32 Technical Reference Manual chapter 4.8.1 "VDD\_SDIO Power
Domain" for details.

A combination of 3 efuses (``XPD_SDIO_FORCE``, ``XPD_SDIO_REG``,
``XPD_SDIO_TIEH``) can be burned in order to override this behaviour and
disable VDD\_SDIO regulator, or set it to a fixed voltage. These efuses
can be burned with individual ``burn_efuse`` commands, but the
``set_flash_voltage`` command makes it easier:

Disable VDD\_SDIO regulator
^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    espefuse.py set_flash_voltage OFF

Once set: \* VDD\_SDIO regulator always disabled. \* MTDI pin (GPIO12)
is ignored. \* Flash must be powered externally and voltage supplied to
VDD\_SDIO pin of ESP32. \* Efuse ``XPD_SDIO_FORCE`` is burned.

Fixed 1.8V VDD\_SDIO
^^^^^^^^^^^^^^^^^^^^

::

    espefuse.py set_flash_voltage 1.8V

Once set: \* VDD\_SDIO regulator always enables at 1.8V. \* MTDI pin
(GPIO12) is ignored. \* External voltage should not be supplied to
VDD\_SDIO. \* Efuses ``XPD_SDIO_FORCE`` and ``XPD_SDIO_REG`` are burned.

Fixed 3.3V VDD\_SDIO
^^^^^^^^^^^^^^^^^^^^

::

    espefuse.py set_flash_voltage 3.3V

Once set: \* VDD\_SDIO regulator always enables at 3.3V. \* MTDI pin
(GPIO12) is ignored. \* External voltage should not be supplied to
VDD\_SDIO. \* Efuses ``XPD_SDIO_FORCE``, ``XPD_SDIO_REG``,
``XPD_SDIO_TIEH`` are burned.

Subsequent changes
^^^^^^^^^^^^^^^^^^

Once an efuse is burned it cannot be un-burned. However, changes can be
made by burning additional efuses:

-  ``set_flash_voltage OFF`` can be changed to ``1.8V`` or ``3.3V``.
-  ``set_flash_voltage 1.8V`` can be changed to ``3.3V``

Burning a key
-------------

**This command can brick your ESP32**

The efuse key blocks BLK1, BLK2 and BLK3 can all hold encryption keys.
The ``burn_key`` subcommand loads a key (stored as a raw binary file)
and burns it to a key block.

"flash\_encryption" can be used as an alias for BLK1, and "secure\_boot"
can be used as an alias for BLK2.

-  The ``burn_key`` command should only be used for hardware flash
   encryption or secure boot keys. See `Burning non-key
   data <#burning-non-key-data>`__ for a command that works for data
   read by software.

Key Coding Scheme
^^^^^^^^^^^^^^^^^

When the "None" coding scheme is in use, keys are 256-bits (32 bytes)
long. When 3/4 Coding Scheme is in use (``CODING_SCHEME`` efuse has
value 1 not 0), keys are 192-bits (24 bytes) long and an additional 64
bits of error correction data are also written. espefuse.py v2.6 or
newer is required to burn keys with 3/4 Coding Scheme. The key file must
be the appropriate length for the coding scheme currently in use.

When keys are stored in ESP32 Efuse blocks, they are stored in reverse
byte order (last byte of the key is written to the first byte of efuse,
etc.)

Unprotected Keys
^^^^^^^^^^^^^^^^

By default, when an encryption key block is burned it is also read and
write protected. The ``--no-protect-key`` option will disable this
behaviour (you can separately read- or write-protect the key later.)
Note that leaving a key unprotected may compromise its use as a security
feature.

::

    espefuse.py --port /dev/DONOTDOTHIS burn_key secure_boot keyfile.bin

Note that the hardware flash encryption and secure boot features require
the key to be written to the efuse block in reversed byte order,
compared to the order used by the AES algorithm on the host.
``burn_key`` automatically reverses the bytes when writing. For this
reason, an unprotected key will read back in the reverse order to the
``keyfile.bin`` on the host.

force-write-always
^^^^^^^^^^^^^^^^^^

Normally, a key will only be burned if the efuse block has not been
previously written to. The ``--force-write-always`` option can be used
to ignore this and try to burn the key anyhow. Note that this option is
still limited by the efuse hardware - hardware doesn't allow any efuse
bits to be cleared 1->0, and can't write anything to write protected
efuse blocks.

Confirmation
^^^^^^^^^^^^

The ``--do-not-confirm`` option can be used with ``burn_key``, otherwise
a manual confirmation step is required.

Limitations of the burn\_key command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``burn_key`` command is only suitable for flash encryption and
secure boot keys:

-  Complete block is always written. (This means 256-bits for "None"
   coding Scheme or 192-bits for 3/4 Coding Scheme).
-  The data is written in reverse byte order for compatibility with
   encryption hardware (see `above <#unprotected-keys>`__).
-  By default, the data is read- and write-protected so it can only be
   used by hardware.

Burning non-key data
--------------------

The ``burn_block_data`` command allows writing arbitrary data from a
file into an efuse block, for software use.

This command is available in espefuse.py v2.6 and newer.

Example
^^^^^^^

Write to Efuse BLK3 from binary file ``device_id.bin``, starting at
efuse byte offset 6:

::

    espefuse.py -p PORT burn_block_data --offset 6 BLK3 device_id.bin

-  Data is written to the Efuse block in normal byte order (treating the
   Efuse block as if it was an array of bytes). It can be read back in
   firmware from the efuse read registers, but these reads must be
   always be complete register words (4-byte aligned).
-  Part of the Efuse block can be written at a time. The ``--offset``
   argument allows writing to a byte offset inside the Efuse block
   itself.
-  This command is not suitable for writing key data which will be used
   by flash encryption or secure boot hardware. Use
   `burn\_key <#burning-a-key>`__ for this.

burn\_block\_data restrictions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For "None" Coding Scheme, there are no restrictions on the range of
bytes which can be written in the Efuse block (but any bit in efuse can
only be set 0->1, never cleared 1->0).

For "3/4" Coding Scheme, the length of the data file and the offset must
both be a multiple of 6 bytes. Each 6 byte span can only be written one
time.

SPI flash pins
--------------

The following efuses configure the SPI flash pins which are used to
boot:

::

    SPI_PAD_CONFIG_CLK     Override SD_CLK pad (GPIO6/SPICLK)                = 0 R/W (0x0)
    SPI_PAD_CONFIG_Q       Override SD_DATA_0 pad (GPIO7/SPIQ)               = 0 R/W (0x0)
    SPI_PAD_CONFIG_D       Override SD_DATA_1 pad (GPIO8/SPID)               = 0 R/W (0x0)
    SPI_PAD_CONFIG_HD      Override SD_DATA_2 pad (GPIO9/SPIHD)              = 0 R/W (0x0)
    SPI_PAD_CONFIG_CS0     Override SD_CMD pad (GPIO11/SPICS0)               = 0 R/W (0x0)

On ESP32 chips without integrated SPI flash, these efuses are set to
zero in the factory. This causes the default GPIO pins (shown in the
summary output above) to be used for the SPI flash.

On ESP32 chips with integrated internal SPI flash, these efuses are
burned in the factory to the GPIO numbers where the flash is connected.
These values override the defaults on boot.

In order to change the SPI flash pin configuration, these efuses can be
burned to the GPIO numbers where the flash is connected. If at least one
of these efuses is burned, all of of them must be set to the correct
values.

If these efuses are burned, GPIO1 (U0TXD pin) is no longer consulted to
set the boot mode from SPI to HSPI flash on reset.

These pins can be set to any GPIO number in the range 0-29, 32 or 33.
Values 30 and 31 cannot be set. The "raw" hex value for pins 32,33 is
30,31 (this is visible in the summary output if these pins are
configured for any SPI I/Os.)

ie:

::

    SPI_PAD_CONFIG_CS0     Override SD_CMD pad (GPIO11/SPICS0)               = 32 R/W (0x1e)

If using the ``burn_efuse`` command to configure these pins, always
specify the actual GPIO number you wish to set.

Read- and Write- protecting efuses
----------------------------------

**This command can severely limit your ESP32 options**

Some efuses can be read- or write-protected, preventing further changes.
``burn_key`` subcommand read and write protects new keys by default, but
other efuses can be protected iwth the ``read_protect_efuse`` and
``write_protect_efuse`` commands.

The ``R/W`` output in the summary display will change to indicate
protected efuses: \* ``-/W`` indicates read protected (value will always
show all-zeroes, even though hardware may use the correct value.) \*
``R/-`` shows write protected (no further bits can be set), \* ``-/-``
means read and write protected.

Sample:

::

    espefuse.py --port /dev/SOMEPORT read_protect_efuse KEY_STATUS

The ``--do-not-confirm`` option can be used with ``burn_key``, otherwise
a manual confirmation step is required.

**NOTE that efuses are often read/write protected as a group, so
protecting one will cause some related efuses to become protected.
espefuse.py will confirm the full list of efuses that will become
protected.**

The following efuses can be read protected:

*  FLASH\_CRYPT\_CONFIG
*  CODING\_SCHEME
*  KEY\_STATUS
*  BLK1
*  BLK2
*  BLK3

The following efuses can be write protected:

*  WR\_DIS,RD\_DIS
*  FLASH\_CRYPT\_CNT
*  MAC
*  XPD\_SDIO\_FORCE
*  XPD\_SDIO\_REG
*  XPD\_SDIO\_TIEH
*  SPI\_PAD\_CONFIG\_CLK
*  SPI\_PAD\_CONFIG\_Q
*  SPI\_PAD\_CONFIG\_D
*  SPI\_PAD\_CONFIG\_HD
*  SPI\_PAD\_CONFIG\_CS0
*  FLASH\_CRYPT\_CONFIG
*  CODING\_SCHEME
*  CONSOLE\_DEBUG\_DISABLE
*  DISABLE\_SDIO\_HOST
*  ABS\_DONE\_0
*  ABS\_DONE\_1
*  JTAG\_DISABLE
*  DISABLE\_DL\_ENCRYPT
*  DISABLE\_DL\_DECRYPT
*  DISABLE\_DL\_CACHE
*  KEY\_STATUS
*  BLK1
*  BLK2
*  BLK3

Execute eFuse python script
---------------------------

::

    espefuse.py execute_scripts efuse_script1.py efuse_script2.py ...

This command allows burning all needed eFuses at one time based on your
own python script and control issues during the burn process if so it
will abort the burn process. This command has a few arguments:

-  ``scripts`` is a list of scripts. The special format of python
   scripts can be executed inside espefuse.py.

Below you can see some examples of the script. This script file is run
from espefuse.py as ``exec(open(file.name).read())`` it means that some
functions and imported libs are available for using like ``os``. Please
use only provided functions. If you want to use other libs in the script
you can add them manually.

Inside this script, you can call all commands which are available in
CLI, see ``espefuse.py --help``. To run a efuse command you need to call
``espefuse(esp, efuses, args, 'burn_efuse DISABLE_DL_DECRYPT 1')``. This
command will not burn eFuses immediately, the burn occurs at the end of
all scripts. But if necessary, you can call ``efuses.burn_all()`` which
asks you ``Type 'BURN' (all capitals) to continue.``. To skip this
question and go without confirmation just add the ``--do-not-confirm``
flag to the ``execute_scripts`` command.

::

    espefuse.py execute_scripts efuse_script1.py --do-not-confirm

Additionally, you can implement some checks based on the value of
eFuses. To get value of a eFuse use -
``efuses['FLASH_CRYPT_CNT'].get()``. Some eFuses have a dictionary to
convert from a value to a human-readable as it looks in the table is
printed by the ``summary`` command. See how it is done for
``CODING_SCHEME`` it calls ``get_meaning()`` 0: "NONE (BLK1-3 len=256
bits)", 1: "3/4 (BLK1-3 len=192 bits)", 2: "REPEAT (BLK1-3 len=128 bits)
not supported", 3: "NONE (BLK1-3 len=256 bits)".

.. code:: python

    print("connected chip: %s, coding scheme %s" % (esp.get_chip_description(), efuses["CODING_SCHEME"].get_meaning()))
    if os.path.exists("flash_encryption_key.bin"):
        espefuse(esp, efuses, args, "burn_key flash_encryption flash_encryption_key.bin")
    else:
        raise esptool.FatalError("The 'flash_encryption_key.bin' file is missing in the project directory")

    espefuse(esp, efuses, args, 'burn_efuse FLASH_CRYPT_CNT 0x7')

    current_flash_crypt_cnt = efuses['FLASH_CRYPT_CNT'].get()
    if current_flash_crypt_cnt in [0, 3]:
        espefuse(esp, efuses, args, 'burn_efuse FLASH_CRYPT_CNT')

    espefuse(esp, efuses, args, 'burn_efuse DISABLE_DL_ENCRYPT 1')

    espefuse(esp, efuses, args, 'burn_efuse DISABLE_DL_DECRYPT 1')

    espefuse(esp, efuses, args, 'burn_efuse DISABLE_DL_CACHE 1')

    espefuse(esp, efuses, args, 'burn_efuse JTAG_DISABLE 1')
    ...

After ``efuses.burn_all()``, all needed eFuses will be burnt to chip in
order BLK\_MAX to BLK\_0. This order prevents cases when protection is
set before the value goes to a block. Please note this while developing
your scripts. Upon completion, the new eFuses will be read back, and
will be done some checks of written eFuses by espefuse.py. In
production, you might need to check that all written eFuses are set
properly, see the example below to get how to check it.

The script below burns some eFuses and checks them after reading back.
To check read and write protection using ``is_readable()`` and
``is_writeable()``.

See
`test\_efuse\_script.py <https://github.com/espressif/esptool/blob/master/test/efuse_scripts/esp32xx/test_efuse_script.py>`__
