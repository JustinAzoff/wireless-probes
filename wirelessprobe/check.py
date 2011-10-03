from wirelessprobe import get_ip
from wirelessprobe import wpa_cli
from wirelessprobe import do_download
from wirelessprobe.util import make_stats

import logging
logger = logging.getLogger(__name__)

def check_ssid(ssid, interface):
    logger.debug("Checking signal")
    access_points = wpa_cli.scan_result(interface)
    this_ssid = [ap for ap in access_points.values() if ap['ssid'] == ssid]
    stats = make_stats([x['signal'] for x in this_ssid])
    stats["aps"] = len(this_ssid)
    stats["ok"] = len(this_ssid) >= 1
    return stats

def check_wpa(ssid, interface):
    wpa_status = wpa_cli.status(interface)
    wpa_status["ok"] = wpa_status['wpa_state'] == "COMPLETED" and wpa_status['EAP state'] == "SUCCESS" and wpa_status['ssid'] == ssid
    return wpa_status

def check_ip(interface):
    try:
        ip = get_ip(interface)
        ok = ip not in ("", "0.0.0.0")
        return dict(ok=ok, ip=ip)
    except IOError:
        return dict(ok=False, ip="")
    
def check_wireless(ssid, interface=None):
    if not interface:
        interface = open("/etc/wireless_interface.conf").read().strip()

    ap_stats = check_ssid(ssid, interface)
    print "AP stats ok=%(ok)s aps=%(aps)d min_signal=%(min)d avg_signal=%(avg)d max_signal=%(max)d" % ap_stats

    wpa_status = check_wpa(ssid, interface)
    print "WPA stats ok=%(ok)s wpa_state=%(wpa_state)s supplicant_state=%(Supplicant PAE state)s eap_state=%(EAP state)s" % wpa_status

    ip_stats = check_ip(interface)
    print "IP address ok=%(ok)s ip=%(ip)s" % ip_stats

    dl_stats = do_download("http://www.example.com/20m", 30)
    print "DL stats ok=%(ok)s elapsed=%(elapsed).2f min_speed=%(min)d avg_speed=%(avg)d max_speed=%(max)d" % dl_stats


def main():
    import sys
    ssid = sys.argv[1]
    check_wireless(ssid)
