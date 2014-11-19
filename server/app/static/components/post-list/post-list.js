ko.components.register('post-list', {
	viewModel: function(params) {
		this.posts = ko.onservableArray();
		this.posts = [ {'title': "yo", 'author': "another"}, {title: "yo", author: "another"}];
	},
	template:
		'<ul data-bind="foreach: posts">
			<li>
				<h3 data-bind="text: title"></h3>
				<p data-bind="text: author"></p>
				<p data-bind="text: contents"></p>
				<p data-bind="text: date"></p>
				<p data-bind="text: id"></p>
				<p data-bind="text: votes"></p>
			</li>
		</ul>'
});
ko.applyBindings();