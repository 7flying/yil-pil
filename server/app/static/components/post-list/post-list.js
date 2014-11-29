define(['knockout', 'text!./post-list.html'], function(ko, template) {

	function PostListViewModel(params) {
		/* Static data to know if it it's working *//*
		this.posts = [{ title: "Post Num 12", author: "seven",
						contents: "Lorem ipsum dolor sit amet",
						date: "13-11-2014 11:26",
						id: "15",
						tags: ["hello", "again"],
						votes: "0"},
					 { title: "Post Num 12", author: "seven",
						contents: "Lorem ipsum dolor sit",
						date: "13-11-2014 11:26",
						id: "15",
						tags: ["hello", "again"],
						votes: "0"
					}];
		*/
		var self = this;
		this.posts = ko.observableArray();

		var getUpdates = function(toStore) {
			var url = '/yilpil/updates?resource=posts';
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
		/* Get the actual data. */
		getUpdates(this.posts);
	}
	return { viewModel: PostListViewModel, template: template };
});
