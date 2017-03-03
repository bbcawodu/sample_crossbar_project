import psycopg2
import os
import urlparse

from twisted.enterprise import adbapi
from twisted.internet.defer import inlineCallbacks, returnValue

from autobahn import wamp
from autobahn.twisted.wamp import ApplicationSession

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

class MyDatabaseComponent(ApplicationSession):

   @inlineCallbacks
   def onJoin(self, details):

      ## create a new database connection pool. connections are created lazy (as needed)
      ##
      def onPoolConnectionCreated(conn):
         ## callback fired when Twisted adds a new database connection to the pool.
         ## use this to do any app specific configuration / setup on the connection
         pid = conn.get_backend_pid()
         print("New DB connection created (backend PID {})".format(pid))

      pool = adbapi.ConnectionPool("psycopg2",
                                    host = url.hostname,
                                    port = url.port,
                                    database = url.path[1:],
                                    user = url.username,
                                    password = url.password,
                                    cp_min = 3,
                                    cp_max = 10,
                                    cp_noisy = True,
                                    cp_openfun = onPoolConnectionCreated,
                                    cp_reconnect = True,
                                    cp_good_sql = "SELECT 1")

      ## we'll be doing all database access via this database connection pool
      ##
      self.db = pool

      ## register all procedures on this class which have been
      ## decorated to register them for remoting.
      ##
      regs = yield self.register(self)
      print("registered {} procedures".format(len(regs)))


   @wamp.register(u'com.example.now.v1')
   def get_dbnow(self):
      ## this variant demonstrates basic usage for running queries

      d = self.db.runQuery("SELECT now()")

      def got(rows):
         res = "{0}".format(rows[0][0])
         return res

      d.addCallback(got)
      return d


   @wamp.register(u'com.example.now.v2')
   @inlineCallbacks
   def get_dbnow_inline(self):
      ## this variant is using inline callbacks which makes code "look synchronous",
      ## nevertheless run asynchronous under the hood

      rows = yield self.db.runQuery("SELECT now()")
      res = "{0}".format(rows[0][0])
      returnValue(res)


   @wamp.register(u'com.example.now.v3')
   def get_dbnow_interaction(self):
      ## this variant runs the query inside a transaction (which might do more,
      ## and still be atomically committed/rolled back)

      def run(txn):
         txn.execute("SELECT now()")
         rows = txn.fetchall()
         res = "{0}".format(rows[0][0])
         return res

      return self.db.runInteraction(run)



if __name__ == '__main__':
   from autobahn.twisted.wamp import ApplicationRunner

   runner = ApplicationRunner(url = u"ws://127.0.0.1:8080/ws", realm = u"example_realm")
   runner.run(MyDatabaseComponent)