#!/usr/bin/env python
#
# SPDX-FileCopyrightText: 2016-2021 Espressif Systems (Shanghai) CO LTD
#
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import division, print_function

import argparse
import os
import sys
from io import StringIO

import espressif.efuse.esp32 as esp32_efuse
import espressif.efuse.esp32c3 as esp32c3_efuse
import espressif.efuse.esp32h2 as esp32h2_efuse
import espressif.efuse.esp32s2 as esp32s2_efuse
import espressif.efuse.esp32s3 as esp32s3_efuse
import espressif.efuse.esp32s3beta2 as esp32s3beta2_efuse

import esptool


def get_esp(port, baud, connect_mode, chip='auto', skip_connect=False, virt=False, debug=False, virt_efuse_file=None):
    if chip not in ['auto', 'esp32', 'esp32s2', 'esp32s3beta2', 'esp32s3', 'esp32c3', 'esp32h2']:
        raise esptool.FatalError("get_esp: Unsupported chip (%s)" % chip)
    if virt:
        esp = {
            'esp32': esp32_efuse,
            'esp32s2': esp32s2_efuse,
            'esp32s3beta2': esp32s3beta2_efuse,
            'esp32s3': esp32s3_efuse,
            'esp32c3': esp32c3_efuse,
            'esp32h2': esp32h2_efuse,
        }.get(chip, esp32_efuse).EmulateEfuseController(virt_efuse_file, debug)
    else:
        if chip == 'auto' and not skip_connect:
            esp = esptool.ESPLoader.detect_chip(port, baud, connect_mode)
        else:
            esp = {
                'esp32': esptool.ESP32ROM,
                'esp32s2': esptool.ESP32S2ROM,
                'esp32s3beta2': esptool.ESP32S3BETA2ROM,
                'esp32s3': esptool.ESP32S3ROM,
                'esp32c3': esptool.ESP32C3ROM,
                'esp32h2': esptool.ESP32H2ROM,
            }.get(chip, esptool.ESP32ROM)(port if not skip_connect else StringIO(), baud)
            if not skip_connect:
                esp.connect(connect_mode)
    return esp


def get_efuses(esp, skip_connect=False, debug_mode=False, do_not_confirm=False):
    try:
        efuse = {
            'ESP32': esp32_efuse,
            'ESP32-S2': esp32s2_efuse,
            'ESP32-S3(beta2)': esp32s3beta2_efuse,
            'ESP32-S3': esp32s3_efuse,
            'ESP32-C3': esp32c3_efuse,
            'ESP32-H2': esp32h2_efuse,
        }[esp.CHIP_NAME]
    except KeyError:
        raise esptool.FatalError("get_efuses: Unsupported chip (%s)" % esp.CHIP_NAME)
    # dict mapping register name to its efuse object
    return (efuse.EspEfuses(esp, skip_connect, debug_mode, do_not_confirm), efuse.operations)


def main(custom_commandline=None):
    """
    Main function for espefuse

    custom_commandline - Optional override for default arguments parsing (that uses sys.argv), can be a list of custom arguments
    as strings. Arguments and their values need to be added as individual items to the list e.g. "--port /dev/ttyUSB1" thus
    becomes ['--port', '/dev/ttyUSB1'].
    """
    init_parser = argparse.ArgumentParser(description='espefuse.py v%s - [ESP32/S2/S3BETA2/S3/C3/H2] efuse get/set tool' % esptool.__version__,
                                          prog='espefuse', add_help=False)

    init_parser.add_argument('--chip', '-c',
                             help='Target chip type',
                             choices=['auto', 'esp32', 'esp32s2', 'esp32s3beta2', 'esp32s3', 'esp32c3', 'esp32h2'],
                             default=os.environ.get('ESPTOOL_CHIP', 'auto'))

    init_parser.add_argument('--baud', '-b',
                             help='Serial port baud rate used when flashing/reading',
                             type=esptool.arg_auto_int,
                             default=os.environ.get('ESPTOOL_BAUD', esptool.ESPLoader.ESP_ROM_BAUD))

    init_parser.add_argument('--port', '-p',
                             help='Serial port device',
                             default=os.environ.get('ESPTOOL_PORT', esptool.ESPLoader.DEFAULT_PORT))

    init_parser.add_argument('--before',
                             help='What to do before connecting to the chip',
                             choices=['default_reset', 'no_reset', 'esp32r1', 'no_reset_no_sync'],
                             default='default_reset')

    init_parser.add_argument('--debug', "-d", help='Show debugging information (loglevel=DEBUG)', action='store_true')
    init_parser.add_argument('--virt', help='For host tests, the tool will work in the virtual mode (without connecting to a chip).', action='store_true')
    init_parser.add_argument('--path-efuse-file', help='For host tests, saves efuse memory to file.', type=str, default=None)
    init_parser.add_argument('--do-not-confirm', help='Do not pause for confirmation before permanently writing efuses. Use with caution.', action='store_true')

    args1, remaining_args = init_parser.parse_known_args(custom_commandline)
    debug_mode = args1.debug or ("dump" in remaining_args)
    just_print_help = [True for arg in remaining_args if arg in ["--help", "-h"]] or remaining_args == []
    esp = get_esp(args1.port, args1.baud, args1.before, args1.chip, just_print_help, args1.virt, args1.debug, args1.path_efuse_file)
    efuses, efuse_operations = get_efuses(esp, just_print_help, debug_mode, args1.do_not_confirm)

    parser = argparse.ArgumentParser(parents=[init_parser])
    subparsers = parser.add_subparsers(dest='operation', help='Run espefuse.py {command} -h for additional help')

    efuse_operations.add_commands(subparsers, efuses)

    args = parser.parse_args(remaining_args)
    vars(args).update(vars(args1))
    args.only_burn_at_end = False
    print('espefuse.py v%s' % esptool.__version__)
    if args.operation is None:
        parser.print_help()
        parser.exit(1)
    operation_func = vars(efuse_operations)[args.operation]

    # each 'operation' is a module-level function of the same name
    operation_func(esp, efuses, args)

    if args1.virt is False:
        esp._port.close()


def _main():
    try:
        main()
    except esptool.FatalError as e:
        print('\nA fatal error occurred: %s' % e)
        sys.exit(2)


if __name__ == '__main__':
    _main()
