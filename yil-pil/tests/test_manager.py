# -*- coding: utf-8 -*-
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash
import unittest
import app
import app.manager as manager

class ManagerTestCase(unittest.TestCase):

	def setup(self):
		pass

	def tearDown(self):
		manager._clear_database()

	def test_1_user_none(self):
		# Before user creation
		self.assertFalse(manager._is_user_created('user'))
		self.assertFalse(manager.get_password('user'))
		self.assertIsNone(manager.get_user('user'))
		self.assertFalse(manager.change_password('user', 'some_pass'))
		self.assertFalse(manager.change_email('user', 'some_email'))
		self.assertFalse(manager.delete_user('user'))
		self.assertIsNone(manager.get_user_tags('user'))
		self.assertFalse(manager.add_favourite('user', '3'))
		self.assertFalse(manager.delete_favourite('user', '3'))
		self.assertIsNone(manager.get_favourites('user'))
		self.assertEqual(-1, manager.get_favourite_count('user'))
		self.assertIsNone(manager.get_post('8'))
		self.assertIsNone(manager.get_posts('user'))

	def test_2_user_data(self):	
		# User creation
		user = {}
		user['name'] = 'user'
		user['password'] = '123'
		user['email'] = 'user@gmail.com'
		self.assertIsNotNone(manager.insert_user(user))
		self.assertTrue(manager._is_user_created('user'))
		self.assertFalse(manager.insert_user(user))
		self.assertFalse(manager.add_favourite('user', '3'))
		# Create post
		post = {'title' : "How to install Node.js", \
				 'contents' : "Download files and sudo make, sudo make intall", \
				 'tags' : ["node.js", "How-to"]}
		created_post = manager.insert_post(post, 'user')
		self.assertIsNotNone(manager.get_posts('user'))
		self.assertIsNotNone(manager.get_posts('user', 1))
		# Favourites
		self.assertTrue(manager.add_favourite('user', created_post['id']))
		self.assertIsNotNone(manager.get_favourites('user'))
		self.assertEqual(1, manager.get_favourite_count('user'))
		self.assertTrue(manager.delete_favourite('user', created_post['id']))
		# User data modification
		db_user = manager.get_user('user')
		self.assertEqual(md5(user['email'].encode('utf-8')).hexdigest(), \
						 db_user['hash'])
		self.assertTrue(user['password'], manager.get_password('user'))
		self.assertTrue(manager.change_password('user', '1234'))
		self.assertIsNone(manager.change_email('user', 'some_email'))
		# User tags
		self.assertIsNotNone(manager.get_user_tags('user'))
		# Update post
		post = {'title' : "MODIFY", \
				 'contents' : "MODIFY", \
				 'tags' : ["node.js", "One tag more"]}
		self.assertIsNotNone(manager.update_post(post, created_post['id'], 'user'))
		
		# Delete user
		#self.assertTrue(manager.delete_user('user'))

	def test_3_post_search(self):
		pass

