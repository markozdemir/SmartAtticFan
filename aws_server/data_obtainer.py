'''==========================================
==== Columbia University - IoT EECS4764  ====
==== Yin Zhang, yz4053                   ====
==== James Mastran, jam2454              ====
==== Mark Ozdemir, mo2804                ====
=========================================='''
# This file contains code that will retrieve
# data from Mongo DB and convert to a specific
# format
import json
import pymongo
import time

def get_array_of_hashes(mongo_data, field_array):
    # field_hash contains the headers/fields wanted and in what order
    data = []
    for data_point in mongo_data:
        data_fmt ={}
        for f in field_array:
            if f in data_point:
                if f is "time" and data_point[f] < 970697983:
                    data_fmt[f] = data_point[f] + 946684800
                else:
                    data_fmt[f] = data_point[f]
            else:
                data_fmt = None
                break
        if data_fmt is not None:
            data.append(data_fmt)
    return data

def get_array_of_arrays(mongo_data, field_array):
    # field_hash contains the headers/fields wanted and in what order
    data = []
    for data_point in mongo_data:
        data_fmt = []
        for f in field_array:
            if f in data_point:
                if f is "time" and data_point[f] < 970697983:
                    data_fmt.append(data_point[f] + 946684800)
                else:
                    data_fmt.append(data_point[f])
            else:
                data_fmt = None
                break
        if data_fmt is not None:
            data.append(data_fmt)
    return data

def get_array_of_tuples(mongo_data, field_array):
    # field_hash contains the headers/fields wanted and in what order
    data = []
    for data_point in mongo_data:
        data_fmt = []
        for f in field_array:
            if f in data_point:
                if f is "time" and data_point[f] < 970697983:
                    data_fmt.append(data_point[f] + 946684800)
                else:
                    data_fmt.append(data_point[f])
            else:
                data_fmt = None
                break
        if data_fmt is not None:
            tuple_fmt = tuple(data_fmt)
            data.append(tuple_fmt)
    return data

def get_data(db_name, fields, type_of_convert):
    # db_name should be "fan"
    # fields contains the headers/fields wanted and in that order
    # type_of_convert can be array of arrays or tuples or hashes

    client = pymongo.MongoClient("mongodb://localhost:27017/")
    DB = client[db_name]
    db = DB["user"]
    mongo_data = db.find({})
    out = None

    if type_of_convert == "tuple":
        out = get_array_of_tuples(mongo_data, fields)
    elif type_of_convert == "array":
        out = get_array_of_arrays(mongo_data, fields)
    elif type_of_convert == "hash":
        out = get_array_of_hashes(mongo_data, fields)

    return out
