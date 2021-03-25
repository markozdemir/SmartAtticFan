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
import requests as urequests
import random as urandom
import pickle
import time
from sklearn import svm

# Mongodb setup and other AI/ML/NN options
client = pymongo.MongoClient("mongodb://localhost:27017/")
trainDB = client["fan"]
trainCollection = trainDB["user"]
filename = "nn.sav"

# Server setup
end = "=============================================\n\n"
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
sock.bind(("0.0.0.0", 80));
sock.listen(1);


def send_response(code, msg, data, conn):
    clientSocket.send("HTTP/1.1 "+str(code)+" "+str(msg)+"\r\n"
            +"\r\n")
            # +str(json.dumps(data)) if data is not None else "" +"\r\n")
    print("Sending response with code and msg:", code, msg)
    clientSocket.close()

# Some functions
def get_request_data(data, conn):
    # This function takes a raw request
    # and gets the json data payload
    # returns None if misformat in request
    data = data.split("\r\n\r\n")
    if len(data) > 1:
        data = data[1]
    else:
        send_response(400, "Bad Request", None, conn)
        return  None
    if len(data) < 20:
        send_response(400, "Bad Request", None, conn)
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

print("Smart Attic Fan Running!")
import time
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
            send_response(400, "Bad", None, clientSocket)
            continue

        if "train" in typ:
            pass
        elif "test" in typ:
            pass
        elif "print" in typ:
            data_print(data)

    send_response(200, "OK", None, clientSocket) # also closes conn
    print(end)
