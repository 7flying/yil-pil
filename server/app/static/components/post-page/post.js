define(['knockout', 'text!./post.html'], function(ko, template) {

	function PostViewModel(params) {

		this.post = ko.observable();
		this.title = ko.observable();
		this.potId = ko.observable(window.location.href.charAt(window.location.href.length));
		ko.postbox.subscribe("idSender", function(receivedValue) {
			//console.log("data received from postbox : " + receivedValue);
			this.postId = receivedValue;
			//getPost(this.post, receivedValue);
		}, PostViewModel);

		var getPost = function(toStore, id, sel) {
			console.log("at get post")
			$.getJSON('/yilpil/post/' + id, function(data) {
				toStore = data;
				sel = toStore['title'];
				console.log(sel);
			});
		};

		getPost(this.post, this.potId, this.title);
		
	}
	return { viewModel: PostViewModel, template: template };
});
