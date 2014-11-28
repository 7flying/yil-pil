define(['knockout', 'text!./user.html'], function(ko, template) {

	function UserViewModel(params) {
		this.user = ko.observable(params.name);
		this.tags = ko.observableArray();

		var getUserTags = function(toStore) {
			$.getJSON('yilpil/tags/' + params.name, function(data) {
				while(data.length > 0)
					toStore.push(data.shift());
			});
		};

		getUserTags(this.tags);
	}
	return { viewModel: UserViewModel, template: template };
});