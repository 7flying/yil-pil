# -*- coding: utf-8 -*-
from __init__ import db

# In user-hashmap
KEY_PASSWORD = 'password'
# In post-hashmap
KEY_TITLE = 'title'
KEY_CONTENTS = 'contents'
KEY_DATE = 'date'
KEY_TAGS = 'tags'
# User-tag, post-tag set key
APPEND_KEY_TAG = '-tags'

def populate_test():
	db.hset('post-1', 'title', 'How to fly')
	db.hset('post-1', 'date', '20141007')
	db.hset('post-1', 'contents', 'Take an aircraft')
	db.hset('post-1', 'tags', 'how-to')
	db.hset('post-2', 'title', 'How to eat')
	db.hset('post-2', 'date', '20141007')
	db.hset('post-2', 'contents', 'Open your mouth and close it repeteately')
	db.hset('post-2', 'tags', 'how-to')

	db.hset('user', 'name', 'seven')
	db.hset('user', 'pass', '123')

	print " $ Printing database values"
	for post in get_posts(None):
		print post

def _is_user_created(username):
	"""
	Checks if a user, given its id is created.
	"""
	if db.hexists(username, KEY_PASSWORD) == 1:
		return True
	else:
		return False

def get_password(username):
	"""
	Returns the user's password. None if ain't a user with that username.
	"""
	if _is_user_created(username):
		return db.hget(username, KEY_PASSWORD)
	else:
		return None

def change_password(username, new_pass):
	"""
	 Changes the user's password. Returns False if the db hasn't that user.
	"""
	if _is_user_created(username):
		db.hset(user, KEY_PASSWORD, new_pass)
		return True
	else:
		return False

def get_user():
	pass

def insert_user(username, password):
	"""
	Inserts a user in the db. Returns False if there is alrealdy a user in the
	db with that username.
	"""
	if !_is_user_created(username):
		db.hset(username, KEY_PASSWORD, password)
		return True
	else:
		return False

def insert_tag_user_tags(username, tag):
	"""
	Inserts a tag to the user's set of tags.
	"""
	# Since it is a set, the elements aren't inserted if present
	db.ssad(username + APPEND_KEY_TAG, tag)

def insert_tag_post_tags(post_id, tag):
	"""
	Inserts a tag to the post's set of tags.
	"""
	# Element isn't inserted if present
	db.ssad(post_id + APPEND_KEY_TAG, tag)

def _is_post_created(post_id):
	"""
	Checks if a post, given its id is created.
	"""
	if db.hexists(post_id, KEY_TITLE) == 1:
		return True
	else:
		return False

def get_post_tags(post_id):
	"""
	Returns the tags of a post, empty array if there aren't tags for the
	given post.
	"""
	return db.smembers(post_id + APPEND_KEY_TAG)

def get_post(key):
	"""
	Returns a dictionary representing a post given its id.
	None if there aren't posts with that id.
	"""
	if _is_post_created(key):
		post = {}
		post[KEY_TITLE] = db.hget(key, KEY_TITLE)
		post[KEY_CONTENTS] = db.hget(key, KEY_CONTENTS)
		post[KEY_DATE] = db.hget(key, KEY_DATE)
		post[KEY_TAGS] = get_post_tags(key)
		return post
	else:
		return None

def get_posts(user_id):
	posts = []
	posts.append(get_post('post-1'))
	posts.append(get_post('post-2'))
	return posts

def insert_post(post):
	db.hset(post['key'], 'title', post['title'])
	db.hset(post['key'], 'date', post['date'])
	db.hset(post['key'], 'contents', post['contents'])
	db.hset(post['key'], 'tags', post['tags'])

def update_post(post):
	db.hset(post['key'], 'title', post['title'])
	db.hset(post['key'], 'date', post['date'])
	db.hset(post['key'], 'contents', post['contents'])
	db.hset(post['key'], 'tags', post['tags'])

def delete_post(id):
	db.hdel(id, 'title')
	db.hdel(id, 'date')
	db.hdel(id, 'contents')
	db.h(id, 'tags')
