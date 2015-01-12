define(["knockout", "text!./post-list.html", "app/mediator"],
	function(ko, template, mediator) {

		function PostListViewModel(params) {
			var self = this;
			this.posts = params.posts;
			this.setWarningSession = ko.observable(null);
			this.setWarnAlreadyVoted = ko.observable(null);
			this.setWarningGeneral = ko.observable(null);
			
			var clearWarnings = function() {
				self.setWarnAlreadyVoted(null);
				self.setWarningGeneral(null);
				self.setWarningSession(null);
			};

			var voteOk = function(data, textStatus, jqXHR) {
				if (data.code == "405") {
					// Already voted on that post
					self.setWarnAlreadyVoted(true);
					window.scrollTo(0,0);
				} else {
					window.location.reload();
				}
			};

			var voteError = function(jqXHR, textStatus, errorThrown) {
				self.setWarningGeneral(true);
			};

			var vote = function(post, up) {
				clearWarnings();
				var user = mediator.getCookie('yt-username');
				var token = mediator.getCookie('yt-token');
				if (user == null || token == null) {
					self.setWarningSession(true);
					window.scrollTo(0,0);
				} else {
					self.setWarningSession(null);
					mediator.vote(post.id, user, up, token, voteOk, voteError);
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
