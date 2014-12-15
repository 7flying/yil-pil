define(['knockout', 'text!./post.html'], function(ko, template) {

	function PostViewModel(params) {

		this.posts = ko.observableArray(); // Arrays are dynamically updated

		var getPost = function(toStore) {
			$.getJSON('/yilpil/post/' + params.postId, function(data){
				var post = {};
				post.title = data.post.title;
				post.author = data.post.author;
				post.contents = data.post.contents;
				post.votes = data.post.votes;
				post.date  = data.post.date;
				post.tags = [];
				while (data.post.tags.length > 0)
					post.tags.push(data.post.tags.shift());
				toStore.push(post);
			});
		};

		getPost(this.posts);
		
	}
	
	return { viewModel: PostViewModel, template: template };
});
