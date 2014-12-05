define(['knockout', 'text!./post-editor.html', 'marked', 'highlight'],
 function(ko, template, marked, hljs) {

	ko.bindingHandlers.executeOnEnter = {
		init: function(element, valueAccessor, allBindingsAccesor, viewModel) {
			var allBindings = allBindingsAccesor();
			$(element).keypress(function(event) {
				var keyCode = (event.which ? event.which : event.keyCode);
				if (keyCode === 13) {
					allBindings.executeOnEnter.call(viewModel);
					return false;
				}
				return true;
			});
		}
	};
	marked.setOptions({
		renderer: new marked.Renderer(),
		gfm: true,
		tables: true,
		breaks: false,
		pedantic: false,
		sanitize: true,
		highlight: function(code) {
			return hljs.highlightAuto(code).value;
		},
		smartLists: true,
		smartypants: false
	});

	function PostEditorViewModel(params) {
		$(function() {
			hljs.initHighlightingOnLoad();
		});
		var self = this;
		this.mdTitle = ko.observable();
		this.mdContents = ko.observable();
		this.title = ko.observable();
		this.contents = ko.observable();
		this.tags = ko.observableArray();
		this.tag = ko.observable();

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

		this.addTag = function() {
			self.tags.push(self.tag());
		};
	}

	return { viewModel: PostEditorViewModel, template: template };
});