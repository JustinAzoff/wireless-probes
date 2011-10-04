from subprocess import Popen, PIPE
import time
import os

from wirelessprobe import parsers

import logging
logger = logging.getLogger(__name__)

def run(cmd):
    output = Popen(cmd, stdout=PIPE).communicate()[0]
    return output

def disconnect(interface):
    run(["ifdown", interface])
    run(["ifconfig", interface, "0.0.0.0"])
    run(["ifconfig", interface, "down"])
    run(["pkill", "wpa_supplicant"])
    run(["pkill", "dhclient"])

    os.unlink("/var/lib/dhcp/dhclient.%s.leases" % interface)

def connect(interface):
    logger.debug("Connecting to %s", interface)

    stats = {}
    start = time.time()
    output = run(["ifup", interface])
    end = time.time()

    stats['elapsed'] = end - start
    return stats
