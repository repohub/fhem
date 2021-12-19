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

import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import time

#DEBUG = True
DEBUG = False

"""
K2
Bad
treppenhaus_unten
hauswirtschaftsraum
stubehinten
stubevorn -> Tuer
kueche -> Tuer
K1
SZ
OG_kinderzimmer
OG_balkon_links
OG_schlafzimmer
OG_treppenhaus
"""
### Reihenfolge beachten! ####
topics = ["kindzwei","bad","treppenhaus_unten","hauswirtschaftsraum","stube_hinten","stube_vorn","kueche","kindeins","schlafzimmer","OG_kinderzimmer","OG_balkon_links","OG_schlafzimmer","OG_treppenhaus"] # Liste aller Raeume
openwindowPins = [29,28,31,4,17,27,22,10,11,9,7,8,25]#,24,23,18]  # 1-8 / 9-16
openwindowState = ['0'] * len(openwindowPins)
openwindowStateTemp = ['0'] * len(openwindowPins)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(True)

for pin in openwindowPins:
  GPIO.setup(pin, GPIO.IN)

def connect_mqtt(client,server,port,timeout):
  client = mqtt.Client(client)
  client.username_pw_set(username="mqttuser",password="mqttpw")
  client.on_connect = on_connect
  client.on_message = on_message
  client.connect(server,port,timeout)
  client.loop_start()
  looop(client)

def on_connect(client, userdata, flags, rc):
  if DEBUG:
    print("Connected with result code " + str(rc))

def on_message(client, userdata, message):
  if DEBUG:
    print("message received=" ,str(message.payload.decode("utf-8")),"=")
    print("message topic=",message.topic)
    #print("message qos=",message.qos)
    #print("message retain flag=",message.retain)

def looop(client):
  # Endlosschleife
  while True:
    for pin in openwindowPins:
      i = openwindowPins.index(pin)
      openwindowStateTemp[i] = openwindowState[i]
      if str(GPIO.input(pin)) == '1':
        openwindowState[i] = 1 # closed
      else:
        openwindowState[i] = 0 # open
      if DEBUG:
        print("Pin: "+str(pin)+" "+str(GPIO.input(pin)))
  
    if (openwindowStateTemp != openwindowState):
      outputString = ['0'] * len(openwindowPins)
      oneopen = 0
      for pin in openwindowPins:
        i = openwindowPins.index(pin)
        if openwindowState[i] == 0:  # open
          outputString[i] = '1'
          if DEBUG:
            print("house/"+topics[i]+"/windowstate", "open")
          client.publish("house/"+topics[i]+"/windowstate", "open")
          oneopen = 1
        else:
          outputString[i] = '0'
          if DEBUG:
            print("house/"+topics[i]+"/windowstate", "closed")
          client.publish("house/"+topics[i]+"/windowstate", "closed")
          
      if oneopen == 1:
        outputString[0] = '1'
        #client.publish("house/screen/show/openwindow", str(''.join(outputString)))
      else:
        #outputString[0] = '0'
        outputString[0] = '-'
        #client.publish("house/screen/show/openwindow", str(''.join(outputString)))  
      #  print("house/alle/windowstate", str(outputString))  
  
    if DEBUG:
      print("------------\n")
    time.sleep(1)

if __name__ == '__main__':
    if DEBUG:
        print ("start")
    connect_mqtt("fensterStatusmqtt", "127.0.0.1", 1883, 60)
