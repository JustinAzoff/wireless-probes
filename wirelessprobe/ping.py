from subprocess import Popen, PIPE
from wirelessprobe import parsers

import time
import logging
logger = logging.getLogger(__name__)

class PingError(Exception):
    pass

def ping(address, count):
    output = Popen(["ping", "-c", str(count), address], stdout=PIPE).communicate()[0]
    try :
        return parsers.parse_ping(output)
    except:
        raise PingError

def is_alive(address, retries=3):
    for _ in range(retries):
        try :
            ret = ping(address, 1)
            if ret['received'] > 0:
                return True
        except PingError:
            continue
        time.sleep(1)
    return False
