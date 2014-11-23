define(['knockout', 'text!./post.html'], function(ko, template) {

	function PostViewModel(params) {

		this.post = ko.observable();

		ko.postbox.subscribe("idSender", function(receivedValue) {
			//console.log("data received from postbox : " + receivedValue);
			getPost(this.post, receivedValue);
		}, PostViewModel);

		var getPost = function(toStore, id) {
			console.log("at get post")
			$.getJSON('/yilpil/post/' + id, function(data) {
				toStore = data;
				console.log("data stored " + toStore)
			});
		};
	}
	return { viewModel: PostViewModel, template: template };
});
