from wirelessprobe import proc

out="Inter-| sta-|   Quality        |   Discarded packets               | Missed | WE\n" \
    " face | tus | link level noise |  nwid  crypt   frag  retry   misc | beacon | 18\n" \
    "   wl0: 0000    4.  193.  160.       1      2      3     20      4        9\n" \

def test_proc_net_wireless():
    parsed = proc.parse_proc_net_wireless(out)
    assert 'wl0' in parsed
    it = parsed['wl0']
    print it
    assert it['link'] == 4
    assert it['level'] == -63
    assert it['noise'] == -96

    assert it['nwid'] == 1
    assert it['crypt'] == 2
    assert it['frag'] == 3
    assert it['retry'] == 20
    assert it['misc'] == 4
    assert it['missed_beacon'] == 9
