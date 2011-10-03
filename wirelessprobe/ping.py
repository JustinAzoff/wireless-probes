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
