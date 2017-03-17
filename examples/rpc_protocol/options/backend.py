from os import environ
from twisted.internet.defer import inlineCallbacks

from autobahn.wamp.types import RegisterOptions, PublishOptions
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner


class Component(ApplicationSession):

    """
    An application component providing procedures with
    different kinds of arguments.
    """

    @inlineCallbacks
    def onJoin(self, details):
        print("session attached")

        def square(val, details=None):
            print("square called from: {}".format(details.caller))

            if val < 0:
                self.publish(u'examples.rpc.options.square_on_nonpositive', val)
            elif val == 0:
                if details.caller:
                    options = PublishOptions(exclude=[details.caller])
                else:
                    options = None
                self.publish(u'examples.rpc.options.square_on_nonpositive', val, options=options)
            return val * val

        yield self.register(square, u'examples.rpc.options.square', RegisterOptions(details_arg='details'))

        print("procedure registered")


if __name__ == '__main__':
    runner = ApplicationRunner(
        environ.get("AUTOBAHN_DEMO_ROUTER", u"ws://127.0.0.1:8080/ws"),
        u"example_realm",
    )
    runner.run(Component)