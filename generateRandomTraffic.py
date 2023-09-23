from net_10_hosts import net
import numpy as np
import time
from mininet.cli import CLI
import random

class Generator:
    """
    Traffic generator class. We use iperf tool
    from each host terminal to start iperf communication.
    """

    def __init__(self, hosts, duration=10):
        self.hosts = hosts
        self.duration = duration
        self.demand = self.initialize_demand()

    def initialize_demand(self):
        # Create a 10 x 10 demand matrix.
        # Each value is rounded to 4 decimal place
        return [[round(random.uniform(1, 9), 4) if i != j else 0.0 \
                 for j in range(len(self.hosts))] for i in range(len(self.hosts))]
    
    def update_demand(self):
        # Make the next demand a function of the previous one.
        # Here we add a small random noise to the previous demand.
        for i in range(len(self.hosts)):
            for j in range(len(self.hosts)):
                if i != j:
                    noise = round(random.uniform(-2.5, 2.5), 4)
                    self.demand[i][j] = max(0, self.demand[i][j] + noise) # Ensuring that demand stays non-negative
    
    def start_iperf(self):
        
        print('Starting iPerf on all hosts')
        for host in self.hosts:
            host.cmd('iperf -s &')
        # Small delay to ensure servers are up
        time.sleep(2)

    def stop_iperf(self):

        print('Stopping iPerf on all hosts')
        for host in self.hosts:
            host.cmd('killall iperf')

    def inject_traffic(self):

        for i, src in enumerate(self.hosts):
            for j, dst in enumerate(self.hosts):
                if i != j:
                    volume = self.demand[i][j]  # in bits
                    if volume > 0:
                        bandwidth_mbps = volume  # renaming for test sake

                        # Use iperf to generate traffic
                        src.cmd(f"iperf -c {dst.IP()} -t {self.duration} -b {bandwidth_mbps}M &")

        self.update_demand()
        time.sleep(5)

# Driver code
if __name__ == '__main__':
    print("*** Starting network")
    net.start()

    traffic_gen = Generator(net.hosts)
    print(len(traffic_gen.hosts))
    
    # Perform 100 experiment
    traffic_gen.start_iperf()
    for i in range(100):
        traffic_gen.inject_traffic()
        print(f'traffic {i} injected')
    
    traffic_gen.stop_iperf()
    print("*** Running CLI")
    CLI(net)

    print("*** Stopping network")
    net.stop()
