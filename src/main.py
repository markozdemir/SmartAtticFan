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
relay_med  = machine.Pin(21, machine.Pin.OUT)
relay_high = machine.Pin(4, machine.Pin.OUT)

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
    global server_on, connected_wifi

    if server_on and connected_wifi:
        rpm_val = 0
        power_val = 0
        if temp > 26.7 or hum > 45:
            rpm_val = 1100
            power_val = 50

# TODO: CHANGE THIS LATER TO GET_RPM()
#        hs = machine.Pin(15, machine.Pin.IN)
        if hs.value() == 1:
            rpm_val = 0
        else:
            rpm_val = 1100

        json = { "type":"data_send_train",
                 "data": {  "temp (C)": temp,
                            "hum": hum,
                            "RPM": rpm_val,
                            "Power (W)": power_val,
                            "time": get_timestamp()
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
    
    rpm_val = (hall_count/time_passed)*60.0
    print("RPM: ", rpm_val)
    return rpm_val

 
def turn_all_relays_off():
    # check and turn off if any relays are on
    if relay_low.value() == 0:
        relay_low.value(1)
    if relay_med.value() == 0:
        relay_med.value(1)
    if relay_high.value() == 0:
        relay_high.value(1)
    return True


def set_relay_switch(gear):
    which_fan_speed = 0
    if turn_all_relays_off():
        if gear == 1:
            relay_low.value(0)
            which_fan_speed = 1
        elif gear == 2:
            relay_med.value(0)
            which_fan_speed = 2
        elif gear == 3:
            relay_high.value(0)
            which_fan_speed = 3
    return which_fan_speed


def run():
    global server_on, connected_wifi

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

    settime()
    print(get_timestamp())

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
        resp_dict = send_data(temp, hum, get_rpm())
        
        set_relay_switch(resp_dict['speed'])



    # get data from server
#    ap_if = network.WLAN(network.AP_IF)
#    huzz_ip = ap_if.ifconfig()[0]
#
#    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    s.bind(('0.0.0.0', 80))
#    s.listen(1)
#    while(1):
#        try:
#            (conn, address) = s.accept()
#        except OSError:
#            print("Nothing")
#        else:
#            print('Connection from %s' % str(address))
#            rec = conn.recv(4096)
#            # rec = rec.split(b'\r\n\r\n')
#            rec = str(rec)[2:-1]
#            print('----------\nAfter Split = ', rec)
#            post_data = (rec.split("PostData=")[-1])
#            post_data = post_data.replace('{', '')
#            post_data = post_data.replace('}', '')
#            post_data = post_data.replace('\"', '')
#            voiceCommand = post_data.split(":")[1]
#            print('Voice Command=<%s>' % voiceCommand)
#
#            ret_data = get_command(voiceCommand)
#
#            conn.send('HTTP/1.1 200 OK\n')
#            conn.send('Content-Type: text/html\n')
#            conn.send('Connection: close\n\n')
#            conn.sendall(ret_data)
#            conn.close()


    time.sleep(5)
    #10000
#    machine.deepsleep(10000)


#run()



    
#import esp32
## internal temp and hall sensor
#esp_hs_val = esp32.hall_sensor()
#esp_temp_val esp32.raw_temperature()
#print("esp's hall sens val = ", esp_hs_val)
#print("esp's temp =", esp_temp_val)


