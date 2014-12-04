define(['knockout', 'text!./sign-in.html', 'knockout.validation'],
 function(ko, template, validation) {

	ko.validation.rules.pattern.message = 'Invalid.';

	ko.validation.configure({
		registerExtenders: true,
		messagesOnModified: true,
		insertMessages: true,
		parseInputAttributes: true,
		messageTemplate: null
	});

	function LoginViewModel(params) {
		var self = this;
		this.username = ko.observable().extend({
			required: true,
			minLegth: 3
		});
		this.password = ko.observable().extend({
			required: true
		});
		this.errors = validation.group(self);

		this.submit = function() {
			if (self.errors().length == 0) {
				console.log("Login successful");
			} else {
				self.errors.showAllMessages();
				console.log("Invalid");
			}
		}
	}
	return { viewModel: LoginViewModel, template: template };
});
