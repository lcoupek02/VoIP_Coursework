from scapy.all import *
import time
import threading
import sys

# Network Interface
interface = "eth0"

# SIP Server IP
sip_server_ip = "10.9.0.4"

# SIP Client 1 (Caller)
client1_ip = "10.9.0.3"
client1_sip = "sip:client1@10.9.0.3"

# SIP Client 2 (Receiver)
client2_ip = "10.9.0.2"
client2_sip = "sip:client2@10.9.0.2"

# Control Flag for ACKs
stop_ack_event = threading.Event()

# Function to send a SIP message
def send_sip_message(src_ip, dst_ip, sip_message):
    sip_packet = (
        IP(src=src_ip, dst=dst_ip) /
        UDP(sport=5060, dport=5060) /
        Raw(load=sip_message)
    )
    send(sip_packet, iface=interface, verbose=False)

# SIP Messages
sip_register_client1 = (
    f"REGISTER sip:{sip_server_ip} SIP/2.0\r\n"
    f"Via: SIP/2.0/UDP {client1_ip}:5060;branch=z9hG4bK-111111\r\n"
    f"To: <{client1_sip}>\r\n"
    f"From: <{client1_sip}>;tag=1234\r\n"
    f"Call-ID: 111111@example.com\r\n"
    f"CSeq: 1 REGISTER\r\n"
    f"Contact: <{client1_sip}>\r\n"
    f"Expires: 3600\r\n"
    f"User-Agent: Scapy-SIP\r\n"
    f"Content-Length: 0\r\n\r\n"
)

sip_register_client2 = (
    f"REGISTER sip:{sip_server_ip} SIP/2.0\r\n"
    f"Via: SIP/2.0/UDP {client2_ip}:5060;branch=z9hG4bK-111111\r\n"
    f"To: <{client2_sip}>\r\n"
    f"From: <{client2_sip}>;tag=1234\r\n"
    f"Call-ID: 22222@example.com\r\n"
    f"CSeq: 1 REGISTER\r\n"
    f"Contact: <{client2_sip}>\r\n"
    f"Expires: 3600\r\n"
    f"User-Agent: Scapy-SIP\r\n"
    f"Content-Length: 0\r\n\r\n"
)

sip_invite = (
    f"INVITE {client2_sip} SIP/2.0\r\n"
    f"Via: SIP/2.0/UDP {client1_ip}:5060;branch=z9hG4bK-222222\r\n"
    f"Max-Forwards: 70\r\n"
    f"To: <{client2_sip}>\r\n"
    f"From: <{client1_sip}>;tag=5678\r\n"
    f"Call-ID: 222222@example.com\r\n"
    f"CSeq: 1 INVITE\r\n"
    f"Contact: <{client1_sip}>\r\n"
    f"User-Agent: Scapy-SIP\r\n"
    f"Content-Length: 0\r\n\r\n"
)

sip_ringing = (
    f"SIP/2.0 180 Ringing\r\n"
    f"Via: SIP/2.0/UDP {client1_ip}:5060;branch=z9hG4bK-222222\r\n"
    f"To: <{client1_sip}>\r\n"
    f"From: <{client2_sip}>;tag=7777\r\n"
    f"Call-ID: 222222@example.com\r\n"
    f"CSeq: 1 INVITE\r\n"
    f"User-Agent: Scapy-SIP\r\n"
    f"Content-Length: 0\r\n\r\n"
)

sip_ok = (
    f"SIP/2.0 200 OK\r\n"
    f"Via: SIP/2.0/UDP {client1_ip}:5060;branch=z9hG4bK-222222\r\n"
    f"To: <{client1_sip}>\r\n"
    f"From: <{client2_sip}>;tag=7777\r\n"
    f"Call-ID: 222222@example.com\r\n"
    f"CSeq: 1 INVITE\r\n"
    f"User-Agent: Scapy-SIP\r\n"
    f"Content-Length: 0\r\n\r\n"
)

sip_ack = (
    f"ACK {client2_sip} SIP/2.0\r\n"
    f"Via: SIP/2.0/UDP {client1_ip}:5060;branch=z9hG4bK-333333\r\n"
    f"To: <{client2_sip}>;tag=7777\r\n"
    f"From: <{client1_sip}>;tag=1234\r\n"
    f"Call-ID: 222222@example.com\r\n"
    f"CSeq: 1 ACK\r\n"
    f"User-Agent: Scapy-SIP\r\n"
    f"Content-Length: 0\r\n\r\n"
)

def simulate_call():
    send_sip_message(client1_ip, sip_server_ip, sip_register_client1)
    send_sip_message(client2_ip, sip_server_ip, sip_register_client2)
    send_sip_message(client2_ip, client1_ip, sip_invite)
    send_sip_message(client1_ip, client2_ip, sip_ringing)
    send_sip_message(client1_ip, client2_ip, sip_ok)
    send_sip_message(client2_ip, client1_ip, sip_ack)
    print("[*] Call started")

# Function to sniff packets and detect BYE
def sniff_sip_packets():
    def process_packet(packet):
        if packet.haslayer(Raw):
            sip_payload = packet[Raw].load.decode(errors="ignore")
            if "BYE" in sip_payload:
                print("[*] BYE received! Stopping ACKs...")
                stop_ack_event.set()  # Signal the main thread to stop sending ACKs
                sys.exit(0)  # Exit the program after receiving BYE

    sniff(filter="udp port 5060", prn=process_packet, store=False, iface=interface)

# Function to keep the call alive with ACKs
def keep_call_alive():
    while not stop_ack_event.is_set():
        send_sip_message(client2_ip, client1_ip, sip_ack)
        print("[*] Sending ACK (Keep-alive)")
        time.sleep(5)
    print("[*] Call ended, ACKs stopped.")

# Start sniffing for BYE messages in a separate thread
sniffer_thread = threading.Thread(target=sniff_sip_packets, daemon=True)
sniffer_thread.start()

# Start call simulation and keep-alive process
simulate_call()
keep_call_alive()
