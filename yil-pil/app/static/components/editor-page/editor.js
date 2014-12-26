define(['knockout', 'text!./editor.html', 'app/mediator'],
 function(ko, template, mediator) {

	function EditorViewModel(params) {
		var self = this;
		this.pageTitle = ko.observable();

		var titleConcat = "What have you learnt today";

		var setContent = function() {
			var cookie = mediator.getCookie("yt-username");
			self.pageTitle(cookie == null 
						   ? titleConcat + "?"
						   : titleConcat + ", " + cookie + "?");
		};
		setContent();
	}

	return { viewModel: EditorViewModel, template: template };
});