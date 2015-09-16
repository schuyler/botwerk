from __future__ import with_statement
import Pyro4, gensim
import time, logging, sys

class ModelService(gensim.models.Word2Vec):
    def frequency(self, word):
        return self.vocab[word]

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

print("Loading", sys.argv[1])
start = time.time()
model = ModelService.load_word2vec_format(sys.argv[1], binary=True)
#model = gensim.models.Word2Vec()
stop=time.time()
print "Loaded model in", (stop-start), "s"

with Pyro4.core.Daemon() as daemon:
    with Pyro4.naming.locateNS() as ns:
        uri = daemon.register(model)
        ns.register("word2vec", uri)
    # enter the service loop.
    print('word2vec is a', model)
    daemon.requestLoop()
