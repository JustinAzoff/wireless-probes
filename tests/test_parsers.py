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

status_out = \
"""bssid=00:17:df:ab:1f:71
ssid=UA_WPA
id=0
pairwise_cipher=CCMP
group_cipher=TKIP
key_mgmt=WPA2/IEEE 802.1X/EAP
wpa_state=COMPLETED
ip_address=192.168.2.3
Supplicant PAE state=AUTHENTICATED
suppPortStatus=Authorized
EAP state=SUCCESS
selectedMethod=25 (EAP-PEAP)
EAP TLS cipher=DHE-RSA-AES256-SHA
EAP-PEAPv0 Phase2 method=MSCHAPV2
"""

def test_parse_status():
    parsed = parsers.parse_status(status_out)
    assert parsed['EAP state'] == 'SUCCESS'
    assert parsed['wpa_state'] == 'COMPLETED'

ping_out = \
"""(test)root@probe1:/tmp# ping -c 5 192.168.1.1
PING 192.168.1.1 (192.168.1.1) 56(84) bytes of data.
64 bytes from 192.168.1.1: icmp_req=1 ttl=255 time=1.93 ms
64 bytes from 192.168.1.1: icmp_req=2 ttl=255 time=1.61 ms
64 bytes from 192.168.1.1: icmp_req=3 ttl=255 time=2.21 ms
64 bytes from 192.168.1.1: icmp_req=4 ttl=255 time=2.84 ms
64 bytes from 192.168.1.1: icmp_req=5 ttl=255 time=5.34 ms

--- 192.168.1.1 ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 4006ms
rtt min/avg/max/mdev = 1.617/2.790/5.346/1.341 ms, pipe 2
"""

def test_parse_ping():
    parsed = parsers.parse_ping(ping_out)
    assert parsed['sent'] == 5
    assert parsed['received'] == 5
    assert parsed['loss'] == 0
    assert parsed['min'] == 1.617
    assert parsed['avg'] == 2.790
    assert parsed['max'] == 5.346
    assert parsed['mdev'] == 1.341
