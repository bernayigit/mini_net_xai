#!usr/bin/python
"""Topoly layout

Switch1---Host1
Switch1---Host2
Switch1---Host3
Switch1---Host4

Switch1---Switch3
Switch2---Switch4

"""
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.log import setLogLevel
from mininet.cli import CLI
from time import sleep

class GTopo(Topo):

    def build(self):

        # add nodes, switches first...
        at1_at = self.addSwitch( 's1', mac='00:00:00:00:00:11' )
        be1_be = self.addSwitch( 's2', mac='00:00:00:00:00:12' )
        ch1_ch = self.addSwitch( 's3', mac='00:00:00:00:00:13' )
        cz1_cz = self.addSwitch( 's4', mac='00:00:00:00:00:14' )

        # ... and now hosts
        at1_at_host = self.addHost( 'h1', 
                                   mac='00:00:00:00:00:01',
                                   ip='10.0.0.1/16')
        be1_be_host = self.addHost( 'h2', 
                                   mac='00:00:00:00:00:02',
                                   ip='10.0.0.2/16')
        ch1_ch_host = self.addHost( 'h3', 
                                   mac='00:00:00:00:00:03',
                                   ip='10.0.0.3/16')
        cz1_cz_host = self.addHost( 'h4', 
                                   mac='00:00:00:00:00:04',
                                   ip='10.0.0.4/16')

        # add edges between switch and corresponding host
        self.addLink( at1_at , at1_at_host )
        self.addLink( be1_be , be1_be_host )
        self.addLink( ch1_ch , ch1_ch_host )
        self.addLink( cz1_cz , cz1_cz_host )

        # add edges between switches
        self.addLink( at1_at , ch1_ch )
        self.addLink( be1_be , cz1_cz )
        

TOPOS = {'gtopo': ( lambda: GTopo() ) }
    
# Drive code
if __name__ == '__main__':

    setLogLevel('info')
    topo = GTopo()
    net = Mininet(topo=topo, 
                  controller=RemoteController('c0', 
                                              ip='127.0.0.1', 
                                              port=6653))
    print("*** Starting network")
    net.start()

    print("*** Running CLI")
    CLI(net)

    print("*** Stopping network")
    net.stop()
