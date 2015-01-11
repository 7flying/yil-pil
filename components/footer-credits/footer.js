define(['knockout', 'text!./footer.html'], function(ko, template) {

	function FooterViewModel(params) {
		this.year = ko.observable();
		this.year(new Date().getFullYear());
	}

	return { viewModel: FooterViewModel, template: template };
});
