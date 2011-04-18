import time
import random

from twisted.words.protocols import irc
from twisted.internet import protocol

class BanliBot(irc.IRCClient):
    nickname = "banli"
    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
    def signedOn(self):
        self.join(self.factory.channel)
    def userJoined(self,user,channel):
        if channel == self.factory.channel:
            self.say(self.factory.channel,"OMG HAI {0}".format(user.upper()))

class BanliFactory(protocol.ClientFactory):

    protocol = BanliBot

    def __init__(self,channel="#que"):
        self.channel = channel
        self.private_messagers = {}

if __name__ == '__main__':
    from twisted.internet import reactor
    f = BanliFactory()
    reactor.connectTCP("irc.ecs.soton.ac.uk",6667,f)
    reactor.run()
