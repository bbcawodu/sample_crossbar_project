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

var connection = new autobahn.Connection({
   url: wsuri,
   realm: 'realm1'}
);

connection.onopen = function (session) {

   var counter = 0;

   setInterval(function () {
      session.publish('com.unsubscribe-pubsub-example.topic1', [counter]);
      counter += 1;
      console.log("events published");
   }, 1000);
};

connection.open();