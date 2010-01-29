from wirelessprobe import parsers

out="Inter-| sta-|   Quality        |   Discarded packets               | Missed | WE\n" \
    " face | tus | link level noise |  nwid  crypt   frag  retry   misc | beacon | 18\n" \
    "   wl0: 0000    4.  193.  160.       1      2      3     20      4        9\n" \

def test_proc_net_wireless():
    parsed = parsers.parse_proc_net_wireless(out)
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

dl_out1 = "null                 100% |*******************************|  4096k 00:00:00 ETA\n" \
          "real    0m 2.93s\n" \
          "user    0m 0.06s\n" \
          "sys     0m 2.36s\n"

dl_out2 = "null                 100% |*******************************|  4096k 00:00:00 ETA\n" \
          "real    1m 4.13s\n" \
          "user    0m 0.06s\n" \
          "sys     0m 2.36s\n"

def test_parse_download():
    parsed = parsers.parse_download(dl_out1)
    assert parsed['time'] == 2.93

def test_parse_download_minute():
    parsed = parsers.parse_download(dl_out2)
    assert parsed['time'] == 64.13
