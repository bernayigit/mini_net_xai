# Overview
This application simulates a mini-network nodes namely: __(h1, h2, h3, and h4)__. These nodes are connected to a remote 
SDN (Software Defined Networking) controller. The network is constructed using Mininet and Ryu. Specifically:

* Nodes h1 and h3 are directly connected via OVSwitches.
* Nodes h2 and h4 are directly connected via OVSwitches.

The primary objective of this application is to generate a traffic matrix from the SDN controller, capturing the traffic 
flows between the end nodes or hosts.

# Prerequisites

Ensure that you have [Mininet](http://mininet.org/download/) and [Ryu](https://ryu-sdn.org/) 
installed on your system. It is recommended that you use a Python virtual environment to isolate your project setup.

# Running the application
After setting up Mininet and Ryu, follow these steps:

1. **Clone the Repository:** This will copy the project files to your local system.
2. **Start the Ryu Controller**:  
Navigate to the root directory of the cloned repository and run.
```
ryu-manager ryu_monitor.py
```
2. **Generate Traffic:**
In a new terminal, execute the ```generateTraffic.py``` script.
```
sudo python generateTraffic.py
```
**Note: Mininet requires root privileges, hence the use of ```sudo``` on Linux systems.

# Output
Upon successful execution, the Ryu controller will generate CSV files named ```traffic_matrix_XXX.csv``` in the root directory. 
Each file represents the traffic matrix at a given time, captured at 10-second intervals. To prevent continuous generation of CSV 
files, ensure you stop the ```ryu_monitor.py``` script.

Below is a sample output of the traffic matrix from a generated CSV file:
|          |          |          |          |
|----------|----------|----------|----------|
| 0.0      | 0.0      | 15898888.0 | 0.0    |
| 0.0      | 0.0      | 0.0      | 0.0      |
| 13275468.0 | 0.0      | 0.0      | 0.0      |
| 0.0      | 0.0      | 0.0      | 0.0      |
