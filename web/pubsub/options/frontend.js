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
   realm: 'example_realm'}
);

connection.onopen = function (session) {

   var received = 0;

   function on_event(args, kwargs, details) {

      console.log("Got event, publication ID " +
                  details.publication + ", publisher " +
                  details.publisher + ": " + args[0]);

      received += 1;
      if (received > 5) {
         console.log("Closing ..");
         connection.close();
      }
   }

   session.subscribe('examples.pubsub.options.topic1', on_event);
};

connection.open();