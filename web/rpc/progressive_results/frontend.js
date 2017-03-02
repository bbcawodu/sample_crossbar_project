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

   session.call('examples.rpc.progressive_results.longop', [3], {}, {receive_progress: true}).then(
      function (res) {
         console.log("Final:", res);
         connection.close();
      },
      function (err) {
      },
      function (progress) {
         console.log("Progress:", progress);
      }
   );
};

connection.open();