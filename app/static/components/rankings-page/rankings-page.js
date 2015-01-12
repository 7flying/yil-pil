define(['knockout', 'text!./rankings-page.html', 'module', 'app/router',
 'app/mediator'], function(ko, template, module, router, mediator) {

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
				mediator.summarizePosts(data, self.rankingPosts);
			});
		};
		// Gets the category/tag specific ranking
		this.getRankingTag = function(category) {
			self.rankingPosts.removeAll();
			self.rankingTitle("Ranking of category '" + category + "'");
			var url = 'yilpil/ranking?resource=posts&category=' + category;
			$.getJSON(url, function(data) {
				self.results(data.posts.length > 0 ? true : null);
				mediator.summarizePosts(data, self.rankingPosts);
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
