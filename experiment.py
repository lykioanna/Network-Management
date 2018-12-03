# !/usr/bin/python
import os
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as mpatches
import numpy as np
from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch, OVSKernelAP
from mininet.link import TCLink
from mininet.log import setLogLevel, debug
from mininet.cli import CLI


import sys
gnet=None

# Implement the graphic function in order to demonstrate the network measurements
# Hint: You can save the measurement in an output file and then import it here
time_=20

def graphic():
	#pass
    z=[]
    graph_data3 = open('RX_out.txt','r').read()
    graph_data = open('TX_out.txt','r').read()
    graph_data1 = open('throughput1.txt','r').read()
    graph_data2 = open('throughput2.txt','r').read()
    lines = graph_data.split('\n')
    lines1 = graph_data1.split('\n')
    lines2 = graph_data2.split('\n')
    lines3 = graph_data3.split('\n')	

    fig, ax = plt.subplots()
    
    ax2 = ax.twinx()
	
    #R_X code
    counter = 0
    temp = []
    tempp = []
    temp1 = []
    temp2 = []
    ys1 = []
    for line in lines3:
	    if len(line) > 1:
		    if counter > 0:
		        temp = line.split(' ')
		        tempp = lines3[counter-1].split(' ')
		        temp1 = temp[11].split(':')
		        temp2 = tempp[11].split(':')
		        temp = int(temp1[1]) - int(temp2[1])
		        ys1.append(temp)
		    counter = counter + 1
			

    
    #T_X code
    counter = 0
    temp = []
    tempp = []
    temp1 = []
    temp2 = []
    ys2 = []
    for line in lines:
	    if len(line) > 1:
		    if counter > 0:
		        temp = line.split(' ')
		        tempp = lines[counter-1].split(' ')
		        temp1 = temp[11].split(':')
		        temp2 = tempp[11].split(':')
		        temp = int(temp1[1]) - int(temp2[1])
		        ys2.append(temp)
		    counter = counter + 1

    #Throughput_1
    counter = 0
    temp = []
    tempp = []
    temp1 = []
    temp2 = []
    ys3 = []
    for line in lines1:
	    if len(line) > 1:
	  	    if counter > 0:
		        temp = line.split(' ')
		        tempp = lines1[counter-1].split(' ')
		        temp1 = temp[16].split(':')
		        temp2 = tempp[16].split(':')
		        temp = int(temp1[1]) - int(temp2[1])
		        ys3.append(temp)
		    counter = counter + 1
			
    #Throughput_2
    counter = 0
    temp = []
    tempp = []
    temp1 = []
    temp2 = []
    ys4 = []
    for line in lines2:
	    if len(line) > 1:
		    if counter > 0:
		        temp = line.split(' ')
		        tempp = lines2[counter-1].split(' ')
		        temp1 = temp[11].split(':')
		        temp2 = tempp[11].split(':')
		        temp = int(temp1[1]) - int(temp2[1])
		        ys4.append(temp)
		    counter = counter + 1
			
    i = 0
    for x in range(len(ys1)):    
        z.append(i)
        i = i + 1
       
    ax.plot(z, ys1, color='green', label='Received Data (client)', markevery=7,linewidth=2)
    ax.plot(z, ys2, color='red', label='Transmited Data (server)', markevery=7,linewidth=2)
    ax2.plot(z, ys3, color='magenta', label='Throughput (server)', markevery=7,linewidth=2)
    ax2.plot(z, ys4, color='blue', label='Throughput (client)', markevery=7,linewidth=2)
    ax.legend(loc=2, borderaxespad=0., fontsize=12)
    ax2.legend(loc=1, borderaxespad=0., fontsize=12)

    ax2.set_yscale('log')

    ax.set_ylabel("# Packets (unit)", fontsize=18)
    ax.set_xlabel("Time (seconds)", fontsize=18)
    ax2.set_ylabel("Throughput (bytes/sec)", fontsize=18)
    
    plt.show()
     
 
def apply_experiment(car,client,switch,net):
    
    #time.sleep(2)
    print "Applying first phase"

    ################################################################################ 
    #   1) Add the flow rules below and the necessary routing commands
    #
    #   Hint 1: For the OpenFlow rules you can either delete and add rules
    #           or modify rules (using mod-flows command)       
    #   Example: os.system('ovs-ofctl mod-flows switch in_port=1,actions=output:2')
    #
    #   Hint 2: For the routing commands check the configuration 
    #           at the beginning of the experiment.
    #
    #   2) Calculate Network Measurements using IPerf or command line tools(ifconfig)
    #       Hint: Remember that you can insert commands via the mininet
    #       Example: car[0].cmd('ifconfig bond0 | grep \"TX packets\" >> %s' % output.data)
    #
    #               ***************** Insert code below *********************  
    #################################################################################
    
    
    os.system('ovs-ofctl add-flow switch in_port=1,actions=output:4')
    os.system('ovs-ofctl mod-flows switch in_port=4,actions=output:1')
    
    os.system('ovs-ofctl mod-flows switch in_port=3,actions=drop')
    os.system('ovs-ofctl mod-flows switch in_port=2,actions=drop')
    
    os.system('ovs-ofctl del-flows eNodeB1')
    os.system('ovs-ofctl del-flows eNodeB2')
    os.system('ovs-ofctl del-flows rsu1')
    car[0].cmd('ip route add 200.0.10.2 via 200.0.10.50')
    client.cmd('ip route add 200.0.10.100 via 200.0.10.150')
    
    timeout = time.time() + time_
    currentTime = time.time()
    i = 0
    while True:
        if time.time() > timeout:
            break;
        if time.time() - currentTime >= i:
            car[0].cmd('ifconfig bond0 | grep \"TX packets\" >> TX_out.txt')
            client.cmd('ifconfig client-eth0 | grep \"RX packets\" >> RX_out.txt')
            car[0].cmd('ifconfig bond0 | grep \ "bytes\" >> throughput1.txt')
            client.cmd('ifconfig client-eth0 | grep \"bytes\" >> throughput2.txt')
            i += 0.5
            
    #print "*** Running CLI"
    #CLI(net)   
    print "Moving nodes"
    car[0].moveNodeTo('150,100,0')
    car[1].moveNodeTo('120,100,0')
    car[2].moveNodeTo('90,100,0')
    car[3].moveNodeTo('70,100,0')
  
    #time.sleep(2)
    print "Applying second phase"
    ################################################################################ 
    #   1) Add the flow rules below and the necessary routing commands
    #
    #   Hint 1: For the OpenFlow rules you can either delete and add rules
    #           or modify rules (using mod-flows command)       
    #   Example: os.system('ovs-ofctl mod-flows switch in_port=1,actions=output:2')
    #
    #   Hint 2: For the routing commands check the configuration 
    #           you have added before.
    #           Remember that now the car connects to RSU1 and eNodeB2
    #
    #   2) Calculate Network Measurements using IPerf or command line tools(ifconfig)
    #       Hint: Remember that you can insert commands via the mininet
    #       Example: car[0].cmd('ifconfig bond0 | grep \"TX packets\" >> %s' % output.data)
    #
    #           ***************** Insert code below ********************* 
    #################################################################################
    
    
    os.system('ovs-ofctl mod-flows switch in_port=2,actions=output:4')
    os.system('ovs-ofctl mod-flows switch in_port=3,actions=output:4')
    os.system('ovs-ofctl mod-flows switch in_port=4,actions=output:2')
    os.system('ovs-ofctl mod-flows switch in_port=4,actions=output:3')
    
    os.system('ovs-ofctl mod-flows switch in_port=1,actions=drop')
    
    os.system('ovs-ofctl del-flows eNodeB1')
    os.system('ovs-ofctl del-flows eNodeB2')
    os.system('ovs-ofctl del-flows rsu1')
    car[0].cmd('ip route del 200.0.10.2 via 200.0.10.50')
    client.cmd('ip route del 200.0.10.100 via 200.0.10.150')
    
    
    timeout = time.time() + time_
    currentTime = time.time()
    i = 0
    while True:
        if time.time() > timeout:
            break;
        if time.time() - currentTime >= i:
            car[0].cmd('ifconfig bond0 | grep \"TX packets\" >> TX_out.txt')
            client.cmd('ifconfig client-eth0 | grep \"RX packets\" >> RX_out.txt')
            car[0].cmd('ifconfig bond0 | grep \ "bytes\" >> throughput1.txt')
            client.cmd('ifconfig client-eth0 | grep \"bytes\" >> throughput2.txt') 
            i += 0.5
    
    #print "*** Running CLI"
    #CLI(net)
    
    
    
    print "Moving nodes"
    car[0].moveNodeTo('190,100,0')
    car[1].moveNodeTo('150,100,0')
    car[2].moveNodeTo('120,100,0')
    car[3].moveNodeTo('90,100,0')

    
     
    #time.sleep(2)
    print "Applying third phase"
    
    ################################################################################ 
    #   1) Add the flow rules below and routing commands if needed
    #
    #   Hint 1: For the OpenFlow rules you can either delete and add rules
    #           or modify rules (using mod-flows command)       
    #   Example: os.system('ovs-ofctl mod-flows switch in_port=1,actions=output:2')
    #
    #
    #   2) Calculate Network Measurements using IPerf or command line tools(ifconfig)
    #       Hint: Remember that you can insert commands via the mininet
    #       Example: car[0].cmd('ifconfig bond0 | grep \"TX packets\" >> %s' % output.data)
    #
    #           ***************** Insert code below ********************* 
    #################################################################################
        
    
    os.system('ovs-ofctl mod-flows switch in_port=2,actions=output:4')
    os.system('ovs-ofctl mod-flows switch in_port=4,actions=output:2')
    
    os.system('ovs-ofctl mod-flows switch in_port=1,actions=drop')
    os.system('ovs-ofctl mod-flows switch in_port=3,actions=drop')
    
    
    os.system('ovs-ofctl del-flows eNodeB1')
    os.system('ovs-ofctl del-flows eNodeB2')
    os.system('ovs-ofctl del-flows rsu1')
    
    timeout = time.time() + time_
    currentTime = time.time()
    i = 0
    while True:
        if time.time() > timeout:
            break;
        if time.time() - currentTime >= i:
            car[0].cmd('ifconfig bond0 | grep \"TX packets\" >> TX_out.txt')
            client.cmd('ifconfig client-eth0 | grep \"RX packets\" >> RX_out.txt')
            car[0].cmd('ifconfig bond0 | grep \ "bytes\" >> throughput1.txt')
            client.cmd('ifconfig client-eth0 | grep \"bytes\" >> throughput2.txt') 
            i += 0.5
  

def topology():
    "Create a network."
    net = Mininet(controller=Controller, link=TCLink, switch=OVSKernelSwitch, accessPoint=OVSKernelAP)
    global gnet
    gnet = net

    print "*** Creating nodes"
    car = []
    stas = []
    for x in range(0, 4):
        car.append(x)
        stas.append(x)
    for x in range(0, 4):
        car[x] = net.addCar('car%s' % (x), wlans=2, ip='10.0.0.%s/8' % (x + 1), \
        mac='00:00:00:00:00:0%s' % x, mode='b')

    
    eNodeB1 = net.addAccessPoint('eNodeB1', ssid='eNodeB1', dpid='1000000000000000', mode='ac', channel='1', position='80,75,0', range=60)
    eNodeB2 = net.addAccessPoint('eNodeB2', ssid='eNodeB2', dpid='2000000000000000', mode='ac', channel='6', position='180,75,0', range=70)
    rsu1 = net.addAccessPoint('rsu1', ssid='rsu1', dpid='3000000000000000', mode='g', channel='11', position='140,120,0', range=40)
    c1 = net.addController('c1', controller=Controller)
    client = net.addHost ('client')
    switch = net.addSwitch ('switch', dpid='4000000000000000')

    net.plotNode(client, position='125,230,0')
    net.plotNode(switch, position='125,200,0')

    print "*** Configuring wifi nodes"
    net.configureWifiNodes()

    print "*** Creating links"
    net.addLink(eNodeB1, switch)
    net.addLink(eNodeB2, switch)
    net.addLink(rsu1, switch)
    net.addLink(switch, client)

    print "*** Starting network"
    net.build()
    c1.start()
    eNodeB1.start([c1])
    eNodeB2.start([c1])
    rsu1.start([c1])
    switch.start([c1])

    for sw in net.vehicles:
        sw.start([c1])

    i = 1
    j = 2
    for c in car:
        c.cmd('ifconfig %s-wlan0 192.168.0.%s/24 up' % (c, i))
        c.cmd('ifconfig %s-eth0 192.168.1.%s/24 up' % (c, i))
        c.cmd('ip route add 10.0.0.0/8 via 192.168.1.%s' % j)
        i += 2
        j += 2

    i = 1
    j = 2
    for v in net.vehiclesSTA:
        v.cmd('ifconfig %s-eth0 192.168.1.%s/24 up' % (v, j))
        v.cmd('ifconfig %s-mp0 10.0.0.%s/24 up' % (v, i))
        v.cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')
        i += 1
        j += 2

    for v1 in net.vehiclesSTA:
        i = 1
        j = 1
        for v2 in net.vehiclesSTA:
            if v1 != v2:
                v1.cmd('route add -host 192.168.1.%s gw 10.0.0.%s' % (j, i))
            i += 1
            j += 2

    client.cmd('ifconfig client-eth0 200.0.10.2')
    net.vehiclesSTA[0].cmd('ifconfig car0STA-eth0 200.0.10.50')

    car[0].cmd('modprobe bonding mode=3')
    car[0].cmd('ip link add bond0 type bond')
    car[0].cmd('ip link set bond0 address 02:01:02:03:04:08')
    car[0].cmd('ip link set car0-eth0 down')
    car[0].cmd('ip link set car0-eth0 address 00:00:00:00:00:11')
    car[0].cmd('ip link set car0-eth0 master bond0')
    car[0].cmd('ip link set car0-wlan0 down')
    car[0].cmd('ip link set car0-wlan0 address 00:00:00:00:00:15')
    car[0].cmd('ip link set car0-wlan0 master bond0')
    car[0].cmd('ip link set car0-wlan1 down')
    car[0].cmd('ip link set car0-wlan1 address 00:00:00:00:00:13')
    car[0].cmd('ip link set car0-wlan1 master bond0')
    car[0].cmd('ip addr add 200.0.10.100/24 dev bond0')
    car[0].cmd('ip link set bond0 up')

    car[3].cmd('ifconfig car3-wlan0 200.0.10.150')

    client.cmd('ip route add 192.168.1.8 via 200.0.10.150')
    client.cmd('ip route add 10.0.0.1 via 200.0.10.150')

    net.vehiclesSTA[3].cmd('ip route add 200.0.10.2 via 192.168.1.7')
    net.vehiclesSTA[3].cmd('ip route add 200.0.10.100 via 10.0.0.1')
    net.vehiclesSTA[0].cmd('ip route add 200.0.10.2 via 10.0.0.4')

    car[0].cmd('ip route add 10.0.0.4 via 200.0.10.50')
    car[0].cmd('ip route add 192.168.1.7 via 200.0.10.50')
    car[0].cmd('ip route add 200.0.10.2 via 200.0.10.50')
    car[3].cmd('ip route add 200.0.10.100 via 192.168.1.8')

    """plot graph"""
    net.plotGraph(max_x=250, max_y=250)

    net.startGraph()

    # Uncomment and modify the two commands below to stream video using VLC 
    car[0].cmdPrint("vlc -vvv bunnyMob.mp4 --sout '#duplicate{dst=rtp{dst=200.0.10.2,port=5004,mux=ts},dst=display}' :sout-keep &")
    client.cmdPrint("vlc rtp://@200.0.10.2:5004 &")

    car[0].moveNodeTo('95,100,0')
    car[1].moveNodeTo('80,100,0')
    car[2].moveNodeTo('65,100,0')
    car[3].moveNodeTo('50,100,0')

    os.system('ovs-ofctl del-flows switch')

    time.sleep(3)

    apply_experiment(car,client,switch,net)

    # Uncomment the line below to generate the graph that you implemented
    graphic()

    # kills all the xterms that have been opened
    #os.system('pkill xterm')

   

    print "*** Running CLI"
    CLI(net)

    print "*** Stopping network"
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    try:
        topology()
    except:
        type = sys.exc_info()[0]
        error = sys.exc_info()[1]
        traceback = sys.exc_info()[2]
        print ("Type: %s" % type)
        print ("Error: %s" % error)
        print ("Traceback: %s" % traceback)
        if gnet != None:
            gnet.stop()
        else:
            print "No network was created..."
