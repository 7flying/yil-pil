define(['knockout', 'text!./post.html', 'marked', 'app/mediator'], 
	function(ko, template, marked, mediator) {

	// markdown
	marked.setOptions({
		renderer: new marked.Renderer(),
		gfm: true,
		tables: true,
		breaks: false,
		pedantic: false,
		sanitize: true,
		smartLists: true,
		smartypants: false
	});

	function PostViewModel(params) {
		var self = this;
		this.id = ko.observable();
		this.title = ko.observable();
		this.author = ko.observable();
		this.date = ko.observable();
		this.contents = ko.observable();
		this.votes = ko.observable();
		this.tags = ko.observableArray();
		this.postOwner = ko.observable(null);
		this.setSuccess = ko.observable(null);
		this.setWarning = ko.observable(null); 

		var successDelete = function() {
			self.setSuccess(true);
			self.setWarning(null);
			setTimeout(function() {
				mediator.redirectUserPage(self.author());
			}, 2000);
		};

		var errorDelete = function() {
			self.setSuccess(null);
			self.setWarning(true);
		};

		this.deletePost = function() {
			mediator.deletePost(self.id(),
				mediator.getCookie('yt-username'),
				mediator.getCookie('yt-token'), successDelete, errorDelete);
		};

		this.editPost = function() {

		};
		// Sets the posts contents (since it's md to html the elements must
		// be inserted)
		var setContents = function(contents) {
			$('#contents').empty();
			$('#contents').append(contents);
		};
		var getPost = function() {
			$.getJSON('/yilpil/post/' + params.postId, function(data){
				var post = {};
				self.id(data.post.id);
				self.title(data.post.title);
				self.author(data.post.author);
				self.contents(marked(data.post.contents));
				setContents(self.contents());
				self.votes(data.post.votes);
				self.date(data.post.date);
				self.tags([]);
				while (data.post.tags.length > 0)
					self.tags.push(data.post.tags.shift());
				checkOwner();
			});
			
		};
		// Check whether the edit/delete buttons should be visible or not
		var checkOwner = function() {
			var us = mediator.getCookie('yt-username');
			if (us != null && self.author() === us)
				self.postOwner(true);
			else
				self.postOwner(null);
		};
		getPost();
	}
	
	return { viewModel: PostViewModel, template: template };
});
