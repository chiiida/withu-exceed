from machine import Pin, PWM, ADC
from time import sleep
import json
import urequests as requests
from _thread import start_new_thread as thread
import network

WIFISTATUS = False

def WIFIConnect():
  global WIFISTATUS
  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)
  WIFISTATUS = False
  wlan.connect('exceed16_8', '12345678')
  while not wlan.isconnected():
    print('connecting...')
    sleep(0.01)
  WIFISTATUS = wlan.isconnected()
  print('connected')


def WIFICheck():
  while True:
    if not WIFISTATUS:
      WIFIConnect()
    sleep(2)
  

WIFIConnect()
