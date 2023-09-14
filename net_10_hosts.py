"""
Custom topology example
	
	h1     h4     h6     h8    h10
	|   	|      |     |      |
	s1 --- s2 --- s3 --- s4 --- s5
	|      |      |      |      |
	h2     h3     h5     h7     h9
"""


from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.log import setLogLevel
from mininet.cli import CLI
from time import sleep

class MyTopo( Topo):
	"Simple topology example."
	
	def build( self ):
		"Create custom topo."
		
		#Add hosts and switches
		h1 = self.addHost('h1', 				
				mac='00:00:00:00:00:01',
				ip='10.0.0.1/16')
		h2 = self.addHost('h2', 		
				mac='00:00:00:00:00:02',
				ip='10.0.0.2/16')
		h3 = self.addHost('h3', 		
				mac='00:00:00:00:00:03',
				ip='10.0.0.3/16')
		h4 = self.addHost('h4', 		
				mac='00:00:00:00:00:04',
				ip='10.0.0.4/16')
		h5 = self.addHost('h5', 		
				mac='00:00:00:00:00:05',
				ip='10.0.0.5/16')
		h6 = self.addHost('h6', 				
				mac='00:00:00:00:00:06',
				ip='10.0.0.6/16')
		h7 = self.addHost('h7', 		
				mac='00:00:00:00:00:07',
				ip='10.0.0.7/16')
		h8 = self.addHost('h8', 		
				mac='00:00:00:00:00:08',
				ip='10.0.0.8/16')
		h9 = self.addHost('h9', 		
				mac='00:00:00:00:00:09',
				ip='10.0.0.9/16')
		h10 = self.addHost('h10', 		
				mac='00:00:00:00:00:10',
				ip='10.0.0.10/16')
		switch1 = self.addSwitch('s1', mac='00:00:00:00:00:11')
		switch2 = self.addSwitch('s2', mac='00:00:00:00:00:12')
		switch3 = self.addSwitch('s3', mac='00:00:00:00:00:13')
		switch4 = self.addSwitch('s4', mac='00:00:00:00:00:14')
		switch5 = self.addSwitch('s5', mac='00:00:00:00:00:15')
		
		#Add links
		self.addLink( h1, switch1 )
		self.addLink( h2, switch1 )
		self.addLink( switch1, switch2  )
		self.addLink( switch2, h3 )
		self.addLink( switch2, h4 )
		self.addLink( switch2, switch3 )
		self.addLink( switch3, h5 )
		self.addLink( switch3, h6 )
		self.addLink( switch3, switch4 )
		self.addLink( switch4, h7 )
		self.addLink( switch4, h8 )
		self.addLink( switch4, switch5 )
		self.addLink( switch5, h9 )
		self.addLink( switch5, h10 )

TOPOS = {'gtopo': ( lambda: MyTopo() ) }

# To allow access to the net object
topo = MyTopo()
net = Mininet(topo=topo, 
                  controller=RemoteController('c0', 
                                              ip='127.0.0.1', 
                                              port=6653))  

# Drive code
if __name__ == '__main__':
	
	setLogLevel('info')