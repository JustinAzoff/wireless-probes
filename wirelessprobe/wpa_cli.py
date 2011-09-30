from subprocess import Popen, PIPE

from wirelessprobe import parsers

def scan_result():
    output = Popen(["wpa_cli", "scan_result"], stdout=PIPE).communicate()[0]
    return parsers.parse_scan_result(output)
