from machine import Pin, ADC
from time import sleep

hit = Pin(27,Pin.IN)

while(True):
  print(hit.value())
  sleep(0.01)
