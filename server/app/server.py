# -*- coding: utf-8 -*-

import os
import redis
import manager
from config import REDIS_HOST, REDIS_PORT, REDIS_DB
from flask import Flask, abort, jsonify, make_response
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
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

@auth.error_handler
def unauthorized():
	return make_response(jsonify({ 'message' , 'Unauthorized access'}), 403)


class UserAPI(Resource):
	""" Class for the User resource."""

	def get(self, id):
		pass

	def put(self, id):
		pass

	def delete(self, id):
		pass

api.add_resource(UserAPI, '/users/<int:id>', endpoint = 'user')

post_fields = {
	'contents' : fields.String,
	'title' : fields.String,
	'tags' : fields.List(fields.String),
	'date' : fields.String,
	'uri' : fields.Url('post')
}

posts_fields = {
	'post' : fields.List(fields.Nested(post_fields))
}

class PostsAPI(Resource):
	"""Class for the Posts resource."""
	decorators = [auth.login_required]

	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('title', type = str, default = '', 
			location = 'json')
		self.reqparse.add_argument('contents', type = str, required = True,
			help = 'No post contents provided.', location = 'json')
		self.reqparse.add_argument('tags', type = str, action = 'append',
			default = '', location = 'json')
		super(PostsAPI, self).__init__()

	def get(self):
		posts = manager.get_posts(None)
		print "[SERVER] Returning: "
		return jsonify(posts=posts)

	def post(self):
		pass

class PostAPI(Resource):
	"""Class for the Post resource."""	
	decorators = [auth.login_required]

	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('title', type = str,	location = 'json')
		self.reqparse.add_argument('contents', type = str, location = 'json')
		self.reqparse.add_argument('tags', type = str, action = 'append',
			location = 'json')
		super(PostAPI, self).__init__()

	def get(self, id):
		post = manager.get_post(id)
		if post == None:
			abort(404)
		return { 'post' : marshal(post, post_fields) }


	def put(self, id):
		post = manager.get_post(id)
		if post == None:
			abort(404)
		args = self.reqparse.parse_args()
		post['title'] = args['title']
		post['contents'] = args['contents']
		post['tags'] = args['tags']
		manager.update_post(post)
		return { 'post': marshal(post, post_fields) }

	def delete(self, id):
		post = manager.get_post(id)
		if post == None:
			abort(404)
		manager.delete_post(id)
		return { 'result': True }

# 'add_resource' is used to register the routes with the framework.
# The endpoint is not necessary since Flask-RESTful generates one. 
api.add_resource(PostsAPI, '/yilpil/posts', endpoint = 'posts')
api.add_resource(PostAPI, '/yilpil/post/<int:id>', endpoint = 'post')

if __name__ == '__main__':
	# Populate database with test data
	manager.populate_test2()
	app.run(debug = True)
