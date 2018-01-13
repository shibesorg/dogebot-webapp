"""Dogebot webapp"""

import os
import json
from datetime import datetime

import dataset
import tweepy
from beaker.middleware import SessionMiddleware
from bottle import (Bottle, get, post, request, error, static_file, template,
                    TEMPLATE_PATH, redirect, response, hook)
from bottle_utils import flash

from app.config import (DATABASE_URL, SALT, SECRET_KEY, MAILGUN_KEY,
                        MAILGUN_SANDBOX, RECOVERY_KEY, TWITTER_CONSUMER_API_KEY,
                        TWITTER_CONSUMER_SECRET_KEY, DOGECOIN_NODE_USERNAME,
                        DOGECOIN_NODE_PASSWORD, DOGECOIN_NODE_HOST, DOGECOIN_NODE_PORT)
from app.doge import DogeConnection
from app.db import users


app = Bottle()


# Create Dogecoin connection
doge = DogeConnection(
    DOGECOIN_NODE_USERNAME,
    DOGECOIN_NODE_PASSWORD,
    host=DOGECOIN_NODE_HOST,
    port=DOGECOIN_NODE_PORT,
)

# Install plugins
try:
    app.install(flash.message_plugin)
except Exception as e:
    print('Error: {0}'.format(e))


# Session setup
session_opts = {
    'session.cookie_expires': True,
    'session.encrypt_key': 'please use a random key and keep it secret!',
    'session.httponly': True,
    'session.timeout': 3600 * 24,  # 1 day
    'session.type': 'cookie',
    'session.validate_key': True,
    'session.auto': True,
}
app_session = SessionMiddleware(app, session_opts)


# Misc settings
PROJECT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH.insert(0, '{0}/templates'.format(PROJECT_PATH))


# Twitter API
auth = tweepy.OAuthHandler(TWITTER_CONSUMER_API_KEY, TWITTER_CONSUMER_SECRET_KEY)


# Session hook
@app.hook('before_request')
def setup_request():
    """Make session object accessible on all requests"""
    request.session = request.environ.get('beaker.session')


# Static files
@app.get('/static/<filename:path>')
def static_files(filename):
    """Serve static files"""
    return static_file(filename, root='{0}/static/'.format(PROJECT_PATH))


# Application routes
@app.get('/')
def index():
    """Serve home page"""

    if 'twitter_id' in request.session:
        return redirect('/app')

    twitter_redirect_url = auth.get_authorization_url()
    request.session['request_token'] = auth.request_token
    return template('index.html', twitter_redirect_url=twitter_redirect_url)


@app.get('/authenticate')
def authenticate():
    """get oauth token"""
    # Exchange request token
    token = request.session['request_token']
    request.session.pop('request_token', None)
    auth.request_token = token
    # Get verifier from request
    oauth_verifier = request.query.oauth_verifier
    # Get access token
    access_token = auth.get_access_token(oauth_verifier)
    # Create API object
    api = tweepy.API(auth)
    # User object from api
    twitter_user = api.me()
    twitter_id = twitter_user._json['id']
    # Get Today's date
    today = str(datetime.utcnow())
    # Attempt to grab user from database
    user = users.find_one(twitter_id=twitter_id)
    # Generate new address from authorized Twitter user
    dogecoin_address = doge.get_newaddress(str(twitter_id))

    # If the user is in the database we pretty much already have the
    # access token necesary to do Twitter API requests
    if user:
        user.update(dict(updated_at=today))
        request.session['twitter_id'] = twitter_id
        return redirect('/app')

    # If user is not in the database we create one
    try:
        users.insert(dict(
            twitter_id=twitter_id,
            created_at=today,
            updated_at=today,
            access_token=access_token[0],
            access_token_secret=access_token[1],
            address=dogecoin_address,
        ))
        request.session['twitter_id'] = twitter_id
    # TODO: Use a more specific exception
    except Exception as e:
        print(e)
        return redirect('/')

    # If everything went well, redirect user to the profile dashboard
    return redirect('/app')


@app.get('/app')
def application():
    """Profile dashboard"""
    if 'twitter_id' in request.session:
        user = users.find_one(twitter_id=request.session['twitter_id'])
        # Setup Twitter API
        auth.set_access_token(user['access_token'], user['access_token_secret'])
        api = tweepy.API(auth)
        # Get Twitter user-object
        twitter_user = api.me()
        twitter_json = twitter_user._json
        # Get Dogecoin balance
        balance = doge.get_balance(str(user['twitter_id']))
        return template(
            'index.html',
            screen_name=twitter_json['screen_name'],
            message=request.message,
            address=user['address'],
            balance=balance,
        )
    else:
        return redirect('/')


@app.get('/logout')
def logout():
    """Delete session"""
    if 'twitter_id' in request.session:
        request.session.delete()
    return redirect('/')


# Transaction routes
@app.post('/send')
def send():
    """Send Doge"""
    if 'twitter_id' in request.session:
        data = request.forms
        address = data.get('address')
        amount = data.get('amount')
        account_name = request.session['twitter_id']

        doge.send_from(
            str(account_name),
            address,
            amount,
            comment='Testing from shibes\' dogebot.'
        )
    else:
        return redirect('/')


# Error routes
@app.error(404)
def error404(err):
    """Page not found"""
    return template('error.html', error=err)


@app.error(500)
def error500(err):
    """Server error"""
    return template('error.html', error=err)
