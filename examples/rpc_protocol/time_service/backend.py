from os import environ
import datetime

from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner


class Component(ApplicationSession):
    """
    A simple time service application component.
    """

    @inlineCallbacks
    def onJoin(self, details):
        print("session attached")

        def utcnow():
            now = datetime.datetime.utcnow()
            return now.strftime("%Y-%m-%dT%H:%M:%SZ")

        try:
            yield self.register(utcnow, u'examples.rpc.timeservice.now')
        except Exception as e:
            print("failed to register procedure: {}".format(e))
        else:
            print("procedure registered")


if __name__ == '__main__':
    runner = ApplicationRunner(
        environ.get("AUTOBAHN_DEMO_ROUTER", u"ws://127.0.0.1:8080/ws"),
        u"example_realm",
    )
    runner.run(Component)