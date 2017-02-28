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

   function add_complex(args, kwargs) {
      console.log("Someone is calling me;)");
      return new autobahn.Result([], {c: args[0] + args[2], ci: args[1] + args[3]});
   }

   session.register('com.examples.rpc.complex_results.add_complex', add_complex).then(
      function (registration) {
         console.log("Procedure registered:", registration.id);
      },
      function (error) {
         console.log("Registration failed:", error);
      }
   );

   function split_name(args) {
      return new autobahn.Result(args[0].split(" "));
   }

   session.register('com.examples.rpc.complex_results.split_name', split_name).then(
      function (registration) {
         console.log("Procedure registered:", registration.id);
      },
      function (error) {
         console.log("Registration failed:", error);
      }
   );
};

connection.open();