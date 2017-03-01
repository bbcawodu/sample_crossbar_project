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

console.log(wsuri);

connection.onopen = function (session) {

   var received = 0;

   function onevent1(args) {
      console.log("Got event:", args[0]);
      received += 1;
      if (received > 5) {
         console.log("Closing ..");
         connection.close();
      }
   }

   session.subscribe('examples.pubsub.basic.topic1', onevent1);
};

connection.open();