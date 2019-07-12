from machine import Pin, PWM, ADC
from time import sleep
import json
import urequests as requests
from _thread import start_new_thread as thread
import network


def WIFIConnect():
  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)
  while True:
    WIFISTATUS = 0
    print('connecting...')
    wlan.connect('exceed16_8', '12345678')
    while not wlan.isconnected():
      sleep(0.01)
      WIFISTATUS = 1
      print('connected')
    while wlan.isconnected():
      sleep(2)

def WIFICheck():
  while True:
    if not wlan.isconnected():
      WIFIConnect()
    sleep(2)
  

WIFIConnect()
