#!/usr/bin/env python3
#-*- encoding:utf8 -*-
#
# MIT License
#
# Copyright (c) 2020 micha
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import time, sys, math

import relay_modbus
import relay_boards

##########################################################
SERIAL_PORT = '/dev/ttyAMA0'


def print_relay_board_info(board):
    print('Relay board "{}" #{}:'.format(board.board_name, board.address))
    print('  Name:      {}'.format(board.board_name))
    print('  Type:      {}'.format(board.board_type))
    print('  Port:      {}'.format(board.serial_port))
    print('  Baudrate:  {}'.format(board.baudrate))
    print('  Addresses: {}'.format(board.num_addresses))
    print('  Relays:    {}'.format(board.num_relays))
    print('  Address:   {} (Configure DIP switches)'.format(board.address))
    print()


# Create relay_modbus object
_modbus = relay_modbus.Modbus(serial_port=SERIAL_PORT, verbose=False)
# Open serial port
try:
  _modbus.open()
except relay_modbus.SerialOpenException as err:
  print(err)
  sys.exit(1)

# ----------------------------------------------------------------------------------------------
# Create relay board objects
relaycard1 = relay_boards.R421A08(_modbus, address=1, board_name='relaycard1')
relaycard2 = relay_boards.R421A08(_modbus, address=2, board_name='relaycard2')
relaycard3 = relay_boards.R421A08(_modbus, address=3, board_name='relaycard3')
relaycard4 = relay_boards.R421A08(_modbus, address=4, board_name='relaycard4')
relaycard5 = relay_boards.R421A08(_modbus, address=5, board_name='relaycard5')
# ----------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------
#examples
#relaycard1.on(1)
#relaycard1.on_multi([2, 3, 7])
#relaycard1.print_status_all()

if __name__ == '__main__':
  print("------ Relaycard 1 -------")
  relaycard1.print_status_all()
  print("------ Relaycard 2 -------")
  relaycard2.print_status_all()
  print("------ Relaycard 3 -------")
  relaycard3.print_status_all()
  print("------ Relaycard 4 -------")
  relaycard4.print_status_all()
  print("------ Relaycard 5 -------")
  relaycard5.print_status_all()
  
  print("------ all off -------")
  relaycard1.off_multi([1, 2, 3, 4, 5, 6, 7, 8])
  relaycard2.off_multi([1, 2, 3, 4, 5, 6, 7, 8])
  relaycard3.off_multi([1, 2, 3, 4, 5, 6, 7, 8])
  relaycard4.off_multi([1, 2, 3, 4, 5, 6, 7, 8])
  relaycard5.off_multi([1, 2, 3, 4, 5, 6, 7, 8])

  print("------ Relaycard 1 -------")
  relaycard1.print_status_all()
  print("------ Relaycard 2 -------")
  relaycard2.print_status_all()
  print("------ Relaycard 3 -------")
  relaycard3.print_status_all()
  print("------ Relaycard 4 -------")
  relaycard4.print_status_all()
  print("------ Relaycard 5 -------")
  relaycard5.print_status_all()
