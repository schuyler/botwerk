from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM

import numpy as np
import random, re, os, logging, time, sys
import yaml, zipfile, simples3, io, shutil

def show_timing(method):
    def wrapped(*args, **kwargs):
        start = time.time()
        logging.info("Starting %s", method.__name__)
        result = method(*args, **kwargs) 
        logging.info("Leaving %s (%.2fs elapsed)", method.__name__, time.time() - start)
        return result
    return wrapped

class CharLSTM(object):
    def __init__(self, path, seq_len=20, step=3):
        self.path = path
        self.sequence_length = seq_len
        self.sequence_step = step
        self.iteration = 0

    @show_timing
    def load_text(self):
        self.text = text = open(self.path).read() #.lower()
        logging.info('corpus length: %d', len(self.text))

        self.chars = list(set(text))
        self.chars.sort()
        logging.info('total chars: %d', len(self.chars))
        self.char_indices = dict((c, i) for i, c in enumerate(self.chars))

    @show_timing
    def generate_char_sequences(self):
        # cut the text in semi-redundant sequences of self.sequence_length characters
        self.sentences = []
        self.next_chars = []
        for i in range(0, len(self.text) - self.sequence_length, self.sequence_step):
            self.sentences.append(self.text[i : i + self.sequence_length])
            self.next_chars.append(self.text[i + self.sequence_length])
        logging.info('nb sequences: %d', len(self.sentences))

    def build_training_vectors(self, mode):
        X = np.memmap(self.path + ".example", mode=mode, shape=(len(self.sentences), self.sequence_length, len(self.chars)), dtype=np.bool)
        y = np.memmap(self.path + ".expect", mode=mode, shape=(len(self.sentences), len(self.chars)), dtype=np.bool)
        return X, y

    @show_timing
    def generate_training_vectors(self):
        if os.path.isfile(self.path + ".example"):
            mode = "r"
        else:
            mode = "w+"
        X, y = self.build_training_vectors(mode)
        if mode != "r":
            for i, sentence in enumerate(self.sentences):
                for t, char in enumerate(sentence):
                    X[i, t, self.char_indices[char]] = 1
                y[i, self.char_indices[self.next_chars[i]]] = 1
            # save and re-open
            del X
            del y
            X, y = self.build_training_vectors("r")
        self.X = X
        self.y = y

    @show_timing
    def build_model(self):
        self.model = Sequential()
        self.model.add(LSTM(len(self.chars), 512, return_sequences=True))
        self.model.add(Dropout(0.2))
        self.model.add(LSTM(512, 512, return_sequences=False))
        self.model.add(Dropout(0.2))
        self.model.add(Dense(512, len(self.chars)))
        self.model.add(Activation('softmax'))

        self.model.compile(loss='categorical_crossentropy', optimizer='rmsprop')

    def find_latest_checkpoint(self):
        dirname = os.path.dirname(self.path) or "."
        files = [f for f in os.listdir(dirname) if re.match(self.path + r'\.\d+\.hdf5$', f)]
        if files:
            files.sort()
            return files[-1]
        else:
            return None

    @show_timing
    def load_model_weights(self):
        w_file = self.find_latest_checkpoint()
        if w_file:
            self.iteration = int(w_file.rsplit(".",2)[-2])
            logging.info("Loading iteration #%d from %s...", self.iteration, w_file)
            self.model.load_weights(w_file)
        else:
            logging.info("Starting from scratch...")

    @show_timing
    def save_model_weights(self):
        w_file = "%s.%03d.hdf5" % (self.path, self.iteration)
        self.model.save_weights(w_file)
        return w_file

    # helper function to sample an index from a probability array
    def sample(self, a, temperature=1.0):
        a = np.log(a)/temperature
        a = np.exp(a)/np.sum(np.exp(a))
        return np.argmax(np.random.multinomial(1,a,1))

    @show_timing
    def train_iteration(self):
        self.iteration += 1
        logging.info('Training iteration #%d', self.iteration)
        self.model.fit(self.X, self.y, batch_size=128, nb_epoch=1)

    def sample_output(self):
        start_index = random.randint(0, len(self.text) - self.sequence_length - 1)
        for diversity in [0.2, 0.5, 1.0, 1.2]:
            print()
            print('----- diversity:', diversity)

            generated = ''
            sentence = self.text[start_index : start_index + self.sequence_length]
            generated += sentence
            print('----- Generating with seed: "' + sentence + '"')
            sys.stdout.write(generated)

            for c in range(400):
                x = np.zeros((1, self.sequence_length, len(self.chars)))
                for t, char in enumerate(sentence):
                    x[0, t, self.char_indices[char]] = 1.

                preds = self.model.predict(x, verbose=0)[0]
                next_index = self.sample(preds, diversity)
                next_char = self.chars[next_index]

                generated += next_char
                sentence = sentence[1:] + next_char

                sys.stdout.write(next_char)
                sys.stdout.flush()
            print()

    def run_training(self, archiver=None):
        self.load_text()
        self.generate_char_sequences()
        self.generate_training_vectors()
        self.build_model()
        self.load_model_weights()
        while True:
            self.train_iteration()
            if archiver:
                archiver.put(self)
            else:
                self.save_model_weights()
            self.sample_output()

class Archiver(object):
    def __init__(self, config):
        if type(config) is not dict:
            config = yaml.load(open(config).read())
        self.bucket = simples3.bucket.S3Bucket(config["bucket"],
                access_key=config["access_key"],
                secret_key=config["secret_key"])
        self.dataset = config["dataset"]

    def text(self):
        self.get()
        return self.dataset + ".txt"

    @show_timing
    def get(self):
        s3_file = self.bucket.get(self.dataset + ".zip")
        buf = io.BytesIO()
        shutil.copyfileobj(s3_file, buf)
        zip_file = zipfile.ZipFile(buf)
        zip_file.extractall()

    @show_timing
    def put(self, model):
        latest = model.save_model_weights()
        buf = io.BytesIO()
        zip_file = zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED)
        zip_file.write(self.dataset + ".txt")
        zip_file.write(latest)
        zip_file.close()
        buf.seek(0)
        self.bucket.put(self.dataset + ".zip", buf.read())

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    archiver = Archiver(sys.argv[1])
    model = CharLSTM(archiver.text())
    model.run_training(archiver)
