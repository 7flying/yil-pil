define(['knockout', 'text!./user.html', 'module', 'app/router'], function(ko, template, module, router) {

	// Register the user-posts component
	ko.components.register('user-posts', {
		template: { require: 'text!components/user-page/user-posts.html'}
	});

	function UserViewModel(params) {
		this.userPosts = ko.observableArray();
		this.user = ko.observable(params.name);
		this.tags = ko.observableArray();

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
