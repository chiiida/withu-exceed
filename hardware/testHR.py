from machine import Pin, ADC
from time import sleep

hr = ADC(Pin(34))
led = Pin(5,Pin.OUT)
 
alpha = 0.75
period = 0.02
change = 0.0

while (True):
  oldValue = 0
  oldChange = 0
  rawValue = hr.read()
  value = alpha * oldValue + (1-alpha) * rawValue
  change = value - oldValue
  if (change < 0.0 and oldChange > 0.0):
    led.value(1)
  oldValue = value
  oldChange = change
  delay(period)
