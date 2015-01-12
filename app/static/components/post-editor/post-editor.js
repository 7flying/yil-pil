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
		// Check whether we are on edit or creation mode
		var editMode = typeof params.title != 'undefined';
		this.setContentWarning = ko.observable(null);
		this.session = ko.observable(null);
		this.mdTitle = ko.observable("");
		this.mdContents = ko.observable("");
		this.mdTags = ko.observableArray([]);
		this.title = ko.observable();
		this.contents = ko.observable();
		this.tags = ko.observableArray();
		this.tag = ko.observable();
		this.id = ko.observable(null);
		try {
			self.id(params.id());
		} catch(err) {
			self.id(null);
		}
		this.mdTitle.subscribe(function(newValue) {
			self.title(newValue);
		});
		try {
			self.mdTitle(params.title());
		} catch(err) {
			self.mdTitle("");
		}

		var generateHTML = function(text) {
			$('#preview-contents').empty();
			$('#preview-contents').append(marked(text));
		}

		this.mdContents.subscribe(function(newValue) {
			generateHTML(newValue);
		});
		// add content from arguments
		try {
			self.mdContents(params.contents());
		} catch(err) {
			self.mdContents("");
		}
		// add tags from arguments
		try {
			params.tags().forEach(function(item) {
				self.tags.push(item);
				self.mdTags.push(item);
			});
		} catch(err) {}

		var storeTag = function(tag) {
			self.mdTags.push(tag);
			self.tags.push(tag);
		};

		this.addTag = function() {
			// If the tag is repeated ignore it.
			if (!self.mdTags().contains(self.tag())) {
				storeTag(self.tag());
				$('#tagAdder').val('');
			}
		};

		this.removeTag = function(tag) {
			self.tags.remove(tag);
			self.mdTags.remove(tag);
		};

		this.submit = function() {
			var data = {};
			data['contents'] = self.mdContents();
			console.log(self.mdContents());
			data['title'] = self.mdTitle();
			var temp = "";
			var first = true;
			// generate b64 of every tag and concatenate them
			self.mdTags().forEach(function(item){
				if (first) {
					temp += btoa(item);
					first = false;
				} else
					temp += ":" + btoa(item);
				console.log(temp);
			});
			data['tags'] = temp;
			if (data['contents'].length == 0 || data['title'].length == 0)
				self.setContentWarning(true);
			else {
				data['username'] = mediator.getCookie('yt-username');
				if (editMode) {
					data['id'] = self.id();
					mediator.updatePost(data, mediator.getCookie('yt-token'));
				} else {
					// Creation mode
					console.log("sending: " + data.toString());
					mediator.createPost(data, mediator.getCookie('yt-token'));	
				}
			}
		};

		var setContent = function() {
			var cookie = mediator.getCookie("yt-username");
			self.session(cookie == null ? null : true);
		};
		setContent();
	}

	return { viewModel: PostEditorViewModel, template: template };
});
