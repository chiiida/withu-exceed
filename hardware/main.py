from machine import Pin, PWM, ADC
from time import sleep
import json
import urequests as requests
from _thread import start_new_thread as thread
import network

p_vibration = Pin(27,Pin.IN)
p_RLED = Pin(14, Pin.OUT) 
p_GLED = Pin(12, Pin.OUT) 
p_BLED = Pin(13, Pin.OUT)

WIFISTATUS = False
LEDSTATUS = 'disconnected'
API = "https://exceed.superposition.pknn.dev/data/withu"
VIBRATIONSTATUS = False

def WIFIConnect():
  global WIFISTATUS, LEDSTATUS
  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)
  WIFISTATUS = False
  wlan.connect('exceed16_8', '12345678')
  LEDSTATUS = 'connecting'
  while not wlan.isconnected():
    sleep(0.01)
  WIFISTATUS = wlan.isconnected()
  LEDSTATUS = 'connected'

def WIFICheck():
  global LEDSTATUS
  while True:
    if not WIFISTATUS:
      LEDSTATUS = 'disconnected'
      WIFIConnect()
    sleep(2)
  
def vibrationSensor():
  global VIBRATIONSTATUS,vibration
  while(True):
    count = 0
    for i in range (60000):
      if (p_vibration == 0):
        count += 1
      sleep(0.001)
    if (count >= 5000):
      vibration = True
    else:
      vibration = False
    VIBRATIONSTATUS = True
    sleep(0.01)
  

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

def postData():
    global API, vibration
    while True:
        if (vibration):
          print('Vibration = True')
        else:
          print('Vibration = False')          
        if WIFISTATUS:
          r = requests.get(API)
          json_data = r.json()
          print(data)
          data = json.dumps({
            'vibration': vibration
          })
          headers = {'Content-type': 'application/json'}
          print(requests.post(API, data=data, headers=headers).content)
          VIBRATIONSTATUS = False
      sleep(0.01)


WIFIConnect()
#thread(WIFICheck, [])
#thread(statusLED(), [])
thread(vibrationSensor(), [])
thread(postData(), [])