import praw
from pymongo import MongoClient
import pymongo
import json
import time
from praw.models import Submission
from praw.models import Comment
import constants as cst


def format_and_save_item(item, subreddit):
    data = {'_id': item.id, 'date': item.created_utc, 'subreddit': subreddit}
    if type(item) == Submission:
        data['text'] = item.title
    elif type(item) == Comment:
        data['text'] = item.body
    save(data)


def save(json_data):
    db.items.save(json_data, True)


def db_setup():
    client = MongoClient(cst.mongodb['DB_CLIENT'], cst.mongodb['DB_PORT'])
    mongo_db = client.test
    mongo_db.items.create_index([('subreddit', pymongo.ASCENDING), ('date', pymongo.DESCENDING)], background=True)
    mongo_db.items.create_index([('text', pymongo.TEXT)], background=True)
    return mongo_db


db = db_setup()
reddit = praw.Reddit('monitor')

with open(cst.INPUT_FILENAME) as data_file:
    subreddits = json.load(data_file)
while True:
    for name in subreddits:
        subreddit = reddit.subreddit(name)
        for submission in subreddit.new(limit=cst.script_limits['NEW_LIMIT']):
            submission.comment_sort = 'new'

            format_and_save_item(submission, name)
            if submission.num_comments > 0:
                comment = submission.comments[0]

                format_and_save_item(comment, name)

    time.sleep(cst.script_limits['SLEEP_SECS'])
