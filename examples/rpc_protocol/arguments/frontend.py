from os import environ
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner


class Component(ApplicationSession):
    """
    An application component calling the different backend procedures.
    """

    @inlineCallbacks
    def onJoin(self, details):
        print("session attached")

        yield self.call(u'examples.rpc.arguments.ping')
        print("Pinged!")

        res = yield self.call(u'examples.rpc.arguments.add2', 2, 3)
        print("Add2: {}".format(res))

        starred = yield self.call(u'examples.rpc.arguments.stars')
        print("Starred 1: {}".format(starred))

        starred = yield self.call(u'examples.rpc.arguments.stars', nick=u'Homer')
        print("Starred 2: {}".format(starred))

        starred = yield self.call(u'examples.rpc.arguments.stars', stars=5)
        print("Starred 3: {}".format(starred))

        starred = yield self.call(u'examples.rpc.arguments.stars', nick=u'Homer', stars=5)
        print("Starred 4: {}".format(starred))

        orders = yield self.call(u'examples.rpc.arguments.orders', u'coffee')
        print("Orders 1: {}".format(orders))

        orders = yield self.call(u'examples.rpc.arguments.orders', u'coffee', limit=10)
        print("Orders 2: {}".format(orders))

        arglengths = yield self.call(u'examples.rpc.arguments.arglen')
        print("Arglen 1: {}".format(arglengths))

        arglengths = yield self.call(u'examples.rpc.arguments.arglen', 1, 2, 3)
        print("Arglen 2: {}".format(arglengths))

        arglengths = yield self.call(u'examples.rpc.arguments.arglen', a=1, b=2, c=3)
        print("Arglen 3: {}".format(arglengths))

        arglengths = yield self.call(u'examples.rpc.arguments.arglen', 1, 2, 3, a=1, b=2, c=3)
        print("Arglen 4: {}".format(arglengths))

        self.leave()

    def onDisconnect(self):
        print("disconnected")
        reactor.stop()


if __name__ == '__main__':
    runner = ApplicationRunner(
        environ.get("AUTOBAHN_DEMO_ROUTER", u"ws://127.0.0.1:8080/ws"),
        u"example_realm",
    )
    runner.run(Component)