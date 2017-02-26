try {
   var autobahn = require('autobahn');
} catch (e) {
   // when running in browser, AutobahnJS will
   // be included without a module system
}

// dynamic connection uri based on file location
var wsuri;
if (document.location.origin == "file://") {
   wsuri = "ws://127.0.0.1:8080/ws";

} else {
   wsuri = (document.location.protocol === "http:" ? "ws:" : "wss:") + "//" +
               document.location.host + "/ws";
}

// Connect to crossbar router component via WAMP protocol
var connection = new autobahn.Connection({
   url: wsuri,
   realm: 'realm1'}
);

connection.onopen = function (session) {

   function on_heartbeat(args, kwargs, details) {
      console.log("Got heartbeat (publication ID " + details.publication + ")");
   }

   session.subscribe('com.complex-pubsub-example.heartbeat', on_heartbeat);


   function on_topic2(args, kwargs) {
      console.log("Got event:", args, kwargs);
   }

   session.subscribe('com.complex-pubsub-example.topic2', on_topic2);


   setTimeout(function () {
      console.log("Closing ..");
      connection.close();
   }, 5000);
};

connection.open();