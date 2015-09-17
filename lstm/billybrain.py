from __future__ import with_statement, print_function
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
import numpy as np
import Pyro4
import time, logging, sys, re, os

path = sys.argv[1] #"t8.shakespeare.txt"
text = open(path).read() #.lower()
print('corpus length:', len(text))

chars = set(text)
print('total chars:', len(chars))
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))

# cut the text in semi-redundant sequences of maxlen characters
maxlen = 16

# build the model: 2 stacked LSTM
print('Build model...')
model = Sequential()
model.add(LSTM(len(chars), 512, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(512, 512, return_sequences=False))
model.add(Dropout(0.2))
model.add(Dense(512, len(chars)))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy', optimizer='rmsprop')

files = [f for f in os.listdir(".") if re.match(path + r'\.\d+\.hdf5$', f)]
if files:
    files.sort()
    w_file = files[-1]
    start_iteration = int(w_file.rsplit(".",2)[-2])
    print("Loading iteration #%d from %s..." % (start_iteration, w_file))
    model.load_weights(w_file)
else:
    raise Exception("Can't load weights for " + path)

# helper function to sample an index from a probability array
def sample(a, temperature=1.0):
    a = np.log(a)/temperature
    a = np.exp(a)/np.sum(np.exp(a))
    return np.argmax(np.random.multinomial(1,a,1))

class Billybrain(object):
    def predict_text(self, text, length, diversity=1.0):
        window = text
        generated = ""
        for i in range(length):
            x = np.zeros((1, maxlen, len(chars)))
            for t, char in enumerate(window):
                x[0, t, char_indices[char]] = 1.

            preds = model.predict(x, verbose=1)[0]
            next_index = sample(preds, diversity)
            next_char = indices_char[next_index]

            generated += next_char
            window = window[1:] + next_char
        return generated

with Pyro4.core.Daemon() as daemon:
    with Pyro4.naming.locateNS() as ns:
        uri = daemon.register(Billybrain())
        ns.register("billybrain", uri)
    daemon.requestLoop()
