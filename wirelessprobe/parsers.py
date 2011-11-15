import re

def clean(s):
    """Strip off any dots and convert to an integer if possible"""
    x = s.strip(".")
    try :
        return int(x)
    except ValueError:
        return x

def parse_proc_net_wireless(txt):
    parsed = {}
    lines = txt.splitlines()
    #first two lines are headers
    data = lines[2:]
    for line in data:
        d = {}

        parts = line.split()
        it = parts[0].strip(":")
        d['link']  = clean(parts[2])
        d['level'] = clean(parts[3]) - 256
        d['noise'] = clean(parts[4]) - 256
        d['nwid']  = clean(parts[5])
        d['crypt'] = clean(parts[6])
        d['frag']  = clean(parts[7])
        d['retry'] = clean(parts[8])
        d['misc']  = clean(parts[9])
        d['missed_beacon'] = clean(parts[10])

        d['interface'] = it
        parsed[it]=d
    return parsed

def parse_download(txt):
    lines = txt.split("\n")
    #progress = [l for l in lines if "null" in l][0]
    #size = [word for word in progress.split() if word.endswith("k")][-1]
    #kilobytes = int(size.strip("k"))
    kilobytes = 4096

    real = [l for l in lines if l.startswith("real")][0]
    minutes, seconds = real[5:].split()
    minutes =   int(minutes.strip("m"))
    seconds = float(seconds.strip("s"))
    t = 60 * minutes + seconds
    return {'time': t, 'kilobytes': kilobytes}

def maybe_int(s):
    if '.' in s:
        func = float
    else:
        func = int

    try:
        return func(s)
    except ValueError:
        return s

def parse_scan_result(txt):
    lines = txt.split("\n")
    aps = {}
    for line in lines:
        if not line.strip(): continue
        if line.startswith("bssid"): continue
        if line.startswith("Selected interface"): continue

        parts = line.split("\t")
        parts = [maybe_int(s) for s in parts]
        while len(parts)!= 5:
            parts.append(None)
            
        bssid, frequency, signal, flags, ssid = parts
        aps[bssid] = dict(bssid=bssid, frequency=frequency, signal=signal, flags=flags, ssid=ssid)
    return aps

def parse_status(txt):
    lines = txt.strip().split("\n")
    ret = {}
    for line in lines:
        key, value = line.split("=")
        ret[key] = value
    return ret

def parse_ping(txt):
    lines = txt.strip().split("\n")
    transmitted_line = [x for x in lines if 'transmitted' in x][0]
    stats_line = [x for x in lines if 'min/avg' in x][0]

    #5 packets transmitted, 5 received, 0% packet loss, time 4006ms
    stats = re.match("(?P<sent>\d+) packets transmitted, (?P<received>\d+) received, (?P<loss>\d+)% packet loss,", transmitted_line).groupdict()

    #rtt min/avg/max/mdev = 9.363/11.902/15.020/2.061 ms, pipe 2
    parts = re.split("[ /]", stats_line.split(" = ")[1])
    stats['min'] = parts[0]
    stats['avg'] = parts[1]
    stats['max'] = parts[2]
    stats['mdev'] = parts[3]


    for k,v in stats.items():
        stats[k] = maybe_int(v)


    return stats
