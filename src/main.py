import machine, time, dht, ujson, network, urequests, socket
import binascii, utime
from ntptime import settime

# info at https://randomnerdtutorials.com/esp32-esp8266-dht11-dht22-micropython-temperature-humidity-sensor/
aws_URL = "http://ec2-3-141-199-6.us-east-2.compute.amazonaws.com"

sta_if = None
server_on = True
connected_wifi = True
longitude = 0
latitude = 0

# ESP32 relay pins
relay_low  = machine.Pin(27, machine.Pin.OUT)
relay_med  = machine.Pin(4, machine.Pin.OUT) # pin 'A5'
relay_high = machine.Pin(21, machine.Pin.OUT)

fan_setting = 0

# hall sensor
hs = machine.Pin(15, machine.Pin.IN)


def get_timestamp():
    return 946684800 + utime.time()


def connect_wifi(ssid, pw):
    global sta_if, connected_wifi
    sta_if = network.WLAN(network.STA_IF)

    fails = 0
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect(ssid, pw)
        while not sta_if.isconnected():
            time.sleep_ms(200)
            fails += 1
            if fails > 100:
                connected_wifi = False
                return None
    return sta_if.ifconfig()


def send_data(temp, hum, rpm_val=0):
    global server_on, connected_wifi, fan_setting

    if server_on and connected_wifi:
        power_val = 0
        if rpm_val > 10:
            power_val = 50
            
            
        json = { "type":"data_send_train",
                 "data": {  "temp (C)": temp,
                            "hum": hum,
                            "RPM": rpm_val,
                            "Power (W)": power_val,
                            "time": get_timestamp(),
                            "fan_setting": fan_setting
                         }
                }
        headers = { "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8" }
        r = urequests.request("POST", aws_URL, json=json, headers=headers)
        print("response=", r.text)
        print("responseCode=", r.status_code)
        return ujson.loads(r.text.replace("'", '"'))
        

def format_mac(mac):
    mac_string = binascii.hexlify(mac)
    formatted_mac = ""
    count = 0
    for c in mac_string:
        formatted_mac += str(chr(c))
        if count > 0 and count % 2 == 1:
            formatted_mac += ":"
        count += 1
    print("Formatted mac addr of router from %s to %s" % (mac, formatted_mac))
    return formatted_mac


def get_location():
    global connected_wifi, latitude, longitude
    if not connected_wifi:
        return (None, None)
    url = "https://www.googleapis.com/geolocation/v1/geolocate?key="
    key = "AIzaSyA-mAkb-BG4f0ZIk1mNceujr1fMDVZozRg"
    mac = format_mac(sta_if.config('mac'))
    request_j = {
                  "considerIp": "true",
                  "wifiAccessPoints": [
                       {
                        "macAddress":  mac
                       }
                  ]
                }
    res = urequests.request("POST", url + key, json=request_j, headers={'content-type': 'application/json'})
    data = ujson.loads(res.text)
    location_data = data["location"]
    latitude = location_data["lat"]
    longitude = location_data["lng"]
    return (location_data["lat"], location_data["lng"])


def get_rpm():
    # 300 for 3 magnets
    hall_thresh = 100
    hall_count = 0
    on_state = False
    
#    hs = machine.Pin(15, machine.Pin.IN)

    start = time.ticks_us()

# TODO: CHANGE TIME
    # set time out for more than 10sec   ## 300sec (5 min)
    while((time.ticks_us() - start)/1000000.0 < 10):
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
    
    # divided by magnet count
    rpm_val = ((hall_count/3)/time_passed)*60.0
    print("RPM: ", int(rpm_val))
    return rpm_val

 
def turn_all_relays_off():
    # check and turn off if any relays are on
    if relay_low.value() == 1:
        relay_low.value(0)
    if relay_med.value() == 1:
        relay_med.value(0)
    if relay_high.value() == 1:
        relay_high.value(0)
    return True


def set_relay_switch(gear):
    global fan_setting, fan_speeds, relay_low, relay_med, relay_high
    
    fan_speeds = {1: relay_low, 2: relay_med, 3: relay_high}
    
    if gear > 3 or gear < 0:
        return -1
    elif gear == 0:
        fan_setting = 0
        turn_all_relays_off()
        return 0
        
    # change gear incrementally
    while gear != fan_setting:
        if gear > fan_setting:
            turn_all_relays_off()
            time.sleep(1)
            fan_setting += 1
            fan_speeds[fan_setting].value(1)
            time.sleep(4)
        else:
            turn_all_relays_off()
            time.sleep(1)
            fan_setting -= 1
            fan_speeds[fan_setting].value(1)
            time.sleep(2)
    
    return fan_setting


def start():
    global server_on, connected_wifi, fan_setting

    ipconfig = connect_wifi('ZEYNET', 'Pamukkale1')
    #ipconfig = connect_wifi('ORBI83', 'jaggedzoo924')
    get_location()
#    print("ip:", ipconfig[0])
    if connected_wifi:
        try:
            json = { "type":"check",
                     "data":   { "longitude": longitude,
                                 "latitude": latitude
                               }
                     }
            r = urequests.request("POST", aws_URL, json=json, headers={})
            print("Server online: response:", r)
        except:
            print("Server offline, this may cause problems")
            server_on = False
    else:
        print("Failed to connect to wifi")
        sever_on = False



def run():
    global server_on, connected_wifi, fan_setting
    if connected_wifi and server_on:
        settime()
        print(get_timestamp())

        sensor = dht.DHT22(machine.Pin(14))
        temp = -1
        hum = -1
        try:
            sensor.measure()
            temp = sensor.temperature()
            hum = sensor.humidity()
            print('Temperature: %3.1f C' %temp)
            print('Humidity: %3.1f %%' %hum)
        except OSError as e:
            print('Failed to read sensor.')
        else:
            try:
                resp_dict = send_data(temp, hum, get_rpm())
            
                fan_setting = set_relay_switch(int(resp_dict['speed']))
            except:
                print("Send data went wrong")

    else:
        print("not connected, could not run")

    #10000
#    machine.deepsleep(10000)

start()
while(1):
    run()
    time.sleep(15)
    
#import esp32
## internal temp and hall sensor
#esp_hs_val = esp32.hall_sensor()
#esp_temp_val esp32.raw_temperature()
#print("esp's hall sens val = ", esp_hs_val)
#print("esp's temp =", esp_temp_val)


