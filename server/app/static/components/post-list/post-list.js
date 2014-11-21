define(['knockout', 'text!./post-list.html'], function(ko, template) {

	function PostListViewModel(params) {
		this.message = ko.observable('Hello from the component!');
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
		this.posts = ko.observableArray();
		var getUpdates = function(toStore) {
			$.getJSON('/yilpil/updates?resource=posts', function(data) {
				while(data.posts.length > 0)
					toStore.push(data.posts.pop());
			});	
		}
		/* Get the actual data. */
		getUpdates(this.posts);
	}
	return { viewModel: PostListViewModel, template: template };
});
