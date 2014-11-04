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
		self.reqparse.add_argument('username', type=str, required=True,
			location='json')
		self.reqparse.add_argument('mode', type=str, location='form')
		self.reqparse.add_argument('password', type=str, location='form')
		self.reqparse.add_argument('oldpassword', type=str, location='form')

		"""
		self.required.add_argument('oldpassword', type=str, required=True,
			location='json')
		"""
		super(UserAPI, self).__init__()

	def put(self, username):
		""" Handles PUT requests.
			If mode=CREATE : we wish to create a new user.
			If mode=UPDATE : we want to change an existing user's password.
		"""
		mode = str(request.form['mode'])
		password = str(request.form['password'])
		user = {'name': username, 'password': password }
		print "PUT %s USER: %s %s" % (mode, username, password)
		if mode == "CREATE":
			if manager.insert_user(username, password):
				return {'user': marshal(user, UserAPI.user_field)}
			else:
				abort(400) # Should be "User already created" or something.
		elif mode == "UPDATE":
			oldpassword = str(request.form['oldpassword'])
			if oldpassword == manager.get_password(username):
				manager.change_password(username, password)
				return {'user': marshal(user, UserAPI.user_field)}
			else:
				abort()
		else:
			abort(400)
	@auth.login_required
	def delete(self, username):
		if manager.delete_user(username):
			return 201 # Change
		else:
			abort(400) # Change

api.add_resource(UserAPI, '/yilpil/user/<string:username>', endpoint='user')


class PostAPI(Resource):
	"""Class for the Post resource."""	
	decorators = [auth.login_required]
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

	def get(self, id):
		print "GET POST id: " + str(id)
		post = manager.get_post(id)
		if post == None:
			abort(404)
		return { 'post' : marshal(post, PostAPI.post_field) }

	def put(self, id, username):
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

	def delete(self, id):
		post = manager.get_post(id)
		if post == None:
			abort(404)
		manager.delete_post(id)
		return { 'result': True }


class PostsAPI(Resource):
	"""Class for the Posts resource."""
	decorators = [auth.login_required]
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
		print "[SERVER] Returning: "
		return jsonify(posts=posts)

	def post(self):
		pass


# 'add_resource' is used to register the routes with the framework.
# The endpoint is not necessary since Flask-RESTful generates one. 
api.add_resource(PostsAPI, '/yilpil/posts/<string:username>', endpoint = 'posts')
api.add_resource(PostAPI, '/yilpil/post/<int:id>', endpoint = 'post')

if __name__ == '__main__':
	# Populate database with test data
	manager.populate_test2()
	app.run(debug = True)
