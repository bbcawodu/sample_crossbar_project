from os import environ
from twisted.internet.defer import inlineCallbacks, \
    returnValue

from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from autobahn.twisted.util import sleep


class Component(ApplicationSession):
    """
    A math service application component.
    """

    @inlineCallbacks
    def onJoin(self, details):
        print("session attached")

        def square(x):
            return x * x

        yield self.register(square, u'examples.rpc.slow-square.square')

        @inlineCallbacks
        def slowsquare(x, delay=1):
            yield sleep(delay)
            returnValue(x * x)

        # ApplicationSession.register can take functions which return deferreds as well as other python objects
        yield self.register(slowsquare, u'examples.rpc.slow-square.slowsquare')

        print("procedures registered")


if __name__ == '__main__':
    runner = ApplicationRunner(
        environ.get("AUTOBAHN_DEMO_ROUTER", u"ws://127.0.0.1:8080/ws"),
        u"example_realm",
    )
    runner.run(Component)
