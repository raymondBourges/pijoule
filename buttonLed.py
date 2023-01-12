from gpiozero import LED, Button
from time import sleep

led = LED(16)
button = Button(17)

def on():
    led.on()
    print("Allumer !")
    return

def off():
    led.off()
    print("Eteindre !")
    return

button.when_pressed = on
button.when_released = off

while True:
    sleep(1)
    print("Attendre...")


