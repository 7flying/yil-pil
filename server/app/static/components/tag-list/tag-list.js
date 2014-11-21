define(['knockout', 'text!./tag-list.html'], function(ko, template) {

	function TagListViewModel(params) {
		/* Static data to know if it it's working */
		this.tags = [{ name: "hello", num: "15"}, { name: "world", num: "15"}];
	}
	return { viewModel: TagListViewModel, template: template };
});
