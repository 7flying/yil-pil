# -*- coding: utf-8 -*-
import unittest
#from flask.ext.testing import TestCase
from hashlib import md5
from base64 import b64encode
import json
import app.yilpil as yilpil
import app.manager as manager

test_app = yilpil.app.test_client()

class ServerTestCase(unittest.TestCase):

	def setUp(self):
		manager.populate_test2()

	def tearDown(self):
		manager._clear_database()

	def get_auth_headers(self, username, password):
		return {'Authorization': 'Basic ' + b64encode( \
			(username + ':' + password).encode('utf-8')).decode('utf-8')}

	def get_token_headers(self, token):
		return {'Authorization': 'Basic ' + b64encode( \
			(token + ':unused').encode('utf-8')).decode('utf-8')}

	def test_1_post(self):
		# GET
		response_json = json.loads(test_app.get('/yilpil/post/0').data)
		self.assertTrue(response_json['code'] == '404')
		response_json = json.loads(test_app.get('/yilpil/post/1').data)
		self.assertTrue(response_json['post']['author'] == 'seven')
		# POST
		data = {'title' : "How to install Node.js", \
				 'contents' : "Download files and sudo make, sudo make install", \
				 'tags' : '', 'username' : 'seven'}
		response_json = test_app.post('/yilpil/post/0', data=data,\
			headers=self.get_auth_headers('seven', '123'))
		response_json = json.loads(response_json.data)
		self.assertTrue(response_json['post']['author'] == 'seven')
		# POST OK
		data = {'title' : "Post with tags", \
				 'contents' : "bka vka", 'tags' : 'aGVsbG8=', 'username':'panfrosio'}
		response_json = test_app.post('/yilpil/post/0', data=data,\
			headers=self.get_auth_headers('panfrosio', '123'))
		response_json = json.loads(response_json.data)
		self.assertTrue(response_json['post']['author'] == 'panfrosio')
		# POST unauthorized
		response_json = test_app.post('/yilpil/post/0', data=data,\
			headers=self.get_auth_headers('', '1234'))
		self.assertTrue(response_json.data == 'Unauthorized Access')
		# PUT
		data = {'title' : "MODIFIED", \
				 'contents' : "MODIFIED", \
				 'tags' : '', 'username' : 'seven'}
		response_json = test_app.put('/yilpil/post/1', data=data,\
			headers=self.get_auth_headers('seven', '123'))
		response_json = json.loads(response_json.data)
		self.assertTrue(response_json['post']['title'] == 'MODIFIED')
		# No tags
		data = {'title' : "MODIFIED AGAIN", \
				 'contents' : "MODIFIED", 'username' : 'seven', 'tags': ''}
		response_json = test_app.put('/yilpil/post/1', data=data,\
			headers=self.get_auth_headers('seven', '123'))
		response_json = json.loads(response_json.data)
		self.assertTrue(response_json['post']['title'] == 'MODIFIED AGAIN')
		# Delete post bad request
		response_json = test_app.delete('/yilpil/post/1', \
			headers=self.get_auth_headers('seven', '123'))
		response_json = json.loads(response_json.data)
		self.assertTrue(response_json['status'] == 400)

	def test_2_user(self):
		# GET
		response_json = json.loads(test_app.get('/yilpil/users/seven').data)
		self.assertTrue(response_json['user']['name'] == 'seven')
		self.assertTrue(response_json['user']['hash'] == \
			md5('seven@gmail.com'.encode('utf-8')).hexdigest())
		# User not found
		response_json = json.loads(test_app.get('/yilpil/users/yo').data)
		self.assertTrue(response_json['code'] == 404)
		# Update data
		data = {'password' : "1234", 'email': 'someNewEmail@gmail.com'}
		response_json = test_app.put('/yilpil/users/seven', data=data,\
			headers=self.get_auth_headers('seven', '123'))
		response_json = json.loads(response_json.data)
		self.assertTrue(response_json['code'] == 201)
		# Create new user
		# Username taken
		data = {'name' : "seven", 'password': '123', 'email': 'user@gmail.com'}
		response_json = test_app.post('/yilpil/users/seven', data=data)
		response_json = json.loads(response_json.data)
		self.assertTrue(response_json['error'] == 480)
		# Proper creation
		data = {'name' : "new-user", 'password': '123', 'email': 'user@gmail.com'}
		response_json = test_app.post('/yilpil/users/new-user', data=data)
		response_json = json.loads(response_json.data)
		self.assertTrue(response_json['code'] == 201)
		# User deletion
		# Ok
		response_json = test_app.delete('/yilpil/users/new-user', data=data,\
			headers=self.get_auth_headers('new-user', '123'))
		response_json = json.loads(response_json.data)
		self.assertTrue(response_json['code'] == 200)
		# Name not found
		response_json = test_app.delete('/yilpil/users/new-useiiir', data=data,\
			headers=self.get_auth_headers('new-useiiir', '123'))
		self.assertTrue(response_json.data == 'Unauthorized Access')

	def test_3_auth(self):
		# GET auth token
		token_response = test_app.get('/yilpil/auth/token/seven',\
			headers=self.get_auth_headers('seven', '123'))
		token_response = json.loads(token_response.data)
		self.assertIsNotNone(token_response['token'])
		# Test the token
		data = {'title' : "How to install Node.js", \
				 'contents' : "Download files and sudo make, sudo make install", \
				 'tags' : '', 'username' : 'seven'}
		response_json = test_app.post('/yilpil/post/0', data=data,\
			headers=self.get_token_headers(token_response['token']))
		response_json = json.loads(response_json.data)
		self.assertTrue(response_json['post']['author'] == 'seven')

	def test_4_posts(self):
		# Errors 40X
		response_json = json.loads(test_app.get('/yilpil/posts').data)
		self.assertTrue(response_json['status'] == 400)
		response_json = json.loads(test_app.get('/yilpil/posts?page=0&username=seven&tag=w').data)
		self.assertTrue(response_json['status'] == 404)
		# Ok
		response_json = json.loads(test_app.get('/yilpil/posts?username=seven&page=1').data)
		self.assertTrue(len(response_json['posts']) > 0)
		response_json = json.loads(test_app.get('/yilpil/posts?tag=lorem').data)
		self.assertTrue(len(response_json['posts']) > 0)

	def test_5_user_tags(self):
		response_json = json.loads(test_app.get('/yilpil/tags/seven').data)
		self.assertTrue(list(response_json) > 0)

	def test_6_voting(self):
		# Vote ok up
		response_json = test_app.put('/yilpil/voting/1?up=true&username=seven',\
			headers=self.get_auth_headers('seven', '123'))
		response_json = json.loads(response_json.data)
		self.assertTrue(response_json['code'] == "200")
		# Vote ok down
		response_json = test_app.put('/yilpil/voting/2?up=false&username=seven',\
			headers=self.get_auth_headers('seven', '123'))
		response_json = json.loads(response_json.data)
		self.assertTrue(response_json['code'] == "200")
		# Already voted
		response_json = test_app.put('/yilpil/voting/1?up=true&username=seven',\
			headers=self.get_auth_headers('seven', '123'))
		response_json = json.loads(response_json.data)
		self.assertTrue(response_json['code'] == "405")
		# Post-id not found
		response_json = test_app.put('/yilpil/voting/100000?up=true&username=seven',\
			headers=self.get_auth_headers('seven', '123'))
		response_json = json.loads(response_json.data)
		self.assertTrue(response_json['code'] == "404")

	def test_7_favourites(self):
		# Get favourite count
		response_json = json.loads(test_app.get('/yilpil/favs/seven?count=true').data)
		self.assertTrue(response_json['count'] == 0)
		# User not found error on count
		response_json = json.loads(test_app.get('/yilpil/favs/se?count=true').data)
		self.assertTrue(response_json['code'] == '404')
		# Get favourite list
		response_json = json.loads(test_app.get('/yilpil/favs/seven').data)
		self.assertTrue(len(response_json['posts']) == 0)
		# User not found error on list
		response_json = json.loads(test_app.get('/yilpil/favs/se').data)
		self.assertTrue(response_json['code'] == '404')
		# Add a favourite
		response_json = json.loads(test_app.post('/yilpil/favs/seven?id=1',\
			headers=self.get_auth_headers('seven', '123')).data)
		self.assertTrue(response_json['code'] == '201')
		# Fav count should be one
		response_json = json.loads(test_app.get('/yilpil/favs/seven?count=true').data)
		self.assertTrue(response_json['count'] == 1)
		# Delete favourite
		response_json = json.loads(test_app.delete('/yilpil/favs/seven?id=1',\
			headers=self.get_auth_headers('seven', '123')).data)
		self.assertTrue(response_json['code'] == '200')
		# Fav count should be zero
		response_json = json.loads(test_app.get('/yilpil/favs/seven?count=true').data)
		self.assertTrue(response_json['count'] == 0)

	def test_8_search_tags(self):
		# Search by starting letter
		response_json = json.loads(test_app.get('/yilpil/search/tag?letter=Z').data)
		self.assertTrue(len(response_json['tags']) == 0)
		response_json = json.loads(test_app.get('/yilpil/search/tag?letter=Z&page=1').data)
		self.assertTrue(len(response_json['tags']) == 0)
		# Force 400
		response_json = json.loads(test_app.get('/yilpil/search/tag?letter=ZS').data)
		self.assertTrue(response_json['status'] == 400)


	def test_9_search_posts_date(self):
		# Get the posts within two dates
		response_json = json.loads(test_app.get(\
			'/yilpil/search/posts/date?user=seven&dateini=20140101&dateend=20251205').data)
		self.assertTrue(len(response_json['posts']) > 0)
		# Get the posts made in a certain date
		response_json = json.loads(test_app.get(\
			'/yilpil/search/posts/date?user=seven&dateini=20140101').data)
		self.assertIsNotNone(response_json.get('posts', None))
		# Use pagination
		response_json = json.loads(test_app.get(\
			'/yilpil/search/posts/date?user=seven&dateini=20140101&page=1').data)
		self.assertIsNotNone(response_json.get('posts', None))
		# Force 400
		response_json = json.loads(test_app.get(\
			'/yilpil/search/posts/date?user=seven&dateini=20140101&dateend=20130110').data)
		self.assertTrue(response_json['status'] == 400)

	def test_10_search_posts_partial_title(self):
		response_json = json.loads(test_app.get('/yilpil/search/posts/title?title=how').data)
		self.assertTrue(len(response_json['posts']) > 0)

	def test_11_get_last_updates(self):
		response_json = json.loads(test_app.get('/yilpil/updates?resource=posts').data)
		self.assertTrue(len(response_json['posts']) > 0)
		# Force 40X
		response_json = json.loads(test_app.get('/yilpil/updates?resource=fake').data)
		self.assertTrue(response_json['status'] == 404)
		response_json = json.loads(test_app.get('/yilpil/updates?resource=').data)
		self.assertTrue(response_json['status'] == 400)

	def test_12_rankings(self):
		# Before voting no posts on the ranking
		response_json = json.loads(test_app.get('/yilpil/ranking?resource=posts').data)
		self.assertTrue(len(response_json['posts']) == 0)
		# vote on a post, there should be a post on the ranking
		response_json = test_app.put('/yilpil/voting/1?up=true&username=seven',\
			headers=self.get_auth_headers('seven', '123'))
		response_json = json.loads(response_json.data)
		response_json = json.loads(test_app.get('/yilpil/ranking?resource=posts').data)
		self.assertTrue(len(response_json['posts']) == 1)
		# Pagination
		response_json = json.loads(test_app.get('/yilpil/ranking?resource=posts&page=1').data)
		self.assertIsNotNone(response_json['posts'])
		# Get the ranking of a certain category
		response_json = json.loads(test_app.get('/yilpil/ranking?resource=posts&category=how-to').data)
		self.assertTrue(len(response_json['posts']) == 1)
		# Get the popular tag list
		response_json = json.loads(test_app.get('/yilpil/ranking?resource=tags').data)
		# greater than zero because it depends on the number of posts, not votes
		self.assertTrue(len(response_json['tags']) > 0)
		# Force 40X
		response_json = json.loads(test_app.get('/yilpil/ranking?resource=eeee').data)
		self.assertTrue(response_json['status'] == 404)
		response_json = json.loads(test_app.get('/yilpil/ranking?resource=').data)
		self.assertTrue(response_json['status'] == 400)

	def test_13_index(self):
		# Request the global index
		response_json = json.loads(test_app.get('/yilpil/index').data)
		self.assertTrue(len(response_json['index']) > 0)
		# Request the index given a letter
		response_json = json.loads(test_app.get('/yilpil/index?symbol=L').data)
		self.assertTrue(len(response_json['tags']) > 0)
		# Force 400
		response_json = json.loads(test_app.get('/yilpil/index?symbol=LL').data)
		self.assertTrue(response_json['status'] == 400)
