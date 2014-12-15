define(['knockout', 'text!./nav-bar.html', 'app/mediator'],
	function(ko, template, mediator) {

	ko.bindingHandlers.executeOnEnter = {
		init: function (element, valueAccessor, allBindingsAccessor, viewModel) {
			var allBindings = allBindingsAccessor();
			$(element).keypress(function(event) {
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
		this.user = ko.observable(null);

		this.query = ko.observable();
		this.sendQuery = function () {
			if (self.query() != undefined) {
				return window.location.href = '#search/'
				 + encodeURIComponent(self.query());
			}
		};
		this.logout = function() {
			// delete stored cookies
			document.cookie = 'yt-token=; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
			document.cookie = 'yt-username=; expires=Thu, 01 Jan 1970 00:00:01 GMT;'
			// redirect to home
			return window.location.href = '#';
		};

		var getUser = function() {
			var cookie = mediator.getCookie('yt-username');
			if (cookie != null) {
				self.user(cookie);
			} else
				self.user(null);
		};
		setInterval(getUser, 3000);
	}

	return { viewModel: NavBarViewModel, template: template };
});
