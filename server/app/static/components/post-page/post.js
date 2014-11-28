define(['knockout', 'text!./post.html', 'app/router'], function(ko, template, router) {

	function PostViewModel(params) {
		
		/* Little working example \o/ 
		var self = this;
		self.id = ko.observable(params.postId); // Or without initialization.
		
		var getId = function() {
			self.id = params.postId;
		};
		getId();
		*/

		this.posts = ko.observableArray(); // Arrays are dynamically updated

		var getPost = function(toStore) {
			$.getJSON('/yilpil/post/' + params.postId, function(data){
				console.log(data.post);
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
