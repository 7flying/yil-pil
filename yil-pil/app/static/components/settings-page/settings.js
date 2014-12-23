define(['knockout', 'text!./settings.html', 'app/mediator'],
 	function(ko, template, mediator) {
	
	function SettingsViewModel(params) {
		this.user = ko.observable(params.user);
		this.gravatar = ko.observable();

		mediator.getAvatar(this.gravatar, params.user);
	}	

	return { viewModel: SettingsViewModel, template: template };
});