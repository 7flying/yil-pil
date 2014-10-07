# -*- coding: utf-8 -*-
from __init__ import db

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



def is_user_created(username):
	pass

def get_password(username):
	return db.hget('user', 'pass')

def get_user():
	pass

def insert_user(username, password):
	pass

def get_post(key):
	if db.hget(key, 'title') == None:
		return None
	else:
		post = {}
		post['title'] = db.hget(key, 'title')
		post['date'] = db.hget(key, 'date')
		post['contents'] = db.hget(key, 'contents')
		post['tags'] = db.hget(key, 'tags')
		return post

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
