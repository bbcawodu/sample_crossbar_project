From: http://crossbar.io/docs/Setup-on-Heroku/

Setup on Heroku

Heroku is a Platform-as-a-Service cloud vendor that allows to run applications in so-called Dynos, which are like glorified OS containers.

Application Setup¶

Crossbar.io can be run on Heroku. Here we describe what you need to do. This walkthrough assumes that you have created an account on Heroku and have installed the Heroku tool belt.

To sign up for a free Heroku account go here.

Once you've created an account install the Heroku toolbelt. You can find the tool belt here.

Heroku also has very thorough walkthroughs for creating apps using a variety of languages.

Installing a Crossbar.io project on Heroku is pretty straightforward once you're familiar with the above but here is a step by step guide in case you need some extra guidance.

```
Create project folder
Create virtual environment (Optional but strongly recommended): You can find out more about virtual environments here to create a virtual environment:
Install virtual env: If you haven't already, install virtualenv through pip: pip install virtualenv
Go to your project: Open a terminal window and navigate to your project folder: cd my_project
Create the virtual environment: virtualenv venv
    - If you have both python 2 and 3 installed, you can specify the version like the following:
        - virtualenv -p /usr/bin/python2.7 <virtual environment name(venv)>
Activate the virtual environment: source venv/bin/activate
Install Crossbar: pip install crossbar
Create project (hello:python template): crossbar init --template hello:python
Freeze requirements: Create a requirements file so that Heroku knows what to install for your project: pip freeze > requirements.txt
Create Procfile: Heroku uses a Procfile to determine what commands to use to start your app: echo "web: crossbar start" > Procfile
Modify Config file: Heroku uses a dynamic urls and ports so you'll need to use config file like the one described in the Crossbar.io configuration below (or copy the one below). You can find your config file in the .crossbar directory of your project folder (assuming you followed the steps above)
Create git repo: You deploy to Heroku via Git. If you don't have Git installed you can find out how to do so here. To create a git repository:
cd my_project_path
git init
git add .
git commit -m "Initial commit"
Create the app on Heroku: Now you should be all set to create an instance of the app: heroku create (NOTE: check the output of this command, on the second line it will tell you the URL of your app - it should be something like random-heroku-assigned-name.herokuapp.com. You can also find it through your account page on Heroku)
Deploy: to deploy and start the app you push it using Git and Heroku should take care of the rest: git push heroku master
You can check the logs of your application once it's deployed by using the logs command: heroku logs --tail
Point your browser to the address that Heroku assigned to your app and you should see the Hello WAMP! page (see the hello:python template for more information). (NOTE: Use http instead of https to access the page.)
Crossbar.io configuration¶
```

Crossbar.io can create a complete node configuration and "Hello, world". Here is how you would create a Python based "Hello, world" application:

crossbar init --template hello:python
The configuration generated will make Crossbar.io listen on the fixed port 8080 for incoming Web and WebSocket connections.

However, Heroku does not allow to expose fixed ports from Dynos to the outside world, but routes HTTP (and WebSocket) request coming in from the Internet via a Heroku frontend load-balancer to Dynos - to a dynamically assigned port. Read more here.

When a Dyno starts, the Dyno will get assigned an externally visible port, and inside the Dyno, the environment variable PORT will allow you to access the assigned port number.

Because of this, we need to modify the Crossbar.io node configuration:

In the Web transport, insted of 8080, we configure the value "$PORT". This will make Crossbar.io read the value dynamically upon startup from the environment variable.
Since the main transport is now listening on a dynamic port, we start a second (WebSocket) transport on our router on fixed port 9000 for the container worker to connect to
    
    - In order to run your crossbar project locally, you need to set the PORT environment variable. There are several approaches
      towards accomplishing this, I will outline 2 below
      - (PREFERRED METHOD) Configure virtual environment activate script to set and unset the PORT environment variable on
        activation and deactivation respectively
        - open venv/bin/activate
        - Add the folllowing the the end of the script:
            - export PORT='9000'
                -This sets the PORT environment variable when the virtual environment activates
        - Add the following at the end of the deactivate () {} function
            - unset PORT
                - This unsets the PORT environment variable when the virtual environment is deactivated
     - Second method is outlined in the NOTES section
Here is a complete, working configuration:
(This config is outdated. Uses version 1 when version 2 is required)

```
{
    "controller": {
    },
    "workers": [
       {
          "type": "router",
          "options": {
             "pythonpath": [".."]
          },
          "realms": [
             {
                "name": "realm1",
                "roles": [
                   {
                      "name": "anonymous",
                      "permissions": [
                         {
                            "uri": "*",
                            "allow": {
                               "call": true,
                               "register": true,
                               "publish": true,
                               "subscribe": true
                            }
                         }
                      ]
                   }
                ]
             }
          ],
          "transports": [
             {
                "type": "websocket",
                "endpoint": {
                   "type": "tcp",
                   "port": 9000
                }
             },
             {
                "type": "web",
                "endpoint": {
                   "type": "tcp",
                   "port": "$PORT"
                },
                "paths": {
                   "/": {
                      "type": "static",
                      "directory": "../hello/web"
                   },
                   "ws": {
                      "type": "websocket"
                   }
                }
             }
          ]
       },
       {
          "type": "container",
          "options": {
             "pythonpath": [".."]
          },
           "components": [
             {
                "type": "class",
                "classname": "hello.hello.AppSession",
                "realm": "realm1",
                "transport": {
                   "type": "websocket",
                   "url": "ws://127.0.0.1:9000",
                   "endpoint": {
                      "type": "tcp",
                      "host": "127.0.0.1",
                      "port": 9000
                  }
                }
             }
          ]
       }
    ]
}
```
What you get¶

When you Heroku app is started, you should be able to access the generated "Hello, world" Crossbar.io demo application like

Crossbar.io on Heroku 2
Crossbar.io renders a status page when you visit the WebSocket endpoint from a browser:

Crossbar.io on Heroku 1
As you can see in above, the IP and port that Crossbar.io runs on is an internal IP - behind the Heroku load-balancer, on a private network (10.x.x.x).

When looking at the WebSocket network connection from the browser dev tools, you can again see from the headers sent in the initial WebSocket opening handshake that a proxy is in place:



NOTES:

```
When you create your local environment (virtualenv) and run the project locally, The crossbar config will read the now changed port value in the web transport of the router worker from your environment. Crossbar wont start if this value is not set. In order to set it do the following: (Taken from Heroku Docs)(https://devcenter.heroku.com/articles/heroku-local)

Set up your local environment variables
When running your app, you will typically use a set of config vars to capture the configuration of the app. For example: say your app uses S3 for image storage. You would want to store the credentials to S3 as config vars. If you’re running your app locally, you typically want to use a different S3 bucket than if you were running it in production.
The .env file lets you capture all the config vars that you need in order to run your app locally. When you start your app using any of the heroku local commands, the .env file is read, and each name/value pair is inserted into the environment, to mimic the action of config vars.
View your app’s config vars
To view all of your app’s config vars, type heroku config.
Look at the contents of your .env file
$ cat .env
Here’s an example .env file:
S3_KEY=mykey
S3_SECRET=mysecret
Add a config var to your .env file
Credentials and other sensitive configuration values should not be committed to source-control. In Git exclude the .env file with: echo .env >> .gitignore.

To add a config var to your .env file, edit it and add a new name=value pair on a new line.
Copy Heroku config vars to your local .env file
Sometimes you may want to use the same config var in both local and Heroku environments. For each config var that you want to add to your .env file, use the following command:
$ heroku config:get CONFIG-VAR-NAME -s  >> .env
Do not commit the .env file to source control. It should only be used for local configuration. Update your .gitignore file to exclude the .env file.

You can also set this value in your global environment file by echoing the port to the global environment file on your local system.
```