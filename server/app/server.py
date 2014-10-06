# -*- coding: utf-8 -*-
import os

from flask import flask
from flask.ext.restful import Api, Resource, reqparse, fields, marshal

from app import api, app, db

class UserAPI(Resource):
	""" Class for the User resource."""
	def get(self, id):
		pass

	def put(self, id):
		pass

	def delete(self, id):
		pass

api.add_resource(UserAPI, '/users/<int:id>', endpoint = 'user')

class PostsAPI(Resource):
	"""Class for the Posts resource."""

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
		pass

	def post(self):
		pass

class PostAPI(Resource):
	"""Class for the Post resource."""	
	
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('title', type = str,	location = 'json')
		self.reqparse.add_argument('contents', type = str, location = 'json')
		self.reqparse.add_argument('tags', type = str, action = 'append',
			location = 'json')

		super(PostAPI, self).__init__()

	def get(self, id):
		pass

	def put(self, id):
		pass

	def delete(self, id):
		pass

		

# 'add_resource' is used to register the routes with the framework.
# The endpoint is not necessary since Flask-RESTful generates one. 
api.add_resource(PostsAPI, '/yilpil/posts', endpoint = 'posts')
api.add_resource(PostAPI, '/yilpil/post/<int:id>', endpoint = 'post')

