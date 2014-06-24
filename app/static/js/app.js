

$(document).ready(function () {


        var filename = $("#file").val();

        $("#file").change(function(){
         $('#myForm').submit();
        });
        $('#myForm').ajaxForm(function(data){
        window.location.reload()
        });

});


betsapp = angular.module('bets',[])

betsapp.config(
function($interpolateProvider) {
$interpolateProvider.startSymbol('||');
$interpolateProvider.endSymbol('||');
}
);

// --- Main App Controller //


betsapp.controller('testCtrl',function($scope,$http){

$('[data-toggle="tooltip"]').tooltip({'placement': 'bottom'});
$scope.allMatches=[];
$scope.loadMatches=function(){


var mtchs = $http.get("/matches");

mtchs.success(function(data, status, headers, config) {

$.each(data, function(index,jsonObject){
   $scope.allMatches.push(jsonObject);
});

});

mtchs.error(function(data, status, headers, config) {
   $("#error").html(data+"hmmn");
    alert("AJAX failed!" + status);
});

}

$scope.loadMatches();





$scope.beton=function(m,mid,tname,id){


var bet = $http.get("/beton/"+mid+"/"+tname);

bet.success(function(data, status, headers, config) {
if(data == "suc"){
m.beton = id
}
else{
alert("Failed: Please refresh page and try again");
}
});

bet.error(function(data, status, headers, config) {
   $("#error").html(data+"hmmn");
    alert("AJAX failed!" + data);
});

}

$scope.togbox=function(id){

$('#'+id+"box").toggle(400);
};

});




//--LeaderboardCtrl //

betsapp.controller('leaderCtrl',function($scope,$http){

$scope.leaders=[]
$scope.loadLeaderBoard=function(){
var lb = $http.get("/getleaderboard");

lb.success(function(data, status, headers, config) {

$.each(data, function(index,jsonObject){
   $scope.leaders.push(jsonObject);
});

});

lb.error(function(data, status, headers, config) {
   $("#error").html(data+"hmmn");
    alert("AJAX failed!" + data);
});

};
$scope.loadLeaderBoard();

});



//--- LoginCtrl //

betsapp.controller('loginCtrl',function($scope,$http){
$scope.loginUser=function(){


var l = $http.get("/loginu/"+$('#login-uname').val()+"/"+$('#login-pwd').val());

l.success(function(data, status, headers, config) {
    if(data=="success")
    window.location.replace("/app");
    else
    alert(data);
});
l.error(function(data, status, headers, config) {
$("#error").html(data);
    alert("AJAX failed!" + data);
});

};


$scope.regUser=function(){


var name=$('#reg-name').val();
var uname=$('#reg-uname').val();
var pwd=$('#reg-pwd').val();

var reg =$http.get("/register/"+name+"/"+uname+"/"+pwd);

reg.success(function(data, status, headers, config){
alert(data)
});

reg.error(function(data, status, headers, config){
alert(data);
$("#error").html(data);
});
};




});

//--- AdminCtrl //

betsapp.controller('adminCtrl',function($scope,$http){
$scope.allMatches=[];
$scope.loadMatches=function(){

var mtchs = $http.get("/adminmatches");

mtchs.success(function(data, status, headers, config) {

$.each(data, function(index,jsonObject){
   $scope.allMatches.push(jsonObject);
});

});

mtchs.error(function(data, status, headers, config) {
   $("#error").html(data+"hmmn");
    alert("AJAX failed!" + status);
});

}

$scope.loadMatches();

$scope.setWinner=function(m,t){

var setWin = $http.get("/setWinner/"+m.mid+"/"+t.id);

setWin.success(function(data, status, headers, config) {
m.winner = t
});

setWin.error(function(data, status, headers, config) {
    alert("AJAX failed!" + data);
    $("#error").html(data);
});
}

});

//--- matchCtrl --//

betsapp.controller('matchCtrl',function($scope,$http){

$scope.team1 = "";
$scope.team2 = "";
$scope.bets = "";
$scope.getMatchDetails=function(){

var match = $http.get("/getMatchDetails/"+$("#mid").val());

match.success(function(data, status, headers, config) {
$scope.bets = data;
});

match.error(function(data, status, headers, config) {
    alert("AJAX failed!" + data);
    $("#error").html(data);
});

};

$scope.getMatchDetails();

});


//--- userMatchCtrl --//

betsapp.controller('userCtrl',function($scope,$http){

$scope.team1 = "";
$scope.team2 = "";
$scope.user = "";
$scope.getUserMatchDetails=function(){

var match = $http.get("/getUserMatchDetails/"+$("#uid").val());

match.success(function(data, status, headers, config) {
$scope.user=data
});

match.error(function(data, status, headers, config) {
    alert("AJAX failed!" + data);
    $("#error").html(data);
});

};

$scope.getUserMatchDetails();

});


//--- profileCtrl --//

betsapp.controller('profileCtrl',function($scope,$http){


$scope.getUserDetails=function(){

var user = $http.get("/getUserDetails/"+$("#uid").val());
$scope.userd="";
user.success(function(data, status, headers, config) {
$scope.userd=data
});

user.error(function(data, status, headers, config) {
    alert("AJAX failed!" + data);
    $("#error").html(data);
});

};

$scope.getUserDetails();


$scope.team1 = "";
$scope.team2 = "";
$scope.userm = "";
$scope.getUserMatchDetails=function(){

var match = $http.get("/getUserMatchDetails/"+$("#uid").val());

match.success(function(data, status, headers, config) {
$scope.userm=data
});

match.error(function(data, status, headers, config) {
    alert("AJAX failed!" + data);
    $("#error").html(data);
});

};

$scope.getUserMatchDetails();

});



// --- ResultCtrl --- //

betsapp.controller('resultCtrl',function($scope,$http){


$scope.allMatches=[];
$scope.loadMatches=function(){


var mtchs = $http.get("/matches");

mtchs.success(function(data, status, headers, config) {

$.each(data, function(index,jsonObject){
   $scope.allMatches.push(jsonObject);
});

});

mtchs.error(function(data, status, headers, config) {
   $("#error").html(data+"hmmn");
    alert("AJAX failed!" + status);
});

}

$scope.loadMatches();


});