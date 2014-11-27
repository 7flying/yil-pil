define(['knockout', 'text!./post.html'], function(ko, template) {

	function PostViewModel(params) {
		//this.id = params.post;
	/*
		var post;
		var self = this;
		self.post = {}

		ko.postbox.subscribe("idSender", function(receivedValue) {
			getPost(receivedValue);
		}, PostViewModel);

		var getPost = function(id, store) {
			console.log("at get post: " + id);
			$.getJSON('/yilpil/post/' + id, function(data) {
				//setValues(data);
				store = data;
			});
		};

		var setValues = function(data) {
			self.post.tit = ko.observable(data.tit);
			self.post.author = ko.observable(data.author);
			self.post.contents = ko.observable(data.contents);
			self.post.votes = ko.observable(data.votes);
		};

		self.post.tit = ko.observable(data.tit);
		self.post.author = ko.observable(data.author);
		self.post.contents = ko.observable(data.contents);
		self.post.votes = ko.observable(data.votes);

		getPost(3,self.post);
		*/
		/* 
		this.post = ko.observable();
		this.post_tit = ko.observable();
		this.author = ko.observable();
		this.potId = ko.observable();
		this.contents = ko.observable();
		this.votes = ko.observable();

		ko.postbox.subscribe("idSender", function(receivedValue) {
			getPost(receivedValue, this.post_tit, this.author, this.contents, this.votes);
		}, PostViewModel);

		var getPost = function(id, post_tit, author, contents, votes) {
			console.log("at get post: " + id);
			$.getJSON('/yilpil/post/' + id, function(data) {
				post_tit = data.post.post_tit;
				author = data.post.author;
				contents = data.post.contents;
				votes = data.post.votes;
				// tags.push("hello");
			});
		};
	*/
		
	}
	return { viewModel: PostViewModel, template: template };
});
