from wirelessprobe import parsers
import httplib2

def fetch_wireless(ip):
    h = httplib2.Http(timeout=1)
    resp, content = h.request("http://%s/cgi-bin/wireless" % ip)
    if resp['status']=='200':
        return parsers.parse_proc_net_wireless(content)

def fetch_download(ip):
    h = httplib2.Http(timeout=30)
    resp, content = h.request("http://%s/cgi-bin/download" % ip)
    if resp['status']=='200':
        return parsers.parse_download(content)
