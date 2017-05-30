from praw.models import Submission
from praw.models import Comment

import constants as cst


class Helper():
    def format_save(self, item, subreddit, db):
        data = self.format_item(item, subreddit)
        db.save(data)

    def format_item(self, item, subreddit):
        data = {'_id': item.id, 'date': item.created_utc, 'subreddit': subreddit}
        if type(item) == Submission:
            data['text'] = item.title
        elif type(item) == Comment:
            data['text'] = item.body
        return data

    def loop_subreddits(self, subreddits, reddit, db):
        for name in subreddits:
            subreddit = reddit.subreddit(name)
            # take the newest submission and the newest comment
            for submission in subreddit.new(limit=cst.script_limits['NEW_LIMIT']):
                submission.comment_sort = 'new'
                self.format_save(submission, name, db)
                if submission.num_comments > 0:
                    comment = submission.comments[0]
                    self.format_save(comment, name, db)
