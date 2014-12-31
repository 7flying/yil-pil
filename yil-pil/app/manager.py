# -*- coding: utf-8 -*-
from __init__ import db
from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash
from config import API_PAGINATION, API_MAX_UPDATES, MANAGER_DEBUG

# Datetime format in posts
FORMAT_TIME = "%d-%m-%Y %H:%M"
# Datetime format in score for timedate stuff
FORMAT_TIME_SEARCH = "%Y%m%d"
# In user-hashmap, user-fields
KEY_PASSWORD = 'password'
KEY_EMAIL = 'email'
KEY_USER = 'name'
KEY_HASH = 'hash' # md5 of the user's email
# In post-hash map, post-fields
KEY_TITLE = 'title'
KEY_CONTENTS = 'contents'
KEY_DATE = 'date'
KEY_TAGS = 'tags'
KEY_AUTHOR = 'author'
KEY_ID = 'id'
KEY_VOTES = 'votes'
# User-tag, post-tag set key
APPEND_KEY_TAG = ':tags'
# User-posts key
APPEND_KEY_POSTS = ':posts'
# User tag
APPEND_KEY_USER = ':user'
# Vote-post
APPEND_KEY_VOTE = ':vote'
# Votes made by a user
APPEND_KEY_HAS_VOTED = ':has-voted'
# Set of favourite posts of a user
APPEND_KEY_FAVS = ':favs'
# Identifiers. This ids are used to reference the tags and the posts.
POST_ID = 'next-key-post-id'
TAG_ID = 'next-tag-id'
VOTE_ID = 'next-vote-id'
## -- Global structures -- ##
# Capped list of last updates
GLOBAL_POST_UPDATE_ID = 'global-post-update'
# Set of tag-name, post-ids with that tag.
APPEND_TAG_NAME_POSTS = ':post-list'
# Append key for the sorted set of tags starting by the given letter
APPEND_KEY_INDEX_LETTER_TAG = ':letter-tags'
# Index for all the letter-tags
GLOBAL_INDEX_LETTER_TAG = 'index-letter-tag'
## -- Search related stuff -- ##
# Tags:
# Id for the sorted set of tag name + score.
# The score is the upper case ASCII value of the character
SEARCH_TAGS_LETTER = 'search-tags-letter'
# Posts by title
# Id for the sorted set of post-titles all with the same score (force Zrangebylex)
SEARCH_POSTS_TITLE = 'search-posts-title'
# This hash makes a relationship between a title and the posts with that title
APPEND_SEARH_POSTS_TITLE_GET_IDS = ':search-posts-title-ids'
## -- Popular/Rankings -- ##
# Most popular tags:
# Id for the sorted set of tag name + score
# The score is the number of times that tag was used
POPULAR_TAGS = 'popular-tags-ranking'
# Top Posts
POPULAR_TOP_POSTS = 'popular-top-posts'
# Most popular posts by category
# Sorted set of posts-ids -- score. The category is the tag.
APPEND_POPULAR_POSTS_CATEGORY = ':popular-category'
# tags-autocomplete : TODO!
# Posts-user:
# Id for the sorted set of post-id + score.
# The score is the time date concatenated ej: 20141109
APPEND_SEARCH_POST_TIMEDATE = ':search-post-user-timedate'

## Notes:
# - Change the hash of :search-posts-title-ids, we cannot remove posts since
# we do not know the key. Make a set for every title.

def debug(to_print):  # pragma: no cover
    """ Debugs the manager. """
    if MANAGER_DEBUG:
        print "[ MANAGER ] ", to_print

def populate_test2():
    """ Add test data. """
    db.flushdb()
    user = {KEY_USER: 'seven', KEY_PASSWORD: '123', KEY_EMAIL: 'seven@gmail.com'}
    insert_user(user)
    user[KEY_EMAIL] = 'panfrosio@gmail.com'
    user[KEY_USER] = 'panfrosio'
    insert_user(user)
    post = {
        KEY_TITLE : "How to install Node.js",
        KEY_CONTENTS: "Download files and sudo make, sudo make intall",
        KEY_TAGS: ["node.js", "How-to"]
    }
    insert_post(post, 'seven')
    insert_post(post, 'panfrosio')

    post2 = {
        KEY_TITLE : "On eating doughnuts",
        KEY_CONTENTS: "You shouldn't eat those. They have oxygenated fat.",
        KEY_TAGS: ["food", "health"]
    }
    insert_post(post2, 'seven')
    insert_post(post2, 'panfrosio')

    post_tem = {
        KEY_TITLE : "",
        KEY_CONTENTS: "Lorem ipsum dolor sit amet, consectetur adipiscing elit,\
         sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        KEY_TAGS: ["lorem", "ipsum"]
    }
    for i in range(3):
        post_tem[KEY_TITLE] = "Post Num " + str(i)
        post_tem[KEY_TAGS].append("Tag number " + str(i))
        insert_post(post_tem, 'seven')
        insert_post(post_tem, 'panfrosio')

    debug("Database created with testing data")

def _clear_database():
    """ Clears all data."""
    db.flushdb()

### User related stuff ###

def _is_user_created(username):
    """
    Checks if a user, given its id is created.
    """
    if db.hexists(username + APPEND_KEY_USER, KEY_USER) == 1:
        debug(username + " EXISTS")
        return True
    else:
        debug(username + " does NOT EXIST")
        return False

def get_password(username): #OK
    """
    Returns the user's password. None if ain't a user with that username.
    """
    debug("GET PASS for: " + username)
    if _is_user_created(username):
        password = db.hget(username + APPEND_KEY_USER, KEY_PASSWORD)
        debug(username + "'s PASS: " + password)
        return password
    else:
        return None

def change_password(username, new_pass): #OK
    """
     Changes the user's password. Returns False if the db hasn't that user.
    """
    debug("CHANGE " + username + "'s password to " + new_pass)
    if _is_user_created(username):
        db.hset(username + APPEND_KEY_USER, KEY_PASSWORD,
                generate_password_hash(new_pass))
        return True
    else:
        return False

def change_email(username, new_email):
    """ Changes the user's email. Returns False if the user is not created. """
    if _is_user_created(username):
        db.hset(username + APPEND_KEY_USER, KEY_EMAIL, new_email)
        # Generate the md5 also.
        db.hset(username + APPEND_KEY_USER, KEY_HASH,
                hashlib.md5(new_email.encode('utf-8')).hexdigest())
        return True
    else:
        return False

def insert_user(user): #OK
    """
    Inserts a user in the db. Returns False if there is already a user in the
    db with that username.
    """
    debug("CREATE USER :" + user[KEY_USER])
    username = user[KEY_USER]
    if not _is_user_created(username):
        hashpass = generate_password_hash(user[KEY_PASSWORD])
        pipe = db.pipeline()
        pipe.hset(username + APPEND_KEY_USER, KEY_USER, user[KEY_USER])
        pipe.hset(username + APPEND_KEY_USER, KEY_PASSWORD, hashpass)
        pipe.hset(username + APPEND_KEY_USER, KEY_EMAIL, user[KEY_EMAIL])
        pipe.hset(username + APPEND_KEY_USER, KEY_HASH,
                  hashlib.md5(user[KEY_EMAIL].encode('utf-8')).hexdigest())
        pipe.execute()
        debug("\tUser successfully created")
        return get_user(username)
    else:
        debug("\tUser creation failed")
        return False

def delete_user(username): #OK -> DELETE ALL HIS/HER POSTS and stuff
    """ Deletes a user. """
    if _is_user_created(username):
        # Delete tags
        user_tags = get_user_tags(username)
        for tag in user_tags:
            delete_tag_user_tags(username, tag)
        # Delete voting records
        db.delete(username + APPEND_KEY_HAS_VOTED)
        # Delete favourites
        db.delete(username + APPEND_KEY_FAVS)
        # Delete posts
        user_posts = _get_posts(username)
        for post in user_posts:
            delete_post(post, username)
        return db.delete(username + APPEND_KEY_USER) > 0
    return False

def get_user(username):
    """ Returns a user. """
    debug('GET user :' + username)
    if _is_user_created(username):
        user = {}
        user[KEY_USER] = db.hget(username + APPEND_KEY_USER, KEY_USER)
        user[KEY_HASH] = db.hget(username + APPEND_KEY_USER, KEY_HASH)
        return user
    else:
        return None

# User's tags

def get_user_tags(username):
    """ Gets the tags of a user. """
    debug("GET TAGS of: " + username)
    if _is_user_created(username):
        array = []
        vals = db.smembers(username + APPEND_KEY_TAG)
        debug("\t returning:" + str(vals))
        for val in vals:
            array.append(val)
        return array
    else:
        return None

def insert_tag_user_tags(username, tag):
    """
    Inserts a tag to the user's set of tags.
    """
    debug("INSERT TAG :" + tag + ", to:" + username)
    # Since it is a set, the elements aren't inserted if present
    db.sadd(username + APPEND_KEY_TAG, tag)
    # Add to global
    _insert_tags_global(tag)

def delete_tag_user_tags(username, tag):
    """
    Deletes a tag from the user's set of tags
    and from the posts the user has written.
    """
    debug("DELETE TAG :" + tag + ", from:" + username)
    db.srem(username + APPEND_KEY_TAG, tag)
    _delete_tag_from_all_user_posts(username, tag)

def _delete_tag_from_all_user_posts(username, tag):
    """
    Deletes a tag from all the posts a given user has.
    """
    debug("DELETE TAG FROM USER POSTS. tag:" + tag + ", user:" + username)
    for post_id in db.lrange(username + APPEND_KEY_POSTS, 0, -1):
        delete_tag_from_post(post_id, tag)

# User's favs

def add_favourite(username, post_id):
    """ Adds the specified post to the user's set of favourites. """
    if _is_user_created(username):
        post_id = str(post_id)
        if _is_post_created(post_id):
            # If the id is already present the insertion is ignored
            db.sadd(username + APPEND_KEY_FAVS, str(post_id))
            return True
        else:
            return False
    else:
        return False

def delete_favourite(username, post_id):
    """ Removes the specified post from the user's set of favourites. """
    if _is_user_created(username):
        post_id = str(post_id)
        db.srem(username + APPEND_KEY_FAVS, str(post_id))
        return True
    else:
        return False

def get_favourites(username):
    """ Returns a list of posts favourited by the given user. """
    if _is_user_created(username):
        ret = []
        to_delete = []
        for post_id in db.smembers(username + APPEND_KEY_FAVS):
            post = get_post(post_id)
            if post == None:
                # Delete from the favourite set
                to_delete.append(post_id)
            else:
                ret.append(post)
        if len(to_delete) > 0:
            for item in to_delete:
                db.srem(username + APPEND_KEY_FAVS, item)
        return ret
    else:
        return None

def get_favourite_count(username):
    """ Returns the number of favourited posts by a user. """
    if _is_user_created(username):
        return db.scard(username + APPEND_KEY_FAVS)
    else:
        return -1

### End of user-related stuff ###

### Post-related ###

def insert_tag_post_tags(post_id, tag):
    """
    Inserts a tag to the post's set of tags.
    """
    get_post_tags(str(post_id))
    debug("INSERT TAG to post. tag:" + tag + " post #:" + str(post_id))
    # Element isn't inserted if present
    if _is_post_created(post_id):
        db.sadd(db.hget(post_id + APPEND_KEY_POSTS, KEY_TAGS) + APPEND_KEY_TAG,
                tag)
        # Add to global tags
        _insert_tags_global(tag)
        # Add to popular
        _inc_dec_tag(tag, True)
        # Add to the sorted set of tag-name -- post-ids
        _insert_post_tag_name(post_id, tag)
        # Insert to the index of tags
        _insert_symbol_index(tag[0])
        # Insert to the specific index of tag[0] -- tags
        _insert_tag_index_letter_tags(tag)
    get_post_tags(str(post_id))

def delete_tag_from_post(post_id, tag):
    """
    Deletes a tag from the post's set of tags
    """
    debug("DELETE TAG from post. tag:" + tag + ", post #:" + str(post_id))
    if _is_post_created(post_id):
        db.srem(db.hget(post_id + APPEND_KEY_POSTS, KEY_TAGS) + APPEND_KEY_TAG, tag)
        # Decrement the score
        _inc_dec_tag(tag, False)
        # Delete from the sorted set of tag-name -- post-ids
        _remove_post_tag_name(post_id, tag)

def _is_post_created(post_id):
    """
    Checks if a post, given its id is created.
    """
    if db.hexists(str(post_id) + APPEND_KEY_POSTS, KEY_TITLE) == 1:
        return True
    else:
        return False

def get_post_tags(post_id): # OK
    """
    Returns the tags of a post given its integer-id.
    An empty array is returned if there aren't tags for the given post.
    """
    tags = db.smembers(str(post_id) + APPEND_KEY_TAG)
    ensure_array = []
    for tag in tags:
        ensure_array.append(tag)
    debug("\t TAGS FROM POST #: " + str(post_id) + '\n' + str(ensure_array))
    return ensure_array

def get_post(key): # OK
    """
    Returns a dictionary representing a post given its integer-id.
    None is returned if there aren't posts with that id.
    """
    debug("GET POST #: " + str(key))
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
        debug("\treturning post with id:" + str(key))
        return post
    else:
        return None

def _get_posts(username):
    """ Returns the posts ids of a user. """
    return db.lrange(username + APPEND_KEY_POSTS, 0, -1)
    

def get_posts(username, int_page=0): # OK
    """
    Returns all the posts written by a user, ordered by latest - oldest.
    int_page: is used for the pagination.
    """
    debug("GET POSTS OF USER: " + username)
    if _is_user_created(username):
        if int_page == 0:
            # Return all the posts
            posts_ids = db.lrange(username + APPEND_KEY_POSTS, 0, -1)
        else:
            # Get the posts specified in the pagination
            posts_ids = db.lrange(username + APPEND_KEY_POSTS,
                                  # Start index
                                  (int_page - 1) * API_PAGINATION,
                                  # End index (included in lrange)
                                  int_page * API_PAGINATION - 1)
        posts = []
        for key in posts_ids:
            posts.append(get_post(key))
        return posts
    else:
        return None

def insert_post(post, username): # OK
    """
    Inserts a new post in the db.
    """
    debug("INSERT POST. username: " + username + "post: " + str(post))
    post_id = str(db.incr(POST_ID))
    db_post_id = post_id + APPEND_KEY_POSTS
    debug("\tASIGNED ID:" + str(post_id))
    # Post fields
    # Set id
    db.hset(db_post_id, KEY_ID, post_id)
    # Create the vote counter and set it to 0 votes
    vote_id = str(db.incr(VOTE_ID)) # get the next vote id
    debug("\tASIGNED POST-VOTE-ID:" + str(vote_id))
    db.set(vote_id + APPEND_KEY_VOTE, "0")
    # Set the id of the vote counter
    db.hset(db_post_id, KEY_VOTES, vote_id)
    # Set author
    db.hset(db_post_id, KEY_AUTHOR, username)
    # Set title
    db.hset(db_post_id, KEY_TITLE, post[KEY_TITLE])
    # Set date-time
    timedatenow = datetime.now()
    date = timedatenow.strftime(FORMAT_TIME)
    db.hset(db_post_id, KEY_DATE, date)
    # Set contents
    db.hset(db_post_id, KEY_CONTENTS, post[KEY_CONTENTS])
    # Set a new set of tags-post to the db
    tag_id = str(db.incr(TAG_ID))
    db_tag_id = tag_id + APPEND_KEY_TAG
    debug("\tASIGNED POST-TAGS-ID:" + str(tag_id))
    for tag in post[KEY_TAGS]:
        # Add tag to the tag-post
        db.sadd(db_tag_id, tag)
        # Add tag to the user's tags
        insert_tag_user_tags(username, tag)
        ## Add tag to the global tags
        _insert_tags_global(tag)
        # Add to popular
        _inc_dec_tag(tag, True)
        # Add to the sorted set of tag-name -- post-ids
        _insert_post_tag_name(post_id, tag)
        # Insert to the index of tags
        _insert_symbol_index(tag[0])
        # Insert to the specific index of tag[0] -- tags
        _insert_tag_index_letter_tags(tag)
    # Add link to the tags in the post
    db.hset(db_post_id, KEY_TAGS, tag_id)
    # Add post id to the head of the user's post-list
    db.lpush(username + APPEND_KEY_POSTS, post_id)
    ## Add post id to the sset of timedate-user-posts
    _insert_post_user_date_ss(post_id, timedatenow, username)
    ## Add post id to the capped list of last post updates
    _insert_post_last_updates(post_id)
    ## Add post's title to the title search sorted set
    _insert_title_ss(post[KEY_TITLE], post_id)
    debug("POST CREATED")
    return get_post(post_id)

def update_post(post, post_id, username): #OK
    """
    Updates a post in the db.
    """
    post_id = str(post_id)
    debug("UPDATE POST. username:" + username + ",post:" + post_id + \
         "\n\t values:" + str(post))
    # The title has changed.
    if post[KEY_TITLE] is not None:
        # ------------------------------------------------------------------
        # The title has changed, so CHANGE in the structure of search-title
        debug("\t-UPDATE title")
        db.hset(post_id + APPEND_KEY_POSTS, KEY_TITLE, post[KEY_TITLE])
        ## Add post's title to the title search sorted set
        _insert_title_ss(post[KEY_TITLE], post_id)
    # The content has changed
    if post[KEY_CONTENTS] is not None:
        debug("\t-UPDATE contents")
        db.hset(post_id + APPEND_KEY_POSTS, KEY_CONTENTS, post[KEY_CONTENTS])
    # The tags have changed.
    if post[KEY_TAGS] is not None:
        debug("\t-UPDATE tags")
        # tag_id = db.hget(post_id + APPEND_KEY_POSTS, KEY_TAGS)
        # Get the old set of tags from the post
        tags_used = dict([(i, False) for i in get_post_tags(post_id)])
        # Check the ones that are used and insert the new ones.
        for tag in post[KEY_TAGS]:
            # The tag does not exist
            if tags_used.get(tag) == None:
                if len(tag) > 0:
                    debug("\t new tag on post: " + tag)
                    insert_tag_post_tags(post_id, tag)
            else:
                tags_used[tag] = True
        # If an old tag is not used it has been deleted.
        for tag in tags_used.keys():
            if not tags_used[tag]:
                debug("\t deleting unused tag: " + tag)
                delete_tag_from_post(post_id, tag)

    return get_post(post_id)

def delete_post(post_id, username):
    """
    Deletes a post (as well as its related set of tags).
    """
    debug("DELETE POST. username:" + username + ",post:" + str(post_id))
    post_id = str(post_id)
    if _is_post_created(post_id):
        # Delete each of the tags (to decrement the score in the ranking)
        for temp_tag in get_post_tags(post_id):
            delete_tag_from_post(post_id, temp_tag)
        # Delete the set of tags that the post has
        tags_id = db.hget(post_id + APPEND_KEY_POSTS, KEY_TAGS)
        db.delete(tags_id + APPEND_KEY_TAG)
        # Delete the counter of votes that the post has
        votes_id = db.hget(post_id + APPEND_KEY_POSTS, KEY_VOTES)
        db.delete(votes_id + APPEND_KEY_VOTE)
        # Delete the post from the sorted set of posts by date
        db.zrem(username + APPEND_SEARCH_POST_TIMEDATE, post_id)
        # Delete the post id from the user's post list
        # (1 is the number of items to be removed)
        db.lrem(username + APPEND_KEY_POSTS, 1, post_id)
        # Delete the post from the last updates
        _delete_post_last_updates(post_id)
        # Delete the post from the global ranking
        db.zrem(POPULAR_TOP_POSTS, post_id)
        # Delete the hash of the post
        db.delete(post_id + APPEND_KEY_POSTS)
        """
        db.hdel(post_id  + APPEND_KEY_POSTS, KEY_TAGS)
        db.hdel(post_id + APPEND_KEY_POSTS, KEY_TITLE)
        db.hdel(post_id + APPEND_KEY_POSTS, KEY_DATE)
        db.hdel(post_id + APPEND_KEY_POSTS, KEY_CONTENTS)
        """
        return True
    else:
        return False

def _insert_post_tag_name(post_id, tag_name):
    """ Inserts a post id to the set of tag-name -- post-ids. """
    db.sadd(tag_name + APPEND_TAG_NAME_POSTS, str(post_id))

def _remove_post_tag_name(post_id, tag_name):
    """ Removes a post-id form the set of tag-name -- post-ids. """
    db.srem(tag_name + APPEND_TAG_NAME_POSTS, str(post_id))
    if db.scard(tag_name + APPEND_TAG_NAME_POSTS) == 0:
        db.delete(tag_name + APPEND_TAG_NAME_POSTS)

def get_posts_with_tag(tag_name):
    """
    Returns all the posts with the provided tag name.
    Pagination is used.
    """
    posts = []
    if tag_name != None and len(tag_name) > 0:
        for post_id in db.smembers(tag_name + APPEND_TAG_NAME_POSTS):
            posts.append(get_post(post_id))
    return posts

### Voting related stuff ###

def _vote(post_id, voting_user, positive): #OK
    """ Private method for handling postivite and negative votes. """
    post_id = str(post_id)
    debug("VOTE POSITIVE. user:" + voting_user + ", post:" + post_id)
    if _is_post_created(post_id) and _is_user_created(voting_user):
        debug("\t CURRENT VOTES of USER.")
        debug("\t\t-user: " + voting_user)
        debug("\t\t-voted to: " + str(db.smembers(voting_user + APPEND_KEY_HAS_VOTED)))
        # Check if the user can vote
        if db.sismember(voting_user + APPEND_KEY_HAS_VOTED, post_id) == 0:
            vote_id = db.hget(post_id + APPEND_KEY_POSTS, KEY_VOTES)
            debug("\t vote_id: " + str(vote_id))
            pipe = db.pipeline()
            if positive:
                pipe.incr(vote_id + APPEND_KEY_VOTE)
            else:
                pipe.decr(vote_id + APPEND_KEY_VOTE)
            pipe.sadd(voting_user + APPEND_KEY_HAS_VOTED, post_id)
            pipe.execute()
            return True
        else:
            return False
    else:
        return None

def vote_positive(post_id, voting_user): # OK
    """ Votes +1 to a post.
        Returns True if the vote was made; False if the user had already voted
        and so, he/she cannot vote again and None if no post for that id was
        found.
        Propagates to the global ranking of posts.
        Propagates the voting to each category that the post has.
    """
    temp = _vote(post_id, voting_user, True)
    if temp:
        _vote_global(post_id, True)
        _vote_post_categories(post_id, True)
        return True
    else:
        return temp

def vote_negative(post_id, voting_user): # OK
    """ Votes -1 to a post.
        Returns True if the vote was made; False if the user had already voted
        and so, he/she cannot vote again and None if no post for that id was
        found.
        Propagates the voting to each category that the post has.
    """
    temp = _vote(post_id, voting_user, False)
    if temp:
        _vote_global(post_id, False)
        _vote_post_categories(post_id, False)
        return True
    else:
        return temp

def _vote_global(post_id, positive):
    """ Propagates the voting to the global ranking of posts. """
    if positive:
        db.zincrby(POPULAR_TOP_POSTS, post_id, 1)
    else:
        db.zincrby(POPULAR_TOP_POSTS, post_id, -1)

def _vote_post_categories(post_id, positive):
    """ Propagates the voting to every category in with the post is."""
    for tag in get_post_tags(str(post_id)):
        if positive:
            db.zincrby(tag.upper() + APPEND_POPULAR_POSTS_CATEGORY, post_id, 1)
        else:
            db.zincrby(tag.upper() + APPEND_POPULAR_POSTS_CATEGORY, post_id, -1)

### End of Voting related stuff ###

### Search stuff!! ###

def _insert_tags_global(tag_name):
    """ Inserts a tag in all the global tag structures. """
    if tag_name != None and len(tag_name) > 0:
        _insert_tag_names_letter(tag_name)

def _insert_tag_names_letter(tag_name): #OK
    """
    Insert the tag in the sorted-set of tags by first-letter score.
    The first-letter-tag sorted set is useful when retrieving all the tags given
    a letter. Like an index.
    Safe to duplicates because we set always the same score.
    """
    db.zadd(SEARCH_TAGS_LETTER, ord(tag_name[0].upper()), tag_name)

def _raw_paginate(some_array, page):
    """ Performs a raw pagination on an array. """
    return some_array[(page - 1) * API_PAGINATION : page * API_PAGINATION]

def search_tag_names_letter(letter, page=0): #OK
    """
    Gets the tags starting by the given letter.
    By default retrieves all the matching elements.
    - Support for pagination by providing a positive 'page' value.
      Pagination works with yil-pil's pagination configuration.
    """
    if len(str(letter)) == 1:
        if page == 0:
            debug("SEARCH BY LETTER: " + letter)
            # Normal behaviour
            return db.zrangebyscore(SEARCH_TAGS_LETTER,
                                    ord(str(letter).upper()),
                                    ord(str(letter).upper())) # One score
        elif page > 0:
            # Pagination
            return _raw_paginate(db.zrangebyscore(SEARCH_TAGS_LETTER,
                                                  ord(str(letter).upper()),
                                                  ord(str(letter).upper())), page)
        else:
            # Bad request

            return None
    else:
        # Bad request, we are searching by a single letter.
        return None
"""
def search_tag_autocomplete(word, max):
    
    Provides autocomplete for searching tags.
    # ZRANGEBYLEX myzset [ab [axxf
    pass
"""

def _insert_post_user_date_ss(post_id, timedate, username):
    """ Inserts a post in a user's sorted set of post-ids by date. """
    db.zadd(username + APPEND_SEARCH_POST_TIMEDATE,
            timedate.strftime(FORMAT_TIME_SEARCH), post_id)
    debug("INSERT sset user_timedate_post_id")

def search_posts_user_date(username, date_ini, date_end, page=0):
    """
    Returns a list of posts wrote by the user at the given date interval.
    All dates must be provided in 'YYYYMMDD' format.
    - Pagination is enabled givin a positive 'page' value.
      Pagination works with yil-pil's pagination configuration.
    """
    if _is_user_created(username) \
    and len(str(date_ini)) == 8 and len(str(date_end)) == 8 \
    and int(date_end) >= int(date_ini) \
    and username != None and len(username) > 0:
        post_ids = db.zrangebyscore(username + APPEND_SEARCH_POST_TIMEDATE,
                                    date_ini, date_end)
        # Slice the array if pagination is requested
        if page > 0:
            post_ids = _raw_paginate(post_ids, page)
        results = []
        for post_id in post_ids:
            results.append(get_post(post_id))
        debug("SEARCH POSTS_USER_DATE returning: " + str(len(results)))
        return results
    else:
        # Bad request
        return None

def _insert_title_ss(title, post_id): # CHANGE - see post UPDATE
    """
    Inserts a title to the sorted set of titles (later on used to find all the
    posts with the given title), and associates the title with the post id.
    """
    title = title.upper()
    # pipe = db.pipeline()
    keys = db.hkeys(title + APPEND_SEARH_POSTS_TITLE_GET_IDS)
    # We simulate a list of post-ids: the fields of the hash are incremented
    # by one with each post_id.
    if keys == None or len(keys) == 0:
        db.hset(title + APPEND_SEARH_POSTS_TITLE_GET_IDS,
                "0", str(post_id))
    else:
        db.hset(title + APPEND_SEARH_POSTS_TITLE_GET_IDS, int(max(keys)) + 1,
                str(post_id))
    db.zadd(SEARCH_POSTS_TITLE, 0, title)
    # db.execute()

def _get_posts_by_title(title):
    """
    Gets the ids of the titles that match the given title and gets the posts for
    those post ids.
    """
    ret = []
    temp_ids = []
    for val in db.hvals(title + APPEND_SEARH_POSTS_TITLE_GET_IDS):
        if val not in temp_ids:
            temp_ids.append(val)
            post = get_post(val)
            if post != None:
                ret.append(get_post(val))
    return ret

def search_posts_title(partial_title, page=0):
    """
    Searches within the posts given a partial title. Pagination may be provided.
    """
    titles = db.zrangebylex(SEARCH_POSTS_TITLE, "[" + partial_title.upper(),
                            "[" + partial_title.upper() + "xff")
    posts = []
    for title in titles:
        temp = _get_posts_by_title(title)
        if len(temp) > 0:
            for results in temp:
                posts.append(results)
    if page > 0 and len(posts) > 0:
        posts = _raw_paginate(posts, page)
    return posts

### End of search stuff ###

### Global things ###

def _insert_post_last_updates(post_id):
    """ Insert post to the  global capped list of last updated posts. """
    pipe = db.pipeline()
    pipe.lpush(GLOBAL_POST_UPDATE_ID, post_id)
    pipe.ltrim(GLOBAL_POST_UPDATE_ID, 0, API_MAX_UPDATES -1)
    pipe.execute()

def get_last_post_updates():
    """ Gets the last post updates. """
    post_ids = db.lrange(GLOBAL_POST_UPDATE_ID, 0, -1)
    ret = []
    for post_id in post_ids:
        post = get_post(post_id)
        if post != None:
            ret.append(post)
    return ret

def _delete_post_last_updates(post_id):
    """ Removes the post from the capped list of last updates if present. """
    db.lrem(GLOBAL_POST_UPDATE_ID, 1, post_id)

def _insert_symbol_index(symbol):
    """ Ads a symbol to the index. """
    if len(symbol) == 1:
        db.sadd(GLOBAL_INDEX_LETTER_TAG, symbol.upper())

def _delete_symbol_index(symbol):
    """ Removes a symbol from the index. """
    if len(symbol) == 1:
        db.srem(GLOBAL_INDEX_LETTER_TAG, symbol.upper())

def get_index_letter_tag():
    """ Returns the contents of the index of letter-tags. """
    return list(db.smembers(GLOBAL_INDEX_LETTER_TAG))

def _insert_tag_index_letter_tags(tag):
    """ Inserts a tag to the index of tag[0] -- tags."""
    db.zadd(tag[0].upper() + APPEND_KEY_INDEX_LETTER_TAG, 0, tag)

def _delete_tag_index_letter_tags(tag):
    """ Deletes a tag from the index of tag[0] -- tags."""
    db.zrem(tag[0].upper() + APPEND_KEY_INDEX_LETTER_TAG, tag)

def get_tags_by_index_letter(letter):
    """ Gets the tags by the provided index letter. Ex 'a': 'angular', 'amazon' """
    if len(letter) == 1:
        return db.zrange(letter + APPEND_KEY_INDEX_LETTER_TAG, 0, -1)

### End of global things ###

### Ranking/Popular stuff ###

def _inc_dec_tag(tag_name, add=True):
    """ Increments or decrements the counter of a tag. """
    if tag_name != None and len(tag_name) > 0:
        if add:
            debug("INC TAG USAGE: "+ tag_name)
            db.zincrby(POPULAR_TAGS, tag_name, 1)
        else:
            debug("DEC TAG USAGE: "+ tag_name)
            db.zincrby(POPULAR_TAGS, tag_name, -1)
            # Delete the tag from the list if it has a score of 0
            #if db.zrank(POPULAR_TAGS, tag_name) == 0:
            if _alternative_score(tag_name) == 0:
                # Delete from the specifig index of tag[0] -- tags
                _delete_tag_index_letter_tags(tag_name)
                # Delete from the index of tags if the tag is the last on index
                num = get_tags_by_index_letter(tag_name[0])
                if num != None and len(num) == 0:
                    _delete_symbol_index(tag_name[0])
                db.zrem(POPULAR_TAGS, tag_name)

def _alternative_score(tag_name):
    """ An alternaive way of checking the score of a tag. """
    result = db.zrangebyscore(POPULAR_TAGS, 0, 1, start=0,
                              num=API_MAX_UPDATES, withscores=True)
    result = [(name, score) for name, score in result if name == tag_name]
    return result[0][1] if result != None and len(result) > 0 else -1

def get_popular_tags():
    """ Returns the most popular tags."""
    # zrevrangebyscore(name, max, min, start=None, num=None, withscores=False,...
    result = db.zrevrangebyscore(POPULAR_TAGS, '+inf', 1, start=0,
                                 num=API_MAX_UPDATES, withscores=True)
    good_format = []
    for name, score in result:
        dic = {}
        dic['name'] = name
        dic['num'] = int(score)
        good_format.append(dic)
    return good_format

def get_popular_posts(category, page=0):
    """
    Returns the most popular posts in a category.
    Pagination may be used, if it isn't, by default returns the first page.
    """
    category = category.upper()
    result = db.zrevrangebyscore(
        str(category) + APPEND_POPULAR_POSTS_CATEGORY,
        '+inf', 1, start=page * API_MAX_UPDATES, num=API_MAX_UPDATES,
        withscores=False)
    ret = []
    for post_id in result:
        ret.append(get_post(post_id))
    return ret

def get_top_posts(page=0):
    """
    Returns the top posts.
    Pagination may be used, if it isn't, by default returns the first page.
    """
    result = db.zrevrangebyscore(POPULAR_TOP_POSTS, '+inf', 1,
                                 start=page * API_MAX_UPDATES,
                                 num=API_MAX_UPDATES, withscores=False)
    ret = []
    for post_id in result:
        ret.append(get_post(post_id))
    return ret

### End of Ranking/Popular stuff ###
