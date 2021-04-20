'''==========================================
==== Columbia University - IoT EECS4764  ====
==== Yin Zhang, yz4053                   ====
==== James Mastran, jam2454              ====
==== Mark Ozdemir, mo2804                ====
=========================================='''
# This file hosts our server "in the cloud"
# where the fan can communicate with via
# sending HTTP requests

import socket
import ssl
import json
import pymongo
import requests
import random
import pickle
import time
from sklearn import svm
import local_weather as lw
import local_time as lt
from subprocess import Popen
import signal
import sys
import data_obtainer as do

# Mongodb setup and other AI/ML/NN options
client = pymongo.MongoClient("mongodb://localhost:27017/")
DB = client["fan2"]
db = DB["user"]
filename = "nn.sav"
users = client["users"]
user_db = users["user"]

# Server setup
end = "=============================================\n\n"
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
sock.bind(("0.0.0.0", 80));
sock.listen(1);
def signal_handler(signal, frame):
        sock.close()
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

# data configs
temp_data_list = ["temp", "hum"]

# location info
longitude = 0
latitude = 0

# fan info
fan_speed = -1
is_broke = False
time_fail_sent = 0
user_off = False

def get_power(x):
    if is_broke:
        return 0
    if x == 0:
        return 0
    elif x == 1:
        return 17
    elif x == 2:
        return 22
    elif x == 3:
        return 25

    return -1

def get_user_details():
    name = None
    email = None
    image = None
    row = user_db.find()
    for r in row:
        print(r)
        name = r['name']
        email = r['email']
        image = r['image']
    return name, email, image

def register_user(data):
    user_db.remove({})
    r = user_db.insert(data)
    send_register_email(data['name'], data['email'])

def send_push():
    Process=Popen('./other/send_push.sh', shell=True)

def send_push_new():
    Process=Popen('./other/send_push_new.sh', shell=True)

def send_fail_email(to, name):
    global time_fail_sent
    threshold = 3600
    if time.time() - time_fail_sent > threshold:
        Process=Popen('./other/send_email.sh %s %s' % (name, to), shell=True)
        send_push()
        time_fail_sent = time.time()

def send_register_email(to, name):
    Process=Popen('./other/send_reg_email.sh %s %s' % (to, name), shell=True)
    send_push_new()

def is_fan_broken(RPM):
    global is_broke, fan_speed
    if fan_speed > 0 and RPM < 10:
            is_broke = True
            return True
    is_broke = False
    return False

def handle_failure(rpm):
    if is_fan_broken(rpm):
        name, email, _ = get_user_details()
        send_fail_email(email, name)
        send_push()
        print("Fan is broken! - notified user")
        return True
    return False

def trigger_ai():
    pass

def get_fan_speed_from_ai():
    global fan_speed

    if user_off:
        fan_speed = 0
        return 0

    d = db.find({})
    h = {}
    id_ = 1
    for z in d:
        x = {}
        for zz in z:
            if zz is "time":
                x[str(zz)] = z[zz] + 946684800
            else:
                x[str(zz)] = z[zz]
        if x is not {} and len(x) != 0:
            h[str(id_)] = x
            id_ += 1
    h2 = {}
    h2["recent"] = h[str(id_ - 1)]
    print("RECENT:", h2)
    if "temp (C)" in h2["recent"]:
        if h2["recent"]["temp (C)"] > 20:
            l = [1, 2, 3]
            fan_speed = random.choice(l)
        else:
            fan_speed = 0
    else:
        print("temp is not in recent!")
        fan_speed = 0
    return fan_speed

def send_response(code, msg, data, conn):
    if data is None:
        clientSocket.sendall("HTTP/1.1 "+str(code)+" "+str(msg)+"\r\n\r\n")
    else:
        clientSocket.sendall("HTTP/1.1 200 OK\r\n"
            +"Content-Type: text/html\r\n"
            +"\r\n"
            +str(data)+"")
    print("Sending response with code and msg:", code, msg)
    clientSocket.close()
    print(end)

# Some functions
def get_request_data(data, conn):
    # This function takes a raw request
    # and gets the json data payload
    # returns None if misformat in request
    data = data.split("\r\n\r\n")
    if len(data) > 1:
        data = data[1]
    else:
        send_response(400, "Bad Request 1", None, conn)
        return  None
    if len(data) < 10:
        send_response(400, "Bad Request 2", None, conn)
        return None
    try:
        data = json.loads(data)
    except:
        send_response(400, "Bad Request 2", None, conn)
        return None
    print("Processing request: "+ data["type"])
    return data

def data_print(data):
        strr = ""
        data_vals = data["data"]
        for k in data_vals:
            strr += "\t" + k + ": " + str(data_vals[k]) + "\n"
        print("Got data:\n" + str(strr))

def ins_data_to_mongo(data):
        r = db.insert(data)
        print("Inserted data")

def set_location(location_hash):
    global longitude, latitude
    longitude = location_hash["longitude"]
    latitude = location_hash["latitude"]
    temp, desc = lw.get_weather(longitude, latitude)
    print("local weather:", temp, desc)

def make_graphs():
    Process=Popen('./other/gen_graphs.sh', shell=True)

make_graphs()
while True:
    print("Waiting...")
    if user_off:
        print("User turned fan off!")
    try:
        (clientSocket, clientAddress) = sock.accept();
    except KeyboardInterrupt:
        sock.close()
        break
    except Exception as e:
        print("error handled...?", e)
        continue
    data = ""
    clientSocket.settimeout(.3)
    while True:
        d = None
        try:
            d =  clientSocket.recv(1024)
        except:
            pass
        print(d)
        if not d or d is None:
            break
        data += d
    data = get_request_data(data, clientSocket)

    if data is None: # get_request_data returns None on error and handles response
        continue

    typ = data["type"]
    if typ == "check":
        location = data["data"]
        set_location(location)
        send_response(200, "OK", lt.get_curr_time(), clientSocket) # also closes conn
        continue

    if typ == "android_check":
        row = user_db.find({})
        name = None
        email = None
        v = 0
        for r in row:
            print(r)
            name = r['name']
            email = r['email']
            image = r['image']
            v = 1
        print("Here")
        send_response(200, "OK", {"valid": str(v), "name":name, "email":email, "image":image, "is_broke": is_broke}, clientSocket) # also closes conn
        continue

    if typ == "android_register":
        register_user(data['data'])
        send_response(200, "OK", None, clientSocket) # also closes conn
        continue

    if typ == "android_toggle_fan":
        user_off = data['data']['off']
        if 'rue' in user_off:
            user_off = True
        elif "alse" in user_off:
            user_off = False
        print("TOGGLED:", user_off)
        send_response(200, "OK", {"user_off": user_off}, clientSocket) # also closes conn
        continue

    if "req_temp_time" in typ:
        x = "HTTP/1.1 200 OK\r\n\r\n\r\n"
        num_b = 0
        with open('./model/temp_time.png', 'r') as file:
            x = file.read()
        num_b = len(x)
        send_response(200, "OK", x, clientSocket) # also closes conn
        continue
    if "req_hum_time" in typ:
        x = "HTTP/1.1 200 OK\r\n\r\n\r\n"
        num_b = 0
        with open('./model/hums_time.png', 'r') as file:
            x = file.read()
        num_b = len(x)
        send_response(200, "OK", x, clientSocket) # also closes conn
        continue
    if "req_rpm_time" in typ:
        x = "HTTP/1.1 200 OK\r\n\r\n\r\n"
        num_b = 0
        with open('./model/rpm_time.png', 'r') as file:
            x = file.read()
        num_b = len(x)
        send_response(200, "OK", x, clientSocket) # also closes conn
        continue

    if "req_LR" in typ:
        x = "HTTP/1.1 200 OK\r\n\r\n\r\n"
        num_b = 0
        with open('./model/linearR_pred_temp.png', 'r') as file:
            x = file.read()
        num_b = len(x)
        send_response(200, "OK", x, clientSocket) # also closes conn
        continue

    if "req_knn" in typ:
        x = "HTTP/1.1 200 OK\r\n\r\n\r\n"
        num_b = 0
        with open('./model/knn_pred_temp.png', 'r') as file:
            x = file.read()
        num_b = len(x)
        send_response(200, "OK", x, clientSocket) # also closes conn
        continue

    if "req_relationships" in typ:
        x = "HTTP/1.1 200 OK\r\n\r\n\r\n"
        num_b = 0
        with open('./model/relationship.png', 'r') as file:
            x = file.read()
        num_b = len(x)
        send_response(200, "OK", x, clientSocket) # also closes conn
        continue


    if "req_data_nn" in typ:
        x = ""
        with open('nn_test_junk.sav', 'r') as file:
            x = file.read().replace('\n', ' ')
        x += "\r\nEND"
        print("Sending...", x)
        send_response(200, "OK", x, clientSocket) # also closes conn
        continue

    if "req_data_climate" in typ:
        d = db.find({})
        h = {}
        id_ = 1
        for z in d:
            x = {}
            for zz in z:
                # if zz not in temp_data_list:
                #    print(zz, "not in list")
                #    continue
                if zz is "time":
                    if z[zz] < 1618802818:
                        x[str(zz)] = z[zz] + 946684800
                    else:
                        x[str(zz)] = z[zz]
                else:
                    x[str(zz)] = z[zz]
            if x is not {} and len(x) != 0:
                h[str(id_)] = x
                id_ += 1

        temp, desc = lw.get_weather(longitude, latitude)
        h2 = {}
        h2["recent"] = h[str(id_ - 1)]
        get_fan_speed_from_ai()
        handle_failure(h2["recent"]["RPM"],)
        h2["broke"] = is_broke
        h2["local_temp"] = temp
        h2["local_desc"] = desc
        h2["recent"]["power"] = get_power(fan_speed)
        print("Sending local weather:", temp, desc)
        x = str(h2)
        x += "\r\nEND"
        print("Sending...", x)
        send_response(200, "OK", x, clientSocket) # also closes conn
        continue

    if "data_send" in typ:

        if "data" not in data:
            send_response(400, "Bad Request - missing data", None, clientSocket)
            continue

        if "train" in typ:
            ins_data_to_mongo(data['data'])
            trigger_ai()
            get_fan_speed_from_ai()
            print("Sending fan speed:", fan_speed)
            handle_failure(data['data']['RPM'])
            make_graphs()
            send_response(200, "OK", {"speed": fan_speed}, clientSocket) # also closes conn
            continue
        elif "test" in typ:
            pass
        elif "print" in typ:
            data_print(data)

    send_response(200, "OK", None, clientSocket) # also closes conn

