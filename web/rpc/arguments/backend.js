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

   function ping() {
   }

   function add2(args) {
      return args[0] + args[1];
   }

   function stars(args, kwargs) {
      kwargs = kwargs || {};
      kwargs.nick = kwargs.nick || "somebody";
      kwargs.stars = kwargs.stars || 0;
      return kwargs.nick + " starred " + kwargs.stars + "x";
   }

   var _orders = [];
   for (var i = 0; i < 50; ++i) _orders.push(i);

   function orders(args, kwargs) {
      kwargs = kwargs || {};
      kwargs.limit = kwargs.limit || 5;
      return _orders.slice(0, kwargs.limit);
   }

   function arglen(args, kwargs) {
      args = args || [];
      kwargs = kwargs || {};
      return [args.length, Object.keys(kwargs).length];
   }

   var dl = [];

   dl.push(session.register('examples.rpc.arguments.ping', ping));
   dl.push(session.register('examples.rpc.arguments.add2', add2));
   dl.push(session.register('examples.rpc.arguments.stars', stars));
   dl.push(session.register('examples.rpc.arguments.orders', orders));
   dl.push(session.register('examples.rpc.arguments.arglen', arglen));

   when.all(dl).then(
      function () {
         console.log("All registered.");
      },
      function () {
         console.log("Registration failed!", arguments);
      });  
};

connection.open();