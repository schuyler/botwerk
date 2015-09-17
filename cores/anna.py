from __future__ import with_statement
import Pyro4
import time, logging, sys, re

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

model = Pyro4.core.Proxy('PYRONAME:word2vec')
analogy = re.compile(r'^(.+?)\s*:\s*(.+?)\s*::\s*(.+?)\s*:\s*\?')
what_is = re.compile(r'(?:what|who)\s+(?:is|are)\s+the\s+(.+?)\s+of\s+(.+?)\??', re.IGNORECASE)
versus = re.compile(r'(.+?)\s+(?:vs\.?|versus)\s+(.+?)')
arithmetic = re.compile(r'\s*([+-])\s*')
min_count = 1e6

class Annalogue(object):
    def underscore(self, word):
        # the lower() is just for the non-GoogleNews models
        return word.strip().replace(" ", "_") #.lower()

    def find_most_similar(self, pos, neg):
        try:
           return model.most_similar(pos, neg, 5)
        except:
            logging.exception("find_most_similar")
        return []

    def analogize(self, match):
        pos = [self.underscore(s) for s in (match.group(2), match.group(3))]
        neg = [self.underscore(s) for s in (match.group(1),)]
        return self.find_most_similar(pos, neg)

    def compare(self, match):
        word1, word2 = (self.underscore(s) for s in (match.group(1), match.group(2)))
        try:
            return "%.1f%%" % (model.similarity(word1, word2) * 100.0)
        except:
            logging.exception("compare")
            return None

    def compute_sum(self, tokens):
        pos, neg = [], []
        positive = True
        for word in tokens:
            if word == '+':
                positive = True
            elif word == '-':
                positive = False
            else:
                token = self.underscore(word)
                if positive:
                    pos.append(token)
                else:
                    neg.append(token)
        return self.find_most_similar(pos, neg)
           
    def tell(self, text):
        results = []
        match = analogy.search(text)
        if match:
            results = self.analogize(match)
        elif arithmetic.search(text):
            tokens = arithmetic.split(text)
            results = self.compute_sum(tokens)
        elif what_is.search(text):
            match = what_is.search(text)
            pos = [self.underscore(match.group(n)) for n in (1,2)]
            results = self.find_most_similar(pos, [])
        elif versus.search(text):
            match = versus.search(text)
            result = self.compare(match)
            if result: return result # a percentage, not an answer

        if not results:
            return ":confused:"

        word, score = results[0]
        word = word.replace("_", " ").capitalize()
        if score > 0.9:
            word += "!"
        elif score > 0.55:
            word += "."
        else:
            other_choices = [w.replace("_", " ") for w, s in results[1:]]
            word += "? (or maybe " + ", ".join(other_choices) + "?)"
        return word

with Pyro4.core.Daemon() as daemon:
    with Pyro4.naming.locateNS() as ns:
        uri = daemon.register(Annalogue())
        ns.register("annalogue", uri)
    daemon.requestLoop()
