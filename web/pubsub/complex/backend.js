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

function randint(min, max) {
  return Math.floor(Math.random() * (max - min + 1) + min);
}

connection.onopen = function (session) {

   var counter = 0;

   setInterval(function () {
      session.publish('examples.pubsub.complex.heartbeat');

      var obj = {'counter': counter, 'foo': [1, 2, 3]};
      session.publish('examples.pubsub.complex.topic2', [randint(0, 100), 23], {c: "Hello", d: obj});

      counter += 1;

      console.log("events published");
   }, 1000);
};

connection.open();