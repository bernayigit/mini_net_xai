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

    def addSwitch( self, name, **opts ):
        kwargs = { 'protocols' : 'OpenFlow13' }
        kwargs.update( opts )
        return super(GeantMplsTopo, self).addSwitch( name, **kwargs )

    def __init__( self ):
        "Create a topology."

        # Initialize Topology
        Topo.__init__( self )

        # add nodes, switches first...
        at1_at = self.addSwitch( 's1' )
        be1_be = self.addSwitch( 's2' )
        ch1_ch = self.addSwitch( 's3' )
        cz1_cz = self.addSwitch( 's4' )
        de1_de = self.addSwitch( 's5' )
        es1_es = self.addSwitch( 's6' )
        fr1_fr = self.addSwitch( 's7' )
        gr1_gr = self.addSwitch( 's8' )
        hr1_hr = self.addSwitch( 's9' )
        hu1_hu = self.addSwitch( 's10' )
        ie1_ie = self.addSwitch( 's11' )
        il1_il = self.addSwitch( 's12' )
        it1_it = self.addSwitch( 's13' )
        lu1_lu = self.addSwitch( 's14' )
        nl1_nl = self.addSwitch( 's15' )
        ny1_ny = self.addSwitch( 's16' )
        pl1_pl = self.addSwitch( 's17' )
        pt1_pt = self.addSwitch( 's18' )
        se1_se = self.addSwitch( 's19' )
        si1_si = self.addSwitch( 's20' )
        sk1_sk = self.addSwitch( 's21' )
        uk1_uk = self.addSwitch( 's22' )

    # ... and now hosts
        at1_at_host = self.addHost( 'h1' )
        be1_be_host = self.addHost( 'h2' )
        ch1_ch_host = self.addHost( 'h3' )
        cz1_cz_host = self.addHost( 'h4' )
        de1_de_host = self.addHost( 'h5' )
        es1_es_host = self.addHost( 'h6' )
        fr1_fr_host = self.addHost( 'h7' )
        gr1_gr_host = self.addHost( 'h8' )
        hr1_hr_host = self.addHost( 'h9' )
        hu1_hu_host = self.addHost( 'h10' )
        ie1_ie_host = self.addHost( 'h11' )
        il1_il_host = self.addHost( 'h12' )
        it1_it_host = self.addHost( 'h13' )
        lu1_lu_host = self.addHost( 'h14' )
        nl1_nl_host = self.addHost( 'h15' )
        ny1_ny_host = self.addHost( 'h16' )
        pl1_pl_host = self.addHost( 'h17' )
        pt1_pt_host = self.addHost( 'h18' )
        se1_se_host = self.addHost( 'h19' )
        si1_si_host = self.addHost( 'h20' )
        sk1_sk_host = self.addHost( 'h21' )
        uk1_uk_host = self.addHost( 'h22' )

        # add edges between switch and corresponding host
        self.addLink( at1_at , at1_at_host )
        self.addLink( be1_be , be1_be_host )
        self.addLink( ch1_ch , ch1_ch_host )
        self.addLink( cz1_cz , cz1_cz_host )
        self.addLink( de1_de , de1_de_host )
        self.addLink( es1_es , es1_es_host )
        self.addLink( fr1_fr , fr1_fr_host )
        self.addLink( gr1_gr , gr1_gr_host )
        self.addLink( hr1_hr , hr1_hr_host )
        self.addLink( hu1_hu , hu1_hu_host )
        self.addLink( ie1_ie , ie1_ie_host )
        self.addLink( il1_il , il1_il_host )
        self.addLink( it1_it , it1_it_host )
        self.addLink( lu1_lu , lu1_lu_host )
        self.addLink( nl1_nl , nl1_nl_host )
        self.addLink( ny1_ny , ny1_ny_host )
        self.addLink( pl1_pl , pl1_pl_host )
        self.addLink( pt1_pt , pt1_pt_host )
        self.addLink( se1_se , se1_se_host )
        self.addLink( si1_si , si1_si_host )
        self.addLink( sk1_sk , sk1_sk_host )
        self.addLink( uk1_uk , uk1_uk_host )

        # add edges between switches
        self.addLink( at1_at , ch1_ch )
        self.addLink( at1_at , de1_de )
        self.addLink( at1_at , hu1_hu )
        self.addLink( at1_at , ny1_ny )
        self.addLink( at1_at , si1_si )
        self.addLink( be1_be , fr1_fr )
        self.addLink( be1_be , lu1_lu )
        self.addLink( be1_be , nl1_nl )
        self.addLink( ch1_ch , fr1_fr )
        self.addLink( ch1_ch , it1_it )
        self.addLink( cz1_cz , de1_de )
        self.addLink( cz1_cz , pl1_pl )
        self.addLink( cz1_cz , sk1_sk )
        self.addLink( de1_de , fr1_fr )
        self.addLink( de1_de , gr1_gr )
        self.addLink( de1_de , ie1_ie )
        self.addLink( de1_de , it1_it )
        self.addLink( de1_de , nl1_nl )
        self.addLink( de1_de , se1_se )
        self.addLink( es1_es , fr1_fr )
        self.addLink( es1_es , it1_it )
        self.addLink( es1_es , pt1_pt )
        self.addLink( fr1_fr , lu1_lu )
        self.addLink( fr1_fr , uk1_uk )
        self.addLink( gr1_gr , it1_it )
        self.addLink( hr1_hr , hu1_hu )
        self.addLink( hr1_hr , si1_si )
        self.addLink( hu1_hu , sk1_sk )
        self.addLink( ie1_ie , uk1_uk )
        self.addLink( il1_il , it1_it )
        self.addLink( il1_il , nl1_nl )
        self.addLink( nl1_nl , uk1_uk )
        self.addLink( ny1_ny , uk1_uk )
        self.addLink( pl1_pl , se1_se )
        self.addLink( pt1_pt , uk1_uk )
        self.addLink( se1_se , uk1_uk )

topos = { 'geant': ( lambda: GeantMplsTopo() ) }

# Driver code
if __name__ == '__main__':
    topo = GeantMplsTopo()
    net = Mininet(topo=topo, link=TCLink,
                  controller=RemoteController('c0', ip='127.0.0.1', port=6653))

    print("*** Starting network")
    net.start()

    print("*** Running CLI")
    CLI(net)

    print("*** Stopping network")
    net.stop()
