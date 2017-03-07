###############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) Crossbar.io Technologies GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
###############################################################################

from __future__ import print_function
from os import environ
import urlparse
from twisted.internet.defer import inlineCallbacks
from twisted.enterprise import adbapi
from twistar.registry import Registry
from twistar.dbobject import DBObject
from autobahn.wamp.types import CallResult
from twisted.internet.defer import returnValue
from twisted.internet.defer import Deferred

from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner

# Get Database url from environment variables
urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(environ["DATABASE_URL"])


class Component(ApplicationSession):
    """
    An application component that adds a user to the users table in the database
    """

    @inlineCallbacks
    def onJoin(self, details):
        print("session attached")

        ## create a new database connection pool. connections are created lazy (as needed)
        ##
        def onPoolConnectionCreated(conn):
            ## callback fired when Twisted adds a new database connection to the pool.
            ## use this to do any app specific configuration / setup on the connection
            pid = conn.get_backend_pid()
            print("New DB connection created (backend PID {})".format(pid))

        Registry.DBPOOL = adbapi.ConnectionPool("psycopg2",
                                                host=url.hostname,
                                                port=url.port,
                                                database=url.path[1:],
                                                user=url.username,
                                                password=url.password,
                                                cp_min=3,
                                                cp_max=10,
                                                cp_noisy=True,
                                                cp_openfun=onPoolConnectionCreated,
                                                cp_reconnect=True,
                                                cp_good_sql="SELECT 1")

        yield self.register(self.add_user, u'examples.twisted_db_comonent.twistar.add_user')
        print("Procedures registered; ready for frontend.")

    @inlineCallbacks
    def inline_add_user(self, first_name, last_name, age):
        # class User(DBObject):
        #     pass
        #
        # def done(user):
        #     print("A user has just been saved with id: %i" % user.id)
        #     # return [user.id, user.first_name, user.last_name, user.age]
        #     return CallResult(id=user.id, first_name=user.first_name, last_name=user.last_name, age=user.age)
        #
        # u = User()
        # u.first_name = first_name
        # u.last_name = last_name
        # u.age = age
        #
        # # Asynchronous call, returns a deferred
        # d = u.save()
        # result = d.addCallback(done)

        # return CallResult(id=result[0], first_name=result[1], last_name=result[2], age=result[3])

        class User(DBObject):
            pass

        u = User()
        u.first_name = first_name
        u.last_name = last_name
        u.age = age

        user = yield u.save()
        print("A user has just been saved with id: %i" % user.id)
        returnValue(CallResult(id=user.id, first_name=user.first_name, last_name=user.last_name, age=user.age))

    def add_user(self, first_name, last_name, age):
        class User(DBObject):
            pass

        def add_user_to_db(user):
            return user.save()

        def done(user):
            print("A user has just been saved with id: %i" % user.id)
            # return [user.id, user.first_name, user.last_name, user.age]
            return CallResult(id=user.id, first_name=user.first_name, last_name=user.last_name, age=user.age)

        u = User()
        u.first_name = first_name
        u.last_name = last_name
        u.age = age

        # Asynchronous call, returns a deferred
        d = Deferred()
        d.addCallback(add_user_to_db)
        d.addCallback(done)

        d.callback(u)
        return d


if __name__ == '__main__':
    runner = ApplicationRunner(
        environ.get("AUTOBAHN_DEMO_ROUTER", u"ws://127.0.0.1:8080/ws"),
        u"example_realm",
    )
    runner.run(Component)
