define(["knockout", "text!./home.html", "app/mediator"],
 function(ko, homeTemplate, mediator) {

 	/*
	// Register the list-posts recycled component
	if (! ko.components.isRegistered('list-posts')) {
		ko.components.register('list-posts', {
			template: { require: 'text!components/recycled/list-posts.html'}
		});
	}*/

  function HomeViewModel(route) {
  	var self = this;
    this.message = ko.observable('Welcome to Yil-Pil!');
    this.latestPosts = ko.observableArray();
    this.results = ko.observable(null);

    var getUpdates = function(toStore) {
			var url = '/yilpil/updates?resource=posts';
			$.getJSON(url, function(data) {
				if(data.posts.length > 0)
					self.results(true);
				else
					self.results(null);
				mediator.summarizePosts(data, toStore);
			});	
		};
		/* Get the actual data. */
		getUpdates(this.latestPosts);
  }

  return { viewModel: HomeViewModel, template: homeTemplate };

});
