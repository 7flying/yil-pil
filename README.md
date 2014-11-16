Yil-Pil
=======

Yil-Pil server for the HP Cloud, it consists of a RESTful api to serve any client.

Yil-Pil, is note-taking app to record what you have daily learned.

Latest development status as well as the client can be found at [Yil-Pil](https://github.com/7flying/yil-pil).


By Irene Díez


#API Documentation

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
    curl -X POST -u seven:123 -i http://localhost:5000/yilpil/post/2 -d "title=Cool post!" -d "contents=how to jump" -d "tags=hello, he, some" -d "username=seven"
    ```

* ```/post/<int:id>,  @auth_required, {title, contents, tags, username}, PUT```

	Updates an existing post.
	```
	curl -X PUT -u seven:123 -i http://localhost:5000/yilpil/post/2 -d "title=sometittle!" -d "contents=how to jump" -d "tags=hello, he, some" -d "username=seven"
    ```

Posts resource
--------------------
		
* ```/posts/<string:username>, page (>0), GET```
	
    Gets all the posts done by a user using pagination.
	```
    curl -X GET -i http://localhost:5000/yilpil/posts/seven -d "page=1"
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
    
Last Updates Resource
--------------------------

* ```/updates, {resource=String}, GET```
 
	Returns the last updates of the requested resource.
    Correct resources are:
    * ```posts```: gets the last posts stored in the app.
    ```
	curl -X  GET -i http://localhost:5000/yilpil/updates -d "resource=posts"
	```

