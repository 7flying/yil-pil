define(['knockout', 'text!./post-grid.html'], function(ko, templateMarkup) {

  function PostGrid(params) {
  	// Expose a 'posts' property to the view
  	this.posts = ko.observableArray();
  	//this.posts = [ {'title': "yo", 'author': "another"}, {title: "yo", author: "another"}]
    /* Deja la respuesta en response header */
    /*
    var res;
    $.getJSON('http://localhost:5000/yilpil/updates?resource=posts&callback=?', function(data) {
      res = data;
      window.alert(res);
    });
    */
     //var url = 'http://localhost:5000/yilpil/updates?resource=posts&callback=?';
    /*
    var sendData = function(url, method, data){
      var request = {
                    url: url,
                    type: method,
                    contentType: "application/json",
                    accepts: "application/json",
                    cache: false,
                    dataType: 'json',
                    data: JSON.stringify(data),
                    error: function(jqXHR) {
                        console.log("ajax error " + jqXHR.status);
                    }
                };
                return $.ajax(request);
      }
    var response = sendData(url, 'GET').done(function(data) {
      console.log(data);
    });
    console.log(response);
    */
    //$.getJSON(url, function(data){ console.log(data); });

    /*
    $.ajax({
      type: 'GET',
      url: url,
      contentType: "application/json",
      dataType: 'jsonp',
      jsonpCallback: 'local'
    });
    function local(json) {
      console.log(json);
    }
    */
    /*
    $.ajax({
      url: 'http://localhost:5000/yilpil/updates?resource=posts&callback=?',
      dataType: 'json',
      jsonpCallback: function(back) {
        alert("at back");
        console.log(back);
      }, // specify the callback name if you're hard-coding it
      success: function(data){
      // we make a successful JSONP call!
        alert("at success");
        console.log(data);   
      }
    });
    */
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
    var request = require(['request']);
    request('http://www.google.com', function (error, response, body) {
      if (!error && response.statusCode == 200) {
        console.log(body) // Print the google web page.
      }
    })};

    
  return { viewModel: PostGrid, template: templateMarkup };

});
