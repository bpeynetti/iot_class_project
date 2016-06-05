
var FirebaseRef = new Firebase("https://seat-occupancy.firebaseio.com/");
var intervalRef = FirebaseRef.child('intervals');
var transitionRef = FirebaseRef.child('transitions');


var num_transition = $('#number_readings_transition');
var num_interval = $('#number_readings_interval');
var state_transition = $('#state_transition');
var state_interval = $('#state_interval');


intervalRef.on('value',function(snapshot){

  var data = snapshot.val();
  console.log(data);
  num_interval.text(data.length);
  state_interval.text(data[data.length-1].state);

});


transitionRef.on('value',function(snapshot){

  var data = snapshot.val();
  num_transition.text(data.length);
  state_transition.text(data[data.length-1].state);

});
