
# VoIP attack demonstration : MITM 

## Required tools / packets

-   Asterisk server
- Wireshark
-   Ettercap : `apt-get -y install ettercap-common`

## Docker details

This setup uses Docker to create a virtual VoIP environment for testing and demonstrating a MITM attack on a VoIP server.

### Network Configuration

The Docker network `voip-net` is configured with a subnet of `10.9.0.0/24`, and all containers communicate within this network. The key services in this setup are:

-   **VoIP Server (`voip-server`)**: Runs an Asterisk VoIP server on `10.9.0.4`.
-   **Clients (`client1 ip : 10.9.0.3` & `client2 : ip 10.9.0.2`)**: SIP clients that connect to the VoIP server.
-   **Attacker (`attacker ip : 10.9.0.5`)**: A container with tools for launching DoS attacks.

### Ports Configuration

The VoIP server exposes several ports:

-   `5060/udp`, `5060/tcp` for SIP communications.
-   `5061/tls` for secure SIP connections.
-   `10000-10099/udp` for RTP media streaming.
-   Dynamic web interface ports through `WEBSMSD_PORT`.

### Volume Mapping

Persistent configurations and shared resources are managed through volumes:

-   `tele-conf` for VoIP server configurations.
-   `pulse` for host audio sharing.
-   `attacker-files` for file transfers related to attacks.

## Attack setup details
1 - Start the docker environment with `docker-compose up -d
`
2 - Register and send/run a test SIP call between client1 and client2 with scapy by executing `sip_communication.py` which is on the attacker-files volume START asterisk -vvv ON EACH ATTACKER/CLIENTS AND LAUCH FROM ATTACKER
3 - Track the simulated call : `tcpdump -vv -i eth0 -G 10 -W 1 -w sip_traffic.pcap
` to get the clients IP (10 seconds)
4 - After identifying the caller, use ettercap to get useful intel like caller id to spoof 
5 - Use the `sip_end_attack.py` to terminate the call.

## Python files usage

### sip_communication.py
1.  **Defines Network Parameters:**
    
    -   `sip_server_ip = "10.9.0.4"` → SIP server (Asterisk in your case)
        
    -   `client1_ip = "10.9.0.3"` → Caller (Client 1)
        
    -   `client2_ip = "10.9.0.2"` → Receiver (Client 2)
        
2.  **Creates and Sends SIP Messages via UDP Port 5060**
    
    -   Uses `send_sip_message(dst_ip, sip_message)` to send messages over the network.
        
3.  **Simulates the SIP Call Flow:**
    
    -   **Client1 Registers** with the SIP server (`REGISTER`)
        
    -   **Client1 Calls Client2** (`INVITE`)
        
    -   **Client2 Rings** (`180 Ringing`)
        
    -   **Client2 Accepts the Call** (`200 OK`)
        
    -   **Client1 Acknowledges** (`ACK`)
        
    -   **Keeps Call Alive** (`ACK` messages every 5 seconds)

### sip_end_attack.py

1.  **Defines Network Parameters:**
    
    -   `client1_ip = "10.9.0.3"` → Legitimate Receiver
        
    -   `client2_ip = "10.9.0.2"` → Legitimate Caller (spoofed)
        
    -   `spoofed_ip = client2_ip` → Spoofed IP to impersonate Client2
        
    -   `sip_call_id = "222222@example.com"` → Call session identifier
        
    -   `sip_cseq = "2"` → Sequence number for SIP messages
        
2.  **Creates and Sends a SIP Message via UDP Port 5060**
    
    -   Uses `send_sip_message(dst_ip, spoofed_ip, sip_message)`
        
    -   Constructs and sends a malicious `BYE` message using Scapy
        
3.  **Simulates a SIP Call Termination Attack:**
    
    -   **Attacker Spoofs Client2's IP** to impersonate the caller
        
    -   **Sends a BYE Request** to Client1 (`BYE sip:client1_ip SIP/2.0`)
        
    -   **Client1 Thinks Client2 Ended the Call** and terminates the session
        

This script essentially disrupts an active SIP call by injecting a fake termination request, causing the call to drop unexpectedly.

## Bibliography

(References and resources used in the setup and attack demonstration.)