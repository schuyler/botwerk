from __future__ import with_statement, print_function
import Pyro4
import numpy as np
import time, logging, sys, re

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

model = Pyro4.core.Proxy('PYRONAME:billybrain')

class Billybard(object):
    def tell(self, text):
        logging.info("< %s" % text)
        result = model.predict_text(text, 255, 0.2)
        logging.info("> %s" % result)
        return result

with Pyro4.core.Daemon() as daemon:
    with Pyro4.naming.locateNS() as ns:
        uri = daemon.register(Billybard())
        ns.register("billybard", uri)
    daemon.requestLoop()
