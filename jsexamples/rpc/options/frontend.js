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

   function on_event(val) {
      console.log("Someone requested to square non-positive:", val);
   }

   session.subscribe('examples.rpc.options.square_on_nonpositive', on_event);

   var dl = [];

   var vals = [2, 0, -2];
   for (var i = 0; i < vals.length; ++i) {

      dl.push(session.call('examples.rpc.options.square', [vals[i]], {}, {}).then(
         function (res) {
            console.log("Squared", res);
         },
         function (error) {
            console.log("Call failed:", error);
         }
      ));
   }

   when.all(dl).then(
      function () {
         console.log("All finished.");
      },
      function () {
         console.log("Error", arguments);
      });
};

connection.open();