#!/usr/bin/env python3
"""Log stats"""
from pymongo import MongoClient


def parse_log():
    """
    Provides some stats about
    Nginx logs stored in MongoDB
    """
    client = MongoClient('localhost', 27017)
    db = client.logs
    nginx_collection = db.nginx

    total_logs = nginx_collection.count_documents({})

    print(f"{total_logs} logs")

    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = nginx_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    count_status = nginx_collection.count_documents({"method": "GET",
                                                    "path": "/status"})
    print(f"{count_status} status check")


if __name__ == "__main__":
    parse_log()
