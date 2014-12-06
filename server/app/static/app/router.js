define(["knockout", "crossroads", "hasher"], function(ko, crossroads, hasher) {

    // This module configures crossroads.js, a routing library. If you prefer, you
    // can use any other routing library (or none at all) as Knockout is designed to
    // compose cleanly with external libraries.
    //
    // You *don't* have to follow the pattern established here (each route entry
    // specifies a 'page', which is a Knockout component) - there's nothing built into
    // Knockout that requires or even knows about this technique. It's just one of
    // many possible ways of setting up client-side routes.

    var router = {
        currentRoute: ko.observable({}),
        routes: {
            home:           route('', { page: 'home-page' }),
            about:          route('about', { page: 'about-page' }),
            login:          route('login', { page: 'sign-in-page' }),
            join:           route('join', { page: 'sign-up-page' }),
            editor:         route('editor', { page: 'editor-page'}),
            post:           route('post/{postId}', { page: 'post-page' }),
            user:           route('user/{name}', { page: 'user-page' }),
            search:         route('search/{query}', { page: 'search-page' }),
            tag:            route('tag/{name}', { page: 'tags-page' })
        }
    };

    activateCrossroads();
    return router;

    function route(url, routeParams) {
        return crossroads.addRoute(url, function(requestParams) {
            router.currentRoute(ko.utils.extend(requestParams, routeParams));
        });
    }

    function activateCrossroads() {
        function parseHash(newHash, oldHash) { crossroads.parse(newHash); }
        crossroads.normalizeFn = crossroads.NORM_AS_OBJECT;
        hasher.initialized.add(parseHash);
        hasher.changed.add(parseHash);
        hasher.init();
    }
});