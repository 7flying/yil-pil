define(['knockout', 'text!./settings.html', 'app/mediator'],
 	function(ko, template, mediator) {
	
	function SettingsViewModel(params) {
		this.user = ko.observable(params.user);
		this.gravatar = ko.observable();
		this.password = ko.observable();
		this.newPassword = ko.observable();
		this.newEmail = ko.observable();
		this.setWarning = ko.observable(null);

		this.submit = function() {

		};

		mediator.getAvatar(this.gravatar, params.user);
	}	

	return { viewModel: SettingsViewModel, template: template };
});