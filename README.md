Yil-Pil
=======

The note-taking app developed for 'Advanced Software Development' subject.

Switch to the [static branch](https://github.com/7flying/yil-pil/tree/static) to obtain all the dependencies.

## How to

- Make sure that you have cloned the [static branch](https://github.com/7flying/yil-pil/tree/static).
- Install all the requirements: ```sudo pip install -r requirements.txt```
- Install Redis, see: [Redis quickstart](http://redis.io/topics/quickstart)
- Start a redis server: ``` $ redis-server ```
- Start Yil-Pil: ``` $ python run.py ```

You can use the user interface or the REST-API.

##API Documentation

Documentation format: 
```
<Resource URL>, [@auth_required], [<data>], <method>
<brief description>
<example>
```
 User resource
---------------------------

* ```/users/<string:username>, {password="String", email="String"}, POST```

	Inserts a new user.
	```
	curl -X POST -i http://localhost:5000/yilpil/users/hello -d "password=123" -d "email=hello@example.com"
	```
* ```/users/<string:name>, @auth_required, password="String", PUT```

	Changes a user's password.
	```
	curl -X PUT -u seven:123 -i http://localhost:5000/yilpil/users/hello -d password=1234
	```

* ```/users/<string:name>, @auth_required, DELETE```

	Deletes a user.
	```
	curl -X POST -i http://localhost:5000/yilpil/users/hello -d "password=123"
	```
	
Post resource
-----------------------

* ```/post/<int:id>, GET```
	
	Gets a post given its id.
	```
	curl -X GET -i http://localhost:5000/yilpil/post/1
	``` 
* ```/post/<int:id>, @auth_required, DELETE```

	Deletes a post given its id.
	```
	curl -X DELETE -u seven:123 -i http://localhost:5000/yilpil/post/1
	```
* ```/post/<int:id> (id ignored but necessary), @auth_required, {title, contents, tags, username}, POST```
	
	Creates a new post.
	```	
	curl -X POST -u seven:123 -i http://localhost:5000/yilpil/post/2 -d "title=Cool post!" -d "contents=how to jump" -d "tags=hello:tag two:cool" -d "username=seven"
	```
	__NOTE__: each tag should be encoded in base64.

* ```/post/<int:id>,  @auth_required, {title, contents, tags, username}, PUT```

	Updates an existing post.
	```
	curl -X PUT -u seven:123 -i http://localhost:5000/yilpil/post/2 -d "title=sometittle!" -d "contents=how to jump" -d "tags=hello:tag two:cool" -d "username=seven"
	```
	__NOTE__: each tag should be encoded in base64.

Posts resource
--------------------
		
* ```/posts, { tag=string, {username=string, page=int}}, GET```
	
	Gets all the posts given some parameters:

	* ```tag```: gets all the posts with that tag.
		```
		curl -X GET -i http://localhost:5000/yilpil/posts -d "tag=sometag"
		```

	* ```username``` and ```page```: gets all the posts of a certain user.
		Nees pagination.
		```
		curl -X GET -i http://localhost:5000/yilpil/posts -d "username=seven" -d "page=1"
		```

Tags resource
------------------------

* ```/tags/<string:username>, GET```

	Gets all the tags used by a user.
	```
	curl -X GET -i http://localhost:5000/yilpil/tags/seven
	```

Voting
---------------

* ```/voting/<int:post_id>, @auth_required, {up:boolean, username:string}, PUT```
 
	Votes up or down a post. (up: true, down:false).
	```
	curl -X  PUT -u seven:123 -i http://localhost:5000/yilpil/voting/2 -d "up=true" -d "username=seven"
	```
	```
	curl -X  PUT -u seven:123 -i http://localhost:5000/yilpil/voting/2 -d "up=false" -d "username=seven"
	```

Favourites Resource
------------------------

* ```favs/<string:user>, [count=string], GET```

	Returns the favourited posts of a user.
	```
	curl -X GET -i http://localhost:5000/yilpil/favs/seven
	```

	If ```count``` is specified just the number of favourites is returned.
	```
	curl -X GET -i http://localhost:5000/yilpil/favs/seven -d "count=true"
	```

* ```favs/<string:user>, @auth_required, {id=int}, POST```
	
	Adds a post to the user's list of favourites.
	```
	curl -X POST -i http://localhost:5000/yilpil/favs/seven -d "id=4"
	```

* ```favs/<string:user>, @auth_required, {id=int}, DELETE```
	Deletes a post from the user's list of favourites.
	```
	curl -X DELTE -i http://localhost:5000/yilpil/favs/seven -d "id=4"
	```	


Search Tags Resource
--------------------------

* ```/search/tag, {letter=String, [page=int]}, GET```
 
	Searches the tags starting by the requested letter; pagination may be used.
	```
	curl -X  GET -i http://localhost:5000/yilpil/search/tag -d "letter=H" -d "page=1"
	```

Search Posts-Date Resource
-----------------

* ```/search/posts/date, {user=String, dateini=Int, [dateend=int], [page=int]}, GET```
 
	Returns a list of posts wrote by the user ```user``` at the given date interval. If no ```dateend``` is specified Yil-Pil will retrieve the posts written at ```dateini``` day.
	
	All dates must be provided in ```YYYYMMDD``` format.
	
	Pagination may be used. 

	```
	curl -X  GET -i http://localhost:5000/yilpil/search/posts/date -d "user=seven" -d "dateini=20141116" -d "page=1"
	```

Search Posts-Title Resource
---------------------------

* ```/search/posts/title, {title=String, [page=int]}, GET```

	Returns a list of posts whose titles match the provided partial title.

	Pagination may be used.

	```
	curl -X GET -i http://localhost:5000/yilpil/search/posts/title -d "title=post" -d "page=2"
	```
	
Last Updates Resource
--------------------------

* ```/updates, {resource=String}, GET```
 
	Returns the last updates of the requested resource.
	Correct resources are:
	* ```posts```: gets the last posts stored in the app.
	```
	curl -X  GET -i http://localhost:5000/yilpil/updates -d "resource=posts"
	```

Ranking Elements Resource
--------------------------

* ```/ranking, {resource=String, [category=string, page=int]}, GET ```

	Returns the most popular items of a certain resource.

	Valid resources are:

	* ```tags```: gets the most used tags. Returns a list of tag names with the tag name and the number of times the tag was used.
	```
	curl -X GET -i http://localhost:5000/yilpil/ranking -d "resource=tags"
	```

	* ```posts```: returns a list of posts ordered by its votes, from high to low.
	Pagination may be used, if not the first page is returned.

	```
	curl -X GET -i http://localhost:5000/yilpil/ranking -d "resource=posts"
	```

	* ```posts``` and ```category``: returns a list of posts in the specified category
	ordered by its votes, from high to low.
	Pagination may be used, if not the first page is returned.
	```
	curl -X GET -i http://localhost:5000/yilpil/ranking -d "resource=posts" -d "category=python"
	```

Index Resource
---------------

* ```/index, [symbol=String], GET```
	
	Returns the index of the categories in the server.
	```
	curl -X GET -i http://localhost:5000/yilpil/index
	```

	If ```symbol``` is provided the categories starting with that symbol are returned.
	```
	curl -X GET -i http://localhost:5000/yilpil/index -d "symbol=l"
	```

Auth Resource
---------------

* ```/auth/token/<string:username>, , @auth_required, GET```
	
	Returns an authorization token that can be used in future requests instead of the pair (user, pass).
	```
	curl -X  GET -u seven:123 -i http://localhost:5000/yilpil/auth/token/seven
	```
