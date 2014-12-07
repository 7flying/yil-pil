define(['jquery', 'knockout', './router', 'bootstrap', 'knockout-projections'], function($, ko, router) {

  // Components can be packaged as AMD modules, such as the following:
  ko.components.register('nav-bar', { require: 'components/nav-bar/nav-bar' });
  ko.components.register('home-page', { require: 'components/home-page/home' });

  // ... or for template-only components, you can just point to a .html file directly:
  ko.components.register('about-page', {
    template: { require: 'text!components/about-page/about.html' }
  });
  ko.components.register('footer-credits', {
    template: { require: 'text!components/footer-credits/footer.html' }
  });

  ko.components.register('sign-in-page', { require: 'components/sign-in-page/sign-in' });
  ko.components.register('sign-up-page', { require: 'components/sign-up-page/sign-up' });
  ko.components.register('post-page', { require: 'components/post-page/post' });
  ko.components.register('user-page', { require: 'components/user-page/user' });
  ko.components.register('search-page', { require: 'components/search-page/search' });
  ko.components.register('editor-page', { require: 'components/editor-page/editor' });
  ko.components.register('rankings-page', { require: 'components/rankings-page/rankings-page'});
  ko.components.register('tag-list', { require: 'components/tag-list/tag-list' });
  ko.components.register('post-editor', { require: 'components/post-editor/post-editor' });
  ko.components.register('tags-page', { require: 'components/tags-page/tags-page'});
  // [Scaffolded component registrations will be inserted here. To retain this feature, don't remove this comment.]

  // Start the application
  ko.applyBindings({ route: router.currentRoute });
});
