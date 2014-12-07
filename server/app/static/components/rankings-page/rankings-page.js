define(['knockout', 'text!./rankings-page.html','module', 'app/router'], function(ko, template, module, router) {

	// Register the list-posts recycled component
	if (! ko.components.isRegistered('list-posts')) {
		ko.components.register('list-posts', {
			template: { require: 'text!components/recycled/list-posts.html'}
		});
	}

	function RankingsPageViewModel(params) {
		var self = this;
		this.index = ko.observableArray();
		this.tagsInCat = ko.observableArray();
		this.categories = ko.observable(null);
		this.rankingTitle = ko.observable("Global Ranking");
		this.rankingPosts = ko.observableArray();
		this.results = ko.observable(null);

		// Gets the tags identified by the symbol
		this.getTags = function(symbol) {
			var url = 'yilpil/index?symbol=' + symbol;
			$.getJSON(url, function(data) {
				self.tagsInCat.removeAll();
				self.categories(data.tags.length > 0 ? true : null);
				while (data.tags.length > 0)
					self.tagsInCat.push(data.tags.shift());
			});
		};
		// Gets the global post ranking
		this.getRankingGlobal = function() {
			self.rankingPosts.removeAll();
			self.rankingTitle("Global Ranking");
			var url = 'yilpil/ranking?resource=posts';
			$.getJSON(url, function(data) {
				self.results(data.posts.length > 0 ? true : null);
				while (data.posts.length > 0) {
					var temp = data.posts.shift();
					// Set preview
					if (temp.contents.length < 200)
						temp.contents = temp.contents.substring(0, temp.contents.length);
					else
						temp.contents = temp.contents.substring(0, 200) + " [...]";
					self.rankingPosts.push(temp);
				}
			});
		};
		// Gets the category/tag specific ranking
		this.getRankingTag = function(category) {
			self.rankingPosts.removeAll();
			self.rankingTitle("Ranking of category '" + category + "'");
			var url = 'yilpil/ranking?resource=posts&category=' + category;
			$.getJSON(url, function(data) {
				self.results(data.posts.length > 0 ? true : null);
				while (data.posts.length > 0) {
					var temp = data.posts.shift();
					// Set preview
					if (temp.contents.length < 200)
						temp.contents = temp.contents.substring(0, temp.contents.length);
					else
						temp.contents = temp.contents.substring(0, 200) + " [...]";
					self.rankingPosts.push(temp);
				}
			});
		};

		var getIndex = function() {
			var url = 'yilpil/index';
			$.getJSON(url, function(data) {
				while (data.index.length > 0)
					self.index.push(data.index.shift());
			});
		};	

		getIndex();
		this.getRankingGlobal();
	}

	return { viewModel: RankingsPageViewModel, template: template };
});
