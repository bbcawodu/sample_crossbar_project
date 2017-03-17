from __future__ import print_function
from os import environ

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner


class Component(ApplicationSession):
    """
    An application component that subscribes and receives events, and
    stop after having received 5 events.
    """

    @inlineCallbacks
    def onJoin(self, details):
        print("session attached")
        self.received = 0
        sub = yield self.subscribe(self.on_event, u'examples.pubsub.basic.topic1')
        print("Subscribed to examples.pubsub.basic.topic1 with {}".format(sub.id))

    def on_event(self, i):
        print("Got event: {}".format(i))
        self.received += 1
        # self.config.extra for configuration, etc. (see [A])
        if self.received > self.config.extra['max_events']:
            print("Received enough events; disconnecting.")
            self.leave()

    def onDisconnect(self):
        print("disconnected")
        if reactor.running:
            reactor.stop()


if __name__ == '__main__':
    runner = ApplicationRunner(
        environ.get("AUTOBAHN_DEMO_ROUTER", u"ws://127.0.0.1:8080/ws"),
        u"example_realm",
        extra=dict(
            max_events=5,  # [A] pass in additional configuration
        ),
    )
    runner.run(Component)