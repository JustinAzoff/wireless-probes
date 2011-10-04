from subprocess import Popen, PIPE
from wirelessprobe import parsers

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

def is_alive(address, count=1):
    ret = ping(address, count)
    try :
        return ret['received'] > 0
    except PingError:
        return False
