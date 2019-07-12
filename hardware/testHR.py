from machine import Pin, ADC
from time import sleep

hr = ADC(Pin(34))

while(True):
  print(hr.read())
  sleep(0.01)
