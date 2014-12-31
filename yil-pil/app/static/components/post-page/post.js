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
		// contents in md
		this.contentsRaw = ko.observable();
		// contents in html
		this.contents = ko.observable();
		this.votes = ko.observable();
		this.tags = ko.observableArray();
		// edition post
		this.post = ko.observable();
		// control
		this.postOwner = ko.observable(null);
		this.editPostEnabled = ko.observable(null);
		this.showPost = ko.observable(true);
		this.isFav = ko.observable(null);
		this.noFav = ko.observable(true); // When the post isn't a fav
		// alerts
		this.setSuccess = ko.observable(null);
		this.setWarning = ko.observable(null);
		this.setWarnAlreadyVoted = ko.observable(null);
		this.setWarningSession = ko.observable(null);
		this.setOkFavourite = ko.observable(null);
		this.setOkUnfavourite = ko.observable(null);

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
			window.scrollTo(0,0);
		};

		this.deletePost = function() {
			mediator.deletePost(self.id(),
			mediator.getCookie('yt-username'),
			mediator.getCookie('yt-token'), successDelete, errorDelete);
		};

		this.editPost = function() {
			self.showPost(null);
			self.editPostEnabled(true);
			self.postOwner(null);
		};

		this.cancelEdition = function() {
			self.showPost(true);
			self.editPostEnabled(null);
			self.postOwner(true);
		};

		var favOk = function(data, textStatus, jqXHR) {
			if (data.code == "201") {
				self.setOkFavourite(true);
				checkFavStatus();
			}
		};
		var unfavOk = function(data, textStatus, jqXHR) {
			if (data.code == "200") {
				self.setOkUnfavourite(true);
				checkFavStatus();
			}
		};

		this.like = function() {
			self.setOkFavourite(null);
			var user = mediator.getCookie('yt-username');
			var token = mediator.getCookie('yt-token');
			if (user == null || token == null){
				self.setWarningSession(true);
				window.scrollTo(0,0);
			}
			else {
				self.setWarningSession(null);
				mediator.like(self.id(), user, token, favOk);
			}
		};

		this.unlike = function() {
			self.setOkUnfavourite(null);
			var user = mediator.getCookie('yt-username');
			var token = mediator.getCookie('yt-token');
			if (user == null || token == null){
				self.setWarningSession(true);
				window.scrollTo(0,0);
			}
			else {
				self.setWarningSession(null);
				mediator.unlike(self.id(), user, token, unfavOk);
			}
		};

		var voteOk = function(data, textStatus, jqXHR) {
			self.setOkFavourite(null);
			if (data.code == "405") {
				 // Already voted on that post
				self.setWarnAlreadyVoted(true);
			} else {
				window.location.reload();
				self.setWarnAlreadyVoted(null);
				self.setWarning(null);
			}
		};

		var voteError = function(jqXHR, textStatus, errorThrown) {
			self.setWarning(true);
		};

		var vote = function(up) {
			self.setOkFavourite(null);
			var user = mediator.getCookie('yt-username');
			var token = mediator.getCookie('yt-token');
			if (user == null || token == null) {
				self.setWarningSession(true);
				window.scrollTo(0,0);
			} else {
				self.setWarningSession(null);
				mediator.vote(self.id(), user, up, token, voteOk, voteOk);
			} 
		};
		this.voteUp = function() {
			vote(true);
		};
		
		this.voteDown = function() {
			vote(false);
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
				self.contentsRaw(data.post.contents);
				self.contents(marked(data.post.contents));
				setContents(self.contents());
				self.votes(data.post.votes);
				self.date(data.post.date);
				self.tags([]);
				while (data.post.tags.length > 0)
					self.tags.push(data.post.tags.shift());
				checkOwner();
				self.post(post);
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
		// Chech witch fav button should be shown (fav or delete from favs)
		var checkFavStatus = function() {
			var user = mediator.getCookie('yt-username');
			var token = mediator.getCookie('yt-token');
			if (user != null && token != null) {
				var url = '/yilpil/favs/' + user;
				$.getJSON(url, function(data) {
					var found = false;
					while(!found & data.posts.length > 0) {
						var temp = data.posts.shift();
						if (temp.id == self.id())
							found = true;
					}
					if (found) {
						self.isFav(true);
						self.noFav(null);
					} else {
						self.isFav(null);
						self.noFav(true);
					}
				});
			}	
		};
		getPost();
		checkFavStatus();
	}
	
	return { viewModel: PostViewModel, template: template };
});
