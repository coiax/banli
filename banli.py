import time
import random
import pickle
import json
import difflib
import sys

from twisted.words.protocols import irc
from twisted.internet import protocol

import markovgen

class BanliBot(irc.IRCClient):
    def __init__(self):
        self.quiet = False

    nickname = "banli"
    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
    def signedOn(self):
        self.join(self.factory.channel)
    def userJoined(self,user,channel):
        if channel == self.factory.channel:
            self.say(self.factory.channel,"OMG HAI {0}".format(user.upper()))
    def action(self,user,channel,msg):
        self.privmsg(user,channel,msg)
    def set_quiet(self,value):
        self.quiet = value
    def privmsg(self,user,channel,msg):
        print user,channel,msg
        clean = msg.strip("\n")
        if clean == self.nickname + ": Quiet!":
            self.set_quiet(True)
            self.msg(self.factory.channel,"I'm shut up. For now.")

            reactor.callLater(600, self.set_quiet, False)
        elif clean.find(self.nickname) != -1 and self.quiet:
            self.set_quiet(False)
            self.say(self.factory.channel,"Someone say my name?")
        elif clean == "Time for markov!":
            self.msg(channel,self.factory.markov.generate())
        if channel == self.factory.channel:
            output = self.factory.check_map(clean)
            if (output is not None) and (not self.quiet):
                self.say(self.factory.channel,str(output))
            self.factory.markov.feed(clean)
            self.factory.dump_markov()

        if channel == self.nickname:
            output = self.factory.add_to_map(msg)
            if output == "bad json":
                key,value = self.factory.check_map(clean,expanded=True)
                print key,value
                self.msg(user.split("!")[0],"{0},{1}".format(key,value))

class BanliFactory(protocol.ClientFactory):

    protocol = BanliBot

    def __init__(self,channel="#awesome"):
        self.channel = channel
        self.map = {}
        with open(sys.argv[2]) as f:
            self.map = pickle.load(f)
        print self.map

        self.markov = markovgen.TwoWordMarkov()
        with open('markov') as f:
            self.markov = pickle.load(f)
        print len(self.markov.words)

    def dump_markov(self):
        with open('markov','w') as f:
            pickle.dump(self.markov,f)

    def check_map(self,item,expanded=False):
        # either return none, or an item
        match = difflib.get_close_matches(item,self.map.keys())
        if not expanded:
            if match == []:
                return None
            else:
                return self.map[match[0]]
        else:
            if match == []:
                return None,None
            else:
                return match[0],self.map[match[0]]

    def add_to_map(self,item):
        try:
            d = json.loads(item)
        except ValueError:
            return "bad json"
        try:
            self.map.update(d)
        except TypeError:
            return "bad type"

        with open(sys.argv[2],'w') as f:
            pickle.dump(self.map,f)
        print self.map

if __name__ == '__main__':
    from twisted.internet import reactor
    f = BanliFactory(sys.argv[1])
    reactor.connectTCP("irc.ecs.soton.ac.uk",6667,f)
    reactor.run()
