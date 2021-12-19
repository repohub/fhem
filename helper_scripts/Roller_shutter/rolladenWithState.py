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

#RS485 = False
RS485 = True

if RS485:
  import relay_modbus
  import relay_boards

thelock = threading.Lock()
guardtime = 1.3

#DEBUG = True
DEBUG = False

import logging
#Creating and Configuring Logger
Log_Format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename = "/tmp/2rs485mqtt.log", filemode = "w", format = Log_Format, level = logging.INFO)
logger = logging.getLogger()
logging.info("#logging has started")

# 0   OPEN
# 100 CLOSED 
topics = ["kueche","stube_vorn","OG_balkon_links","OG_balkon_rechts","schlafzimmer","kindeins","stube_hinten","stube_erker_links","stube_erker_mitte","stube_erker_rechts","hauswirtschaftsraum","treppenhaus_unten","bad","kindzwei","OG_schlafzimmer","OG_kueche_links","OG_kueche_rechts","OG_treppenhaus","OG_kinderzimmer"] # Liste aller Raeume
secondsDown = [28,21,15,15,18,18,18,24,24,23,18,18,18,18,15,15,15,15,15]
secondsUp = [30,23,15,15,19,20,19,25,26,25,20,20,20,19,15,15,15,15,15]

state = ["STOP"] * len(topics)
#percentState = [0] * len(topics)
runtime = [0] * len(topics)
#runningTime = [0] * len(topics)
CurPosition = [0] * len(topics)
timer1 = [None] * len(topics)
#timer2 = [None] * len(topics)

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
      logging.error("SerialOpenException " + err)
      #print(err)
      sys.exit(1)

  # ----------------------------------------------------------------------------------------------
  # Create relay board objects
  relaycard1 = relay_boards.R421A08(_modbus, address=1, board_name='relaycard1')
  relaycard2 = relay_boards.R421A08(_modbus, address=2, board_name='relaycard2')
  relaycard3 = relay_boards.R421A08(_modbus, address=3, board_name='relaycard3')
  relaycard4 = relay_boards.R421A08(_modbus, address=4, board_name='relaycard4')
  relaycard5 = relay_boards.R421A08(_modbus, address=5, board_name='relaycard5')
  # ----------------------------------------------------------------------------------------------
  if DEBUG:
    # Print board info
    print_relay_board_info(relaycard1)
    print_relay_board_info(relaycard2)
    print_relay_board_info(relaycard3)
    print_relay_board_info(relaycard4)
    print_relay_board_info(relaycard5)
  # ----------------------------------------------------------------------------------------------
  #relaycard1.on(1)
  #relaycard1.on_multi([2, 3, 7])
  #relaycard1.print_status_all()
else:
  relaycard1 = 0
  relaycard2 = 0
  relaycard3 = 0
  relaycard4 = 0
  relaycard5 = 0


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


relaylist = [kueche,stube_vorn,OG_balkon_links,OG_balkon_rechts,schlafzimmer,kindeins,stube_hinten,stube_erker_links,stube_erker_mitte,stube_erker_rechts,hauswirtschaftsraum,treppenhaus_unten,bad,kindzwei,OG_schlafzimmer,OG_kueche_links,OG_kueche_rechts,OG_treppenhaus,OG_kinderzimmer] # Liste aller Raeume
##########################################################


if len(topics)!= len(relaylist):
  logging.error("Mismatch error: PLEASE CHECK topics AND relaylist!!")
  sys.exit(1)

class RepeatedTimer(object):
  def __init__(self, interval, eggtime, function, *args, **kwargs):
    self._timer = None
    self.interval = interval
    self.function = function
    self.eggtime = eggtime
    self.args = args
    self.kwargs = kwargs
    self.is_running = False
    self.next_call = time.time()
    self.tmp = 0
    self.start()
    #print("init")

  def _run(self):
    self.is_running = False
    self.start()
    self.function(*self.args, **self.kwargs)
    #print("_run")

  def start(self):
    #print("start1")
    if not self.is_running:
      self.next_call += self.interval
      self._timer = threading.Timer(self.next_call - time.time(), self._run)
      self._timer.start()
      self.is_running = True
      #print("start2")
      self.tmp = self.tmp + 1
      #print("tmp: " + str(self.tmp))
      if self.eggtime <= self.tmp:
        #print("self.stop()")
        self.stop()


  def stop(self):
    self._timer.cancel()
    self.is_running = False
    #print("stop")


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
    print("message received=" ,str(message.payload.decode("utf-8")),"=")
    print("message topic=",message.topic)
    #print("message qos=",message.qos)
    #print("message retain flag=",message.retain)

  payload = str(message.payload.decode("utf-8"))
  topic = str(message.topic).split('/')[1]
  logging.info('message received - topic: ' + topic + ' payload: ' + payload)
  
  if topic in topics:
    ind = topics.index(topic)
    #with thelock:
    executeCMD(payload,topic,ind,client)
  else:
    ind = -1
  if DEBUG:
    print("Topic: " + str(topic) + " Ind: " + str(ind))

def executeCMD(payload,topic,ind,client):
  # helper to avoid simultaneous command execution, because RS485 need guard times
  global state
  global runtime
  global CurPosition
  global timer1

  if ind >= 0: #topic exist
    logging.info('Start executeCMD - topic: ' + topic + ' payload: ' + payload + '-> Actual state: ' + state[ind])
    #if DEBUG:
    #  print("Starte payload: " + str(payload) + " ; Current state: " + state[ind])
    ###################################################################################
    if payload == "UP":
      #if DEBUG:
      #  print("payload UP start")
      #if state == UP:
        #ignore
      if state[ind] == "DOWN":
        timer1[ind].stop()
        state[ind] = "STOP"
        logging.info('Has been state DOWN, timer1 stopped, actual state ' + state[ind])
        #if DEBUG:
        #  print("DOWN/STOP")
      if state[ind] == "STOP":
        #if DEBUG:
        #  print("state[ind] == STOP")
        runtime[ind] = ((CurPosition[ind] * secondsUp[ind]) / 100.0)
        stepsize = (CurPosition[ind]) / (runtime[ind] - 1)
        logging.info('Has been state STOP, now running UP ' + str(runtime[ind]) + 'sec, CurPosition: ' + str(CurPosition[ind]))
        #if DEBUG:
        #  print("Run UP: " + str(runtime[ind]) + "sec, CurPosition: " + str(CurPosition[ind]))
        if runtime[ind] > 0:
          #logging.info("runtime > 0: " + runtime[ind])
          if RS485:
            if relaylist[ind][0].on(relaylist[ind][1][0]):
              timer1[ind] = RepeatedTimer(1,runtime[ind],publisherPercent,client,topic,ind,stepsize) #-> publish/percent alle 1s
              state[ind] = "UP"
              ##logging.info('Has been state STOP, now switch UP - board: ' + str(relaylist[ind][0]) + ' relay: ' + str(relaylist[ind][1][0]))
              #if DEBUG:
              #  print ("schalte " + topic + " UP - board: " + str(relaylist[ind][0]) + " relay: " + str(relaylist[ind][1][0]))
            else:
              client.publish("house/"+topic+"/error","UP failed")
              #logging.error('Has been state STOP, now state UP FAILED to mqtt')
          else:
              # no #logging required in no serial
              timer1[ind] = RepeatedTimer(1,runtime[ind],publisherPercent,client,topic,ind,stepsize) #-> publish/percent alle 1s
              state[ind] = "UP"
              #if DEBUG:
              #  print ("schalte " + topic + " UP - board")
        else:
          client.publish("house/"+topic+"/command","STOP")
          #logging.info('Has been state UP, now command STOP to mqtt')
    ###################################################################################
    if payload == "DOWN":
      #if DEBUG:
      #  print("payload DOWN start " + state[ind])
      #if state == DOWN:
        #ignore
      if state[ind] == "UP":
        timer1[ind].stop()
        state[ind] = "STOP"
        logging.info('Has been state UP, timer1 stopped, actual state ' + state[ind])
        #if DEBUG:
        #  print("UP/STOP")
      if state[ind] == "STOP":
        runtime[ind] = (((100 - CurPosition[ind]) * secondsDown[ind]) / 100.0)
        stepsize = (100 - CurPosition[ind]) / (runtime[ind] - 1)
        logging.info('Has been state STOP, now running DOWN ' + str(runtime[ind]) + 'sec, CurPosition: ' + str(CurPosition[ind]))
        #if DEBUG:
        #  print("Run DOWN " + str(runtime[ind]) + "sec, CurPosition: " + str(CurPosition[ind]))
        if runtime[ind] > 0:
          #logging.info("runtime > 0: " + runtime[ind])
          if RS485:
            if relaylist[ind][0].on(relaylist[ind][1][1]):
              timer1[ind] = RepeatedTimer(1,runtime[ind],publisherPercent,client,topic,ind,stepsize) #-> publish/percent alle 1s
              state[ind] = "DOWN"
              ##logging.info('Has been state STOP, now switch DOWN - board: ' + str(relaylist[ind][0]) + ' relay: ' + str(relaylist[ind][1][0]))
              #if DEBUG:
              #  print ("schalte " + topic + " DOWN - board: " + str(relaylist[ind][0]) + " relay: " + str(relaylist[ind][1][1]))
            else:
              client.publish("house/"+topic+"/error","DOWN failed")
              #logging.error('Has been state STOP, now state DOWN FAILED to mqtt')
          else:
            # no #logging required in no serial
            timer1[ind] = RepeatedTimer(1,runtime[ind],publisherPercent,client,topic,ind,stepsize) #-> publish/percent alle 1s
            state[ind] = "DOWN"
            #if DEBUG:
            #  print ("schalte " + topic + " DOWN - board")
        else:
          client.publish("house/"+topic+"/command","STOP")
          #logging.info('Has been state DOWN, now command STOP to mqtt')
    ###################################################################################
    if payload == "STOP":
      #if state == STOP:
        #ignore
      if state[ind] == "UP" or state[ind] == "DOWN":
        timer1[ind].stop()
        state[ind] = "STOP"
        logging.info('Has been state UP or DOWN, timer1 stopped, actual state ' + state[ind])
        if RS485:
          while not relaylist[ind][0].off_multi([relaylist[ind][1][0], relaylist[ind][1][1]]):
            client.publish("house/"+topic+"/error","STOP failed")
            time.sleep(0.5)
            ##logging.info('Has been state STOP, now state STOP FAILED to mqtt for topic: ' + topic)
          ##logging.info('executeCMD - topic: ' + topic + 'payload: ' + payload + '-> schalte STOP - timer - board' + str(relaylist[ind][0]) + ' relay: ' + str(relaylist[ind][1][0]) + ' relay: ' + str(relaylist[ind][1][1]))
          #if DEBUG:
          #  print ("schalte STOP - direkt - board: " + str(relaylist[ind][0]) + " relay: " + str(relaylist[ind][1][0]) + " relay: " + str(relaylist[ind][1][1]))
        else:
          # no #logging required in no serial
          if DEBUG:
            print ("schalte STOP - direkt - board")
    time.sleep(guardtime)

 
def publisherPercent(client, topic, ind, stepsize):
  global CurPosition
  
  if DEBUG:
    print ("stepsize: " + str(stepsize) + "%; CurPosition: " + str(CurPosition) + "%")
  if state[ind] == "UP":    
    CurPosition[ind] =  CurPosition[ind] - stepsize
    if CurPosition[ind] <= 1:
      state[ind] = "STOP"
      client.publish("house/"+topic+"/command","STOP")
      CurPosition[ind] = 0
      if RS485:
        while not relaylist[ind][0].off_multi([relaylist[ind][1][0], relaylist[ind][1][1]]):
          client.publish("house/"+topic+"/error","STOP failed")
          time.sleep(0.5)
          ##logging.error('publisherPercent - STOP FAILED to mqtt')
        #if DEBUG:
        #  print ("schalte STOP - timer - board: " + str(relaylist[ind][0]) + " relay: " + str(relaylist[ind][1][0]) + " relay: " + str(relaylist[ind][1][1]))
      else:
        if DEBUG:
          print ("schalte STOP - timer - board")
    client.publish("house/"+topic+"/percent", rounddown(CurPosition[ind]))

  if state[ind] == "DOWN":
    CurPosition[ind] =  CurPosition[ind] + stepsize
    if CurPosition[ind] >= 99:
      state[ind] = "STOP"
      client.publish("house/"+topic+"/command","STOP")
      CurPosition[ind] = 100
      if RS485:
        while not relaylist[ind][0].off_multi([relaylist[ind][1][0], relaylist[ind][1][1]]):
          client.publish("house/"+topic+"/error","STOP failed")
          time.sleep(0.5)
          ##logging.error('publisherPercent - STOP FAILED to mqtt')
        #if DEBUG:
        #  print ("schalte STOP - timer - board: " + str(relaylist[ind][0]) + " relay: " + str(relaylist[ind][1][0]) + " relay: " + str(relaylist[ind][1][1]))
      else:
        if DEBUG:
          print ("schalte STOP - timer - board")
    client.publish("house/"+topic+"/percent", roundup(CurPosition[ind]))

  #if DEBUG:
  #  print ("stepsize: " + str(stepsize) + "%; CurPosition: " + str(CurPosition) + "%")

def roundup(x):
  return int(math.ceil(x / 10.0)) * 10

def rounddown(x):
  return int(math.floor(x / 10.0)) * 10

if __name__ == '__main__':
    connect_mqtt("rs485mqtt", "127.0.0.1", 1883, 60)
