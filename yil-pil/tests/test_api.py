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
		"""
		self.assertTrue(test_app.get('/').status_code == 302)
		expected = {'user' : 'seven', \
			'hash': md5('seven@gmail.com'.encode('utf-8')).hexdigest()}
		login = {'user': 'seven', 'password': '123'}
		response = test_app.get(\
			'http://localhost:5000/yilpil/auth/token/seven', data=login)
		"""

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
