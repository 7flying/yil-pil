define(['knockout', 'text!./post-editor.html', 'marked'], function(ko, template, marked) {

	function PostEditorViewModel(params) {
		var self = this;
		this.mdTitle = ko.observable();
		this.mdContents = ko.observable();
		this.title = ko.observable();
		this.contents = ko.observable();

		this.mdTitle.subscribe(function(newValue) {
			self.title(newValue);
		});

		var generateHTML = function(text) {
			$('#preview-contents').empty();
			$('#preview-contents').append(marked(text));
		}

		this.mdContents.subscribe(function(newValue) {
			generateHTML(newValue);
		});
	}

	return { viewModel: PostEditorViewModel, template: template };
});