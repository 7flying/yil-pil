define(['knockout', 'text!./search.html','module', 'app/router'], function(ko, template, module, router) {

	// Register the list-posts recycled component
	ko.components.register('list-posts', {
		template: { require: 'text!components/recycled/list-posts.html'}
	});

	function SearchViewModel(params) {
		var self = this;
		this.query = ko.observable(params.query);
		this.searchPosts = ko.observableArray();

		var getPosts = function(toStore) {
			var url = '/yilpil/search/posts/title?title=' + self.query();
			$.getJSON(url, function(data) {
				while (data.length > 0) {
					var temp = data.shift();
					// Set preview
					if (temp.contents.length < 200)
						temp.contents = temp.contents.substring(0, temp.contents.length);
					else
						temp.contents = temp.contents.substring(0, 200) + " [...]";
					toStore.push(temp);
				}
			});	
		};
		getPosts(this.searchPosts);
	}
	return { viewModel: SearchViewModel, template: template };
});