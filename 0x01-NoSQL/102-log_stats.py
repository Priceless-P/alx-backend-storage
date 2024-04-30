#!/usr/bin/env python3
"""Log stats"""
from pymongo import MongoClient
from collections import Counter


def get_log_stats(nginx_collection):
    """Provides some stats about Nginx
    logs stored in MongoDB"""
    logs = nginx_collection.count_documents({})
    print("{} logs".format(logs))
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")

    for method_ in methods:
        count = nginx_collection.count_documents({"method": method_})
        print("\tmethod {}: {}".format(method_, count))

    status_check = nginx_collection.count_documents(
                                    {"method": "GET", "path": "/status"})
    print("{} status check".format(status_check))
    count_ips = Counter(doc['ip'] for doc in nginx_collection.find({}, {"ip":1}))
    top_ten = count_ips.most_common(10)
    for ip, count in top_ten:
        print("      {}: {}".format(ip, count))

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx
    get_log_stats(nginx_collection)
