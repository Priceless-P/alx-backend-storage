#!/usr/bin/env python3
"""Insert a document in Python"""


def insert_school(mongo_collection, **kwargs):
    """Lists all documents in a collection"""
    new_item = mongo_collection.insert_one(kwargs)
    return new_item.inserted_id
