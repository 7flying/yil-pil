define(['knockout', 'text!./user.html', 'module', 'app/router', 'bootstrap-datetimepicker'], function(ko, template, module, router, datetimepicker) {

	// Register the user-posts component
	ko.components.register('user-posts', {
		template: { require: 'text!components/user-page/user-posts.html'}
	});

	function UserViewModel(params) {
		var self = this;
		this.userPosts = ko.observableArray();
		this.user = ko.observable(params.name);
		this.tags = ko.observableArray();
		this.displayTitle = ko.observable('Latest posts: ');

		this.filterPosts = function() {
			console.log("Filter posts clicked:");
			console.log("From: " + $('#text-from').val());
			console.log("To: " + $('#text-to').val());
			var from = $('#text-from').val().match(/\d/g);
			var to = $('#text-to').val().match(/\d/g);
			console.log(from);
			console.log(to);
			if (from.length == 8 && to.length == 8) {
				console.log(from);
				console.log(to);
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

		getUserPosts(this.userPosts);
		getUserTags(this.tags);

	}
	return { viewModel: UserViewModel, template: template };
});
