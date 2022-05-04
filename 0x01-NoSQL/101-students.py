#!/usr/bin/env python3
"""14. Top students"""


def top_students(mongo_collection):
    """
    Function that returns all students sorted by average score
    """
    students = mongo_collection.find()
    for student in students:
        topics = student.get('topics', [])
        size = len(topics)
        accumulated = 0
        for topic in topics:
            accumulated += topic.get('score')
        avg = accumulated / size
        mongo_collection.update_many(
            { 'name': student.get('name') },
            { '$set': { 'averageScore': avg } }
        )

    return mongo_collection.find().sort('averageScore', -1)
