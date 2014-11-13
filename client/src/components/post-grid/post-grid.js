define(['knockout', 'text!./post-grid.html'], function(ko, templateMarkup) {

  function PostGrid(params) {
  	// Expose a 'posts' property to the view
  	this.posts = ko.observableArray();
  	//this.posts = [ {'title': "yo", 'author': "another"}, {title: "yo", author: "another"}]
    //$.getJSON('http://localhost:5000/yilpil/updates?resource=posts', this.posts);
    var params = {'resource' : 'posts'};
    $.ajax({
        url: 'http://localhost:5000/yilpil/updates',
        type: 'GET',
        contentType: 'application/json',
        data: "resource=posts",
        dataType: 'json',
        complete: function(data) {
          window.alert(data);
          //this.channels = data.posts;
        },
        error: function(xhr, ajaxOptions, thrownError) {
          window.alert("some error");
        }
      });
    /*
    this.posts = [{
      title: "Post Num 12", author: "seven",
      contents: "Lorem ipsum dolor sit amet, consectetur adipiscing elit,\t\t sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.", 
      date: "13-11-2014 11:26", 
      id: "15",  
      votes: "0"},
      { title: "Post Num 12", author: "seven", 
      contents: "Lorem ipsum dolor sit amet, consectetur adipiscing elit,\t\t sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.", 
      date: "13-11-2014 11:26", 
      id: "15",  
      votes: "0"
    }] */
  }

    
  return { viewModel: PostGrid, template: templateMarkup };

});
