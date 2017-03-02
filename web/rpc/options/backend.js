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

   function square(args, kwargs, details) {
      console.log("Someone is calling me;)", details);

      var val = args[0];
      if (val < 0) {
         session.publish('examples.rpc.options.square_on_nonpositive', [val]);
      } else if (val === 0) {
         var options = {};
         if (details && details.caller) {
            options = {exclude: [details.caller]};
         }
         session.publish('examples.rpc.options.square_on_nonpositive', [val], {}, options);
      }
      return args[0] * args[0]
   }

   session.register('examples.rpc.options.square', square).then(
      function (registration) {
         console.log("Procedure registered:", registration.id);
      },
      function (error) {
         console.log("Registration failed:", error);
      }
   );
};

connection.open();