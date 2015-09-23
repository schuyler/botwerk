# Notes on RNNs etc.


## char-rnn

* ["The Unreasonable Effectiveness of Recurrent Neural Networks"](http://karpathy.github.io/2015/05/21/rnn-effectiveness/)
* [Lua code in Github](https://github.com/karpathy/char-rnn)
* [Project page](http://cs.stanford.edu/people/karpathy/char-rnn/)
* [The numpy prototype](https://gist.github.com/karpathy/d4dee566867f8291f086) which is probably worth understanding.


The blog post is great. The actual *char-rnn* code is based on Torch, which is written in (argh) Lua. Someone even went so far as to write a [JSON server in Python](https://github.com/samim23/char-rnn-api) to get around the fact that... it's Lua.

> If training vanilla neural nets is optimization over functions, training recurrent nets is optimization over programs.

However:

> ... in practice most of us use a slightly different formulation than what I presented above called a Long Short-Term Memory (LSTM) network. The LSTM is a particular type of recurrent network that works slightly better in practice, owing to its more powerful update equation and some appealing backpropagation dynamics.

## Chainer

* Python framework for deep learning
* [Website](http://chainer.org/) and [Github](https://github.com/pfnet/chainer)
* [chainer-char-rnn](https://github.com/yusuketomoto/chainer-char-rnn) was how I found Chainer -- an implementation of *char-rnn* in Python.
* This was kind of appealing in principle but the API isn't nearly as nice as Keras's. OTOH, that chainer-char-rnn code is 50 lines.

## Keras

* Theano-based Deep Learning library (convnets, recurrent neural networks, and more).
* [Website](http://keras.io/) and [Github](https://github.com/fchollet/keras)
* The syntax is nice and Pythonic but the API is compositional and Torch-like.
* [haiku_rnn](https://github.com/napsternxg/haiku_rnn) is an unreasonably charming effort to generate haiku with an RNN.
* Installing Keras was tricky as it wanted to install HDF5, which dependend on a system library for which the formula in Homebrew was broken (the given version was missing, not the most recent, and the formula guessed the version number wrong so I had to explicitly declare it in a `version` directive). I need to send an upstream patch to Homebrew.

## Passage

* A little library for text analysis with RNNs. "Warning: Very alpha, work in progress."
* [Github](https://github.com/IndicoDataSolutions/Passage)
* Has an API at least as nice as Keras, and is designed for text processing.

## GPUs on EC2s

* [Install Theano on AWS](http://markus.com/install-theano-on-aws/) -- Keras depends on Theano, so.
* [NVIDIA GPU kernel module tuning](http://techblog.netflix.com/2014/02/distributed-neural-networks-with-gpus.html) -- seems to make a big difference, if Netflix's numbers are to be believed. Also this article is a year and a half old. In practice it doesn't seem to make a difference on the current g2.2xlarges.
* [Install OpenBLAS](http://www.stat.cmu.edu/~nmv/2013/07/09/for-faster-r-use-openblas-instead-better-than-atlas-trivial-to-switch-to-on-ubuntu/) as it is supposed to be a lot faster than the stock libblas.

## Data sources

* Wikipedia plain text could be generated using [wikipedia-extractor](https://github.com/bwbaugh/wikipedia-extractor). You know, it's about goddamn time this exists.
* 