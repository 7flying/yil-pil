define(["knockout", "text!./post-list.html", "app/mediator"],
	function(ko, template, mediator) {

		function PostListViewModel(params) {
			this.posts = params.posts;
			this.setWarning = ko.observable(null);
			
			this.like = function(post) {

			};
			
			this.voteUp = function(post) {

			};
			
			this.voteDown = function(post) {

			};

		}
	
	return { viewModel: PostListViewModel, template: template };
});