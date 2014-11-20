define(['knockout', 'text!./post-list.html'], function(ko, template) {

	function PostListViewModel(params) {
		this.message = ko.observable('Hello from the component!');
		/* Static data to know if it it's working */
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
	}

	return { viewModel: PostListViewModel, template: template };
});
