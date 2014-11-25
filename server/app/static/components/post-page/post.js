define(['knockout', 'text!./post.html'], function(ko, template) {

	function PostViewModel(params) {

		this.post = ko.observable();
		this.title = ko.observable();
		this.author = ko.observable();
		this.potId = ko.observable();
		this.contents = ko.observable();
		this.votes = ko.observable();

		ko.postbox.subscribe("idSender", function(receivedValue) {
			getPost(receivedValue, this.title, this.author, this.contents, this.votes);
		}, PostViewModel);

		var getPost = function(id, title, author, contents, votes) {
			console.log("at get post")
			$.getJSON('/yilpil/post/' + id, function(data) {
				title = data.post.title;
				author = data.post.author;
				contents = data.post.contents;
				votes = data.post.votes;
				// tags.push("hello");
			});
		};

		//getPost(this.post, this.potId, this.title);
		
	}
	return { viewModel: PostViewModel, template: template };
});
