import machine, time, dht, ujson, network, urequests
from ntptime import settime

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

server_on = True
def send_data(temp, hum):
    global server_on

    if server_on:
        rpm_val = 0
        power_val = 0
        if temp > 26.7 or hum > 45:
            rpm_val = 1100
            power_val = 50

        json = { "type":"data_send_train",
                 "data": {  "temp (C)": temp,
                            "hum": hum,
                            "RPM": rpm_val,
                            "Power (W)": power_val,
                            "time": time.time()
                         }
                }
        headers = { "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8" }
        r = urequests.request("POST", aws_URL, json=json, headers=headers)
#        print("response=", r.text)


def get_rpm():
    hall_thresh = 100
    hall_count = 0
    on_state = False
    
    hs = machine.Pin(15, machine.Pin.IN)

    start = time.ticks_us()

    while(1):
        if hs.value() == 0:
            if not on_state:
                on_state = True
                hall_count += 1
        else:
            on_state = False

        if hall_count >= hall_thresh:
            break

    end = time.ticks_us()
    time_passed = ((end - start)/1000000.0)
    print("Time Passed:", time_passed)
    
    rpm_val = (hall_count/time_passed)*60.0
    print("RPM: ", rpm_val)
    time.sleep(1)
    

def run():
    global server_on
#    print("Trying to connect...")

    ipconfig = connect_wifi('ZEYNET', 'Pamukkale1')
#    print("ip:", ipconfig[0])

    try:
        urequests.request("POST", aws_URL, json={"type":"check"}, headers={})
        print("Server online")
    except:
        print("Server offline, this may cause problems")
        server_on = False

    settime()
    sensor = dht.DHT22(machine.Pin(14))
    temp = -1
    hum = -1
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
#        print('Temperature: %3.1f C' %temp)
#        print('Humidity: %3.1f %%' %hum)
    except OSError as e:
        print('Failed to read sensor.')
    else:
        send_data(temp, hum)

    #10000
    machine.deepsleep(1200000)


run()


    
#import esp32
## internal temp and hall sensor
#esp_hs_val = esp32.hall_sensor()
#esp_temp_val esp32.raw_temperature()
#print("esp's hall sens val = ", esp_hs_val)
#print("esp's temp =", esp_temp_val)


