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

   var runs = 0;

   function test() {

      var received = 0;
      var sub = null;

      function on_event(args) {
         console.log("Got event", args[0]);
         received += 1;
         if (received > 5) {
            runs += 1;
            if (runs > 1) {
               console.log("Closing ..");
               connection.close();
            } else {
               sub.unsubscribe();
               console.log("Unsubscribed .. continue in 2s ..");
               setTimeout(test, 2000);
            }
         }
      }

      session.subscribe('examples.pubsub.unsubscribe.topic1', on_event).then(
         function (subscription) {
            sub = subscription;
            console.log("Subscribed with subscription ID " + subscription.id);
         }
      );
   }

   test();
};

connection.open();