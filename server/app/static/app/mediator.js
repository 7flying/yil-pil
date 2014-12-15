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
		/* Gets a cookie given its name. */
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
		}
	}
	
});
