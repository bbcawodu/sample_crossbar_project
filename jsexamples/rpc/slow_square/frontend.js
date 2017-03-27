try {
   var autobahn = require('autobahn');
   var when = require('when');
   var now = require("performance-now");
} catch (e) {
   // when running in browser, AutobahnJS will
   // be included without a module system
   var when = autobahn.when;
   var now = function () { return performance.now() };
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

   var dl = [];

   var t1 = now();
   dl.push(session.call('examples.rpc.slow-square.slowsquare', [3]).then(
      function (res) {
         var duration = now() - t1;
         console.log("Slow Square:", res, duration);
      }
   ));

   var t2 = now();
   dl.push(session.call('examples.rpc.slow-square.square', [3]).then(
      function (res) {
         var duration = now() - t2;
         console.log("Quick Square:", res, duration);
      }
   ));

   when.all(dl).then(function () {
      console.log("All finished.");
      connection.close();
   });
};

connection.open();