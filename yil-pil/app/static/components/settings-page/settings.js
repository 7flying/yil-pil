define(['knockout', 'text!./settings.html', 'knockout.validation', 'app/mediator'],
 	function(ko, template, validation, mediator) {
 	
	ko.validation.rules.pattern.message = 'Invalid.';

	ko.validation.configure({
		registerExtenders: true,
		messagesOnModified: true,
		insertMessages: true,
		parseInputAttributes: true,
		messageTemplate: null
	});
	
	function SettingsViewModel(params) {
		var self = this;
		this.user = ko.observable(params.user);
		this.gravatar = ko.observable();
		this.newPassword = ko.observable().extend({
			required: true,
			minLength: 8
		});
		this.newPasswordAgain = ko.observable().extend({
			required: true,
			validation: {
				validator: mediator.validateMustEqual,
				message: 'Passwords do not match',
				params: self.password
			}
		});
		this.newEmail = ko.observable().extend({
			required: true,
			pattern: {
				message: 'Enter a valid email address',
				params: '@'
			}
		});
		this.setWarning = ko.observable(null);
		this.errors = validation.group(self);

		this.submitPass = function() {
			mediator.changePass(self.newPassword(),
				mediator.getCookie('yt-username'),
				mediator.getCookie('yt-token'));
		};

		this.submitEmail = function() {
			mediator.changeEmail	
		};

		mediator.getAvatar(this.gravatar, params.user);
	}

	return { viewModel: SettingsViewModel, template: template };
});
