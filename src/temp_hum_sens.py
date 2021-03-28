import machine, time, dht

# info at https://randomnerdtutorials.com/esp32-esp8266-dht11-dht22-micropython-temperature-humidity-sensor/

sensor = dht.DHT22(machine.Pin(14))

while True:
    try:
        sleep(2)
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        print('Temperature: %3.1f C' %temp)
        print('Humidity: %3.1f %%' %hum)
    except OSError as e:
        print('Failed to read sensor.')


#import esp32
## internal temp and hall sensor
#esp_hs_val = esp32.hall_sensor()
#esp_temp_val esp32.raw_temperature()
#print("esp's hall sens val = ", esp_hs_val)
#print("esp's temp =", esp_temp_val)
