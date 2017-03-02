try {
   var autobahn = require('autobahn');
   var when = require('when');
} catch (e) {
   // When running in browser, AutobahnJS will
   // be included without a module system
   var when = autobahn.when;
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

   // Application component that calls procedures which
   // produce complex results (call results with more than one
   // positional or keyword results) and showing how to access those.
   var dl = [];

   dl.push(session.call('examples.rpc.complex_result.add_complex', [2, 3, 4, 5]).then(
      function (res) {
         console.log("Result: " + res.kwargs.c + " + " + res.kwargs.ci + "i");
      }
   ));

   dl.push(session.call('examples.rpc.complex_result.split_name', ['Homer Simpson']).then(
      function (res) {
         console.log("Forename: " + res.args[0] + ", Surname: " + res.args[1]);
      }
   ));

   when.all(dl).then(function () {
      console.log("All finished.");
      connection.close();
   });
};

connection.open();