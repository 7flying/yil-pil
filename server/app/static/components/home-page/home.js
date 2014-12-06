define(["knockout", "text!./home.html"], function(ko, homeTemplate) {

	// Register the list-posts recycled component
	if (! ko.components.isRegistered('list-posts')) {
		ko.components.register('list-posts', {
			template: { require: 'text!components/recycled/list-posts.html'}
		});
	}

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
		/* Get the actual data. */
		getUpdates(this.latestPosts);
  }

  return { viewModel: HomeViewModel, template: homeTemplate };

});
