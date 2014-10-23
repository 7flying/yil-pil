# -*- coding: utf-8 -*-
from __init__ import db
from datetime import datetime

# Datetime format in posts
FORMAT_TIME = "%d-%m-%Y %H:%M"
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

_DEBUG_ = True

def debug(to_print):
	if _DEBUG_:
		print "[MANAGER]:", to_print

def populate_test():
	db.flushdb()
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

def populate_test2():
	db.flushdb()
	insert_user('seven', '123')
	post = { 
		KEY_TITLE : "How to install Node.js",
		KEY_CONTENTS: "Download files and sudo make, sudo make intall",
		KEY_TAGS: ["node.js", "How-to"]
	}
	insert_post(post, 'seven')

def _is_user_created(username):
	"""
	Checks if a user, given its id is created.
	"""
	if db.hexists(username, KEY_PASSWORD) == 1:
		debug(username + " found")
		return True
	else:
		debug(username + " not found")
		return False

def get_password(username):
	"""
	Returns the user's password. None if ain't a user with that username.
	"""
	debug("Getting " + username + "'s password")
	if _is_user_created(username):
		return db.hget(username, KEY_PASSWORD)
	else:
		return None

def change_password(username, new_pass):
	"""
	 Changes the user's password. Returns False if the db hasn't that user.
	"""
	debug("Changing " + username + "'s password")
	if _is_user_created(username):
		db.hset(user, KEY_PASSWORD, new_pass)
		return True
	else:
		return False

def get_user():
	pass

def insert_user(username, password):
	"""
	Inserts a user in the db. Returns False if there is already a user in the
	db with that username.
	"""
	debug("Creating user '" + username + "' with some secret password")
	if not _is_user_created(username):
		db.hset(username, KEY_PASSWORD, password)
		debug("User successfully created")
		return True
	else:
		debug("User creation failed")
		return False

def insert_tag_user_tags(username, tag):
	"""
	Inserts a tag to the user's set of tags.
	"""
	debug("Inserting tag '" + tag + "' to " + username )
	# Since it is a set, the elements aren't inserted if present
	db.sadd(username + APPEND_KEY_TAG, tag)

def delete_tag_user_tags(username, tag):
	"""
	Deletes a tag from the user's set of tags
	and from the posts the user has written.
	"""
	debug("Deleting tag '" + tag + "' to " + username )
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
	debug("Inserting tag '" + tag + "' to post #" + post_id)
	# Element isn't inserted if present
	if _is_post_created(post_id):
		db.sadd(get_post(post_id)[KEY_TAGS], tag)

def delete_tag_from_post(post_id, tag):
	"""
	Deletes a tag from the post's set of tags
	"""
	debug("Deleting tag '" + tag + "' to post #" + post_id )
	if _is_post_created(post_id):
		db.srem(get_post(post_id)[KEY_TAGS], tag)

def _is_post_created(post_id):
	"""
	Checks if a post, given its id is created.
	"""
	if db.hexists(post_id, KEY_TITLE) == 1:
		debug("Post #" + str(post_id) + " found")
		return True
	else:
		debug("Post #" + str(post_id) + " not found")
		return False

def get_post_tags(post_id):
	"""
	Returns the tags of a post, empty array if there aren't tags for the
	given post.
	"""
	debug("Getting tags of post #" + post_id)
	tags = db.smembers(post_id + APPEND_KEY_TAG)
	ensure_array = []
	for tag in tags:
		ensure_array.append(tag)
	return ensure_array

def get_post(key):
	"""
	Returns a dictionary representing a post given its id.
	None if there aren't posts with that id.
	"""
	key = str(key) + APPEND_KEY_POSTS
	if _is_post_created(key):
		post = {}
		post[KEY_TITLE] = db.hget(key, KEY_TITLE)
		post[KEY_CONTENTS] = db.hget(key, KEY_CONTENTS)
		post[KEY_DATE] = db.hget(key, KEY_DATE)
		post[KEY_TAGS] = get_post_tags(key)
		debug("Getting post: " + str(post))
		return post
	else:
		return None

def get_posts(username):
	"""
	Returns all the posts written by a user.
	"""
	posts_ids = db.smembers(username + APPEND_KEY_POSTS)
	posts = []
	for key in posts_ids:
		posts.append(get_post(key))
	debug("Getting posts of user: " + username)
	return posts

def insert_post(post, username):
	"""
	Inserts a new post in the db.
	"""
	print "[MANAGER] : { post: %s, user: %s} " % (post, username)
	post_id = str(db.incr(POST_ID)) + APPEND_KEY_POSTS
	print "[MANAGER] post-id:", post_id
	db.hset(post_id, KEY_TITLE, post[KEY_TITLE])
	db.hset(post_id, KEY_DATE, datetime.now().strftime(FORMAT_TIME))
	db.hset(post_id, KEY_CONTENTS, post[KEY_CONTENTS])
	# Set a new set of tags
	tags_id = str(db.incr(TAG_ID)) + APPEND_KEY_TAG
	print "[MANAGER] tags-id:", tags_id
	for tag in post[KEY_TAGS]: # TODO: See if can be made without the for
		print "[MANAGER] add tag:", tag
		db.sadd(tags_id, tag)
	db.hset(post_id, KEY_TAGS, tags_id)
	# Add post id to users post-set
	db.sadd(username + APPEND_KEY_POSTS, post_id)

def update_post(post, post_id, username):
	"""
	Updates a post in the db.
	"""
	debug("Updating " + username + "'s post #" + post_id + " with: " + post)
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
	debug("Deleting " + username + "'s post #" + post_id)
	db.hdel(post_id, KEY_TITLE)
	db.hdel(post_id, KEY_DATE)
	db.hdel(post_id, KEY_CONTENTS)
	# Delete the set of tags that the post has
	tags_id = db.hget(post_id, KEY_TAGS)
	db.delete(tags_id)
	db.hdel(post_id, KEY_TAGS)
	# Delete the post id from the user's post list
	db.srem(username + APPEND_KEY_POSTS, post_id)
