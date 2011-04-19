import time
import random
import pickle
import json
import difflib
import sys

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

    def privmsg(self,user,channel,msg):
        print user,channel,msg
        clean = msg.strip("\n")
        if channel == self.factory.channel:
            output = self.factory.check_map(clean)
            if output is not None:
                self.say(self.factory.channel,str(output))
        if channel == self.nickname:
            self.factory.add_to_map(msg)

class BanliFactory(protocol.ClientFactory):

    protocol = BanliBot

    def __init__(self,channel="#awesome"):
        self.channel = channel
        self.map = {}
        with open(sys.argv[2]) as f:
            self.map = pickle.load(f)
        print self.map

    def check_map(self,item):
        # either return none, or an item
        match = difflib.get_close_matches(item,self.map.keys())
        if match == []:
            return None
        else:
            return self.map[match[0]]

    def add_to_map(self,item):
        try:
            d = json.loads(item)
        except ValueError:
            return
        try:
            self.map.update(d)
        except TypeError:
            return

        with open(sys.argv[2],'w') as f:
            pickle.dump(self.map,f)
        print self.map

if __name__ == '__main__':
    from twisted.internet import reactor
    f = BanliFactory(sys.argv[1])
    reactor.connectTCP("irc.ecs.soton.ac.uk",6667,f)
    reactor.run()
