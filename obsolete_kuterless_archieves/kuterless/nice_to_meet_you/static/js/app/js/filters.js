'use strict';

/* Filters */

angular.module('kuterlessFilters', []).filter('checkmark', function() {

  return function(input) {
    return input ? '\u2713' : '\u2718';
  };
//$filter('date')(date, medium, timezone)


});


