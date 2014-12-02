// require.js looks for the following global when initializing
var require = {
    baseUrl: "./",
    paths: {
        "bootstrap":            "bower_modules/components-bootstrap/js/bootstrap.min",
        "bootstrapvalidator":   "bower_modules/bootstrapvalidator/src/js/bootstrapValidator",
        "crossroads":           "bower_modules/crossroads/dist/crossroads.min",
        "eonasdan-bootstrap-datetimepicker":
                                "bower_modules/eonasdan-bootstrap-datetimepicker/src/js/bootstrap-datetimepicker",
        "hasher":               "bower_modules/hasher/dist/js/hasher.min",
        "jquery":               "bower_modules/jquery/dist/jquery",
        "knockout":             "bower_modules/knockout/dist/knockout",
        "knockout-projections": "bower_modules/knockout-projections/dist/knockout-projections",
        "knockout-postbox":     "bower_modules/knockout-postbox/build/knockout-postbox",
        "moment":               "bower_modules/moment/min/moment.min",
        "request":              "bower_modules/request/request",
        "signals":              "bower_modules/js-signals/dist/signals.min",
        "text":                 "bower_modules/requirejs-text/text"
    },
    shim: {
        "bootstrap": { deps: ["jquery"] }
    }
};
