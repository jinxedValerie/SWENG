from machine import Pin
from time import sleep

onboard_led = Pin("LED", Pin.OUT)

while True:
    onboard_led.on()
    sleep(1)
    onboard_led.off()
    sleep(1)