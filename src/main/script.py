import praw
from pymongo import MongoClient
import pymongo
import json
import time
from praw.models import Submission
from praw.models import Comment

# constants
DB_CLIENT = 'localhost'
DB_PORT = 27017
INPUT_FILENAME = 'resources/subreddits.json'
NEW_LIMIT = 1
SLEEP_SECS = 1


def format_and_save_item(item, subreddit):
    data = {'_id': item.id, 'date': item.created_utc, 'subreddit': subreddit}
    if type(item) == Submission:
        data['text'] = item.title
    elif type(item) == Comment:
        data['text'] = item.body
    save(data)


#
# def addTitle(data, submission):
#     data['text'] = submission.title
#
#
# def addBody(data, comment):
#     data['text'] = comment.body
#

def save(json):
    db.items.save(json, True)


def db_setup():
    client = MongoClient(DB_CLIENT, DB_PORT)
    db = client.test
    db.items.create_index([('subreddit', pymongo.ASCENDING), ('date', pymongo.DESCENDING)], background=True)
    db.items.create_index([('text', pymongo.TEXT)], background=True)
    return db


db = db_setup()
reddit = praw.Reddit('monitor')

with open(INPUT_FILENAME) as data_file:
    subreddits = json.load(data_file)
while True:
    for name in subreddits:
        subreddit = reddit.subreddit(name)
        for submission in subreddit.new(limit=NEW_LIMIT):
            submission.comment_sort = 'new'

            format_and_save_item(submission, name)
            if submission.num_comments > 0:
                comment = submission.comments[0]

                format_and_save_item(comment, name)

    time.sleep(SLEEP_SECS)
