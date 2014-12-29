# -*- coding: utf-8 -*-
import unittest
from hashlib import md5
import app.yilpil as yilpil
import app.manager as manager

class ServerTestCase(unittest.TestCase):
	test_app = yilpil.app.test_client()

	def setup(self):
		manager.populate_test2()

	def tearDown(self):
		manager._clear_database()

	def test_1_user_api(self):
		yilpil.debug("hello")
		expected = {'user' : 'seven', \
			'hash': md5('seven@gmail.com'.encode('utf-8')).hexdigest()}
		ServerTestCase.test_app.get('/')
		ServerTestCase.test_app.get('/yilpil/auth/token/seven')
