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
# User-posts key
APPEND_KEY_POSTS = '-posts'
# Identifiers. This ids are used to reference the tags and the posts.
POST_ID = 'key-post-id'
TAG_ID = 'tag-id'

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
	if not _is_user_created(username):
		db.hset(username, KEY_PASSWORD, password)
		return True
	else:
		return False

def insert_tag_user_tags(username, tag):
	"""
	Inserts a tag to the user's set of tags.
	"""
	# Since it is a set, the elements aren't inserted if present
	db.sadd(username + APPEND_KEY_TAG, tag)

def delete_tag_user_tags(username, tag):
	"""
	Deletes a tag from the user's set of tags
	and from the posts the user has writen.
	"""
	db.srem(user + APPEND_KEY_TAG, tag)
	_delete_tag_from_all_user_posts(username, tag)

def _delete_tag_from_all_user_posts(username, tag):
	"""
	Deletes a tag from all the posts a given user has.
	"""
	for post_id in db.smembers(username + APPEND_KEY_POSTS):
		delete_tag_from_post(post_id)

def insert_tag_post_tags(post_id, tag):
	"""
	Inserts a tag to the post's set of tags.
	"""
	# Element isn't inserted if present
	if _is_post_created(post_id):
		db.sadd(get_post(post_id)[KEY_TAGS], tag)

def delete_tag_from_post(post_id, tag):
	"""
	Deletes a tag from the post's set of tags
	"""
	if _is_post_created(post_id):
		db.srem(get_post(post_id)[KEY_TAGS], tag)

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

def get_posts(username):
	"""
	Returns all the posts writen by a user.
	"""
	posts_ids = db.smembers(username + APPEND_KEY_POSTS)
	posts = []
	for key in posts_ids:
		posts.append(get_post(key))
	return posts

def insert_post(post, username):
	"""
	Inserts a new post in the db.
	"""
	post_id = db.incr(POST_ID)
	db.hset(post_id, KEY_TITLE, post[KEY_TITLE])
	db.hset(post_id, KEY_DATE, post[KEY_DATE])
	db.hset(post_id, KEY_CONTENTS, post[KEY_CONTENTS])
	# Set a new set of tags
	tags_id = db.incr(TAG_ID)
	for tag in post[KEY_TAGS]: # TODO: See if can be made without the for
		db.sadd(tags_id, tag)
	db.hset(post_id, KEY_TAGS, tags_id)
	# Add post id to users post-set
	db.sadd(username + APPEND_KEY_POSTS, post_id)

def update_post(post, post_id, username):
	"""
	Updates a post in the db.
	"""
	db.hset(post_id, KEY_TITLE, post[KEY_TITLE])
	db.hset(post_id, KEY_DATE, post[KEY_DATE])
	db.hset(post_id, KEY_CONTENTS, post[KEY_CONTENTS])
	tag_id = db.hget(post_id, KEY_TAGS)
	# Add new tags (if any)
	for tag in post[KEY_TAGS]:
		db.sadd(tag_id, tag)

def delete_post(post_id, username):
	"""
	Deletes a post (as well as its related set of tags).
	"""
	db.hdel(post_id, KEY_TITLE)
	db.hdel(post_id, KEY_DATE)
	db.hdel(post_id, KEY_CONTENTS)
	# Delete the set of tags that the post has
	tags_id = db.hget(post_id, KEY_TAGS)
	db.delete(tags_id)
	db.hdel(post_id, KEY_TAGS)
	# Delete the post id from the user's post list
	db.srem(username + APPEND_KEY_POSTS, post_id)
