from os import environ
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks

from autobahn.wamp.types import CallOptions
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner


class Component(ApplicationSession):
    """
    An application component calling the different backend procedures.
    """

    @inlineCallbacks
    def onJoin(self, details):
        print("session attached")

        def on_event(val):
            print("Someone requested to square non-positive: {}".format(val))

        yield self.subscribe(on_event, u'examples.rpc.options.square_on_nonpositive')

        for val in [2, 0, -2]:
            res = yield self.call(u'examples.rpc.options.square', val, options=CallOptions())
            print("Squared {} = {}".format(val, res))

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