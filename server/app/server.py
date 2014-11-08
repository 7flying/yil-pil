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
		'email' : fields.String,
		'password' : fields.String
	}

	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('username', type=str, location='form')
		self.reqparse.add_argument('email', type=str, location='form')
		self.reqparse.add_argument('password', type=str, location='form')
		super(UserAPI, self).__init__()

	def post(self, username): #OK
		""" Handles POST requests to create new users."""
		password = self.reqparse.parse_args()['password']
		email = self.reqparse.parse_args()['email']
		user = {'name': username, 'password': password, 'email' : email}
		print "POST USER: %s %s" % (username, password)
		if manager.insert_user(username, password, email):
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

	response_post_field = {
		'contents' : fields.String,
		'title' : fields.String,
		'tags' : fields.List(fields.String),
		'date' : fields.String,
		'id' : fields.Integer,
		'author' : fields.String,
		'votes' : fields.Integer
	}

	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('title', type = str,	location = 'form')
		self.reqparse.add_argument('contents', type = str, location = 'form')
		self.reqparse.add_argument('tags', type = str, action = 'append',
			location = 'form')
		self.reqparse.add_argument('username', type=str, location='form')
		super(PostAPI, self).__init__()

	def get(self, id): #OK
		""" Gets a post given its id."""
		print "[ SERVER ] GET POST id: " + str(id)
		post = manager.get_post(id)
		if post == None:
			abort(404)
		return { 'post' : marshal(post, PostAPI.response_post_field) }

	@auth.login_required
	def post(self, id): # OK
		""" Handles a POST request. Creates a new post. """
		print "[ SERVER ] POST a post"
		args = self.reqparse.parse_args()
		post = {}
		post['contents'] = args['contents']
		post['title'] = args['title']
		post['tags'] = args['tags']
		user = args['username']
		created_post = manager.insert_post(post, user)
		return {'post': marshal(created_post, PostAPI.response_post_field)}

	@auth.login_required
	def put(self, id): # OK
		""" Handles PUT request. Updates an existing post data."""
		print "[ SERVER ] PUT POST id:", str(id)
		post = manager.get_post(id)
		if post == None:
			abort(404)
		args = self.reqparse.parse_args()
		if 'username' in args.keys():
			username = args['username']
			if 'title' in args.keys():
				post['title'] = args['title']
			if 'post' in args.keys():
				post['contents'] = args['contents']
			if 'tags' in args.keys():
				post['tags'] = args['tags']
			post = manager.update_post(post, id, username)
			return { 'post': marshal(post, PostAPI.post_field) }
		else:
			abot(404)

	@auth.login_required
	def delete(self, id): # OK
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
		super(PostsAPI, self).__init__()

	def get(self, username): #OK, but review jsonify again
		# Get posts given a username
		posts = manager.get_posts(username)
		print "[ SERVER ] Returning: "
		return jsonify(posts=posts)

api.add_resource(PostsAPI, '/yilpil/posts/<string:username>', endpoint = 'posts')


class TagsAPI(Resource):
	""" Class for the tags resource."""
	def __init__(self):
		super(TagsAPI, self).__init__()

	def get(self, user): #OK
		""" Gets all the tags used by a user."""
		print "[ SERVER ] Get '", user, "'s tags"
		return manager.get_user_tags(user)
		
api.add_resource(TagsAPI, '/yilpil/tags/<string:user>', endpoint = 'tags')

class VotingAPI(Resource):
	""" Class for voting a post. """
	decorators = [auth.login_required]

	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('up', type=bool, location='form',
			required=True)
		self.reqparse.add_argument('username', type=str, location='form',
			required=True)
		super(VotingAPI, self).__init__()

	def put(self, post_id):
		""" PUT request. Updates the value of the post by a vote up or down. """
		print "[ SERVER ] Vote to post ", post_id
		args = self.reqparse.parse_args()
		res = None
		if args['up']:
			# vote up
			res = manager.vote_positive(post_id, args['username'])
		else:
			# vote down
			res = manager.vote_negative(post_id, args['username'])
		if res == None:
			return "Post-id not found", 404
		if res:
			return "Vote stored", 200
		else:
			return "Already voted on that post", 200

api.add_resource(VotingAPI, '/yilpil/voting/<int:post_id>', endpoint='voting')	

if __name__ == '__main__':
	# Populate database with test data
	manager.populate_test2()
	app.run(debug = True)
