define(['knockout', 'text!./post-editor.html', 'marked'], function(ko, template, marked) {

	function PostEditorViewModel(params) {
		var self = this;
		this.mdTitle = ko.observable();
		this.mdContents = ko.observable();
		this.title = ko.observable();
		this.contents = ko.observable();

		this.generate = function() {
			console.log(marked(self.mdContents()));
			self.contents(marked(self.mdContents()));
		}
	}

	return { viewModel: PostEditorViewModel, template: template };
});