from flask import Flask
from flask import request
from bson.json_util import dumps
from flask_pymongo import PyMongo
import pymongo
from flask import abort

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'test'
mongo = PyMongo(app, config_prefix='MONGO')


@app.route('/items/', methods=['GET'])
def items():
    subreddit = request.args.get('subreddit')
    t1 = request.args.get('from')
    t2 = request.args.get('to')
    keyword = request.args.get('keyword')
    if not subreddit or not t1 or not t2:
        abort(400)
    query = {'subreddit': subreddit, 'date': {'$gt': float(t1), '$lt': float(t2)}}
    if (keyword):
        query['text'] = {'$regex': keyword}
    result = dumps(mongo.db.items.find(query).sort('date', pymongo.DESCENDING))
    return result


if __name__ == '__main__':
    app.run()
