#!/usr/bin/env python3
"""Log stats"""
from pymongo import MongoClient


def get_log_stats(nginx_collection):
    """Provides some stats about Nginx
    logs stored in MongoDB"""
    logs = nginx_collection.count_documents({})
    print(f"{logs} logs")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")

    for method_ in methods:
        count = nginx_collection.count_documents({"method": method_})
        print(f"\tmethod {method_}: {count}")

    status_check = nginx_collection.count_documents(
                                    {"method": "GET", "path": "/status"})
    print(f"{status_check} status check")


if __name__ == "__main__":
    client = MongoClient('localhost' '27017')
    nginx_collection = client.logs.nginx
    get_log_stats(nginx_collection)
