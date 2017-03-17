from __future__ import print_function

from os import environ
from twisted.internet.defer import inlineCallbacks

from autobahn.wamp.types import PublishOptions
from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner


class Component(ApplicationSession):
    """
    An application component that publishes an event every second.
    """

    @inlineCallbacks
    def onJoin(self, details):
        print("session attached")

        def on_event(i):
            print("Got event: {}".format(i))

        yield self.subscribe(on_event, u'examples.pubsub.options.topic1')

        counter = 0
        while True:
            print("publish: examples.pubsub.options.topic1", counter)
            pub_options = PublishOptions(
                acknowledge=True,
                exclude_me=False
            )
            publication = yield self.publish(
                u'examples.pubsub.options.topic1', counter,
                options=pub_options,
            )
            print("Published with publication ID {}".format(publication.id))
            counter += 1
            yield sleep(1)


if __name__ == '__main__':
    runner = ApplicationRunner(
        environ.get("AUTOBAHN_DEMO_ROUTER", u"ws://127.0.0.1:8080/ws"),
        u"example_realm",
    )
    runner.run(Component)
