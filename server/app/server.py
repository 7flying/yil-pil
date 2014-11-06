#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import redis
import manager
from config import REDIS_HOST, REDIS_PORT, REDIS_DB
from flask import Flask, abort, jsonify, make_response, request
from flask.ext.restful import Api, Resource, reqparse, fields, marshal, \
	 marshal_with
from flask.ext.httpauth import HTTPBasicAuth

# Flask general
app = Flask(__name__)

# Restful api
api = Api(app)

# Redis
db = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

# Authentication
auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
	return manager.get_password(username)


class UserAPI(Resource):
	""" Class for the User resource."""
	user_field = {
		'name' : fields.String,
		'password' : fields.String
	}

	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('username', type=str, location='json')
		self.reqparse.add_argument('password', type=str, location='form')
		super(UserAPI, self).__init__()

	def post(self, username): #OK
		""" Handles POST requests to create new users."""
		#mode = str(request.form['mode'])
		password = self.reqparse.parse_args()['password']
		user = {'name': username, 'password': password }
		print "POST USER: %s %s" % (username, password)
		if manager.insert_user(username, password):
			return {'user': marshal(user, UserAPI.user_field)}
		else:
			abort(400) # Should be "User already created" or something.

	@auth.login_required
	def put(self, username): #OK
		""" Handles PUT requests to update existing users."""
		password = self.reqparse.parse_args()['password']
		#password = str(request.form['newpassword'])
		if manager.change_password(username, password):
			user = {}
			user['name'] = username
			user['password'] = password
			return {'user': marshal(user, UserAPI.user_field)} # Igual mejor un 200
		

	@auth.login_required
	def delete(self, username): #OK
		""" Hanldes DELETE requests to delete an existing user."""
		print "DELETE USER: %s", username
		if manager.delete_user(username):
			return 200 # Change "Ok, created"
		else:
			abort(400) # Change

api.add_resource(UserAPI, '/yilpil/user/<string:username>', endpoint='user')


class PostAPI(Resource):
	"""Class for the Post resource."""	
	post_field = {
		'contents' : fields.String,
		'title' : fields.String,
		'tags' : fields.List(fields.String),
		'date' : fields.String
	}

	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('title', type = str,	location = 'json')
		self.reqparse.add_argument('contents', type = str, location = 'json')
		self.reqparse.add_argument('tags', type = str, action = 'append',
			location = 'json')
		self.reqparse.add_argument('username', type=str, location='form')
		super(PostAPI, self).__init__()

	def get(self, id): #OK
		""" Gets a post given its id."""
		print "GET POST id: " + str(id)
		post = manager.get_post(id)
		if post == None:
			abort(404)
		return { 'post' : marshal(post, PostAPI.post_field) }

	def put(self, id, username): # TODO: REVIEW
		""" Handles PUT request. Updates an existing post data."""
		print "PUT POST id:", str(id)
		post = manager.get_post(id)
		if post == None:
			abort(404)
		args = self.reqparse.parse_args()
		post['title'] = args['title']
		post['contents'] = args['contents']
		post['tags'] = args['tags']
		manager.update_post(post, id, username)
		return { 'post': marshal(post, PostAPI.post_field) }

	@auth.login_required
	def delete(self, id):
		""" Deletes an existing post."""
		username = self.reqparse.parse_args()['username']
		print "[ SERVER ] DELETE POST id:", id,"user", username
		post = manager.get_post(id)
		#if post == None:
		#abort(404)
		if manager.delete_post(id, username):
			return 200 # Ok. Post deleted
		else:
			return 404 # Meaning post not found

# 'add_resource' is used to register the routes with the framework.
# The endpoint is not necessary since Flask-RESTful generates one. 
api.add_resource(PostAPI, '/yilpil/post/<int:id>', endpoint = 'post')


class PostsAPI(Resource):
	"""Class for the Posts resource."""
	posts_fields = {
		'posts' : fields.List(fields.Nested(PostAPI.post_field))
	}

	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('title', type = str, default = '', 
			location = 'json')
		self.reqparse.add_argument('contents', type = str, required = True,
			help = 'No post contents provided.', location = 'json')
		self.reqparse.add_argument('tags', type = str, action = 'append',
			default = '', location = 'json')
		super(PostsAPI, self).__init__()

	def get(self, username):
		posts = manager.get_posts(username)
		print "[ SERVER ] Returning: "
		return jsonify(posts=posts)

	def post(self):
		pass

api.add_resource(PostsAPI, '/yilpil/posts/<string:username>', endpoint = 'posts')

if __name__ == '__main__':
	# Populate database with test data
	manager.populate_test2()
	app.run(debug = True)
