import random
import collections

class TwoWordMarkov(object):
    def __init__(self):
        self.words = []
        self.cache = collections.defaultdict(list)

    def feed(self,sentence):
        # Given a string, feed it into the database.
        words = sentence.split()
        self.words.extend(words)
        for w1, w2, w3 in triples(words):
            key = (w1, w2)
            self.cache[key].append(w3)

    def generate(self, size=25):
        seed = random.randint(0, len(self.words)-3)
        seed_word, next_word = self.words[seed], self.words[seed+1]
        w1, w2 = seed_word, next_word
        gen_words = list()
        for i in xrange(size):
            gen_words.append(w1)
            w1, w2 = w2, random.choice(self.cache[(w1, w2)])
        gen_words.append(w2)
        return ' '.join(gen_words)

def triples(words):
    """ Generates triples from the given data string. So if our string were
    "What a lovely day", we'd generate (What, a, lovely) and then
    (a, lovely, day).
    """
    if len(words) < 3:
        return
    for i in range(len(words) - 2):
        yield (words[i], words[i+1], words[i+2])
