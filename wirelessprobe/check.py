from wirelessprobe import get_ip
from wirelessprobe import wpa_cli
from wirelessprobe import do_download
from wirelessprobe import ping
from wirelessprobe.ping import PingError
from wirelessprobe.util import make_stats
import IPy

import datetime
import logging
import sys
logger = logging.getLogger(__name__)

def check_ssid(ssid, interface, **kwargs):
    logger.debug("Checking signal")
    access_points = wpa_cli.scan_result(interface)
    this_ssid = [ap for ap in access_points.values() if ap['ssid'] == ssid]
    stats = make_stats([x['signal'] for x in this_ssid])
    stats["aps"] = len(this_ssid)
    stats["ok"] = len(this_ssid) >= 1
    return stats

check_ssid.format = "check=AP ok=%(ok)s aps=%(aps)d min_signal=%(min)d avg_signal=%(avg)d max_signal=%(max)d"


def check_wpa(ssid, interface, **kwargs):
    wpa_status = wpa_cli.status(interface)
    wpa_status["ok"] = wpa_status['wpa_state'] == "COMPLETED" and wpa_status['EAP state'] == "SUCCESS" and wpa_status['ssid'] == ssid
    return wpa_status

check_wpa.format = "check=WPA ok=%(ok)s wpa_state=%(wpa_state)s supplicant_state=%(Supplicant PAE state)s eap_state=%(EAP state)s"


def check_ip(interface, wireless_netblocks, **kwargs):
    try:
        ip = get_ip(interface)
    except IOError:
        return dict(ok=False, ip="")

    for net in wireless_netblocks.split(","):
        if ip in IPy.IP(net):
            return dict(ok=True, ip=ip)
    return dict(ok=False, ip=ip)

check_ip.format = "check=IP ok=%(ok)s ip=%(ip)s"


def check_ping(ping_host, ping_count, **kwargs):
    try :
        stats = ping(ping_host, ping_count)
    except PingError:
        return dict(ok=False, error=True)

    stats['ok'] = stats['loss'] < 4
    return stats

check_ping.format = "check=PING ok=%(ok)s sent=%(sent)d received=%(received)d loss=%(loss)d min=%(min).2f avg=%(avg).2f max=%(max).2f"
check_ping.alt_format = "check=PING ok=%(ok)s error=%(error)s"
check_ping.alt_key = "error"


def check_download(url, url_timeout, **kwargs):
    stats = do_download(url, url_timeout)
    stats["ok"] = not stats['timeout'] and not stats['exception']
    return stats

check_download.format = "check=DL ok=%(ok)s elapsed=%(elapsed).2f timeout=%(timeout)s min_speed=%(min)d avg_speed=%(avg)d max_speed=%(max)d"
check_download.alt_format = "check=DL ok=%(ok)s exception='%(exception)s'"
check_download.alt_key = "exception"


def check_wireless(**config):


    for func in check_ssid, check_wpa, check_ip, check_ping, check_download:
        stats = func(**config)
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if getattr(func, 'alt_key', 'mooo') in stats and stats[func.alt_key]:
            print now, func.alt_format % stats
        else:
            print now, func.format % stats
        sys.stdout.flush()

def main():
    import sys
    import ConfigParser
    from wirelessprobe.parsers import maybe_int
    cfile = sys.argv[1]
    config = ConfigParser.ConfigParser()
    config.read(cfile)
    configuration = dict(config.items("probe"))
    for k,v in configuration.items():
        configuration[k] = maybe_int(v)
    check_wireless(**configuration)
