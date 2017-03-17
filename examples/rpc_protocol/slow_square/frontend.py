import time
from os import environ

from twisted.internet import reactor
from twisted.internet.defer import DeferredList

from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner


class Component(ApplicationSession):
    """
    An application component using the time service.
    """

    def onJoin(self, details):
        print("session attached")

        def got(res, started, msg):
            duration = 1000. * (time.clock() - started)
            print("{}: {} in {}".format(msg, res, duration))

        t1 = time.clock()
        d1 = self.call(u'examples.rpc.slow-square.slowsquare', 3)
        d1.addCallback(got, t1, "Slow Square")

        t2 = time.clock()
        d2 = self.call(u'examples.rpc.slow-square.square', 3)
        d2.addCallback(got, t2, "Quick Square")

        def done(_):
            print("All finished.")
            self.leave()

        DeferredList([d1, d2]).addBoth(done)

    def onDisconnect(self):
        print("disconnected")
        reactor.stop()


if __name__ == '__main__':
    runner = ApplicationRunner(
        environ.get("AUTOBAHN_DEMO_ROUTER", u"ws://127.0.0.1:8080/ws"),
        u"example_realm",
    )
    runner.run(Component)