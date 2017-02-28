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

   function sqrt(args) {
      var x = args[0];
      if (x === 0) {
         throw "don't ask foolish questions;)";
      }
      var res = Math.sqrt(x);
      if (res !== res) {
         //throw "cannot take sqrt of negative";
         throw new autobahn.Error('com.examples.rpc_protocol.errors.error', ['fuck'], {a: 23, b: 9});
      }
      return res;
   }

   session.register('com.examples.rpc_protocol.errors.sqrt', sqrt).then(
      function (registration) {
         console.log("Procedure registered:", registration.id);
      },
      function (error) {
         console.log("Registration failed:", error);
      }
   );
};

connection.open();