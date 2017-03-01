# The bulk of this README is taken from: (http://autobahn.ws/python/wamp/examples.html)

Overview of Examples

The examples are organized between asyncio and Twisted at the top-level, with similarly-named examples demonstrating the same functionality with the respective framework.

Each example typically includes four things:
(LOCATED IN EXAMPLES PACKAGE)
frontend.py: the Caller or Subscriber, in Python
backend.py: the Callee or Publisher, in Python

(LOCATED IN CORRESPONDING WEB DIRECTORY)
frontend.js: JavaScript version of the frontend
backend.js: JavaScript version of the backend
*.html: boilerplate so a browser can run the JavaScript

So for each example, you start one backend and one frontend component (your choice). You can usually start multiple frontend components with no problem, but will get errors if you start two backends trying to register at the same procedure URI (for example).

Still, you are encouraged to try playing with mixing and matching the frontend and backend components, starting multiple front-ends, etc. to explore Crossbar and Autobahn’s behavior. Often the different examples use similar URIs for procedures and published events, so you can even try mixing between the examples.

The provided Crossbar.io configuration will run a Web server that you can visit at http://localhost:8080 and includes links to the frontend/backend HTML for the javascript versions. Usually these just use console.log() so you’ll have to open up the JavaScript console in your browser to see it working.

# How to run

In the configuration of the crossbar router that I have set up, all of the example backends are already running on worker components attached to crossbar so you dont need to explicitly worry about starting up the backends once you start crossbar. You can play around with removing some and starting them up manually with python or javascript by visiting the corresponding backend.html file in the browser either from the local url or the file system. 

If all that is too many options to consider, you want to do this:

1) Open 2 terminals
2) In terminal 1, setup and run a local Crossbar in the root of your Autobahn checkout.
3) In terminal 2, go to the root of your Autobahn checkout and activate the virtualenv from step 2 (source venv-autobahn/bin/activate)
4) In terminal 2 run python ./examples/rpc_protocol/arguments/frontend.py OR go to localhost:<port_number>/rpc_protocol/arguments/frontend.html