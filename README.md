# Botwerk

_Botwerk_, in the sense of [a factory or a workshop](https://en.wiktionary.org/wiki/Werk#Noun), is meant to be a collection of techniques for managing language models and making generative text applications out of them. The code is all in Python for now, but whatever.

Right now the two working language models are character-based recurrent neural nets ("char-RNN" etc.), and a neural method for estimating term vectors in a distributed representation called word2vec. 

Botwerk also contains code for creating bot agents and connecting them both to language models and transport mechanisms. Right now the only transport supported is Slack, but I want to build that out ASAP: Twitter, IRC, Hangouts, I'll take other suggestions. 

Finally Botwerk has some code to make it convenient to spin up training runs on persistent EC2 spot requests, and for posting trained models to S3.

Botwerk is emphatically not ever intended to do anything useful. I want it to be a creative palette and a platform for developing intellectual curiosity.

## "Architecture"

The technical "design" of Botwerk conceives of bots as a set of networked
microservices, connecting language models on the backend with chat interfaces
on the front end (Slack to start, eventually IRC, Hangouts, Twitter, etc).
In between the two would typically sit a "core" microservice that provides the
"view" functionality (in the sense of a model-view-controller design).

Part of the motivation behind the microservice architecture is that language
models often take a long time to assemble and/or load into memory. By
separating out the model, view, and controller as RPC-linked services, the
"logic" of the chatbot can be tinkered on, without taking the bot's presence
offline, or necessitating a complete reload of its language models.

## "Implementation"

[Botwerk](https://github.com/schuyler/botwerk/) is presently a bunch of Python code gluing together
[Gensim](https://radimrehurek.com/gensim/) and [Keras](http://keras.io/) in a
way that can be incorporated into a
[Slack](https://github.com/slackhq/python-rtmbot) bot, using
[Pyro4](https://github.com/irmen/Pyro4) as the RPC layer (for now).

Absolutely all of this is subject to change.

## Contents

* `cores/` - individual bot view services
* `doc/` - notes on making bots in Python in the modern era
* `gpu/` - a junk drawer of stuff for making Theano work well on EC2 GPU instances
* `lstm/` - character-based RNN text models using Long Short Term Memory units with Keras
* `slack/` - controller code for Slackbots, includes a generic plugin for connecting to cores via Pyro4
* `spot/` - a bunch of stuff for training Keras models on EC2 spot instances
* `wikipedia/` - code for extracting text from Wikipedia dumps
* `word2vec/` - word2vec models using Gensim

## Installation

Strongly recommend using `virtualenv` and then simply running `pip install -r requirements.txt`. See `doc/install.md` for how I went about setting up the code on a fresh EC2 instance.


## License

Anything in this repo that identifiably came from somewhere is the property of
its creators and is provided here for convenience under its original license.

Everything else is copyright (c) 2015 Schuyler Erle, and is offered under the
MIT License, in the fervent hope that it will be entertaining:

> Permission is hereby granted, free of charge, to any person obtaining a copy of
> this software and associated documentation files (the "Software"), to deal in
> the Software without restriction, including without limitation the rights to
> use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
> of the Software, and to permit persons to whom the Software is furnished to do
> so, subject to the following conditions:
>
>The above copyright notice and this permission notice shall be included in all
> copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
> IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
>FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
> AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
> LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
> OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
> SOFTWARE.

-=- **PATCHES WELCOME** -=-
