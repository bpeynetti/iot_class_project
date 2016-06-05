
var FirebaseRef = new Firebase("https://seat-occupancy.firebaseio.com/");
var seat1Ref = FirebaseRef.child('seat_1');
var intervalRef = seat1Ref.child('intervals');
var transitionRef = seat1Ref.child('transitions');


var num_transition = $('#number_readings_transition');
var num_interval = $('#number_readings_interval');
var state_transition = $('#state_transition');
var state_interval = $('#state_interval');


intervalRef.on('value',function(snapshot){

  var data = snapshot.val();
  console.log(data);
  num_interval.text(data.length-1);
  state_interval.text(data[data.length-1].state);

});


transitionRef.on('value',function(snapshot){

  var data = snapshot.val();
  num_transition.text(data.length-1);
  state_transition.text(data[data.length-1].state);

});
