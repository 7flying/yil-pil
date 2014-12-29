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

	def test_2_user(self):
		# GET
		response_json = json.loads(test_app.get('/yilpil/users/seven').data)
		self.assertTrue(response_json['user']['name'] == 'seven')
		self.assertTrue(response_json['user']['hash'] == \
			md5('seven@gmail.com'.encode('utf-8')).hexdigest())
		
