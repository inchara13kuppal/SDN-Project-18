# SDN Project 18: Dynamic Host Blocking System

## Project Overview
This repository contains the implementation of a Dynamic Host Blocking System using a POX controller and Mininet. The objective of this lab project is to create an OpenFlow controller module that functions as a standard learning switch but actively monitors packet counts per host. If a host exceeds a predefined threshold (15 packets), the controller dynamically installs a flow rule in the switch to drop all subsequent traffic from that specific MAC address.



## Prerequisites
* Ubuntu Linux Environment
* Mininet Network Emulator
* POX OpenFlow Controller
* Python 3.x

## Project Structure
* `pox_blocker.py`: The main controller script containing the dynamic blocking logic. It extends the POX controller base classes to handle `PacketIn` events.

## Setup and Execution
To run this project, you will need two terminal windows.

1. **Start the POX Controller:**
Navigate to the POX directory and run the custom blocker module with debug logging enabled to monitor suspicious activity.
`cd ~/pox`
`./pox.py log.level --DEBUG ext.pox_blocker`

2. **Start the Mininet Topology:**
In a separate terminal, launch a Mininet network with a single switch and 3 hosts, connected to the remote POX controller.
`sudo mn --topo single,3 --controller remote,ip=127.0.0.1 --mac`

## Testing and Verification

### 1. Triggering the Block
Generate traffic from host 1 to host 2 to exceed the 15-packet threshold.
`mininet> h1 ping -c 20 h2`
*Expected Output:* The initial pings will succeed, but after the threshold is reached, the POX controller will log "SUSPICIOUS ACTIVITY!" and install a drop rule. The remaining pings will result in high packet loss (e.g., 70% or more).

### 2. Inspecting the Flow Tables
Verify that the switch has received the drop rule from the controller.
`mininet> dpctl dump-flows`
*Expected Output:* You will see a flow entry matching the source MAC address of the blocked host with an empty action list (actions=drop) and a priority of 100.

### 3. Throughput Interruption
Test how the block handles high-bandwidth TCP traffic using iperf.
`mininet> iperf h1 h2`
*Expected Output:* The test will hang or fail almost immediately because the controller will detect the massive influx of packets within the first fraction of a second and drop the traffic, preventing the connection from completing.

## Baseline Connectivity Testing
Before triggering the dynamic block, a `pingall` test was executed to verify that all hosts in the default topology could successfully communicate with zero dropped packets.

<img width="613" height="569" alt="sdn1" src="https://github.com/user-attachments/assets/9c8c3d12-ce93-4846-86e7-e62e01e2d6e3" />

1. **Start the POX Controller:**
Navigate to the POX directory and run the custom blocker module with debug logging enabled to monitor suspicious activity.
`cd ~/pox`
`./pox.py log.level --DEBUG ext.pox_blocker`

**Controller Connection Status:**
<img width="607" height="403" alt="sdn2" src="https://github.com/user-attachments/assets/fa01c24a-0dd6-4ca7-b346-351649cf71e5" />

### 2. Inspecting the Flow Tables
Verify that the switch has received the drop rule from the controller after the threshold is breached.
`mininet> dpctl dump-flows`

**Traffic Block and Flow Table Verification:**
<img width="639" height="245" alt="Screenshot 2026-04-08 170126" src="https://github.com/user-attachments/assets/84a01885-51c3-4058-910a-adabdaecd9c2" />
