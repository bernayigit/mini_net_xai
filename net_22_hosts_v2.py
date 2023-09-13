#!/usr/bin/env python

"""
"""
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.node import Node
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.util import dumpNodeConnections

class GeantMplsTopo( Topo ):
    "Internet Topology Zoo Specimen."

    # host list
    hosts = ['at1_at_host', 'be1_be_host', 'ch1_ch_host', 'cz1_cz_host', 'de1_de_host', 
             'es1_es_host', 'fr1_fr_host', 'gr1_gr_host', 'hr1_hr_host', 'hu1_hu_host', 
             'ie1_ie_host', 'il1_il_host', 'it1_it_host', 'lu1_lu_host', 'nl1_nl_host', 
             'ny1_ny_host', 'pl1_pl_host', 'pt1_pt_host',  'se1_se_host', 'si1_si_host', 
             'sk1_sk_host', 'uk1_uk_host']
    
    # Switches
    switches = ['at1_at', 'be1_be', 'ch1_ch', 'cz1_cz', 'de1_de', 'es1_es', 'fr1_fr', 'gr1_gr', 'hr1_hr', 
                'hu1_hu', 'ie1_ie', 'il1_il', 'it1_it', 'lu1_lu', 'nl1_nl', 'ny1_ny', 'pl1_pl', 
                'pt1_pt', 'se1_se', 'si1_si', 'sk1_sk', 'uk1_uk']
    
    # Switch links based on index in the switches list
    switch_links = [
        (0, 2),  # at1_at , ch1_ch
        (0, 4),  # at1_at , de1_de
        (0, 9),  # at1_at , hu1_hu
        (0, 15), # at1_at , ny1_ny
        (0, 19), # at1_at , si1_si
        (1, 6),  # be1_be , fr1_fr
        (1, 13), # be1_be , lu1_lu
        (1, 14), # be1_be , nl1_nl
        (2, 6),  # ch1_ch , fr1_fr
        (2, 12), # ch1_ch , it1_it
        (3, 4),  # cz1_cz , de1_de
        (3, 16), # cz1_cz , pl1_pl
        (3, 20), # cz1_cz , sk1_sk
        (4, 6),  # de1_de , fr1_fr
        (4, 7),  # de1_de , gr1_gr
        (4, 10), # de1_de , ie1_ie
        (4, 12), # de1_de , it1_it
        (4, 14), # de1_de , nl1_nl
        (4, 18), # de1_de , se1_se
        (5, 6),  # es1_es , fr1_fr
        (5, 12), # es1_es , it1_it
        (5, 17), # es1_es , pt1_pt
        (6, 13), # fr1_fr , lu1_lu
        (6, 21), # fr1_fr , uk1_uk
        (7, 12), # gr1_gr , it1_it
        (8, 9),  # hr1_hr , hu1_hu
        (8, 19), # hr1_hr , si1_si
        (9, 20), # hu1_hu , sk1_sk
        (10, 21),# ie1_ie , uk1_uk
        (11, 12),# il1_il , it1_it
        (11, 14),# il1_il , nl1_nl
        (14, 21),# nl1_nl , uk1_uk
        (15, 21),# ny1_ny , uk1_uk
        (16, 18),# pl1_pl , se1_se
        (17, 21),# pt1_pt , uk1_uk
        (18, 21) # se1_se , uk1_uk
    ]


    def addSwitch( self, name, **opts ):
        kwargs = { 'protocols' : 'OpenFlow13' }
        kwargs.update( opts )
        return super(GeantMplsTopo, self).addSwitch( name, **kwargs )

    def __init__( self ):
        "Create a topology."

        # Initialize Topology
        Topo.__init__( self )

        # Add switches and store in a dict for referencing
        switch_objects = {name: self.addSwitch(f's{i}') for i, name in enumerate(self.switches)}

        # Add hosts and link them to their corresponding switches
        i = 1
        for switch, _ in zip(self.switches, self.hosts):
            host_mac = '00:00:00:00:00:{:02}'.format(i)  # Using integer mac address
            host = self.addHost(f'h{i}', mac=host_mac)
            self.addLink(switch_objects[switch], host)
            i += 1

        # Add switch links based on the switch_links list
        for (src_idx, dst_idx) in self.switch_links:
            self.addLink(switch_objects[self.switches[src_idx]], switch_objects[self.switches[dst_idx]])

TOPOS = {'geant': ( lambda: GeantMplsTopo() ) }

# To allow access to the net object
topo = GeantMplsTopo()
net = Mininet(topo=topo, 
                  controller=RemoteController('c0', 
                                              ip='127.0.0.1', 
                                              port=6653))  

# Driver code
if __name__ == '__main__':

    setLogLevel('info')