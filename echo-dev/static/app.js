(function(){
    var clean = false;
    var app = angular.module('developmentApp', []);

    app.controller('DevController', ['$scope', function($scope){
        var oldResponse = document.getElementById('oldResponse').value;
        $scope.newResponse = oldResponse;
    }]);

    app.directive('json', function(){
        return {
            restrict: 'E',
            templateUrl: '/static/json.html',
            controller: 'DevController',
        };
    });

    app.filter('dictionaryFilter', function(){
        return function(text){
           if(typeof(text) !== typeof('string')) {
               return '';
           }
           try {
               response = JSON.parse(text);
           } catch (err){
               clean = false;
               return 'INVALID FORMAT: ' + err.message;
           }
           clean = true;

           return response;

        }
    });

    document.addEventListener("submit", function(event){
        console.log('fire');
        if(!clean){ 
            alert('Invalid format check syntax');
            event.preventDefault();
        }
    });

})();

console.log(JSON.parse('{"foo": 1}'));
