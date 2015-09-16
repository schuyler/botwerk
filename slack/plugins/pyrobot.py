import Pyro4
import time, logging, re
crontable = []
outputs = []

bot_name = "annalogue"
bot = Pyro4.core.Proxy('PYRONAME:' + bot_name)
bot_uid = "U0AJBPH7X"
mention = re.compile(r'^\s*<@' + bot_uid + r'>\W+?', re.IGNORECASE)
print mention

def process_message(data):
    if not 'text' in data: return
    if data['channel'].startswith("D") or mention.match(data['text']):
        print repr(data)
        data['text'] = mention.sub("", data["text"])
        retry = True
        while retry:
            retry = False
            try:
                if not 'text' in data: return
                response = bot.tell(data['text'])
                if response:
                    outputs.append([data['channel'], response])
            except Pyro4.errors.ConnectionClosedError:
                time.sleep(1.0)
                retry = True
            except:
                logging.exception("pyrobot")
                outputs.append([data['channel'], ":cry:"])
