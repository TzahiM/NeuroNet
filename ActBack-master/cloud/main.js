// Use Parse.Cloud.define to define as many cloud functions as you want.
// For example:

Parse.Cloud.define("addActBack", function (request, response) {
    Parse.Cloud.useMasterKey();

    var Actback = Parse.Object.extend("Actback");
    var actback = new Actback();

    var data = {
        sourceUrl: request.params.sourceUrl,
        destinationUrl: request.params.destinationUrl,
        title: request.params.title,
        subtitle: request.params.subtitle,
        actType: request.params.actType
    };

    actback.save(data, {
        success: function (actBack) {
            response.success(actBack.toJSON());
        },
        error: function (actBack, error) {
            response.error(error);
        }
    });

});

