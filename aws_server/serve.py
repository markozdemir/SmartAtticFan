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


# Mongodb setup and other AI/ML/NN options
client = pymongo.MongoClient("mongodb://localhost:27017/")
DB = client["fan"]
db = DB["user"]
filename = "nn.sav"
users = client["users"]
user_db = users["user"]

# Server setup
end = "=============================================\n\n"
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
sock.bind(("0.0.0.0", 80));
sock.listen(1);

# data configs
temp_data_list = ["temp", "hum"]

# location info
longitude = 0
latitude = 0

def register_user(data):
    user_db.remove({})
    r = user_db.insert(data)
    send_register_email(data['name'], data['email'])

def send_push():
    Process=Popen('./send_push.sh', shell=True)

def send_push_new():
    Process=Popen('./send_push_new.sh', shell=True)

def send_fail_email(to, name):
    Process=Popen('./send_email.sh %s %s' % (name, to), shell=True)
    send_push()

def send_register_email(to, name):
    Process=Popen('./send_reg_email.sh %s %s' % (to, name), shell=True)
    send_push_new()

def is_fan_broken(RPM, temp):
    if RPM < 10:
        if temp > 31:
            return True
    return False

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

while True:
    print("Waiting...")
    (clientSocket, clientAddress) = sock.accept();
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
            v = 1
        send_response(200, "OK", {"valid": str(v), "name":name, "email":email}, clientSocket) # also closes conn
        continue

    if typ == "android_register":
        register_user(data['data'])
        send_response(200, "OK", None, clientSocket) # also closes conn
        continue

    if "req_LR" in typ:
        x = "HTTP/1.1 200 OK\r\n\r\n\r\n"
        num_b = 0
        with open('linearR_pred_temp.png', 'r') as file:
            x = file.read()
        num_b = len(x)
        send_response(200, "OK", x, clientSocket) # also closes conn
        continue

    if "req_knn" in typ:
        x = "HTTP/1.1 200 OK\r\n\r\n\r\n"
        num_b = 0
        with open('knn_pred_temp.png', 'r') as file:
            x = file.read()
        num_b = len(x)
        send_response(200, "OK", x, clientSocket) # also closes conn
        continue

    if "req_relationships" in typ:
        x = "HTTP/1.1 200 OK\r\n\r\n\r\n"
        num_b = 0
        with open('relationship.png', 'r') as file:
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
                    x[str(zz)] = z[zz] + 946684800
                else:
                    x[str(zz)] = z[zz]
            if x is not {} and len(x) != 0:
                h[str(id_)] = x
                id_ += 1

        temp, desc = lw.get_weather(longitude, latitude)
        h2 = {}
        h2["recent"] = h[str(id_ - 1)]
        is_broke = is_fan_broken(h2["recent"]["RPM"], h2["recent"]["temp (C)"])
        h2["broke"] = is_broke
        h2["local_temp"] = temp
        h2["local_desc"] = desc
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
        elif "test" in typ:
            pass
        elif "print" in typ:
            data_print(data)

    send_response(200, "OK", None, clientSocket) # also closes conn

