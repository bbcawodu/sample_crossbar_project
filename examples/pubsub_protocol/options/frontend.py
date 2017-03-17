from __future__ import print_function

from os import environ
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks

from autobahn.wamp.types import SubscribeOptions
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner


class Component(ApplicationSession):

    """
    An application component that subscribes and receives events,
    and stop after having received 5 events.
    """

    @inlineCallbacks
    def onJoin(self, details):
        print("session attached")

        self.received = 0

        def on_event(i, details=None):
            msg = "Got event, publication ID {}, publisher {}: {}"
            print(msg.format(details.publication, details.publisher, i))
            self.received += 1
            if self.received > 5:
                self.leave()

        yield self.subscribe(on_event, u'examples.pubsub.options.topic1',
                             options=SubscribeOptions(details_arg='details'))

    def onDisconnect(self):
        print("disconnected")
        reactor.stop()


if __name__ == '__main__':
    runner = ApplicationRunner(
        environ.get("AUTOBAHN_DEMO_ROUTER", u"ws://127.0.0.1:8080/ws"),
        u"example_realm",
    )
    runner.run(Component)