Wireless Probes
===============

Generate test results and metrics for wireless networks. The output is designed
to be forwarded into splunk, but it would be possible to modify things a bit to
insert data into a different system.

It outputs something like this:

    2011-11-15 16:53:11 check=Connect ok=True connect_time=6
    2011-11-15 16:53:19 check=AP ok=True aps=3 min_signal=188 avg_signal=200 max_signal=207
    2011-11-15 16:53:24 check=WPA ok=True wpa_state=COMPLETED supplicant_state=AUTHENTICATED eap_state=SUCCESS bssid=00:1f:6d:b9:6c:42
    2011-11-15 16:53:26 check=IP ok=True ip=192.168.1.101
    2011-11-15 16:53:28 check=DL ok=True download_time=11.46 timeout=False min_speed=1664 avg_speed=1786 max_speed=1864
    2011-11-15 16:53:41 check=PING ok=True sent=300 received=298 packet_loss=0 min_rtt=1.17 avg_rtt=12.13 max_rtt=288.18

It runs the following tests:

Connect
-------

Either a no-op, or times how long it takes for 'ifup wlan0' to run.

AP
--

Logs number of access points visible and signal strength

WPA
---

Logs the status of wpa_supplicant

IP
--

Logs the IP Address received from DHCP, verifies that it is in the expectect subnet.

DL
--

Downloads a file over http

PING
----
Pings an address
