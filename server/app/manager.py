# -*- coding: utf-8 -*-
from __init__ import db
from datetime import datetime

# Datetime format in posts
FORMAT_TIME = "%d-%m-%Y %H:%M"
# In user-hashmap
KEY_PASSWORD = 'password'
KEY_EMAIL = 'email'
KEY_USER = 'name'
# In post-hashmap
KEY_TITLE = 'title'
KEY_CONTENTS = 'contents'
KEY_DATE = 'date'
KEY_TAGS = 'tags'
KEY_AUTHOR = 'author'
KEY_ID = 'id'
KEY_VOTES = 'votes'
# User-tag, post-tag set key
APPEND_KEY_TAG = '-tags'
# User-posts key
APPEND_KEY_POSTS = '-posts'
# User tag
APPEND_KEY_USER = '-user'
# Vote-post
APPEND_KEY_VOTE = '-vote'
# Votes made by a user
APPEND_KEY_HAS_VOTED = 'has-voted'
# Identifiers. This ids are used to reference the tags and the posts.
POST_ID = 'next-key-post-id'
TAG_ID = 'next-tag-id'
VOTE_ID = 'next-vote-id'

_DEBUG_ = True

def debug(to_print):
	if _DEBUG_:
		print "[ MANAGER ]:", to_print

def populate_test2():
	db.flushdb()
	insert_user('seven', '123', 'seven@server.com')
	post = { 
		KEY_TITLE : "How to install Node.js",
		KEY_CONTENTS: "Download files and sudo make, sudo make intall",
		KEY_TAGS: ["node.js", "How-to"]
	}
	insert_post(post, 'seven')
	post2 = { 
		KEY_TITLE : "On eating doughnuts",
		KEY_CONTENTS: "You shouldn't eat those. They have oxygenated fat.",
		KEY_TAGS: ["food", "health"]
	}
	insert_post(post2, 'seven')

### User related stuff ###

def _is_user_created(username):
	"""
	Checks if a user, given its id is created.
	"""
	if db.hexists(username + APPEND_KEY_USER, KEY_USER) == 1:
		debug(username + " found")
		return True
	else:
		debug(username + " not found")
		return False

def get_password(username): #OK
	"""
	Returns the user's password. None if ain't a user with that username.
	"""
	debug("Getting " + username + "'s password")
	if _is_user_created(username):
		password = db.hget(username + APPEND_KEY_USER, KEY_PASSWORD)
		debug(username + "'s password: " + password)
		return password
	else:
		return None

def change_password(username, new_pass): #OK
	"""
	 Changes the user's password. Returns False if the db hasn't that user.
	"""
	debug("Changing " + username + "'s password")
	if _is_user_created(username):
		db.hset(username + APPEND_KEY_USER, KEY_PASSWORD, new_pass)
		return True
	else:
		return False

def insert_user(username, password, email): #OK
	"""
	Inserts a user in the db. Returns False if there is already a user in the
	db with that username.
	"""
	debug("Create user '" + username + "' pass: '" + password + "'")
	if not _is_user_created(username):
		db.hset(username + APPEND_KEY_USER, KEY_USER, username)
		db.hset(username + APPEND_KEY_USER, KEY_PASSWORD, password)
		db.hset(username + APPEND_KEY_USER, KEY_EMAIL, email)
		debug("User successfully created")
		return get_user(username)
	else:
		debug("User creation failed")
		return False

def delete_user(username): #OK
	if _is_user_created(username):
		return db.delete(username + APPEND_KEY_USER) > 0
	return False

def get_user(username):
	""" Returns a user. """
	if _is_user_created(username):
		debug('Returning user :' + username)
		user = {}
		user[KEY_USER] = db.hget(username + APPEND_KEY_USER, KEY_USER)
		user[KEY_EMAIL] = db.hget(username + APPEND_KEY_USER, KEY_EMAIL)
		return user
	else:
		return None

def get_user_tags(username):
	""" Gets the tags of a user. """
	debug("Getting the tags of: " + username)
	if _is_user_created(username):
		array = []
		vals = db.smembers(username + APPEND_KEY_TAG)
		for val in vals:
			print val
			array.append(val)
		return array
	else:
		return None

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

### End of user-related stuff ###

### Post-related ###

def insert_tag_post_tags(post_id, tag):
	"""
	Inserts a tag to the post's set of tags.
	"""
	debug("Inserting tag '" + tag + "' to post #" + str(post_id))
	# Element isn't inserted if present
	if _is_post_created(post_id):
		db.sadd(get_post(post_id)[KEY_TAGS], tag)

def delete_tag_from_post(post_id, tag):
	"""
	Deletes a tag from the post's set of tags
	"""
	debug("Deleting tag '" + tag + "' to post #" + str(post_id))
	if _is_post_created(post_id):
		db.srem(get_post(post_id)[KEY_TAGS] + APPEND_KEY_TAG, tag)

def _is_post_created(post_id):
	"""
	Checks if a post, given its id is created.
	"""
	if db.hexists(str(post_id) + APPEND_KEY_POSTS, KEY_TITLE) == 1:
		debug("Post #" + str(post_id) + " found")
		return True
	else:
		debug("Post #" + str(post_id) + " not found")
		return False

def get_post_tags(post_id): # OK
	"""
	Returns the tags of a post given its integer-id.
	An empty array is returned if there	aren't tags for the	given post.
	"""
	debug("Getting tags of post #" + str(post_id))
	tags = db.smembers(str(post_id) + APPEND_KEY_TAG)
	
	ensure_array = []
	for tag in tags:
		ensure_array.append(tag)
	return ensure_array

def get_post(key): # OK
	"""
	Returns a dictionary representing a post given its integer-id.
	None is returned if there aren't posts with that id.
	"""
	debug("Requested post with id: " + str(key))
	db_key = str(key) + APPEND_KEY_POSTS
	if _is_post_created(str(key)):
		post = {}
		post[KEY_TITLE] = db.hget(db_key, KEY_TITLE)
		post[KEY_CONTENTS] = db.hget(db_key, KEY_CONTENTS)
		post[KEY_DATE] = db.hget(db_key, KEY_DATE)
		post[KEY_TAGS] = get_post_tags(key)
		post[KEY_AUTHOR] = db.hget(db_key, KEY_AUTHOR)
		post[KEY_ID] = db.hget(db_key, KEY_ID)
		post[KEY_VOTES] = db.get(db.hget(db_key, KEY_VOTES) + APPEND_KEY_VOTE)
		debug("Getting post: " + str(post))
		return post
	else:
		return None	

def get_posts(username): # OK
	"""
	Returns all the posts written by a user.
	"""
	if _is_user_created(username):
		posts_ids = db.smembers(username + APPEND_KEY_POSTS)
		posts = []
		debug("Getting posts of user: " + username)
		for key in posts_ids:
			print "key", key
			posts.append(get_post(key))
		return posts
	else:
		return None

def insert_post(post, username): # OK
	"""
	Inserts a new post in the db.
	"""
	print "[ MANAGER ] : { post: %s, user: %s} " % (post, username)
	post_id = str(db.incr(POST_ID))
	db_post_id = post_id + APPEND_KEY_POSTS
	print "[ MANAGER ] post-id:", post_id
	# Post fields
	# Set id
	db.hset(db_post_id, KEY_ID, post_id)
	# Create the vote counter and set it to 0 votes
	vote_id = str(db.incr(VOTE_ID)) # get the next vote id
	db.set(vote_id + APPEND_KEY_VOTE, "0")
	# Set the id of the vote counter
	db.hset(db_post_id, KEY_VOTES, vote_id)
	# Set author
	db.hset(db_post_id, KEY_AUTHOR, username)
	# Set title
	db.hset(db_post_id, KEY_TITLE, post[KEY_TITLE])
	# Set date-time
	date = datetime.now().strftime(FORMAT_TIME)
	db.hset(db_post_id, KEY_DATE, date)
	# Set contents
	db.hset(db_post_id, KEY_CONTENTS, post[KEY_CONTENTS])
	# Set a new set of tags-post to the db
	tag_id = str(db.incr(TAG_ID))
	db_tag_id = tag_id + APPEND_KEY_TAG
	print "[ MANAGER ] tags-id (db):", db_tag_id
	for tag in post[KEY_TAGS]:
		print "[ MANAGER ] add tag:", tag
		# Add tag to the tag-post
		db.sadd(db_tag_id, tag)
		# Add tag to the user's tags
		insert_tag_user_tags(username, tag)

	db.hset(db_post_id, KEY_TAGS, tag_id)
	# Add post id to users post-set
	db.sadd(username + APPEND_KEY_POSTS, post_id)
	return get_post(post_id)

def update_post(post, post_id, username): #OK
	"""
	Updates a post in the db.
	"""
	post_id = str(post_id)
	debug("Updating " + username + "'s post #" + post_id + " with: " + str(post))
	if post[KEY_TITLE] is not None:
		db.hset(post_id + APPEND_KEY_POSTS, KEY_TITLE, post[KEY_TITLE])
	if post[KEY_CONTENTS] is not None:
		db.hset(post_id + APPEND_KEY_POSTS, KEY_CONTENTS, post[KEY_CONTENTS])
	if post[KEY_TAGS] is not None:
		tag_id = db.hget(post_id + APPEND_KEY_POSTS, KEY_TAGS)
		# Add new tags (if any)
		for tag in post[KEY_TAGS]:
			db.sadd(tag_id + APPEND_KEY_TAG, tag)
	return get_post(post_id)

def delete_post(post_id, username):
	"""
	Deletes a post (as well as its related set of tags).
	"""
	post_id = str(post_id)
	if _is_post_created(post_id):
		db.hdel(post_id + APPEND_KEY_POSTS, KEY_TITLE)
		db.hdel(post_id + APPEND_KEY_POSTS, KEY_DATE)
		db.hdel(post_id + APPEND_KEY_POSTS, KEY_CONTENTS)
		# Delete the set of tags that the post has
		tags_id = db.hget(post_id + APPEND_KEY_POSTS, KEY_TAGS)
		db.delete(tags_id + APPEND_KEY_TAG)
		# Delete the counter of votes that the post has
		votes_id = db.hget(post_id + APPEND_KEY_POSTS, KEY_VOTES)
		db.delete(votes_id + APPEND_KEY_VOTE)
		# First, delete the reference to the post to ensure that is not retrieved
		# Delete the post id from the user's post list
		db.srem(username + APPEND_KEY_POSTS, post_id)
		# Delete the post
		db.hdel(post_id  + APPEND_KEY_POSTS, KEY_TAGS)
		return True
	else:
		return False

# CHECK THIS ONE
def vote_positive(post_id, voting_user):
	""" Votes +1 to a post.
		Returns True if the vote was made; False if the user had already voted
		and so, he/she cannot vote again and None if no post for that id was
		found.
	"""
	post_id = str(post_id)
	if _is_post_created(post_id):
		if db.sismember(voting_user + APPEND_KEY_HAS_VOTED, post_id) == 0:
			db.sadd(voting_user + APPEND_KEY_HAS_VOTED, post_id)
			debug("votes of post no incre: " + post_id + ": " + str(db.get(db.hget(post_id + APPEND_KEY_POSTS, KEY_VOTES))))
			db.incr(db.get(db.hget(post_id + APPEND_KEY_POSTS, KEY_VOTES)))
			debug("votes of post after incre: " + post_id + ": " + str(db.get(db.hget(post_id + APPEND_KEY_POSTS, KEY_VOTES))))
			return True
		else:
			return False
	else:
		return None

def vote_negative(post_id, voting_user):
	""" Votes -1 to a post.
		Returns True if the vote was made; False if the user had already voted
		and so, he/she cannot vote again and None if no post for that id was
		found.
	"""

	if _is_post_created(str(post_id)):
		if db.sismember(voting_user + APPEND_KEY_HAS_VOTED, post_id) == 0:
			db.sadd(voting_user + APPEND_KEY_HAS_VOTED, post_id)
			db.decr(db.get(db.hget(post_id + APPEND_KEY_POSTS, KEY_VOTES)))	
		return True
	else:
		return None
