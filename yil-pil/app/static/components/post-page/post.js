define(['knockout', 'text!./post.html', 'marked'], 
	function(ko, template, marked) {

	// markdown
	marked.setOptions({
		renderer: new marked.Renderer(),
		gfm: true,
		tables: true,
		breaks: false,
		pedantic: false,
		sanitize: true,
		smartLists: true,
		smartypants: false
	});

	function PostViewModel(params) {
		var self = this;
		this.title = ko.observable();
		this.author = ko.observable();
		this.date = ko.observable();
		this.contents = ko.observable();
		this.votes = ko.observable();
		this.tags = ko.observableArray();
		var setContents = function(contents) {
			$('#contents').empty();
			$('#contents').append(contents);
		};
		var getPost = function() {
			$.getJSON('/yilpil/post/' + params.postId, function(data){
				var post = {};
				self.title(data.post.title);
				self.author(data.post.author);
				self.contents(marked(data.post.contents));
				setContents(self.contents());
				self.votes(data.post.votes);
				self.date(data.post.date);
				self.tags([]);
				while (data.post.tags.length > 0)
					self.tags.push(data.post.tags.shift());
			});
		};
		getPost();
	}
	
	return { viewModel: PostViewModel, template: template };
});
