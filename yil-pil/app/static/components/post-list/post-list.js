define(["knockout", "text!./post-list.html", "app/mediator"],
	function(ko, template, mediator) {

		function PostListViewModel(params) {
			var self = this;
			this.posts = params.posts;
			this.warningTitle = ko.observable();
			this.setWarning = ko.observable(null);
			
			this.like = function(post) {
				var user = mediator.getCookie('yt-username');
				var token = mediator.getCookie('yt-token');
				if (user == null || token == null){
					self.setWarning(true);
					window.scrollTo(0,0);
				} else {
					self.setWarning(null);
					mediator.like(post.id, user, token);
				}
			};
			var vote = function(post, up) {
				var user = mediator.getCookie('yt-username');
				var token = mediator.getCookie('yt-token');
				if (user == null || token == null) {
					self.setWarning(true);
					window.scrollTo(0,0);
				} else {
					self.setWarning(null);
					mediator.vote(post.id, user, up, token);
				} 
			};
			this.voteUp = function(post) {
				vote(post, true);
			};
			
			this.voteDown = function(post) {
				vote(post, false);
			};

		}
	
	return { viewModel: PostListViewModel, template: template };
});