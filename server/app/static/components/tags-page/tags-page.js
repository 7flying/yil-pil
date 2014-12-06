define(['knockout', 'text!./tags-page.html','module', 'app/router'], function(ko, template, module, router) {

	// Register the list-posts recycled component
	if (! ko.components.isRegistered('list-posts')) {
		ko.components.register('list-posts', {
			template: { require: 'text!components/recycled/list-posts.html'}
		});
	}

	function TagsPageViewModel(params) {
		var self = this;
		this.name = ko.observable(params.name);
		this.postsByTag = ko.observableArray();
		this.results = ko.observable(null);

		var getPosts = function(toStore) {
			var url = '/yilpil/posts?tag=' + self.name();
			$.getJSON(url, function(data) {
				if (data.posts.length ==  0)
					self.results(null);
				else
					self.results("Posts with '" + params.name + "'");
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
		getPosts(this.postsByTag);
	}
	return { viewModel: TagsPageViewModel, template: template };
});
