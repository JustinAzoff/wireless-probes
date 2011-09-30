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
    assert parsed['kilobytes'] == 4096

def test_parse_download_minute():
    parsed = parsers.parse_download(dl_out2)
    assert parsed['time'] == 64.13
    assert parsed['kilobytes'] == 4096


scan_result_out = \
"""bssid / frequency / signal level / flags / ssid
00:1f:6d:b9:6c:42	2412	204	[WPA-EAP-TKIP][WPA2-EAP-TKIP+CCMP]	UA_WPA
00:17:df:ab:1f:73	2462	204	[WPA-EAP-TKIP][WPA2-EAP-TKIP+CCMP]	
00:17:df:ab:1f:71	2462	198	[WPA-EAP-TKIP][WPA2-EAP-TKIP+CCMP]	UA_WPA
00:1f:6d:b9:85:12	2437	188	[WPA-EAP-TKIP][WPA2-EAP-TKIP+CCMP]	UA_WPA
c4:7d:4f:88:4a:24	2437	180	[WPA2-PSK-CCMP] THOR
00:1f:6d:b9:6c:45	2412	206		UAAthletics
00:1f:6d:b9:6c:41	2412	204		
00:1f:6d:b9:6c:46	2412	204		UAGuest
00:1f:6d:b9:6c:47	2412	204		UAWirelessHelp
00:17:df:ab:1f:72	2462	204		
00:17:df:ab:1f:75	2462	198		UAAthletics
00:17:df:ab:1f:70	2462	198		UAGuest
00:1f:6d:b9:85:11	2437	190		
00:1f:6d:b9:85:16	2437	188		UAGuest
00:1f:6d:b9:85:17	2437	187		UAWirelessHelp
00:1f:6d:b9:85:15	2437	187		UAAthletics
"""

def test_parse_scan_result():
    parsed = parsers.parse_scan_result(scan_result_out)
    assert parsed["00:1f:6d:b9:6c:42"]["signal"] == 204
    assert parsed["00:1f:6d:b9:6c:42"]["ssid"] == "UA_WPA"
