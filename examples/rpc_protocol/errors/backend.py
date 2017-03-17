import math
from os import environ

from twisted.internet.defer import inlineCallbacks

from autobahn import wamp
from autobahn.wamp.exception import ApplicationError
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner


@wamp.error(u"com.examples.rpc_protocol.errors.error1")
class AppError1(Exception):
    """
    An application specific exception that is decorated with a WAMP URI,
    and hence can be automapped by Autobahn.
    """


class Component(ApplicationSession):
    """
    Example WAMP application backend that raised exceptions.
    """

    @inlineCallbacks
    def onJoin(self, details):
        print("session attached")

        # raising standard exceptions
        ##
        def sqrt(x):
            if x == 0:
                raise Exception("don't ask foolish questions;)")
            else:
                # this also will raise, if x < 0
                return math.sqrt(x)

        yield self.register(sqrt, u'examples.rpc_protocol.errors.sqrt')

        # raising WAMP application exceptions
        ##
        def checkname(name):
            if name in ['foo', 'bar']:
                raise ApplicationError(u"examples.rpc_protocol.errors.reserved")

            if name.lower() != name.upper():
                # forward positional arguments in exceptions
                raise ApplicationError(u"examples.rpc_protocol.errors.mixed_case", name.lower(), name.upper())

            if len(name) < 3 or len(name) > 10:
                # forward keyword arguments in exceptions
                raise ApplicationError(u"examples.rpc_protocol.errors.invalid_length", min=3, max=10)

        yield self.register(checkname, u'examples.rpc_protocol.errors.checkname')

        # defining and automapping WAMP application exceptions
        ##
        self.define(AppError1)

        def compare(a, b):
            if a < b:
                raise AppError1(b - a)

        yield self.register(compare, u'examples.rpc_protocol.errors.compare')

        print("procedures registered")


if __name__ == '__main__':
    runner = ApplicationRunner(
        environ.get("AUTOBAHN_DEMO_ROUTER", u"ws://127.0.0.1:8080/ws"),
        u"example_realm",
    )
    runner.run(Component)