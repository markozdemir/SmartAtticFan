'''==========================================
==== Columbia University - IoT EECS4764  ====
==== Yin Zhang, 4053                     ====
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

# Mongodb setup and other AI/ML/NN options
client = pymongo.MongoClient("mongodb://localhost:27017/")
DB = client["fan"]
db = DB["user"]
filename = "nn.sav"

# Server setup
end = "=============================================\n\n"
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
sock.bind(("0.0.0.0", 80));
sock.listen(1);


def send_response(code, msg, data, conn):
    if data is None:
        clientSocket.send("HTTP/1.1 "+str(code)+" "+str(msg)+"\r\n\r\n")
    else:
        clientSocket.send("HTTP/1.1 "+str(code)+" "+str(msg)+"\r\n"
             + str(json.dumps(data)) + "\r\n")
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
    if len(data) < 20:
        send_response(400, "Bad Request 2", None, conn)
        return None
    data = json.loads(data)
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

print("Smart Attic Fan Running!")
while(True):
    print("Waiting...")
    (clientSocket, clientAddress) = sock.accept();
    data = clientSocket.recv(1024)
    data = get_request_data(data, clientSocket)

    if data is None: # get_request_data returns None on error and handles response
        continue

    typ = data["type"]

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