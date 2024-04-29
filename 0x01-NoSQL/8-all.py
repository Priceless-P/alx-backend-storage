#!/usr/bin/env python3
"""List all documents in Python"""


def list_all(mongo_collection):
    """Lists all documents in a collection"""
    return [document for document in mongo_collection.find()]
