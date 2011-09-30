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
    try:
        return int(s)
    except ValueError:
        return s

def parse_scan_result(txt):
    lines = txt.split("\n")
    aps = {}
    for line in lines:
        if line.startswith("bssid"): continue

        parts = line.split("\t")
        parts = [maybe_int(s) for s in parts]
        while len(parts)!= 5:
            parts.append(None)
            
        bssid, frequency, signal, flags, ssid = parts
        aps[bssid] = dict(bssid=bssid, frequency=frequency, signal=signal, flags=flags, ssid=ssid)
    return aps
