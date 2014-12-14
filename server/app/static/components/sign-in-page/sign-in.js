define(['knockout', 'text!./sign-in.html', 'knockout.validation', 'app/mediator'],
 function(ko, template, validation, mediator) {

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
		this.setWarning = ko.observable(null);

		var success = function(data) {
			document.cookie = "yt-token=" + data.token;
			document.cookie = "yt-username=" + self.username();
			self.setWarning(null);
			return window.location.href = "#user/" + self.username();
		};
		var errors = function(jqXHR, textStatus, errorThrown) {
			self.setWarning(true);
		};

		this.submit = function() {
			if (self.errors().length == 0) {
				mediator.getToken(self.username(), self.password(), success, errors);
			} else {
				self.errors.showAllMessages();
				console.log("Invalid");
			}
		}
	}
	return { viewModel: LoginViewModel, template: template };
});
