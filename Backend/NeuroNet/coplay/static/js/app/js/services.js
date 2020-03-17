'use strict';

/* Services */


/*
- = + -- ++ <= => < > != ^ && % * << <<< >> || 

var phonecatServices = angular.module('phonecatServices', ['ngResource']);

phonecatServices.factory('Phone', ['$resource',
  function($resource){
    return $resource('phones/:phoneId.json', {}, {
      query: {method:'GET', params:{phoneId:'phones'}, isArray:true}
    });
  }]);

*/

/**/
/*http://angular.github.io/angular-phonecat/step-12/app/#/phones*/

/* http://stackoverflow.com/questions/21102690/angularjs-not-detecting-access-control-allow-origin-header */
/* https://github.com/TzahiM/NeuroNet/blob/master/kuterless/coplay/urls.py */
/*
var phonecatServices = angular.module('phonecatServices', ['ngResource']);

phonecatServices.factory('Phone', ['$resource',
  function($resource){
    return $resource('http://kuterless.org.il/labs/coplay/api/discussions/', {}, {
      query: {method:'GET', params:{id:'8'}, isArray:true}
    });
  }]);


angular.module('myApp.services', ['ngResource']).
  factory("geoProvider", function($resource) {
    return {
      states: $resource('../data/states.json', {}, {
        query: { method: 'GET', params: {}, isArray: false }
      }),
      countries: $resource('../data/countries.json', {}, {
        query: { method: 'GET', params: {}, isArray: false }
      })
    };
  });


*/
var kuterlessServices = angular.module('kuterlessServices', ['ngResource']);

//https://docs.angularjs.org/api/ngMock/service/$httpBackend
//https://docs.angularjs.org/api/ngResource/service/$resource

kuterlessServices.factory('$stream', ['$resource',
  function($resource){
    return {
      discussions: $resource('http://kuterless.org.il/labs/coplay/api/discussions/', {}, {
        query: { method: 'GET', params: {}, isArray: true }
      }),
      users: $resource('http://kuterless.org.il/labs/coplay/api/users/', {}, {
        query: { method: 'GET', params: {}, isArray: true }
      }),

      users2: $resource('http://kuterless.org.il/labs/coplay/api/users/', {}, {
        query: { method: 'POST', params: {}, isArray: true }
      }),


      /*users: $resource('http://kuterless.org.il/labs/coplay/api/users/', {}, {
        query: { method: 'GET', params: {phoneId:'phone'}, isArray: true }
      }),*/
	    discussion_whole: $resource('http://kuterless.org.il/labs/coplay/api/discussion_whole/:phoneId'),
	    //discussion_whole: $resource('http://kuterless.org.il/labs/coplay/api/discussion_whole/:phoneId')
	    //$resource('http://example.com/:id.json')
      // post
      create_task: $resource('http://kuterless.org.il/labs/coplay/api/create_task/:phoneId')

      };
  }]);


// http://kuterless.org.il/labs/coplay/api/create_discussion/

// http://kuterless.org.il/labs/coplay/api/create_task/:

//	  dw: $resource('http://kuterless.org.il/labs/coplay/api/discussion_whole/:phoneId')
//	discussion_whole.feedback_set.id

// http://wsf.cdyne.com/WeatherWS/Weather.asmx/GetCityWeatherByZIP?ZIP=01901
