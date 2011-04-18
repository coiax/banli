import time
import random

from twisted.words.protocols import irc
from twisted.internet import protocol

class BanliBot(irc.IRCClient):
    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
    def signedOn(self):
        self.setNick("banli")
        self.join(self.factory.channel)
    def userJoined(self,user,channel):
        if channel == self.factory.channel:
            self.say(self.factory.channel,"OMG HAI {0}".format(user.upper()))
    def privmsg(self,user,channel,msg):
        print user,channel,msg
        if channel == self.nickname:
            last_bothered = self.factory.private_messagers.get(user,0)
            diff = time.time() - last_bothered
            if diff > 600:
                msg = "Private messages, srsly?"
                self.msg(user,msg)
                self.factory.private_messagers[user] = time.time()
        if channel == self.factory.channel:
            if msg.find(self.nickname) != -1:
                msg = "{0}: tsup".format(user.split('!')[0])
                self.msg(channel,msg)

class BanliFactory(protocol.ClientFactory):

    protocol = BanliBot

    def __init__(self,channel="#awesome"):
        self.channel = channel
        self.private_messagers = {}

if __name__ == '__main__':
    from twisted.internet import reactor
    f = BanliFactory()
    reactor.connectTCP("irc.ecs.soton.ac.uk",6667,f)
    reactor.run()
