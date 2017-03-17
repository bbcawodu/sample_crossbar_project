import math
from os import environ

from twisted.internet import reactor
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
    Example WAMP application frontend that catches exceptions.
    """

    @inlineCallbacks
    def onJoin(self, details):
        print("session attached")

        # catching standard exceptions
        ##
        for x in [2, 0, -2]:
            try:
                res = yield self.call(u'examples.rpc_protocol.errors.sqrt', x)
            except Exception as e:
                print("Error: {} {}".format(e, e.args))
            else:
                print("Result: {}".format(res))

        # catching WAMP application exceptions
        ##
        for name in ['foo', 'a', '*' * 11, 'Hello']:
            try:
                res = yield self.call(u'examples.rpc_protocol.errors.checkname', name)
            except ApplicationError as e:
                print("Error: {} {} {} {}".format(e, e.error, e.args, e.kwargs))
            else:
                print("Result: {}".format(res))

        # defining and automapping WAMP application exceptions
        ##
        self.define(AppError1)

        try:
            yield self.call(u'examples.rpc_protocol.errors.compare', 3, 17)
        except AppError1 as e:
            print("Compare Error: {}".format(e))

        print("Exiting; we received only errors we expected.")
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