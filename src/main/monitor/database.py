from pymongo import MongoClient
import pymongo

import constants as cst


class DatabaseConfig():
    def __init__(self):
        client = MongoClient(cst.mongodb['DB_CLIENT'], cst.mongodb['DB_PORT'])
        self.db = client.test
        self.db.items.create_index([('subreddit', pymongo.ASCENDING), ('date', pymongo.DESCENDING)], background=True)
        self.db.items.create_index([('text', pymongo.TEXT)], background=True)

    def save(self, json_data):
        self.db.items.save(json_data, True)