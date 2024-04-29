#!/usr/bin/env python3
"""Where can I learn Python?"""


def schools_by_topic(mongo_collection, topic):
    """Lists all documents in a collection"""
    documents = mongo_collection.find({'topics': topic})
    return list(documents)
