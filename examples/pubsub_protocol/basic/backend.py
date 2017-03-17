from __future__ import print_function
from os import environ

from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner


class Component(ApplicationSession):
    """
    An application component that publishes an event every second.
    """

    @inlineCallbacks
    def onJoin(self, details):
        print("session attached")
        counter = 0
        while True:
            print('backend publishing examples.pubsub.basic.topic1', counter)
            self.publish(u'examples.pubsub.basic.topic1', counter)
            counter += 1
            yield sleep(1)


if __name__ == '__main__':
    runner = ApplicationRunner(
        environ.get("AUTOBAHN_DEMO_ROUTER", u"ws://127.0.0.1:8080/ws"),
        u"example_realm",
    )
    runner.run(Component)
