'use strict';

/* App Module */
/* nameing convention kutterless */

var App = angular.module('kuterlessApp', [
/*
  'ngRoute',
  'phonecatAnimations',
  'phonecatControllers',
  'phonecatFilters',
  'phonecatServices'
*/
  'ngRoute',
  /*'kuterlessAnimations',*/
  'kuterlessControllers',
  'kuterlessFilters',
  'kuterlessServices'
]);

// http://stackoverflow.com/questions/29547003/angularjs-no-access-control-allow-origin-header-is-present-on-the-requested-r

// /login

App.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
    // when('/phones', {
    // when('/discussions', {

      when('/discussions', {
        templateUrl: 'partials/phone-list.html',
        controller: 'DiscussionListCtrl'
      }).
      when('/discussions/:phoneId', {
        templateUrl: 'partials/phone-detail.html',
        controller: 'DiscussionDetailCtrl'
      }).
      otherwise({
        redirectTo: '/discussions'
      });
  }]);
