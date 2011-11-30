from wirelessprobe import get_ip
from wirelessprobe import wpa_cli
from wirelessprobe import do_download
from wirelessprobe import ping, is_alive
from wirelessprobe import connect, disconnect
from wirelessprobe.ping import PingError
from wirelessprobe.util import make_stats
from wirelessprobe.parsers import maybe_int
import IPy

import time
import datetime
import logging
import sys
import ConfigParser
logger = logging.getLogger(__name__)

class Checker:
    def __init__(self, configuration):
        self.disconnect_before_checks = False
        self.connect_offset = 0
        self.config = configuration
        for k,v in configuration.items():
            setattr(self, k, v)

    def check_ssid(self):
        logger.debug("Checking signal")
        access_points = wpa_cli.scan_result(self.interface)
        this_ssid = [ap for ap in access_points.values() if ap['ssid'] == self.ssid]
        stats = make_stats([x['signal'] for x in this_ssid])
        stats["aps"] = len(this_ssid)
        stats["ok"] = len(this_ssid) >= 1
        return stats

    check_ssid.format = "check=AP ok=%(ok)s aps=%(aps)d min_signal=%(min)d avg_signal=%(avg)d max_signal=%(max)d"
    check_ssid.name = "AP"

    def check_connect(self):
        if not is_alive(self.ping_host, 2):
            disconnect(self.interface)
            stats = connect(self.interface)
            stats["connect_time"] -= self.connect_offset # account for firmware delays
            stats["ok"] = stats["connect_time"] < 30
        else:
            stats = dict(ok=True, already=True)
        return stats

    check_connect.format = "check=Connect ok=%(ok)s connect_time=%(connect_time)d"
    check_connect.alt_format = "check=Connect ok=%(ok)s already_connected=True"
    check_connect.alt_key = "already"
    check_connect.name = "Connect"
    
    def check_wpa(self):
        wpa_status = wpa_cli.status(self.interface)
        wpa_status["ok"] = wpa_status['wpa_state'] == "COMPLETED" and wpa_status['EAP state'] == "SUCCESS" and wpa_status['ssid'] == self.ssid
        return wpa_status

    check_wpa.format = "check=WPA ok=%(ok)s wpa_state=%(wpa_state)s supplicant_state=%(Supplicant PAE state)s eap_state=%(EAP state)s bssid=%(bssid)s"
    check_wpa.name = "WPA"

    def check_ip(self):
        try:
            ip = get_ip(self.interface)
        except IOError:
            return dict(ok=False, ip="")

        for net in self.wireless_netblocks.split(","):
            if ip in IPy.IP(net):
                return dict(ok=True, ip=ip)
        return dict(ok=False, ip=ip)

    check_ip.format = "check=IP ok=%(ok)s ip=%(ip)s"
    check_ip.name = "IP"

    def check_connectivity(self):
        is_connected = is_alive(self.ping_host, 3)
        return dict(ok=is_connected)
    check_connectivity.format = "check=CONN ok=%(ok)s"
    check_connectivity.name = "CONN"

    def check_ping(self):
        try :
            stats = ping(self.ping_host, self.ping_count)
        except PingError:
            return dict(ok=False, error=True)

        stats['ok'] = stats['loss'] < 4
        return stats

    check_ping.format = "check=PING ok=%(ok)s sent=%(sent)d received=%(received)d packet_loss=%(loss)d min_rtt=%(min).2f avg_rtt=%(avg).2f max_rtt=%(max).2f"
    check_ping.alt_format = "check=PING ok=%(ok)s error=%(error)s"
    check_ping.alt_key = "error"
    check_ping.name = "PING"


    def check_download(self):
        stats = do_download(self.url, self.url_timeout)
        stats["ok"] = not stats['timeout'] and not stats['exception']
        stats['failed'] = not stats['ok']
        return stats

    check_download.format = "check=DL ok=%(ok)s download_time=%(elapsed).2f timeout=%(timeout)s min_speed=%(min)d avg_speed=%(avg)d max_speed=%(max)d"
    check_download.alt_format = "check=DL ok=%(ok)s timeout=%(timeout)s kbytes=%(kbytes)d exception='%(exception)s'"
    check_download.alt_key = "failed"
    check_download.name = "DL"

    all_checks = [
        check_connect,
        check_ssid,
        check_wpa,
        check_ip,
        check_connectivity,
        check_download,
        check_ping,
    ]

    def run_checks(self):
        if self.disconnect_before_checks:
            disconnect(self.interface)
        for func in self.all_checks:
            time.sleep(2)
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try :
                stats = func(self)
                if getattr(func, 'alt_key', 'mooo') in stats and stats[func.alt_key]:
                    print now, func.alt_format % stats
                else:
                    print now, func.format % stats
            except Exception, e:
                import traceback
                traceback.print_exc(file=sys.stderr)
                print now, "check=%s ok=False exception='%s'" % (func.name, e)
            sys.stdout.flush()

    @classmethod
    def from_ini(self, config_file):
        config = ConfigParser.ConfigParser()
        config.read(config_file)
        configuration = dict(config.items("probe"))
        for k,v in configuration.items():
            configuration[k] = maybe_int(v)
        return Checker(configuration)

def main():
    cfile = sys.argv[1]
    checker = Checker.from_ini(cfile)
    checker.run_checks()
