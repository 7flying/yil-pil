# -*- coding: utf-8 -*-
from flask import Flask

# Flask general
app = Flask(__name__, static_url_path='')
app.config.from_object('config')

from app.routes import index
from base64 import b64decode
import redis
import manager
from app.config import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD, \
    SECRET_KEY, DEBUG, SSL_DISABLE
from flask import abort, jsonify
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
from flask.ext.httpauth import HTTPBasicAuth
from flask_sslify import SSLify
from werkzeug.security import check_password_hash
from werkzeug.contrib.fixers import ProxyFix
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature

# Restful api
api = Api(app)

# Redis
db = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB,
                       password=REDIS_PASSWORD)

# Authentication
auth = HTTPBasicAuth()

if not DEBUG and not SSL_DISABLE:
    # SSL
    sslify = SSLify(app, subdomains=True)
    # Reverse proxy stuff
    app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
    # Populate database with test data
    manager.populate_test2()
    app.run(debug=True)
