# word2vec

* A [Wired fluff piece](http://www.wired.com/2015/06/ais-next-frontier-machines-understand-language/) where Socher says:

>“The insight—and it’s almost trivial—is that every task in NLP is actually a question-and-answer task,” says Richard Socher.  The system does all this using what Socher calls “episodic memory.” If a neutral network is analogous to the cerebral cortex—the means of processing information—its episodic memory is something akin to hippocampus, which provides short-term memory in humans.... “You can’t do transitive reasoning without episodic memory,” Socher says.

* [Original project](https://code.google.com/p/word2vec/) from Google
* gensim looks like the most mature Python implementation
* gensim can be [installed](https://radimrehurek.com/gensim/install.html) with `pip install` but not all its dependencies can. I might have wanted to do this in a virtualenv.
* [Installing latest numpy / scipy on OSX](https://gist.github.com/goldsmith/7262122)
* basically using gensim for everything word2vec relateed
* Radim's [word2vec tutorial](http://rare-technologies.com/word2vec-tutorial/) for gensim
* [Plain language discussion of Hierarchical Softmax](https://yinwenpeng.wordpress.com/2013/09/26/hierarchical-softmax-in-neural-network-language-model/)
* Really nice [blog post](http://multithreaded.stitchfix.com/blog/2015/03/11/word-is-worth-a-thousand-vectors/) overviw of word2vec, including links to all kinds of resources.
* [Five crazy abstractions my word2vec model just did](http://byterot.blogspot.com/2015/06/five-crazy-abstractions-my-deep-learning-word2doc-model-just-did-NLP-gensim.html) -- this guy uses gensim, fwiw
* [Approximate nearest neighbor indexing](https://github.com/spotify/annoy) in C++/Python from Spotify
* Gensim _requires_ the 1.9.0 release of the Python `six` library, which doesn't `pip install`. [six.py github](https://github.com/kelp404/six)
* Loading the Google News model (from the word2vec project site) on my 2013 MacBook Air takes 7.5 minutes and occupies 2.5G of RAM. It does do some nice analogies but it is full of crazy and useless trigrams, which is probably why it's so huge.
* Note: had to hack gensim.model.Word2Vec.load_word2vec_format to instatiate the class by its self rather than the its name

```
# m=Word2Vec.load_word2vec_format('GoogleNews-vectors-negative300.bin.gz', binary=True)
# m.most_similar(positive=['San_Francisco', 'Minnesota'], negative=['California'], topn=1)
[(u'Minneapolis', 0.7336386442184448)]
```

### Other resources

* [Dependency-based word embeddings](https://levyomer.wordpress.com/2014/04/25/dependency-based-word-embeddings/) -- takes a different approach from skip-gram, includes code and models
* [Using GloVe vectors in gensim](http://tokestermw.github.io/posts/glove-vectors-gensim/)

## ipython

* `sudo easy_install readline` on OSX for god's sake, or [things will wrap weirdly](https://github.com/ipython/ipython/issues/3329/#issuecomment-18053861)