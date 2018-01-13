"""Configuration"""

import os

# Twitter
TWITTER_CONSUMER_API_KEY = os.getenv('TWITTER_CONSUMER_API_KEY', 'api key')
TWITTER_CONSUMER_SECRET_KEY = os.getenv('TWITTER_CONSUMER_SECRET_KEY', 'secret key')

# Doge node
DOGECOIN_NODE_USERNAME = os.getenv('DOGECOIN_NODE_USERNAME', 'username')
DOGECOIN_NODE_PASSWORD = os.getenv('DOGECOIN_NODE_PASSWORD', 'password')
DOGECOIN_NODE_HOST = os.getenv('DOGECOIN_NODE_HOST', 'host')
DOGECOIN_NODE_PORT = os.getenv('DOGECOIN_NODE_PORT', 12345)

HOST = os.getenv('HOST', 'localhost')
PORT = os.getenv('PORT', 4000)
DEBUG = os.getenv('DEBUG', True)
RELOADER = os.getenv('RELOADER', True)

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///database.sqlite')

SALT = os.getenv('SALT', 'some salt')
SECRET_KEY = os.getenv('SECRET_KEY', 'secret key')
RECOVERY_KEY = os.getenv('RECOVERY_KEY', 'recovery key')

MAILGUN_KEY = os.getenv('MAILGUN_KEY', 'mailgun key')
MAILGUN_SANDBOX = os.getenv('MAILGUN_SANDBOX', 'mailgun sandbox')
