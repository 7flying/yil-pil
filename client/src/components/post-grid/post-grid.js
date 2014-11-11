define(['knockout', 'text!./post-grid.html'], function(ko, templateMarkup) {

  function PostGrid(params) {
  	// Expose a 'posts' property to the view
  	this.posts = ko.observableArray();
  	// Populate array via ajax
  	//$.getJSON('http://localhost:5000/yilpil/post/2', this.channels);
  	$.getJSON({
  		url: 'http://localhost:5000/yilpil/updates',
  		data: {resource: "posts"},
  		success: function(data) { this.channels = data; }
  	});
  
  }

    
  return { viewModel: PostGrid, template: templateMarkup };

});
