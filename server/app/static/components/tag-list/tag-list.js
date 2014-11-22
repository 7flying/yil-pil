define(['knockout', 'text!./tag-list.html'], function(ko, template) {

	function TagListViewModel(params) {
		/* Static data to know if it it's working *//*
		this.tags = [{ name: "hello", num: "15"}, { name: "world", num: "15"}];*/
		this.tags = ko.observableArray();
		var getPopular = function(toStore) {
			$.getJSON('/yilpil/ranking?resource=tags', function(data) {
				while(data.tags.length > 0)
					toStore.push(data.tags.shift())
			});
		};
		/* Populate the array */
		getPopular(this.tags)
	}
	return { viewModel: TagListViewModel, template: template };
});
