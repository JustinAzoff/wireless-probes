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
