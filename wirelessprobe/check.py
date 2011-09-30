from wirelessprobe import get_ip
from wirelessprobe import wpa_cli
from wirelessprobe import do_download
from wirelessprobe.util import make_stats

import logging
logger = logging.getLogger(__name__)

def check_ssid(ssid):
    logger.debug("Checking signal")
    access_points = wpa_cli.scan_result()
    this_ssid = [ap for ap in access_points.values() if ap['ssid'] == ssid]
    stats = make_stats([x['signal'] for x in this_ssid])
    stats["aps"] = len(this_ssid)
    return stats

def check_ip(interface):
    try:
        ip = get_ip(interface)
        return ip not in ("", "0.0.0.0")
    except IOError:
        return False

def check_download(url, timeout):
    stats = do_download(url, timeout)
    return stats
    
def check_wireless(ssid, interface=None):
    if not interface:
        interface = open("/etc/wireless_interface.conf").read().strip()

    ap_stats = check_ssid(ssid)
    print "AP stats", ap_stats

    print "IP address", check_ip(interface)

    dl_stats = check_download("http://www.example.com/20m", 30)
    print "DL stats", dl_stats


def main():
    import sys
    ssid = sys.argv[1]
    check_wireless(ssid)
