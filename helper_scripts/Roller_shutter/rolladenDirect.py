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
"""
schlafzimmer_rolladen
kindeins_rolladen
kueche_rolladen -> Tuer
stube_hinten_rolladen
stube_erker_links_rolladen
stube_erker_mitte_rolladen
stube_erker_rechts_rolladen
stube_vorn_rolladen -> Tuer
hauswirtschaftsraum_rolladen
treppenhaus_unten_rolladen
bad_rolladen
kindzwei_rolladen

OG_schlafzimmer
OG_kueche_links
OG_kueche_rechts
OG_balkon_links
OG_balkon_rechts
OG_treppenhaus
OG_kinderzimmer
"""

import time, sys, math
import paho.mqtt.client as mqtt
import threading

guardtime = 0.5

#RS485 = False
RS485 = True

if RS485:
  import relay_modbus
  import relay_boards

DEBUG = False
#DEBUG = False
DEBUG_D = False

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

if RS485:
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
  if DEBUG_D:
    # Print board info
    print_relay_board_info(relaycard1)
    print_relay_board_info(relaycard2)
    print_relay_board_info(relaycard3)
    print_relay_board_info(relaycard4)
    print_relay_board_info(relaycard5)
  # ----------------------------------------------------------------------------------------------

else:
  relaycard1 = 0
  relaycard2 = 0
  relaycard3 = 0
  relaycard4 = 0
  relaycard5 = 0
  # ----------------------------------------------------------------------------------------------


###########################################################
# relaycard1
# relaycard2

# stube_hoch = relaycard1.on(1)
# stube_runter = relaycard1.on(2)

# kueche_hoch = relaycard2.on(5)
# kueche_runter = relaycard2.on(6)

kindzwei = [relaycard1,[1,2]]
bad = [relaycard1,[3,4]]
treppenhaus_unten = [relaycard1,[5,6]]
hauswirtschaftsraum = [relaycard1,[7,8]]

stube_hinten = [relaycard2,[1,2]]
stube_vorn = [relaycard2,[3,4]]
stube_erker_links = [relaycard2,[5,6]]
stube_erker_mitte = [relaycard2,[7,8]]

stube_erker_rechts = [relaycard3,[1,2]]
kueche = [relaycard3,[3,4]] # relaycard1, 3-hoch, 4-runter
kindeins = [relaycard3,[5,6]]
schlafzimmer = [relaycard3,[7,8]]

OG_kinderzimmer = [relaycard4,[1,2]]
OG_balkon_links = [relaycard4,[3,4]]
OG_balkon_rechts = [relaycard4,[5,6]]
OG_kueche_links = [relaycard4,[7,8]]

OG_kueche_rechts = [relaycard5,[2,1]] # ACHTUNG - getauscht
OG_schlafzimmer = [relaycard5,[3,4]]
OG_treppenhaus = [relaycard5,[5,6]]

topics = ["kueche","stube_vorn","OG_balkon_links","OG_balkon_rechts","schlafzimmer","kindeins","stube_hinten","stube_erker_links","stube_erker_mitte","stube_erker_rechts","hauswirtschaftsraum","treppenhaus_unten","bad","kindzwei","OG_schlafzimmer","OG_kueche_links","OG_kueche_rechts","OG_treppenhaus","OG_kinderzimmer"] # Liste aller Raeume
relaylist = [kueche,stube_vorn,OG_balkon_links,OG_balkon_rechts,schlafzimmer,kindeins,stube_hinten,stube_erker_links,stube_erker_mitte,stube_erker_rechts,hauswirtschaftsraum,treppenhaus_unten,bad,kindzwei,OG_schlafzimmer,OG_kueche_links,OG_kueche_rechts,OG_treppenhaus,OG_kinderzimmer] # Liste aller Raeume
##########################################################

if len(topics)!= len(relaylist):
  logging.error("Mismatch error: PLEASE CHECK topics AND relaylist!!")
  sys.exit(1)

def connect_mqtt(client,server,port,timeout):
  client = mqtt.Client(client)
  client.username_pw_set(username="mqttuser",password="mqttpw")
  client.on_connect = on_connect
  client.on_message = on_message
  client.connect(server,port,timeout)
  client.subscribe("house/+/command")
  client.loop_forever()

def on_connect(client, userdata, flags, rc):
  logger.info("Connected with result code " + str(rc))

def on_message(client, userdata, message):
  if DEBUG:
    print("message received=",str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    #print("message qos=",message.qos)
    #print("message retain flag=",message.retain)

  payload = str(message.payload.decode("utf-8"))
  topic = str(message.topic).split('/')[1]
  
  if topic in topics:
    ind = topics.index(topic)
    if DEBUG:
      print("Topic: " + str(topic) + " ind: " + str(ind))
    
    if ind >= 0: #topic exist
      if DEBUG:
        print("Starte payload: " + str(payload) + " ; Current ind: " + str(ind))
      ###################################################################################
      if payload == "UP":
        if RS485:
          if (relaylist[ind][0].on(relaylist[ind][1][0])):
            client.publish("house/"+topic+"/debug","UP done")
        else:
          client.publish("house/"+topic+"/debug","UP done")
      ###################################################################################
      if payload == "DOWN":
        if RS485:
          if relaylist[ind][0].on(relaylist[ind][1][1]):
            client.publish("house/"+topic+"/debug","DOWN done")
        else:
          client.publish("house/"+topic+"/debug","DOWN done")
      ###################################################################################
      if payload == "STOP":
        if RS485:
          if relaylist[ind][0].off_multi([relaylist[ind][1][0], relaylist[ind][1][1]]):
            client.publish("house/"+topic+"/debug","STOP done")
        else:
          client.publish("house/"+topic+"/debug","STOP done")

      time.sleep(guardtime)
  else:
    ind = -1
    if DEBUG:
      print("Topic: " + str(topic) + " ind: " + str(ind))  

if __name__ == '__main__':
    connect_mqtt("rs485mqtt", "127.0.0.1", 1883, 60)
