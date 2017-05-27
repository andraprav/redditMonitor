from flask import Flask
from flask import request
from bson.json_util import dumps
from flask_pymongo import PyMongo
import pymongo

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'test'
mongo = PyMongo(app, config_prefix='MONGO')


@app.route('/items/', methods=['GET'])
def items():
    subreddit = request.args.get('subreddit')
    t1 = float(request.args.get('from'))
    t2 = float(request.args.get('to'))
    result = dumps(mongo.db.items.find({'subreddit': subreddit, 'date': {'$gt': t1, '$lt': t2}}).sort(
            'date', pymongo.DESCENDING))
    return result


if __name__ == '__main__':
    app.run()
