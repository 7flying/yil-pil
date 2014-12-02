define(['knockout', 'text!./user.html', 'module', 'app/router', 'bootstrap-datetimepicker'],
 function(ko, template, module, router, datetimepicker) {

	// Register the user-posts component
	ko.components.register('user-posts', {
		template: { require: 'text!components/user-page/user-posts.html'}
	});

	function UserViewModel(params) {
		var self = this;
		this.userPosts = ko.observableArray();
		this.user = ko.observable(params.name);
		this.tags = ko.observableArray();
		this.gravatar = ko.observable();
		this.displayTitle = ko.observable('Latest posts: ');
		this.alertTitle = ko.observable("It seems that " + params.name
			+ " hasn't post anything yet.");

		this.filterPosts = function() {
			var from = $('#text-from').val().match(/\d/g);
			from = from.join("");
			// Change order
			from = from.substring(from.length -4, from.length)
				+ from.substring(from.length -6, from.length -4)
				+ from.substring(0, from.length - 6);
			var to = $('#text-to').val().match(/\d/g);
			to = to.join("");
			// Change order
			to = to.substring(to.length -4, to.length)
				+ to.substring(to.length -6, to.length -4)
				+ to.substring(0, to.length - 6);
			if (from.length == 8 && to.length == 8) {
				var url = '/yilpil/search/posts/date?user=' + self.user()
				+ "&dateini=" + from + "&dateend=" + to; 
				$.getJSON(url, function(data) {
					if (data.posts.length == 0) {
						self.userPosts(null);
						self.displayTitle("There aren't posts in that period.");
					} else {
						self.userPosts.removeAll();
						self.displayTitle(data.posts.length + " posts found:");
					}
					while (data.posts.length > 0) {
						var temp = data.posts.shift();
						// Set preview
						if (temp.contents.length < 200)
							temp.contents = temp.contents.substring(0, temp.contents.length);
						else
							temp.contents = temp.contents.substring(0, 200) + " [...]";
						self.userPosts.push(temp);
					}
				});
			}
		};

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
			var url = '/yilpil/posts/' + params.name + '?page=1';
			$.getJSON(url, function(data) {
				while (data.posts.length > 0) {
					var temp = data.posts.shift();
					// Set preview
					if (temp.contents.length < 200)
						temp.contents = temp.contents.substring(0, temp.contents.length);
					else
						temp.contents = temp.contents.substring(0, 200) + " [...]";
					toStore.push(temp);
				}
			});	
		};

		var getAvatar = function(toStore) {
			var url = '/yilpil/users/' + params.name;
			$.getJSON(url, function(data) {
				toStore('http://www.gravatar.com/avatar/' + data.user.hash);
			});
		};

		getUserPosts(this.userPosts);
		getUserTags(this.tags);
		getAvatar(this.gravatar);

	}
	return { viewModel: UserViewModel, template: template };
});
