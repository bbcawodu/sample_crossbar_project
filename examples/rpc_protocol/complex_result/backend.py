from os import environ
from twisted.internet.defer import inlineCallbacks

from autobahn.wamp.types import CallResult
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner


class Component(ApplicationSession):

    """
    Application component that provides procedures which
    return complex results(call results with more than one positional or keyword results).
    """

    @inlineCallbacks
    def onJoin(self, details):
        print("session attached")

        def add_complex(a, ai, b, bi):
            return CallResult(c=a + b, ci=ai + bi)

        yield self.register(add_complex, u'examples.rpc.complex_result.add_complex')

        def split_name(fullname):
            forename, surname = fullname.split()
            return CallResult(forename, surname)

        yield self.register(split_name, u'examples.rpc.complex_result.split_name')

        print("procedures registered")


if __name__ == '__main__':
    runner = ApplicationRunner(
        environ.get("AUTOBAHN_DEMO_ROUTER", u"ws://127.0.0.1:8080/ws"),
        u"example_realm",
    )
    runner.run(Component)