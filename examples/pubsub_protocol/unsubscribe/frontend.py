from __future__ import print_function

from os import environ
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner


class Component(ApplicationSession):
    """
    An application component that subscribes and receives events.
    After receiving 5 events, it unsubscribes, sleeps and then
    resubscribes for another run. Then it stops.
    """

    @inlineCallbacks
    def test(self):
        self.received = 0
        self.sub = yield self.subscribe(self.on_event, u'examples.pubsub.unsubscribe.topic1')
        print("Subscribed with subscription ID {}".format(self.sub.id))

    @inlineCallbacks
    def on_event(self, i):
        print("Got event: {}".format(i))
        self.received += 1
        if self.received > 5:
            self.runs += 1
            if self.runs > 1:
                self.leave()
            else:
                yield self.sub.unsubscribe()
                print("Unsubscribed .. continue in 5s ..")
                reactor.callLater(5, self.test)

    @inlineCallbacks
    def onJoin(self, details):
        print("session attached")
        self.runs = 0
        yield self.test()

    def onDisconnect(self):
        print("disconnected")
        reactor.stop()


if __name__ == '__main__':
    runner = ApplicationRunner(
        environ.get("AUTOBAHN_DEMO_ROUTER", u"ws://127.0.0.1:8080/ws"),
        u"example_realm",
    )
    runner.run(Component)