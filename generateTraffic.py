from net_4_hosts import net
import numpy as np
import time
from mininet.cli import CLI

class Generator:
    """
    Traffic generator class. We use iperf tool
    from each host terminal to start iperf communication.
    """

    def __init__(self, hosts, demand, duration=10):

        self.hosts = hosts
        self.demand = demand
        self.duration = duration

    def start_iperf(self):
        
        # Start iperf serers on all hosts
        for host in self.hosts:
            host.cmd('iperf -s &')

    def stop_iperf(self):
        
        # Stop iperf servers on all hosts
        for host in self.hosts:
            host.cmd('killall iperf')

    def inject_traffic(self):

        self.start_iperf()

        # Small delay to ensure servers are up
        time.sleep(2)

        for i, src in enumerate(self.hosts):
            for j, dst in enumerate(self.hosts):
                if i != j:
                    volume = self.demand[i][j] # in bits
                    if volume > 0:
                        """
                        # Convert volume to bandwidth over given duration
                        bandwidth = int(volume / self.duration) # in bits per second
                        # Convert bandwidth to Mbps for iperf 
                        bandwidth_mbps = bandwidth / (10**6)
                        """
                        bandwidth_mbps = volume # renaming for test sake

                        # Use iperf to generate traffic
                        src.cmd(f"iperf -c {dst.IP()} -t {self.duration} -b {bandwidth_mbps}M &")
        
        time.sleep(self.duration + 5)

        # Stop iperf servers
        self.stop_iperf()

# Driver code
if __name__ == '__main__':

    print("*** Starting network")
    net.start()

    #traffic_data = np.load('Geant.npy')
    #demands = traffic_data[0]
    pseudo_demands = [[0.0, 0.0, 12.0, 0.0],
                      [0.0, 0.0, 0.0, 9.0],
                      [10.0, 0.0, 0.0, 0.0],
                      [0.0, 4.0, 0.0, 0.0]]
    
    traffic_gen = Generator(net.hosts, pseudo_demands)
    traffic_gen.inject_traffic() # Adding traffic

    print("*** Running CLI")
    CLI(net)

    print("*** Stopping network")
    net.stop()