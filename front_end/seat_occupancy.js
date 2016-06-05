
var FirebaseRef = new Firebase("https://seat-occupancy.firebaseio.com/");
var seat1Ref = FirebaseRef.child('seat_4');
var intervalRef = seat1Ref.child('intervals');
var transitionRef = seat1Ref.child('transitions');


var num_transition = $('#number_readings_transition');
var num_interval = $('#number_readings_interval');
var state_transition = $('#state_transition');
var state_interval = $('#state_interval');

var intervalGraph = $('#interval_graph');
var transitionGraph = $('#transition_graph');


// STATE: 2 = empty, 3 = occupied
// function initializeGraph(graph_obj,type){
//
//
//
// }
// updateGraph()

intervalRef.on('value',function(snapshot){

  var userid = 0;
  var data = snapshot.val(); // in object form
  if(!data) {
     return;
   }
  console.log(data);
  var data_array = []
  snapshot.forEach(function(childSnap){
    data_array.push(childSnap.val());
  })
  data = data_array;
  console.log(data)
  num_interval.text(data.length);

  last_state = data[data.length-1].state;
  if (last_state<=1 | last_state==="empty")
  {
    addEvent(0,2);
    chair = 'empty'
  }
  else
  {
    addEvent(0,3);
    chair = 'occupied'
  }
  state_interval.text(chair);

});


transitionRef.on('value',function(snapshot){

  var data = snapshot.val();
  if(!data){
     return;
   }
  var data_array = []
  snapshot.forEach(function(childSnap){
    data_array.push(childSnap.val());
  })
  data = data_array;
  num_transition.text(data.length);

  last_state = data[data.length-1].state;
  if (last_state<=1 | last_state==="empty")
  {
    addEvent(1,2);
    chair = 'empty'
  }
  else
  {
    addEvent(1,3);
    chair = 'occupied'
  }
  state_transition.text(chair);

});


//////////////////////////////////////////////////
//DISCRETE CUBISM.JS
//////////////////////////////////////////////////
//This is a version of cubism.js written by Patrick Thompson
//to use cubism tracking for discrete events
//that occur in real time
////////////////////////////////////////////////////
//Cubism is a library written by Mike Bostock
//For more information about cubism go to
//https://square.github.io/cubism/
//////////////////////////////////////////////////
//(Note:this is written in the user/event paradigm)
//but can be translated into any system that has discrete events
//////////////////////////////////////////////////
//TODO
//1. Add block colors (I do not fully understand how to add colors to cubism.js yet)
//2. Add a line above the first user (just haven't gotten around to it yet
//3. Add "delete user" and "delete event" input (not really necessary to demonstrate)

var AllUsers = []; //Create an array that will contain all users

var Users = [{ //Create the first template user
    name: "Interval Graph",
    event: 1,
    newevent: false
},
{ //Create the first template user
    name: "Transition Graph",
    event: 1,
    newevent: false
}];
var events = [{ //Create the New event notification
    name: "New Event!",
    value: "20"
}]
events.push({ //Create the default event notification
    name: "No Events",
    value: "0.0"
});
events.push({ //Create a couple of events
    name: "Empty",
    value: "5.0"
});
events.push({ //Create a couple of events
    name: "Occupied",
    value: "-5.0"
});



//////////////////////////////////////////////////
//BEGIN CUBISM FUNCTIONS /////////////////////////
//////////////////////////////////////////////////


//////////////////////////////////////////////////
//Add the cubism context /////////////////////////
//Required for cubism to work ////////////////////
//////////////////////////////////////////////////

var context = cubism.context() // set the cubism context
.serverDelay(0) // No server delay
.clientDelay(0) // No client delay
.step(2.5e2) // step once every second
.size(1000); // and make the horizon div 960 px wide.

//////////////////////////////////////////////////
//Execute when AddNewEvent button pressed ////////
//Adds a new event to the event list /////////////
//////////////////////////////////////////////////

d3.select("#example1").call(function (div) {

    AddAllUsers();

    div.append("div")
        .attr("class", "axis")
        .call(context.axis().orient("top"));

    RunData();

    div.append("div")
        .attr("class", "rule")
        .call(context.rule());

    RefreshUsers();
    RefreshEvents();
    RefreshRule();

});

//////////////////////////////////////////////////
//Execute when AddAllUsers button pressed ////////
//Adds a new user to the AllUsers list /////////////
//////////////////////////////////////////////////

function AddAllUsers() {
    for (var i = 0; i < Users.length; i++) {
        var myuser = random(Users[i].name);
        AllUsers.push(myuser);
    }
}

//////////////////////////////////////////////////
//Execute RunData function ////////
//Adds all horizons to cubism div /////////////
//////////////////////////////////////////////////

function RunData() {
    d3.select("#example1").selectAll(".horizon")
        .data(AllUsers)
    .enter().append("div")
        .attr("class", "horizon")
        .call(context.horizon().extent([-20, 20]));
}



/////////////////////////////////////////////////////////////////////
//Execute the running process (heart of the code)////////////////////
//This is also executed each time a user is added////////////////////
/////////////////////////////////////////////////////////////////////
function random(name) {
    var value = 0,
        values = [],
        area = [],
        i = 0,
        last;
    return context.metric(function (start, stop, step, callback) {
        start = +start, stop = +stop;
        if (isNaN(last)) last = start;
        // console.log(step);
        // console.log(name);
        // console.log(values);
        while (last < stop) {
            last += step;
            // console.log(last);
            for (var j = 0; j < Users.length; j++) { //For all users
                if (Users[j].name == name) { //If the user name in the loop matches the current user name
                    if (Users[j].newevent) { //If the user has a new event
                        value = parseInt(events[0].value); //Show a "blip" in event zero
                        Users[j].newevent = false; //And switch newevent OFF
                    } else { //Otherwise
                        value = parseFloat(events[Users[j].event].value); //Write the value of the current user
                    }
                    values.push(value); //And add it to the values array
                }
            }
        }
        // console.log(values);
        callback(null, values = values.slice((start - stop) / step)); //And execute the callback function
    }, name);
}

//////////////////////////////////////////////////
//Execute when AddNewEvent button pressed ////////
//Adds a new event to the event list /////////////
//////////////////////////////////////////////////

function UpdateRule(i) {
    d3.selectAll(".value").each(function (index, d, k) {
        for (l = 0; l < events.length; l++) {
            //console.log($(this).text().replace("−", "-"));
            if ($(this).text().replace("−", "-") == events[l].value) {
                $(this).text(events[l].name);
            }
        }
    }).style("right", i == null ? null : context.size() - i + 10 + "px");
}

//////////////////////////////////////////////////
//BEGIN INPUT FUNCTIONS ////////
//////////////////////////////////////////////////

//////////////////////////////////////////////////
//Execute when AddNewEvent button pressed ////////
//Adds a new event to the event list /////////////
//////////////////////////////////////////////////

function addNewEvent() {
    var prefixstring = "";
    var suffixstring = "";
    if (events.length + 4 < 10) {
        suffixstring = ".0"
    }
    if (events.length % 2 == 0) {
        prefixstring = "-"
    }
    events.push({
        name: $("#NewEventName").val(),
        value: prefixstring + (events.length + 4).toString() + suffixstring
    });
    $(NewEventName).val('');
    RefreshEvents();
};

/////////////////////////////////////////////////////////////////////
//Execute when AddEvent button pressed //////////////////////////////
//Adds event to the selected user //////////////////////////////////
/////////////////////////////////////////////////////////////////////

function addEvent(id,state) {
    Users[id].newevent = true;
    Users[id].event = state;
}

//////////////////////////////////////////////////
//Execute when AddUser button pressed ////////
//Adds a new user to the user list /////////////
//////////////////////////////////////////////////

function addUser() { //Add a user function (executed by pressing add user button)
    totalusers = Users.length + 1; //a variable for total users
    Users.push({ //add a user to the users object
        name: $("#UserName").val(), //name equals username text field value
        event: 1, //default event of 1
        newevent: false //the event for this user has not been created yet, so keep the newevent false
    });
    $("#UserName").val(''); //clear the username field
    RefreshUsers(); //execute the refreshusers function
    myuser = random(Users[totalusers - 1].name); //

    AllUsers.push(myuser); //push the user onto the AllUsers array of users
    RunData();        //Run the data with the new user
    RefreshRule();    //Refresh the rule for all users (will not refresh new user rule if not invoked)
}

//////////////////////////////////////////////////
//BEGIN SELECT OPTION UPDATE FUNCTIONS ////////
//////////////////////////////////////////////////

//////////////////////////////////////////////////
//Execute RefreshUsers function ////////
//Clears and populates the user select option list /////////////
//////////////////////////////////////////////////

function RefreshUsers() {
    $('#UserList')
        .find('option')
        .remove();
    for (i = 0; i < Users.length; i++) {
        $('#UserList').append('<option value="' + i + '">' + Users[i].name + '</option>');
    }
};

//////////////////////////////////////////////////
//Execute the RefreshEvents function ////////
//Clears and populates the event select option list /////////////
//////////////////////////////////////////////////

function RefreshEvents() {
    $('#EventList')
        .find('option')
        .remove();
    for (i = 2; i < events.length; i++) {
        $('#EventList').append('<option value="' + i + '">' + events[i].name + '</option>');
    }
};
//////////////////////////////////////////////////
//Execute the RefreshRule function ////////
//Refreshes the horizontal rule on mouse context focus
//////////////////////////////////////////////////

function RefreshRule() {
    // On mousemove, reposition the chart values to match the rule.
    context.on("focus", function (i) {
        UpdateRule(i)
    });
}
