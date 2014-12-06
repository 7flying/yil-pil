define(['knockout', 'text!./search.html','module', 'app/router'], function(ko, template, module, router) {

	// Register the list-posts recycled component
	if (! ko.components.isRegistered('list-posts')) {
		ko.components.register('list-posts', {
			template: { require: 'text!components/recycled/list-posts.html'}
		});
	}

	function SearchViewModel(params) {
		var self = this;
		this.query = ko.observable(params.query);
		this.searchPosts = ko.observableArray();
		this.results = ko.observable(null);
		this.similarTags = ko.observableArray();
		this.similarTagsResults = ko.observable(null);
		
		var getPosts = function(toStore) {
			var url = '/yilpil/search/posts/title?title=' + self.query();
			$.getJSON(url, function(data) {
				if (data.posts.length ==  0)
					self.results(null);
				else
					self.results(data.posts.length + " posts matched:");
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

		var getSimilarTags = function(toStore) {
			var url = 'yilpil/search/tag?letter=' + self.query()[0];
			$.getJSON(url, function(data) {
				if (data.tags.length ==  0)
					self.similarTagsResults(null);
				else
					self.similarTagsResults(true);
				while (data.tags.length > 0) {
					toStore.push(data.tags.shift());
				}
			});
		};

		getPosts(this.searchPosts);
		getSimilarTags(this.similarTags);
	}
	return { viewModel: SearchViewModel, template: template };
});
