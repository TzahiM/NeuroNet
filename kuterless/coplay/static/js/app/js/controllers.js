'use strict';

/* Controllers */
/* Controllers: / DiscussionListCtrl / DiscussionDetailCtrl / userAreaCtrl / createCtrl / loginCtrl */

/* var App =  App.controller */
var kuterlessControllers = angular.module('kuterlessControllers', []);

//kuterlessControllers.controller('PhoneListCtrl', ['$rootScope', '$stream=Phone',

kuterlessControllers.controller('DiscussionListCtrl', ['$scope', '$stream',
  function($scope, $stream) {

            window.$scope = $scope; // debug

    //todo-array-$scope.obj = Flow.discussions.query();
    $scope.discussions = $stream.discussions.query();
    $scope.orderProp = 'id';

// $scope.shipmentMethod = ((default_shipment_method || []).length > 0) ? default_shipment_method[0].type : $scope.alldeliveries;


    for(var i = 1; i < 333; i++){
       console.log($scope.discussions[i]);
    }
  }]);


//kuterlessControllers.controller('PhoneDetailCtrl', ['$scope', '$routeParams', '$stream=Phone',
kuterlessControllers.controller('DiscussionDetailCtrl', ['$scope', '$routeParams', '$stream',
  function($scope, $routeParams, $stream) {

            window.$routeParams = $routeParams; // debug
            window.$scope = $scope; // debug

    //$scope.feedbacks = $stream.feedbacks.query();
    //$scope.discussions = $stream.discussions.query();
    //$scope.discussion_whole = $stream.discussion_whole.query();
    //$scope.phone = $stream.discussion_whole.query(); // becuse per id


    $scope.users = $stream.users.query();
    $scope.discussion_whole = $stream.discussion_whole.get({phoneId: $routeParams.phoneId});
//http://www.sitepoint.com/creating-crud-app-minutes-angulars-resource/
//http://stackoverflow.com/questions/23578951/angularjs-push-item-does-not-work
//$scope.nameo.$save({ id: "yet_another_noteId" });

    $scope.doAuthorizeClaim = function() {
      $scope.discussion_whole.task_set.save($scope.test, function() {
        alert('Authorize claim saved');
      });
    };

    //$scope.discussion_whole = $stream.discussion_whole.save({ ida: "yet_another_noteId" });
    //$scope.discussion_whole = $stream.discussion_whole.feedback_set.save({ idA: "yet_another_noteId" });

//$scope.discussion_whole.task_set
//goal_description:
//target_date:







var myApp = angular.module('myApp', ['ngResource', 'myAppServices']);

myApp.controller('AuthorizeController', ['$scope', 'Authorize',
  function($scope, Authorize) {

    $scope.doAuthorizeClaim = function() {
      $scope.discussion_whole.task_set.save($scope.authorizeClaim, function() {
        alert('Authorize claim saved');
      });
    };
  }
]);

var myAppServices = angular.module('myAppServices', ['ngResource']);

myAppServices.factory('Authorize', ['$resource',
  function($resource) {
    return $resource('/api/authClaims', {}, {});
  }
]);









    $scope.create_task = function (){

        //if($scope.create_task){}
          //$scope.discussion_whole.feedback_set.push({});
          $scope.discussion_whole.feedback_set.push({
              test: $scope.nameo

          });
          // return scope.user.push()
    }


// add to model
function parseData() {

    var usersObj = {};
    
    angular.forEach($scope.users, function (user) {
        usersObj[user.id] = user;
    });

    console.log(usersObj);

    angular.forEach($scope.discussion_whole.feedback_set, function (feedback) {
        feedback.userObject = usersObj[feedback.user];
    });
}




    $scope.discussion_whole.$promise.then(function (data) {
        console.log('discussion_whole data -> ', data);

          $scope.users.$promise.then(function (data) {
              console.log('users data -> ', data);

              parseData();
          });

    });


        $scope.get_user = function (id) {
            if ($scope.users) {
                for (var index = 0; index < $scope.users.length; index++) {
                    if ($scope.users[index].id == id){
                      console.log($scope.users[index]);
                      //console.log($scope.feedback_set.user[index]);
                      return $scope.users[index];

                    }
                }
            }
            return null;
        };



/*
    $scope.setImage = function(imageUrl) {
      $scope.mainImageUrl = imageUrl;
    };*/
    $scope.setId = function(id) {
      $scope.mainImageUrl = id;
    };
  }]);
