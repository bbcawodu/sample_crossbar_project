from os import environ
from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner


class Component(ApplicationSession):
    """
    An application component providing procedures with different kinds
    of arguments.
    """

    @inlineCallbacks
    def onJoin(self, details):
        print("session attached")

        def ping():
            return

        def add2(a, b):
            return a + b

        def stars(nick="somebody", stars=0):
            return u"{} starred {}x".format(nick, stars)

        def orders(product, limit=5):
            return [u"Product {}".format(i) for i in range(50)][:limit]

        def arglen(*args, **kwargs):
            return [len(args), len(kwargs)]

        yield self.register(ping, u'examples.rpc.arguments.ping')
        yield self.register(add2, u'examples.rpc.arguments.add2')
        yield self.register(stars, u'examples.rpc.arguments.stars')
        yield self.register(orders, u'examples.rpc.arguments.orders')
        yield self.register(arglen, u'examples.rpc.arguments.arglen')
        print("Procedures registered; ready for frontend.")


if __name__ == '__main__':
    runner = ApplicationRunner(
        environ.get("AUTOBAHN_DEMO_ROUTER", u"ws://127.0.0.1:8080/ws"),
        u"example_realm",
    )
    runner.run(Component)