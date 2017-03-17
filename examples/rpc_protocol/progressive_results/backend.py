from os import environ
from twisted.internet.defer import inlineCallbacks, returnValue

from autobahn.wamp.types import RegisterOptions
from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner


class Component(ApplicationSession):
    """
    Application component that produces progressive results.
    """

    @inlineCallbacks
    def onJoin(self, details):
        print("session attached")

        @inlineCallbacks
        def longop(n, details=None):
            if details.progress:
                # caller can (and requested to) consume progressive results
                for i in range(n):
                    details.progress(i)
                    yield sleep(1)
            else:
                # process like a normal call (not producing progressive results)
                yield sleep(1 * n)
            returnValue(n)

        yield self.register(longop, u'examples.rpc.progressive_results.longop', RegisterOptions(details_arg='details'))

        print("procedures registered")


if __name__ == '__main__':
    runner = ApplicationRunner(
        environ.get("AUTOBAHN_DEMO_ROUTER", u"ws://127.0.0.1:8080/ws"),
        u"example_realm",
    )
    runner.run(Component)