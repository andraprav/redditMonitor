import praw
import json
import time
import constants as cst
import database
import helpers

db = database.DatabaseConfig()
reddit = praw.Reddit('monitor')
with open(cst.INPUT_FILENAME) as data_file:
    subreddits = json.load(data_file)

while True:
    helpers.loop_subreddits(subreddits, reddit, db)
    time.sleep(cst.script_limits['SLEEP_SECS'])
