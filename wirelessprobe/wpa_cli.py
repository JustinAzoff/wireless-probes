from subprocess import Popen, PIPE
import time

from wirelessprobe import parsers

import logging
logger = logging.getLogger(__name__)


def scan_result(interface):
    logger.debug("Scanning %s", interface)
    output = Popen(["wpa_cli", "-i", interface, "scan"], stdout=PIPE).communicate()[0]
    time.sleep(3)
    output = Popen(["wpa_cli", "-i", interface, "scan_result"], stdout=PIPE).communicate()[0]
    return parsers.parse_scan_result(output)

def status(interface):
    output = Popen(["wpa_cli", "-i", interface, "status"], stdout=PIPE).communicate()[0]
    data = parsers.parse_status(output)
    if "bssid" not in data:
        data["bssid"]=""
    return data
