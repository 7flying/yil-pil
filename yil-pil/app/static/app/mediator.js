define(["knockout"], function(ko) {
	return {
		
		/* Gets the posts from the given url and applies a preview. */
		summarizePosts: function(data, toStore) {
			while (data.posts.length > 0) {
				var temp = data.posts.shift();
				// Set preview
				temp.contents = (temp.contents.length > 200 ?
					temp.contents.substring(0, 200) + " [...]"
					: temp.contents);
				toStore.push(temp);
			}
		},
		/* Gets the avatar from a user. */
		getAvatar: function(toStore, username) {
			$.getJSON('/yilpil/users/' + username, function(data) {
				toStore('http://www.gravatar.com/avatar/' + data.user.hash);
			});
		},
		/* Gets the number of favourites a user has. */
		getFavCount: function(toStore, username) {
			$.getJSON('/yilpil/favs/' + username + '?count=true', function(data) {
				toStore = username.count;
			});
		},
		/* Gets the number of favourites a user has. */
		getFavCounte: function(username) {
			$.getJSON('/yilpil/favs/' + username + '?count=true', function(data) {
				return username.count;
			});
		},
		/* Gets the most popular tags from the server. */
		getPopularTags: function(toStore) {
			$.getJSON('/yilpil/ranking?resource=tags', function(data) {
				while(data.tags.length > 0)
					toStore.push(data.tags.shift());
			});
		},
		/* Gets similar tags given a letter. */
		getSimilarTags: function(toStore, letter) {
			$.getJSON('yilpil/search/tag?letter=' + letter, function(data) {
				while (data.tags.length > 0)
						toStore.push(data.tags.shift());
			});
		},
		/* Get authentication token. */
		getToken: function(username, password, success, error) {
			var url = '/yilpil/auth/token/' + username;
			$.ajax({
				type: "GET",
				url: url,
				dataType: 'json',
				beforeSend: function(xhr) {
					xhr.setRequestHeader("Authorization", "Basic " + 
						btoa(username + ":" + password));
				},
				async: false,
				success: success,
				error: error
			});
		},
		/* Gets a cookie given its name. 
		 * We store: 'yt-username' and 'yt-token'
		*/
		getCookie: function(cookieName) {
			var name = cookieName + "=";
			var ca = document.cookie.split(';');
			for (var i = 0; i < ca.length; i++) {
				var c = ca[i];
				while (c.charAt(0) == ' ')
					c = c.substring(1);
				if (c.indexOf(name) != -1)
					return c.substring(name.length,c.length);
    		}
    		return null;
		},
		/* Requests an user creation */
		createUser: function(username, email, pass, success, error) {
			var url = 'yilpil/users/' + username;
			var user = {'username' : username, 'email': email, "password": pass}
			$.ajax({
				type: "POST",
				url: url,
				data: user,
				success: success,
				error: error
			});
		},
		/* Votes up or down a post. */
		vote: function(postId, user, up, token, success, error) {
			var url = '/yilpil/voting/' + postId + "?up=" + up.toString()
				+ "&username=" + user;
			$.ajax({
				type: "PUT",
				url: url,
				beforeSend: function(xhr) {
					xhr.setRequestHeader("Authorization", "Basic " + 
						btoa(token + ":unused"));
				},
				success: success,
				error: error
			});
		},
		/* Adds a post to the user list of favourites. */
		like: function(postId, user, token, success) {
			var url = '/yilpil/favs/' + user + "?id=" + postId;
			$.ajax({
				type: "POST",
				url: url,
				beforeSend: function(xhr) {
					xhr.setRequestHeader("Authorization", "Basic " +
						btoa(token + ":unused"));
				},
				success: success
			});
		},
		/* Deletes a post from the user list of favourites */
		unlike: function(postId, user) {

		},
		/* Creates a new post */
		createPost: function(post, token) {
			var url = 'yilpil/post/0';
			//curl -X POST -u seven:123 -i http://localhost:5000/yilpil/post/2
			// -d "title=Cool post!" -d "contents=how to jump"
			// -d "tags=hello, he, some" -d "username=seven"
			$.ajax({
				type: "POST",
				url: url,
				data: post,
				beforeSend: function(xhr) {
					xhr.setRequestHeader("Authorization", "Basic " +
						btoa(token + ":unused"));
				},
				success: function(data, textStatus, jqXHR) {
					return window.location.href = '#post/' + data.post.id;
				}
			});
		},
		/* Deletes a post.*/
		deletePost: function(postId, user, token, success, error) {
			var url = 'yilpil/post/' + postId;
			$.ajax({
				type: "DELETE",
				url: url,
				data: { 'username': user },
				beforeSend: function(xhr) {
					xhr.setRequestHeader("Authorization", "Basic "
						+ btoa(token + ":unused"));
				},
				success: success,
				error: error
			});
		},
		/* Updates a post. */
		updatePost: function(post, token) {
			var url = 'yilpil/post/' + post.id;
			$.ajax({
				type: "PUT",
				url: url,
				data: post,
				beforeSend: function(xhr) {
					xhr.setRequestHeader("Authorization", "Basic " +
						btoa(token + ":unused"));
				},
				success: function(data, textStatus, jqXHR) {
					window.location.reload();
				}
			});
		},
		/* Change an user's email. */
		changeEmail: function(newMail, user, token, success, error) {
			var url = 'yilpil/users/' + user + "?email=" + newMail;
			$.ajax({
				type: "PUT",
				url: url,
				beforeSend: function(xhr) {
					xhr.setRequestHeader("Authorization", "Basic "
					 + btoa(token + ":unused"));
				},
				success: success,
				error: error
			});
		},
		/* Change an user's password. */
		changePass: function(newPass, user, token, success, error) {
			var url = 'yilpil/users/' + user + "?password=" + newPass;
			$.ajax({
				type: "PUT",
				url: url,
				beforeSend: function(xhr) {
					xhr.setRequestHeader("Authorization", "Basic "
					 + btoa(token + ":unused"));
				},
				success: success,
				error: error
			});
		},
		/* Custom validator to ensure that two elements are equal. */
		validateMustEqual: function(val, other) {
			return val == other();
		},
		/* Redirects to a user's profile page. */
		redirectUserPage: function(user) {
			console.log("redirecting");
			return window.location.href = '#user/' + user;
		}
	}
});
