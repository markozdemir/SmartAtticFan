from Pin, time

led = machine.Pin(2, machine.Pin.OUT)

while True:
  led.value(not led.value())
  time.sleep(0.5)

