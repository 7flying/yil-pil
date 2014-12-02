define(['knockout', 'text!./sign-up.html', 'knockout.validation'], function(ko, template, validation) {

	ko.validation.rules.pattern.message = 'Invalid.';

	ko.validation.configure({
		registerExtenders: true,
		messagesOnModified: true,
		insertMessages: true,
		parseInputAttributes: true,
		messageTemplate: null
	});

	function mustEqual(val, other) {
		return val == other();
	};

	function JoinViewModel(params) {
		var self = this;
		this.username = ko.observable().extend({
			required: true,
			minLength: 3,
			maxLength: 15
		});
		this.email = ko.observable().extend({
			required: true,
			pattern: {
				message: 'Enter a valid email adress',
				params: "@"
			}
		});
		this.password = ko.observable().extend({
			required: true,
			minLength: 8
		})
		this.passAgain = ko.observable().extend({
			required: true,
			validation: {
				validator: mustEqual,
				message: 'Passwords do not match',
				params: self.password
			}
		});
		this.errors = validation.group(self);

		this.submit = function() {
			if (self.errors().length == 0) {
				console.log("Good")
			} else {
				self.errors.showAllMessages();
			}
		};

	}


	return { viewModel: JoinViewModel, template: template };
});
