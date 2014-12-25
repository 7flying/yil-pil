define(['knockout', 'text!./post-editor.html', 'marked', 'app/mediator'],
	function(ko, template, marked, mediator ) {

	// key listener
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

	Array.prototype.contains = function(element) {
		for (var i in this)
			if (this[i] == element)
				return true;
		return false;
	};

	function PostEditorViewModel(params) {
		var self = this;
		this.pageTitle = ko.observable();
		this.setWarning = ko.observable(null);
		this.setContentWarning = ko.observable(null);
		this.session = ko.observable(null);
		this.mdTitle = ko.observable("");
		this.mdContents = ko.observable("");
		this.mdTags = ko.observableArray([]);
		this.title = ko.observable();
		this.contents = ko.observable();
		this.tags = ko.observableArray();
		this.tag = ko.observable();

		this.mdTitle.subscribe(function(newValue) {
			self.title(newValue);
		});

		var titleConcat = "What have you learnt today";

		var generateHTML = function(text) {
			$('#preview-contents').empty();
			$('#preview-contents').append(marked(text));
		}

		this.mdContents.subscribe(function(newValue) {
			generateHTML(newValue);
		});

		this.addTag = function() {
			// If the tag is repeated ignore it.
			if (!self.mdTags().contains(self.tag())) {
				self.mdTags.push(self.tag());
				self.tags.push(self.tag());	
			}
		};

		this.removeTag = function(tag) {
			self.tags.remove(tag);
			self.mdTags.remove(tag);
		};

		this.submit = function() {
			var data = {};
			data['contents'] = self.mdContents();
			data['title'] = self.mdTitle();
			data['tags'] = self.mdTags().length == 0 ? [] : self.mdTags().toString();
			if (data['contents'].length == 0 || data['title'].length == 0)
				self.setContentWarning(true);
			else {
				data['username'] = mediator.getCookie('yt-username');
				mediator.createPost(data, mediator.getCookie('yt-token'));	
			}
		};

		var setContent = function() {
			var cookie = mediator.getCookie("yt-username");
			if (cookie != null) {
				self.pageTitle(titleConcat + ", " + cookie + "?");
				self.session(true);
			} else {
				self.pageTitle(titleConcat + "?");
				self.setWarning(true);
			}
		};
		setContent();
	}

	return { viewModel: PostEditorViewModel, template: template };
});
