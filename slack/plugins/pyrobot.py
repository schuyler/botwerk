import Pyro4
import time, logging, re
crontable = []
outputs = []
config = {}

def setup():
    bot_name = config["name"]
    bot_uid = config["user_id"]
    config["bot"] = Pyro4.core.Proxy('PYRONAME:' + bot_name)
    config["mention"] = re.compile(r'^\s*<@' + bot_uid + r'>\W+?', re.IGNORECASE)
    print "pyrobot setup:", config

def process_message(data):
    if not 'text' in data: return
    if data['channel'].startswith("D") or config["mention"].match(data['text']):
        print repr(data)
        data['text'] = config["mention"].sub("", data["text"])
        retry = True
        while retry:
            retry = False
            try:
                if not 'text' in data: return
                response = config["bot"].tell(data['text'])
                if response:
                    outputs.append([data['channel'], response])
            except Pyro4.errors.ConnectionClosedError:
                time.sleep(1.0)
                retry = True
            except:
                logging.exception("pyrobot")
                outputs.append([data['channel'], ":cry:"])
