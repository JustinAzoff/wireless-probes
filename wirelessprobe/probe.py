from wirelessprobe import fetch_wireless, fetch_download
def probe_ap(ip):
    combined = {'ip': ip}
    radio_info = {}
    info = fetch_wireless(ip)
    if info:
        #should be only one returned
        for it, stats in info.items():
            stats['interface'] = it
            combined.update(stats)
    info = fetch_download(ip)
    if info:
        combined.update(info)
    return combined
