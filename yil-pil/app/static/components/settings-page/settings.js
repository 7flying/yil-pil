define(['knockout', 'text!./settings.html', 'app/mediator'],
 	function(ko, template, mediator) {
	
	function SettingsViewModel(params) {
		this.user = ko.observable(params.user);
		this.gravatar = ko.observable();
		this.newPassword = ko.observable();
		this.newPasswordAgain = ko.observable();
		this.newEmail = ko.observable();
		this.setWarning = ko.observable(null);

		this.submitPass = function() {
			
		};

		this.submitEmail = function() {
			
		};

		mediator.getAvatar(this.gravatar, params.user);
	}	

	return { viewModel: SettingsViewModel, template: template };
});