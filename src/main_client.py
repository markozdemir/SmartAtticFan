import machine, time, dht, ujson
import network, urequests

# info at https://randomnerdtutorials.com/esp32-esp8266-dht11-dht22-micropython-temperature-humidity-sensor/
aws_URL = "http://ec2-3-141-199-6.us-east-2.compute.amazonaws.com"

sta_if = None
def connect_wifi(ssid, pw):
    global sta_if
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect(ssid, pw)
        while not sta_if.isconnected():
            time.sleep_ms(200)
            pass
    return sta_if.ifconfig()

print("Trying to connect...")
ipconfig = connect_wifi('router_name', 'pass')
print("ip:", ipconfig[0])

try:
    urequests.request("POST", aws_URL, json={"type":"check"}, headers={})
    print("Server online")
except:
    print("Server offline, this may cause problems")


sensor = dht.DHT22(machine.Pin(14))

while True:
    try:
        sleep(2)
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        print('Temperature: %3.1f C' %temp)
        print('Humidity: %3.1f %%' %hum)
        r = urequests.request("POST", aws_URL, json={"type":"data_send_print", \
            "data": {"temp": temp, "hum": hum}}, \
            headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"})
        print("response", r.text)
    except OSError as e:
        print('Failed to read sensor.')


#import esp32
## internal temp and hall sensor
#esp_hs_val = esp32.hall_sensor()
#esp_temp_val esp32.raw_temperature()
#print("esp's hall sens val = ", esp_hs_val)
#print("esp's temp =", esp_temp_val)
