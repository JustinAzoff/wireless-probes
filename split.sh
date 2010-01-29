get_ip () {
    IF=$1
    IP=`ifconfig $IF | grep inet|cut -d : -f 2|cut -d " " -f 1`
    echo $IP
}

get_net () {
    IF=$1
    NET=`ip addr show $IF |grep inet|cut -d t -f 2|cut -d ' ' -f 2`
    #convert 1.2.3.4/xx to 1.2.3.0/xx
    echo $NET|sed "s/[0-9]*\//0\//"
}

get_gateway () {
    IF=$1
    NET=`ip addr show $IF |grep inet|cut -d t -f 2|cut -d ' ' -f 2`
    #convert 1.2.3.4/xx to 1.2.3.1
    echo $NET | sed "s/[0-9]*\/.*/1/"
}

IF1=eth0.1
IF2=wl0

IP1=`get_ip $IF1`
IP2=`get_ip $IF2`

P1_NET=`get_net $IF1`
P2_NET=`get_net $IF2`

P1=`get_gateway $IF1`
P2=`get_gateway $IF2`


ip route add $P1_NET dev $IF1 src $IP1 table T1
ip route add default via $P1 table T1
ip route add $P2_NET dev $IF2 src $IP2 table T2
ip route add default via $P2 table T2

ip route add $P1_NET dev $IF1 src $IP1
ip route add $P2_NET dev $IF2 src $IP2

#ip route add default via $P1
