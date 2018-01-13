from bottle import request
from db import users


def setup_cookie(twitter_id, name='twitter_id'):
    session = request.environ.get('beaker.session')
    session[name] = twitter_id
    session.save()


def current_user():
    session = request.environ.get('beaker.session')
    twitter_id = session.get('twitter_id', None)
    user = users.find_one(twitter_id=twitter_id)
    return user
