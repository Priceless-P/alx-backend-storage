#!/usr/bin/env python3
"""Log stats"""
from pymongo import MongoClient


def get_log_stats(nginx_collection):
    """Provides some stats about Nginx
    logs stored in MongoDB"""
    logs = nginx_collection.count_documents({})
    print("{} logs".format(logs))
    methods = ["GET", "POST", "PUT", "PATCH", "DELTE"]
    print("Methods:")
    for method_ in methods:
        print("\tmethod: {}".format(nginx_collection.
                                    count_documents({"method": method_})))

    status_check = nginx_collection.count_documents(
                                    {"method": "GET", "path": "/status"})
    print("{} status check".format(status_check))


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx
    get_log_stats(nginx_collection)