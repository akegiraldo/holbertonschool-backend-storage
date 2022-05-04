#!/usr/bin/env python3
"""11. Where can I learn Python?"""


def schools_by_topic(mongo_collection, topic):
    """
    Function that returns the list of school
    having a specific topic
    """
    response = []
    schools = mongo_collection.find()
    for school in schools:
        if topic in school.get('topics', []):
            response.append(school)
    return response
