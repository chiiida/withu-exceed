from machine import Pin, PWM, ADC
from time import sleep
import json
import urequests as requests
from _thread import start_new_thread as thread
import network

p_hit = Pin(27,Pin.IN)
p_RLED = Pin(14, Pin.OUT) 
p_GLED = Pin(12, Pin.OUT) 
p_BLED = Pin(13, Pin.OUT)
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

WIFISTATUS = False
LEDSTATUS = 'disconnected'

def WIFIConnect():
  global WIFISTATUS, LEDSTATUS, wlan
  WIFISTATUS = False
  wlan.connect('exceed16_8', '12345678')
  LEDSTATUS = 'connecting'
  while not wlan.isconnected():
    sleep(0.01)
  WIFISTATUS = True
  LEDSTATUS = 'connected'

def WIFICheck():
  while True:
    if not wlan.isconnected():
      LEDSTATUS = 'disconnected'
      WIFIConnect()
    sleep(2)
  
def HitSensor():
  while(True):
    print(p_hit.value())
    sleep(0.000001)

def statusLED():
  while(True):
    if (LEDSTATUS == 'disconnected'):
      p_RLED.value(1)
      p_GLED.value(0)
      p_BLED.value(0)
    elif (LEDSTATUS == 'connecting'):
      p_RLED.value(1)
      p_GLED.value(0)
      p_BLED.value(0)
      sleep(0.01)
      p_RLED.value(0)
      p_GLED.value(0)
      p_BLED.value(0)
    else:
      p_RLED.value(0)
      p_GLED.value(1)
      p_BLED.value(0)
  sleep(0.01)

WIFIConnect()
thread(WIFICheck, [])
thread(statusLED(), [])