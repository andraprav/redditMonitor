import praw
from pymongo import MongoClient
import pymongo
import json
import time

# constants
DB_CLIENT = 'localhost'
DB_PORT = 27017
INPUT_FILENAME = 'subreddits.json'
NEW_LIMIT = 1
SLEEP_SECS = 1


def formatItem(data, item, subreddit):
    data['_id'] = item.id
    data['date'] = item.created_utc
    data['subreddit'] = subreddit
    return data


def addTitle(data, submission):
    data['text'] = submission.title


def addBody(data, comment):
    data['text'] = comment.body


def save(json):
    db.items.save(json, True)


def dbSetup():
    client = MongoClient(DB_CLIENT, DB_PORT)
    db = client.test
    db.items.create_index([('subreddit', pymongo.ASCENDING), ('date', pymongo.DESCENDING)], background=True)
    db.items.create_index([('text', pymongo.TEXT)], background=True)
    return db


db = dbSetup()
reddit = praw.Reddit('monitor')

with open(INPUT_FILENAME) as data_file:
    subreddits = json.load(data_file)
while True:
    for name in subreddits:
        subreddit = reddit.subreddit(name)
        for submission in subreddit.new(limit=NEW_LIMIT):
            submission.comment_sort = 'new'

            data = {}
            addTitle(data, submission)
            json_data = formatItem(data, submission, name)
            save(json_data)

            if submission.num_comments > 0:
                comment = submission.comments[0]
                data = {}
                addBody(data, comment)
                json_data = formatItem(data, comment, name)
                save(json_data)
    time.sleep(SLEEP_SECS)
