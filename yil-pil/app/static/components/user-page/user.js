define(['knockout', 'text!./user.html', 'module', 'app/router', 'app/mediator',
	'bootstrap-datetimepicker'],
 function(ko, template, module, router, mediator, datetimepicker) {

	function UserViewModel(params) {
		var self = this;
		this.userPosts = ko.observableArray();
		this.user = ko.observable(params.name);
		this.tags = ko.observableArray();
		this.gravatar = ko.observable();
		this.favCount = ko.observable();
		this.displayTitle = ko.observable('Latest posts');
		this.alertTitle = ko.observable("It seems that " + params.name
			+ " hasn't post anything yet.");
		this.page = ko.observable(1);

		// Filters the posts given two dates
		this.filterPosts = function() {
			self.userPosts([]);
			var from = $('#text-from').val().match(/\d/g);
			from = from.join("");
			// Change order
			from = from.substring(from.length - 4, from.length)
				+ from.substring(from.length - 6, from.length - 4)
				+ from.substring(0, from.length - 6);
			var to = $('#text-to').val().match(/\d/g);
			to = to.join("");
			// Change order
			to = to.substring(to.length - 4, to.length)
				+ to.substring(to.length - 6, to.length - 4)
				+ to.substring(0, to.length - 6);
			if (from.length == 8 && to.length == 8) {
				var url = '/yilpil/search/posts/date?user=' + self.user()
				+ "&dateini=" + from + "&dateend=" + to;
				$.getJSON(url, function(data) {
					if (data.posts.length == 0) {
						self.userPosts(null);
						self.alertTitle("There aren't posts in that period.");
					} else {
						self.userPosts.removeAll();
						self.displayTitle(data.posts.length + " posts found");
					}
					mediator.summarizePosts(data, self.userPosts);
				});
			}
		};

		// Shows the favourites
		this.showFavs = function() {
			if (self.favCount() == 0) {
				self.userPosts(null);
				self.alertTitle(params.name + " hasn't liked anything yet.");
			} else {
				self.userPosts.removeAll();
				self.displayTitle("Liked posts");
				getFavourites(self.userPosts);
			}
		};

		this.next = function() {
			self.page(self.page() + 1);
			self.userPosts.removeAll();
			getUserPosts(self.userPosts);
		};

		this.previous = function() {
			if( self.page() != 0) {
				self.userPosts.removeAll()
				self.page(self.page() - 1);
				getUserPosts(self.userPosts);
			}
		};

		// Initialises the date picker
		$(function () {
			$('#date-from').datetimepicker({
				pickTime: false
			});
			$('#date-to').datetimepicker({
				pickTime: false
			});
			 $('#date-from').on("dp.change",function (e) {
				$('#date-to').data("DateTimePicker")
					.setDate($('#date-from').data("DateTimePicker").getDate());
			});
		});

		var getUserTags = function(toStore) {
			$.getJSON('yilpil/tags/' + params.name, function(data) {
				while(data.length > 0)
					toStore.push(data.shift());
			});
		};

		var getUserPosts = function(toStore) {
			var url = '/yilpil/posts?username=' + params.name + '&page=' + self.page();
			$.getJSON(url, function(data) {
				mediator.summarizePosts(data, toStore);
			});	
		};

		var getFavourites = function(toStore) {
			var url = '/yilpil/favs/' + params.name;
			$.getJSON(url, function(data) {
				self.favCount(data.posts.length);
				mediator.summarizePosts(data, self.userPosts);
			});
		};

		getUserPosts(this.userPosts);
		getUserTags(this.tags);
		mediator.getAvatar(this.gravatar, params.name);
		mediator.getFavCount(self.favCount, params.name);

	}
	return { viewModel: UserViewModel, template: template };
});
