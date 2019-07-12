from machine import Pin, ADC
from time import sleep

p_hit = Pin(27,Pin.IN)

def HitSensor():
  while(True):
    print(p_hit.value())
    sleep(0.000001)
