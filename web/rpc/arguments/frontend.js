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
   realm: 'realm1'}
);

connection.onopen = function (session) {

   var dl = [];

   dl.push(session.call('com.examples.rpc.arguments.ping').then(
      function () {
         console.log("Pinged!");
      }
   ));

   dl.push(session.call('com.examples.rpc.arguments.add2', [2, 3]).then(
      function (res) {
         console.log("Add2:", res);
      }
   ));

   dl.push(session.call('com.examples.rpc.arguments.stars').then(
      function (res) {
         console.log("Starred 1:", res);
      }
   ));

   dl.push(session.call('com.examples.rpc.arguments.stars', [], {nick: 'Homer'}).then(
      function (res) {
         console.log("Starred 2:", res);
      }
   ));

   dl.push(session.call('com.examples.rpc.arguments.stars', [], {stars: 5}).then(
      function (res) {
         console.log("Starred 3:", res);
      }
   ));

   dl.push(session.call('com.examples.rpc.arguments.stars', [], {nick: 'Homer', stars: 5}).then(
      function (res) {
         console.log("Starred 4:", res);
      }
   ));

   dl.push(session.call('com.examples.rpc.arguments.orders', ['coffee']).then(
      function (res) {
         console.log("Orders 1:", res);
      }
   ));

   dl.push(session.call('com.examples.rpc.arguments.orders', ['coffee'], {limit: 10}).then(
      function (res) {
         console.log("Orders 2:", res);
      },
      function (err) {
         console.log(err);
      }
   ));

   dl.push(session.call('com.examples.rpc.arguments.arglen').then(
      function (res) {
         console.log("Arglen 1", res);
      }
   ));

   dl.push(session.call('com.examples.rpc.arguments.arglen', [1, 2, 3]).then(
      function (res) {
         console.log("Arglen 2", res);
      }
   ));

   dl.push(session.call('com.examples.rpc.arguments.arglen', [], {a: 1, b: 2, c: 3}).then(
      function (res) {
         console.log("Arglen 3", res);
      }
   ));

   dl.push(session.call('com.examples.rpc.arguments.arglen', [1, 2, 3], {a: 1, b: 2, c: 3}).then(
      function (res) {
         console.log("Arglen 4", res);
      }
   ));

   when.all(dl).then(function () {
      console.log("All finished.");
      connection.close();
   });
};

connection.open();