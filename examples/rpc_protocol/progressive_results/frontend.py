from os import environ
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks

from autobahn.wamp.types import CallOptions
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner


class Component(ApplicationSession):
    """
    Application component that consumes progressive results.
    """

    @inlineCallbacks
    def onJoin(self, details):
        print("session attached")

        def on_progress(i):
            print("Progress: {}".format(i))

        res = yield self.call(u'examples.rpc.progressive_results.longop', 3, options=CallOptions(on_progress=on_progress))

        print("Final: {}".format(res))

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