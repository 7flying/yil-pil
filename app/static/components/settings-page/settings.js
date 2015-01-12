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
			minLength: 3
		});
		this.newPasswordAgain = ko.observable().extend({
			required: true,
			validation: {
				validator: mediator.validateMustEqual,
				message: 'Passwords do not match',
				params: self.newPassword
			}
		});
		this.newEmail = ko.observable().extend({
			required: true,
			pattern: {
				message: 'Enter a valid email address',
				params: '@'
			}
		});
		this.confirmation = ko.observable().extend({
			required: true,
			validation: {
				validator: mediator.validateDeleteAccount
			}
		});
		this.setSuccess = ko.observable(null);
		this.setWarning = ko.observable(null);
		this.displayGoodbye = ko.observable(null);

		this.errorsPass = validation.group([self.newPassword, self.newPasswordAgain]);
		this.errorsEmail = validation.group([self.newEmail]);
		this.errorsDelete = validation.group([self.confirmation]);

		var success = function(data) {
			self.setWarning(null);
			self.setSuccess(true);
		};
		var successPass = function(data) {
			success(data);
			mediator.getToken(mediator.getCookie('yt-username'), self.newPassword());
		};
		var successEmail = function(data) {
			success(data);
			// Update gravatar
			mediator.getAvatar(self.gravatar, mediator.getCookie('yt-username'));
		};
		var succesDelete = function(data) {
			self.displayGoodbye(true);
			setTimeout(function() {
				document.cookie = 'yt-token=; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
				document.cookie = 'yt-username=; expires=Thu, 01 Jan 1970 00:00:01 GMT;'
				// redirect to home
				return window.location.href = '#';
			}, 2000);
		};
		var error = function(jqXHR, textStatus, errorThrown) {
			self.setWarning(true);
			self.setSuccess(null);
		};

		this.submitPass = function() {
			self.setWarning(null);
			self.setSuccess(null);
			if (self.errorsPass().length == 0) {
				mediator.changePass(self.newPassword(),
					mediator.getCookie('yt-username'),
					mediator.getCookie('yt-token'),
					successPass, error);
			} else {
				self.errorsPass.showAllMessages();
			}
		};

		this.submitEmail = function() {
			self.setWarning(null);
			self.setSuccess(null);
			if (self.errorsEmail().length == 0) {
				mediator.changeEmail(self.newEmail(),
					mediator.getCookie('yt-username'),
					mediator.getCookie('yt-token'),
					successEmail, error);
			} else {
				self.errorsEmail.showAllMessages();
			}
			
		};

		this.deleteAccount = function() {
			if (self.errorsDelete().length == 0) {
				mediator.deleteUser(mediator.getCookie('yt-username'),
									mediator.getCookie('yt-token'),
									succesDelete, error);
			} else {
				self.errorsDelete.showAllMessages();
			}
		};

		mediator.getAvatar(this.gravatar, mediator.getCookie('yt-username'));
	}

	return { viewModel: SettingsViewModel, template: template };
});
