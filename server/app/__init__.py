# -*- coding: utf-8 -*-
from flask import Flask

# Flask general
app = Flask(__name__, static_url_path='')
app.config.from_object('config')

from app.routes import index

import os
import redis
import manager
from config import REDIS_HOST, REDIS_PORT, REDIS_DB
from flask import abort, jsonify, make_response, request, \
	render_template, make_response
from flask.ext.restful import Api, Resource, reqparse, fields, marshal, \
	 marshal_with
from flask.ext.httpauth import HTTPBasicAuth
from flask_sslify import SSLify
from werkzeug.security import generate_password_hash, check_password_hash

# Restful api
api = Api(app)

# Redis
db = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

# Authentication
auth = HTTPBasicAuth()

# SSL
sslify = SSLify(app, subdomains=True)

_DEBUG_ = True

def debug(to_print):
	if _DEBUG_:
		print "[ SERVER ] ", to_print

@auth.verify_password
def verify_password(username, password):
	db_pass = manager.get_password(username)
	return check_password_hash(db_pass, password)

class UsersAPI(Resource):
	""" Class for the User resource."""
	user_field = {
		'name' : fields.String,
		'email' : fields.String
	}

	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('username', type=str, location='form')
		self.reqparse.add_argument('email', type=str, location='form')
		self.reqparse.add_argument('password', type=str, location='form')
		super(UsersAPI, self).__init__()

	def post(self, username): #OK
		""" Handles POST requests to create new users."""
		password = self.reqparse.parse_args()['password']
		email = self.reqparse.parse_args()['email']
		user = {'name': username, 'password': password, 'email' : email}
		debug("POST USER: " + username + ":" + password)
		if manager.insert_user(username, password, email):
			return {'user': marshal(user, UsersAPI.user_field)}
		else:
			abort(400) # Should be "User already created" or something.

	@auth.login_required
	def put(self, username): #OK
		""" Handles PUT requests to update existing users."""
		password = self.reqparse.parse_args()['password']
		if manager.change_password(username, password):
			user = manager.get_user(username)
			return {'user': marshal(user, UsersAPI.user_field)} # Igual mejor un 200
		

	@auth.login_required
	def delete(self, username): #OK
		""" Hanldes DELETE requests to delete an existing user."""
		debug("DELETE USER:", username)
		if manager.delete_user(username):
			return 200 # Change "Ok, created"
		else:
			abort(400) # Change

api.add_resource(UsersAPI, '/yilpil/users/<string:username>', endpoint='users')


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
		debug("GET POST id: " + str(id))
		post = manager.get_post(id)
		if post == None:
			abort(404)
		return { 'post' : marshal(post, PostAPI.response_post_field) }

	@auth.login_required
	def post(self, id): # OK
		""" Handles a POST request. Creates a new post. """
		debug("POST a post")
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
		debug("PUT POST id:", str(id))
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
		if username != None and len(username) > 0:
			debug("DELETE POST id: " + str(id) + " user: " + username)
			if manager.delete_post(id, username):
				return 200 # Ok. Post deleted
			else:
				return 404 # Meaning post not found
		else:
			abort(400)

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
		self.reqparse.add_argument('page', type=int, required=True)
		super(PostsAPI, self).__init__()

	def get(self, username): #OK, but review jsonify again
		""" Get posts given a username. """
		debug("GET POSTS")
		args = self.reqparse.parse_args()
		if args['page'] == 0:
			abort(404)
		posts = manager.get_posts(username, args['page'])
		
		return jsonify(posts=posts)

api.add_resource(PostsAPI, '/yilpil/posts/<string:username>', endpoint = 'posts')


class TagsAPI(Resource):
	""" Class for the tags resource."""
	def __init__(self):
		super(TagsAPI, self).__init__()

	def get(self, user): #OK
		""" Gets all the tags used by a user."""
		debug("(GET) Get '" + str(user) + "'s tags")
		return manager.get_user_tags(user)
		
api.add_resource(TagsAPI, '/yilpil/tags/<string:user>', endpoint = 'tags')


class VotingAPI(Resource): #Ok
	""" Class for voting a post. """
	decorators = [auth.login_required]

	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('up', type=str, location='form',
			required=True)
		self.reqparse.add_argument('username', type=str, location='form',
			required=True)
		super(VotingAPI, self).__init__()

	def put(self, post_id): #Ok
		""" PUT request. Updates the value of the post by a vote up or down. """
		args = self.reqparse.parse_args()
		debug("(PUT) Vote to post ", str(post_id), ". Vote up? ", str(args['up']))
		res = None
		if str(args['up']) == 'true':
			# vote up
			debug("voting up")
			res = manager.vote_positive(post_id, args['username'])
		elif str(args['up']) == 'false':
			# vote down
			debug("voting down")
			res = manager.vote_negative(post_id, args['username'])
		if res == None:
			return "Post-id not found", 404
		if res:
			return "Vote stored", 200
		else:
			return "Already voted on that post", 200

api.add_resource(VotingAPI, '/yilpil/voting/<int:post_id>', endpoint='voting')	


class SearchTagsAPI(Resource):
	""" Provides search in all the tags. """

	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('page', type=int)
		self.reqparse.add_argument('letter', type=str)
		super(SearchTagsAPI, self).__init__()

	def get(self):
		""" Search within the tags given the query."""
		args = self.reqparse.parse_args()
		# Search by starting letter	
		if args['letter'] != None and len(args['letter']) == 1: #OK
			result = None
			if args['page'] != None:
				# Pagination requested
				result = manager.search_tag_names_letter(
					args['letter'],
					int(args['page']))
			else:
				result = manager.search_tag_names_letter(args['letter'])
			return jsonify(tags=result)
		else:
			abort(400)

api.add_resource(SearchTagsAPI, '/yilpil/search/tag', endpoint='tag')


class SearchPostsDateAPI(Resource):
	""" Provides search of posts by date. """

	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('page', type=int)
		self.reqparse.add_argument('user', type=str, required=True)
		self.reqparse.add_argument('dateini', type=int, required=True)
		self.reqparse.add_argument('dateend', type=int)
		super(SearchPostsDateAPI, self).__init__()

	def get(self):
		""" Search within the posts given the query. """
		args = self.reqparse.parse_args()
		if len(args['user']) > 0 \
		and args['dateini'] != None and len(str(args['dateini'])) == 8:
			debug("GET search of posts user-date")
			result = None
			page = 0 # All by default
			if args['page'] != None and args['page'] > 0:
				page = args['page']
			# Interval requested
			if args['dateend'] != None and len(str(args['dateend'])) == 8:
				if int(args['dateend']) >= int(args['dateini']):
					result = manager.search_posts_user_date(
						args['user'],
						args['dateini'], args['dateend'],
						page)
				else:
					abort(400)
			# Get the posts of a certain day
			else:
				result = manager.search_posts_user_date(
					args['user'],
					args['dateini'], args['dateini'],
					page)
			return jsonify(posts=result)

api.add_resource(SearchPostsDateAPI, '/yilpil/search/posts/date', endpoint='date')


class SearchPostsTitleAPI(Resource):
	""" Provides search of pots given a title. """

	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('title', type=str, required=True)
		super(SearchPostsTitleAPI, self).__init__()

	def get(self):
		""" Search withing the posts given the title query. """
		args = self.reqparse.parse_args()
		return manager.search_posts_title(args['title'])

api.add_resource(SearchPostsTitleAPI, '/yilpil/search/posts/title', endpoint='title')


class GetLastUpdates(Resource):
	""" Returns the last updates of resources. """
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('resource', type=str, required=True)
		super(GetLastUpdates, self).__init__()

	def get(self):
		""" Gets the last updates of the requested resource. """
		args = self.reqparse.parse_args()
		if args['resource'] != None and len(args['resource']) > 0:
			# Get the last post updates
			if args['resource'] == 'posts':
				result = manager.get_last_post_updates()
				return jsonify(posts=result)
			else:
				abort(404)
		else:
			abort(400)

api.add_resource(GetLastUpdates, '/yilpil/updates', endpoint='updates')		


class GetPopular(Resource):
	""" Returns the most popular resources. """

	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('resource', type=str, required=True)
		super(GetPopular, self).__init__()

	def get(self):
		""" Gets the most popular items of a certain resource. """
		args = self.reqparse.parse_args()
		if args['resource'] != None and len(args['resource']) > 0:
			# Check resource type
			if args['resource'] == 'tags':
				result = manager.get_popular_tags()
				return jsonify(tags=result)
			else:
				abort(404)
		else:
			abort(400)

api.add_resource(GetPopular, '/yilpil/ranking', endpoint='ranking')		


if __name__ == '__main__':
	# Populate database with test data
	manager.populate_test2()
	app.run(debug = True)
