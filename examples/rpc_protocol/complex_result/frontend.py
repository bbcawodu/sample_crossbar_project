from os import environ
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner


class Component(ApplicationSession):
    """
    Application component that calls procedures which
    produce complex results (call results with more than one
    positional or keyword results) and showing how to access those.
    """

    @inlineCallbacks
    def onJoin(self, details):
        print("session attached")

        res = yield self.call(u'examples.rpc.complex_result.add_complex', 2, 3, 4, 5)
        print("Result: {} + {}i".format(res.kwresults['c'], res.kwresults['ci']))

        res = yield self.call(u'examples.rpc.complex_result.split_name', 'Homer Simpson')
        print("Forname: {}, Surname: {}".format(res.results[0], res.results[1]))

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