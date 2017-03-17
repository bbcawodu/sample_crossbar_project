from os import environ

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks

from autobahn.wamp.types import SubscribeOptions
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner


class Component(ApplicationSession):

    """
    An application component that subscribes and receives events
    of no payload and of complex payload, and stops after 5 seconds.
    """

    @inlineCallbacks
    def onJoin(self, details):
        print("session attached")

        self.received = 0

        def on_heartbeat(details=None):
            print("heartbeat (publication ID {})".format(details.publication))

        yield self.subscribe(
            on_heartbeat, u'examples.pubsub.complex.heartbeat',
            options=SubscribeOptions(details_arg='details')
        )

        def on_topic2(a, b, c=None, d=None):
            print("Got event: {} {} {} {}".format(a, b, c, d))

        yield self.subscribe(on_topic2, u'examples.pubsub.complex.topic2')

        reactor.callLater(5, self.leave)

    def onDisconnect(self):
        print("disconnected")
        reactor.stop()


if __name__ == '__main__':
    runner = ApplicationRunner(
        environ.get("AUTOBAHN_DEMO_ROUTER", u"ws://127.0.0.1:8080/ws"),
        u"example_realm",
    )
    runner.run(Component)