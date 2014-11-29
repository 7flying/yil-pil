define(['knockout', 'text!./nav-bar.html'], function(ko, template) {

	ko.bindingHandlers.executeOnEnter = {
		init: function (element, valueAccessor, allBindingsAccessor, viewModel) {
			var allBindings = allBindingsAccessor();
			$(element).keypress(function (event) {
				var keyCode = (event.which ? event.which : event.keyCode);
				if (keyCode === 13) {
					allBindings.executeOnEnter.call(viewModel);
					return false;
				}
				return true;
			});
		}
	};

	function NavBarViewModel(params) {

		var self = this;
		this.route = params.route;

		self.query = ko.observable();
		self.sendQuery = function () {
			if (self.query() != undefined) {
				return window.location.href = '#search/'
				 + encodeURIComponent(self.query());
			}
		};
	}

	return { viewModel: NavBarViewModel, template: template };
});
