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
		self.assertFalse(manager.delete_post('8', 'user'))
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
		

	def test_3_post_search(self):
		# Posts by tag name
		self.assertIsNone(manager.search_tag_names_letter('He'))
		self.assertIsNone(manager.search_tag_names_letter('H', -2))
		self.assertIsNotNone(manager.search_tag_names_letter('H'))
		self.assertIsNotNone(manager.search_tag_names_letter('H', 1))
		# Posts by creation date
		manager.populate_test2()
		self.assertTrue(manager._is_user_created('seven'))
		self.assertIsNotNone(manager.search_posts_user_date('seven', 20141101, 20150101, 0))
		self.assertIsNotNone(manager.search_posts_user_date('seven', 20141101, 20150101, 1))
		self.assertEqual(len(manager.search_posts_user_date('seven', 20141101, 20150101, 2)), 0)
		self.assertIsNone(manager.search_posts_user_date('', 20141101, 20150101, 2))
		# Search posts by title
		self.assertEqual(len(manager.search_posts_title('Z')), 0)
		self.assertEqual(len(manager.search_posts_title('How')), 2)
		self.assertEqual(len(manager.search_posts_title('How', 3)), 0)
		# Get posts with a certain tag
		self.assertEqual(len(manager.get_posts_with_tag('node.js')), 2)
		# Get index
		self.assertGreater(len(manager.get_index_letter_tag()), 0)
		self.assertGreater(len(manager.get_tags_by_index_letter('H')), 0)

	def test_4_updates(self):
		self.assertEqual(len(manager.get_last_post_updates()), 0)
		manager.populate_test2()
		self.assertGreater(len(manager.get_last_post_updates()), 0)

	def test_5_voting_popular(self):
		self.assertEqual(len(manager.get_top_posts()), 0)
		self.assertEqual(len(manager.get_popular_posts('How-to')), 0)
		manager.populate_test2()
		self.assertFalse(manager.vote_positive('8', 'fake-User'))
		self.assertFalse(manager.vote_negative('8', 'fake-User'))
		self.assertTrue(manager.vote_positive('1', 'seven'))
		self.assertFalse(manager.vote_positive('1', 'seven'))
		self.assertTrue(manager.vote_negative('2', 'panfrosio'))
		# get popular
		self.assertGreater(len(manager.get_top_posts()), 0)
		self.assertGreater(len(manager.get_popular_posts('How-to')), 0)
		self.assertGreater(len(manager.get_popular_tags()), 0)

	def test_6_deleting(self):
		manager.populate_test2()
		self.assertTrue(manager.delete_post('1', 'seven'))
		self.assertFalse(manager._is_post_created('1'))
		print manager.delete_user('seven')

	def test_7_special(self):
		# Add a fav and delete the post -> the fav should dissapear
		manager.populate_test2()
		self.assertTrue(manager.add_favourite('seven', '1'))
		self.assertEqual(1, manager.get_favourite_count('seven'))
		self.assertTrue(manager.delete_post('1', 'seven'))
		self.assertEqual(0, len(manager.get_favourites('seven')))
