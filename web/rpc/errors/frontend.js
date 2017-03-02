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

   dl = [];

   var vals1 = [2, 0, -2];
   for (var i = 0; i < vals1.length; ++i) {

      dl.push(session.call('examples.rpc_protocol.errors.sqrt', [vals1[i]]).then(
         function (res) {
            console.log("Result:", res);
         },
         function (err) {
            console.log("Error:", err.error, err.args, err.kwargs);
         }
      ));
   }

   when.all(dl).then(function () {
      console.log("All finished.");
      connection.close();
   });
};

connection.open();