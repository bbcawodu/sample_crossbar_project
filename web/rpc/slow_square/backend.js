try {
   var autobahn = require('autobahn');
   var when = require('when');
} catch (e) {
   // when running in browser, AutobahnJS will
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
   realm: 'realm1'}
);

connection.onopen = function (session) {

   // a "fast" function or a function that returns
   // a direct value (not a promise)
   function square(x) {
      return x * x;
   }

   session.register('com.examples.rpc.slow-square.square', square);


   // simulates a "slow" function or a function that
   // returns a promise
   function slowsquare(x) {

      // create a deferred
      var d = when.defer();

      // resolve the promise after 1s
      setTimeout(function () {
         d.resolve(x * x);
      }, 1000);

      // need to return the promise
      return d.promise;
   }

   session.register('com.examples.rpc.slow-square.slowsquare', slowsquare).then(
      function (registration) {
         console.log("Procedure registered:", registration.id);
      },
      function (error) {
         console.log("Registration failed:", error);
      }
   );
};

connection.open();